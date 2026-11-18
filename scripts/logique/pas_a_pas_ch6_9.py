"""2ᵉ passe de la logique des cours RC, RL, RLC et ch9 (18 novembre 2026, skill logique-de-cours) : un exercice du
national JOUÉ pas à pas dans chaque cours, une diapositive par étape (simulation `national-pas-a-pas.html` du dossier
du cours, `?etape=k`) :
  - la diapositive « le sujet » : lu deux fois (règle 6 du professeur), sans question ;
  - une diapositive par question : la voix confirme la correction de l'étape d'avant (moment `rappel`, la construction
    se fait au tableau), puis pose UNE question (moment `question`) ; la réponse de l'élève vient avant la correction
    (question ouverte jugée sur `attendu`, ou QCM avec ses réactions préparées), puis la démonstration écrite comme le
    barème la lit ;
  - « la copie complète » après la dernière étape (règle 33 : le récapitulatif vient après).
Ne touche que les copies en attente ; les cours en ligne ne bougent pas. Relançable : les diapositives `*_np*` sont
d'abord retirées, puis reconstruites.
Usage : python -X utf8 scripts/logique/pas_a_pas_ch6_9.py
"""
import copy, json, sys
from pathlib import Path

R = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(Path(__file__).parent))
from outils import charger, diapos, verifier_mots, reactions  # noqa: E402

ATT = R / "backend/data/courses/en_attente"


def premier_mots(t, debut, n=4):
    """Le morceau exact de la voix qui déclenche un geste : les n premiers mots à partir de `debut`."""
    i = t.index(debut)
    return " ".join(t[i:].split()[:n])


def diapo(id_, titre, url, mixed, fr, *, lead, cahier, comp, pointage, question=None, slide_type="application",
          caption="", alt=""):
    s = {
        "id": id_, "slide_type": slide_type, "title": titre,
        "screen_content": {"lead": lead, "bullets": [], "student_trace": cahier},
        "visual": {"kind": "simulation", "url": url, "caption": caption or titre,
                   "alt": alt or "Le sujet du national redessiné à la craie, joué une étape à la fois, avec « Ta copie » à droite"},
        "speech_text": {"fr": fr, "mixed": mixed},
        "concentration": {"demarrer": "reset", "pointage": pointage, "centre": [], "cahier": cahier, "reponses": {}},
        "competence_ids": [comp],
    }
    if question:
        s["question"] = question
        if question.get("type") == "qcm":
            s["concentration"]["reponses"] = {"q": question.pop("_reactions")}
    for p in pointage:
        assert p["mot"] in mixed, (id_, p["mot"])
    return s


def ouverte(prompt, attendu, enonce_dit, parole, lignes, aides=(), pieges=()):
    q = {"type": "open", "prompt": prompt, "attendu": attendu, "timeout_seconds": 180, "advance_on_timeout": False,
         "enonce_dit": enonce_dit,
         "demonstration": {"parole": parole, "lignes": [{"texte": t, "mot": m} for t, m in lignes]}}
    if aides or pieges:
        q["clavier"] = {"aides": list(aides), "pieges": list(pieges)}
    for l in q["demonstration"]["lignes"]:
        assert l["mot"] in parole, (prompt, l["mot"])
    return q


def qcm(prompt, options, correct, enonce_dit, parole, lignes, rep):
    q = {"type": "qcm", "prompt": prompt, "options": options, "timeout_seconds": 60, "correct": correct,
         "enonce_dit": enonce_dit,
         "demonstration": {"parole": parole, "lignes": [{"texte": t, "mot": m} for t, m in lignes]},
         "_reactions": reactions(correct, len(options), rep)}
    for l in q["demonstration"]["lignes"]:
        assert l["mot"] in parole, (prompt, l["mot"])
    return q


def construire(deck, pre, url, sujet, etapes, fin):
    """sujet = (titre, mixed, fr, lead, cahier, comp) ; etapes = [dict] ; fin = (titre, mixed, fr, lead, cahier, comp)."""
    out = []
    t, mixed, fr, lead, cahier, comp = sujet
    out.append(diapo(f"{pre}_np0_sujet", t, f"{url}&etape=sujet", mixed, fr, lead=lead, cahier=cahier, comp=comp,
                     slide_type="situation",
                     pointage=[{"mot": premier_mots(mixed, "القراءة التانية"), "commande": "play_until", "parametres": {"moment": "donnees"}},
                               {"mot": premier_mots(mixed, "شنو كنقلبو"), "commande": "play_until", "parametres": {"moment": "questions"}}]))
    for k, e in enumerate(etapes, 1):
        p = []
        if e.get("courbe"):
            p.append({"mot": premier_mots(e["mixed"], e["courbe"]), "commande": "play_until", "parametres": {"moment": "courbe"}})
        if e.get("rappel"):
            p.append({"mot": premier_mots(e["mixed"], e["rappel"]), "commande": "play_until", "parametres": {"moment": "rappel"}})
        for mot, rep in e.get("reperes", []):
            p.append({"mot": premier_mots(e["mixed"], mot, 3), "repere": rep})
        p.append({"mot": premier_mots(e["mixed"], e["question_mot"]), "commande": "play_until", "parametres": {"moment": "question"}})
        p.sort(key=lambda x: e["mixed"].index(x["mot"]))
        out.append(diapo(f"{pre}_np{k}_{e['id']}", e["titre"], f"{url}&etape={k}", e["mixed"], e["fr"], lead=e["lead"],
                         cahier=e["cahier"], comp=e["comp"], pointage=p, question=e["q"]))
    t, mixed, fr, lead, cahier, comp = fin
    out.append(diapo(f"{pre}_np{len(etapes) + 1}_copie", t, f"{url}&etape=fin", mixed, fr, lead=lead, cahier=cahier, comp=comp,
                     slide_type="synthesis", pointage=[{"mot": premier_mots(mixed, "هادي هي la copie"), "repere": "copie"}]))
    for s in out:
        verifier_mots(s)
    return out


def inserer(m, nouvelles, act_id, act_titre, avant, duree, seances):
    """Retire les anciennes *_np*, ajoute l'activité avant `avant`, refait les séances données (les autres restent)."""
    for a in m["activities"]:
        a["slides"] = [s for s in a["slides"] if "_np" not in s["id"]]
    m["activities"] = [a for a in m["activities"] if a["id"] != act_id and a["slides"]]
    i = next(k for k, a in enumerate(m["activities"]) if a["id"] == avant)
    m["activities"].insert(i, {"id": act_id, "title": act_titre, "phase": "application", "duration_minutes": duree, "slides": nouvelles})
    m["estimated_minutes"] = sum(a["duration_minutes"] for a in m["activities"])
    D = diapos(m)
    for n, s in enumerate((s for a in m["activities"] for s in a["slides"])):
        s["order_index"] = n
    # séances : celles listées sont remplacées (dans l'ordre), les blocs gardent « retrouver » et « exercice » d'avant
    anciens = {b["id"]: b for se in m["seances"] for b in se["blocs"]}
    gardees = [se for se in m["seances"] if se["id"] not in {x[0] for x in seances}]
    # retirer les séances refaites, puis les remettre à la fin, dans l'ordre donné
    m["seances"] = gardees
    for sid, stitre, blocs in seances:
        bl = []
        for bid, btitre, ids in blocs:
            b = copy.deepcopy(anciens.get(bid, {}))
            b.update({"id": bid, "titre": btitre, "slide_ids": ids})
            cahier = []
            for x in ids:
                c = (D[x].get("concentration") or {}).get("cahier")
                if c and {"texte": c} not in cahier:
                    cahier.append({"texte": c})
            b["cahier"] = cahier
            if bid not in anciens:
                for k in ("retrouver", "exercice", "cahier_figures"):
                    b.pop(k, None)
            bl.append(b)
        m["seances"].append({"id": sid, "titre": stitre, "blocs": bl})
    ordre = [x for se in m["seances"] for b in se["blocs"] for x in b["slide_ids"]]
    tout = [s["id"] for a in m["activities"] for s in a["slides"]]
    assert ordre == tout, [(a, b) for a, b in zip(ordre, tout) if a != b][:3]
    for c in m["competences"]:
        c["slide_ids"] = [x for x in tout if c["id"] in (D[x].get("competence_ids") or [])]


