"""2ᵉ passe du cours SVT ch1 (18 novembre 2026) : chaque cas type du national joué pas à pas en animation.

Relit la version en attente backend/data/courses/en_attente/svt_ch1_reactions_responsables_liberation_energie.json et :
  - remplace le_x1_restitution (texte) par trois étapes jouées (définir, sens des protons, QCM) sur national.html?vue=restitution ;
  - remplace le_x2_qui_respire (tableau) par deux étapes (comparer, expliquer) sur national.html?vue=sportifs (2016 N) ;
  - coupe le_x3_chaine_en_panne (tout dit d'un coup) en trois étapes (décrire, déduire, hypothèse et vérification) sur
    exao.html?vue=mitochondries&conclusions=false ;
  - donne une animation aux tableaux de le_e3b_masse_levures (texte et voix gardés) et de le_m3a_glucose_marque.
Une seule consigne par diapositive, la question posée après la voix, la correction (démonstration au barème) après la
réponse ; la diapositive suivante rejoue la correction au tableau avant la consigne suivante.
Idempotent : relancer le script ne change rien de plus. Chaque `mot` est contrôlé dans son texte.
"""
import json
from pathlib import Path

R = Path(__file__).resolve().parents[2]
DECK = "svt_ch1_reactions_responsables_liberation_energie"
F = R / f"backend/data/courses/en_attente/{DECK}.json"
SIM = "/media/simulations/svt/reactions_responsables_liberation_energie-tableau/"
NAT = SIM + "national.html"
EXAO = SIM + "exao.html?vue=mitochondries&conclusions=false"


def reac(parole, ecrit):
    return {"parole": parole, "ecrit": ecrit}


def reponses(bonne, faux):
    """faux : {option: (indice 1er essai, réponse 2e essai)} ; bonne : (option, réaction juste)."""
    q = {str(bonne[0]): {"juste": reac(*bonne[1])}}
    for o, (r1, r2) in faux.items():
        q[str(o)] = {"1": reac(*r1), "2": reac(*r2)}
    return {"q": dict(sorted(q.items()))}


SLIDES = {}

# ─────────────────────────── X. Restitution (2024 R, 2022 N) ───────────────────────────
SLIDES["le_x1_restitution"] = {
    "id": "le_x1_restitution", "slide_type": "evaluation", "title": "Restitution (1/3) : définir, comme au national",
    "screen_content": {
        "lead": "2024 R : « Définir la fermentation lactique » (0,5 pt). Une définition a trois éléments.",
        "bullets": ["1. la nature : ce que c'est", "2. le lieu et les conditions", "3. les produits (ou le rôle)",
                    "À toi : quelle définition gagne les 0,5 point ?"],
        "student_trace": "Définir = nature + lieu et conditions + produits.",
    },
    "visual": {"kind": "simulation", "url": NAT + "?vue=restitution&depart=0&cacher=nature",
               "caption": "Examen 2024 R : définir la fermentation lactique",
               "alt": "La consigne du national et trois cadres vides : nature, lieu et conditions, produits"},
    "speech_text": {
        "fr": "Les questions de restitution, comme au national. 2024 R : définir la fermentation lactique, 0,5 point. "
              "Une définition a toujours trois éléments : la nature, ce que c'est ; le lieu et les conditions ; les produits. "
              "S'il en manque un, on perd une partie de la note. À toi : choisis la définition qui a les trois éléments, sans erreur.",
        "mixed": "دابا نخدمو أسئلة الدرس، بحال فالوطني. سؤال ديال deux mille vingt-quatre: définir la "
                 "fermentation lactique، وعليه zéro virgule cinq. la définition فيها ديما تلاتة ديال الحوايج. اللولة: la "
                 "nature، يعني شنو هي. التانية: le lieu و les conditions، يعني فين وكيفاش. التالتة: les produits، يعني "
                 "شنو كتعطي. وإلا نقصات وحدة، كتضيع عليك شي نقطة. دابا نتا: شوف تلاتة ديال الأجوبة، واختار اللي فيها "
                 "تلاتة كاملين، وبلا حتى غلط.",
    },
    "concentration": {
        "demarrer": "reset",
        "pointage": [
            {"mot": "سؤال ديال deux mille", "repere": "enonce"},
            {"mot": "la définition فيها ديما", "commande": "play_until", "parametres": {"moment": "cadres"}},
            {"mot": "اللولة: la", "repere": "cadre_nature"},
            {"mot": "التانية: le lieu", "repere": "cadre_lieu"},
            {"mot": "التالتة: les produits", "repere": "cadre_produit"},
        ],
        "cahier": "Définir = nature + lieu et conditions + produits. Fermentation lactique : dégradation incomplète du glucose "
                  "dans le hyaloplasme, en absence de dioxygène, avec production d'acide lactique et d'une faible quantité "
                  "d'énergie (2 ATP).",
        "reponses": reponses(
            (1, ("مزيان! فيها تلاتة كاملين: dégradation incomplète du glucose، dans le hyaloplasme en absence de dioxygène، "
                 "و l'acide lactique مع شوية ديال l'énergie.",
                 "Oui : la nature (dégradation incomplète du glucose), le lieu et les conditions (hyaloplasme, sans dioxygène), "
                 "les produits (acide lactique, faible quantité d'énergie).")),
            {0: (("فيها حاجة صحيحة: l'acide lactique. ولكن ناقصين incomplète، و فين كتوقع، و بلا dioxygène. قلب على الجواب "
                  "اللي فيه تلاتة كاملين.",
                  "Juste en partie : l'acide lactique y est. Mais il manque « incomplète », le lieu et l'absence de dioxygène. "
                  "Cherche la définition qui a les trois éléments."),
                 ("الجواب هو B. A ناقصة: ما فيهاش le lieu، ما فيهاش بلا dioxygène، وما فيهاش l'énergie. فالامتحان، هاد "
                  "الجواب كياخد غير جزء من النقطة.",
                  "La bonne réponse est B. La A est incomplète : ni le lieu (hyaloplasme), ni l'absence de dioxygène, ni la "
                  "faible quantité d'énergie. Elle ne gagne qu'une partie de la note.")),
             2: (("شوف البلاصة. la fermentation lactique واش كتوقع فla mitochondrie؟ عاود فكر فين كتوقع la glycolyse.",
                  "Regarde le lieu : la fermentation lactique se fait-elle dans la mitochondrie ? Pense au lieu de la "
                  "glycolyse, puis réessaie."),
                 ("الجواب هو B. C فيها كلمة غالطة: la mitochondrie. la fermentation lactique كتوقع فle hyaloplasme. كلمة "
                  "وحدة غالطة كتضيع النقطة.",
                  "La bonne réponse est B. La C contient un mot faux : la mitochondrie. La fermentation lactique se fait dans "
                  "le hyaloplasme. Un seul mot faux fait perdre le point."))}),
    },
    "question": {
        "type": "qcm", "prompt": "Quelle définition de la fermentation lactique gagne les 0,5 point ?",
        "options": ["Une dégradation du glucose qui produit de l'acide lactique.",
                    "Une dégradation incomplète du glucose dans le hyaloplasme, en absence de dioxygène, avec production "
                    "d'acide lactique et d'une faible quantité d'énergie.",
                    "Une dégradation incomplète du glucose dans la mitochondrie, en absence de dioxygène, avec production "
                    "d'acide lactique."],
        "correct": 1, "timeout_seconds": 45,
        "enonce_dit": "سؤال: أشمن définition ديال la fermentation lactique كتاخد zéro virgule cinq؟",
        "demonstration": {
            "parole": "la définition اللي كتاخد النقطة كاملة. dégradation incomplète du glucose، هادي la nature. dans le hyaloplasme، "
                      "en absence de dioxygène، هادو le lieu و les conditions. avec production d'acide lactique et d'une "
                      "faible quantité d'énergie، هادو les produits.",
            "lignes": [
                {"texte": "nature : dégradation incomplète du glucose", "mot": "dégradation incomplète du glucose، هادي"},
                {"texte": "lieu et conditions : dans le hyaloplasme, en absence de dioxygène", "mot": "dans le hyaloplasme، en absence"},
                {"texte": "produits : acide lactique et faible quantité d'énergie (2 ATP)", "mot": "avec production d'acide"},
            ],
        },
    },
    "competence_ids": ["C7"],
}

