"""Architecture des cours RC, RL, RLC et ch9 après la 2ᵉ passe (18 novembre 2026) : le tableau des séances est recalculé
depuis la copie en attente, la partie « joué pas à pas » est ajoutée diapositive par diapositive, et la section
« 2ᵉ passe » dit ce qui a changé, pourquoi, et ce qui reste. Relançable (les blocs ajoutés sont remplacés).
Usage : python -X utf8 scripts/logique/architecture_pas_a_pas.py
"""
import json, re
from pathlib import Path

R = Path(__file__).resolve().parents[2]
ARCHI = R / "backend/data/curriculum/architecture"
DEBUT, FIN = "<!-- 2e passe : début -->", "<!-- 2e passe : fin -->"

POURQUOI = {
    "sujet": "Règle 6 du professeur : le sujet lu deux fois (de quoi parle-t-il ? puis les données et ce qu'on cherche) avant tout calcul ; aucune question notée.",
    "copie": "Règle 33 : la copie complète vient après la dernière étape, jamais avant ; chaque réponse se relit comme le barème la lit (relation, application numérique, résultat et unité).",
}


def seances_md(m, pre):
    D = {s["id"]: s for a in m["activities"] for s in a["slides"]}
    lignes = ["| Séance | Blocs (diapositives) |", "|---|---|"]
    for se in m["seances"]:
        bl = " ; ".join(f"**{b['titre']}** ({', '.join(x[len(pre) + 1:] for x in b['slide_ids'])})" for b in se["blocs"])
        lignes.append(f"| {se['titre']} | {bl} |")
    return "\n".join(lignes)


def partie_md(m, act_id, pourquoi_etapes):
    a = next(x for x in m["activities"] if x["id"] == act_id)
    out = [f"#### {a['title']}", "", "| Diapositive | Titre | Visuel | À toi | Pourquoi ici |", "|---|---|---|---|---|"]
    for s in a["slides"]:
        q = s.get("question") or {}
        atoi = {"open": "écrit", "qcm": "QCM"}.get(q.get("type"), "")
        vis = s["visual"]["url"].split("/")[-1]
        k = s["id"].split("_np")[1].split("_", 1)
        cle = "sujet" if s["id"].endswith("_sujet") else "copie" if s["id"].endswith("_copie") else k[1]
        out.append(f"| `{s['id']}` | {s['title']} | {vis} | {atoi} | {POURQUOI.get(cle) or pourquoi_etapes[cle]} |")
    return "\n".join(out)


COMMUN = """
**La règle suivie à chaque étape** (demande du 18 novembre : « simple, animé, expliqué ; ne pas tout donner au départ ; laisser
à l'élève le temps de trouver seul ») :
1. la voix confirme la correction de l'étape d'avant pendant qu'elle se construit au tableau (moment `rappel` : la tangente
   se trace, la ligne du tableau d'avancement s'écrit, la réponse s'ajoute dans « Ta copie ») ;
2. elle pose UNE question (moment `question`) en nommant l'outil, jamais le résultat ; la simulation écrit la question
   et « … à toi d'abord » : la réponse reste cachée (`conclusions` faux par défaut) ;
3. l'élève répond (question ouverte jugée sur l'`attendu`, ou QCM avec ses réactions préparées) ;
4. la démonstration écrit la correction ligne par ligne, comme le barème la lit (relation, conversion, application
   numérique, résultat avec son unité) ; la diapositive suivante la redessine au tableau (étape 1).
Une diapositive par étape (`?etape=k`) : l'iframe se recharge et s'ouvre sur son état (règle 39). Les formules sont écrites
en notation (fractions superposées au tableau), les unités dites en mots dans la voix.

**Règle « un tableau par bloc ».** Dans cette partie, chaque étape porte sa question : c'est la demande du 18 novembre
(« la réponse de l'élève avant la correction »), plus récente que la règle du 13 novembre. Ailleurs, elle ne change pas.
Les questions ouvertes n'ont pas de réaction préparée : elles sont jugées en direct sur l'`attendu`, comme `rc_e2a`.

**La simulation** `national-pas-a-pas.html` (nouvelle, dans le dossier du cours) et son moteur `pas-a-pas.js` (une copie
par dossier de cours, aucun fichier partagé modifié) : figure du sujet à gauche (circuit peint avec les flèches de la
convention récepteur, courbes tracées à la craie, tableau d'avancement), « Ta copie » à droite. Moments : `enonce`,
`courbe`, `rappel`, `question`, `correction` ; vue `sujet` : `donnees`, `questions` ; `?etape=fin` : la copie complète.
Vérifiée dans Chromium à 1280 × 640 et 724 × 350 (téléphone en paysage) : aucune erreur, aucun texte hors cadre, texte ≥ 15 px
(plancher du kit), fractions sans chevauchement.
"""

