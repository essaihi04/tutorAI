"""(VPS) Refait les voix des diapositives où le modèle répète des mots (16 novembre 2026).
Chaque morceau (~300 caractères) est généré, transcrit par MoulSot v4, et refait (3 essais au plus) tant qu'il contient
une répétition absente du texte ; on garde l'essai avec le moins de répétitions.
Usage : python refaire_boucles.py LISTE.json   (LISTE : {"deck/id": "texte mixed"} ; accès : /tmp/essai_acces.json)
Écrit /srv/corpus_v4/voix_lot/att_<deck>/mixed/<id>.wav et met son hash dans cours.json (pour poser_en_ligne.py)."""
import hashlib, io, json, os, re, sys, time, wave
from concurrent.futures import ThreadPoolExecutor
import httpx

R = "/srv/corpus_v4/voix_lot"
liste = json.load(open(sys.argv[1], encoding="utf-8"))
A = json.load(open("/tmp/essai_acces.json"))
H = {"Authorization": "Bearer " + A["jeton"]}
sys.path.insert(0, "/opt/moalim/backend/kaggle_tts")
from texte_parle import parle
# règles de prononciation du dépôt (le kernel d'essai peut tourner avec une version plus ancienne de texte_parle.py)
sys.path.insert(0, "/srv/corpus_v4/voix_lot/_stt_tous")
try:
    from texte_parle_depot import prononciation as pron_depot
except ImportError:
    pron_depot = lambda p: p


def toks(s):
    return re.findall(r"[\w'’]+", parle(s).lower())


def reps(t, maxn=5):
    out = []
    for n in range(1, maxn + 1):
        i = 0
        while i + 2 * n <= len(t):
            g = t[i:i + n]
            k = 1
            while t[i + k * n:i + (k + 1) * n] == g:
                k += 1
            if k >= (3 if n == 1 else 2) and len(" ".join(g)) > 2:
                out.append(" ".join(g))
                i += k * n
            else:
                i += 1
    return out


def boucles(stt, texte):
    deja = set(reps(toks(texte)))
    return [g for g in reps(toks(stt)) if g not in deja]


def fin_dite(stt, texte):
    """Au moins la moitié des 10 derniers mots du texte se retrouvent (à peu près) dans la transcription."""
    import difflib
    fin = [x for x in toks(texte) if len(x) > 2][-10:]
    vus = [x for x in toks(stt) if len(x) > 2]
    if not fin:
        return True
    ok = sum(1 for x in fin if x in vus or difflib.get_close_matches(x, vus, 1, 0.75))
    return ok >= len(fin) / 2


def defauts(stt, texte):
    return boucles(stt, texte) + ([] if fin_dite(stt, texte) else ["FIN MANQUANTE"])


def morceaux(texte):
    if len(texte) <= 330:
        return [texte]
    coupes = [mt.end() for mt in re.finditer(r"[.!?؟:]\s+", texte)]
    n = -(-len(texte) // 320)
    bornes = sorted({min(coupes, key=lambda c: abs(c - len(texte) * k / n)) for k in range(1, n)}) if coupes else []
    return [x for x in (texte[a:b].strip() for a, b in zip([0] + bornes, bornes + [len(texte)])) if x]


def appel(c, chemin, **kw):
    for essai in range(8):
        try:
            r = c.post(A["url"] + chemin, headers=H, timeout=300, **kw)
            if r.status_code == 200:
                return r
            print("  ", chemin, r.status_code, r.text[:60], flush=True)
        except Exception as e:
            print("  ", chemin, repr(e)[:60], flush=True)
        time.sleep(20)
    raise RuntimeError(chemin + " KO")


rapport = {}


def une(c, cle, texte):
    deck, *typ, i = cle.split("/")
    typ = typ[0] if typ else "mixed"
    wavs, notes = [], []
    for x in morceaux(texte.strip()):
        meilleur = None
        for essai in range(3):
            w = appel(c, "/tts", json={"texte": pron_depot(x), "langue": "ma", "pas_flow": 10}).content
            s = appel(c, "/stt", params={"langue": "ma"}, content=w).json().get("texte", "")
            b = defauts(s, x)
            if meilleur is None or len(b) < len(meilleur[1]):
                meilleur = (w, b, s)
            if not b:
                break
        wavs.append(meilleur[0])
        notes.append({"morceau": x[:60], "essais": essai + 1, "reste": meilleur[1], "stt": meilleur[2]})
    d = f"{R}/att_{deck}/{typ}"
    os.makedirs(d, exist_ok=True)
    with wave.open(io.BytesIO(wavs[0])) as w0:
        pr = w0.getparams()
    tmp = f"{d}/{i}.wav.part"
    with wave.open(tmp, "wb") as w:
        w.setnchannels(pr.nchannels); w.setsampwidth(pr.sampwidth); w.setframerate(pr.framerate)
        for k, b in enumerate(wavs):
            if k:
                w.writeframes(b"\x00" * int(0.3 * pr.framerate) * pr.sampwidth * pr.nchannels)
            with wave.open(io.BytesIO(b)) as wi:
                w.writeframes(wi.readframes(wi.getnframes()))
    os.replace(tmp, f"{d}/{i}.wav")
    f = f"{d}/cours.json"
    idx = json.load(open(f)) if os.path.isfile(f) else []
    idx = [e for e in idx if e["id"] != i] + [{"id": i, "hash": hashlib.sha256(texte.encode("utf-8")).hexdigest()}]
    json.dump(idx, open(f, "w"), ensure_ascii=False, indent=1)
    rapport[cle] = notes
    print("ok", cle, [n["reste"] for n in notes], flush=True)


import threading
verrou = threading.Lock()
with httpx.Client() as c, ThreadPoolExecutor(2) as pool:
    def tache(kv):
        try:
            une(c, *kv)
        except Exception as e:
            print("ÉCHEC", kv[0], repr(e)[:120], flush=True)
        with verrou:
            json.dump(rapport, open(f"{R}/_rapport_boucles.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    list(pool.map(tache, liste.items()))
print("FIN", len(rapport), "refaites", flush=True)