SLIDES["le_x1b_protons"] = {
    "id": "le_x1b_protons", "slide_type": "evaluation", "title": "Restitution (2/3) : le sens des protons",
    "screen_content": {
        "lead": "La définition au tableau, puis la question suivante du même sujet (2024 R) : le sens des H⁺.",
        "bullets": ["Avant de répondre : refaire de mémoire la membrane interne.",
                    "Au-dessus : l'espace intermembranaire ; au-dessous : la matrice.",
                    "Dans la membrane : la chaîne respiratoire et la sphère pédonculée."],
        "student_trace": "Sens des H⁺ : chaîne respiratoire, matrice → espace intermembranaire ; sphère pédonculée, espace "
                         "intermembranaire → matrice.",
    },
    "visual": {"kind": "simulation", "url": NAT + "?vue=restitution&depart=cadres&cacher=fleche_chaine",
               "caption": "Examen 2024 R : la définition, puis le sens des protons",
               "alt": "Les trois cadres se remplissent ; puis la membrane interne peinte, avec une protéine de la chaîne et une sphère pédonculée"},
    "speech_text": {
        "fr": "La définition au tableau : la nature, dégradation incomplète du glucose ; le lieu et les conditions, dans le "
              "hyaloplasme, en absence de dioxygène ; les produits, acide lactique et peu d'énergie. Puis la phrase complète. "
              "La question suivante du même sujet : le sens des protons. Avant de répondre, refais de mémoire la membrane "
              "interne : au-dessus l'espace intermembranaire, au-dessous la matrice ; dans la membrane, la chaîne respiratoire "
              "et la sphère pédonculée. Quand la chaîne fonctionne, où vont les protons ?",
        "mixed": "نكتبو la définition فle tableau. la nature: dégradation incomplète du glucose. le lieu و les conditions: "
                 "dans le hyaloplasme، en absence de dioxygène. les produits: l'acide lactique، وشوية ديال l'énergie. "
                 "وهادي هي الجملة كاملة. دابا السؤال التاني ديال نفس الامتحان: le sens ديال les protons H plus. قبل ما "
                 "تجاوب، رسم فراسك la membrane interne. الفوق: l'espace intermembranaire. التحت: la matrice. وفla "
                 "membrane: la chaîne respiratoire، و la sphère pédonculée. سؤال: ملي كتخدم la chaîne respiratoire، فين "
                 "كيمشيو les protons؟",
    },
    "concentration": {
        "demarrer": "reset",
        "pointage": [
            {"mot": "la nature: dégradation", "commande": "play_until", "parametres": {"moment": "nature"}},
            {"mot": "le lieu و les conditions:", "commande": "play_until", "parametres": {"moment": "lieu"}},
            {"mot": "les produits: l'acide", "commande": "play_until", "parametres": {"moment": "produit"}},
            {"mot": "وهادي هي الجملة", "commande": "play_until", "parametres": {"moment": "phrase"}},
            {"mot": "رسم فراسك la membrane", "commande": "play_until", "parametres": {"moment": "membrane"}},
            {"mot": "membrane: la chaîne respiratoire", "repere": "chaine"},
            {"mot": "و la sphère pédonculée.", "repere": "sphere"},
        ],
        "cahier": "Sens des H⁺ : chaîne respiratoire, de la matrice vers l'espace intermembranaire ; sphère pédonculée, de "
                  "l'espace intermembranaire vers la matrice.",
        "reponses": reponses(
            (1, ("مزيان! la chaîne كتخرج les protons من la matrice ل l'espace intermembranaire، وهكا كيتكون le gradient.",
                 "Oui : la chaîne respiratoire fait passer les H⁺ de la matrice vers l'espace intermembranaire ; c'est ainsi "
                 "que se forme le gradient.")),
            {0: (("هادا هو الاتجاه ديال la sphère pédonculée، ماشي ديال la chaîne. la chaîne هي اللي كتخرج les protons. منين "
                  "كتخرج؟",
                  "C'est le sens de la sphère pédonculée, pas celui de la chaîne. La chaîne fait sortir les protons : d'où "
                  "sortent-ils ? Réessaie."),
                 ("الجواب هو B. la chaîne كتخرج les protons من la matrice ل l'espace intermembranaire. الاتجاه اللي ختاريتي "
                  "هو ديال la sphère، ملي كيرجعو.",
                  "La bonne réponse est B : la chaîne respiratoire fait passer les H⁺ de la matrice vers l'espace "
                  "intermembranaire. Le sens que tu as choisi est celui de la sphère pédonculée, quand ils reviennent.")),
             2: (("le hyaloplasme برا la mitochondrie. les protons كيبقاو داخل la mitochondrie. شوف الفوق والتحت ديال la "
                  "membrane interne.",
                  "Le hyaloplasme est hors de la mitochondrie. Les protons restent dans la mitochondrie : regarde au-dessus et "
                  "au-dessous de la membrane interne. Réessaie."),
                 ("الجواب هو B: من la matrice ل l'espace intermembranaire. les protons كيبقاو داخل la mitochondrie.",
                  "La bonne réponse est B : de la matrice vers l'espace intermembranaire. Les protons ne sortent pas de la "
                  "mitochondrie."))}),
    },
    "question": {
        "type": "qcm", "prompt": "Pendant le fonctionnement de la chaîne respiratoire, les protons H⁺ passent…",
        "options": ["de l'espace intermembranaire vers la matrice", "de la matrice vers l'espace intermembranaire",
                    "de la matrice vers le hyaloplasme"],
        "correct": 1, "timeout_seconds": 40,
        "enonce_dit": "سؤال: ملي كتخدم la chaîne respiratoire، les protons H plus كيدوزو من فين لفين؟",
        "demonstration": {
            "parole": "la chaîne respiratoire كتخرج les protons، من la matrice ل l'espace intermembranaire. و la sphère "
                      "pédonculée كترجع les protons، من l'espace intermembranaire ل la matrice.",
            "lignes": [
                {"texte": "chaîne respiratoire : H⁺ de la matrice → espace intermembranaire", "mot": "la chaîne respiratoire كتخرج"},
                {"texte": "sphère pédonculée : H⁺ de l'espace intermembranaire → matrice", "mot": "و la sphère"},
            ],
        },
    },
    "competence_ids": ["C6"],
}