def enregistrer(m, deck):
    (ATT / f"{deck}.json").write_text(json.dumps(m, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(deck, len([s for a in m["activities"] for s in a["slides"]]), "diapositives,", len(m["seances"]), "séances")


FIN_Q = "خود الوقت ديالك، ومن بعد جاوب."


# ════════════════════════════ Dipôle RC : national 2022 N, partie 1 ════════════════════════════
def rc():
    deck = "phys_ch6_dipole_RC"
    url = "/media/simulations/physics/dipole-rc-tableau/national-pas-a-pas.html?sujet=rc2022n"
    sujet = (
        "Le national 2022 N : lire le sujet deux fois",
        "دابا غادي نديرو exercice كامل من le national deux mille vingt-deux، خطوة بخطوة. القراءة الأولى: شنو هو الموضوع؟ "
        "la charge ديال condensateur، من خلال la résistance R. القراءة التانية: les données. E égale douze volts، "
        "و le condensateur خاوي فالبداية. عند t égale zéro، K ف la position un. فla figure جوج courbes: C un هي u C، "
        "و C deux هي i. و T هي la tangente ديال C un، ف t égale zéro. دابا شنو كنقلبو؟ تمنية ديال الأسئلة: l'équation، "
        "i de t، E و i zéro، R، tau بجوج ديال الطرق، C، و l'énergie. كل سؤال بوحدو: الجواب ديالك اللول، ومن بعد التصحيح.",
        "Maintenant, un exercice complet du national deux mille vingt-deux, pas à pas. Première lecture : de quoi parle-t-il ? "
        "La charge d'un condensateur à travers une résistance R. Deuxième lecture : les données. E égale douze volts, le "
        "condensateur est vide au départ ; à t égale zéro, K en position un. La figure a deux courbes : C un est u C, C deux "
        "est i, et T est la tangente à C un en t égale zéro. Ce qu'on cherche : huit questions. Chaque question seule : tu "
        "réponds d'abord, puis la correction.",
        "Les données, puis ce qu'on cherche : huit questions, une à la fois.",
        "National 2022 N : E = 12 V, C déchargé, K en (1) à t = 0 ; (C₁) = u_C(t), (C₂) = i(t), (T) tangente en t = 0.",
        "C7")
    E = [
        dict(id="equation", titre="2022 N, étape 1 : l'équation différentielle", comp="C4",
             lead="Le circuit fléché : à toi d'établir l'équation.",
             mixed="السؤال الأول: l'équation différentielle ديال u C. شوف le circuit: les flèches ديال i، ديال u R و ديال u C. "
                   "نفس الخطوات اللي درنا: la loi d'additivité، من بعد u R و i، ومن بعد نكتبو l'équation. كتب l'équation فالدفتر ديالك. " + FIN_Q,
             fr="Première question : l'équation différentielle de u C. Regarde le circuit, les flèches de i, de u R et de u C. "
                "Les mêmes étapes : la loi d'additivité, puis u R et i, puis on range. Écris l'équation dans ton cahier. Prends ton temps, puis réponds.",
             question_mot="السؤال الأول", reperes=[("شوف le circuit", "circuit")],
             cahier="1.1 : u_R + u_C = E ; u_R = R·i = RC·du_C/dt ; du_C/dt + u_C/(RC) = E/(RC).",
             q=ouverte("2022 N, question 1.1 : montre que du_C/dt + u_C/(RC) = E/(RC).",
                       "u_R + u_C = E ; u_R = R·i avec i = C·du_C/dt ; RC·du_C/dt + u_C = E ; du_C/dt + u_C/(RC) = E/(RC)",
                       "شوف هاد السؤال: montre que dé u C sur dé t، plus u C sur R C، égale E sur R C.",
                       "d'après la loi d'additivité des tensions: u R plus u C égale E. la loi d'Ohm: u R égale R i، "
                       "و i égale C dé u C sur dé t. كنعوضو: R C dé u C sur dé t، plus u C، égale E. "
                       "كنقسمو كلشي على R C: dé u C sur dé t، plus u C sur R C، égale E sur R C.",
                       [("Loi d'additivité : u_R + u_C = E", "d'après la loi d'additivité"),
                        ("Loi d'Ohm : u_R = R·i, avec i = C·du_C/dt", "la loi d'Ohm"),
                        ("RC·du_C/dt + u_C = E", "كنعوضو"),
                        ("On divise par RC : du_C/dt + u_C/(RC) = E/(RC)", "كنقسمو كلشي")],
                       aides=["u_R", "u_C", "du_C/dt", "RC"], pieges=["u_R − u_C", "= 0"])),
        dict(id="courant", titre="2022 N, étape 2 : l'expression de i(t)", comp="C5",
             lead="On dérive u_C(t), puis on multiplie par C.",
             mixed="شوف la figure: C un كتطلع نحو E، و C deux كتهبط نحو zéro. و فla copie، l'équation ديال السؤال الأول، "
                   "مكتوبة بحال ف التصحيح. السؤال التاني: la solution هي u C égale E fois un moins exponentielle de moins t sur R C. "
                   "حسب i de t، بدلالة E، R، C و t. " + FIN_Q,
             fr="Regarde la figure : C un monte vers E, C deux descend vers zéro. Dans la copie, l'équation de la première question, "
                "écrite comme le corrigé. Deuxième question : la solution est u C égale E fois un moins exponentielle de moins t sur R C. "
                "Établis i de t en fonction de E, R, C et t.",
             courbe="شوف la figure", rappel="و فla copie", question_mot="السؤال التاني",
             cahier="1.2.1 : i = C·du_C/dt = (E/R)·e^(−t/(RC)).",
             q=ouverte("2022 N, question 1.2.1 : u_C(t) = E·(1 − e^(−t/(RC))). Établis i(t) en fonction de E, R, C et t.",
                       "i = C·du_C/dt = (E/R)·e^(−t/(RC))",
                       "شوف هاد السؤال: u C égale E fois un moins exponentielle de moins t sur R C. حسب i de t.",
                       "i égale C dé u C sur dé t. كنحسبو la dérivée: dé u C sur dé t égale E sur R C، fois exponentielle de moins t sur R C. "
                       "كنضربو ف C: i de t égale E sur R، fois exponentielle de moins t sur R C.",
                       [("i = C·du_C/dt", "i égale C dé u C"),
                        ("du_C/dt = (E/(RC))·e^(−t/(RC))", "كنحسبو la dérivée"),
                        ("i(t) = (E/R)·e^(−t/(RC))", "كنضربو ف C")],
                       aides=["C·du_C/dt", "e^(−t/(RC))"], pieges=["E·e^(−t/(RC))"])),
        dict(id="lire", titre="2022 N, étape 3 : lire E et i(0)", comp="C7",
             lead="Lis l'axe avant la courbe : unité, valeur d'une graduation.",
             mixed="i de t égale E sur R، fois exponentielle de moins t sur R C: هادي هي. السؤال الجاي: قرا E على C un، "
                   "و i zéro على C deux. رد البال للوحدات ديال les axes: les volts و les milliampère. " + FIN_Q,
             fr="i de t égale E sur R fois exponentielle de moins t sur R C. Question suivante : lis E sur C un, et i zéro sur C deux. "
                "Attention aux unités des axes.",
             rappel="i de t égale", question_mot="السؤال الجاي",
             cahier="Lecture : E = 12 V (régime permanent de u_C) ; i(0) = 12 mA.",
             q=ouverte("Lis E sur (C₁), puis i(0) sur (C₂).", "E = 12 V (asymptote de u_C, régime permanent) ; i(0) = 12 mA",
                       "شوف هاد السؤال: قرا E على C un، و i zéro على C deux.",
                       "فle régime permanent، u C كتوقف عند l'asymptote: E égale douze volts. عند t égale zéro، C deux كتبدا من "
                       "douze milliampère: i zéro égale douze milliampère.",
                       [("Régime permanent : u_C = E = 12 V", "فle régime permanent"),
                        ("À t = 0 : i(0) = 12 mA", "عند t égale zéro")])),
        dict(id="R", titre="2022 N, étape 4 : la valeur de R", comp="C7",
             lead="Pars de i(t) à t = 0.",
             mixed="شوف: E égale douze volts على l'asymptote، و i zéro égale douze milliampère. السؤال الجاي: حسب R. "
                   "بدا من i de t، ف t égale zéro. " + FIN_Q,
             fr="Regarde : E égale douze volts sur l'asymptote, et i zéro égale douze milliampères. Question suivante : calcule R. "
                "Pars de i de t à t égale zéro.",
             rappel="شوف: E égale", question_mot="السؤال الجاي",
             cahier="1.2.2 : i(0) = E/R, donc R = E/i(0) = 12/(12·10⁻³) = 1,0·10³ Ω = 1 kΩ.",
             q=ouverte("2022 N, question 1.2.2 : déduis la valeur de R.",
                       "i(0) = E/R donc R = E/i(0) = 12/(12·10⁻³) = 1,0·10³ Ω = 1 kΩ",
                       "شوف هاد السؤال: حسب la valeur ديال R.",
                       "la relation: i zéro égale E sur R، fois exponentielle de zéro، يعني E sur R. إذن R égale E sur i zéro. "
                       "la conversion: douze milliampère égale douze fois dix puissance moins trois ampère. "
                       "l'application numérique: douze، sur douze fois dix puissance moins trois. le résultat: R égale mille ohm.",
                       [("i(0) = (E/R)·e⁰ = E/R, donc R = E/i(0)", "la relation"),
                        ("i(0) = 12 mA = 12·10⁻³ A", "la conversion"),
                        ("R = 12/(12·10⁻³)", "l'application numérique"),
                        ("R = 1,0·10³ Ω = 1 kΩ", "le résultat")],
                       aides=["E/i(0)", "10⁻³"], pieges=["i(0)/E"])),
        dict(id="tangente", titre="2022 N, étape 5 : τ par la tangente", comp="C7",
             lead="La tangente (T) à l'origine coupe l'asymptote : où ?",
             mixed="R égale mille ohm: كتبناه فla copie. السؤال الجاي: قرا tau ب la tangente T. شوف la droite T: "
                   "فين كتقطع l'asymptote ديال u C؟ " + FIN_Q,
             fr="R égale mille ohms : c'est écrit dans la copie. Question suivante : lis tau avec la tangente T. "
                "Regarde la droite T : où coupe-t-elle l'asymptote de u C ?",
             rappel="R égale mille", question_mot="السؤال الجاي", reperes=[("شوف la droite T", "droite_T")],
             cahier="τ par la tangente : (T) coupe l'asymptote u_C = E à t = τ ; τ = 50 ms.",
             q=ouverte("Lis τ avec la tangente (T) à l'origine.", "(T) coupe l'asymptote u_C = E à t = τ : τ = 50 ms",
                       "شوف هاد السؤال: قرا tau ب la tangente T.",
                       "la tangente à l'origine كتقطع l'asymptote u C égale E عند t égale tau. كنهبطو للمحور ديال الوقت: "
                       "tau égale cinquante millisecondes.",
                       [("(T) coupe l'asymptote u_C = E à t = τ", "la tangente à l'origine"),
                        ("τ = 50 ms", "كنهبطو للمحور")])),
        dict(id="pourcent", titre="2022 N, étape 6 : τ par les 63 %", comp="C7",
             lead="Une deuxième méthode, pour vérifier.",
             mixed="شوف: T كتقطع l'asymptote عند cinquante millisecondes. tau égale cinquante millisecondes. "
                   "السؤال الجاي: تأكد من tau بطريقة أخرى، soixante-trois pour cent. حسب zéro virgule soixante-trois fois E، "
                   "من بعد قرا الوقت على C un. " + FIN_Q,
             fr="Regarde : T coupe l'asymptote à cinquante millisecondes, tau égale cinquante millisecondes. Question suivante : "
                "vérifie tau par une autre méthode, soixante-trois pour cent. Calcule zéro virgule soixante-trois fois E, puis lis le temps sur C un.",
             rappel="شوف: T كتقطع", question_mot="السؤال الجاي",
             cahier="τ par les 63 % : u_C(τ) = E·(1 − e⁻¹) ≈ 0,63·E = 7,56 V ; on lit t = 50 ms = τ.",
             q=ouverte("Vérifie τ par la méthode des 63 %.", "u_C(τ) ≈ 0,63·E = 7,56 V ; on lit t = 50 ms = τ",
                       "شوف هاد السؤال: تأكد من tau ب soixante-trois pour cent.",
                       "u C de tau égale E fois un moins exponentielle de moins un، يعني تقريبا zéro virgule soixante-trois fois E. "
                       "l'application numérique: zéro virgule soixante-trois fois douze، تقريبا sept virgule six volts. "
                       "على C un، sept virgule six volts كيكون عند cinquante millisecondes: هو tau.",
                       [("u_C(τ) = E·(1 − e⁻¹) ≈ 0,63·E", "u C de tau"),
                        ("0,63 × 12 = 7,56 V", "l'application numérique"),
                        ("On lit t = 50 ms : c'est bien τ", "على C un")])),
        dict(id="C", titre="2022 N, étape 7 : montrer que C = 50 µF", comp="C7",
             lead="Tu as τ et R.",
             mixed="zéro virgule soixante-trois fois E عطاتنا نفس tau: cinquante millisecondes. السؤال الجاي: بين بلي C égale "
                   "cinquante micro farad. عندك tau و R. " + FIN_Q,
             fr="Zéro virgule soixante-trois fois E donne le même tau, cinquante millisecondes. Question suivante : montre que C égale "
                "cinquante micro farad. Tu as tau et R.",
             rappel="zéro virgule soixante-trois fois E عطاتنا", question_mot="السؤال الجاي",
             cahier="1.2.3 : τ = R·C, donc C = τ/R = (50·10⁻³)/10³ = 5·10⁻⁵ F = 50 µF.",
             q=ouverte("2022 N, question 1.2.3 : montre que C = 50 µF.", "τ = R·C donc C = τ/R = (50·10⁻³)/10³ = 5·10⁻⁵ F = 50 µF",
                       "شوف هاد السؤال: بين بلي C égale cinquante micro farad.",
                       "la relation: tau égale R C، إذن C égale tau sur R. la conversion: cinquante millisecondes égale cinquante fois "
                       "dix puissance moins trois seconde. l'application numérique: cinquante fois dix puissance moins trois، sur mille. "
                       "le résultat: C égale cinq fois dix puissance moins cinq farad، يعني cinquante micro farad.",
                       [("τ = R·C, donc C = τ/R", "la relation"),
                        ("τ = 50 ms = 50·10⁻³ s", "la conversion"),
                        ("C = (50·10⁻³)/10³", "l'application numérique"),
                        ("C = 5·10⁻⁵ F = 50 µF", "le résultat")])),
        dict(id="energie", titre="2022 N, étape 8 : l'énergie emmagasinée", comp="C8",
             lead="Question ajoutée : elle tombe dans d'autres sujets.",
             mixed="C égale cinquante micro farad: هادي هي القيمة اللي عطا le sujet. سؤال زايد، كيجي ف وطنيات أخرى: "
                   "حسب l'énergie ديال le condensateur فle régime permanent. " + FIN_Q,
             fr="C égale cinquante micro farad : c'est la valeur que donne le sujet. Une question ajoutée, qui tombe dans d'autres "
                "nationaux : calcule l'énergie du condensateur en régime permanent.",
             rappel="C égale cinquante micro farad:", question_mot="سؤال زايد",
             cahier="Énergie : E_e = ½·C·E² = ½ × 50·10⁻⁶ × 12² = 3,6·10⁻³ J = 3,6 mJ.",
             q=ouverte("Question ajoutée : calcule l'énergie emmagasinée dans le condensateur en régime permanent.",
                       "E_e = ½·C·u_C² avec u_C = E : E_e = ½ × 50·10⁻⁶ × 12² = 3,6·10⁻³ J",
                       "شوف هاد السؤال: حسب l'énergie ديال le condensateur فle régime permanent.",
                       "la relation: E e égale un demi C u C au carré، و فle régime permanent u C égale E. l'application numérique: "
                       "un demi fois cinquante fois dix puissance moins six، fois douze au carré. le résultat: trois virgule six fois "
                       "dix puissance moins trois joule، يعني trois virgule six millijoule.",
                       [("E_e = ½·C·u_C², avec u_C = E en régime permanent", "la relation"),
                        ("E_e = ½ × 50·10⁻⁶ × 12²", "l'application numérique"),
                        ("E_e = 3,6·10⁻³ J = 3,6 mJ", "le résultat")])),
    ]
    fin = ("2022 N : la copie complète",
           "l'énergie: trois virgule six millijoule. هادي هي la copie كاملة ديال هاد التمرين، بحال اللي كتلقى فالتصحيح. "
           "كل جواب فيه la relation، من بعد l'application numérique، من بعد le résultat مع l'unité. "
           "نفس الطريقة غادي نلقاوها ف le dipôle RL و ف le circuit RLC.",
           "L'énergie : trois virgule six millijoules. Voici la copie complète de l'exercice, comme la lit le correcteur. Chaque "
           "réponse a la relation, puis l'application numérique, puis le résultat avec son unité. On retrouvera la même démarche "
           "dans le dipôle RL et le circuit RLC.",
           "Chaque réponse : la relation, l'application numérique, le résultat avec son unité.",
           "2022 N : équation ; i(t) = (E/R)·e^(−t/(RC)) ; E = 12 V, i(0) = 12 mA ; R = 1 kΩ ; τ = 50 ms (tangente, 63 %) ; C = 50 µF ; E_e = 3,6 mJ.",
           "C7")
    for e in E:
        e.setdefault("question_mot", "السؤال")
    nouvelles = construire(deck, "rc", url, sujet, E, fin)
    m = charger(ATT / f"{deck}.json")
    ids = [s["id"] for s in nouvelles]
    inserer(m, nouvelles, "rc_partie8b", "IX. Le national 2022 N, joué pas à pas", "rc_partie9", 50, [
        ("rc_s7", "Séance 7 — L’énergie, puis le national 2022 N joué pas à pas", [
            ("rc_s4_b2b", "L’énergie emmagasinée", ["rc_l7_energie", "rc_l8_calcul"]),
            ("rc_np_b1", "2022 N : le sujet, l’équation, i(t), la lecture", ids[0:4]),
            ("rc_np_b2", "2022 N : R, puis τ par la tangente et par les 63 %", ids[4:7])]),
        ("rc_s8", "Séance 8 — La fin du 2022 N, deux sujets complets, le bilan", [
            ("rc_np_b3", "2022 N : C, l’énergie, la copie complète", ids[7:10]),
            ("rc_s4_b3", "Deux sujets du national", ["rc_n1_2019", "rc_n2_2021R"]),
            ("rc_s4_b4", "Le bilan et la carte", ["rc_b1_bilan", "rc_b2_carte"])]),
    ])
    for a in m["activities"]:
        if a["id"] == "rc_partie9":
            a["title"] = "X. Deux sujets complets du national"
        if a["id"] == "rc_bilan" and a["title"].startswith("X."):
            a["title"] = "XI." + a["title"][2:]
    enregistrer(m, deck)
    return ids


# ════════════════════════════ Dipôle RL : national 2023 N, partie 1 ════════════════════════════
def rl():
    deck = "phys_ch7_dipole_RL"
    url = "/media/simulations/physics/dipole-rl-tableau/national-pas-a-pas.html?sujet=rl2023n"
    sujet = (
        "Le national 2023 N : lire le sujet deux fois",
        "دابا exercice كامل من le national deux mille vingt-trois، خطوة بخطوة، بحال اللي درنا ف le dipôle RC. القراءة الأولى: "
        "شنو هو الموضوع؟ l'établissement ديال le courant ف dipôle RL. القراءة التانية: les données. E égale vingt-quatre volts، "
        "و la résistance ديال la bobine négligeable. K كتولي fermé عند t égale zéro. فla figure: la courbe ديال i، "
        "و T هي la tangente ف t égale zéro. دابا شنو كنقلبو؟ تسعة ديال الأسئلة: l'équation، la solution، tau و A و B، I zéro، "
        "tau بجوج ديال الطرق، L، u b de t، و l'énergie. نفس الترتيب ديال RC: غادي تعرف الخطوات.",
        "Maintenant, un exercice complet du national deux mille vingt-trois, pas à pas, comme dans le dipôle RC. Première "
        "lecture : l'établissement du courant dans un dipôle RL. Deuxième lecture : E égale vingt-quatre volts, la résistance de "
        "la bobine est négligeable ; on ferme K à t égale zéro ; la figure donne la courbe de i et sa tangente T. Ce qu'on "
        "cherche : neuf questions, dans le même ordre que pour le RC.",
        "Les données, puis ce qu'on cherche : neuf questions, dans l'ordre du RC.",
        "National 2023 N : E = 24 V, bobine (L, r négligeable), K fermé à t = 0 ; la courbe i(t) et sa tangente (T) en t = 0.",
        "C7")
    E = [
        dict(id="equation", titre="2023 N, étape 1 : l'équation différentielle", comp="C4",
             lead="Le circuit fléché : à toi d'établir l'équation.",
             mixed="السؤال الأول: l'équation différentielle ديال i. شوف le circuit: les flèches ديال i، ديال u R و ديال u b. "
                   "نفس الخطوات: la loi d'additivité، من بعد u b و u R، ومن بعد نكتبو l'équation. رد البال: r صغيرة بزاف. " + FIN_Q,
             fr="Première question : l'équation différentielle de i. Regarde le circuit et ses flèches. Les mêmes étapes : "
                "additivité, puis u b et u R, puis on range. Attention : r est négligeable.",
             question_mot="السؤال الأول", reperes=[("شوف le circuit", "circuit")],
             cahier="1-1 : u_b + u_R = E ; L·di/dt + R·i = E ; di/dt + (R/L)·i = E/L.",
             q=ouverte("2023 N, question 1-1 : établis l'équation différentielle vérifiée par i(t).",
                       "u_b + u_R = E ; u_b = L·di/dt (r négligeable), u_R = R·i ; di/dt + (R/L)·i = E/L",
                       "شوف هاد السؤال: كتب l'équation différentielle ديال i de t.",
                       "d'après la loi d'additivité des tensions: u b plus u R égale E. la bobine: u b égale L dé i sur dé t، "
                       "حيت r صغيرة بزاف. la loi d'Ohm: u R égale R i. كنعوضو: L dé i sur dé t، plus R i، égale E. "
                       "كنقسمو كلشي على L: dé i sur dé t، plus R sur L fois i، égale E sur L.",
                       [("Loi d'additivité : u_b + u_R = E", "d'après la loi d'additivité"),
                        ("u_b = L·di/dt (r négligeable) et u_R = R·i", "la bobine"),
                        ("L·di/dt + R·i = E", "كنعوضو"),
                        ("On divise par L : di/dt + (R/L)·i = E/L", "كنقسمو كلشي")],
                       aides=["u_b", "u_R", "di/dt"], pieges=["= 0", "r·i"])),
        dict(id="remplacer", titre="2023 N, étape 2 : dériver et remplacer", comp="C5",
             lead="La même méthode que pour le RC : dériver, remplacer.",
             mixed="شوف la courbe: i كتطلع، ومن بعد كتوقف عند واحد القيمة. و فla copie، l'équation: dé i sur dé t، plus R sur L "
                   "fois i، égale E sur L. السؤال التاني: la solution هي i égale A plus B exponentielle de moins t sur tau. "
                   "حسب dé i sur dé t، ومن بعد عوض فl'équation. " + FIN_Q,
             fr="Regarde la courbe : i monte, puis se stabilise. Dans la copie, l'équation. Deuxième question : la solution est i "
                "égale A plus B exponentielle de moins t sur tau. Calcule dé i sur dé t, puis remplace dans l'équation.",
             courbe="شوف la courbe", rappel="و فla copie", question_mot="السؤال التاني",
             cahier="di/dt = −(B/τ)·e^(−t/τ) ; B·e^(−t/τ)·(R/L − 1/τ) + (R/L)·A − E/L = 0.",
             q=ouverte("i(t) = A + B·e^(−t/τ). Calcule di/dt, puis remplace dans l'équation et regroupe.",
                       "di/dt = −(B/τ)·e^(−t/τ) ; B·e^(−t/τ)·(R/L − 1/τ) + (R/L)·A − E/L = 0",
                       "شوف هاد السؤال: حسب dé i sur dé t، وعوض فl'équation.",
                       "la dérivée: dé i sur dé t égale moins B sur tau، fois exponentielle de moins t sur tau. كنعوضو فl'équation: "
                       "moins B sur tau exponentielle، plus R sur L fois A plus B exponentielle، égale E sur L. كنجمعو les termes "
                       "اللي فيهم l'exponentielle: B exponentielle de moins t sur tau، fois R sur L moins un sur tau، plus R sur L "
                       "fois A، moins E sur L، égale zéro.",
                       [("di/dt = −(B/τ)·e^(−t/τ)", "la dérivée"),
                        ("−(B/τ)·e^(−t/τ) + (R/L)·(A + B·e^(−t/τ)) = E/L", "كنعوضو فl'équation"),
                        ("B·e^(−t/τ)·(R/L − 1/τ) + (R/L)·A − E/L = 0", "كنجمعو les termes")])),
        dict(id="constantes", titre="2023 N, étape 3 : τ, A et B", comp="C5",
             lead="L'égalité est vraie à tout instant t.",
             mixed="هادي هي العلاقة اللي كتبنا: B exponentielle، fois R sur L moins un sur tau، plus R sur L fois A، moins E sur L، "
                   "égale zéro. السؤال الجاي: هاد العلاقة صحيحة فكل لحظة. استنتج tau و A، ومن بعد B ب i de zéro égale zéro. " + FIN_Q,
             fr="Voici la relation écrite. Question suivante : elle est vraie à tout instant. Déduis tau et A, puis B avec i de zéro égale zéro.",
             rappel="هادي هي العلاقة", question_mot="السؤال الجاي",
             cahier="1-2-1 : τ = L/R ; A = E/R ; B = −E/R ; i(t) = (E/R)·(1 − e^(−t/τ)).",
             q=ouverte("2023 N, question 1-2-1 : détermine τ, puis A et B en fonction de E et R.",
                       "R/L − 1/τ = 0 donc τ = L/R ; R·A = E donc A = E/R ; i(0) = A + B = 0 donc B = −E/R",
                       "شوف هاد السؤال: لقا tau، A و B.",
                       "l'exponentielle عمرها ما كتولي zéro، إذن R sur L moins un sur tau égale zéro: tau égale L sur R. "
                       "و R sur L fois A moins E sur L égale zéro: A égale E sur R. la condition initiale: i de zéro égale zéro، "
                       "يعني A plus B égale zéro: B égale moins E sur R.",
                       [("R/L − 1/τ = 0, donc τ = L/R", "l'exponentielle عمرها"),
                        ("(R/L)·A − E/L = 0, donc A = E/R", "و R sur L fois A"),
                        ("i(0) = A + B = 0, donc B = −E/R", "la condition initiale")])),
        dict(id="lire", titre="2023 N, étape 4 : lire I₀", comp="C7",
             lead="Lis l'axe avant la courbe.",
             mixed="tau égale L sur R، A égale E sur R، و B égale moins E sur R. السؤال الجاي: قرا I zéro، l'intensité ديال "
                   "le régime permanent. رد البال للوحدة: milliampère. " + FIN_Q,
             fr="Tau égale L sur R, A égale E sur R, B égale moins E sur R. Question suivante : lis I zéro, l'intensité du régime "
                "permanent. Attention à l'unité, le milliampère.",
             rappel="tau égale L sur R،", question_mot="السؤال الجاي",
             cahier="Lecture : I₀ = A = E/R = 48 mA.",
             q=ouverte("Lis l'intensité I₀ du régime permanent.", "i tend vers I₀ = E/R ; I₀ = 48 mA",
                       "شوف هاد السؤال: قرا I zéro.",
                       "فle régime permanent، i كتوقف عند l'asymptote: I zéro égale A، يعني E sur R. على la courbe: "
                       "I zéro égale quarante huit milliampère.",
                       [("Régime permanent : i → I₀ = A = E/R", "فle régime permanent"),
                        ("I₀ = 48 mA", "على la courbe")])),
        dict(id="tangente", titre="2023 N, étape 5 : τ par la tangente", comp="C7",
             lead="La tangente (T) à l'origine coupe l'asymptote : où ?",
             mixed="شوف: I zéro égale quarante huit milliampère. السؤال الجاي: قرا tau ب la tangente T، بحال ف RC. "
                   "شوف la droite T: فين كتقطع l'asymptote؟ " + FIN_Q,
             fr="Regarde : I zéro égale quarante huit milliampères. Question suivante : lis tau avec la tangente T, comme pour le RC. "
                "Où coupe-t-elle l'asymptote ?",
             rappel="شوف: I zéro", question_mot="السؤال الجاي", reperes=[("شوف la droite T", "droite_T")],
             cahier="τ par la tangente : (T) coupe l'asymptote i = I₀ à t = τ ; τ = 2 ms.",
             q=ouverte("Lis τ avec la tangente (T) à l'origine.", "(T) coupe l'asymptote i = I₀ à t = τ : τ = 2 ms",
                       "شوف هاد السؤال: قرا tau ب la tangente T.",
                       "la tangente à l'origine كتقطع l'asymptote i égale I zéro عند t égale tau. كنهبطو للمحور ديال الوقت: "
                       "tau égale deux millisecondes.",
                       [("(T) coupe l'asymptote i = I₀ à t = τ", "la tangente à l'origine"),
                        ("τ = 2 ms", "كنهبطو للمحور")])),
        dict(id="pourcent", titre="2023 N, étape 6 : τ par les 63 %", comp="C7",
             lead="Une deuxième méthode, pour vérifier.",
             mixed="شوف: T كتقطع l'asymptote عند deux millisecondes. السؤال الجاي: تأكد من tau ب soixante-trois pour cent. "
                   "حسب zéro virgule soixante-trois fois I zéro، من بعد قرا الوقت. " + FIN_Q,
             fr="Regarde : T coupe l'asymptote à deux millisecondes. Question suivante : vérifie tau avec soixante-trois pour cent.",
             rappel="شوف: T كتقطع", question_mot="السؤال الجاي",
             cahier="τ par les 63 % : i(τ) ≈ 0,63·I₀ ≈ 30 mA ; on lit t = 2 ms = τ.",
             q=ouverte("Vérifie τ par la méthode des 63 %.", "i(τ) ≈ 0,63·I₀ ≈ 30 mA ; on lit t = 2 ms = τ",
                       "شوف هاد السؤال: تأكد من tau ب soixante-trois pour cent.",
                       "i de tau égale I zéro fois un moins exponentielle de moins un، يعني تقريبا zéro virgule soixante-trois fois "
                       "I zéro. l'application numérique: zéro virgule soixante-trois fois quarante huit، تقريبا trente milliampère. "
                       "على la courbe، trente milliampère كيكون عند deux millisecondes: هو tau.",
                       [("i(τ) = I₀·(1 − e⁻¹) ≈ 0,63·I₀", "i de tau"),
                        ("0,63 × 48 ≈ 30 mA", "l'application numérique"),
                        ("On lit t = 2 ms : c'est bien τ", "على la courbe")])),
        dict(id="L", titre="2023 N, étape 7 : montrer que L = 1 H", comp="C7",
             lead="Tu as τ, E et I₀.",
             mixed="zéro virgule soixante-trois fois I zéro عطاتنا نفس tau: deux millisecondes. السؤال الجاي: بين بلي L égale "
                   "un henry. عندك tau، E و I zéro. " + FIN_Q,
             fr="Zéro virgule soixante-trois fois I zéro donne le même tau, deux millisecondes. Question suivante : montre que L égale "
                "un henry. Tu as tau, E et I zéro.",
             rappel="zéro virgule soixante-trois fois I zéro", question_mot="السؤال الجاي",
             cahier="1-2-2 : τ = L/R et R = E/I₀, donc L = τ·E/I₀ = 2·10⁻³ × 24/(48·10⁻³) = 1 H.",
             q=ouverte("2023 N, question 1-2-2 : montre que L = 1 H.", "τ = L/R et R = E/I₀ donc L = τ·E/I₀ = 2·10⁻³ × 24/(48·10⁻³) = 1 H",
                       "شوف هاد السؤال: بين بلي L égale un henry.",
                       "la relation: tau égale L sur R، إذن L égale tau fois R. و I zéro égale E sur R، إذن R égale E sur I zéro: "
                       "vingt-quatre sur quarante huit fois dix puissance moins trois، يعني cinq cents ohm. l'application numérique: "
                       "L égale deux fois dix puissance moins trois، fois cinq cents. le résultat: L égale un henry.",
                       [("τ = L/R, donc L = τ·R", "la relation"),
                        ("R = E/I₀ = 24/(48·10⁻³) = 500 Ω", "و I zéro égale E sur R"),
                        ("L = 2·10⁻³ × 500", "l'application numérique"),
                        ("L = 1 H", "le résultat")])),
        dict(id="ub", titre="2023 N, étape 8 : l'expression de u_b(t)", comp="C5",
             lead="u_b = L·di/dt : dériver i(t).",
             mixed="L égale un henry: هادي هي القيمة اللي عطا le sujet. السؤال الجاي: la tension ديال la bobine، u b de t، "
                   "ف le sujet سميتها u L. عطي l'expression numérique ديالها، و t ب seconde. " + FIN_Q,
             fr="L égale un henry, la valeur du sujet. Question suivante : la tension de la bobine, u b de t, notée u L dans le sujet. "
                "Donne son expression numérique en unités du système international.",
             rappel="L égale un henry:", question_mot="السؤال الجاي",
             cahier="1-3 : u_b = L·di/dt = E·e^(−t/τ) ; u_b(t) = 24·e^(−500·t).",
             q=ouverte("2023 N, question 1-3 : donne, en unités SI, l'expression numérique de u_b(t) (notée u_L dans le sujet).",
                       "u_b = L·di/dt = L·(E/R)·(1/τ)·e^(−t/τ) = E·e^(−t/τ) ; u_b(t) = 24·e^(−500·t)",
                       "شوف هاد السؤال: عطي l'expression numérique ديال u b de t.",
                       "la relation: u b égale L dé i sur dé t. la dérivée: dé i sur dé t égale E sur R، fois un sur tau، fois "
                       "exponentielle de moins t sur tau. و L sur R fois un sur tau égale un، حيت tau égale L sur R. إذن u b égale "
                       "E exponentielle de moins t sur tau. un sur tau égale un sur deux fois dix puissance moins trois، يعني cinq cents. "
                       "le résultat: u b de t égale vingt-quatre، exponentielle de moins cinq cents t.",
                       [("u_b = L·di/dt", "la relation"),
                        ("di/dt = (E/R)·(1/τ)·e^(−t/τ)", "la dérivée"),
                        ("u_b = E·e^(−t/τ), car L/(R·τ) = 1", "إذن u b égale"),
                        ("1/τ = 1/(2·10⁻³) = 500 s⁻¹", "un sur tau égale"),
                        ("u_b(t) = 24·e^(−500·t)", "le résultat")])),
        dict(id="energie", titre="2023 N, étape 9 : l'énergie de la bobine", comp="C8",
             lead="Question ajoutée : elle tombe dans d'autres sujets.",
             mixed="u b de t égale vingt-quatre exponentielle de moins cinq cents t. سؤال زايد، بحال ف RC: حسب l'énergie "
                   "اللي مخزونة ف la bobine فle régime permanent. " + FIN_Q,
             fr="u b de t égale vingt-quatre exponentielle de moins cinq cents t. Une question ajoutée, comme pour le RC : calcule "
                "l'énergie emmagasinée dans la bobine en régime permanent.",
             rappel="u b de t égale vingt-quatre", question_mot="سؤال زايد",
             cahier="Énergie : E_m = ½·L·I₀² = ½ × 1 × (48·10⁻³)² ≈ 1,2·10⁻³ J.",
             q=ouverte("Question ajoutée : calcule l'énergie emmagasinée dans la bobine en régime permanent.",
                       "E_m = ½·L·I₀² = ½ × 1 × (48·10⁻³)² ≈ 1,2·10⁻³ J",
                       "شوف هاد السؤال: حسب l'énergie ديال la bobine فle régime permanent.",
                       "la relation: E m égale un demi L i au carré، و فle régime permanent i égale I zéro. l'application numérique: "
                       "un demi fois un، fois quarante huit fois dix puissance moins trois، au carré. le résultat: تقريبا un virgule "
                       "deux fois dix puissance moins trois joule.",
                       [("E_m = ½·L·i², avec i = I₀ en régime permanent", "la relation"),
                        ("E_m = ½ × 1 × (48·10⁻³)²", "l'application numérique"),
                        ("E_m ≈ 1,2·10⁻³ J", "le résultat")])),
    ]
    fin = ("2023 N : la copie complète",
           "l'énergie: تقريبا un virgule deux millijoule. هادي هي la copie كاملة ديال هاد التمرين، بحال اللي كتلقى فالتصحيح. "
           "شوف la copie ديال RC: نفس الخطوات. l'équation، la solution، la lecture، tau بجوج ديال الطرق، "
           "la grandeur اللي كنقلبو عليها، و l'énergie.",
           "L'énergie : environ un virgule deux millijoule. Voici la copie complète, comme la lit le correcteur. Compare-la avec "
           "celle du RC : les mêmes étapes.",
           "Les mêmes étapes que le RC : équation, solution, lecture, τ deux fois, la grandeur cherchée, l'énergie.",
           "2023 N : di/dt + (R/L)·i = E/L ; τ = L/R, A = E/R, B = −E/R ; I₀ = 48 mA ; τ = 2 ms ; L = 1 H ; u_b(t) = 24·e^(−500·t) ; E_m ≈ 1,2 mJ.",
           "C7")
    nouvelles = construire(deck, "rl", url, sujet, E, fin)
    m = charger(ATT / f"{deck}.json")
    ids = [s["id"] for s in nouvelles]
    inserer(m, nouvelles, "rl_partie8b", "IX. Le national 2023 N, joué pas à pas", "rl_partie9", 55, [
        ("rl_s6", "Séance 6 — Étincelle et diode, l’énergie, puis le national 2023 N joué pas à pas", [
            ("rl_s3_b4", "Étincelle, diode et le national 2025 R", ["rl_t3_diode", "rl_t4_national"]),
            ("rl_s4_b2b", "L’énergie magnétique", ["rl_l7_energie", "rl_l8_double"]),
            ("rl_np_b1", "2023 N : le sujet, l’équation, la solution", ids[0:4])]),
        ("rl_s7", "Séance 7 — La fin du 2023 N, deux sujets complets, le bilan", [
            ("rl_np_b2", "2023 N : I₀, puis τ par la tangente et par les 63 %, L", ids[4:8]),
            ("rl_np_b3", "2023 N : u_b(t), l’énergie, la copie complète", ids[8:11]),
            ("rl_s4_b3", "Deux sujets du national, puis le bilan", ["rl_n1_2022R", "rl_n2_2024N", "rl_bl_fiche", "rl_cr_carte"])]),
    ])
    for a in m["activities"]:
        if a["id"] == "rl_partie9" and a["title"].startswith("IX."):
            a["title"] = "X." + a["title"][3:]
        if a["id"] == "rl_bilan" and a["title"].startswith("X."):
            a["title"] = "XI." + a["title"][2:]
    enregistrer(m, deck)
    return ids


# ════════════════════════════ Circuit RLC : national 2022 N, partie 2 ════════════════════════════
def rlc():
    deck = "phys_ch8_circuit_RLC"
    url = "/media/simulations/physics/circuit-rlc-tableau/national-pas-a-pas.html?sujet=rlc2022n"
    sujet = (
        "Le national 2022 N : lire le sujet deux fois",
        "دابا exercice كامل من le national deux mille vingt-deux، خطوة بخطوة، بحال ف RC و RL. القراءة الأولى: شنو هو الموضوع؟ "
        "la décharge ديال condensateur مشارجي ف bobine. القراءة التانية: les données. C égale cinquante micro farad، مشارجي ب douze volts. "
        "الحالة الأولى: r égale zéro، و فla figure trois تلاتة ديال les courbes. الحالة التانية: r ماشي zéro، و فla figure quatre "
        "u C و i. دابا شنو كنقلبو؟ تسعة ديال الأسئلة: l'équation، الاختيار ديال la courbe، T zéro، la lecture، L، "
        "l'énergie totale، les lectures، l'énergie dissipée، و l'entretien.",
        "Maintenant, un exercice complet du national deux mille vingt-deux, pas à pas, comme pour le RC et le RL. Première "
        "lecture : un condensateur chargé se décharge dans une bobine. Deuxième lecture : C égale cinquante micro farad, chargé "
        "sous douze volts ; premier cas r égale zéro, figure trois avec trois courbes ; deuxième cas r non nul, figure quatre "
        "avec u C et i. Ce qu'on cherche : neuf questions.",
        "Les données, puis ce qu'on cherche : neuf questions, une à la fois.",
        "National 2022 N : C = 50 µF chargé sous 12 V, décharge dans une bobine (L, r) ; r = 0 (figure 3), puis r ≠ 0 (figure 4).",
        "C5")
    rep_choix = {
        1: ("Juste. r = 0 : pas de perte, l'amplitude reste constante, et à t = 0 u_C = 12 V : c'est (C₁).",
            "مزيان. r égale zéro: ما كاين حتى perte، l'amplitude كتبقى ثابتة. و عند t égale zéro، u C égale douze volts، "
            "حيت le condensateur مشارجي. إذن هي C un."),
        0: (("(C₂) a une amplitude qui diminue. Avec r = 0, y a-t-il une perte d'énergie ? Regarde l'amplitude.",
             "شوف C deux: l'amplitude ديالها كتنقص. ولكن r égale zéro. واش كاينة شي perte ديال l'énergie؟ شوف l'amplitude مزيان، وعاود."),
            ("Faux. (C₂) est amortie : il faudrait r ≠ 0. Ici r = 0, l'amplitude reste constante et u_C(0) = 12 V : c'est (C₁).",
             "لا. C deux فيها l'amortissement، و هادا خاصو r ماشي zéro. هنا r égale zéro، l'amplitude ثابتة، و u C de zéro "
             "égale douze volts. الجواب هو C un.")),
        2: (("(C₃) part de 0 à t = 0. Que vaut u_C(0) si le condensateur est chargé sous 12 V ?",
             "شوف C trois: كتبدا من zéro عند t égale zéro. ولكن le condensateur مشارجي ب douze volts. شحال كتساوي u C de zéro؟ عاود."),
            ("Faux. À t = 0, le condensateur est chargé : u_C(0) = 12 V, pas 0. Et r = 0 : amplitude constante. C'est (C₁).",
             "لا. عند t égale zéro، le condensateur مشارجي: u C de zéro égale douze volts، ماشي zéro. و r égale zéro: "
             "l'amplitude ثابتة. الجواب هو C un.")),
    }
    E = [
        dict(id="equation", titre="2022 N, étape 1 : l'équation différentielle (r = 0)", comp="C3",
             lead="Le circuit fléché : à toi d'établir l'équation.",
             mixed="السؤال الأول: r égale zéro. l'équation différentielle ديال u C. شوف le circuit: le condensateur و la bobine، "
                   "و les flèches ديال u C و u b. نفس الخطوات: la loi d'additivité، من بعد كل tension، ومن بعد نكتبو l'équation. "
                   "رد البال: ما كاينش le générateur. " + FIN_Q,
             fr="Première question : r égale zéro. L'équation différentielle de u C. Regarde le circuit et ses flèches. Les mêmes "
                "étapes : additivité, puis chaque tension, puis on range. Attention : il n'y a pas de générateur.",
             question_mot="السؤال الأول", reperes=[("شوف le circuit", "circuit")],
             cahier="2.1.1 : u_b + u_C = 0 ; LC·d²u_C/dt² + u_C = 0 ; d²u_C/dt² + u_C/(LC) = 0.",
             q=ouverte("2022 N, question 2.1.1 (r = 0) : montre que d²u_C/dt² + u_C/(LC) = 0.",
                       "u_b + u_C = 0 ; u_b = L·di/dt et i = C·du_C/dt donc di/dt = C·d²u_C/dt² ; d²u_C/dt² + u_C/(LC) = 0",
                       "شوف هاد السؤال: montre que dé deux u C sur dé t deux، plus u C sur L C، égale zéro.",
                       "d'après la loi d'additivité des tensions: ما كاينش le générateur، إذن u b plus u C égale zéro. la bobine: "
                       "u b égale L dé i sur dé t، حيت r égale zéro. و i égale C dé u C sur dé t، إذن dé i sur dé t égale C dé deux "
                       "u C sur dé t deux. كنعوضو: L C dé deux u C sur dé t deux، plus u C، égale zéro. كنقسمو كلشي على L C.",
                       [("Loi d'additivité : u_b + u_C = 0", "d'après la loi d'additivité"),
                        ("u_b = L·di/dt (r = 0)", "la bobine"),
                        ("i = C·du_C/dt, donc di/dt = C·d²u_C/dt²", "و i égale C"),
                        ("LC·d²u_C/dt² + u_C = 0", "كنعوضو"),
                        ("On divise par LC : d²u_C/dt² + u_C/(LC) = 0", "كنقسمو كلشي")],
                       aides=["u_b", "u_C", "d²u_C/dt²", "LC"], pieges=["= E", "R·i"])),
        dict(id="choix", titre="2022 N, étape 2 : choisir la courbe", comp="C4",
             lead="Trois courbes : laquelle est u_C(t) quand r = 0 ?",
             mixed="شوف la figure trois: تلاتة ديال les courbes. و فla copie، l'équation ديال السؤال الأول. السؤال التاني: "
                   "شمن courbe هي u C de t؟ فكر ف جوج حوايج: r égale zéro، و le condensateur مشارجي عند t égale zéro. " + FIN_Q,
             fr="Regarde la figure trois : trois courbes. Dans la copie, l'équation de la première question. Deuxième question : "
                "quelle courbe est u C de t ? Pense à deux choses : r égale zéro, et le condensateur est chargé à t égale zéro.",
             courbe="شوف la figure trois", rappel="و فla copie", question_mot="السؤال التاني",
             cahier="2.1.2 : r = 0, amplitude constante, u_C(0) = 12 V : c'est (C₁).",
             q=qcm("2022 N, question 2.1.2 : quelle courbe représente u_C(t) quand r = 0 ?", ["(C₂)", "(C₁)", "(C₃)"], 1,
                   "شوف هاد السؤال: شمن courbe هي u C de t، ملي r égale zéro؟",
                   "r égale zéro: ما كاين حتى perte، l'amplitude كتبقى ثابتة. هادشي كيحيد C deux. عند t égale zéro، le condensateur "
                   "مشارجي: u C de zéro égale douze volts. هادشي كيحيد C trois. إذن u C de t هي C un.",
                   [("r = 0 : pas de perte, l'amplitude reste constante : ce n'est pas (C₂)", "r égale zéro"),
                    ("À t = 0, le condensateur est chargé : u_C(0) = 12 V : ce n'est pas (C₃)", "عند t égale zéro"),
                    ("u_C(t) est représentée par (C₁)", "إذن u C de t")],
                   rep_choix)),
        dict(id="T0", titre="2022 N, étape 3 : l'expression de T₀", comp="C4",
             lead="Dériver deux fois un cosinus, puis remplacer.",
             mixed="هي C un: l'amplitude ثابتة، و u C de zéro égale douze volts. السؤال الجاي: la solution هي u C égale U zéro "
                   "cos de deux pi sur T zéro fois t. لقا T zéro بدلالة L و C. دير la dérivée seconde، وعوض فl'équation. " + FIN_Q,
             fr="C'est C un : amplitude constante, u C de zéro égale douze volts. Question suivante : la solution est u C égale U zéro "
                "cosinus de deux pi sur T zéro fois t. Trouve T zéro en fonction de L et C.",
             rappel="هي C un:", question_mot="السؤال الجاي",
             cahier="2.1.3.a : d²u_C/dt² = −(2π/T₀)²·u_C ; (2π/T₀)² = 1/(LC) ; T₀ = 2π·√(LC).",
             q=ouverte("2022 N, question 2.1.3.a : u_C = U₀·cos(2π·t/T₀). Trouve T₀ en fonction de L et C.",
                       "d²u_C/dt² = −(2π/T₀)²·u_C ; [1/(LC) − (2π/T₀)²]·u_C = 0 ; T₀ = 2π·√(LC)",
                       "شوف هاد السؤال: لقا T zéro بدلالة L و C.",
                       "la dérivée seconde: dé deux u C sur dé t deux égale moins deux pi sur T zéro au carré، fois u C. كنعوضو "
                       "فl'équation: un sur L C، moins deux pi sur T zéro au carré، fois u C، égale zéro. u C ماشي ديما zéro، إذن "
                       "deux pi sur T zéro au carré égale un sur L C. le résultat: T zéro égale deux pi racine de L C.",
                       [("d²u_C/dt² = −(2π/T₀)²·u_C", "la dérivée seconde"),
                        ("(1/(LC) − (2π/T₀)²)·u_C = 0", "كنعوضو فl'équation"),
                        ("u_C n'est pas toujours nulle : (2π/T₀)² = 1/(LC)", "u C ماشي ديما"),
                        ("T₀ = 2π·√(LC)", "le résultat")])),
        dict(id="lire", titre="2022 N, étape 4 : lire T₀", comp="C5",
             lead="Lis l'axe, puis mesure sur plusieurs périodes.",
             mixed="T zéro égale deux pi racine de L C: كتبناها. السؤال الجاي: قرا T zéro على C un. باش تكون la lecture مزيانة، "
                   "قرا جوج ديال les périodes، ومن بعد قسم على جوج. " + FIN_Q,
             fr="T zéro égale deux pi racine de L C : c'est écrit. Question suivante : lis T zéro sur C un. Pour bien lire, mesure "
                "deux périodes, puis divise par deux.",
             rappel="T zéro égale deux pi racine", question_mot="السؤال الجاي",
             cahier="Lecture sur (C₁) : 2T₀ = 20 ms, donc T₀ = 10 ms.",
             q=ouverte("Lis T₀ sur (C₁), sur deux périodes.", "2T₀ = 20 ms donc T₀ = 10 ms",
                       "شوف هاد السؤال: قرا T zéro على C un.",
                       "على C un، جوج ديال les périodes كيبداو من t égale zéro، وكيوصلو ل vingt millisecondes. إذن deux T zéro "
                       "égale vingt millisecondes. le résultat: T zéro égale dix millisecondes.",
                       [("Sur (C₁) : 2T₀ = 20 ms", "على C un"),
                        ("T₀ = 10 ms", "le résultat")])),
        dict(id="L", titre="2022 N, étape 5 : montrer que L = 0,05 H", comp="C5",
             lead="Le carré d'abord, puis on isole L.",
             mixed="شوف: deux T zéro égale vingt millisecondes، إذن T zéro égale dix millisecondes. السؤال الجاي: بين بلي L égale "
                   "zéro virgule zéro cinq henry. خود pi deux égale dix. " + FIN_Q,
             fr="Regarde : deux T zéro égale vingt millisecondes, donc T zéro égale dix millisecondes. Question suivante : montre que L "
                "égale zéro virgule zéro cinq henry. Prends pi carré égale dix.",
             rappel="شوف: deux T zéro", question_mot="السؤال الجاي",
             cahier="2.1.3.b : T₀² = 4π²·L·C, donc L = T₀²/(4π²·C) = (10·10⁻³)²/(4 × 10 × 50·10⁻⁶) = 0,05 H.",
             q=ouverte("2022 N, question 2.1.3.b : montre que L = 0,05 H (π² = 10).",
                       "T₀² = 4π²·L·C donc L = T₀²/(4π²·C) = (10·10⁻³)²/(4 × 10 × 50·10⁻⁶) = 0,05 H",
                       "شوف هاد السؤال: بين بلي L égale zéro virgule zéro cinq henry.",
                       "la relation: T zéro au carré égale quatre pi carré، fois L، fois C. إذن L égale T zéro au carré، sur quatre pi "
                       "carré C. la conversion: dix millisecondes égale dix fois dix puissance moins trois seconde. l'application "
                       "numérique: dix fois dix puissance moins trois، au carré، sur quatre fois dix fois cinquante fois dix puissance "
                       "moins six. le résultat: L égale zéro virgule zéro cinq henry.",
                       [("T₀² = 4π²·L·C, donc L = T₀²/(4π²·C)", "la relation"),
                        ("T₀ = 10 ms = 10·10⁻³ s", "la conversion"),
                        ("L = (10·10⁻³)²/(4 × 10 × 50·10⁻⁶)", "l'application numérique"),
                        ("L = 0,05 H", "le résultat")])),
        dict(id="energie", titre="2022 N, étape 6 : l'énergie totale (r ≠ 0)", comp="C6",
             lead="Deux réservoirs : le condensateur et la bobine.",
             mixed="شوف la figure quatre: r ماشي zéro، u C و i كينقصو. و فla copie، L égale zéro virgule zéro cinq henry. "
                   "السؤال الجاي: كتب l'énergie totale ديال le circuit، بدلالة C، u C، L و i. " + FIN_Q,
             fr="Regarde la figure quatre : r non nul, u C et i diminuent. Dans la copie, L égale zéro virgule zéro cinq henry. "
                "Question suivante : écris l'énergie totale du circuit en fonction de C, u C, L et i.",
             courbe="شوف la figure quatre", rappel="و فla copie", question_mot="السؤال الجاي",
             cahier="2.2.1 : E_t = E_e + E_m = ½·C·u_C² + ½·L·i².",
             q=ouverte("2022 N, question 2.2.1 : écris l'énergie totale E_t en fonction de C, u_C, L et i.",
                       "E_t = E_e + E_m = ½·C·u_C² + ½·L·i²",
                       "شوف هاد السؤال: كتب l'énergie totale ديال le circuit.",
                       "l'énergie totale هي المجموع ديال جوج: l'énergie ديال le condensateur، و l'énergie ديال la bobine. "
                       "E t égale un demi C u C au carré، plus un demi L i au carré.",
                       [("E_t = E_e + E_m", "l'énergie totale"),
                        ("E_t = ½·C·u_C² + ½·L·i²", "E t égale")])),
        dict(id="lectures", titre="2022 N, étape 7 : lire u_C et i à t₀ et à t₁", comp="C7",
             lead="Lis les deux courbes au même instant.",
             mixed="E t égale un demi C u C au carré، plus un demi L i au carré. السؤال الجاي: قرا u C و i عند t zéro égale zéro، "
                   "ومن بعد عند t un égale neuf millisecondes. رد البال للوحدات: les volts و les milliampère. " + FIN_Q,
             fr="E t égale un demi C u C carré plus un demi L i carré. Question suivante : lis u C et i à t zéro égale zéro, puis à t un "
                "égale neuf millisecondes. Attention aux unités.",
             rappel="E t égale un demi", question_mot="السؤال الجاي",
             cahier="Lecture : t₀ = 0 : u_C = 12 V, i = 0 ; t₁ = 9 ms : u_C = 6 V, i = 140 mA.",
             q=ouverte("Lis u_C et i à t₀ = 0, puis à t₁ = 9 ms.", "t₀ = 0 : u_C = 12 V et i = 0 ; t₁ = 9 ms : u_C = 6 V et i = 140 mA",
                       "شوف هاد السؤال: قرا u C و i عند t zéro، ومن بعد عند t un.",
                       "عند t zéro égale zéro: u C égale douze volts، و i égale zéro. عند t un égale neuf millisecondes: u C égale "
                       "six volts، و i égale cent quarante milliampère.",
                       [("t₀ = 0 : u_C = 12 V et i = 0", "عند t zéro"),
                        ("t₁ = 9 ms : u_C = 6 V et i = 140 mA", "عند t un")])),
        dict(id="dissipee", titre="2022 N, étape 8 : l'énergie dissipée", comp="C7",
             lead="L'énergie à t₀, l'énergie à t₁, puis la différence.",
             mixed="شوف les points: douze volts و zéro عند t zéro، six volts و cent quarante milliampère عند t un. السؤال الجاي: "
                   "حسب l'énergie dissipée بين t zéro و t un. حسب E zéro، من بعد E un، من بعد الفرق. " + FIN_Q,
             fr="Regarde les points : douze volts et zéro à t zéro, six volts et cent quarante milliampères à t un. Question suivante : "
                "calcule l'énergie dissipée entre t zéro et t un. Calcule E zéro, puis E un, puis la différence.",
             rappel="شوف les points", question_mot="السؤال الجاي",
             cahier="2.2.2 : E₀ = ½ × 50·10⁻⁶ × 12² = 3,6 mJ ; E₁ = ½ × 50·10⁻⁶ × 6² + ½ × 0,05 × 0,14² ≈ 1,39 mJ ; ΔE = E₁ − E₀ ≈ −2,2 mJ.",
             q=ouverte("2022 N, question 2.2.2 : trouve l'énergie ΔE dissipée entre t₀ = 0 et t₁ = 9 ms.",
                       "E₀ = ½·C·12² = 3,6 mJ ; E₁ = ½·C·6² + ½·L·(0,14)² ≈ 1,39 mJ ; ΔE = E₁ − E₀ ≈ −2,2 mJ",
                       "شوف هاد السؤال: حسب l'énergie dissipée بين t zéro و t un.",
                       "عند t zéro: i égale zéro، إذن E zéro égale un demi C fois douze au carré، يعني trois virgule six millijoule. "
                       "عند t un: E un égale un demi C fois six au carré، plus un demi L fois zéro virgule quatorze au carré. "
                       "يعني zéro virgule neuf، plus zéro virgule quarante-neuf: un virgule trente neuf millijoule. "
                       "le résultat: delta E égale E un moins E zéro، تقريبا moins deux virgule deux millijoule. "
                       "la signe moins: l'énergie نقصات، مشات chaleur، effet Joule.",
                       [("E₀ = ½ × 50·10⁻⁶ × 12² = 3,6·10⁻³ J (i = 0)", "عند t zéro"),
                        ("E₁ = ½ × 50·10⁻⁶ × 6² + ½ × 0,05 × 0,14²", "عند t un"),
                        ("E₁ = 0,9 + 0,49 ≈ 1,39 mJ", "يعني zéro virgule neuf"),
                        ("ΔE = E₁ − E₀ ≈ −2,2 mJ", "le résultat"),
                        ("Signe moins : énergie dissipée par effet Joule", "la signe moins")])),
        dict(id="entretien", titre="2022 N, étape 9 : entretenir les oscillations", comp="C8",
             lead="Question ajoutée : l'entretien tombe dans d'autres sujets.",
             mixed="delta E تقريبا moins deux virgule deux millijoule: هادي هي l'énergie dissipée. سؤال زايد، كيجي ف وطنيات أخرى: "
                   "شنو خاصنا نزيدو ف le circuit، باش l'amplitude تبقى ثابتة؟ و شحال غادي تكون la période؟ " + FIN_Q,
             fr="Delta E vaut environ moins deux virgule deux millijoules : c'est l'énergie dissipée. Une question ajoutée : que faut-il "
                "ajouter au circuit pour garder l'amplitude constante ? Et quelle sera la période ?",
             rappel="delta E تقريبا", question_mot="سؤال زايد",
             cahier="Entretien : un générateur u_G = k·i rend l'énergie dissipée ; k = résistance totale du circuit ; oscillations sinusoïdales de période T₀ = 10 ms.",
             q=ouverte("Question ajoutée : que faut-il ajouter pour garder l'amplitude constante ? Avec quelle période ?",
                       "un générateur d'entretien u_G = k·i, avec k égal à la résistance totale du circuit ; oscillations sinusoïdales de période T₀ = 10 ms",
                       "شوف هاد السؤال: شنو خاصنا نزيدو باش l'amplitude تبقى ثابتة؟",
                       "كنزيدو générateur ديال l'entretien: u G égale k i. كيرد l'énergie اللي كتضيع ف la résistance. k خاصها تساوي "
                       "la résistance totale ديال le circuit. إذن les oscillations كيوليو sinusoïdales، و la période ديالهم هي T zéro، "
                       "dix millisecondes.",
                       [("Générateur d'entretien : u_G = k·i", "كنزيدو générateur"),
                        ("Il rend l'énergie dissipée : k = résistance totale du circuit", "كيرد l'énergie"),
                        ("Oscillations sinusoïdales, période T₀ = 10 ms", "إذن les oscillations")])),
    ]
    fin = ("2022 N : la copie complète",
           "l'entretien: générateur u G égale k i، و la période T zéro. هادي هي la copie كاملة ديال هاد التمرين، بحال اللي كتلقى فالتصحيح"
           ". نفس الخطوات ديال RC و RL: l'équation، la solution، la lecture، la grandeur اللي كنقلبو عليها، و l'énergie.",
           "L'entretien : un générateur u G égale k i, et la période T zéro. Voici la copie complète, comme la lit le correcteur. "
           "Les mêmes étapes que le RC et le RL.",
           "Les mêmes étapes que le RC et le RL : équation, solution, lecture, la grandeur cherchée, l'énergie.",
           "2022 N : d²u_C/dt² + u_C/(LC) = 0 ; (C₁) ; T₀ = 2π·√(LC) = 10 ms ; L = 0,05 H ; E_t = ½·C·u_C² + ½·L·i² ; ΔE ≈ −2,2 mJ ; entretien u_G = k·i.",
           "C5")
    nouvelles = construire(deck, "lc", url, sujet, E, fin)
    m = charger(ATT / f"{deck}.json")
    ids = [s["id"] for s in nouvelles]
    inserer(m, nouvelles, "lc_partie9b", "X. Le national 2022 N, joué pas à pas", "lc_partie10", 55, [
        ("lc_s7", "Séance 7 — Le national 2022 N, joué pas à pas", [
            ("lc_np_b1", "2022 N : le sujet, l’équation, le choix de la courbe", ids[0:3]),
            ("lc_np_b2", "2022 N : T₀, sa lecture, L", ids[3:6]),
            ("lc_np_b3", "2022 N : l’énergie totale, les lectures, l’énergie dissipée", ids[6:9])]),
        ("lc_s8", "Séance 8 — L’entretien, la copie, deux sujets complets, le bilan", [
            ("lc_np_b4", "2022 N : l’entretien, la copie complète", ids[9:11]),
            ("lc_s4_b3", "Deux sujets du national", ["lc_n1_2020N", "lc_n2_2025N"]),
            ("lc_s4_b4", "Le bilan et la carte", ["lc_bl_fiche", "lc_cr_carte"])]),
    ])
    for a in m["activities"]:
        if a["id"] == "lc_partie10" and a["title"].startswith("X."):
            a["title"] = "XI." + a["title"][2:]
        if a["id"] == "lc_bilan" and a["title"].startswith("XI."):
            a["title"] = "XII." + a["title"][3:]
    enregistrer(m, deck)
    return ids


# ════════════════════════════ Ch9 : exercice type national, eau oxygénée et ions iodure ════════════════════════════
def ch9():
    deck = "phys_ch9_transformations_lentes_rapides"
    url = "/media/simulations/chimie/transformations-lentes-rapides-tableau/national-pas-a-pas.html?sujet=iodure"
    sujet = (
        "Un exercice type national : lire le sujet deux fois",
        "دابا exercice بحال اللي كيجي ف le national، خطوة بخطوة. فيه الأسئلة اللي كتجي بزاف ف هاد le chapitre. القراءة الأولى: "
        "شنو هو الموضوع؟ l'eau oxygénée مع les ions iodure، transformation lente. القراءة التانية: les données. cent millilitres، "
        "deux millimoles ديال l'eau oxygénée، و les ions iodure ب zéro virgule un mole par litre. les ions H plus en excès. "
        "le diiode كيعطي لون brun، وكنتبعو la quantité ديالو مع الوقت. جوج ديال les expériences: vingt degrés و quarante degrés. "
        "دابا شنو كنقلبو؟ تسعة ديال الأسئلة: les demi-équations، l'équation، le tableau d'avancement سطر بسطر، x max، "
        "la courbe، la température، نفس الحالة النهائية، و la trempe.",
        "Maintenant, un exercice comme au national, pas à pas, avec les questions qui tombent le plus dans ce chapitre. Première "
        "lecture : l'eau oxygénée et les ions iodure, une transformation lente. Deuxième lecture : cent millilitres, deux millimoles "
        "d'eau oxygénée, ions iodure à zéro virgule un mole par litre, ions H plus en excès ; le diiode est brun, on suit sa "
        "quantité ; deux expériences, à vingt et à quarante degrés. Ce qu'on cherche : neuf questions.",
        "Les données, puis ce qu'on cherche : neuf questions, une à la fois.",
        "Exercice type national : V = 100 mL, n₀(H₂O₂) = 2 mmol, [I⁻]₀ = 0,1 mol/L, H⁺ en excès ; on suit n(I₂) ; 20 °C et 40 °C.",
        "C7")
    rep_courbe = {
        0: ("Juste. (a) atteint sa valeur finale plus tôt : la transformation est plus rapide, donc à 40 °C.",
            "مزيان. a كتوصل للقيمة النهائية ديالها قبل: la transformation كتمشي بالزربة. إذن a هي quarante degrés. "
            "la température facteur cinétique."),
        1: (("(b) monte plus lentement. À une température plus haute, la transformation va-t-elle plus vite ou moins vite ?",
             "شوف b: كتطلع بشوية. ملي la température كتطلع، la transformation كتمشي بالزربة ولا بشوية؟ عاود."),
            ("Faux. (b) monte plus lentement : c'est 20 °C. (a) atteint sa valeur finale plus tôt : c'est 40 °C.",
             "لا. b كتطلع بشوية: هي vingt degrés. a كتوصل قبل للقيمة النهائية: هي quarante degrés.")),
        2: (("Les deux courbes n'ont pas la même montée. Laquelle arrive la première à sa valeur finale ?",
             "شوف: جوج ديال les courbes ماشي كيطلعو بحال بحال. شكون فيهم كتوصل اللولى للقيمة النهائية؟ عاود."),
            ("Faux. On peut trancher : (a) atteint sa valeur finale plus tôt, la transformation est plus rapide : c'est 40 °C.",
             "لا. نقدرو نعرفو: a كتوصل قبل للقيمة النهائية، يعني plus rapide: هي quarante degrés.")),
    }
    E = [
        dict(id="demi", titre="Étape 1 : les deux demi-équations", comp="C2",
             lead="Les deux couples, en milieu acide.",
             mixed="السؤال الأول: كتب la demi-équation ديال كل couple، en milieu acide. le couple eau oxygénée sur eau، و le couple "
                   "diiode sur ion iodure. نفس les étapes اللي درنا: les atomes، les oxygènes، les H plus، و les électrons. " + FIN_Q,
             fr="Première question : écris la demi-équation de chaque couple, en milieu acide. Les mêmes gestes : atomes, oxygènes, "
                "H plus, électrons.",
             question_mot="السؤال الأول", reperes=[("le couple eau oxygénée", "donnees")],
             cahier="H₂O₂ + 2H⁺ + 2e⁻ ⇌ 2H₂O ; I₂ + 2e⁻ ⇌ 2I⁻.",
             q=ouverte("Écris la demi-équation de chaque couple : H₂O₂/H₂O et I₂/I⁻, en milieu acide.",
                       "H₂O₂ + 2H⁺ + 2e⁻ ⇌ 2H₂O ; I₂ + 2e⁻ ⇌ 2I⁻",
                       "شوف هاد السؤال: كتب la demi-équation ديال كل couple.",
                       "le couple eau oxygénée sur eau: deux oxygènes، إذن deux molécules d'eau. كنزيدو deux H plus، و deux électrons. "
                       "le couple diiode sur ion iodure: deux atomes ديال I، إذن deux ions iodure، و deux électrons.",
                       [("H₂O₂ + 2H⁺ + 2e⁻ ⇌ 2H₂O", "le couple eau oxygénée"),
                        ("I₂ + 2e⁻ ⇌ 2I⁻", "le couple diiode")])),
        dict(id="equation", titre="Étape 2 : l'équation de la réaction", comp="C3",
             lead="Un couple donne les électrons, l'autre les reçoit.",
             mixed="les demi-équations مكتوبين فla copie. السؤال الجاي: l'eau oxygénée كتاخد les électrons، و les ions iodure "
                   "كيعطيو les électrons. كتب l'équation ديال la réaction. " + FIN_Q,
             fr="Les demi-équations sont écrites dans la copie. Question suivante : l'eau oxygénée prend les électrons, les ions "
                "iodure les donnent. Écris l'équation de la réaction.",
             rappel="les demi-équations مكتوبين", question_mot="السؤال الجاي",
             cahier="2I⁻ → I₂ + 2e⁻ ; H₂O₂ + 2I⁻ + 2H⁺ → I₂ + 2H₂O.",
             q=ouverte("Écris l'équation de la réaction entre l'eau oxygénée et les ions iodure.",
                       "H₂O₂ + 2I⁻ + 2H⁺ → I₂ + 2H₂O",
                       "شوف هاد السؤال: كتب l'équation ديال la réaction.",
                       "les ions iodure كيعطيو deux électrons: deux I moins donne I deux، plus deux électrons. l'eau oxygénée كتاخد les électrons. "
                       "نفس العدد ديال les électrons، إذن كنجمعو: l'eau oxygénée، plus deux ions iodure، plus deux H plus، donne "
                       "le diiode، plus deux molécules d'eau.",
                       [("2I⁻ → I₂ + 2e⁻", "les ions iodure كيعطيو"),
                        ("H₂O₂ + 2H⁺ + 2e⁻ → 2H₂O", "l'eau oxygénée كتاخد"),
                        ("H₂O₂ + 2I⁻ + 2H⁺ → I₂ + 2H₂O", "نفس العدد")])),
        dict(id="initial", titre="Étape 3 : le tableau, l'état initial", comp="C6",
             lead="La première ligne : les quantités au départ, en mmol.",
             mixed="هادي هي l'équation: فوق le tableau d'avancement. السؤال الجاي: عمر السطر الأول، l'état initial، ب millimole. "
                   "شحال ديال l'eau oxygénée؟ وشحال ديال les ions iodure؟ استعمل la concentration و le volume. " + FIN_Q,
             fr="Voici l'équation, en haut du tableau d'avancement. Question suivante : remplis la première ligne, l'état initial, en "
                "millimoles. Utilise la concentration et le volume.",
             rappel="هادي هي l'équation", question_mot="السؤال الجاي", reperes=[("فوق le tableau", "tableau")],
             cahier="État initial (x = 0) : n₀(H₂O₂) = 2 mmol ; n₀(I⁻) = [I⁻]₀·V = 0,1 × 0,100 = 10 mmol ; n(I₂) = 0.",
             q=ouverte("Remplis la ligne de l'état initial du tableau d'avancement, en mmol.",
                       "x = 0 ; n₀(H₂O₂) = 2 mmol ; n₀(I⁻) = [I⁻]₀·V = 0,1 × 0,100 = 10⁻² mol = 10 mmol ; n₀(I₂) = 0",
                       "شوف هاد السؤال: عمر السطر ديال l'état initial.",
                       "l'état initial: x égale zéro. l'eau oxygénée: deux millimoles، عطاها le sujet. les ions iodure: n zéro égale la "
                       "concentration fois le volume، zéro virgule un fois zéro virgule un، égale dix millimoles. le diiode: zéro "
                       "فالبداية.",
                       [("État initial : x = 0", "l'état initial"),
                        ("n₀(H₂O₂) = 2 mmol", "l'eau oxygénée"),
                        ("n₀(I⁻) = [I⁻]₀·V = 0,1 × 0,100 = 10⁻² mol = 10 mmol", "les ions iodure"),
                        ("n₀(I₂) = 0", "le diiode")])),
        dict(id="encours", titre="Étape 4 : le tableau, en cours", comp="C6",
             lead="La deuxième ligne : avec l'avancement x.",
             mixed="شوف السطر الأول: deux، dix، و zéro. السؤال الجاي: عمر السطر التاني، en cours، ب l'avancement x. "
                   "شوف les coefficients ديال l'équation. " + FIN_Q,
             fr="Regarde la première ligne : deux, dix et zéro. Question suivante : remplis la deuxième ligne, en cours, avec "
                "l'avancement x. Regarde les coefficients de l'équation.",
             rappel="شوف السطر الأول", question_mot="السؤال الجاي",
             cahier="En cours : n(H₂O₂) = 2 − x ; n(I⁻) = 10 − 2x (coefficient 2) ; n(I₂) = x.",
             q=ouverte("Remplis la ligne « en cours » avec l'avancement x.", "n(H₂O₂) = 2 − x ; n(I⁻) = 10 − 2x ; n(I₂) = x",
                       "شوف هاد السؤال: عمر السطر ديال en cours.",
                       "l'eau oxygénée: le coefficient un، إذن deux moins x. les ions iodure: le coefficient deux، إذن dix moins deux x. "
                       "le diiode: كيتكون، إذن x.",
                       [("n(H₂O₂) = 2 − x", "l'eau oxygénée"),
                        ("n(I⁻) = 10 − 2x (coefficient 2)", "les ions iodure"),
                        ("n(I₂) = x", "le diiode")])),
        dict(id="limitant", titre="Étape 5 : x_max et le réactif limitant", comp="C6",
             lead="La troisième ligne : l'état final.",
             mixed="شوف السطر التاني: deux moins x، dix moins deux x، و x. السؤال الجاي: لقا x max و le réactif limitant. "
                   "كل réactif: إمتى كيسالي؟ ومن بعد خود القيمة الصغيرة. " + FIN_Q,
             fr="Regarde la deuxième ligne. Question suivante : trouve x max et le réactif limitant. Pour chaque réactif, quand "
                "est-il épuisé ? Puis garde la plus petite valeur.",
             rappel="شوف السطر التاني", question_mot="السؤال الجاي",
             cahier="État final : 2 − x_max = 0 donne 2 mmol ; 10 − 2x_max = 0 donne 5 mmol ; x_max = 2 mmol ; H₂O₂ est le réactif limitant.",
             q=ouverte("Trouve x_max et le réactif limitant.", "2 − x_max = 0 donne 2 mmol ; 10 − 2x_max = 0 donne 5 mmol ; x_max = 2 mmol ; H₂O₂ limitant",
                       "شوف هاد السؤال: لقا x max و le réactif limitant.",
                       "l'eau oxygénée كتسالي ملي deux moins x max égale zéro: deux millimoles. les ions iodure: dix moins deux x max "
                       "égale zéro: cinq millimoles. كناخدو القيمة الصغيرة: x max égale deux millimoles. إذن l'eau oxygénée هي le réactif "
                       "limitant، و les ions iodure en excès.",
                       [("2 − x_max = 0 donne x_max = 2 mmol", "l'eau oxygénée كتسالي"),
                        ("10 − 2x_max = 0 donne x_max = 5 mmol", "les ions iodure:"),
                        ("On garde la plus petite : x_max = 2 mmol", "كناخدو القيمة"),
                        ("H₂O₂ est le réactif limitant ; I⁻ est en excès", "إذن l'eau oxygénée")])),
        dict(id="suivi", titre="Étape 6 : suivre la transformation par n(I₂)", comp="C6",
             lead="La quantité de diiode, mesurée au cours du temps.",
             mixed="شوف la courbe: n de I deux مع الوقت، ف جوج ديال les expériences. و فle tableau، السطر الأخير: x max égale deux "
                   "millimoles. السؤال الجاي: شحال كتوصل la courbe فالأخير؟ وعلاش؟ " + FIN_Q,
             fr="Regarde la courbe : n de I deux en fonction du temps, dans les deux expériences. Dans le tableau, la dernière ligne : "
                "x max égale deux millimoles. Question suivante : quelle valeur atteint la courbe à la fin, et pourquoi ?",
             courbe="شوف la courbe", rappel="و فle tableau", question_mot="السؤال الجاي",
             cahier="Suivi : n(I₂) = x ; à la fin, n(I₂) = x_max = 2 mmol.",
             q=ouverte("On suit n(I₂). Quelle valeur atteint la courbe à la fin ? Pourquoi ?", "n(I₂) = x ; à la fin n(I₂) = x_max = 2 mmol",
                       "شوف هاد السؤال: شحال كتوصل la courbe فالأخير؟",
                       "le tableau كيقول: n de I deux égale x. إذن la courbe كتعطي l'avancement. فالأخير، x égale x max: n de I deux "
                       "égale deux millimoles.",
                       [("D'après le tableau : n(I₂) = x", "le tableau كيقول"),
                        ("À la fin : n(I₂) = x_max = 2 mmol", "فالأخير")])),
        dict(id="temperature", titre="Étape 7 : quelle courbe à 40 °C ?", comp="C5",
             lead="Seule la température change entre les deux expériences.",
             mixed="جوج ديال les courbes كيوصلو ل deux millimoles. السؤال الجاي: غير la température اللي تبدلات. شمن courbe هي "
                   "quarante degrés؟ شوف شكون كتوصل اللولى. " + FIN_Q,
             fr="Les deux courbes arrivent à deux millimoles. Question suivante : seule la température change. Quelle courbe est à "
                "quarante degrés ? Regarde laquelle arrive la première.",
             rappel="جوج ديال les courbes", question_mot="السؤال الجاي",
             cahier="(a) atteint sa valeur finale plus tôt : à 40 °C ; la température est un facteur cinétique.",
             q=qcm("Seule la température change. Quelle courbe correspond à 40 °C ?", ["(a)", "(b)", "On ne peut pas savoir"], 0,
                   "شوف هاد السؤال: شمن courbe هي quarante degrés؟",
                   "a كتوصل للقيمة النهائية ديالها قبل b. يعني la transformation كتمشي بالزربة. ملي la température كتطلع، "
                   "la transformation كتولي plus rapide. إذن a هي quarante degrés، و la température facteur cinétique.",
                   [("(a) atteint sa valeur finale plus tôt que (b)", "a كتوصل"),
                    ("Plus chaud, transformation plus rapide", "ملي la température"),
                    ("(a) : 40 °C ; la température est un facteur cinétique", "إذن a هي")],
                   rep_courbe)),
        dict(id="final", titre="Étape 8 : le même état final", comp="C5",
             lead="La température change la durée… et l'état final ?",
             mixed="a هي quarante degrés: كتوصل قبل. السؤال الجاي: علاش جوج ديال les courbes عندهم نفس القيمة النهائية؟ " + FIN_Q,
             fr="C'est la courbe a, à quarante degrés : elle arrive avant. Question suivante : pourquoi les deux courbes ont-elles la "
                "même valeur finale ?",
             rappel="a هي quarante degrés", question_mot="السؤال الجاي",
             cahier="La température change la durée, pas l'état final : même réactif limitant H₂O₂, même x_max = 2 mmol.",
             q=ouverte("Pourquoi les deux courbes ont-elles la même valeur finale ?",
                       "la température change la durée, pas l'état final ; même réactif limitant H₂O₂, même x_max = 2 mmol",
                       "شوف هاد السؤال: علاش نفس القيمة النهائية؟",
                       "la température كتبدل la durée، ماشي l'état final. ف جوج ديال les expériences، نفس les quantités: نفس le réactif "
                       "limitant، l'eau oxygénée. إذن نفس x max: deux millimoles.",
                       [("La température change la durée, pas l'état final", "la température كتبدل"),
                        ("Mêmes quantités : même réactif limitant H₂O₂", "ف جوج ديال"),
                        ("Même x_max = 2 mmol", "إذن نفس x max")])),
        dict(id="trempe", titre="Étape 9 : arrêter la transformation", comp="C7",
             lead="Pour doser le diiode à un instant donné.",
             mixed="نفس le réactif limitant، إذن نفس x max. السؤال الجاي: باش نعرفو la quantité ديال le diiode ف واحد اللحظة، خاصنا "
                   "نحبسو la transformation. كيفاش؟ " + FIN_Q,
             fr="Même réactif limitant, donc même x max. Question suivante : pour connaître la quantité de diiode à un instant, il faut "
                "arrêter la transformation. Comment ?",
             rappel="نفس le réactif limitant،", question_mot="السؤال الجاي",
             cahier="La trempe : on verse le prélèvement dans de l'eau glacée ; froid et dilution, la transformation devient très lente.",
             q=ouverte("Pour doser I₂ à un instant t, comment arrête-t-on la transformation ?",
                       "la trempe : on verse le prélèvement dans de l'eau glacée ; le froid et la dilution rendent la transformation très lente",
                       "شوف هاد السؤال: كيفاش نحبسو la transformation؟",
                       "كنديرو la trempe: كنحطو شوية من le mélange ف l'eau glacée. la température كتهبط، و la concentration "
                       "كتنقص. جوج ديال les facteurs cinétiques كينقصو، إذن la transformation كتولي lente بزاف.",
                       [("La trempe : prélèvement versé dans de l'eau glacée", "كنديرو la trempe"),
                        ("La température baisse et la concentration diminue (dilution)", "la température كتهبط"),
                        ("Deux facteurs cinétiques diminuent : la transformation devient très lente", "جوج ديال les facteurs")])),
    ]
    fin = ("La copie complète",
           "la trempe: l'eau glacée. هادي هي la copie كاملة ديال هاد التمرين، بحال اللي كتلقى فالتصحيح. les demi-équations، "
           "l'équation، le tableau، x max، la courbe، la température، و la trempe: هادو هوما الأسئلة اللي كتجي ف le national.",
           "La trempe : de l'eau glacée. Voici la copie complète de l'exercice, comme la lit le correcteur : les questions qui tombent au national.",
           "Les questions qui tombent au national, réunies dans une copie.",
           "H₂O₂ + 2I⁻ + 2H⁺ → I₂ + 2H₂O ; tableau d'avancement : x_max = 2 mmol, H₂O₂ limitant ; n(I₂) = x ; (a) à 40 °C ; même état final ; trempe.",
           "C7")
    nouvelles = construire(deck, "tl", url, sujet, E, fin)
    m = charger(ATT / f"{deck}.json")
    ids = [s["id"] for s in nouvelles]
    inserer(m, nouvelles, "tl_partie8b", "IX. Un exercice type national, joué pas à pas", "tl_partie9", 50, [
        ("tl_s4", "Séance 4 — La trempe, le catalyseur, puis un national joué pas à pas", [
            ("tl_s3_b2", "La trempe, la vie quotidienne et le catalyseur", ["tl_t1_trempe", "tl_t2_vie", "tl_t3_catalyseur", "tl_t4_courbes"]),
            ("tl_np_b1", "Le sujet, les demi-équations, l’équation", ids[0:3]),
            ("tl_np_b2", "Le tableau d’avancement, ligne par ligne", ids[3:6])]),
        ("tl_s5", "Séance 5 — Les courbes, la trempe, deux nationaux et le bilan", [
            ("tl_np_b3", "Suivre n(I₂), la température, le même état final", ids[6:9]),
            ("tl_np_b4", "La trempe, la copie complète", ids[9:11]),
            ("tl_s3_b3", "Deux nationaux et le bilan", ["tl_n1_lecture", "tl_n2_glacee", "tl_bl_fiche", "tl_cr_carte"])]),
    ])
    for a in m["activities"]:
        if a["id"] == "tl_partie9" and a["title"].startswith("IX."):
            a["title"] = "X." + a["title"][3:]
        if a["id"] == "tl_bilan" and a["title"].startswith("X."):
            a["title"] = "XI." + a["title"][2:]
    enregistrer(m, deck)
    return ids


if __name__ == "__main__":
    for f in (rc, rl, rlc, ch9):
        f()


# ════════════════ Mots rares des pistes de la 1ʳᵉ passe (pas encore en voix : les réécrire ne coûte rien) ════════════════
def remplacer_dans(s, paires):
    """Remplace dans la voix (fr et mixed) et dans les mots du pointage / de l'observation, qui doivent rester des extraits."""
    st = s["speech_text"]
    for a, b in paires:
        for k in ("fr", "mixed"):
            st[k] = st[k].replace(a, b)
        c = s.get("concentration") or {}
        for p in c.get("pointage") or []:
            p["mot"] = p["mot"].replace(a, b)
        o = c.get("observation")
        if o:
            o["apres_mot"] = o["apres_mot"].replace(a, b)
    s.pop("audio", None)
    verifier_mots(s)


def mots():
    m = charger(ATT / "phys_ch6_dipole_RC.json"); D = diapos(m)
    remplacer_dans(D["rc_m5_observer"], [("deux kiloohms", "deux mille ohm"), ("un kiloohm", "mille ohm"),
                                         ("microfarads", "micro farad"), ("kiloohms", "mille ohm"), ("kiloohm", "mille ohm")])
    enregistrer(m, "phys_ch6_dipole_RC")

    m = charger(ATT / "phys_ch7_dipole_RL.json"); D = diapos(m)
    remplacer_dans(D["rl_m5_observer"], [("ohms", "ohm"), ("milliampères", "milliampère"), ("le palier هبط", "la valeur finale هبطات"),
                                         ("le palier", "la valeur finale")])
    enregistrer(m, "phys_ch7_dipole_RL")

    m = charger(ATT / "phys_ch8_circuit_RLC.json"); D = diapos(m)
    remplacer_dans(D["lc_r5_observer"], [("microfarads", "micro farad"), ("و les sommets كينقصو شوية", "و l'amplitude كتنقص شوية"),
                                         ("les sommets", "l'amplitude")])
    enregistrer(m, "phys_ch8_circuit_RLC")

    m = charger(ATT / "phys_ch9_transformations_lentes_rapides.json"); D = diapos(m)
    r6 = D["tl_r6_classer"]["concentration"]["reponses"]["e0"]
    r6["0"]["1"]["parole"] = ("شوف، la rouille هي transformation معروفة. ولكن شحال كتاخد ديال الوقت؟ des années: ما كتبانش كتبدل فلحظة. "
                              "السؤال كيقول rapide، يعني كتسالي فلحظة. قارن la durée ديال كل واحد، و جرب مرة أخرى.")
    r6["0"]["2"]["parole"] = ("لا، هادي ماشي هي. الجواب هو B: le solide blanc ديال le chlorure d'argent كيبان فلحظة، إذن transformation "
                              "rapide. أما la rouille، كتاخد des années: lente بزاف. ديما كنشوفو la durée، ماشي la quantité ديال le produit.")
    r6["1"]["juste"]["parole"] = ("مزيان، الجواب B صحيح. le solide blanc ديال le chlorure d'argent كيبان دغيا: transformation rapide. "
                                  "ديما كنشوفو la durée، ماشي la quantité ديال le produit. la rouille كتاخد des années، و le diiode "
                                  "كياخد plusieurs minutes: هوما lentes.")
    r6["2"]["1"]["parole"] = ("شوف، فهاد la transformation اللون كيتبدل فعلا. ولكن شحال ديال الوقت كيدوز حتى كيولي brun بزاف؟ "
                              "فكر ف la durée، و قارن بين les trois choix. جرب مرة أخرى.")
    r6["2"]["2"]["parole"] = ("لا، هادي ماشي هي. le diiode كيتكون ف des minutes: اللون brun كيجي بشوية، إذن transformation lente. "
                              "الجواب الصحيح هو B: le solide blanc ديال le chlorure d'argent كيبان فلحظة، transformation rapide.")
    f8 = D["tl_f8_variable"]["concentration"]["reponses"]["e0"]
    f8["1"]["1"]["parole"] = ("شوف، مزيان بلي بغيتي تقارن جوج expériences. ولكن بين un و trois، شنو اللي تبدل؟ غير la concentration، "
                              "ولا حتى la température؟ خاص paramètre واحد اللي يتبدل، و les autres يبقاو هوما هوما. جرب تاني.")
    f8["1"]["2"]["parole"] = ("لا، هادي ماشي هي. الجواب الصحيح هو deux و trois: la température هي هي، quarante degrés Celsius، و غير "
                              "la concentration اللي تبدلات. بين un و trois، جوج paramètres تبدلو: ما نقدرش نعرف شكون فيهم دار الفرق. "
                              "ما تخافش، دابا فهمتي la règle: un seul paramètre كيتبدل.")
    f8["2"]["1"]["parole"] = ("شوف، الفكرة مزيانة: جوج expériences، و paramètre واحد كيتبدل. ولكن بين un و deux، شنو اللي تبدل؟ "
                              "والسؤال على شنو؟ على la concentration ديال les ions iodure. شوف la concentration ف هاد جوج: واش تبدلات؟ عاود جرب.")
    f8["2"]["2"]["parole"] = ("لا، هادي ماشي هي. الجواب الصحيح هو deux و trois: غير la concentration اللي تبدلات، و la température بقات "
                              "quarante degrés. بين un و deux، غير la température اللي تبدلات: هادو باش ندرسو la température، ماشي la concentration.")
    for x in (r6["0"]["1"], r6["0"]["2"], r6["1"]["juste"], r6["2"]["1"], r6["2"]["2"], f8["1"]["1"], f8["1"]["2"], f8["2"]["1"], f8["2"]["2"]):
        x.pop("audio", None)
    ex = D["tl_f8_variable"]["exercises"][0]
    ex["enonce_dit"] = ex["enonce_dit"].replace("on compare quelles expériences ?", "شمن جوج expériences كنقارنو؟")
    ex.pop("enonce_audio", None)
    # Le chiffre de la carte d'ouverture, vérifié sur les 20 sujets (2016-2025) : des questions sur les facteurs cinétiques,
    # le catalyseur ou la trempe dans 8 sessions (2016 R, 2017 N, 2017 R, 2018 N, 2018 R, 2023 N, 2024 N, 2025 N), pas 10.
    s = D["tl_o1_carte"]
    s["screen_content"]["bullets"] = [b.replace("questions de facteurs cinétiques dans 10 sessions sur 20",
                                                "facteurs cinétiques, catalyseur ou trempe dans 8 sessions sur 20")
                                      for b in s["screen_content"]["bullets"]]
    remplacer_dans(s, [("et les facteurs cinétiques dans dix sessions", "et les facteurs cinétiques, le catalyseur ou la trempe dans huit sessions"),
                       ("و les facteurs cinétiques ف dix sessions", "و les facteurs cinétiques، le catalyseur ولا la trempe ف huit sessions")])
    assert "dix sessions" not in s["speech_text"]["mixed"] + s["speech_text"]["fr"]
    for k in ("tl_o1_carte", "tl_cr_carte"):   # le tableau de la carte écrit le même chiffre que la voix
        v = D[k]["visual"]
        v["url"] = v["url"].split("?")[0] + "?sessions=8"
    enregistrer(m, "phys_ch9_transformations_lentes_rapides")


if __name__ == "__main__":
    mots()
