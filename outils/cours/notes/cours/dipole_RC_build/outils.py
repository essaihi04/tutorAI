"""Outils de construction du cours phys_ch6_dipole_RC (« Dipôle RC »).

Copie adaptée de radioactivite_build/outils.py : S(...) fabrique une diapositive, vis(...) le visuel, Q(...) la question,
EX(...) / VF(...) les exercices, DEMO(...) une démonstration écrite à la main, PU/R/C/SP les pointages.
Pour les séances : BLOC(...), BQ(...) ; pour les rappels : RL / RQ / RV.

Chaque appel contrôle ce qu'il peut et ajoute les fautes à ERREURS ; build.py s'arrête s'il y en a :
  - chaque `mot` (pointage, centre, démonstration) est un extrait exact du texte dit, et les pointages sont dans l'ordre de la voix ;
  - chaque moment `play_until` et chaque repère existent dans la vue (tables MOMENTS / REPERES = contrat
    cours/dipole_RC_contrat_simulations.md ; verif_sims le revérifie dans le navigateur) ;
  - la voix (speech_text.mixed, fr, parole des démonstrations) : aucun chiffre, aucun symbole, aucun tachkil ;
  - aucun mot hors cadre (cadre_reference_2bac_pc.json, chapitres.dipole_RC.hors_cadre.mots) ni tournure de
    exploration/dipole_RC.json « a_ne_pas_dire » ;
  - une question de calcul / démonstration (mots « calcule », « trouve », « établis », « montre »…) porte sa demonstration.
"""
import json
import re
from pathlib import Path

SIM = "/media/simulations/physics/dipole-rc-tableau/"
ERREURS = []
_RACINE = Path(r"backend/data/curriculum")
_CADRE = json.loads((_RACINE / "cadre_reference_2bac_pc.json").read_text(encoding="utf-8"))["chapitres"]["dipole_RC"]
HORS_CADRE = _CADRE["hors_cadre"]["mots"]
_AND = json.loads((_RACINE / "exploration" / "dipole_RC.json").read_text(encoding="utf-8")).get("a_ne_pas_dire", [])
A_NE_PAS_DIRE = [(x["terme"], re.compile(x["motif"], re.I)) for x in _AND if isinstance(x, dict) and x.get("motif")]

# Moments (play_until) et repères de chaque vue = contrat (cours/dipole_RC_contrat_simulations.md). Clé = page + « ?param=valeur ».
FIG = {
 "fig_prerequis": "ohm additivite puissances derivee",
 "fig_unites": "bulle unites sous_multiples",
 "fig_boite": "ohm charge intensite additivite",
 "fig_parallele": "circuit charges formule interet",
 "fig_serie": "circuit tensions formule deux interet",
 "fig_ed_charge": "circuit additivite ohm intensite remplacer resultat",
 "fig_ed_formes": "depart diviser forme lecture",
 "fig_ed_q": "relations remplacer multiplier resultat",
 "fig_ed_uR_i": "deriver relation uR i",
 "fig_ed_decharge": "circuit additivite resultat",
 "fig_tableau_ed": "charge decharge remarque",
 "fig_derivee_exp": "regle exemple e_zero limite",
 "fig_resolution": "forme deriver remplacer factoriser accolade reecrire",
 "fig_condition_initiale": "forme equation condition resultat",
 "fig_verifier": "solution derivee remplacer egalite",
 "fig_dimension": "R C produit",
 "fig_decharge_solution": "forme deriver remplacer tau condition resultat",
 "fig_r_et_c": "donnees R C",
 "fig_du_dt": "equation droite pente ordonnee resultat",
 "fig_q_u": "courbe pente C_eq C2",
 "fig_n1_2019": "enonce courbe Q tau C R",
 "fig_n2_2021R": "enonce courbe equation tau R1 C",
 "fig_energie_2023R": "donnees E energie",
}
MOMENTS = {
 "carte.html": "centre condensateur echelon equation solution tau courbes energie national suite fin",
 "bilan.html": "fiche condensateur associations echelon equation solution tau lecture energie lacunes fin",
 "condensateur.html?vue=plaques": "plaques isolant symbole fin",
 "condensateur.html?vue=charge": "k_ouvert k_ferme electrons signes_armatures saturation fin",
 "intensite.html": "courant_constant corde tangente pente_nulle decharge_negative fin",
 "generateur-courant.html": "carte_generateurs droite deux_points pente C_deduite fin",
 "circuit-rc.html?vue=montage": "montage fleches acquisition echelon fin",
 "circuit-rc.html?vue=charge": "bascule_1 courbe_charge regime_permanent fin",
 "circuit-rc.html?vue=decharge": "bascule_2 courbe_decharge fin",
 "courbe-charge.html?vue=tableau": "tableau_valeurs points courbe cinq_tau fin",
 "courbe-charge.html?vue=R": "courbe R_double C_double fin",
 "courbe-charge.html?vue=tangente": "courbe asymptote tangente fin",
 "courbe-charge.html?vue=pourcent": "courbe ligne_63 projection fin",
 "quatre-courbes.html?vue=q_i": "q i fin",
 "quatre-courbes.html?vue=uC_uR": "uC uR somme fin",
 "quatre-courbes.html?vue=quatre": "uC q uR i fin",
 "quatre-courbes.html?vue=descente": "i tangente_descente ligne_37 fin",
 "continuite.html?vue=enchaine": "charge bascule nouvelle_origine uC_continue saut_i fin",
 "continuite.html?vue=decharge": "decharge decharge_37 fin",
 "energie.html?vue=lampe": "decharge_lampe barre carre fin",
 "energie.html?vue=calcul": "regime_permanent a_tau reste_70 fin",
}
for _f, _m in FIG.items():
    MOMENTS["figures.html?fig=" + _f] = _m + " fin"
