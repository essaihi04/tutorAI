"""Met à jour backend/data/curriculum/architecture/<deck>_voix.json après la 2ᵉ passe (18 novembre 2026) des cours RC, RL,
RLC et ch9 : les pistes sans voix de la copie en attente, moins celles qui n'avaient déjà pas de voix dans le cours en
ligne (gardées à part, pour mémoire). Chaque fichier garde son format et ses ids (RC, RL, RLC : backend/scripts/
lister_voix_attente.py ; ch9 : scripts/voix/pistes_cours.py, comme scripts/logique/lister_voix.py).
« passe » : 1 = 1ʳᵉ passe de la logique, 2 = ajoutée ou réécrite par la 2ᵉ passe (exercice joué pas à pas, mots).
Usage : python -X utf8 scripts/logique/voix_pas_a_pas.py
"""
import hashlib, json, sys
from pathlib import Path

R = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(R / "backend/scripts"), str(R / "scripts/voix"), str(R / "backend/kaggle_tts")]
import lister_voix_attente as LVA  # noqa: E402
from pistes_cours import pistes as pistes_cours  # noqa: E402

ARCHI = R / "backend/data/curriculum/architecture"
REECRITES = {"rc_m5_observer", "rl_m5_observer", "lc_r5_observer", "tl_o1_carte", "tl_r6_classer", "tl_f8_variable"}
A_ECOUTER = {
    "phys_ch6_dipole_RC": [],
    "phys_ch7_dipole_RL": ["anri (henry, règle de prononciation : unité du programme)"],
    "phys_ch8_circuit_RLC": ["anri (henry)", "pseudo-période (terme du programme)"],
    "phys_ch9_transformations_lentes_rapides": ["diiode", "iodure", "trempe", "glacée", "chlorure (AgCl, nom d'espèce)",
                                                "précipitation (nom du choix écrit)"],
}


def charger(p):
    return json.loads(p.read_text(encoding="utf-8"))


def passe(i):
    base = i.split("/")[0].split("__")[0]
    base = base[len("enonce_"):] if base.startswith("enonce_") else base
    base = base[len("obs_"):] if base.startswith("obs_") else base
    return 2 if ("_np" in base or any(base.startswith(x) for x in REECRITES)) else 1


def sans_voix_cours(m):
    """Schéma de scripts/logique/lister_voix.py (ch9)."""
    H = lambda t: hashlib.sha256(t.encode("utf-8")).hexdigest()
    D = {s["id"]: s for a in m["activities"] for s in a["slides"]}
    out = []
    for d, i, t, poser in pistes_cours(m):
        if d == "mixed":
            a = (D[i].get("audio") or {}).get("mixed") or {}
            if not (a.get("url") and a.get("speech_hash") == H(t)):
                out.append({"type": "diapositive", "id": i, "texte": t})
            continue
        obj = next((c.cell_contents for c in (poser.__closure__ or ()) if isinstance(c.cell_contents, dict)), {})
        if not obj.get("enonce_audio" if i.startswith("enonce_") else "audio"):
            out.append({"type": {"reponses": "enonce" if i.startswith("enonce_") else "reaction", "demos": "demonstration"}[d], "id": i, "texte": t})
    for s in D.values():
        o = (s.get("concentration") or {}).get("observation")
        if not o:
            continue
        b = f"enonce_obs_{s['id']}"
        if not o.get("enonce_audio"):
            out.append({"type": "observation", "id": f"{b}_q", "texte": o.get("enonce_dit") or o["enonce"]})
        for k, x in enumerate(o.get("indices") or []):
            if not x.get("audio"):
                out.append({"type": "observation", "id": f"{b}_i{k}", "texte": x.get("dit") or x["texte"]})
        for k, x in enumerate(o.get("retours") or []):
            if not x.get("audio"):
                out.append({"type": "observation", "id": f"{b}_r{k}", "texte": x["parole"]})
        so = o.get("solution") or {}
        if so.get("parole") and not so.get("audio"):
            out.append({"type": "observation", "id": f"{b}_s", "texte": so["parole"]})
    return out


for deck in A_ECOUTER:
    att = charger(R / f"backend/data/courses/en_attente/{deck}.json")
    lig = charger(R / f"backend/data/courses/{deck}.json")
    f = ARCHI / f"{deck}_voix.json"
    brut = f.read_text(encoding="utf-8")
    retrait = len(brut.split("\n")[1]) - len(brut.split("\n")[1].lstrip())
    v = json.loads(brut)
    lister = sans_voix_cours if deck.endswith("rapides") else LVA.pistes
    # déjà sans voix en ligne : même texte (les ids des blocs suivent la place du bloc, qui a bougé avec les séances)
    deja = {p["texte"] for p in lister(lig)}
    pis = []
    for p in lister(att):
        if p["texte"] in deja:
            continue
        p["passe"] = passe(p["id"])
        pis.append(p)
    v["date"] = "2026-11-18"
    v["pistes"] = pis
    v["deuxieme_passe"] = sum(p["passe"] == 2 for p in pis)
    if "nombre" in v:
        v["nombre"] = len(pis)
        v["nouvelles"] = len(pis)
    ancien = v.get("a_ecouter") or []
    v["a_ecouter"] = sorted(set(ancien) | set(A_ECOUTER[deck]))
    cle = "_note" if "_note" in v else "note"
    note = v.get(cle, "")
    ajout = (" 2ᵉ passe (18/11/2026, scripts/logique/pas_a_pas_ch6_9.py) : l'exercice du national joué pas à pas (diapositives *_np*) "
             "et les pistes réécrites pour leurs mots rares ont « passe » = 2 ; la liste est recalculée par scripts/logique/voix_pas_a_pas.py "
             "(pistes sans voix de la copie en attente, moins celles qui n'avaient déjà pas de voix dans le cours en ligne).")
    v[cle] = note.split(" 2ᵉ passe (18/11/2026")[0] + ajout
    f.write_text(json.dumps(v, ensure_ascii=False, indent=retrait or 1) + "\n", encoding="utf-8")
    from collections import Counter
    print(deck, len(pis), "pistes ;", v["deuxieme_passe"], "de la 2ᵉ passe ;", dict(Counter(p["type"] for p in pis)))
