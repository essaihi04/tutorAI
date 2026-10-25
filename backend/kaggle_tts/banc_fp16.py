"""Banc fp32 / fp16 de la voix du prof (modèle Academy v3, voix Amine) sur T4.

Trois modes, mêmes phrases, mêmes graines :
  fp32        référence (ce que sert academy-tts-direct aujourd'hui)
  fp16_t3     autocast fp16 sur le seul T3 (le transformeur qui génère les jetons de parole)
  fp16_tout   autocast fp16 sur toute la génération (T3 + S3Gen)

Mesures : temps de calcul / durée audio (vitesse), temps du premier morceau
(~45 caractères, ce qui fixe le premier son en séance), et intelligibilité
par CER : transcription MoulSot (atlasia/moulsot.v0.3) comparée au texte.
Sorties : /kaggle/working/banc/<mode>/<id>.wav et banc.json.
Poussé par `python -m scripts.kaggle_tts banc` (kernel séparé : ne gêne pas la voix en service).
"""
import base64, glob, json, os, re, subprocess, sys, threading, time, unicodedata

T0 = time.time()
W, WORK = "/kaggle/working", "/tmp/academy"
os.makedirs(WORK, exist_ok=True)
REF_B64 = "__REF_B64__"
MODELE = "__MODELE__"


def say(*a):
    print(f"[{time.time() - T0:6.1f}s]", *a, flush=True)


def sh(cmd):
    r = subprocess.run(cmd, shell=True, capture_output=True, text=True, executable="/bin/bash")
    if r.returncode:
        say("$", cmd[:90], "->", r.returncode, (r.stdout + r.stderr)[-400:])
    return r


PHRASES = [
    ("d1", "ma", "دابا غادي نشوفو الشحن ديال المكثف."),
    ("d2", "ma", "شوف معايا، التوتر كيطلع بشوية بشوية حتى كيوصل لE."),
    ("d3", "ma", "إذن، الثابتة ديال الزمن هي R ضرب C."),
    ("d4", "ma", "واش فهمتي علاش التيار كينقص مع الوقت؟"),
    ("d5", "ma", "مزيان بزاف، الجواب ديالك صحيح، نكملو."),
    ("d6", "ma", "رد البال، هاد الخطأ كيديروه بزاف ديال التلاميذ فالامتحان."),
    ("f1", "fr", "Donc retiens bien : la constante de temps est égale à R fois C."),
    ("f2", "fr", "Quand on ferme l'interrupteur, le condensateur se charge progressivement."),
    ("f3", "fr", "Très bien, ta réponse est juste. On passe à la question suivante."),
    ("f4", "fr", "Qu'est-ce qui se passe pour la tension aux bornes du condensateur ?"),
    ("f5", "fr", "Attention, l'intensité du courant diminue au cours de la charge."),
    ("f6", "fr", "Je relis : à t égal tau, la tension vaut soixante-trois pour cent de E."),
]
PREMIER = ("p1", "fr", "Bonjour, aujourd'hui on étudie le dipôle RC,")
MODES = ["fp32", "fp16_t3", "fp16_tout"]

# ── installation (même socle que le kernel direct) ──
SOCLE = next((os.path.dirname(p) for p in glob.glob("/kaggle/input/**/socle.json", recursive=True)), None)
say("socle", SOCLE)
if SOCLE and os.path.exists(f"{SOCLE}/site.tar"):
    os.makedirs(f"{WORK}/site", exist_ok=True)
    sh(f"tar -xf '{SOCLE}/site.tar' -C {WORK}/site")
    sys.path.insert(0, f"{WORK}/site")
else:
    sh("pip -q install 'transformers==4.57.6' 'tokenizers==0.22.1' 'accelerate==1.12.0' 'huggingface-hub==0.36.0' "
       "resemble-perth conformer diffusers s3tokenizer omegaconf einops safetensors")
sh(f"cp -r '{SOCLE}/lahgtna-chatterbox' {WORK}/" if SOCLE else
   f"git clone -q --depth 1 https://github.com/Oddadmix/lahgtna-chatterbox.git {WORK}/lahgtna-chatterbox")