SLIDES["le_x1c_qcm"] = {
    "id": "le_x1c_qcm", "slide_type": "evaluation", "title": "Restitution (3/3) : un QCM, le mot faux",
    "screen_content": {
        "lead": "QCM 2022 N : une seule proposition correcte. Le schéma en tête, on cherche le mot faux de chaque proposition.",
        "bullets": ["a. la sphère pédonculée transporte H⁺ vers l'espace intermembranaire ;",
                    "b. la sphère pédonculée est responsable de la phosphorylation de l'ADP ;",
                    "c. la membrane externe contient des protéines qui transportent les électrons vers le dioxygène ;",
                    "d. la membrane externe contient des enzymes d'oxydoréduction."],
        "student_trace": "QCM : refaire le schéma de mémoire, puis chercher le mot faux de chaque proposition (le lieu, le "
                         "sens, le nombre, le produit). 2022 N : (1, b).",
    },
    "visual": {"kind": "simulation", "url": NAT + "?vue=restitution&depart=membrane&cacher=elimine_c",
               "caption": "Examen 2022 N : QCM, éliminer le mot faux",
               "alt": "Les flèches des protons sur la membrane interne, puis les quatre propositions du QCM ; la première est rayée"},
    "speech_text": {
        "fr": "La réponse sur le schéma : dans la chaîne, les protons montent de la matrice vers l'espace intermembranaire ; "
              "dans la sphère, ils redescendent vers la matrice. Maintenant le QCM de 2022 N : quatre propositions, une seule "
              "correcte. La méthode : le schéma en tête, puis chercher le mot faux de chaque proposition. On commence par a : "
              "la sphère porte les protons vers l'espace intermembranaire. Non, le sens est faux : la sphère les ramène vers la "
              "matrice. a est rayée. À toi : b, c ou d ? Cherche le mot faux.",
        "mixed": "شوف الجواب فle schéma. فla chaîne: les protons كيطلعو، من la matrice ل l'espace intermembranaire. وفla "
                 "sphère: كيهبطو، من l'espace ل la matrice. دابا le QCM ديال deux mille vingt-deux. ربعة ديال les "
                 "propositions، وحدة فقط صحيحة. الطريقة: le schéma فراسك، ومن بعد فكل proposition، قلب على الكلمة "
                 "الغالطة. نبداو ب A: la sphère كتخرج les protons ل l'espace intermembranaire. لا، الاتجاه غالط: la sphère "
                 "كترجع les protons ل la matrice. إذن A غالطة، نحيدوها. دابا نتا: B ولا C ولا D؟ قلب على الكلمة الغالطة.",
    },
    "concentration": {
        "demarrer": "reset",
        "pointage": [
            {"mot": "فla chaîne: les protons", "commande": "play_until", "parametres": {"moment": "fleche_chaine"}},
            {"mot": "وفla sphère: كيهبطو", "commande": "play_until", "parametres": {"moment": "fleche_sphere"}},
            {"mot": "دابا le QCM", "commande": "play_until", "parametres": {"moment": "qcm"}},
            {"mot": "نبداو ب A", "repere": "prop_a"},
            {"mot": "إذن A غالطة", "commande": "play_until", "parametres": {"moment": "elimine_a"}},
        ],
        "cahier": "QCM : refaire le schéma de mémoire, puis chercher le mot faux de chaque proposition (le lieu, le sens, le "
                  "nombre, le produit). 2022 N : a faux (le sens), c et d faux (membrane externe) → (1, b).",
        "reponses": reponses(
            (0, ("مزيان! la sphère pédonculée هي l'ATP synthase، كتدير la phosphorylation ديال l'ADP. و C و D غالطين: la "
                 "membrane externe ما فيهاش la chaîne.",
                 "Oui : (1, b). La sphère pédonculée (ATP synthase) phosphoryle l'ADP en ATP. c et d sont fausses : « membrane "
                 "externe » ; la chaîne est dans la membrane interne.")),
            {1: (("قرا مزيان كل كلمة. فين كاينة la chaîne respiratoire: فla membrane interne ولا externe؟",
                  "Lis chaque mot : la chaîne respiratoire est-elle dans la membrane interne ou externe ? Réessaie."),
                 ("الجواب هو A، يعني la proposition b. فهادي كلمة غالطة: externe. les protéines اللي كيدوزو les électrons "
                  "كاينين فla membrane interne.",
                  "La bonne réponse est (1, b). Celle-ci contient un mot faux : « externe ». Les transporteurs d'électrons "
                  "sont dans la membrane interne.")),
             2: (("قلب على الكلمة الغالطة. واش les enzymes ديال l'oxydoréduction كاينين فla membrane externe؟",
                  "Cherche le mot faux : les enzymes d'oxydoréduction sont-elles dans la membrane externe ? Réessaie."),
                 ("الجواب هو A، يعني la proposition b. فهادي نفس الغلط: la membrane externe. l'oxydoréduction كتوقع فla "
                  "membrane interne و فla matrice.",
                  "La bonne réponse est (1, b). Celle-ci contient le même mot faux : « externe ». Les oxydoréductions ont lieu "
                  "dans la membrane interne et la matrice."))}),
    },
    "question": {
        "type": "qcm", "prompt": "QCM 2022 N : a est rayée. Laquelle des trois autres (b, c, d) est correcte ?",
        "options": ["b. la sphère pédonculée est responsable de la phosphorylation de l'ADP",
                    "c. la membrane externe contient des protéines qui transportent les électrons vers le dioxygène",
                    "d. la membrane externe contient des enzymes d'oxydoréduction"],
        "correct": 0, "timeout_seconds": 50,
        "enonce_dit": "سؤال: A غالطة. من التلاتة اللي بقاو، أشمن proposition صحيحة؟",
        "demonstration": {
            "parole": "A غالطة: الاتجاه. C غالطة: la membrane externe، والصحيح la membrane interne. D غالطة حتى هي: la "
                      "membrane externe. B صحيحة: la sphère pédonculée كتدير la phosphorylation ديال l'ADP. فالورقة كتكتب: "
                      "un، b.",
            "lignes": [
                {"texte": "a : faux (le sens : la sphère ramène les H⁺ vers la matrice)", "mot": "A غالطة: الاتجاه"},
                {"texte": "c : faux (membrane externe ; la chaîne est dans la membrane interne)", "mot": "C غالطة"},
                {"texte": "d : faux (membrane externe)", "mot": "D غالطة حتى"},
                {"texte": "b : vrai (la sphère pédonculée phosphoryle l'ADP en ATP)", "mot": "B صحيحة"},
                {"texte": "Réponse : (1, b)", "mot": "فالورقة كتكتب"},
            ],
        },
    },
    "competence_ids": ["C6"],
}

# ─────────────────────────── Voie dominante (2016 N, documents 1 et 2) ───────────────────────────
X2_TABLE = {"headers": ["Critère", "Personne entraînée", "Personne non entraînée"],
            "rows": [["Volume des mitochondries (% du volume de la cellule)", "11", "5"],
                     ["Activité des enzymes mitochondriales", "importante", "faible"],
                     ["Consommation de O₂ (L/min)", "5,5", "2,5"], ["Acide lactique produit (mmol/L)", "6", "12"]]}

SLIDES["le_x2_qui_respire"] = {
    "id": "le_x2_qui_respire", "slide_type": "exercise", "title": "Exercice type : qui respire, qui fermente ? (1/2) — comparer",
    "screen_content": {
        "lead": "Examen 2016 N : deux personnes font le même effort. D'abord, comparer avec les valeurs.",
        "bullets": ["Document 1 : volume des mitochondries, activité des enzymes mitochondriales.",
                    "Document 2 : consommation de O₂ et acide lactique produit.",
                    "Consigne 1 : comparer la personne non entraînée à la personne entraînée."],
        "student_trace": "Comparer : critère par critère, « plus faible (ou plus élevé) chez … (valeur) que chez … (valeur) ».",
        "table": X2_TABLE,
    },
    "visual": {"kind": "simulation", "url": NAT + "?vue=sportifs&depart=0&cacher=comparaison",
               "caption": "Examen 2016 N, documents 1 et 2",
               "alt": "Deux muscles peints font le même effort ; les jauges d'O₂ et d'acide lactique montent, les fibres montrent leurs mitochondries, puis le tableau"},
    "speech_text": {
        "fr": "Un exercice du national 2016. Deux personnes font le même effort : l'une entraînée, l'autre non. Le dioxygène "
              "consommé : 5,5 L/min chez l'entraînée, 2,5 chez la non entraînée. L'acide lactique : 6 mmol/L contre 12. Dans la "
              "fibre musculaire, les mitochondries : 11 % du volume de la cellule et des enzymes très actives chez l'entraînée ; "
              "5 % et des enzymes peu actives chez la non entraînée. Puis tout passe dans le tableau. Consigne 1 : comparer la "
              "personne non entraînée à l'entraînée. Quelle comparaison est rédigée comme le barème ?",
        "mixed": "هادا تمرين كاين فالوطني، deux mille seize. جوج ديال الناس كيديرو نفس l'effort: واحد كيدير الرياضة ديما، "
                 "la personne entraînée، و واحد كيدير قليل، la personne non entraînée. شوف le dioxygène اللي كيستهلكو: "
                 "l'entraînée cinq virgule cinq litres par minute. la non entraînée غير deux virgule cinq. دابا l'acide "
                 "lactique: l'entraînée six millimoles par litre. la non entraînée douze. ودابا نشوفو داخل la fibre "
                 "musculaire: les mitochondries. عند l'entraînée: onze pour cent ديال le volume ديال la cellule، و les "
                 "enzymes ديالها كيخدمو بزاف. عند la non entraînée: غير cinq pour cent، و les enzymes ضعاف. ودابا كلشي "
                 "فle tableau. الطلب اللول: قارن la personne non entraînée مع l'entraînée. سؤال: أشمن مقارنة مكتوبة بحال "
                 "la correction ديال الامتحان؟",
    },
    "concentration": {
        "demarrer": "reset",
        "pointage": [
            {"mot": "جوج ديال الناس كيديرو", "commande": "play_until", "parametres": {"moment": "effort"}},
            {"mot": "شوف le dioxygène اللي", "commande": "play_until", "parametres": {"moment": "o2"}},
            {"mot": "l'entraînée cinq virgule", "repere": "o2_A"},
            {"mot": "la non entraînée غير deux", "repere": "o2_B"},
            {"mot": "دابا l'acide", "commande": "play_until", "parametres": {"moment": "lactique"}},
            {"mot": "la non entraînée douze", "repere": "lac_B"},
            {"mot": "ودابا نشوفو داخل", "commande": "play_until", "parametres": {"moment": "mitochondries"}},
            {"mot": "عند l'entraînée: onze", "repere": "fibre_A"},
            {"mot": "عند la non entraînée: غير", "repere": "fibre_B"},
            {"mot": "ودابا كلشي", "commande": "play_until", "parametres": {"moment": "tableau"}},
        ],
        "cahier": "Comparer (2016 N) : chez la personne non entraînée, le volume des mitochondries est plus faible (5 % contre "
                  "11 %), la consommation de O₂ est plus faible (2,5 L/min contre 5,5 L/min) et l'acide lactique est plus "
                  "élevé (12 mmol/L contre 6 mmol/L).",
        "reponses": reponses(
            (1, ("مزيان! واحد بواحد، مع les valeurs ديال جوج: les mitochondries، le dioxygène، و l'acide lactique.",
                 "Oui : chaque critère, avec les valeurs des deux personnes : mitochondries, O₂ consommé, acide lactique.")),
            {0: (("صحيح فالمعنى، ولكن ما فيهاش les valeurs، ونسيتي le dioxygène. la correction كتبغي كل حاجة مع الرقم ديالها.",
                  "Juste sur le sens, mais sans valeurs, et la consommation de O₂ manque. Le barème veut chaque critère avec "
                  "ses valeurs. Réessaie."),
                 ("الجواب هو B: كل حاجة مع جوج ديال les valeurs. A ما فيهاش الأرقام، و فla correction هاد الجواب كياخد غير جزء من النقطة.",
                  "La bonne réponse est B : chaque critère avec les deux valeurs. A n'a pas de valeurs : elle ne gagne qu'une "
                  "partie des points.")),
             2: (("هادي ماشي مقارنة، هادي déjà l'explication. الطلب اللول كيقول: قارن. شنو كنقارنو؟ les valeurs ديال le tableau.",
                  "Ce n'est pas une comparaison, c'est déjà l'explication. La consigne 1 demande de comparer les valeurs du "
                  "tableau. Réessaie."),
                 ("الجواب هو B. C هي الجواب ديال سؤال آخر: l'explication. فالوطني، كل طلب عندو الجواب ديالو: اللول نقارنو بالأرقام.",
                  "La bonne réponse est B. C répond à une autre question (l'explication). Au national, chaque consigne a sa "
                  "réponse : d'abord la comparaison chiffrée."))}),
    },
    "question": {
        "type": "qcm", "prompt": "Consigne 1 (2016 N) : quelle comparaison est rédigée comme le barème ?",
        "options": ["La personne non entraînée a moins de mitochondries et plus d'acide lactique.",
                    "Chez la personne non entraînée, le volume des mitochondries est plus faible (5 % contre 11 %), la "
                    "consommation de O₂ est plus faible (2,5 L/min contre 5,5 L/min) et l'acide lactique est plus élevé "
                    "(12 mmol/L contre 6 mmol/L).",
                    "La personne non entraînée fait surtout la fermentation lactique, donc elle se fatigue."],
        "correct": 1, "timeout_seconds": 50,
        "enonce_dit": "سؤال: أشمن مقارنة مكتوبة بحال la correction ديال الامتحان؟",
        "demonstration": {
            "parole": "كنقارنو واحد بواحد، مع les valeurs. les mitochondries: cinq pour cent عند la non entraînée، "
                      "contre onze. le dioxygène: deux virgule cinq، contre cinq virgule cinq. l'acide lactique: douze، "
                      "contre six.",
            "lignes": [
                {"texte": "volume des mitochondries plus faible chez la non entraînée (5 % contre 11 %)", "mot": "les mitochondries: cinq"},
                {"texte": "consommation de O₂ plus faible (2,5 L/min contre 5,5 L/min)", "mot": "le dioxygène: deux"},
                {"texte": "acide lactique plus élevé (12 mmol/L contre 6 mmol/L)", "mot": "l'acide lactique: douze"},
            ],
        },
    },
    "competence_ids": ["C9"],
}

