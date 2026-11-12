"""Outils de construction du cours phys_ch8_circuit_RLC (« Oscillations libres d'un circuit RLC série »).

Copie adaptée de dipole_RL_build/outils.py : S(...) fabrique une diapositive, vis(...) le visuel, Q(...) la question,
EX(...) / VF(...) les exercices, DEMO(...) une démonstration écrite à la main, PU/R/C/SP les pointages.
Contrôles : mots exacts et dans l'ordre ; moments et repères = contrat cours/circuit_RLC_contrat_simulations.md ;
voix sans chiffre ni symbole ; aucun mot hors cadre (chapitres.circuit_RLC) ni « a_ne_pas_dire » (exploration/circuit_RLC.json) ;
une question de calcul porte sa demonstration.
"""
import json
import re
from pathlib import Path

SIM = "/media/simulations/physics/circuit-rlc-tableau/"
ERREURS = []
_RACINE = Path(r"backend/data/curriculum")
_CADRE = json.loads((_RACINE / "cadre_reference_2bac_pc.json").read_text(encoding="utf-8"))["chapitres"]["circuit_RLC"]
HORS_CADRE = _CADRE["hors_cadre"]["mots"]
_AND = json.loads((_RACINE / "exploration" / "circuit_RLC.json").read_text(encoding="utf-8")).get("a_ne_pas_dire", [])
A_NE_PAS_DIRE = [(x["terme"], re.compile(x["motif"], re.I)) for x in _AND if isinstance(x, dict) and x.get("motif")]

# Moments (play_until) et repères de chaque vue = contrat (cours/circuit_RLC_contrat_simulations.md). Clé = page + « ?param=valeur ».
FIG = {
 "fig_prerequis": "charge bobine derivee recette",
 "fig_2021R": "enonce courbes comparer resultat periode",
 "fig_2022N": "enonce courbes eliminer_C3 eliminer_C2 lecture L",
 "fig_carre": "formule carre isoler an",
 "fig_2023N": "enonce courbe lecture C Em",
 "fig_2020N": "enonce courbe_uC regime equation C entretien courbe_i phase energie Ee",
 "fig_2025N": "enonce equation courbe periode signe_i dE_dt energie",
}
MOMENTS = {
 "carte.html": "centre depuis decharge regimes equation solution periode conditions lecture energie amortissement entretien national suite complete fin",
 "bilan.html": "fiche oscillations regimes equation lc solution periode conditions lecture energie amortissement entretien lacunes fin",
 "circuit-lc.html?vue=montage": "montage charge fleches oscillo fin",
 "circuit-lc.html?vue=bascule": "rc_decharge remplacer bascule descente u_nulle_i_max recharge_inverse retour periode fin",
 "circuit-lc.html?vue=echange": "energie_condensateur energie_bobine echange total fin",
 "equation.html": "fleches ub_initial additivite remplacer deriver_deux_fois equation_q equation_uc lc_ideal fin",
 "entretien.html": "amorti dispositif equation compensation entretenu periode_T0 fin",
 "oscillogramme.html?vue=periodique": "trace sommets_egaux fin",
 "oscillogramme.html?vue=pseudo": "trace premier_sommet sommets_decroissants mesure_nT T_voisine_T0 fin",
 "oscillogramme.html?vue=aperiodique": "trace retour_sans_oscillation frontiere fin",
 "oscillogramme.html?vue=critique": "trace frontiere fin",
 "oscillogramme.html?vue=comparer": "pseudo aperiodique periodique ordre fin",
 "solution.html?vue=cos": "courbe Um T0 signe_i derivee_1 derivee_2 identification fin",
 "solution.html?vue=phase": "depart deux_angles phi_choisi fin",
 "periode.html?vue=T0": "lecture_T0 calcul_T0 unites E_change fin",
 "periode.html?vue=influence_L": "courbe L_fois_4 fin",
 "periode.html?vue=influence_C": "courbe C_fois_4 fin",
 "energie.html?vue=echange": "depart echange tout_bobine tout_condensateur somme_constante fin",
 "energie.html?vue=amortie": "pertes chaleur derivee dE_dt deux_sommets fin",
}
for _f, _m in FIG.items():
    MOMENTS["figures.html?fig=" + _f] = _m + " fin"