CHAPITRES = {
    "phys_ch6_dipole_RC": dict(pre="rc", act="rc_partie8b", texte="""
### Ce qui manquait (évaluation de la 1ʳᵉ passe)
Les deux sujets complets (`rc_n1_2019`, `rc_n2_2021R`) se jouaient question par question, mais la voix donnait tout :
l'équation, A et α, Q, τ, puis « calcule C, puis R » ; l'élève ne répondait qu'à la fin. Aucun exercice du national ne
faisait chercher l'élève étape par étape sur τ (le cas le plus fréquent, 8 sujets sur 20), ni sur l'énergie.

### Ce qui est ajouté : le national 2022 N, partie 1, joué pas à pas (10 diapositives)
Choisi parce qu'il réunit les cas types les plus fréquents avec des valeurs rondes (corrigé lu le 18/11 : E = 12 V,
i(0) = 12 mA, τ = 50 ms, R = 1 kΩ, C = 50 µF) et qu'aucune diapositive du cours ne l'utilisait. Deux questions ajoutées,
signalées comme telles : τ par les 63 % (la seconde méthode, que d'autres sujets demandent) et l'énergie ½·C·E² = 3,6 mJ
(2023 R). Placé après l'énergie et avant les deux sujets complets : tout ce qu'il demande est déjà enseigné (règle 27).
L'ordre des étapes (équation, solution, lecture, τ deux fois, la grandeur cherchée, l'énergie) est le même dans le RL et
le RLC : l'élève reconnaît la démarche.
""", pourquoi=dict(
        equation="Cas type « établir l'équation » (4 sujets) : la démarche des étapes `rc_e2a`–`rc_e2c`, maintenant sur un sujet.",
        courant="Cas type « expression de i(t) » (3 sujets) : dériver la solution donnée ; la courbe se trace avant la question.",
        lire="Règle 12 : lire l'axe avant la courbe ; E et i(0) lus seuls, avant tout calcul (une idée à la fois).",
        R="Cas type « en déduire R, C ou E » (9 sujets) : la relation, la conversion, l'application numérique, le résultat.",
        tangente="Cas type le plus fréquent, τ graphiquement (8 sujets) : la tangente (T) du sujet ; sa construction se voit à l'étape suivante.",
        pourcent="Seconde méthode (règle 11 : vérifier par une deuxième route) ; 0,63·E calculé, pas affirmé (règle 37).",
        C="Question 1.2.3 du sujet : C = τ/R = 50 µF.",
        energie="Question ajoutée (énergie : 2023 R, cadre RC9) : ½·C·E² ; même valeur que E₀ de la partie RLC du même sujet.")),
    "phys_ch7_dipole_RL": dict(pre="rl", act="rl_partie8b", texte="""
### Ce qui manquait (évaluation de la 1ʳᵉ passe)
Les sujets du national (`rl_n1_2022R`, `rl_n2_2024N`, `rl_e7`, `rl_e8`, `rl_t4`) se jouaient avec la voix qui donnait
chaque réponse ; aucun n'était fait par l'élève étape par étape, en particulier « vérifier la solution, trouver A, B et τ »
(4 sessions) et la lecture de τ (9 sessions).

### Ce qui est ajouté : le national 2023 N, partie 1, joué pas à pas (11 diapositives)
Corrigé lu le 18/11 : E = 24 V, r négligeable, I₀ = 48 mA, τ = 2 ms, R = 500 Ω, L = 1 H, u_L(t) = 24·e^(−500·t)
(écrite u_b, la notation du cours, « notée u_L dans le sujet »). Le cours ne l'utilisait pas (le RLC n'en garde que la
partie LC, `lc_l4_2023`). Mêmes étapes, dans le même ordre, que le RC 2022 N ; deux questions ajoutées : les 63 % et
l'énergie ½·L·I₀² ≈ 1,2 mJ. Placé après l'énergie magnétique, avant les deux sujets complets.
""", pourquoi=dict(
        equation="Cas type « établir l'équation en i » (6 sessions), la démarche de `rl_e0a`–`rl_e0c` sur un sujet.",
        remplacer="Cas type « vérifier la solution » (4 sessions) : dériver, remplacer, regrouper — une étape seule.",
        constantes="Identifier « pour tout t », puis la condition initiale : B séparé de A (corrigé du sujet, règle 37).",
        lire="Régime permanent I₀ (6 sessions), lu seul avant le calcul de L.",
        tangente="τ graphiquement (9 sessions) : la tangente (T) du sujet, comme dans le RC.",
        pourcent="Seconde méthode, comme dans le RC (règle 11).",
        L="Trouver L à partir de τ (9 sessions) : L = τ·E/I₀.",
        ub="Question 1-3 du sujet (u_b(t), « u_L » dans le sujet) : dériver, simplifier L/(R·τ) = 1, écrire en SI.",
        energie="Question ajoutée (énergie : 4 sessions, cadre RL8), parallèle au RC.")),
    "phys_ch8_circuit_RLC": dict(pre="lc", act="lc_partie9b", texte="""
### Ce qui manquait (évaluation de la 1ʳᵉ passe)
Les huit nationaux du cours se jouaient par `figures.html`, `oscillogramme.html` et `energie.html`, mais la voix donnait
les réponses ; l'élève ne cherchait seul ni le choix de la courbe, ni T₀ et L, ni l'énergie dissipée entre deux instants
(14 sessions calculent une énergie, 13 lisent la période).

### Ce qui est ajouté : le national 2022 N, partie 2, joué pas à pas (11 diapositives)
Corrigé lu le 18/11 : C = 50 µF chargé sous 12 V ; r = 0 : courbe (C₁), T₀ = 10 ms, L = 0,05 H (π² = 10) ; r ≠ 0 : à t₀ = 0,
u_C = 12 V et i = 0 ; à t₁ = 9 ms, u_C = 6 V et i = 140 mA ; ΔE ≈ −2,2 mJ. La figure 4 est un modèle amorti ajusté pour
redonner exactement ces lectures (T = 10,1 ms, θ = 20,9 ms). (C₂) et (C₃) de la figure 3 sont redessinées comme les deux
pièges de la question (amortie ; partant de 0). Question ajoutée : l'entretien (2018 N, 2020 N), placé après la partie IX
qui l'enseigne. C'est la suite du RC 2022 N : le même condensateur, la même énergie de départ 3,6 mJ.
""", pourquoi=dict(
        equation="Cas type « établir l'équation » (très fréquent) : la démarche de `lc_e0a`–`lc_e0c`, en LC idéal (r = 0).",
        choix="Reconnaître la courbe : deux critères (pas de perte ; u_C(0) = 12 V), chacun élimine un piège. QCM avec réactions préparées.",
        T0="Dériver deux fois un cosinus et identifier T₀ = 2π√(LC) (cadre RLC4), une étape seule.",
        lire="Lire la période sur deux périodes (13 sessions) : règle 12, l'axe avant la courbe.",
        L="Trouver L (13 sessions) : le carré d'abord, π² = 10.",
        energie="Énergie totale (cadre RLC6) : deux réservoirs ; la figure 4 se trace avant la question.",
        lectures="Les quatre lectures seules, avant le calcul (une idée à la fois).",
        dissipee="Énergie dissipée entre deux instants (14 sessions calculent une énergie) : E₀, E₁, la différence et son signe.",
        entretien="Question ajoutée (2018 N, 2020 N) : u_G = k·i, k = résistance totale, période T₀.")),
    "phys_ch9_transformations_lentes_rapides": dict(pre="tl", act="tl_partie8b", texte="""
### Ce qui manquait (évaluation de la 1ʳᵉ passe)
Le tableau d'avancement n'était qu'un rappel dit par la voix (`tl_rp5_avancement`, sans visuel) ; aucun exercice ne faisait
construire le tableau ligne par ligne, ni exploiter une grandeur suivie au cours du temps ; les deux nationaux (`tl_n1`,
`tl_n2`) portent sur les courbes et la trempe, sans les couples ni l'équation.

### Ce qui est ajouté : un exercice type national, joué pas à pas (11 diapositives)
Les sujets 2016-2025 ne posent pas un exercice de ch9 entier : les questions de ce chapitre tombent dans des exercices de
piles, d'électrolyse ou de cinétique. L'exercice réunit donc leurs cas types sur la réaction du cours (eau oxygénée et ions
iodure, valeurs de `tl_rp5_avancement` et `tl_f7_palier`) : demi-équations et équation (piles, électrolyse : 12 à 15
sessions), tableau d'avancement ligne par ligne et réactif limitant, la grandeur suivie n(I₂) = x, la température facteur
cinétique et le même état final (2018 N, 2023 N, 2024 N, 2025 N), la trempe (2017 R). Il est appelé « exercice type
national » à l'écran, jamais « national 20xx ». Rien hors du cadre : ni vitesse, ni t½ (ch10).
Placé après la trempe et le catalyseur, avant les deux nationaux.

### Le chiffre de la carte (`tl_o1_carte`), vérifié
« Facteurs cinétiques dans dix sessions » ne tenait pas : relevé sur les 20 sujets (exam.json, questions et corrigés), des
questions sur les facteurs cinétiques, le catalyseur ou la trempe tombent dans **8 sessions** (2016 R, 2017 N, 2017 R,
2018 N, 2018 R, 2023 N, 2024 N, 2025 N). La voix (fr et darija) et la puce disent maintenant « huit », et la carte l'écrit
(`carte.html?sessions=8` ; sans paramètre, la carte garde 10 pour le cours en ligne, dont la voix dit « dix »). Sa voix est à
refaire. Les « quatorze sessions » des demi-équations restent : notre relevé donne 12 à 15 selon ce qu'on compte.

### `facteurs.html` : `conclusions: false` vérifié dans le navigateur
Vue `concentration` (observation de `tl_f5_concentre`) : avec `conclusions: false`, la ligne « le plus concentré brunit
plus vite » n'est pas écrite et la bulle demande « Lequel brunit le plus vite ? » ; après `conclusions: true`, la ligne
s'écrit et la bulle dit « le plus concentré est en avance ». Rien de décisif avant la réponse.
""", pourquoi=dict(
        demi="Couples et demi-équations (TLR2) : la question la plus fréquente du chapitre au national.",
        equation="L'équation à partir des deux demi-équations (TLR3) : un couple donne les électrons, l'autre les reçoit.",
        initial="Le tableau construit ligne par ligne (demande du 18/11) : l'état initial seul, n₀(I⁻) = [I⁻]₀·V calculé.",
        encours="La ligne « en cours » seule : les coefficients disent combien part et se forme.",
        limitant="L'état final : x_max pour chaque réactif, la plus petite valeur, le réactif limitant (TLR6 : le palier).",
        suivi="La grandeur suivie : n(I₂) = x ; la courbe se trace avant la question ; sa valeur finale vient du tableau.",
        temperature="La température facteur cinétique sur deux courbes (2023 N, 2025 N) : QCM avec réactions préparées.",
        final="Le même état final (2024 N, 2025 N : vrai/faux) : la température change la durée, pas x_max.",
        trempe="La trempe (2017 R) : froid et dilution, deux facteurs cinétiques qui diminuent.")),
}


