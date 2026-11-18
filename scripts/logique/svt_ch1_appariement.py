"""SVT ch1, exercice joué pas à pas (18 novembre 2026) : le national 2020 R, restitution III — « Reliez chaque
phénomène à la réaction bilan qui lui convient » (cas type `equation` de l'exploration), sur
national.html?vue=reactions.

Trois diapositives, une consigne chacune, après le_x1c_qcm : le tuteur montre la méthode sur a (regarder ce que donne
la réaction), l'élève fait b, puis c, puis départage d et e (cycle de Krebs, d est l'intrus). La correction de chaque
consigne reste cachée (?cacher=) jusqu'à la réponse ; `apres_reponse` la joue au tableau, puis la démonstration au
barème. Un bloc de séance à part (le_s6_b1b), pour ne pas dépasser quatre diapositives par bloc.
Idempotent. Chaque `mot` est contrôlé dans son texte.
"""
import json
import re
from pathlib import Path

R = Path(__file__).resolve().parents[2]
DECK = "svt_ch1_reactions_responsables_liberation_energie"
F = R / f"backend/data/courses/en_attente/{DECK}.json"
NAT = "/media/simulations/svt/reactions_responsables_liberation_energie-tableau/national.html?vue=reactions"
APRES = "le_x1c_qcm"
IDS = ["le_x1d_reactions", "le_x1e_reactions_c", "le_x1f_reactions_krebs"]

REACS = ["a- C₆H₁₂O₆ + 2 ADP + 2 Pi → 2 CH₃CH₂OH + 2 CO₂ + 2 ATP",
         "b- C₆H₁₂O₆ + 2 ADP + 2 Pi → 2 CH₃CHOHCOOH + 2 ATP",
         "c- C₆H₁₂O₆ + 2 ADP + 2 Pi + 2 NAD⁺ → 2 CH₃COCOOH + 2 ATP + 2 NADH,H⁺",
         "d- CH₃COCOOH + 2 ATP → CH₃COOH + 2 ADP + 2 Pi",
         "e- CH₃CO-SCoA + 3 NAD⁺ + 3 H₂O + FAD + GDP + Pi → 2 CO₂ + HSCoA + 3 NADH,H⁺ + FADH₂ + GTP"]


def reac(parole, ecrit):
    return {"parole": parole, "ecrit": ecrit}


def reponses(bonne, faux):
    q = {str(bonne[0]): {"juste": reac(*bonne[1])}}
    for o, (r1, r2) in faux.items():
        q[str(o)] = {"1": reac(*r1), "2": reac(*r2)}
    return {"q": dict(sorted(q.items()))}


def rejeu(moment):
    """Après la réponse : la correction s'écrit au tableau (elle était cachée), puis la démonstration."""
    return {"question": "q", "sim_avant": {"conclusions": False}, "duree_s": 6,
            "etapes": [{"commande": "set_parameters", "parametres": {"conclusions": True}},
                       {"commande": "play_until", "parametres": {"moment": moment}}]}