SLIDES["le_x2b_fatigue"] = {
    "id": "le_x2b_fatigue", "slide_type": "exercise", "title": "Exercice type : qui respire, qui fermente ? (2/2) — expliquer",
    "screen_content": {
        "lead": "La comparaison au tableau, puis la consigne 2 : expliquer la fatigabilité de la personne non entraînée.",
        "bullets": ["Indices de la respiration : beaucoup de mitochondries, beaucoup de O₂ consommé.",
                    "Indice de la fermentation lactique : beaucoup d'acide lactique.",
                    "Expliquer en flèches, jusqu'à l'ATP et la fatigue."],
        "student_trace": "Expliquer (2016 N) : non entraînée → ATP renouvelé surtout par la fermentation lactique (voie "
                         "anaérobie) → faible production d'ATP (2 ATP par glucose) → fatigabilité élevée.",
        "table": X2_TABLE,
    },
    "visual": {"kind": "simulation", "url": NAT + "?vue=sportifs&depart=tableau&cacher=explication",
               "caption": "Examen 2016 N : la comparaison, puis l'explication",
               "alt": "Le tableau des documents 1 et 2 ; la comparaison s'écrit sous le tableau, ligne par ligne"},
    "speech_text": {
        "fr": "La comparaison au tableau, critère par critère. Consigne 2 du sujet : expliquez l'augmentation de la fatigabilité "
              "chez la personne non entraînée. Pourquoi se fatigue-t-elle plus vite ? Pense à deux choses : combien de "
              "dioxygène et de mitochondries ; et l'acide lactique, quelle voie le produit ? Quelle explication est juste ?",
        "mixed": "شوف la comparaison فle tableau، واحد بواحد. دابا الطلب التاني ديال الامتحان: علاش la fatigue "
                 "كتجي بالزربة عند la personne non entraînée؟ فكر فجوج ديال "
                 "الحوايج. شحال ديال le dioxygène كتستهلك، وشحال ديال les mitochondries عندها؟ و l'acide lactique، أشمن "
                 "voie كتعطيه؟ سؤال: أشمن explication صحيحة؟",
    },
    "concentration": {
        "demarrer": "reset",
        "pointage": [
            {"mot": "شوف la comparaison", "commande": "play_until", "parametres": {"moment": "comparaison"}},
            {"mot": "واحد بواحد. دابا", "repere": "comparaison"},
            {"mot": "شحال ديال le dioxygène", "repere": "ligne_o2"},
            {"mot": "وشحال ديال les mitochondries", "repere": "ligne_mito"},
            {"mot": "و l'acide lactique، أشمن", "repere": "ligne_lact"},
        ],
        "cahier": "Expliquer (2016 N) : la personne non entraînée renouvelle son ATP surtout par la fermentation lactique "
                  "(voie anaérobie) → faible production d'ATP (2 ATP par glucose) → fatigabilité élevée.",
        "reponses": reponses(
            (1, ("مزيان! peu de mitochondries و بزاف ديال l'acide lactique: la fermentation lactique. deux ATP par glucose، "
                 "إذن قليل ديال l'ATP، و la fatigue.",
                 "Oui : peu de mitochondries et beaucoup d'acide lactique → surtout la fermentation lactique → 2 ATP par "
                 "glucose → peu d'ATP → fatigabilité élevée.")),
            {0: (("l'acide lactique ماشي من la respiration. شكون اللي كيعطي l'acide lactique؟",
                  "La respiration ne produit pas d'acide lactique. Quelle voie le produit ? Réessaie."),
                 ("الجواب هو B. l'acide lactique كتعطيه la fermentation lactique. و la non entraînée عندها قليل ديال les "
                  "mitochondries، إذن قليل ديال la respiration.",
                  "La bonne réponse est B. L'acide lactique vient de la fermentation lactique ; avec peu de mitochondries, la "
                  "personne non entraînée respire peu.")),
             2: (("نفس l'effort، إذن نفس الحاجة ديال l'énergie. المشكل فشحال ديال l'ATP كتنتج.",
                  "Même effort, donc même besoin d'énergie. Le problème est la quantité d'ATP produite. Réessaie."),
                 ("الجواب هو B. الجوج كيديرو نفس l'effort. la non entraînée كتنتج قليل ديال l'ATP، حيت كتستعمل surtout la "
                  "fermentation lactique، deux ATP par glucose.",
                  "La bonne réponse est B. Même effort pour les deux ; la personne non entraînée produit peu d'ATP, car elle "
                  "utilise surtout la fermentation lactique (2 ATP par glucose)."))}),
    },
    "question": {
        "type": "qcm", "prompt": "Consigne 2 : pourquoi la personne non entraînée se fatigue-t-elle plus vite ?",
        "options": ["Elle utilise surtout la respiration, qui produit beaucoup d'acide lactique.",
                    "Elle renouvelle son ATP surtout par la fermentation lactique (peu de mitochondries, peu de O₂ consommé) : "
                    "peu d'ATP produit, donc fatigabilité élevée.",
                    "Elle consomme moins de dioxygène, donc elle a besoin de moins d'énergie."],
        "correct": 1, "timeout_seconds": 50,
        "enonce_dit": "سؤال: علاش la fatigue كتجي بالزربة عند la personne non entraînée؟",
        "demonstration": {
            "parole": "l'explication بالflèches. قليل ديال les mitochondries، قليل ديال le dioxygène، وبزاف ديال l'acide "
                      "lactique. إذن كتستعمل surtout la fermentation lactique. la fermentation كتعطي غير deux ATP par "
                      "glucose. إذن قليل ديال l'ATP، و la fatigue كتجي بالزربة.",
            "lignes": [
                {"texte": "non entraînée : mitochondries ↓, O₂ consommé ↓, acide lactique ↑", "mot": "قليل ديال les mitochondries"},
                {"texte": "→ ATP renouvelé surtout par la fermentation lactique (voie anaérobie)", "mot": "إذن كتستعمل surtout"},
                {"texte": "→ 2 ATP par glucose : faible production d'ATP", "mot": "la fermentation كتعطي"},
                {"texte": "→ fatigabilité élevée", "mot": "و la fatigue كتجي"},
            ],
        },
    },
    "competence_ids": ["C9"],
}

