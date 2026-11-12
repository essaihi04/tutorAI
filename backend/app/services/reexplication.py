"""Le cycle de reprise (user rule, 8 novembre 2026) : une réponse fausse → le tuteur réexplique AUTREMENT, sur la
même diapositive, puis pose une question jumelle ; juste → on passe ; faux → nouveau cycle, trois au plus.

Ce que le tuteur reçoit pour expliquer autrement : la diapositive (titre, ce qu'il a déjà dit), la question et la
réponse fausse de l'élève, les méthodes déjà essayées sur cette notion, les méthodes qui marchent avec CET élève
(suivi des acquis), et ce que la simulation sait faire (instants clés `moments`, repères). Il répond en JSON :
  - parole : ce qu'il dit (règles de la voix), 5 à 8 phrases, une autre entrée que la première fois ;
  - gestes : ce qu'il fait dans la simulation pendant qu'il parle : [{"commande": "play_until", "parametres":
    {"moment": "..."}}, {"repere": "..."}], 2 à 5 gestes, seulement des moments et repères existants ;
  - question : une question JUMELLE (même compétence, autre forme ou autres valeurs), jamais la même ;
  - au 3e cycle : `reponse_finale` (la bonne réponse et sa justification, dite) et `cahier` (une phrase à écrire).
"""
from __future__ import annotations

import json
from typing import Any, Optional

from app.services.simulation_reaction import REGLES_VOIX, lire_json, parole_propre, valider_question

MAX_CYCLES = 3
ENTREES = {
    1: "repars de la SIMULATION : rejoue-la et fige-la sur les instants qui montrent la notion, en décrivant ce qu'on voit à chaque arrêt",
    2: "repars d'un EXEMPLE CONCRET avec d'autres valeurs (chiffres simples), fais le raisonnement à voix haute étape par étape, puis relie-le à la figure",
    3: "repars de la RÉPONSE : donne-la, justifie-la en deux phrases avec la relation du cours, et fais écrire une phrase au cahier",
}


def prompt_reexplication(ctx: dict) -> tuple[str, int]:
    n = max(1, min(MAX_CYCLES, int(ctx.get("cycle") or 1)))
    q = ctx.get("question") or {}
    choix = q.get("choix") or []
    bonne = q.get("bonne")
    cle = f"Bonne réponse : {choix[bonne]}" if isinstance(bonne, int) and 0 <= bonne < len(choix) else (f"Réponse attendue : {q['attendu']}" if q.get("attendu") else "")
    moments = ctx.get("moments") or {}
    reperes = ctx.get("reperes") or {}
    marchent = ctx.get("methodes_qui_marchent") or []
    essayees = ctx.get("methodes_essayees") or []
    genre = "vrai_faux" if n >= 2 else "qcm"
    forme = {
        "qcm": '"question": {"type": "qcm", "enonce": "...", "choix": ["...", "...", "..."], "bonne": 0, "explication": "...", "parole_juste": "...", "parole_faux": "..."}',
        "vrai_faux": '"question": {"type": "vrai_faux", "enonce": "...", "affirmations": [{"texte": "...", "vrai": true}, {"texte": "...", "vrai": false}], "explication": "...", "parole_juste": "...", "parole_faux": "..."}',
    }[genre]
    finale = ', "reponse_finale": "la bonne réponse et sa justification, dites (règles de la voix)", "cahier": "une phrase à écrire au cahier, en français"' if n >= MAX_CYCLES else ""
    sim = ""
    if moments or reperes:
        sim = f"""La simulation de la diapositive sait se figer sur ces instants (play_until) : {', '.join(f'{k} ({v})' for k, v in moments.items()) or 'aucun'}.
Repères qu'on peut montrer du doigt (highlight) : {', '.join(f'{k} ({v})' for k, v in reperes.items()) or 'aucun'}.
Pendant que tu parles, tu fais 2 à 5 gestes dans la simulation, dans l'ordre de ton explication, en n'utilisant QUE ces noms."""
    return f"""Tu es le professeur de physique d'un élève de 2e Bac PC BIOF au Maroc. Diapositive « {ctx.get('title', '')} ».
Ce que tu as déjà expliqué (ne le répète pas tel quel) : {str(ctx.get('speech') or '')[:1200]}

Question posée : {q.get('enonce', '')}
{chr(10).join(f'  {chr(65 + i)}. {c}' for i, c in enumerate(choix))}
{cle}
Réponse(s) fausse(s) de l'élève : {ctx.get('reponses_fausses') or '—'}
Méthodes déjà essayées avec lui sur cette notion : {', '.join(essayees) or 'l’explication du cours'}.
Méthodes qui marchent avec cet élève d'après son suivi : {', '.join(marchent) or 'inconnues (préfère la simulation manipulée, puis un exercice)'}.

C'est le cycle de reprise n° {n} sur {MAX_CYCLES} : {ENTREES[n]}. Une autre porte d'entrée que la première explication,
jamais la même phrase. 5 à 8 phrases, puis tu annonces une question.
{sim}

Puis pose une question JUMELLE de type « {genre} » : même compétence, autre forme ou autres valeurs, jamais la même
question. Énoncé et choix ÉCRITS comme au tableau : relations en écriture mathématique (« g(x) = (2x² − 8)/(x − 2) »,
« lim_{{x→2}} g(x) »), nombres en chiffres (« 8 », pas « huit »), unités en symboles — jamais en toutes lettres.

{REGLES_VOIX}

Réponds UNIQUEMENT par ce JSON :
{{"parole": "...", "ecrit": "l'idée clé en une phrase, en français écrit", "gestes": [{{"commande": "play_until", "parametres": {{"moment": "..."}}}}, {{"repere": "..."}}], {forme}{finale}}}""", n


def valider_gestes(gestes: Any, moments: dict, reperes: dict) -> list[dict]:
    out = []
    for g in gestes or []:
        if not isinstance(g, dict):
            continue
        if g.get("repere") in reperes:
            out.append({"repere": g["repere"]})
        elif g.get("commande") == "play_until" and isinstance(g.get("parametres"), dict) and g["parametres"].get("moment") in moments:
            out.append({"commande": "play_until", "parametres": {"moment": g["parametres"]["moment"]}})
        elif g.get("commande") in ("start", "fire_pulse"):
            out.append({"commande": g["commande"]})
    return out[:5]


def reexplication_depuis(texte_llm: str, ctx: dict, n: int) -> Optional[dict]:
    d = lire_json(texte_llm)
    if not d:
        return None
    parole = parole_propre(d.get("parole"))
    genre = "vrai_faux" if n >= 2 else "qcm"
    question = valider_question(d.get("question"), genre)
    if not parole or not question:
        return None
    out = {"cycle": n, "parole": parole, "ecrit": str(d.get("ecrit") or "").strip()[:400],
           "gestes": valider_gestes(d.get("gestes"), ctx.get("moments") or {}, ctx.get("reperes") or {}), "question": question,
           "dernier": n >= MAX_CYCLES}
    if n >= MAX_CYCLES:
        out["reponse_finale"] = parole_propre(d.get("reponse_finale"))
        out["cahier"] = str(d.get("cahier") or "").strip()[:300]
    return out
