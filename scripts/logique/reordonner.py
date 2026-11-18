"""Réordonne un cours en attente selon une architecture (skill logique-de-cours, 18 novembre 2026).

Usage : python -X utf8 scripts/logique/reordonner.py <spec.json>
spec = {
  "deck": "<id>",
  "parties": [{"id", "title", "phase", "slides": [ids…]}],        # ordre nouveau ; une diapo absente est retirée
  "seances": [{"id", "titre", "blocs": [{"id", "titre", "slides": [ids…]}]}],
  "nouvelles": {"<id>": {diapositive complète}},                    # diapositives nouvelles (déjà écrites)
  "retirees": {"<id>": "raison"}
}
- Une diapositive gardée n'est pas touchée (id, texte, voix).
- Un bloc qui garde son id et ses diapositives garde son cahier, retrouver, exercice et figures ; un bloc nouveau prend le cahier de ses
  diapositives et le retrouver / l'exercice du bloc ancien qui portait le plus de ses diapositives.
- competences[].slide_ids suivent l'ordre nouveau (diapositives retirées enlevées, nouvelles ajoutées par competence_ids).
- duration_minutes de chaque partie et estimated_minutes : voix (enregistrée, ou 14 caractères/s) × le rapport
  minutes / voix du cours avant.
"""
import json, os, sys

RACINE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")


def duree_s(s):
    au = (s.get("audio") or {}).get("mixed") or {}
    if au.get("duration_ms"):
        return au["duration_ms"] / 1000
    return len((s.get("speech_text") or {}).get("mixed", "")) / 14


def main(chemin_spec):
    spec = json.load(open(chemin_spec, encoding="utf-8"))
    chemin = os.path.join(RACINE, "backend/data/courses/en_attente", spec["deck"] + ".json")
    d = json.load(open(chemin, encoding="utf-8"))
    anciennes = {s["id"]: s for a in d["activities"] for s in a["slides"]}
    toutes = dict(anciennes)
    toutes.update(spec.get("nouvelles") or {})
    ordre = [i for p in spec["parties"] for i in p["slides"]]
    assert len(ordre) == len(set(ordre)), "diapositive en double"
    manquantes = [i for i in ordre if i not in toutes]
    assert not manquantes, manquantes
    retirees = [i for i in anciennes if i not in ordre]
    non_justifiees = [i for i in retirees if i not in (spec.get("retirees") or {})]
    assert not non_justifiees, f"retirées sans raison : {non_justifiees}"
    dans_blocs = [i for se in spec["seances"] for b in se["blocs"] for i in b["slides"]]
    assert dans_blocs == ordre, "les blocs ne suivent pas l'ordre des parties"

    anciennes_parties = {a["id"]: a for a in d["activities"]}
    # minutes par seconde de voix : le rapport du cours avant (temps de regarder, de répondre, d'écrire)
    rapport = d["estimated_minutes"] / max(1, sum(duree_s(s) for s in anciennes.values()))
    acts = []
    for p in spec["parties"]:
        base = {k: v for k, v in anciennes_parties.get(p["id"], {}).items() if k != "slides"}
        base.update({k: v for k, v in p.items() if k != "slides"})
        base["slides"] = [toutes[i] for i in p["slides"]]
        base["duration_minutes"] = max(3, round(sum(duree_s(s) for s in base["slides"]) * rapport))
        acts.append(base)
    d["activities"] = acts

    anciens_blocs = {b["id"]: b for se in d["seances"] for b in se["blocs"]}
    seances = []
    for se in spec["seances"]:
        blocs = []
        for b in se["blocs"]:
            if b["id"] in anciens_blocs and anciens_blocs[b["id"]]["slide_ids"] == list(b["slides"]):
                nb = dict(anciens_blocs[b["id"]])
            else:
                nb = {"id": b["id"]}
                meilleur = max(anciens_blocs.values(), key=lambda ob: len(set(ob["slide_ids"]) & set(b["slides"])))
                for k in ("retrouver", "exercice"):
                    if k in meilleur:
                        nb[k] = meilleur[k]
                nb["cahier"] = [{"texte": (toutes[i].get("concentration") or {}).get("cahier")}
                                for i in b["slides"] if (toutes[i].get("concentration") or {}).get("cahier")]
                figs = [f for i in b["slides"] for f in ((toutes[i].get("concentration") or {}).get("cahier_figures") or [])]
                if figs:
                    nb["cahier_figures"] = figs[:2]
            if "cahier" in b:
                nb["cahier"] = [{"texte": t} for t in b["cahier"]]
            nb["titre"] = b["titre"]
            nb["slide_ids"] = list(b["slides"])
            blocs.append(nb)
        seances.append({"id": se["id"], "titre": se["titre"], "blocs": blocs})
    d["seances"] = seances

    rang = {i: n for n, i in enumerate(ordre)}
    for c in d["competences"]:
        ids = [i for i in c["slide_ids"] if i in rang]
        ids += [i for i in ordre if c["id"] in (toutes[i].get("competence_ids") or []) and i not in ids]
        c["slide_ids"] = sorted(set(ids), key=rang.get)
    d["competences"] = [c for c in d["competences"] if c["slide_ids"]]
    d["estimated_minutes"] = sum(a["duration_minutes"] for a in acts)
    open(chemin, "w", encoding="utf-8").write(json.dumps(d, ensure_ascii=False, indent=2) + "\n")
    print(f"{spec['deck']} : {len(ordre)} diapositives ({len(retirees)} retirées, "
          f"{len(spec.get('nouvelles') or {})} nouvelles), {len(seances)} séances, "
          f"{sum(len(se['blocs']) for se in seances)} blocs, {d['estimated_minutes']} min")


if __name__ == "__main__":
    main(sys.argv[1])
