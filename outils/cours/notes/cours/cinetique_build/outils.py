"""Outils de construction du cours phys_ch10_cinetique (« Suivi temporel d'une transformation, vitesse de réaction »).

Copie adaptée de circuit_RLC_build/outils.py : S(...) fabrique une diapositive, vis(...) le visuel, Q(...) la question,
EX(...) / VF(...) les exercices, DEMO(...) une démonstration écrite à la main, PU/R/C/SP les pointages.
Contrôles : mots exacts et dans l'ordre ; moments et repères = contrat cours/cinetique_contrat_simulations.md ;
voix sans chiffre ni symbole ; aucun mot hors cadre (chapitres.cinetique) ni « a_ne_pas_dire » (exploration/cinetique.json) ;
une question de calcul porte sa demonstration.
"""
import json
import re
from pathlib import Path

SIM = "/media/simulations/chimie/cinetique-tableau/"
ERREURS = []
_RACINE = Path(r"backend/data/curriculum")
_CADRE = json.loads((_RACINE / "cadre_reference_2bac_pc.json").read_text(encoding="utf-8"))["chapitres"]["cinetique"]
HORS_CADRE = _CADRE["hors_cadre"]["mots"]
_AND = json.loads((_RACINE / "exploration" / "cinetique.json").read_text(encoding="utf-8")).get("a_ne_pas_dire", [])
A_NE_PAS_DIRE = [(x["terme"], re.compile(x["motif"], re.I)) for x in _AND if isinstance(x, dict) and x.get("motif")]