# ─────────────────────────── Mitochondries isolées, inhibiteur, hypothèse ───────────────────────────
SLIDES["le_x3_chaine_en_panne"] = {
    "id": "le_x3_chaine_en_panne", "slide_type": "exercise", "title": "Exercice type : la chaîne en panne (1/3) — décrire",
    "screen_content": {
        "lead": "Un document comme au national : des mitochondries isolées, des ajouts, puis un poison.",
        "bullets": ["Les ajouts : glucose (1 min), acide pyruvique (2,5 min), ADP + Pi (4,5 min), cyanure (8 min).",
                    "Consigne 1 : décrire, période par période (entre deux ajouts), avec les valeurs."],
        "student_trace": "Décrire : une période entre deux ajouts, avec les valeurs de [O₂] et de l'ATP.",
    },
    "visual": {"kind": "simulation", "url": EXAO + "&depart=0",
               "caption": "Document type : mitochondries isolées et cyanure",
               "alt": "La suspension de mitochondries : quatre ajouts, les courbes de [O₂] et de l'ATP se tracent sans note écrite"},
    "speech_text": {
        "fr": "Un document comme au national : des mitochondries dans un milieu riche en dioxygène. On mesure le dioxygène et "
              "l'ATP, et on ajoute des substances l'une après l'autre : le glucose, l'acide pyruvique, ADP et phosphate, puis "
              "le cyanure. La courbe entière est devant toi. Consigne 1 : décrire, période par période, entre deux ajouts, "
              "avec les valeurs. Après ADP et phosphate, quelle description est juste ?",
        "mixed": "هادا document بحال اللي فالوطني. عندنا des mitochondries، فواحد milieu فيه بزاف ديال le dioxygène. "
                 "نقيسو le dioxygène و l'ATP، ونزيدو حوايج وحدة بوحدة. شوف: زدنا le glucose. ومن بعد l'acide pyruvique. "
                 "ومن بعد ADP و phosphate. وفاللخر le cyanure. la courbe كاملة قدامك. الطلب اللول: décrire. نوصفو مرحلة "
                 "بمرحلة، مع les valeurs. سؤال: من بعد ADP و phosphate، أشمن description صحيحة؟",
    },
    "concentration": {
        "demarrer": "reset",
        "pointage": [
            {"mot": "هادا document بحال", "repere": "montage"},
            {"mot": "عندنا des mitochondries", "repere": "mitochondries"},
            {"mot": "شوف: زدنا le glucose", "commande": "play_until", "parametres": {"moment": "glucose_ajoute"}},
            {"mot": "ومن بعد l'acide pyruvique", "commande": "play_until", "parametres": {"moment": "pyruvate_ajoute"}},
            {"mot": "ومن بعد ADP", "commande": "play_until", "parametres": {"moment": "o2_baisse_atp_monte"}},
            {"mot": "وفاللخر le cyanure", "commande": "play_until", "parametres": {"moment": "palier_final"}},
            {"mot": "la courbe كاملة", "repere": "graphique"},
        ],
        "cahier": "Décrire par périodes, avec les valeurs. Après le glucose : [O₂] stable à 100 %, ATP stable à 10 UA. Après "
                  "l'acide pyruvique : [O₂] diminue faiblement (100 → 96 %). Après ADP + Pi : [O₂] diminue de 96 à 40 % et "
                  "l'ATP augmente de 10 à 90 UA. Après le cyanure : [O₂] stable à 40 %, ATP stable à 90 UA.",
        "reponses": reponses(
            (0, ("مزيان! وصف مع les valeurs: le dioxygène من quatre-vingt-seize لquarante، و l'ATP من dix "
                 "لquatre-vingt-dix.",
                 "Oui : une description avec les valeurs : [O₂] diminue de 96 à 40 % et l'ATP augmente de 10 à 90 UA.")),
            {1: (("هادي déjà déduction، ماشي description. décrire كيطلب شنو كتدير la courbe، مع الأرقام.",
                  "C'est déjà une déduction. Décrire, c'est dire ce que fait chaque courbe, avec les valeurs. Réessaie."),
                 ("الجواب هو A. فdécrire كنقولو غير شنو كتدير la courbe، مع les valeurs. la déduction كتجي من بعد.",
                  "La bonne réponse est A. Décrire = ce que font les courbes, avec les valeurs ; la déduction vient après.")),
             2: (("شوف مزيان الاتجاه ديال la courbe ديال le dioxygène من بعد ADP و phosphate. كتطلع ولا كتهبط؟",
                  "Regarde le sens de la courbe de [O₂] après ADP + Pi : elle monte ou elle descend ? Réessaie."),
                 ("الجواب هو A. le dioxygène كيهبط من quatre-vingt-seize لquarante، و l'ATP كيطلع من dix لquatre-vingt-dix. "
                  "نتا قلبتي الاتجاه.",
                  "La bonne réponse est A : [O₂] diminue de 96 à 40 % et l'ATP augmente de 10 à 90 UA. Tu as inversé les "
                  "sens."))}),
    },
    "question": {
        "type": "qcm", "prompt": "Consigne 1 : après l'ajout d'ADP + Pi (de 4,5 à 8 min), quelle description est juste ?",
        "options": ["[O₂] diminue de 96 % à 40 % et l'ATP augmente de 10 UA à 90 UA.",
                    "La mitochondrie consomme le dioxygène pour produire l'ATP.",
                    "[O₂] augmente de 40 % à 96 % et l'ATP diminue."],
        "correct": 0, "timeout_seconds": 45,
        "enonce_dit": "سؤال: من بعد ADP و phosphate، أشمن description صحيحة؟",
        "demonstration": {
            "parole": "نوصفو كل مرحلة. من بعد le glucose: le dioxygène ثابت فcent pour cent، و l'ATP ثابت فdix. من بعد "
                      "l'acide pyruvique: le dioxygène كينقص شوية، من cent لquatre-vingt-seize. من بعد ADP و phosphate: le "
                      "dioxygène كينقص من quatre-vingt-seize لquarante، و l'ATP كيطلع من dix لquatre-vingt-dix. من بعد le "
                      "cyanure: بجوج بقاو كيفما هوما، quarante و quatre-vingt-dix.",
            "lignes": [
                {"texte": "après le glucose (1 min) : [O₂] stable à 100 % ; ATP stable à 10 UA", "mot": "من بعد le glucose:"},
                {"texte": "après l'acide pyruvique (2,5 min) : [O₂] diminue faiblement, de 100 à 96 %", "mot": "من بعد l'acide pyruvique:"},
                {"texte": "après ADP + Pi (4,5 min) : [O₂] diminue de 96 à 40 % ; ATP augmente de 10 à 90 UA", "mot": "من بعد ADP و phosphate:"},
                {"texte": "après le cyanure (8 min) : [O₂] stable à 40 % ; ATP stable à 90 UA", "mot": "من بعد le cyanure:"},
            ],
        },
    },
    "competence_ids": ["C9"],
}

