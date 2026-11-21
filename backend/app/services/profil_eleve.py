"""Le profil d'apprentissage de l'élève : UNE source pour toute la plateforme (21 novembre 2026).

Demande de l'utilisateur : « câbler toutes les données ; elles seront utilisées par le mode libre ; toute la plateforme
doit y avoir accès pour organiser et donner à l'élève ce qu'il doit faire : exercice à donner, cours à entendre,
élément à apprendre, par cours… préparer l'infrastructure ».

Sources (rien d'inventé, rien de nouveau à stocker) :
  - services/stats_cours.py : lectures, temps, diapositives vues, 14 derniers jours (avec l'historique d'avant) ;
  - services/suivi_acquis.py : statut par compétence, méthodes qui marchent, lacunes et manière de les reprendre ;
  - les cours eux-mêmes (version allégée : diapositives, titres, compétences par diapositive).

Ce qu'on en tire :
  - `profil(student_id)` : global + par cours + `a_faire`, la liste ordonnée de ce que l'élève doit faire ;
  - `bloc_prompt(p)` : le texte court que le tuteur (mode libre, et tout autre écran plus tard) met dans son prompt.

`a_faire` (ordre de priorité) — chaque action porte de quoi l'ouvrir directement (cours, diapositives, compétence) :
  1. « exercice » : une compétence NON ACQUISE (faux deux fois) → un exercice dessus, avec la méthode à essayer ;
  2. « exercice » : une compétence PARTIELLE (juste au 2e essai) → un exercice de consolidation ;
  3. « cours » : un cours commencé et pas fini → la prochaine diapositive non vue (« cours à entendre ») ;
  4. « element » : une compétence d'un cours commencé jamais évaluée → l'élément à apprendre, avec ses diapositives.
Les règles de choix (dosage, rappels espacés de la mémoire longue, examens…) viendront ici, au même endroit.
"""
from __future__ import annotations

from typing import Any, Optional

from app.services import stats_cours, suivi_acquis

#: au plus tant d'actions renvoyées (l'écran et le tuteur n'en montrent que quelques-unes)
MAX_ACTIONS = 12


def _diapos_par_competence(deck: dict) -> dict[str, list[dict]]:
    _, par_diapo = suivi_acquis.competences_du_cours(deck)
    titres = {s["id"]: s.get("title", "") for a in deck.get("activities", []) for s in a.get("slides", [])}
    out: dict[str, list[dict]] = {}
    for sid, comps in par_diapo.items():
        for c in comps:
            out.setdefault(c, []).append({"id": sid, "titre": titres.get(sid, "")})
    return out


def _prochaine_non_vue(deck: dict, vues: set[str]) -> Optional[dict]:
    """La première diapositive pas encore vue après la dernière vue (sinon la première non vue du cours)."""
    ordre = [(s["id"], s.get("title", "")) for a in deck.get("activities", []) for s in a.get("slides", [])]
    derniere = max((i for i, (sid, _) in enumerate(ordre) if sid in vues), default=-1)
    for sid, titre in ordre[derniere + 1:] + ordre[:derniere + 1]:
        if sid not in vues:
            return {"id": sid, "titre": titre, "index": next(i for i, (x, _) in enumerate(ordre) if x == sid)}
    return None


