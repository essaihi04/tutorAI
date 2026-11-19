"""Vérifie les deux formats du parcours d'un cours (18 novembre 2026, skill `cours-concentration`) :
`concentration.apres_reponse` (rejouer la simulation après la réponse) et `concentration.rappel` (sauter un rappel
déjà su). Même lecture que le lecteur (`frontend/src/components/course/parcours.js`).

    python -I backend/scripts/verifier_parcours.py backend/data/courses/en_attente/math_ch4_primitives.json [...]
    python -I backend/scripts/verifier_parcours.py --tous

Imprime les erreurs (le lecteur ignorerait le format : la diapositive se jouerait comme avant) et les remarques
(une commande qui jouerait le résultat avant la réponse : le lecteur la saute). Rien d'imprimé : tout est bon.
Code de sortie 1 s'il y a une erreur.
"""
from __future__ import annotations

import glob
import json
import sys
from pathlib import Path

RACINE = Path(__file__).resolve().parents[2]


def cles_des_questions(slide: dict) -> list[str]:
    """`q`, `e{i}`, `e{i}s{j}` : les questions du tableau, dans l'ordre (comme `questionsDeLaDiapo`)."""
    out = ["q"] if (slide.get("question") or {}).get("prompt") else []
    for i, ex in enumerate(slide.get("exercises") or []):
        if ex.get("type") == "association" and ((ex.get("association") or {}).get("gauche")):
            out.append(f"e{i}")
        if ex.get("type") == "qcm" and len(ex.get("choices") or []) >= 2:
            out.append(f"e{i}")
        if ex.get("type") == "vrai_faux":
            out += [f"e{i}s{j}" for j in range(len(ex.get("statements") or []))]
    return out


def _moment(c: dict):
    return (c.get("parametres") or {}).get("moment") if c.get("commande") == "play_until" else None


def verifier(deck: dict) -> tuple[list[str], list[str]]:
    """(erreurs, remarques) des formats `apres_reponse` et `rappel` d'un cours."""
    erreurs: list[str] = []
    remarques: list[str] = []
    slides = [s for a in deck.get("activities") or [] for s in a.get("slides") or []]
    rang = {s.get("id"): i for i, s in enumerate(slides)}
    for i, s in enumerate(slides):
        sid, conc = s.get("id"), s.get("concentration") or {}
        brut = conc.get("apres_reponse")
        if brut is not None:
            liste = brut if isinstance(brut, list) else [brut]
            cles = cles_des_questions(s)
            if not cles:
                erreurs.append(f"{sid} : apres_reponse sur une diapositive sans question")
            reserves: set[str] = set()
            vues: set[str] = set()
            for n, r in enumerate(liste):
                ici = f"{sid} : apres_reponse" + (f"[{n}]" if isinstance(brut, list) else "")
                if not isinstance(r, dict):
                    erreurs.append(f"{ici} doit être un objet")
                    continue
                etapes = r.get("etapes")
                if not isinstance(etapes, list) or not etapes:
                    erreurs.append(f"{ici}.etapes est vide")
                    etapes = []
                for k, e in enumerate(etapes):
                    if not isinstance(e, dict) or not (e.get("commande") or e.get("repere")):
                        erreurs.append(f"{ici}.etapes[{k}] n'a ni commande ni repere")
                    elif e.get("commande") == "play_until" and _moment(e) in (None, ""):
                        erreurs.append(f"{ici}.etapes[{k}] : play_until sans moment")
                    elif _moment(e) not in (None, ""):
                        reserves.add(str(_moment(e)))
                q = r.get("question") or (cles[0] if n == 0 and cles else None)
                if cles and q is None:
                    erreurs.append(f"{ici} : après le premier rejeu, chaque rejeu nomme sa question")
                elif cles and q not in cles:
                    erreurs.append(f"{ici}.question « {q} » inconnue (questions : {', '.join(cles)})")
                elif q in vues:
                    erreurs.append(f"{ici} : deux rejeux pour la question « {q} » (seul le premier compte)")
                vues.add(q)
                duree = r.get("duree_s")
                if duree is not None and (isinstance(duree, bool) or not isinstance(duree, (int, float)) or duree < 0):
                    erreurs.append(f"{ici}.duree_s doit être un nombre ≥ 0")
            avant = [("pointage", p) for p in conc.get("pointage") or []]
            avant += [("variante", e) for e in (conc.get("variante") or {}).get("etapes") or []]
            avant += [("observation.gestes", g) for g in (conc.get("observation") or {}).get("gestes") or []]
            for ou, c in avant:
                if isinstance(c, dict) and _moment(c) is not None and str(_moment(c)) in reserves:
                    remarques.append(f"{sid} : {ou} joue « {_moment(c)} » avant la réponse — le lecteur le saute (rejoué après)")
        rp = conc.get("rappel")
        if rp is not None:
            si = rp.get("si_reussi") if isinstance(rp, dict) else None
            liste = [si] if isinstance(si, str) else si if isinstance(si, list) else []
            liste = [x for x in liste if isinstance(x, str) and x.strip()]
            if not liste:
                erreurs.append(f"{sid} : rappel.si_reussi doit nommer la diapositive diagnostic")
            for d in liste:
                if d not in rang:
                    erreurs.append(f"{sid} : rappel.si_reussi « {d} » introuvable dans le cours")
                    continue
                if rang[d] >= i:
                    erreurs.append(f"{sid} : le diagnostic « {d} » doit venir AVANT le rappel")
                if not cles_des_questions(slides[rang[d]]):
                    erreurs.append(f"{sid} : le diagnostic « {d} » n'a pas de question (le rappel ne serait jamais sauté)")
    return erreurs, remarques


def main(args: list[str]) -> int:
    fichiers = sorted(glob.glob(str(RACINE / "backend/data/courses/**/*.json"), recursive=True)) if args == ["--tous"] else args
    code = 0
    for f in fichiers:
        try:
            deck = json.loads(Path(f).read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as e:
            print(f"{f} : illisible ({e})")
            code = 1
            continue
        if not isinstance(deck, dict) or "activities" not in deck:
            continue
        erreurs, remarques = verifier(deck)
        for m in erreurs:
            print(f"{Path(f).name} : ERREUR {m}")
        for m in remarques:
            print(f"{Path(f).name} : remarque {m}")
        code = code or (1 if erreurs else 0)
    return code


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