SLIDES["le_x3b_deduire"] = {
    "id": "le_x3b_deduire", "slide_type": "exercise", "title": "Exercice type : la chaîne en panne (2/3) — déduire",
    "screen_content": {
        "lead": "Consigne 2 : déduire. Ce que la description permet de dire, avec « donc ».",
        "bullets": ["Après le glucose : rien ne change.",
                    "Après l'acide pyruvique, puis ADP + Pi : [O₂] diminue et l'ATP augmente en même temps."],
        "student_trace": "Déduire : la mitochondrie n'utilise pas le glucose mais l'acide pyruvique ; la consommation de O₂ est "
                         "couplée à la synthèse d'ATP.",
    },
    "visual": {"kind": "simulation", "url": EXAO + "&depart=palier_final",
               "caption": "Document type : déduire",
               "alt": "Les courbes de [O₂] et de l'ATP, avec les quatre ajouts"},
    "speech_text": {
        "fr": "Regarde de nouveau la courbe entière. Consigne 2 : déduire, c'est dire ce que la description nous apprend. Deux "
              "observations : après le glucose, rien ne change ; après l'acide pyruvique, puis ADP et phosphate, le dioxygène "
              "diminue et l'ATP augmente en même temps. Que peut-on déduire ?",
        "mixed": "عاود شوف la courbe كاملة. الطلب التاني: déduire، يعني شنو كنفهمو من هاد الوصف. جوج ديال الملاحظات. le "
                 "glucose: ما تبدل والو. l'acide pyruvique، ومن بعد ADP و phosphate: le dioxygène كينقص، و l'ATP كيطلع فنفس "
                 "الوقت. سؤال: شنو نستنتجو؟",
    },
    "concentration": {
        "demarrer": "reset",
        "pointage": [
            {"mot": "عاود شوف la courbe كاملة", "repere": "graphique"},
            {"mot": "glucose: ما تبدل والو", "repere": "ajout_glucose"},
            {"mot": "l'acide pyruvique، ومن بعد", "repere": "ajout_pyruvate"},
            {"mot": "le dioxygène كينقص،", "repere": "courbe_o2"},
            {"mot": "و l'ATP كيطلع فنفس", "repere": "courbe_atp"},
        ],
        "cahier": "Déduire : la mitochondrie n'utilise pas le glucose mais l'acide pyruvique ; la consommation de O₂ est "
                  "couplée à la synthèse d'ATP.",
        "reponses": reponses(
            (1, ("مزيان! ماشي le glucose، l'acide pyruvique. و la consommation ديال le dioxygène مرتبطة ب l'ATP اللي كتنتج.",
                 "Oui : la mitochondrie utilise l'acide pyruvique, pas le glucose ; la consommation de O₂ est couplée à la "
                 "synthèse d'ATP.")),
            {0: (("شوف شنو وقع ملي زدنا le glucose: واش تبدل شي حاجة؟",
                  "Regarde ce qui se passe après l'ajout de glucose : quelque chose change-t-il ? Réessaie."),
                 ("الجواب هو B. من بعد le glucose ما تبدل والو، إذن le glucose ماشي هو اللي كتستعمل la mitochondrie. كتستعمل l'acide "
                  "pyruvique، و le dioxygène مرتبط ب l'ATP.",
                  "La bonne réponse est B. Après le glucose, rien ne change : la mitochondrie n'utilise pas le glucose, mais "
                  "l'acide pyruvique ; le O₂ consommé et l'ATP produit vont ensemble.")),
             2: (("la courbe ديال le dioxygène كتطلع ولا كتنقص؟",
                  "La courbe de [O₂] monte-t-elle ou diminue-t-elle ? Réessaie."),
                 ("الجواب هو B. le dioxygène كينقص: la mitochondrie كتستهلك le dioxygène، ماشي كتعطيه.",
                  "La bonne réponse est B. [O₂] diminue : la mitochondrie consomme le dioxygène, elle n'en produit pas."))}),
    },
    "question": {
        "type": "qcm", "prompt": "Consigne 2 : que peut-on déduire ?",
        "options": ["La mitochondrie utilise le glucose ; le dioxygène n'a pas de rôle.",
                    "La mitochondrie n'utilise pas le glucose mais l'acide pyruvique ; la consommation de O₂ est couplée à la "
                    "synthèse d'ATP.",
                    "La mitochondrie produit du dioxygène et de l'ATP."],
        "correct": 1, "timeout_seconds": 45,
        "enonce_dit": "سؤال: شنو نستنتجو من هاد le document؟",
        "demonstration": {
            "parole": "le glucose ما بدل والو، إذن le glucose ماشي هو اللي كتستعمل la mitochondrie. l'acide pyruvique خلا le "
                      "dioxygène ينقص، إذن كتستعمل l'acide pyruvique. le dioxygène كينقص و l'ATP كيطلع فنفس الوقت، إذن la "
                      "consommation ديال le dioxygène مرتبطة ب la synthèse ديال l'ATP.",
            "lignes": [
                {"texte": "glucose : rien ne change → la mitochondrie n'utilise pas le glucose", "mot": "le glucose ما بدل"},
                {"texte": "acide pyruvique : [O₂] diminue → la mitochondrie utilise l'acide pyruvique", "mot": "l'acide pyruvique خلا"},
                {"texte": "[O₂] ↓ et ATP ↑ ensemble → consommation de O₂ couplée à la synthèse d'ATP", "mot": "le dioxygène كينقص و"},
            ],
        },
    },
    "competence_ids": ["C9"],
}

SLIDES["le_x3c_hypothese"] = {
    "id": "le_x3c_hypothese", "slide_type": "exercise", "title": "Exercice type : la chaîne en panne (3/3) — hypothèse",
    "screen_content": {
        "lead": "Consigne 3 : proposer une hypothèse sur l'effet du cyanure, puis la vérifier.",
        "bullets": ["Après le cyanure : [O₂] reste à 40 %, l'ATP reste à 90 UA.",
                    "Une hypothèse relie la cause possible à l'observation, au conditionnel.",
                    "Vérifier : « l'hypothèse est vérifiée (ou rejetée) car… » + la donnée du document."],
        "student_trace": "Hypothèse : le cyanure bloquerait la chaîne respiratoire. Vérification : cyanure → électrons arrêtés "
                         "→ O₂ non consommé → pas de gradient → pas d'ATP ; après le cyanure, [O₂] reste à 40 % et l'ATP à "
                         "90 UA : l'hypothèse est vérifiée.",
    },
    "visual": {"kind": "simulation", "url": EXAO + "&depart=hypothese",
               "caption": "Document type : l'hypothèse",
               "alt": "Après le cyanure, les deux courbes restent en palier"},
    "speech_text": {
        "fr": "Maintenant le cyanure. Après le cyanure, le dioxygène reste à 40 % et l'ATP reste à 90 UA. Consigne 3 : "
              "proposez une hypothèse. Une hypothèse relie la cause possible à l'observation, et s'écrit au conditionnel. "
              "Rappelle-toi : où le cyanure bloque-t-il, dans la chaîne ? Quelle hypothèse est bien rédigée ?",
        "mixed": "دابا le cyanure. شوف: من بعد le cyanure، le dioxygène بقا ثابت فquarante، و l'ATP بقا ثابت "
                 "فquatre-vingt-dix. الطلب التالت: proposez une hypothèse. الفرضية كتعطي السبب ديال الملاحظة، وكتكتب "
                 "بالconditionnel. عقل: فين سد le cyanure فla chaîne؟ سؤال: أشمن hypothèse مكتوبة مزيان؟",
    },
    "concentration": {
        "demarrer": "reset",
        "pointage": [
            {"mot": "دابا le cyanure", "repere": "ajout_cyanure"},
            {"mot": "le dioxygène بقا ثابت فquarante", "repere": "courbe_o2"},
            {"mot": "و l'ATP بقا ثابت", "repere": "courbe_atp"},
        ],
        "cahier": "Hypothèse (au conditionnel) : le cyanure bloquerait la chaîne respiratoire. Vérification : cyanure → "
                  "transfert des électrons arrêté → O₂ non consommé → pas de pompage des H⁺ → pas de gradient → pas d'ATP ; "
                  "après le cyanure, [O₂] reste à 40 % et l'ATP à 90 UA : l'hypothèse est vérifiée.",
        "reponses": reponses(
            (1, ("مزيان! بالconditionnel، وكتجمع le cyanure و la chaîne، و le dioxygène و l'ATP.",
                 "Oui : au conditionnel, elle relie le cyanure à la chaîne respiratoire, et à l'arrêt de la consommation de "
                 "O₂ et de la synthèse d'ATP.")),
            {0: (("الفكرة قريبة، ولكن عامة بزاف، وماشي بالconditionnel. فين بالضبط فla mitochondrie؟",
                  "L'idée est proche, mais trop vague et pas au conditionnel. Où exactement dans la mitochondrie ? Réessaie."),
                 ("الجواب هو B: بالconditionnel، وكتعطي السبب، la chaîne اللي توقفات، ديال الملاحظة، le dioxygène و l'ATP.",
                  "La bonne réponse est B : au conditionnel, elle relie la cause (la chaîne bloquée) à l'observation ([O₂] et "
                  "ATP).")),
             2: (("هادي معلومة، ماشي فرضية. الفرضية كتقول السبب ديال الملاحظة ديال le document.",
                  "C'est une information, pas une hypothèse. Une hypothèse explique l'observation du document. Réessaie."),
                 ("الجواب هو B. الفرضية كتقول علاش le dioxygène و l'ATP بقاو ثابت: la chaîne respiratoire توقفات، "
                  "بالconditionnel.",
                  "La bonne réponse est B. L'hypothèse dit pourquoi [O₂] et l'ATP s'arrêtent : la chaîne respiratoire serait "
                  "bloquée (conditionnel)."))}),
    },
    "question": {
        "type": "qcm", "prompt": "Consigne 3 : quelle hypothèse est bien rédigée ?",
        "options": ["Le cyanure bloque la mitochondrie.",
                    "Le cyanure bloquerait la chaîne respiratoire, ce qui arrêterait la consommation de O₂ et la synthèse d'ATP.",
                    "Le cyanure est un poison."],
        "correct": 1, "timeout_seconds": 45,
        "enonce_dit": "سؤال: أشمن hypothèse مكتوبة مزيان؟",
        "demonstration": {
            "parole": "l'hypothèse: le cyanure bloquerait la chaîne respiratoire. نتأكدو بالflèches: le cyanure سد T "
                      "quatre، ما بقاش كيدوزو les électrons، la consommation ديال le dioxygène توقفات، ما كاينش le pompage ديال les protons، ما "
                      "كاينش le gradient، ما كاينش l'ATP. وفle document: من بعد le cyanure، le dioxygène بقا فquarante، و "
                      "l'ATP فquatre-vingt-dix. إذن l'hypothèse est vérifiée.",
            "lignes": [
                {"texte": "Hypothèse : le cyanure bloquerait la chaîne respiratoire.", "mot": "l'hypothèse: le cyanure"},
                {"texte": "cyanure → électrons arrêtés → O₂ non consommé → pas de pompage des H⁺ → pas de gradient → pas d'ATP", "mot": "نتأكدو بالflèches"},
                {"texte": "document : après le cyanure, [O₂] reste à 40 % et l'ATP à 90 UA", "mot": "وفle document"},
                {"texte": "→ l'hypothèse est vérifiée.", "mot": "إذن l'hypothèse"},
            ],
        },
    },
    "competence_ids": ["C9", "C6"],
}