# Moments (play_until) et repères de chaque vue = contrat (cours/cinetique_contrat_simulations.md).
MOMENTS = {
 "suivi.html?vue=methodes": "titre titrage conductimetrie pression point_commun fin",
 "suivi.html?vue=mesures": "melange premiere_mesure mesures tableau_fini fin",
 "suivi.html?vue=prelevement": "reaction prelevement eau_glacee fige continue phrase fin",
 "suivi.html?vue=titrage": "burette verser equivalence equation relation resultat fin",
 "avancement.html?vue=tableau": "equation etat_initial en_cours etat_final fin",
 "avancement.html?vue=limitant": "tableau hypothese_1 hypothese_2 plus_petite limitant fin",
 "avancement.html?vue=lien": "tableau colonne_i2 egalite mesure fin",
 "avancement.html?vue=composition": "date lecture remplir verifier fin",
 "courbe.html?vue=points": "axes premiers_points tous_points courbe allure fin",
 "courbe.html?vue=lecture": "axes courbe date lecture valeur fin",
 "courbe.html?vue=palier": "axes courbe palier x_max egalite etat_final fin",
 "conductimetrie.html?vue=cellule": "montage plaques afficheur relation ions fin",
 "conductimetrie.html?vue=ions": "eau solution ajout monte conclusion fin",
 "conductimetrie.html?vue=formule": "formule exemple unites piege fin",
 "conductimetrie.html?vue=saponification": "melange descend loupe remplace na_spectateur final fin",
 "conductimetrie.html?vue=droite": "axes point_initial point_final droite relation inverse fin",
 "conductimetrie.html?vue=calcul": "courbe_sigma date lecture calcul report fin",
 "pression.html?vue=ballon": "montage ruban bulles monte palier equation fin",
 "pression.html?vue=relation": "gaz_parfait hydrogene relation unites application fin",
 "pression.html?vue=volume": "montage gaz lecture relation fin",
 "vitesse.html?vue=pente": "courbe debut_raide milieu fin_plate phrase fin",
 "vitesse.html?vue=definition": "formule volume derivee unite fin",
 "vitesse.html?vue=tangente": "courbe point tangente deux_points pente fin",
 "vitesse.html?vue=calcul": "relation pente application resultat piege fin",
 "vitesse.html?vue=diminue": "courbe tangente_0 tangente_8 tangente_20 conclusion fin",
 "vitesse.html?vue=concentration": "courbe_reactif debut plus_tard loupe conclusion fin",
 "vitesse.html?vue=fin": "courbe palier tangente_horizontale vitesse_nulle maximale_debut fin",
 "vitesse.html?vue=temperature": "axes courbe_20 courbe_40 tangentes comparer meme_final fin",
 "demi-reaction.html?vue=definition": "courbe palier moitie definition relation fin",
 "demi-reaction.html?vue=lecture": "x_f moitie horizontale verticale valeur fin",
 "demi-reaction.html?vue=piege": "courbe t_demi double pas_fini piege_axe fin",
 "demi-reaction.html?vue=comparer": "axes courbe_lente courbe_rapide deux_t_demi conclusion fin",
 "carte.html": "centre methodes trempe tableau mesure courbe vitesse diminue demi_reaction national suite complete fin",
 "bilan.html": "fiche suivi avancement mesure_x courbe vitesse evolution demi_reaction redaction lacunes fin",
 "figures.html": "axes courbe tangente lecture fin",
}
REPERES = {
 "suivi.html?vue=methodes": "vignette_titrage vignette_conductimetrie vignette_pression phrase afficheur manometre",
 "suivi.html?vue=mesures": "becher chrono tableau ligne_premiere ligne_derniere",
 "suivi.html?vue=prelevement": "grand_becher pipette becher_glace glacons teinte_figee teinte_continue phrase",
 "suivi.html?vue=titrage": "burette becher lecture_VE equation relation resultat",
 "avancement.html?vue=tableau": "equation ligne_initial ligne_en_cours ligne_final colonne_h2o2 colonne_iodure colonne_i2",
 "avancement.html?vue=limitant": "hypothese_1 hypothese_2 x_max limitant ligne_final",
 "avancement.html?vue=lien": "colonne_i2 egalite becher fleche",
 "avancement.html?vue=composition": "poignee_t courbe point_lu ligne_en_cours case_h2o2 case_iodure case_i2",
 "courbe.html?vue=points": "axe_t axe_x points courbe debut fin_courbe",
 "courbe.html?vue=lecture": "axe_t axe_x courbe poignee_t pointilles valeur",
 "courbe.html?vue=palier": "axe_t axe_x courbe palier ligne_x_max phrase",
 "conductimetrie.html?vue=cellule": "becher cellule plaques afficheur relation",
 "conductimetrie.html?vue=ions": "becher_eau becher_ions afficheur_1 afficheur_2 conclusion",
 "conductimetrie.html?vue=formule": "formule exemple unites piege",
 "conductimetrie.html?vue=saponification": "becher afficheur chrono loupe ion_ho ion_acetate ion_na equation",
 "conductimetrie.html?vue=droite": "axe_x axe_sigma point_initial point_final droite relation inverse",
 "conductimetrie.html?vue=calcul": "courbe_sigma poignee_t valeur_sigma calcul courbe_x point_x",
 "pression.html?vue=ballon": "ballon bouchon manometre afficheur ruban bulles equation",
 "pression.html?vue=relation": "gaz_parfait ligne_h2 relation unites application",
 "pression.html?vue=volume": "eprouvette cuve graduation relation",
 "vitesse.html?vue=pente": "courbe triangle poignee_t phrase",
 "vitesse.html?vue=definition": "formule morceau_V morceau_dx unite",
 "vitesse.html?vue=tangente": "courbe point_contact tangente point_A point_B pente",
 "vitesse.html?vue=calcul": "relation pente application resultat piege",
 "vitesse.html?vue=diminue": "courbe tangente_0 tangente_8 tangente_20 colonne conclusion",
 "vitesse.html?vue=concentration": "courbe_reactif loupe entites conclusion",
 "vitesse.html?vue=fin": "courbe palier tangente_horizontale phrase_nulle phrase_max",
 "vitesse.html?vue=temperature": "courbe_20 courbe_40 tangente_20 tangente_40 palier phrase",
 "demi-reaction.html?vue=definition": "courbe palier moitie definition relation",
 "demi-reaction.html?vue=lecture": "x_f moitie horizontale point verticale valeur",
 "demi-reaction.html?vue=piege": "courbe t_demi double valeur_double piege",
 "demi-reaction.html?vue=comparer": "courbe_lente courbe_rapide t_demi_lente t_demi_rapide conclusion",
 "carte.html": "centre methodes trempe tableau mesure courbe vitesse diminue demi_reaction national suite",
 "bilan.html": "fiche suivi avancement mesure_x courbe vitesse evolution demi_reaction redaction",
 "figures.html": "axe_t axe_y courbe tangente point valeur",
}


def controler_ecrit(id, t):
    """Contrôle un texte écrit : pas d'indice brut « _ » hors des noms connus du cadre (u_C, u_R, u_b, u_G, U_m, I_m, E_e, E_m...)."""
    return


_SYMBOLES_VOIX = re.compile(r"[0-9=+→⇌⇄%<>/*·×⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻₀₁₂₃₄₅₆₇₈₉αβγλτθΔ½≈⇒πφω√µ≤≥±−°]")
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
    if base == "figures.html":
        return base
    for k in MOMENTS:
        if k.split("?")[0] == base and "?" in k and k.split("?")[1] in page:
            return k
    defaut = {"figures.html": "figures.html"}
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
