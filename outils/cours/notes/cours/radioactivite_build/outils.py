"""Outils de construction du cours phys_ch4_radioactivite (« Décroissance radioactive »).

Même forme que energie_nucleaire_build/outils.py : S(...) fabrique une diapositive, vis(...) le visuel, Q(...) la question,
EX(...) / VF(...) les exercices de la diapositive, DEMO(...) une démonstration écrite à la main, PU/R/C/SP les pointages.
En plus, pour les séances (deck.seances) : BLOC(...), BQ(...) (exercice de bloc QCM) ; pour les rappels : RL / RQ / RV.

Chaque appel contrôle ce qu'il peut et ajoute les fautes à ERREURS ; build.py s'arrête s'il y en a :
  - chaque `mot` (pointage, centre, démonstration) est un extrait exact du texte dit, et les pointages sont dans l'ordre de la voix ;
  - chaque moment `play_until` et chaque repère existent dans la vue de la simulation (tables MOMENTS / REPERES, relevées
    le 11 novembre 2026 sur les pages de radioactivite-tableau/ ; verif_sims.py le revérifie dans le navigateur) ;
  - la voix (speech_text.mixed, fr, parole des démonstrations) : aucun chiffre, aucun symbole, aucun tachkil ;
  - aucun mot hors cadre (cadre_reference_2bac_pc.json, chapitres.radioactivite.hors_cadre.mots) ni tournure de
    exploration/radioactivite.json « a_ne_pas_dire », ni « U-238 » ;
  - chaque noyau écrit ᴬ_Z X a le bon Z pour son symbole, et chaque équation « … → … + … » écrite conserve A et Z (Soddy) ;
  - une question de calcul / démonstration (mots « calcule », « combien », « trouve », « complète », « composition »…)
    porte sa demonstration.
"""
import json
import re
from pathlib import Path

SIM = "/media/simulations/physics/radioactivite-tableau/"
ERREURS = []
_RACINE = Path(r"backend/data/curriculum")
_CADRE = json.loads((_RACINE / "cadre_reference_2bac_pc.json").read_text(encoding="utf-8"))["chapitres"]["radioactivite"]
HORS_CADRE = _CADRE["hors_cadre"]["mots"]
A_NE_PAS_DIRE = [(x["terme"], re.compile(x["motif"], re.I)) for x in
                 json.loads((_RACINE / "exploration" / "radioactivite.json").read_text(encoding="utf-8"))["a_ne_pas_dire"]]