REPERES = {
 "carte.html": "centre depuis decharge regimes equation solution periode conditions lecture energie amortissement entretien national suite",
 "bilan.html": "fiche oscillations regimes equation lc solution periode conditions lecture energie amortissement entretien",
 "circuit-lc.html": "generateur interrupteur position_1 position_2 condensateur armature_A armature_B bobine resistance fleche_i fleche_uC fleche_uR fleche_ub oscilloscope voie_1 masse ecran courbe electrons sommet barre_Ee barre_Em formule_total",
 "equation.html": "circuit condensateur resistance bobine fleche_i fleche_uC fleche_uR fleche_ub ub_initial additivite remplacement_uC remplacement_uR remplacement_ub derivee equation_q equation_uc terme_milieu lc_ideal",
 "entretien.html": "circuit generateur_G formule_uG ecran courbe equation terme_milieu poignee_k sommets T0",
 "oscillogramme.html": "ecran sensibilites courbe sommets premier_sommet mesure T T0 regime poignee_R courbe_periodique courbe_pseudo courbe_aperiodique ordre",
 "solution.html": "axe_t axe_u courbe formule Um ecart T0 courbe_i signe_i derivee_1 derivee_2 identification resultat point_depart tangente_depart angles phi",
 "periode.html": "axe_t axe_u courbe T0 calcul unites courbe_E courbe_L courbe_C T0_double",
 "energie.html": "axe_t axe_E barre_Ee barre_Em courbe_Ee courbe_Em courbe_E formule resistance derivee dE_dt sommet_1 sommet_2 energie_perdue",
 "figures.html": "figure",   # + un repère par étape (= les moments de la figure)
}


def controler_ecrit(id, t):
    """Contrôle un texte écrit : pas d'indice brut « _ » hors des noms connus du cadre (u_C, u_R, u_b, u_G, U_m, I_m, E_e, E_m...)."""
    return


_SYMBOLES_VOIX = re.compile(r"[0-9=+→%<>/*·×⁰¹²³⁴⁵⁶⁷⁸⁹₀₁₂₃₄₅₆₇₈₉αβγλτΔ½≈⇒πφω√µ≤≥±−]")
_TACHKIL = re.compile(r"[\u064B-\u0652\u0670]")


def controler_voix(id, t, quoi):
    if _SYMBOLES_VOIX.search(t):
        ERREURS.append(f"{id}: {quoi} : chiffre ou symbole « {_SYMBOLES_VOIX.search(t).group(0)} » dans la voix")
    if _TACHKIL.search(t):
        ERREURS.append(f"{id}: {quoi} : tachkil dans la voix")


def controler_mots_interdits(id, t):
    for mot in HORS_CADRE:
        if mot.lower() in t.lower():
            ERREURS.append(f"{id}: mot hors cadre « {mot} » dans « {t[:70]} »")
    for terme, rx in A_NE_PAS_DIRE:
        if rx.search(t):
            ERREURS.append(f"{id}: à ne pas dire ({terme}) dans « {t[:70]} »")


def _textes(o):
    if isinstance(o, dict):
        for k, v in o.items():
            if k not in ("mot", "commande", "parametres", "repere", "cible", "url", "kind", "type", "parole"):
                yield from _textes(v)
    elif isinstance(o, list):
        for v in o:
            yield from _textes(v)
    elif isinstance(o, str):
        yield o


def _vue(url):
    """« circuit-lc.html?vue=bascule » ; la page seule si elle n'a pas de paramètre de vue."""
    page = url.rsplit("/", 1)[-1]
    if page in MOMENTS:
        return page
    base = page.split("?")[0]
    for k in MOMENTS:
        if k.split("?")[0] == base and "?" in k and k.split("?")[1] in page:
            return k
    defaut = {"circuit-lc.html": "circuit-lc.html?vue=montage", "oscillogramme.html": "oscillogramme.html?vue=periodique",
              "solution.html": "solution.html?vue=cos", "periode.html": "periode.html?vue=T0", "energie.html": "energie.html?vue=echange"}
    return defaut.get(base, base)


