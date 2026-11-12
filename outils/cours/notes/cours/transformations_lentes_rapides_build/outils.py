"""Outils de construction du cours phys_ch9_transformations_lentes_rapides (« Transformations lentes et transformations rapides »).

Copie adaptée de circuit_RLC_build/outils.py : S(...) fabrique une diapositive, vis(...) le visuel, Q(...) la question,
EX(...) / VF(...) les exercices, DEMO(...) une démonstration écrite à la main, PU/R/C/SP les pointages.
Contrôles : mots exacts et dans l'ordre ; moments et repères = contrat cours/transformations_lentes_rapides_contrat_simulations.md ;
voix sans chiffre ni symbole ; aucun mot hors cadre (chapitres.transformations_lentes_rapides) ni « a_ne_pas_dire » (exploration/transformations_lentes_rapides.json) ;
une question de calcul porte sa demonstration.
"""
import json
import re
from pathlib import Path

SIM = "/media/simulations/chimie/transformations-lentes-rapides-tableau/"
ERREURS = []
_RACINE = Path(r"backend/data/curriculum")
_CADRE = json.loads((_RACINE / "cadre_reference_2bac_pc.json").read_text(encoding="utf-8"))["chapitres"]["transformations_lentes_rapides"]
HORS_CADRE = _CADRE["hors_cadre"]["mots"]
_AND = json.loads((_RACINE / "exploration" / "transformations_lentes_rapides.json").read_text(encoding="utf-8")).get("a_ne_pas_dire", [])
A_NE_PAS_DIRE = [(x["terme"], re.compile(x["motif"], re.I)) for x in _AND if isinstance(x, dict) and x.get("motif")]

# Moments (play_until) et repères de chaque vue = contrat (cours/transformations_lentes_rapides_contrat_simulations.md).
MOMENTS = {
 "carte.html": "centre couple demi_equation equation rapide lente temperature concentration catalyseur trempe national suite complete fin",
 "bilan.html": "fiche oxydoreduction demi_equation equation rapide_lente facteur temperature concentration catalyseur trempe lacunes fin",
 "transfert.html?vue=zinc": "depart depot palit loupe electrons etiquettes bilan fin",
 "transfert.html?vue=couple": "oxydant gagne reducteur perd couple exemples oxydation_reduction fin",
 "bechers.html?vue=comparer": "depart verser rapide_fini lente_continue lente_finie fin",
 "bechers.html?vue=lente": "melange jaune brun palier fin",
 "bechers.html?vue=soufre": "melange trouble croix_cachee fin",
 "bechers.html?vue=echelle": "axe rapide lente tres_lente appareils fin",
 "facteurs.html?vue=temperature": "melange depart chaud_avance chaud_fini froid_fini meme_final agitation fin",
 "facteurs.html?vue=concentration": "melange depart concentre_avance concentre_fini dilue_fini meme_final rencontres fin",
 "facteurs.html?vue=trempe": "reaction prelevement eau_glacee fige continue titrage fin",
 "facteurs.html?vue=une_variable": "tableau comparer_1_2 comparer_2_3 comparer_1_3 conclusion fin",
 "facteurs.html?vue=vie": "frigo lait autocuiseur vapeur conclusion fin",
 "facteurs.html?vue=catalyseur": "melange ajout catalyse_avance catalyse_fini sans_fini meme_final equation fin",
 "courbes.html?vue=temperature": "axes courbe_froid courbe_chaud meme_palier plus_raide fin",
 "courbes.html?vue=concentration": "axes courbe_dilue courbe_concentre meme_palier piege fin",
 "courbes.html?vue=catalyseur": "axes courbe_C2 courbe_C1 meme_palier plus_tot piege fin",
 "courbes.html?vue=lecture": "enonce courbes debut associer conclusion fin",
}
for _v in ("permanganate", "eau_oxygenee", "iode", "oxalique"):
    MOMENTS["demi-equation.html?vue=" + _v] = "couple atomes oxygene hydrogene charges verifier fin"
for _v in ("zinc_cuivre", "eau_oxygenee", "permanganate", "fer"):
    MOMENTS["equation.html?vue=" + _v] = "couples reduction oxydation multiplier additionner simplifier verifier fin"
REPERES = {
 "carte.html": "centre couple demi_equation equation rapide lente temperature concentration catalyseur trempe national suite",
 "bilan.html": "fiche oxydoreduction demi_equation equation rapide_lente facteur temperature concentration catalyseur trempe",
 "transfert.html?vue=zinc": "becher lame solution depot loupe atome_zn ion_cu fleche_electrons ion_zn etiquette_reducteur etiquette_oxydant equation",
 "transfert.html?vue=couple": "ox red electrons double_fleche sens_reduction sens_oxydation couple_cu couple_zn couple_i definition",
 "demi-equation.html": "ligne_couple ligne_atomes ligne_oxygene ligne_hydrogene ligne_charges charge_gauche charge_droite electrons resultat balance",
 "equation.html": "demi_1 demi_2 facteur_1 facteur_2 electrons_1 electrons_2 trait bilan simplification charges oxydant reducteur",
 "bechers.html?vue=comparer": "becher_rapide becher_lent burette_fer burette_oxalique chrono etiquette_rapide etiquette_lente",
 "bechers.html?vue=lente": "becher teinte chrono etiquette",
 "bechers.html?vue=soufre": "becher croix trouble chrono",
 "bechers.html?vue=echelle": "axe_temps case_rapide case_lente case_tres_lente portail phrase",
 "facteurs.html?vue=temperature": "becher_froid becher_chaud thermometre_froid thermometre_chaud chrono teinte_froid teinte_chaud loupe poignee_theta",
 "facteurs.html?vue=concentration": "becher_dilue becher_concentre etiquette_dilue etiquette_concentre chrono loupe",
 "facteurs.html?vue=trempe": "grand_becher pipette becher_glace glacons teinte_figee teinte_continue burette phrase",
 "facteurs.html?vue=une_variable": "tableau ligne_1 ligne_2 ligne_3 colonne_theta colonne_c fleche_12 fleche_23 fleche_13 conclusion",
 "facteurs.html?vue=vie": "frigo lait autocuiseur flamme thermometre conclusion",
 "facteurs.html?vue=catalyseur": "becher_sans becher_avec gouttes chrono teinte_sans teinte_avec equation phrase",
 "courbes.html?vue=temperature": "axe_t axe_n courbe_froid courbe_chaud palier debut etiquette_froid etiquette_chaud",
 "courbes.html?vue=concentration": "axe_t axe_n courbe_dilue courbe_concentre palier courbe_piege",
 "courbes.html?vue=catalyseur": "axe_t axe_x courbe_C1 courbe_C2 palier debut piege",
 "courbes.html?vue=lecture": "axe_t axe_n courbe_a courbe_b courbe_c tableau palier conclusion",
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
    for k in MOMENTS:
        if k.split("?")[0] == base and "?" in k and k.split("?")[1] in page:
            return k
    defaut = {"transfert.html": "transfert.html?vue=zinc", "demi-equation.html": "demi-equation.html?vue=permanganate",
              "equation.html": "equation.html?vue=zinc_cuivre", "bechers.html": "bechers.html?vue=comparer",
              "facteurs.html": "facteurs.html?vue=temperature", "courbes.html": "courbes.html?vue=temperature"}
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