ORDRE_X = ["le_x1_restitution", "le_x1b_protons", "le_x1c_qcm", "le_x2_qui_respire", "le_x2b_fatigue",
           "le_x3_chaine_en_panne", "le_x3b_deduire", "le_x3c_hypothese"]

# Les tableaux qui deviennent des animations (règle 35) : le_e3b (texte et voix gardés), le_m3a (sans voix : texte retouché)
E3B_POINTAGE = [
    {"mot": "درنا des levures", "commande": "play_until", "parametres": {"moment": "flacons"}},
    {"mot": "مع le dioxygène: cent", "commande": "play_until", "parametres": {"moment": "aerobie"}},
    {"mot": "بلا dioxygène: quarante-cinq", "commande": "play_until", "parametres": {"moment": "anaerobie"}},
    {"mot": "وبان l'éthanol.", "repere": "ethanol"},
    {"mot": "باش نقارنو مزيان", "commande": "play_until", "parametres": {"moment": "tableau"}},
    {"mot": "يعني مع le dioxygène، تقريبا", "commande": "play_until", "parametres": {"moment": "rapport"}},
]
M3A_REMPLACER = [("شوف le tableau: les plus كيبينو شحال كاين ديال les molécules radioactives.",
                  "شوف la cellule: les boules هوما les molécules radioactives، و les plus كيبينو شحال كاين منهم."),
                 ("بحال واحد la balise: كنتبعوه فين ما مشى.", "بحال واحد العلامة: نتبعو فين مشى.")]
M3A_FR_ANCIEN = "Où se passe chaque étape ? Une expérience du bac : des cellules reçoivent du glucose marqué au carbone 14, radioactif, comme une balise."
M3A_FR_NOUVEAU = M3A_FR_ANCIEN.replace("une balise", "une marque") + " Les billes lumineuses sont les molécules radioactives ; les plus disent combien il y en a."
M3A_POINTAGE = [
    {"mot": "شوف la cellule:", "repere": "hyaloplasme"},
    {"mot": "فT zéro:", "commande": "play_until", "parametres": {"moment": "t0"}},
    {"mot": "فT un:", "commande": "play_until", "parametres": {"moment": "t1"}},
    {"mot": "فT deux:", "commande": "play_until", "parametres": {"moment": "t2"}},
    {"mot": "فT trois:", "commande": "play_until", "parametres": {"moment": "t3"}},
    {"mot": "فT quatre:", "commande": "play_until", "parametres": {"moment": "t4"}},
    {"mot": "دابا نتا اللي", "commande": "play_until", "parametres": {"moment": "tableau"}},
]