SLIDES = [
    {
        "id": "le_x1d_reactions", "slide_type": "evaluation", "title": "Relier phénomène et réaction (1/3) : la méthode",
        "screen_content": {
            "lead": "2020 R : « Reliez chaque phénomène à la réaction bilan qui lui convient » (1 pt). Quatre phénomènes, "
                    "cinq réactions : une est de trop.",
            "bullets": ["1- La glycolyse ; 2- Le cycle de Krebs ; 3- La fermentation lactique ; 4- La fermentation alcoolique"] + REACS
                       + ["La méthode : regarder ce que donne chaque réaction (à droite de la flèche)."],
            "student_trace": "Relier une réaction à son phénomène : regarder ce qu'elle donne. Éthanol + CO₂ → fermentation "
                             "alcoolique : (4 ; a).",
        },
        "visual": {"kind": "simulation", "url": NAT + "&cacher=b_lien",
                   "caption": "Examen 2020 R : relier chaque phénomène à sa réaction bilan",
                   "alt": "Les quatre phénomènes à gauche, les cinq réactions à droite ; ce que donne a est souligné et relié à la fermentation alcoolique, puis ce que donne b est souligné"},
        "speech_text": {
            "fr": "Une autre question de restitution, 2020 R : relier chaque phénomène à sa réaction bilan, un point. "
                  "Quatre phénomènes : la glycolyse, le cycle de Krebs, la fermentation lactique et la fermentation alcoolique. "
                  "Cinq réactions, de a à e : une est de trop. La méthode : on ne lit pas toute la réaction, on regarde ce "
                  "qu'elle donne, après la flèche. On commence par a : elle donne de l'éthanol et du CO₂. L'éthanol et le CO₂, "
                  "c'est la fermentation alcoolique. On écrit donc (4 ; a). À toi : regarde ce que donne la réaction b. "
                  "À quel phénomène correspond-elle ?",
            "mixed": "دابا سؤال آخر ديال الدرس، من deux mille vingt: نربطو كل phénomène ب la réaction bilan ديالو، وعليه "
                     "un point. عندنا ربعة ديال les phénomènes: la glycolyse، le cycle de Krebs، la fermentation lactique، "
                     "و la fermentation alcoolique. وعندنا خمسة ديال les réactions، من a حتى ل e. يعني كاينة وحدة "
                     "زايدة. الطريقة: ما غاديش نقراو la réaction كاملة. نشوفو غير شنو كتعطي، من بعد la flèche. نبداو ب a. "
                     "شوف شنو كتعطي: l'éthanol، و CO deux. l'éthanol و CO deux، هادي la fermentation alcoolique. إذن "
                     "نكتبو: quatre، a. دابا نتا: شوف la réaction b، شنو كتعطي؟ ومن بعد، أشمن phénomène؟",
        },
        "concentration": {
            "demarrer": "reset",
            "pointage": [
                {"mot": "دابا سؤال آخر", "commande": "play_until", "parametres": {"moment": "enonce"}},
                {"mot": "عندنا ربعة ديال les phénomènes", "commande": "play_until", "parametres": {"moment": "phenomenes"}},
                {"mot": "وعندنا خمسة ديال les réactions", "commande": "play_until", "parametres": {"moment": "reactions"}},
                {"mot": "نبداو ب a.", "commande": "play_until", "parametres": {"moment": "a_produit"}},
                {"mot": "شوف شنو كتعطي: l'éthanol", "repere": "produit_a"},
                {"mot": "إذن نكتبو: quatre", "commande": "play_until", "parametres": {"moment": "a_lien"}},
                {"mot": "دابا نتا: شوف la réaction b", "commande": "play_until", "parametres": {"moment": "b_produit"}},
            ],
            "cahier": "Relier une réaction à son phénomène : regarder ce qu'elle donne (après la flèche). Éthanol + CO₂ → "
                      "fermentation alcoolique : (4 ; a).",
            "apres_reponse": rejeu("b_lien"),
            "reponses": reponses(
                (1, ("مزيان! b كتعطي l'acide lactique. و l'acide lactique كتعطيه la fermentation lactique. إذن: trois، b.",
                     "Oui : b donne l'acide lactique (CH₃CHOHCOOH), produit de la fermentation lactique. Couple (3 ; b).")),
                {0: (("la glycolyse كتعطي l'acide pyruvique. واش b كتعطي l'acide pyruvique؟ عاود شوف شنو كتعطي.",
                      "La glycolyse donne l'acide pyruvique. Est-ce ce que donne b ? Regarde après la flèche, puis réessaie."),
                     ("الجواب هو la fermentation lactique. b كتعطي l'acide lactique، ماشي l'acide pyruvique. إذن: trois، b.",
                      "La bonne réponse : la fermentation lactique. b donne l'acide lactique (CH₃CHOHCOOH), pas l'acide "
                      "pyruvique. Couple (3 ; b).")),
                 2: (("la fermentation alcoolique كتعطي CO deux. واش كاين CO deux من بعد la flèche ديال b؟ عاود شوف.",
                      "La fermentation alcoolique donne du CO₂. Y a-t-il du CO₂ après la flèche de b ? Réessaie."),
                     ("الجواب هو la fermentation lactique. b ما فيهاش CO deux، كتعطي l'acide lactique. la fermentation "
                      "alcoolique هي a. إذن: trois، b.",
                      "La bonne réponse : la fermentation lactique. b ne donne pas de CO₂ mais l'acide lactique ; la "
                      "fermentation alcoolique, c'est a. Couple (3 ; b)."))}),
        },
        "question": {
            "type": "qcm", "prompt": "La réaction b (→ 2 CH₃CHOHCOOH + 2 ATP) correspond à quel phénomène ?",
            "options": ["1- La glycolyse", "3- La fermentation lactique", "4- La fermentation alcoolique"],
            "correct": 1, "timeout_seconds": 45,
            "enonce_dit": "سؤال: la réaction b، لأشمن phénomène كتمشي؟",
            "demonstration": {
                "parole": "شوف شنو كتعطي b: l'acide lactique. و l'acide lactique كتعطيه la "
                          "fermentation lactique. إذن فالورقة: trois، b.",
                "lignes": [
                    {"texte": "b donne : 2 CH₃CHOHCOOH + 2 ATP", "mot": "شوف شنو كتعطي b"},
                    {"texte": "CH₃CHOHCOOH = acide lactique", "mot": "b: l'acide lactique. و"},
                    {"texte": "l'acide lactique est produit par la fermentation lactique", "mot": "و l'acide lactique كتعطيه"},
                    {"texte": "Couple : (3 ; b)", "mot": "إذن فالورقة"},
                ],
            },
        },
        "competence_ids": ["C7"],
    },
    {
        "id": "le_x1e_reactions_c", "slide_type": "evaluation", "title": "Relier phénomène et réaction (2/3) : la réaction c",
        "screen_content": {
            "lead": "(4 ; a) et (3 ; b) sont écrits. La même méthode pour c : ce qu'elle donne, et d'où elle part.",
            "bullets": [REACS[2], "Elle part de quoi ? Elle donne quoi ?"],
            "student_trace": "Glucose → 2 acides pyruviques + 2 ATP + 2 NADH,H⁺ : la glycolyse (1 ; c).",
        },
        "visual": {"kind": "simulation", "url": NAT + "&depart=b_lien&cacher=c_lien",
                   "caption": "Examen 2020 R : la réaction c",
                   "alt": "(4 ; a) et (3 ; b) sont reliés ; ce que donne c est souligné, sans le lien"},
        "speech_text": {
            "fr": "b donne l'acide lactique : c'est la fermentation lactique, (3 ; b). Maintenant la réaction c. Même méthode : "
                  "regarde ce qu'elle donne, après la flèche, et regarde aussi d'où elle part. À toi : à quel phénomène "
                  "correspond la réaction c ?",
            "mixed": "شوف: b كتعطي l'acide lactique، إذن la fermentation lactique: trois، b. دابا la réaction c. نفس "
                     "الطريقة: شوف شنو كتعطي، من بعد la flèche. وشوف حتى من فين كتبدا. دابا نتا: la réaction c، "
                     "لأشمن phénomène كتمشي؟",
        },
        "concentration": {
            "demarrer": "reset",
            "pointage": [
                {"mot": "شوف: b كتعطي", "repere": "lien_b"},
                {"mot": "دابا la réaction c.", "commande": "play_until", "parametres": {"moment": "c_produit"}},
                {"mot": "شوف شنو كتعطي، من بعد", "repere": "produit_c"},
                {"mot": "وشوف حتى من فين كتبدا", "repere": "reac_c"},
            ],
            "cahier": "Glucose → 2 acides pyruviques + 2 ATP + 2 NADH,H⁺ : la glycolyse, (1 ; c).",
            "apres_reponse": rejeu("c_lien"),
            "reponses": reponses(
                (0, ("مزيان! c كتبدا من le glucose، وكتعطي جوج ديال l'acide pyruvique، و ATP، و NADH,H plus. هادي la "
                     "glycolyse. إذن: un، c.",
                     "Oui : c part du glucose et donne 2 acides pyruviques (CH₃COCOOH), 2 ATP et 2 NADH,H⁺ : la glycolyse. "
                     "Couple (1 ; c).")),
                {1: (("le cycle de Krebs كيبدا من le glucose؟ شوف من فين كتبدا c.",
                      "Le cycle de Krebs part-il du glucose ? Regarde d'où part c, puis réessaie."),
                     ("الجواب هو la glycolyse. c كتبدا من le glucose، وكتعطي l'acide pyruvique. le cycle de Krebs كيبدا "
                      "من l'acétyl-CoA، فla matrice. إذن: un، c.",
                      "La bonne réponse : la glycolyse. c part du glucose et donne l'acide pyruvique ; le cycle de Krebs "
                      "part de l'acétyl-CoA, dans la matrice. Couple (1 ; c).")),
                 2: (("la fermentation lactique كتعطي l'acide lactique. واش c كتعطي l'acide lactique؟ عاود شوف.",
                      "La fermentation lactique donne l'acide lactique. Est-ce ce que donne c ? Réessaie."),
                     ("الجواب هو la glycolyse. c كتعطي l'acide pyruvique، ماشي l'acide lactique. و la fermentation "
                      "lactique راه خديناها: b. إذن: un، c.",
                      "La bonne réponse : la glycolyse. c donne l'acide pyruvique, pas l'acide lactique ; la fermentation "
                      "lactique, c'est déjà b. Couple (1 ; c)."))}),
        },
        "question": {
            "type": "qcm", "prompt": "La réaction c correspond à quel phénomène ?",
            "options": ["1- La glycolyse", "2- Le cycle de Krebs", "3- La fermentation lactique"],
            "correct": 0, "timeout_seconds": 45,
            "enonce_dit": "سؤال: la réaction c، لأشمن phénomène كتمشي؟",
            "demonstration": {
                "parole": "c كتبدا من le glucose. وكتعطي جوج ديال l'acide pyruvique، و deux ATP، و deux NADH,H plus. "
                          "le glucose كيولي جوج ديال l'acide pyruvique: هادي la glycolyse. إذن فالورقة: un، c.",
                "lignes": [
                    {"texte": "c part du glucose (C₆H₁₂O₆)", "mot": "c كتبدا من le glucose"},
                    {"texte": "c donne : 2 CH₃COCOOH (acide pyruvique) + 2 ATP + 2 NADH,H⁺", "mot": "وكتعطي جوج ديال"},
                    {"texte": "glucose → 2 acides pyruviques : la glycolyse", "mot": "le glucose كيولي"},
                    {"texte": "Couple : (1 ; c)", "mot": "إذن فالورقة"},
                ],
            },
        },
        "competence_ids": ["C3"],
    },
    {
        "id": "le_x1f_reactions_krebs", "slide_type": "evaluation", "title": "Relier phénomène et réaction (3/3) : d ou e ?",
        "screen_content": {
            "lead": "(1 ; c) est écrit. Reste le cycle de Krebs, et deux réactions : d et e. Une est l'intrus.",
            "bullets": [REACS[3], REACS[4], "Qu'est-ce qui entre dans le cycle de Krebs ? Qu'est-ce qui en sort ?"],
            "student_trace": "Cycle de Krebs : acétyl-CoA → 2 CO₂ + 3 NADH,H⁺ + FADH₂ + GTP : (2 ; e) ; d est l'intrus. "
                             "Réponse : (1 ; c) ; (2 ; e) ; (3 ; b) ; (4 ; a).",
        },
        "visual": {"kind": "simulation", "url": NAT + "&depart=c_lien&cacher=e_lien",
                   "caption": "Examen 2020 R : d ou e, le cycle de Krebs",
                   "alt": "Trois couples reliés ; ce que donnent d et e est souligné, sans le lien"},
        "speech_text": {
            "fr": "c part du glucose et donne l'acide pyruvique : c'est la glycolyse, (1 ; c). Il reste le cycle de Krebs, et "
                  "deux réactions : d et e. Une est de trop. Rappelle-toi ce qui entre dans le cycle de Krebs, dans la "
                  "matrice, et ce qui en sort. Puis regarde d'où part chaque réaction et ce qu'elle donne. À toi : quelle "
                  "réaction est celle du cycle de Krebs ?",
            "mixed": "شوف: c كتبدا من le glucose، وكتعطي l'acide pyruvique: هادي la glycolyse، un، c. بقا لينا le "
                     "cycle de Krebs، وبقاو جوج ديال les réactions: d و e. وحدة منهم زايدة. تفكر: شنو كيدخل ل "
                     "le cycle de Krebs، فla matrice، وشنو كيخرج منو؟ ومن بعد شوف من فين كتبدا كل réaction، وشنو "
                     "كتعطي. دابا نتا: أشمن réaction هي ديال le cycle de Krebs؟",
        },
        "concentration": {
            "demarrer": "reset",
            "pointage": [
                {"mot": "شوف: c كتبدا", "repere": "lien_c"},
                {"mot": "بقا لينا le", "repere": "phen_2"},
                {"mot": "وبقاو جوج ديال les réactions", "commande": "play_until", "parametres": {"moment": "de_produit"}},
                {"mot": "ومن بعد شوف من فين", "repere": "reac_d"},
                {"mot": "وشنو كتعطي. دابا", "repere": "reac_e"},
            ],
            "cahier": "Cycle de Krebs : acétyl-CoA → 2 CO₂ + 3 NADH,H⁺ + FADH₂ + GTP : (2 ; e) ; d est l'intrus. Réponse : "
                      "(1 ; c) ; (2 ; e) ; (3 ; b) ; (4 ; a).",
            "apres_reponse": rejeu("couples"),
            "reponses": reponses(
                (1, ("مزيان! e كتبدا من l'acétyl-CoA، وكتعطي جوج CO deux، و trois NADH,H plus، و FADH deux. هادا le "
                     "cycle de Krebs. و d ما كتمشي لحتى phénomène.",
                     "Oui : e part de l'acétyl-CoA et donne 2 CO₂, 3 NADH,H⁺, FADH₂ et GTP : le cycle de Krebs, (2 ; e). "
                     "d n'est aucun des quatre phénomènes.")),
                {0: (("d كتبدا من l'acide pyruvique، وكتاكل ATP. واش le cycle de Krebs كيعطي CO deux و NADH,H plus؟ "
                      "شوف واش d فيها CO deux و NADH,H plus.",
                      "d part de l'acide pyruvique et consomme de l'ATP. Le cycle de Krebs donne du CO₂ et du NADH,H⁺ : d en "
                      "donne-t-elle ? Réessaie."),
                     ("الجواب هو e. le cycle de Krebs كيبدا من l'acétyl-CoA، وكيعطي CO deux و NADH,H plus و FADH "
                      "deux، بحال e. d ما فيهاش CO deux، وكتاكل ATP: ما كتمشي لحتى phénomène.",
                      "La bonne réponse : e. Le cycle de Krebs part de l'acétyl-CoA et donne CO₂, NADH,H⁺ et FADH₂, comme e. "
                      "d ne donne pas de CO₂ et consomme de l'ATP : c'est l'intrus.")),
                 2: (("غير وحدة اللي صحيحة: كل phénomène عندو réaction وحدة. شوف شكون فيهم كتعطي CO deux و NADH,H plus.",
                      "Une seule convient : chaque phénomène a une seule réaction. Laquelle donne du CO₂ et du NADH,H⁺ ? "
                      "Réessaie."),
                     ("الجواب هو e. e كتبدا من l'acétyl-CoA، وكتعطي CO deux و NADH,H plus و FADH deux: هادا le cycle "
                      "de Krebs. d ما كتمشي لحتى phénomène.",
                      "La bonne réponse : e. e part de l'acétyl-CoA et donne CO₂, NADH,H⁺ et FADH₂ : le cycle de Krebs. d "
                      "n'est aucun des quatre phénomènes."))}),
        },
        "question": {
            "type": "qcm", "prompt": "Quelle réaction est la réaction bilan du cycle de Krebs ?",
            "options": [REACS[3], REACS[4], "d et e, les deux"],
            "correct": 1, "timeout_seconds": 50,
            "enonce_dit": "سؤال: أشمن réaction هي ديال le cycle de Krebs؟",
            "demonstration": {
                "parole": "e كتبدا من l'acétyl-CoA، اللي كيدخل ل le cycle de Krebs فla matrice. وكتعطي جوج CO deux، و "
                          "trois NADH,H plus، و FADH deux، و GTP. إذن: deux، e. و d؟ كتاكل ATP، وكتعطي l'acide "
                          "acétique: ما كتمشي لحتى phénomène. فالورقة كنكتبو: un، c. deux، e. trois، b. quatre، a.",
                "lignes": [
                    {"texte": "e part de l'acétyl-CoA (CH₃CO-SCoA), qui entre dans le cycle de Krebs (matrice)", "mot": "e كتبدا من l'acétyl-CoA"},
                    {"texte": "e donne : 2 CO₂ + 3 NADH,H⁺ + FADH₂ + GTP → cycle de Krebs : (2 ; e)", "mot": "وكتعطي جوج CO deux"},
                    {"texte": "d consomme de l'ATP et donne l'acide acétique : aucun des quatre phénomènes", "mot": "و d؟ كتاكل ATP"},
                    {"texte": "Réponse : (1 ; c) ; (2 ; e) ; (3 ; b) ; (4 ; a)", "mot": "فالورقة كنكتبو"},
                ],
            },
        },
        "competence_ids": ["C5"],
    },
]