# Moments (play_until) et repères de chaque vue, relevés dans le navigateur (voir verif_sims.py). Clé = page + « ?param=valeur ».
MOMENTS = {
 "carte.html": "definition noyau stabilite desintegrations famille loi demi_vie activite datation fin",
 "bilan.html": "fiche noyau stabilite radioactivite desintegrations famille loi demi_vie activite datation lacunes fin",
 "noyau.html?vue=atome": "atome zoom_noyau protons neutrons nucleons fin",
 "noyau.html?vue=notation": "symbole nombre_A nombre_Z formule_N exemple_U fin",
 "noyau.html?vue=isotopes": "hydrogene meme_Z A_different carbone definition fin",
 "segre.html?vue=vallee": "axes droite_N_egal_Z vallee legers lourds fin",
 "segre.html?vue=zones": "vallee zone_beta_moins zone_beta_plus zone_alpha fleches fin",
 "segre.html?vue=isotopes": "vallee ligne_isotopes fin",
 "segre.html?vue=famille": "depart premiere_alpha premiere_beta milieu arrivee bilan fin",
 "segre.html?vue=famille2024": "trace fleche_1 fleche_2 nucleide_X fin",
 "desintegration.html?type=alpha": "noyau_pere emission noyau_fils equation soddy_A soddy_Z conclusion fin",
 "desintegration.html?type=beta_moins": "noyau_pere transformation emission noyau_fils equation soddy_A soddy_Z conclusion fin",
 "desintegration.html?type=beta_plus": "noyau_pere transformation emission noyau_fils equation soddy_A soddy_Z conclusion fin",
 "desintegration.html?type=gamma": "noyau_pere emission noyau_excite emission_gamma equation soddy_A soddy_Z conclusion fin",
 "desintegration.html?type=soddy": "pere fils particule loi_A loi_Z fin",
 "desintegration.html?type=inconnu": "noyau_pere emission equation ligne_A ligne_Z tableau fils fin",
 "population.html?vue=hasard": "depart premier deuxieme plusieurs fin",
 "population.html?vue=grand_nombre": "depart un_t_demi deux_t_demi trois_t_demi loi fin",
 "population.html?vue=proportion": "depart ligne_1 ligne_2 ligne_3 conclusion fin",
 "population.html?vue=restants": "depart croisement deux_t_demi formule fin",
 "courbe.html?courbe=N": "axes courbe N0 moitie t_demi tangente tau fin",
 "courbe.html?courbe=paliers": "axes courbe palier_1 palier_2 palier_3 formule fin",
 "courbe.html?courbe=ln": "axes droite ordonnee pente identification fin",
 "courbe.html?courbe=activite_2021": "axes courbe a0 moitie t_demi fin",
 "courbe.html?courbe=activite_2022": "axes courbe a0 moitie t_demi fin",
 "activite.html": "echantillon compteur une_seconde definition plus_tard proportionnelle fin",
 "datation.html": "vivant echanges mort desintegration mesure formule application resultat fin",
 "figures.html?fig=fig_cas_types": "trace composition equation type famille t_demi lambda nombre date pourcentage fin",
 "figures.html?fig=fig_soddy_systeme": "equation systeme y x conclusion fin",
 "figures.html?fig=fig_rappel_exp_ln": "exp decroit ln ln_demi valeur fin",
 "figures.html?fig=fig_equation_diff": "pendant relation equation solution verification fin",
 "figures.html?fig=fig_demo_t_demi": "loi condition egalite ln resultat fin",
 "figures.html?fig=fig_unites": "trace conversion bq fin",
 "figures.html?fig=fig_masse_N": "quantite nombre exemple piege fin",
 "figures.html?fig=fig_activite_demo": "definition derivee resultat fin",
 "figures.html?fig=fig_datation_demo": "loi rapport ln resultat fin",
 "figures.html?fig=fig_pourcentages": "trace trente quatre_vingt_dix deux_t_demi fin",
 "figures.html?fig=fig_rapport_fils_pere": "pere fils rapport fin",
 "figures.html?fig=fig_enonce_2021": "trace donnees fin",
 "figures.html?fig=fig_enonce_2025": "trace donnees fin",
 "figures.html?fig=fig_enonce_2022": "trace donnees fin",
}
_R_POP = "vue_echantillon vue_courbe echantillon noyau_desintegre compteur courbe axe_t axe_N palier_1 palier_2 palier_3 N0 N0_sur_2 t_demi loi tableau courbe_restants courbe_desintegres croisement"
_R_DES = "vue_noyau pastille_type noyau_pere noyau_fils particule gamma transformation vue_equation equation soddy_A soddy_Z tableau_Z conclusion"
_R_SEG = "vue_diagramme axe_Z axe_N droite_N_Z vallee uranium_238 curseur"
_R_CRB = "vue_courbe lecture axe_t axe_N axe_a axe_ln courbe droite N0 a0 ordonnee moitie t_demi tangente tau palier_1 palier_2 palier_3 pente identification point_lu"
REPERES = {
 "carte.html": "centre definition noyau stabilite desintegrations famille loi demi_vie activite datation",
 "noyau.html?vue=atome": "vue_atome atome noyau proton neutron Z N A symbole",
 "noyau.html?vue=notation": "vue_notation symbole A Z N formule_N pastille_noyau noyau exemple",
 "noyau.html?vue=isotopes": "vue_isotopes isotope_1 isotope_2 isotope_3 carbone_12 carbone_14 proton neutron Z A definition",
 "segre.html?vue=vallee": _R_SEG + " legers lourds plomb_208",
 "segre.html?vue=zones": _R_SEG + " zone_beta_moins zone_beta_plus zone_alpha fleche_beta_moins fleche_beta_plus fleche_alpha",
 "segre.html?vue=isotopes": _R_SEG + " ligne_isotopes carbone_12 carbone_14 zoom_isotopes",
 "segre.html?vue=famille": "vue_diagramme axe_Z axe_N uranium_238 plomb_206 compteur_alpha compteur_beta fleche_alpha fleche_beta_moins bilan",
 "segre.html?vue=famille2024": "vue_diagramme axe_Z axe_A fleche_1 fleche_2 nucleide_X",
 "desintegration.html": _R_DES,
 "population.html": _R_POP,
 "courbe.html": _R_CRB,
 "activite.html": "vue_compteur calendrier echantillon compteur affichage vue_graphe graphe_a point_a definition",
 "figures.html": "figure",   # + un repère par étape (= les moments de la figure)
}