def mots_md(deck):
    v = json.loads((ARCHI / f"{deck}_voix.json").read_text(encoding="utf-8"))
    n2 = sum(1 for p in v["pistes"] if p.get("passe") == 2)
    return f"""
### Les mots
`python -X utf8 scripts/voix/verifier_mots.py en_attente/{deck}` sur chaque piste nouvelle ou réécrite : plus aucun mot
rare évitable. Remplacés : « milliampères » (0 fois dans le corpus de la voix) → « milliampère » ; « kiloohm(s) » (0) →
« mille ohm » ; « microfarads » (0) → « micro farad » ; « millijoules » (1) → « millijoule » ; « palier » (0) → « la valeur
finale » ; « sommets » (0) → « l'amplitude » ; « quarante-huit », « cinquante-six », « trente-neuf » écrits sans trait
d'union (« quarante huit ») ; en darija, « فارغ » → « خاوي », « نرتبو » → « نكتبو l'équation », « كتوافق » → « كيكون عند »,
« ضاعت » → « dissipée », « كيصحح / كيقراها » → « فالتصحيح » ; au ch9, les réactions de `tl_r6_classer` (« portail », « الراسب »,
« كنحكمو »…) et de `tl_f8_variable` (« تقلقش », « فالتابلو », « quelles »…) sont réécrites. Restent, parce que ce sont des
termes du programme : {', '.join(v.get('a_ecouter') or []) or '—'} (liste `a_ecouter` du fichier des voix).
Pistes à mettre en voix : {len(v['pistes'])}, dont {n2} de la 2ᵉ passe (`{deck}_voix.json`, champ « passe »).
"""