BLOC = {
    "id": "le_s6_b1b", "titre": "Relier phénomènes et réactions bilans (2020 R)", "slide_ids": IDS,
    "cahier": [{"texte": "Relier une réaction à son phénomène : regarder ce qu'elle donne (après la flèche) et d'où elle part."},
               {"texte": "Éthanol + CO₂ → fermentation alcoolique ; acide lactique → fermentation lactique ; glucose → 2 acides "
                         "pyruviques + 2 NADH,H⁺ → glycolyse ; acétyl-CoA → 2 CO₂ + 3 NADH,H⁺ + FADH₂ → cycle de Krebs."},
               {"texte": "2020 R : (1 ; c) ; (2 ; e) ; (3 ; b) ; (4 ; a) — d est l'intrus."}],
    "retrouver": {"prompt": "Cahier fermé : quel produit signe chaque phénomène (glycolyse, Krebs, fermentation lactique, fermentation alcoolique) ?",
                  "attendu": "Glycolyse : acide pyruvique + NADH,H⁺ ; cycle de Krebs : CO₂ + NADH,H⁺ + FADH₂ ; fermentation lactique : "
                             "acide lactique ; fermentation alcoolique : éthanol + CO₂.",
                  "competence_id": "C7",
                  "enonce_dit": "شوف هاد السؤال: cahier fermé، شنو كيعطي كل phénomène: la glycolyse، le cycle de Krebs، la fermentation lactique، و la fermentation alcoolique؟"},
    "exercice": {"type": "qcm", "prompt": "Une réaction donne 2 CH₃CH₂OH + 2 CO₂ + 2 ATP. C'est :",
                 "options": ["la glycolyse", "la fermentation alcoolique", "la fermentation lactique"], "correct": 1,
                 "explanation": "Éthanol (CH₃CH₂OH) + CO₂ : la fermentation alcoolique.",
                 "enonce_dit": "شوف هاد السؤال: واحد la réaction كتعطي l'éthanol و CO deux و deux ATP. شنو هي؟"},
}