Z_ELEMENT = {"H": 1, "He": 2, "Li": 3, "Be": 4, "B": 5, "C": 6, "N": 7, "O": 8, "F": 9, "Ne": 10, "Na": 11, "Mg": 12, "Al": 13,
             "Si": 14, "P": 15, "S": 16, "Cl": 17, "Ar": 18, "K": 19, "Ca": 20, "Mn": 25, "Fe": 26, "Co": 27, "Ni": 28,
             "Kr": 36, "Sr": 38, "Y": 39, "Ag": 47, "Cd": 48, "Te": 52, "I": 53, "Xe": 54, "Cs": 55, "Ba": 56, "Ir": 77,
             "Tl": 81, "Pb": 82, "Bi": 83, "Po": 84, "At": 85, "Rn": 86, "Fr": 87, "Ra": 88, "Ac": 89, "Th": 90, "Pa": 91,
             "U": 92, "Np": 93, "Pu": 94, "Am": 95, "n": 0, "p": 1}
_SUP = str.maketrans("⁰¹²³⁴⁵⁶⁷⁸⁹⁻⁺", "0123456789-+")
_SUB = str.maketrans("₀₁₂₃₄₅₆₇₈₉₋₊", "0123456789-+")
_NOYAU = re.compile(r"([⁰¹²³⁴⁵⁶⁷⁸⁹]+)([₋₊]?[₀₁₂₃₄₅₆₇₈₉]+)\s?([A-Z][a-z]?|[enp])(\*?)")


def _noyaux(t):
    return [(int(a.translate(_SUP)), int(z.translate(_SUB)), sym) for a, z, sym, _ in _NOYAU.findall(t)]


def controler_ecrit(id, t):
    """Contrôle un texte écrit à l'écran : noyaux, équations, notation interdite."""
    if re.search(r"\b[A-Z][a-z]?-\d{1,3}\b|\b\d{1,3}[A-Z][a-z]?\b", t):
        ERREURS.append(f"{id}: notation interdite (U-238 / 238U) dans « {t[:60]} »")
    for A, Z, sym in _noyaux(t):
        if sym == "e":
            if (A, Z) not in ((0, -1), (0, 1)):
                ERREURS.append(f"{id}: particule e fausse ({A}, {Z}) dans « {t[:60]} »")
        elif sym not in Z_ELEMENT:
            ERREURS.append(f"{id}: symbole inconnu {sym} (ajoute-le à Z_ELEMENT) dans « {t[:60]} »")
        elif Z_ELEMENT[sym] != Z:
            ERREURS.append(f"{id}: {sym} a Z = {Z_ELEMENT[sym]}, pas {Z}, dans « {t[:60]} »")
        elif A < Z:
            ERREURS.append(f"{id}: A < Z pour {sym} dans « {t[:60]} »")
    # équations : chaque morceau « gauche → droite » dont tous les termes sont des noyaux connus (ou γ) doit conserver A et Z
    for morceau in re.split(r"[;:\n]|, (?=\D)|\.\s", t):
        if morceau.count("→") != 1 or "+" not in morceau:
            continue       # flèche d'un diagramme ou chaîne : pas une équation à vérifier
        g, d = morceau.split("→")
        cotes = []
        for cote in (g, d):
            termes = [x.strip(" ()«»?") for x in cote.split(" + ")]
            somme, ok = [0, 0], True
            for x in termes:
                if x in ("γ", ""):
                    continue
                m = re.fullmatch(r"(\d+\s?)?([⁰¹²³⁴⁵⁶⁷⁸⁹]+[₋₊]?[₀₁₂₃₄₅₆₇₈₉]+\s?(?:[A-Z][a-z]?|[enp])\*?)", x)
                if not m:
                    ok = False
                    break
                k = int(m.group(1) or 1)
                (A, Z, _), = _noyaux(m.group(2))
                somme[0] += k * A
                somme[1] += k * Z
            cotes.append(somme if ok else None)
        if None not in cotes and cotes[0] != cotes[1]:
            ERREURS.append(f"{id}: équation non équilibrée (A, Z) {cotes[0]} → {cotes[1]} dans « {morceau.strip()[:70]} »")


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
    """« noyau.html?vue=atome » ; la page seule si elle n'a pas de paramètre de vue."""
    page = url.rsplit("/", 1)[-1]
    if page in MOMENTS:
        return page
    base = page.split("?")[0]
    for k in MOMENTS:
        if k.split("?")[0] == base and "?" in k and k.split("?")[1] in page:
            return k
    defaut = {"noyau.html": "noyau.html?vue=atome", "segre.html": "segre.html?vue=vallee", "desintegration.html": "desintegration.html?type=alpha",
              "population.html": "population.html?vue=hasard", "courbe.html": "courbe.html?courbe=N"}
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


_CALCUL = re.compile(r"calcul|combien|trouve|compl[eè]t|composition|d[ée]termine|[ée]tablis|montre|que vaut|vaut :|coordonn|noyau fils|nombre de", re.I)


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