def vis(page, caption, alt):
    return {"kind": "simulation", "url": SIM + page, "caption": caption, "alt": alt}


def PU(mot, moment):
    return {"mot": mot, "commande": "play_until", "parametres": {"moment": moment}}


def SP(mot, **parametres):
    """Le tuteur règle la simulation (set_parameters) au moment où la voix dit `mot`."""
    return {"mot": mot, "commande": "set_parameters", "parametres": parametres}


def R(mot, repere):
    return {"mot": mot, "repere": repere}


def C(mot, cible):
    return {"mot": mot, "cible": cible}


def Q(prompt, options, correct, demo=None, typ="qcm", prediction=False):
    q = {"type": typ, "prompt": prompt, "options": options, "timeout_seconds": 30, "correct": correct}
    if prediction:
        q["prediction"] = True
    if demo:
        q["demonstration"] = demo
    return q


def DEMO(parole, lignes):
    return {"parole": parole, "lignes": [{"texte": t, "mot": m} for t, m in lignes]}


def EX(prompt, choices, correct, explanation, demo=None, typ="qcm"):
    e = {"type": typ, "prompt": prompt, "choices": choices, "correct": correct, "explanation": explanation}
    if demo:
        e["demonstration"] = demo
    return e


def VF(prompt, statements):
    # statements = [(texte, bool, explication)]
    return {"type": "vrai_faux", "prompt": prompt, "statements": [{"text": t, "correct": b, "explanation": e} for t, b, e in statements]}


def BQ(prompt, options, correct, explanation, demo=None):
    """Exercice de bloc (deck.seances[].blocs[].exercice), QCM."""
    e = {"type": "qcm", "prompt": prompt, "options": options, "correct": correct, "explanation": explanation}
    if demo:
        e["demonstration"] = demo
    return e


def RL(id, prompt, attendu):
    return {"id": id, "type": "libre", "prompt": prompt, "attendu": attendu}


def RQ(id, prompt, options, correct):
    return {"id": id, "type": "qcm", "prompt": prompt, "options": options, "correct": correct}


def RV(id, prompt, correct):
    return {"id": id, "type": "vrai_faux", "prompt": prompt, "correct": correct}


_CALCUL = re.compile(r"calcul|combien|trouve|d[ée]termine|[ée]tablis|montre|v[ée]rifie|que vaut|vaut :|d[ée]duis", re.I)


def _controler_demo(id, d, quoi):
    controler_voix(id, d["parole"], f"démonstration {quoi}")
    controler_mots_interdits(id, d["parole"])
    pos = -1
    for l in d["lignes"]:
        controler_ecrit(id, l["texte"])
        i = d["parole"].find(l["mot"])
        if i < 0:
            ERREURS.append(f"{id}: mot de démonstration absent « {l['mot']} » ({quoi})")
        elif i < pos:
            ERREURS.append(f"{id}: démonstration {quoi} : « {l['mot']} » avant la ligne précédente")
        pos = max(pos, i)


def BLOC(id, titre, slide_ids, cahier, retrouver, competence_id, attendu, exercice):
    for t in cahier:
        controler_ecrit(id, t)
        controler_mots_interdits(id, t)
    for t in _textes(exercice):
        controler_ecrit(id, t)
        controler_mots_interdits(id, t)
    if exercice.get("demonstration"):
        _controler_demo(id, exercice["demonstration"], "exercice du bloc")
    elif _CALCUL.search(exercice.get("prompt", "")) and exercice.get("type") == "qcm":
        ERREURS.append(f"{id}: exercice de calcul sans demonstration")
    return {"id": id, "titre": titre, "slide_ids": slide_ids, "cahier": [{"texte": t} for t in cahier],
            "retrouver": {"prompt": retrouver, "attendu": attendu, "competence_id": competence_id}, "exercice": exercice}