LETTRE = re.compile(r"(?<![A-Za-zÀ-ÿ'’,])([a-e])(?![A-Za-zÀ-ÿ'’⁺₀-₉])")


def maj(t):
    return LETTRE.sub(lambda m: m.group(1).upper(), t)


def majuscules(s):
    """La voix dit les lettres des réactions en majuscules (A, B…), comme le_x1c_qcm ; l'écrit garde a, b…"""
    s["speech_text"]["mixed"] = maj(s["speech_text"]["mixed"])
    for p in s["concentration"]["pointage"]:
        p["mot"] = maj(p["mot"])
    for q in s["concentration"]["reponses"].values():
        for o in q.values():
            for r in o.values():
                r["parole"] = maj(r["parole"])
    s["question"]["enonce_dit"] = maj(s["question"]["enonce_dit"])
    d = s["question"]["demonstration"]
    d["parole"] = maj(d["parole"])
    for l in d["lignes"]:
        l["mot"] = maj(l["mot"])


def controler(s):
    voix = s["speech_text"]["mixed"]
    for p in s["concentration"]["pointage"]:
        assert voix.count(p["mot"]) == 1, (s["id"], p["mot"])
    demo = s["question"]["demonstration"]
    for l in demo["lignes"]:
        assert demo["parole"].count(l["mot"]) == 1, (s["id"], l["mot"])