def profil(student_id: str) -> dict[str, Any]:
    tab = stats_cours.tableau(student_id, avec_vues=True)
    decks = stats_cours.cours_alleges()
    cours: dict[str, dict] = {}
    actions: list[dict] = []
    total_min = acquises = total_comp = commences = termines = 0
    for cle, t in tab.items():
        st, comp = t["stats"], t["competences"]
        evalue = comp["total"] - comp["non_evalue"]
        if not st and not evalue:
            continue                    # cours jamais ouvert : rien à dire de l'élève dessus
        deck = decks.get(cle) or {}
        par_comp = _diapos_par_competence(deck)
        vues = set(t.get("diapos_vues") or [])
        commences += 1
        termines += 1 if (st or {}).get("terminaisons") else 0
        total_min += (st or {}).get("minutes", 0)
        acquises += comp["acquis"]
        total_comp += comp["total"]
        prochaine = _prochaine_non_vue(deck, vues) if t["vu_pourcent"] < 100 else None
        cours[cle] = {
            "titre": t.get("titre", ""), "vu_pourcent": t["vu_pourcent"], "diapos": t["diapos"],
            "lectures_terminees": (st or {}).get("terminaisons", 0), "seances": (st or {}).get("ouvertures", 0),
            "minutes": (st or {}).get("minutes", 0), "derniere": (st or {}).get("derniere"),
            "competences": {k: comp[k] for k in ("total", "acquis", "partiel", "non_acquis", "non_evalue")},
            "lacunes": [c for c in comp["liste"] if c["statut"] in ("non_acquis", "partiel")],
            "a_apprendre": [c for c in comp["liste"] if c["statut"] == "non_evalue"],
            "prochaine_diapo": prochaine,
        }
        for c in comp["liste"]:
            if c["statut"] in ("non_acquis", "partiel"):
                actions.append({"type": "exercice", "priorite": 1 if c["statut"] == "non_acquis" else 2, "cours": cle,
                                "titre_cours": t.get("titre", ""), "competence": c["id"], "label": c["label"], "statut": c["statut"],
                                "methode": c["reprendre_avec"][:1], "diapos": par_comp.get(c["id"], [])[:6],
                                "derniere": (st or {}).get("derniere")})
            elif c["statut"] == "non_evalue":
                actions.append({"type": "element", "priorite": 4, "cours": cle, "titre_cours": t.get("titre", ""),
                                "competence": c["id"], "label": c["label"], "diapos": par_comp.get(c["id"], [])[:6],
                                "derniere": (st or {}).get("derniere")})
        if prochaine:
            actions.append({"type": "cours", "priorite": 3, "cours": cle, "titre_cours": t.get("titre", ""),
                            "diapo": prochaine, "vu_pourcent": t["vu_pourcent"], "derniere": (st or {}).get("derniere")})
    # même priorité : le cours travaillé le plus récemment d'abord (il est encore frais)
    actions.sort(key=lambda a: (a["priorite"], -_horodatage(a.get("derniere"))))
    return {
        "global": {"cours_commences": commences, "cours_lus_en_entier": termines, "minutes": total_min,
                   "competences_acquises": acquises, "competences_total": total_comp,
                   "pourcent_acquis": round(acquises * 100 / total_comp) if total_comp else 0},
        "cours": cours,
        "a_faire": actions[:MAX_ACTIONS],
    }


def _horodatage(iso: Optional[str]) -> float:
    from datetime import datetime
    try:
        return datetime.fromisoformat(str(iso)).timestamp() if iso else 0.0
    except ValueError:
        return 0.0


def bloc_prompt(p: dict, max_car: int = 2500) -> str:
    """Le profil en texte court pour le prompt du tuteur : où en est l'élève, ses lacunes, ce qu'il doit faire."""
    if not p["cours"]:
        return ""
    g = p["global"]
    lignes = [
        "[PROFIL DE L'ÉLÈVE — toutes ses données de cours]",
        f"{g['cours_commences']} cours commencés, {g['cours_lus_en_entier']} lus en entier, {g['minutes']} min de travail ; "
        f"compétences acquises : {g['competences_acquises']}/{g['competences_total']} ({g['pourcent_acquis']} %).",
    ]
    for c in sorted(p["cours"].values(), key=lambda c: -_horodatage(c.get("derniere"))):
        k = c["competences"]
        lignes.append(f"- {c['titre']} : vu {c['vu_pourcent']} %, {c['seances']} séances, {c['minutes']} min, "
                      f"acquises {k['acquis']}/{k['total']}, partielles {k['partiel']}, à revoir {k['non_acquis']}, "
                      f"pas encore évaluées {k['non_evalue']}.")
    noms = {"exercice": "Exercice", "cours": "Cours à entendre", "element": "Élément à apprendre"}
    if p["a_faire"]:
        lignes.append("CE QUE L'ÉLÈVE DOIT FAIRE, dans l'ordre (propose la première action quand il demande quoi faire, "
                      "ou quand la conversation le permet ; une seule à la fois) :")
        for i, a in enumerate(p["a_faire"][:6], 1):
            if a["type"] == "cours":
                quoi = f"reprendre « {a['titre_cours']} » à la diapositive « {a['diapo']['titre']} » (vu {a['vu_pourcent']} %)"
            else:
                quoi = f"{a['label']} ({a['titre_cours']})"
                if a.get("methode"):
                    quoi += f", à reprendre avec {a['methode'][0]}"
            lignes.append(f"{i}. {noms[a['type']]} : {quoi}.")
    return "\n".join(lignes)[:max_car]