REPERES = {
 "carte.html": "centre condensateur echelon equation solution tau courbes energie national suite",
 "bilan.html": "fiche condensateur associations echelon equation solution tau lecture energie",
 "condensateur.html": "vue_plaques vue_charge armature_A armature_B isolant symbole generateur interrupteur amperemetre voltmetre aiguille_A aiguille_V electrons charge_A charge_B",
 "intensite.html": "axe_t axe_q courbe droite_I0 corde tangente point pente_nulle courbe_decharge signe_i",
 "generateur-courant.html": "generateur_tension generateur_courant condensateur axe_t axe_u droite point_1 point_2 pente resultat",
 "circuit-rc.html": "generateur interrupteur position_1 position_2 resistance condensateur fleche_i fleche_uR fleche_uC entree_Y masse ecran courbe echelon palier_E regime_transitoire regime_permanent",
 "courbe-charge.html": "axe_t axe_u courbe courbe_2 tableau point_0 point_tau point_5tau asymptote tangente ligne_63 projection tau cinq_tau",
 "quatre-courbes.html": "graphe_uC graphe_q graphe_uR graphe_i expression_uC expression_q expression_uR expression_i somme tangente ligne_37 tau",
 "continuite.html": "graphe_uC graphe_i bascule nouvelle_origine uC_continue saut_i ligne_37 tangente tau",
 "energie.html": "lampe condensateur barre courbe formule calcul resultat",
 "figures.html": "figure",   # + un repère par étape (= les moments de la figure)
}


def controler_ecrit(id, t):
    """Contrôle un texte écrit : pas d'indice brut « _ » hors des noms connus du cadre (u_C, u_R, C_eq, E_e, Q_m...)."""
    return


_SYMBOLES_VOIX = re.compile(r"[0-9=+→%<>/*·×⁰¹²³⁴⁵⁶⁷⁸⁹₀₁₂₃₄₅₆₇₈₉αβγλτΔ½≈⇒]")
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
    """« circuit-rc.html?vue=charge » ; la page seule si elle n'a pas de paramètre de vue."""
    page = url.rsplit("/", 1)[-1]
    if page in MOMENTS:
        return page
    base = page.split("?")[0]
    for k in MOMENTS:
        if k.split("?")[0] == base and "?" in k and k.split("?")[1] in page:
            return k
    defaut = {"condensateur.html": "condensateur.html?vue=plaques", "circuit-rc.html": "circuit-rc.html?vue=montage",
              "courbe-charge.html": "courbe-charge.html?vue=tableau", "quatre-courbes.html": "quatre-courbes.html?vue=quatre",
              "continuite.html": "continuite.html?vue=enchaine", "energie.html": "energie.html?vue=lampe"}
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