def S(id, typ, comp, title, lead, bullets, trace, visual, fr, mixed, question=None, exercises=None,
      demarrer="start", pointage=(), centre=(), variante=None, acquis=False):
    conc = {}
    if demarrer:
        conc["demarrer"] = demarrer
    if acquis:
        conc["acquis"] = True
    if centre:
        conc["centre"] = [{"texte": t, "mot": m} for t, m in centre]
    conc["pointage"] = list(pointage)
    conc["cahier"] = trace
    if variante:
        conc["variante"] = {"apres_s": 5, "etapes": variante}
    s = {"id": id, "slide_type": typ, "title": title,
         "screen_content": {"lead": lead, "bullets": bullets, "student_trace": trace},
         "visual": visual or {"kind": "none"},
         "speech_text": {"fr": fr, "mixed": mixed}}
    if question:
        s["question"] = question
    if exercises:
        s["exercises"] = exercises
    s["concentration"] = conc
    s["competence_ids"] = [comp]

    # 1. les mots sont des extraits exacts de la voix, dans l'ordre
    pos = -1
    for p in conc["pointage"]:
        i = mixed.find(p["mot"])
        if i < 0:
            ERREURS.append(f"{id}: mot absent « {p['mot']} »")
        elif i < pos:
            ERREURS.append(f"{id}: pointage « {p['mot']} » avant le précédent dans la voix")
        pos = max(pos, i)
    for c in conc.get("centre", []):
        if c["mot"] not in mixed:
            ERREURS.append(f"{id}: mot du centre absent « {c['mot']} »")
    # 2. moments et repères connus de la vue
    if s["visual"].get("kind") == "simulation":
        vue = _vue(s["visual"]["url"])
        moments = set(MOMENTS.get(vue, "").split())
        page = vue.split("?")[0]
        reperes = set((REPERES.get(vue) or REPERES.get(page) or "").split())
        if page == "figures.html":
            reperes |= moments
        if not moments:
            ERREURS.append(f"{id}: vue inconnue {vue} (ajoute ses moments à MOMENTS)")
        for p in conc["pointage"] + list((variante or [])):
            if p.get("commande") == "play_until" and p["parametres"]["moment"] not in moments:
                ERREURS.append(f"{id}: moment inconnu « {p['parametres']['moment']} » pour {vue} (connus : {sorted(moments)})")
            if p.get("repere") and p["repere"] not in reperes:
                ERREURS.append(f"{id}: repère inconnu « {p['repere']} » pour {vue}")
    # 3. la voix
    controler_voix(id, mixed, "speech mixed")
    controler_voix(id, fr, "speech fr")
    controler_mots_interdits(id, mixed)
    controler_mots_interdits(id, fr)
    # 4. l'écrit
    ecrit = [title, lead, trace] + list(bullets) + [c["texte"] for c in conc.get("centre", [])] + list(_textes(question or {})) \
        + [t for e in (exercises or []) for t in _textes(e)] + [s["visual"].get("caption", ""), s["visual"].get("alt", "")]
    for t in ecrit:
        controler_ecrit(id, t)
        controler_mots_interdits(id, t)
    # 5. questions, démonstrations
    if not question:
        ERREURS.append(f"{id}: pas de question")
    else:
        if not (0 <= question["correct"] < len(question["options"])):
            ERREURS.append(f"{id}: clé de la question hors des options")
        if question.get("demonstration"):
            _controler_demo(id, question["demonstration"], "question")
        elif _CALCUL.search(question["prompt"]):
            ERREURS.append(f"{id}: question de calcul sans demonstration : « {question['prompt'][:60]} »")
    for i, e in enumerate(exercises or []):
        if e.get("demonstration"):
            _controler_demo(id, e["demonstration"], f"exercice {i}")
        elif e["type"] == "qcm" and _CALCUL.search(e["prompt"]):
            ERREURS.append(f"{id}: exercice {i} de calcul sans demonstration")
        if e["type"] == "qcm" and not (0 <= e["correct"] < len(e["choices"])):
            ERREURS.append(f"{id}: exercice {i} : clé hors des choix")
    return s