VERIF = """
### Vérifications faites (2ᵉ passe)
- Les copies en attente se chargent ; chaque `mot` du pointage et des démonstrations est un extrait exact de sa voix
  (`scripts/logique/outils.py`, `verifier_mots`) ; les blocs suivent l'ordre du cours.
- `python backend/scripts/verifier_pointage_simulations.py <cours> --ecarts` : aucune erreur « introuvable », ni sur la copie
  en attente ni sur le cours en ligne. Les seuls avertissements des nouvelles diapositives sont des « GESTE » : sans piste,
  la durée vaut 0 et tous les gestes tombent au même instant ; à relancer après la voix.
- `cd backend && python -m pytest -q app/tests -k "course or cours or concentration"` (résultat dans le rapport du commit).
- Simulations : Chromium, 1280 × 640 et 724 × 350, chaque étape à `question` puis `correction` : pas d'erreur console,
  aucun texte hors cadre (`__horsCadre` vide), la réponse invisible avant `correction`.

### Ce qui reste à faire (hors de cette session)
- Les voix (Bodi, VPS, quota Kaggle épuisé aujourd'hui) des pistes du fichier `_voix.json`, puis relancer le contrôle du
  pointage avec les vraies durées.
- Les questions ouvertes de l'exercice joué n'ont pas de réaction préparée (jugées en direct sur l'`attendu`).
- Aucun fichier partagé n'a été modifié (`shared/`, `frontend/src/`).
"""


for deck, c in CHAPITRES.items():
    f = ARCHI / f"{deck}.md"
    md = f.read_text(encoding="utf-8")
    m = json.loads((R / f"backend/data/courses/en_attente/{deck}.json").read_text(encoding="utf-8"))
    md = re.sub(re.escape(DEBUT) + ".*?" + re.escape(FIN) + "\n?", "", md, flags=re.S)
    # le tableau des séances, recalculé
    if "| Séance | Blocs (diapositives) |" in md:
        md = re.sub(r"\| Séance \| Blocs \(diapositives\) \|\n\|---\|---\|\n(?:\|.*\|\n)+", seances_md(m, c["pre"]) + "\n", md)
    bloc = (f"{DEBUT}\n## 2ᵉ passe (18 novembre 2026) : le national joué pas à pas\n" + c["texte"] + COMMUN + "\n"
            + partie_md(m, c["act"], c["pourquoi"]) + "\n" + mots_md(deck) + VERIF + FIN + "\n")
    md = md.rstrip("\n") + "\n\n" + bloc
    f.write_text(md, encoding="utf-8")
    print(deck, "architecture à jour")