BLOCS_S6 = [
    {"id": "le_s6_b1", "titre": "Restitution comme au national", "slide_ids": ["le_x1_restitution", "le_x1b_protons", "le_x1c_qcm"],
     "cahier": [{"texte": "Définir = nature + lieu et conditions + produits. Fermentation lactique : dégradation incomplète du glucose "
                          "dans le hyaloplasme, en absence de dioxygène, avec production d'acide lactique et d'une faible quantité d'énergie."},
                {"texte": "Sens des H⁺ : chaîne respiratoire, matrice → espace intermembranaire ; sphère pédonculée, espace intermembranaire → matrice."},
                {"texte": "QCM : refaire le schéma de mémoire, puis chercher le mot faux de chaque proposition (lieu, sens, nombre, produit)."}],
     "retrouver": {"prompt": "Cahier fermé : définis la fermentation lactique avec ses trois éléments.",
                   "attendu": "Dégradation incomplète du glucose (nature), dans le hyaloplasme en absence de dioxygène (lieu et conditions), "
                              "avec production d'acide lactique et d'une faible quantité d'énergie (produits).",
                   "competence_id": "C7", "enonce_dit": "شوف هاد السؤال: cahier fermé، définis la fermentation lactique، بالتلاتة ديال الحوايج."},
     "exercice": {"type": "vrai_faux", "prompt": "Vrai ou faux ? (2023 R)",
                  "statements": [{"text": "Le CO₂ est un déchet minéral de la respiration cellulaire et de la fermentation alcoolique.", "correct": True,
                                  "explanation": "Respiration : 6 CO₂ ; fermentation alcoolique : 2 CO₂."},
                                 {"text": "Les sphères pédonculées de la membrane mitochondriale externe produisent de l'ATP.", "correct": False,
                                  "explanation": "Mot faux : « externe ». Les sphères pédonculées sont sur la membrane interne."}],
                  "enonce_dit": "شوف هاد السؤال: vrai ou faux. la première: le CO deux est un déchet minéral de la respiration cellulaire et de la fermentation alcoolique. la deuxième: les sphères pédonculées de la membrane mitochondriale externe produisent de l'ATP."}},
    {"id": "le_s6_b2", "titre": "Quelle voie domine ? (2016 N)", "slide_ids": ["le_x2_qui_respire", "le_x2b_fatigue"],
     "cahier": [{"texte": "Comparer : critère par critère, avec les valeurs des deux personnes (« plus faible chez … (valeur) que chez … (valeur) »)."},
                {"texte": "Indices de la respiration : beaucoup de mitochondries, enzymes mitochondriales actives, forte consommation de O₂ ; "
                          "indices de la fermentation lactique : acide lactique élevé, peu de mitochondries."},
                {"texte": "Expliquer (2016 N) : non entraînée → ATP surtout par la fermentation lactique → 2 ATP par glucose → peu d'ATP → fatigabilité élevée."}],
     "retrouver": {"prompt": "Cahier fermé : cite deux indices de la respiration et un indice de la fermentation lactique dans un document.",
                   "attendu": "Respiration : beaucoup de mitochondries, forte consommation de O₂ (enzymes mitochondriales actives) ; fermentation lactique : acide lactique élevé.",
                   "competence_id": "C9", "enonce_dit": "شوف هاد السؤال: cahier fermé، عطيني جوج ديال les indices ديال la respiration، و واحد ديال la fermentation lactique."},
     "exercice": {"type": "qcm", "prompt": "Des fibres B ont peu de mitochondries et produisent beaucoup d'acide lactique pendant l'effort. Quelle voie domine dans ces fibres ?",
                  "options": ["la respiration", "la fermentation lactique", "aucune des deux"], "correct": 1,
                  "explanation": "Peu de mitochondries et beaucoup d'acide lactique : la fermentation lactique domine (2 ATP par glucose).",
                  "enonce_dit": "شوف هاد السؤال: des fibres B فيهم قليل ديال les mitochondries، وكيعطيو بزاف ديال l'acide lactique. أشمن voie غالبة؟"}},
    {"id": "le_s6_b3", "titre": "Un document : décrire, déduire, proposer et vérifier une hypothèse", "slide_ids": ["le_x3_chaine_en_panne", "le_x3b_deduire", "le_x3c_hypothese"],
     "cahier": [{"texte": "Décrire (périodes bornées par les ajouts, valeurs) → déduire (donc) → hypothèse (conditionnel) → vérifier (vérifiée ou rejetée + la donnée)."},
                {"texte": "Mitochondries isolées : pas d'effet du glucose ; l'acide pyruvique et ADP + Pi : [O₂] ↓ et ATP ↑ ensemble → la mitochondrie utilise "
                          "l'acide pyruvique ; consommation de O₂ couplée à la synthèse d'ATP."},
                {"texte": "Cyanure : électrons arrêtés → O₂ non consommé → pas de pompage des H⁺ → pas de gradient → pas d'ATP. « Le cyanure bloquerait la chaîne "
                          "respiratoire » : vérifiée, car après le cyanure [O₂] reste à 40 % et l'ATP à 90 UA."}],
     "retrouver": {"prompt": "Cahier fermé : dans quel ordre exploite-t-on un document au national ?",
                   "attendu": "Décrire (périodes, valeurs), déduire (donc), proposer une hypothèse au conditionnel, puis la vérifier avec la donnée du document.",
                   "competence_id": "C9", "enonce_dit": "شوف هاد السؤال: cahier fermé، بأشمن ترتيب كنخدمو document فالوطني؟"},
     "exercice": {"type": "qcm", "prompt": "Une substance bouche le canal des sphères pédonculées (les H⁺ ne peuvent plus revenir vers la matrice). Que devient la synthèse d'ATP ?",
                  "options": ["elle augmente", "elle s'arrête", "elle ne change pas"], "correct": 1,
                  "explanation": "Sans retour des H⁺ par les sphères pédonculées, l'ATP n'est plus synthétisé (2023 N : canal de l'ATP synthase déformé).",
                  "enonce_dit": "شوف هاد السؤال: واحد la substance كتسد le canal ديال les sphères pédonculées. شنو كيوقع ل la synthèse ديال l'ATP؟"}},
]
EXO_SYNTHESE = {"type": "qcm", "prompt": "Combien d'ATP par glucose donnent la respiration, puis la fermentation ?",
                "options": ["36 ou 38, puis 2", "2, puis 36 ou 38", "4, puis 2"], "correct": 0,
                "explanation": "Respiration : dégradation complète, 36 ou 38 ATP ; fermentation : dégradation incomplète, 2 ATP.",
                "enonce_dit": "شوف هاد السؤال: شحال ديال l'ATP par glucose كتعطي la respiration، ومن بعد la fermentation؟"}


def controler(s):
    """Chaque `mot` est dans son texte (pointage → voix, démonstration → sa parole)."""
    voix = s["speech_text"]["mixed"]
    for p in s.get("concentration", {}).get("pointage", []):
        assert voix.count(p["mot"]) >= 1, (s["id"], p["mot"])
    demo = (s.get("question") or {}).get("demonstration")
    if demo:
        for l in demo["lignes"]:
            assert l["mot"] in demo["parole"], (s["id"], l["mot"])


def main():
    m = json.load(open(F, encoding="utf-8"))
    act = next(a for a in m["activities"] if any(s["id"] == "le_x1_restitution" for s in a["slides"]))
    anciens = {s["id"]: s for s in act["slides"]}
    garder = [s for s in act["slides"] if s["id"] not in ORDRE_X]   # le_x4_synthese
    x1 = anciens["le_x1_restitution"]
    nouveaux = []
    for i in ORDRE_X:
        s = json.loads(json.dumps(SLIDES[i], ensure_ascii=False))
        if i == "le_x1_restitution":   # les exercices de fin de cours restent attachés à la restitution
            for k in ("exercices_fin_de_cours", "reponses_fin_de_cours"):
                if k in x1:
                    s[k] = x1[k]
        if "stable_id" in anciens.get(i, {}):
            s["stable_id"] = anciens[i]["stable_id"]
        controler(s)
        nouveaux.append(s)
    act["slides"] = nouveaux + garder
    act["duration_minutes"] = max(act.get("duration_minutes", 25), 35)

    S = {s["id"]: s for a in m["activities"] for s in a["slides"]}
    e3b = S["le_e3b_masse_levures"]
    e3b["visual"] = {"kind": "simulation", "url": NAT + "?vue=levures&depart=0",
                     "caption": "Deux cultures de levures : avec et sans O₂",
                     "alt": "Deux béchers peints : la culture aérée se remplit de levures, la culture fermée beaucoup moins ; les masses s'écrivent, puis le tableau et le rapport par gramme de glucose"}
    e3b["concentration"]["pointage"] = E3B_POINTAGE
    e3b["concentration"]["demarrer"] = "reset"
    controler(e3b)

    m3a = S["le_m3a_glucose_marque"]
    for ancien, nouveau in M3A_REMPLACER:
        if ancien in m3a["speech_text"]["mixed"]:
            m3a["speech_text"]["mixed"] = m3a["speech_text"]["mixed"].replace(ancien, nouveau)
            m3a.pop("audio", None)
    if M3A_FR_ANCIEN in m3a["speech_text"]["fr"] and M3A_FR_NOUVEAU not in m3a["speech_text"]["fr"]:
        m3a["speech_text"]["fr"] = m3a["speech_text"]["fr"].replace(M3A_FR_ANCIEN, M3A_FR_NOUVEAU)
    m3a["visual"] = {"kind": "simulation", "url": NAT + "?vue=marquage&depart=0",
                     "caption": "Le glucose marqué au ¹⁴C, de T0 à T4",
                     "alt": "Une cellule peinte et sa mitochondrie : les molécules radioactives passent du milieu au hyaloplasme puis à la mitochondrie ; les + s'écrivent, puis le tableau"}
    m3a["concentration"]["pointage"] = M3A_POINTAGE
    m3a["concentration"]["demarrer"] = "reset"
    controler(m3a)

    # Séances : les cas du bac deviennent une séance à part (séance 6, quatre blocs : une consigne par diapositive, donc
    # plusieurs « À toi » par bloc, comme un exercice du national), la séance 5 garde fermentations et bilans.
    s5 = next(se for se in m["seances"] if se["id"] == "le_s5")
    ancien = next((b for b in s5["blocs"] if b["id"] == "le_s5_b3"), None)
    if ancien is not None:
        s5["blocs"].remove(ancien)
        s5["titre"] = "Séance 5 — Fermentations, bilans et rendements"
        synth = {**ancien, "id": "le_s6_b4", "titre": "Le schéma de synthèse", "slide_ids": ["le_x4_synthese", "le_b1_bilan"],
                 "cahier": ancien["cahier"][3:], "exercice": EXO_SYNTHESE}
        m["seances"].append({"id": "le_s6", "titre": "Séance 6 — Les cas du national joués pas à pas, puis la synthèse",
                             "blocs": BLOCS_S6 + [synth]})
        m["estimated_minutes"] = m.get("estimated_minutes", 245) + 30
    for c in m["competences"]:
        ids = [i for i in c["slide_ids"] if i not in ORDRE_X]
        ids += [i for i in ORDRE_X if c["id"] in SLIDES[i]["competence_ids"]]
        c["slide_ids"] = ids
    json.dump(m, open(F, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print("ok :", len(ORDRE_X), "diapositives d'exercices joués ; le_e3b et le_m3a animées")


if __name__ == "__main__":
    main()
