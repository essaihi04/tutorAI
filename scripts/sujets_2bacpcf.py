"""Construit les deux examens de 30 min du lien /2bacpcf à partir des exercices EXISTANTS (aucune voix nouvelle).

Chaque examen = deux exercices de 15 min (un par chapitre) de `frontend/public/media/exercices/`, repris tels quels :
énoncé, figures, données, questions, réponse attendue, correction rédigée et ses voix (intro_audio, texte_audio,
correction.audio). Le barème de chaque question vient de `pointsDe` (longueur de la correction), ramené à 20 points.
Écrit `frontend/src/publication/bac2pcf/sujets.ts`.

Usage : python -I scripts/sujets_2bacpcf.py [dossier_des_exercices]
"""
import json
import sys
from pathlib import Path

RACINE = Path(__file__).resolve().parents[1]
SOURCE = Path(sys.argv[1]) if len(sys.argv) > 1 else RACINE / "frontend/public/media/exercices"
CIBLE = RACINE / "frontend/src/publication/bac2pcf/sujets.ts"

EXAMENS = {
    "physique": {"titre": "Examen de révision — Physique : ondes lumineuses et décroissance radioactive",
                 "programme": "les ondes lumineuses (diffraction, écart angulaire) ; la décroissance radioactive (demi-vie, loi de décroissance)",
                 "matiere": "Physique", "exercices": ["phys_ex_ch3_fente_2", "phys_ex_ch4_demivie_2"]},
    "chimie": {"titre": "Examen de révision — Chimie : transformations dans les deux sens et état d'équilibre",
               "programme": "les transformations dans les deux sens (pH, taux d'avancement final) ; l'état d'équilibre (quotient de réaction, constante K)",
               "matiere": "Chimie", "exercices": ["phys_ex_ch11_deux_sens_1", "phys_ex_ch12_etat_equilibre_2"]},
}
VARIANTES = {"j⁻¹": ["j⁻¹", "j-1", "jour⁻¹", "jour-1", "/j", "/jour", "j^-1"], "mol/L": ["mol/l", "mol.l", "mol·l", "mol l"],
             "noyaux": ["noyau", ""], "jours": ["jour", "j"], "rad": ["rad"], "cm": ["cm"], "mol": ["mol"]}


def points_de(q):
    """comme `pointsDe` (frontend/src/components/exercice/types.ts)"""
    if isinstance(q.get("points"), (int, float)) and q["points"] > 0:
        return q["points"]
    n = len(q.get("correction", {}).get("lignes") or []) or 1
    return 0.5 if n <= 2 else 0.75 if n == 3 else 1 if n <= 5 else 1.25


def convertir(nom, conf):
    parties, voix = [], {}
    brut = []
    for k, ex_id in enumerate(conf["exercices"], 1):
        ex = json.loads((SOURCE / f"{ex_id}.json").read_text(encoding="utf-8"))
        e = ex["enonce"]
        pid = f"E{k}"
        if e.get("intro_audio"):
            voix[f"partie/{pid}"] = e["intro_audio"]
        qs = []
        for q in e["questions"]:
            qid = f"{k}-{q['id']}"
            r = q["reponse"]
            lignes = [l["texte"] for l in q["correction"]["lignes"]]
            base = {"id": qid, "texte": q["texte"], "points": points_de(q)}
            if r["type"] == "valeur" and r.get("valeur") is not None:
                u = r.get("unite") or ""
                qs.append({**base, "genre": "valeur", "grandeur": r.get("grandeur") or "résultat", "valeur": r["valeur"],
                           "unites": VARIANTES.get(u, [u]) if u else [""], "tolerance": r.get("tolerance") or 0.03, "correction": lignes})
            else:
                qs.append({**base, "genre": "redaction", "attendu": r.get("attendu") or " ".join(lignes),
                           "elements": lignes[:8], "correction": lignes})
            if q.get("texte_audio"):
                voix[f"question/{qid}"] = q["texte_audio"]
            if q["correction"].get("audio"):
                voix[f"correction/{qid}"] = q["correction"]["audio"]
        brut.append((pid, ex, e, qs))
    total = sum(q["points"] for _, _, _, qs in brut for q in qs)
    for pid, ex, e, qs in brut:
        for q in qs:   # ramené à 20 points, au quart de point
            q["points"] = max(0.25, round(q["points"] * 20 / total * 4) / 4)
        parties.append({"id": pid, "court": f"Ex. {pid[1:]}", "titre": f"Exercice {pid[1:]} — {ex['titre']}",
                        "minutes": int(ex.get("duree_min") or 15), "intro": e.get("intro", ""), "figures": e.get("figures") or [],
                        "donnees": e.get("donnees") or [], "questions": qs})
    # l'arrondi au quart : on ajuste la dernière question pour tomber pile sur 20
    somme = sum(q["points"] for pa in parties for q in pa["questions"])
    parties[-1]["questions"][-1]["points"] = round((parties[-1]["questions"][-1]["points"] + 20 - somme) * 4) / 4
    sujet = {"titre": conf["titre"], "niveau": "2ᵉ Bac PC BIOF", "matiere": conf["matiere"],
             "minutes": sum(pa["minutes"] for pa in parties), "programme": conf["programme"],
             "consigne": "Révise en conditions d'examen : réponds à chaque question comme sur ta copie. Dès que tu réponds, "
                         "tu as ta note sur le barème et la correction expliquée, avec la voix du professeur. Prévois 30 minutes ; tu avances à ton rythme.",
             "parties": parties}
    return sujet, voix


def main():
    out = {}
    for nom, conf in EXAMENS.items():
        out[nom] = convertir(nom, conf)
    CIBLE.parent.mkdir(parents=True, exist_ok=True)
    corps = ["/** Généré par scripts/sujets_2bacpcf.py à partir des exercices existants (voix déjà enregistrées) : ne pas modifier à la main. */",
             "import type { PartieExamen } from '../tronc-commun/sujet';", ""]
    for nom, (sujet, voix) in out.items():
        corps.append(f"export const SUJET_{nom.upper()} = {json.dumps(sujet, ensure_ascii=False, indent=1)} as unknown as {{ titre: string; niveau: string; matiere: string; minutes: number; programme: string; consigne: string; parties: PartieExamen[] }};")
        corps.append(f"export const VOIX_{nom.upper()}: Record<string, string> = {json.dumps(voix, ensure_ascii=False, indent=1)};")
        corps.append("")
        n = sum(len(p["questions"]) for p in sujet["parties"])
        print(nom, ":", n, "questions,", sum(q["points"] for p in sujet["parties"] for q in p["questions"]), "points,", sujet["minutes"], "min,", len(voix), "voix")
    CIBLE.write_text("\n".join(corps), encoding="utf-8")


if __name__ == "__main__":
    main()
