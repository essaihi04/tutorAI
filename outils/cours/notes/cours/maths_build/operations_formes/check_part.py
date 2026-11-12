"""Contrôle d'une partie du cours : python outils/cours/notes/cours/maths_build/operations_formes/check_part.py p2   (depuis la racine du dépôt)
Vérifie : mots de pointage/démonstration présents (outils.ERREURS), voix sans chiffre ni symbole (règles de blocs.py),
mots hors cadre, moments et repères cités existants (contrat pour les pages, CALC pour calculs.html), questions bien formées."""
import importlib, json, re, sys
from pathlib import Path
ICI = Path(__file__).resolve().parent
sys.path.insert(0, str(ICI))
sys.path.insert(0, str(ICI.parents[1] / "methode_blocs"))
import outils
from blocs import controle_parole

mod = importlib.import_module(sys.argv[1])
slides = [s for v in vars(mod).values() if isinstance(v, list) for s in v if isinstance(s, dict) and "slide_type" in s]
cadre = json.loads(Path("backend/data/curriculum/cadre_reference_2bac_pc.json").read_text(encoding="utf-8"))["chapitres"]["operations_formes"]
HC = [m.lower() for m in cadre["hors_cadre"]["mots"]]
contrat = (ICI / "CONTRAT_SIMULATIONS.md").read_text(encoding="utf-8")
SIMDIR = Path("frontend/public/media/simulations/maths/operations-formes-tableau")
pb = list(outils.ERREURS)

def textes(o):
    if isinstance(o, dict):
        for v in o.values(): yield from textes(v)
    elif isinstance(o, list):
        for v in o: yield from textes(v)
    elif isinstance(o, str): yield o

def moments_page(page, vue):
    """Noms entre backticks dans le contrat pour cette vue + noms marqués dans la page (K.marque('…'), repere('…'))."""
    noms = set(re.findall(r"`([a-z0-9_]+)`", contrat))
    f = SIMDIR / page
    if f.exists():
        t = f.read_text(encoding="utf-8")
        noms |= set(re.findall(r"marque\(\s*'([a-z0-9_]+)'", t)) | set(re.findall(r"repere\(\s*'([a-z0-9_]+)'", t))
        noms |= set(re.findall(r"""['"]([a-z0-9_]+)['"]""", t))
    return noms

for s in slides:
    sid = s["id"]
    for k in ("fr", "mixed"):
        for p in controle_parole(s["speech_text"][k]):
            pb.append(f"{sid} speech {k} : {p}")
    for o in [s.get("question")] + list(s.get("exercises") or []):
        if not o: continue
        if o.get("demonstration"):
            for p in controle_parole(o["demonstration"]["parole"]):
                pb.append(f"{sid} démonstration : {p}")
        opts = o.get("options") or o.get("choices")
        if o.get("type") == "qcm" and (not opts or not isinstance(o.get("correct"), int) or not 0 <= o["correct"] < len(opts)):
            pb.append(f"{sid} : QCM mal formé « {o.get('prompt', '')[:40]} »")
    tout = " ".join(textes(s)).lower()
    for m in HC:
        if m in tout: pb.append(f"{sid} : mot hors cadre « {m} »")
    vis = s.get("visual") or {}
    url = vis.get("url", "")
    pt = s["concentration"].get("pointage", [])
    if "calculs.html" in url:
        vue = url.split("vue=")[1]
        d = outils.CALCULS.get(vue, {"lignes": []})
        ms = {l.get("m") for l in d["lignes"]} | {l["r"][0] for l in d["lignes"] if l.get("r")}
    elif url:
        page = url.split("operations-formes-tableau/")[1].split("?")[0]
        ms = moments_page(page, None)
    else:
        ms = None
    for p in pt:
        nom = p.get("parametres", {}).get("moment") or p.get("repere")
        if nom and ms is not None and nom not in ms:
            pb.append(f"{sid} : moment/repère inconnu « {nom} » ({url.split('/')[-1]})")
    if s.get("question") and not s["question"].get("prompt"): pb.append(f"{sid} : question sans énoncé")
print(len(slides), "diapositives :", ", ".join(s["id"] for s in slides))
print("\n".join(pb) if pb else "partie : OK")