sys.path.insert(0, f"{WORK}/lahgtna-chatterbox/src")
os.makedirs(f"{WORK}/base", exist_ok=True)
fin = [p for p in glob.glob("/kaggle/input/**/t3_mtl23ls_v2.safetensors", recursive=True) if MODELE in p][0]
sh(f"cp '{fin}' {WORK}/base/t3_mtl23ls_v2.safetensors")
for f in ["ve.pt", "s3gen.pt", "grapheme_mtl_merged_expanded_v1.json", "conds.pt", "Cangjie5_TC.json"]:
    sh(f"cp '{SOCLE}/lahgtna_base/{f}' {WORK}/base/")
REF = f"{WORK}/reference_amine.flac"
open(REF, "wb").write(base64.b64decode(REF_B64))
say("installé")

import numpy as np  # noqa: E402
import torch  # noqa: E402
import soundfile as sf  # noqa: E402

AR = re.compile("[؀-ۿ]")


def generer(m, k, mode, texte, langue, graine):
    lg = "pl" if (langue != "fr" and AR.search(texte)) else "fr"
    torch.manual_seed(graine)
    kw = dict(language_id=lg, exaggeration=0.6, temperature=0.75, cfg_weight=0.35)
    torch.cuda.synchronize(k)
    t = time.time()
    with torch.inference_mode():
        if mode == "fp16_tout":
            with torch.autocast("cuda", dtype=torch.float16):
                w = m.generate(texte, **kw)
        else:
            w = m.generate(texte, **kw)
    torch.cuda.synchronize(k)
    return w.float().cpu().numpy()[0], time.time() - t


def banc(k, modes, res):
    torch.cuda.set_device(k)
    from chatterbox.mtl_tts import ChatterboxMultilingualTTS
    m = ChatterboxMultilingualTTS.from_local(f"{WORK}/base", device=f"cuda:{k}")
    m.t3.to(f"cuda:{k}").eval()
    try:
        m.t3.tfmr.set_attn_implementation("eager")
    except Exception:
        pass
    m.t3.tfmr.config._attn_implementation = "eager"
    m.prepare_conditionals(REF, exaggeration=0.6)
    inference_t3 = m.t3.inference
    for mode in modes:
        if mode == "fp16_t3":
            def t3_fp16(*a, **kw):
                with torch.autocast("cuda", dtype=torch.float16):
                    return inference_t3(*a, **kw)
            m.t3.inference = t3_fp16
        else:
            m.t3.inference = inference_t3
        os.makedirs(f"{W}/banc/{mode}", exist_ok=True)
        try:
            generer(m, k, mode, "Bonjour.", "fr", 0)          # chauffe
            lignes = []
            for i, (nom, langue, texte) in enumerate([PREMIER] + PHRASES):
                w, dt = generer(m, k, mode, texte, langue, 1000 + i)
                d = len(w) / m.sr
                sf.write(f"{W}/banc/{mode}/{nom}.wav", w, m.sr)
                lignes.append({"nom": nom, "langue": langue, "texte": texte, "calcul_s": round(dt, 2),
                               "audio_s": round(d, 2), "vitesse": round(dt / max(d, 0.01), 2),
                               "nan": bool(np.isnan(w).any()), "crete": round(float(np.abs(w).max()), 3)})
                say(mode, nom, f"{dt:.2f} s pour {d:.1f} s")
            res[mode] = lignes
        except Exception as e:
            say(mode, "ÉCHEC", repr(e)[:300])
            res[mode] = {"echec": repr(e)[:300]}
        torch.cuda.empty_cache()
    del m
    torch.cuda.empty_cache()


RES = {}
n = torch.cuda.device_count()
# Une seule carte, modes à la suite : deux fils Python en parallèle se
# disputent le verrou de l'interpréteur et faussent la comparaison.
plan = {0: MODES}
fils = [threading.Thread(target=banc, args=(k, modes, RES)) for k, modes in plan.items()]
for f in fils:
    f.start()
for f in fils:
    f.join()
say("génération finie sur", n, "carte(s)")