def main():
    m = json.load(open(F, encoding="utf-8"))
    act = next(a for a in m["activities"] if any(s["id"] == APRES for s in a["slides"]))
    neuf = all(i not in {s["id"] for s in act["slides"]} for i in IDS)
    garder = [s for s in act["slides"] if s["id"] not in IDS]
    k = next(i for i, s in enumerate(garder) if s["id"] == APRES) + 1
    for s in SLIDES:
        majuscules(s)
        controler(s)
    act["slides"] = garder[:k] + json.loads(json.dumps(SLIDES, ensure_ascii=False)) + garder[k:]
    s6 = next(se for se in m["seances"] if se["id"] == "le_s6")
    s6["blocs"] = [b for b in s6["blocs"] if b["id"] != BLOC["id"]]
    s6["blocs"].insert(next(i for i, b in enumerate(s6["blocs"]) if b["id"] == "le_s6_b1") + 1, BLOC)
    for c in m["competences"]:
        c["slide_ids"] = [i for i in c["slide_ids"] if i not in IDS]
        c["slide_ids"] += [s["id"] for s in SLIDES if c["id"] in s["competence_ids"]]
    if neuf:
        act["duration_minutes"] = act.get("duration_minutes", 35) + 10
        m["estimated_minutes"] = m.get("estimated_minutes", 275) + 10
    F.write_text(json.dumps(m, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("ok :", ", ".join(IDS), "après", APRES, "; bloc", BLOC["id"])


if __name__ == "__main__":
    main()