# ── intelligibilité : MoulSot, isolé dans son propre site (autres versions) ──
sh("pip -q install --no-deps --target /tmp/qa transformers==4.57.6 tokenizers==0.22.1 accelerate==1.12.0 "
   "huggingface-hub==0.36.0 qwen-asr==0.0.6 qwen-omni-utils soynlp==0.0.493")
os.makedirs("/tmp/qa/nagisa", exist_ok=True)
open("/tmp/qa/nagisa/__init__.py", "w").close()
json.dump({"modes": [m for m in MODES if isinstance(RES.get(m), list)],
           "items": [(nom, langue, texte) for nom, langue, texte in [PREMIER] + PHRASES]},
          open(f"{WORK}/items.json", "w"), ensure_ascii=False)
open(f"{WORK}/cer.py", "w").write(r'''
import sys, json, os, re, unicodedata, torch
sys.path.insert(0, "/tmp/qa")
from qwen_asr import Qwen3ASRModel
asr = Qwen3ASRModel.from_pretrained("atlasia/moulsot.v0.3", dtype=torch.float16, device_map="cuda", max_new_tokens=256)
d = json.load(open(sys.argv[1]))
def norm(s):
    s = unicodedata.normalize("NFKC", str(s).lower()); s = re.sub(r"[ً-ْـ]", "", s)
    for a, b in (("أ","ا"),("إ","ا"),("آ","ا"),("ة","ه"),("ى","ي")): s = s.replace(a, b)
    return re.sub(r"[^\w]", "", s)
def cer(a, b):
    a, b = norm(a), norm(b)
    if not a: return 1.0
    p = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        q, p[0] = p[0], i
        for j, cb in enumerate(b, 1):
            q, p[j] = p[j], min(p[j] + 1, p[j - 1] + 1, q + (ca != cb))
    return min(1.0, p[len(b)] / len(a))
out = {}
for mode in d["modes"]:
    out[mode] = {}
    for nom, langue, texte in d["items"]:
        f = f"/kaggle/working/banc/{mode}/{nom}.wav"
        if not os.path.exists(f): continue
        hyp = asr.transcribe(audio=f, language="French" if langue == "fr" else "Arabic")[0].text
        out[mode][nom] = {"cer": round(cer(texte, hyp), 3), "hyp": hyp}
json.dump(out, open("/tmp/academy/cer.json", "w"), ensure_ascii=False)
print("ok")
''')
r = sh(f"python {WORK}/cer.py {WORK}/items.json")
cer = json.load(open(f"{WORK}/cer.json")) if os.path.exists(f"{WORK}/cer.json") else {}

# ── bilan ──
bilan = {}
for mode in MODES:
    lignes = RES.get(mode)
    if not isinstance(lignes, list):
        bilan[mode] = RES.get(mode)
        continue
    for l in lignes:
        l.update(cer.get(mode, {}).get(l["nom"], {}))
    corps = [l for l in lignes if l["nom"] != "p1"]
    moy = lambda cle, ls: round(sum(l.get(cle, 1.0) for l in ls) / max(len(ls), 1), 3)
    bilan[mode] = {
        "vitesse_moyenne": round(sum(l["calcul_s"] for l in corps) / sum(l["audio_s"] for l in corps), 3),
        "premier_morceau_s": next(l["calcul_s"] for l in lignes if l["nom"] == "p1"),
        "cer_darija": moy("cer", [l for l in corps if l["langue"] == "ma"]),
        "cer_francais": moy("cer", [l for l in corps if l["langue"] == "fr"]),
        "nan": any(l["nan"] for l in lignes),
        "detail": lignes,
    }
json.dump(bilan, open(f"{W}/banc.json", "w"), ensure_ascii=False, indent=1)
for mode, b in bilan.items():
    if isinstance(b, dict) and "vitesse_moyenne" in b:
        say(f"BILAN {mode}: vitesse {b['vitesse_moyenne']}x, premier morceau {b['premier_morceau_s']} s, "
            f"CER darija {b['cer_darija']}, CER fr {b['cer_francais']}, nan={b['nan']}")
    else:
        say("BILAN", mode, b)
say("TERMINÉ")
