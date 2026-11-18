"""SVT ch3 — notion de l'information génétique : la logique refaite (18 novembre 2026).
Lit le cours en ligne, écrit backend/data/courses/en_attente/svt_ch3_notion_information_genetique.json.
Architecture et raisons : backend/data/curriculum/architecture/svt_ch3_notion_information_genetique.md"""
import copy, json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from outils import *

R = Path(__file__).resolve().parents[2]
DECK = "svt_ch3_notion_information_genetique"
m = charger(R / f"backend/data/courses/{DECK}.json")
D = diapos(m)

# ---------------------------------------------------------------- I. le noyau : les cas décisifs posés en question
D["ig_l3_section"]["concentration"]["observation"] = observation(
    "غير le rhizoïde اللي كيرجع يدير tige و chapeau كامل.",
    "Seul le morceau avec le rhizoïde refait une algue entière. Est-ce une preuve que le noyau commande ?",
    "شوف مزيان. غير le rhizoïde اللي رجع دار algue كاملة. واش هادي preuve بلي le noyau هو اللي كيتحكم؟",
    [("Le rhizoïde contient le noyau… et contient-il autre chose ?",
      "le rhizoïde فيه le noyau. واش فيه غير le noyau؟", "fragment_3"),
     ("Le rhizoïde contient aussi du cytoplasme. Qui des deux commande : on ne peut pas encore le dire.",
      "le rhizoïde فيه حتى le cytoplasme. شكون اللي كيتحكم: le noyau ولا le cytoplasme؟ خاصنا نعرفو.", None)],
    ["Oui, c'est une preuve : le noyau commande",
     "Non, c'est une hypothèse : le rhizoïde contient aussi du cytoplasme",
     "Non : les trois morceaux finissent par mourir"],
    1,
    [("Pas encore : le rhizoïde contient le noyau, mais aussi du cytoplasme. Lequel des deux commande ? Réfléchis encore.",
      "مازال. le rhizoïde فيه le noyau، ولكن فيه حتى le cytoplasme. شكون فيهم اللي كيتحكم؟ عاود فكر."),
     ("Oui ! Le rhizoïde contient le noyau ET du cytoplasme : on peut seulement supposer que le noyau commande. Il faudra vérifier.",
      "مزيان! le rhizoïde فيه le noyau و فيه le cytoplasme. إذن غير نقدرو نفترضو بلي le noyau هو اللي كيتحكم. خاصنا نتأكدو."),
     ("Non : le rhizoïde, lui, survit et refait une algue entière. Regarde-le encore.",
      "لا، le rhizoïde بقا حي، و رجع دار algue كاملة. شوفو مرة أخرى.")],
    ("C'est une hypothèse : le morceau qui régénère contient le noyau, mais aussi du cytoplasme. On suppose que le noyau commande ; une autre expérience doit le vérifier.",
     "هادي غير hypothèse. الجزء اللي رجع فيه le noyau، ولكن فيه حتى le cytoplasme. كنفترضو بلي le noyau هو اللي كيتحكم، وخاص تجربة أخرى باش نتأكدو."),
    gestes=[{"repere": "fragment_3"}])

D["ig_l4_greffe"]["concentration"]["observation"] = observation(
    "ديال mediterranea، والعكس.",
    "Le rhizoïde de mediterranea (chapeau lisse) reçoit le noyau de crenulata (chapeau crénelé). Quel chapeau repousse ?",
    "دابا فكر نتا. le rhizoïde ديال mediterranea، اللي عندها chapeau lisse، خدا le noyau ديال crenulata، اللي عندها chapeau crénelé. أشمن chapeau غادي يرجع؟",
    [("La forme du chapeau est un caractère héréditaire. Qu'est-ce qu'on a échangé entre les deux espèces ?",
      "الشكل ديال le chapeau caractère héréditaire. شنو اللي بدلنا بين جوج espèces؟", "noyau_cren"),
     ("Le cytoplasme vient de mediterranea, le noyau de crenulata. Si le noyau commande, quel chapeau attend-on ?",
      "le cytoplasme ديال mediterranea، و le noyau ديال crenulata. يلا le noyau هو اللي كيتحكم، أشمن chapeau غادي يبان؟", None)],
    ["Un chapeau lisse, comme mediterranea qui a donné le rhizoïde",
     "Un chapeau crénelé, comme crenulata qui a donné le noyau",
     "Aucun chapeau : l'algue meurt"],
    1,
    [("Le rhizoïde et son cytoplasme viennent bien de mediterranea. Mais qu'est-ce qui porte l'information ? Réessaie.",
      "صحيح، le rhizoïde و le cytoplasme ديال mediterranea. ولكن شكون اللي فيه l'information؟ عاود جاوب."),
     ("Oui ! Le chapeau suit le noyau, pas le cytoplasme : l'hypothèse est vérifiée.",
      "مزيان! le chapeau كيمشي مع le noyau، ماشي مع le cytoplasme. إذن l'hypothèse صحيحة."),
     ("Non : avec un noyau, le rhizoïde refait toujours un chapeau. La question est : lequel ?",
      "لا، ملي كاين le noyau، le rhizoïde ديما كيرجع يدير chapeau. السؤال هو: أشمن chapeau؟")],
    ("Un chapeau crénelé : il a la forme de l'espèce qui a donné le noyau. Le chapeau suit le noyau, pas le cytoplasme.",
     "chapeau crénelé: عندو الشكل ديال l'espèce اللي عطات le noyau. le chapeau كيمشي مع le noyau، ماشي مع le cytoplasme."),
    gestes=[{"repere": "noyau_cren"}])

# Gurdon : l'expérience seule, le résultat posé en question ; la définition passe à la diapositive suivante.
g = D["ig_l5_gurdon"]
reecrire(g,
    fr="Une autre expérience, chez l'animal : Gurdon. Nous avons une grenouille pigmentée et un têtard albinos. On prend un ovule de la grenouille pigmentée et on l'irradie aux UV : son noyau est détruit. Puis on prend le noyau d'une cellule de l'intestin du têtard albinos, et on l'injecte dans l'ovule. L'œuf se divise beaucoup et donne un têtard, puis une grenouille albinos. Le caractère vient du noyau, pas de l'ovule.",
    mixed="تجربة أخرى عند la grenouille: Gurdon. عندنا grenouille pigmentée، و têtard albinos. كناخدو ovule من la grenouille pigmentée، وكنضربوه ب les UV، باش le noyau ديالو ما يبقاش يخدم. ومن بعد كناخدو le noyau ديال خلية ديال le têtard albinos، وكنحطوه ف l'ovule. l'œuf كيتقسم بزاف وكيعطي têtard، وفاللخر grenouille albinos. يعني الصفة جات من le noyau، ماشي من l'ovule.",
    pointage=g["concentration"]["pointage"])
g.pop("question", None)
g["concentration"]["reponses"] = {}
g["screen_content"]["bullets"] = g["screen_content"]["bullets"][:3]
g["screen_content"]["student_trace"] = "Gurdon : un ovule sans noyau (irradié aux UV) reçoit le noyau d'une cellule de têtard albinos ; il donne une grenouille albinos : le caractère vient du noyau."
g["concentration"]["cahier"] = g["screen_content"]["student_trace"]
g["concentration"]["observation"] = observation(
    "وكنحطوه ف l'ovule.",
    "L'ovule vient d'une grenouille pigmentée, le noyau d'un têtard albinos. Que donne cet œuf ?",
    "دابا فكر نتا. l'ovule جا من grenouille pigmentée، و le noyau جا من têtard albinos. شنو غادي يعطي هاد l'œuf؟",
    [("Dans l'ovule, le noyau a été détruit. Il ne reste que son cytoplasme.",
      "ف l'ovule، le noyau تهرس. بقا غير le cytoplasme ديالو.", None),
     ("Le seul noyau de cet œuf vient du têtard albinos. Qui commande, d'après l'acétabulaire ?",
      "le noyau الوحيد ف هاد l'œuf جا من le têtard albinos. شكون اللي كيتحكم، كيف شفنا ف l'acétabulaire؟", None)],
    ["Une grenouille pigmentée, comme celle qui a donné l'ovule",
     "Une grenouille albinos, comme le têtard qui a donné le noyau",
     "Une grenouille à moitié pigmentée, à moitié albinos"],
    1,
    [("L'ovule vient bien de la grenouille pigmentée, mais son noyau a été détruit. Qui commande les caractères ? Réessaie.",
      "صحيح، l'ovule جا من grenouille pigmentée، ولكن le noyau ديالو تهرس. شكون اللي كيتحكم ف les caractères؟ عاود جاوب."),
     ("Oui ! La grenouille est albinos, comme le donneur du noyau : le caractère suit le noyau.",
      "مزيان! la grenouille albinos، بحال اللي عطا le noyau. الصفة كتبع le noyau."),
     ("Non : un seul noyau commande cet œuf. D'où vient-il ?",
      "لا، كاين غير noyau واحد ف هاد l'œuf. منين جا؟")],
    ("Une grenouille albinos : elle a le caractère de l'animal qui a donné le noyau, pas de celui qui a donné l'ovule.",
     "grenouille albinos: عندها الصفة ديال اللي عطا le noyau، ماشي ديال اللي عطا l'ovule."),
    gestes=[{"commande": "play_until", "parametres": {"moment": "noyau_injecte"}}])

# Nouvelle diapositive : la définition, construite après les trois expériences, dite deux fois.
d6 = nouvelle(g, "ig_l6_definition", "Trois expériences, une définition")
d6["visual"] = dict(g["visual"], url="/media/simulations/svt/notion_information_genetique-tableau/noyau.html?vue=gurdon&diapo=l6_definition",
                    caption="Après l'amibe, l'acétabulaire et Gurdon : le caractère suit toujours le noyau")
d6["screen_content"] = {
    "lead": "Amibe, acétabulaire, Gurdon : chaque fois, le caractère suit le noyau.",
    "bullets": ["Amibe : sans noyau, le fragment meurt.", "Acétabulaire : le chapeau suit le noyau greffé.",
                "Gurdon : la grenouille a le caractère du donneur du noyau.",
                "Information génétique : ensemble des instructions, portées par le noyau, qui commandent les caractères héréditaires."],
    "student_trace": "Information génétique : ensemble des instructions, portées par le noyau, qui commandent les caractères héréditaires."}
d6["speech_text"] = {
    "fr": "Trois expériences : l'amibe, l'acétabulaire, Gurdon. Chaque fois, le caractère suit le noyau. Construisons la définition par trois questions. Quoi ? un ensemble d'instructions. Où ? dans le noyau. Quel rôle ? commander les caractères héréditaires. Je relis : l'information génétique est l'ensemble des instructions, portées par le noyau, qui commandent les caractères héréditaires. Autrement dit : le noyau est comme le chef d'une usine. Quand on change le chef, ce qu'on fabrique change comme le veut le nouveau chef, pas comme les murs de l'usine.",
    "mixed": "تلاتة ديال التجارب: l'amibe، l'acétabulaire، و Gurdon. ف كل مرة، الصفة كتبع le noyau. دابا نكتبو la définition ب تلاتة ديال الأسئلة. شنو هي؟ مجموعة ديال المعلومات. فين كاينة؟ ف le noyau. شنو كتدير؟ كتحكم ف les caractères héréditaires. نعاود نقرا: l'information génétique، est l'ensemble des instructions، portées par le noyau، qui commandent les caractères héréditaires. نعاودوها بطريقة أخرى: le noyau بحال المدير ديال واحد المعمل. ملي كنبدلو المدير، المعمل كيدير داكشي اللي بغا المدير الجديد، ماشي داكشي اللي بغاو الحيوط."}
d6["concentration"]["pointage"] = [
    {"mot": "تلاتة ديال التجارب:", "commande": "play_until", "parametres": {"moment": "adulte_albinos"}},
    {"mot": "ف كل مرة، الصفة", "repere": "grenouille_pigmentee"}]
d6["concentration"]["cahier"] = d6["screen_content"]["student_trace"]
d6["slide_type"] = "concept"
d6["question"] = {
    "type": "qcm", "prompt": "Dans les trois expériences (amibe, acétabulaire, Gurdon), le caractère suit toujours…",
    "options": ["le cytoplasme", "le noyau", "la cellule la plus grande"], "timeout_seconds": 30, "correct": 1,
    "enonce_dit": "سؤال: ف التجارب التلاتة، l'amibe، l'acétabulaire و Gurdon، الصفة ديما كتبع شنو؟"}
d6["concentration"]["reponses"] = {"q": reactions(1, 3, {
    0: (("Le cytoplasme est présent dans toutes les expériences, c'est vrai. Mais dans la greffe, le cytoplasme venait de mediterranea et le chapeau était crénelé. Que suivait le chapeau ? Réessaie.",
         "صحيح، le cytoplasme كاين ف كل التجارب. ولكن ف la greffe، le cytoplasme كان ديال mediterranea، و le chapeau جا crénelé. شنو اللي تبع le chapeau؟ عاود جاوب."),
        ("La bonne réponse : le noyau. Dans la greffe, le chapeau a la forme de l'espèce qui a donné le noyau ; chez Gurdon, la grenouille a le caractère du donneur du noyau.",
         "الجواب الصحيح هو le noyau. ف la greffe، le chapeau عندو الشكل ديال l'espèce اللي عطات le noyau. و عند Gurdon، la grenouille عندها الصفة ديال اللي عطا le noyau.")),
    1: ("Oui : chaque fois, le caractère suit le noyau. C'est lui qui porte l'information génétique.",
        "مزيان، جوابك صحيح. ف كل مرة، الصفة كتبع le noyau. هو اللي فيه l'information génétique."),
    2: (("La taille ne compte pas ici. Regarde ce qu'on a échangé dans la greffe et chez Gurdon. Réessaie.",
         "الحجم ماشي هو المهم هنا. شوف شنو اللي بدلنا ف la greffe و عند Gurdon. عاود جاوب."),
        ("La bonne réponse : le noyau. Dans la greffe comme chez Gurdon, on a changé le noyau, et le caractère a suivi le noyau.",
         "الجواب الصحيح هو le noyau. ف la greffe و عند Gurdon، بدلنا le noyau، و الصفة مشات مع le noyau.")),
})}
D[d6["id"]] = d6

# ---------------------------------------------------------------- II. noyau : la chromatine d'abord, puis le chromosome
p1 = D["ig_p1_chromosomes"]
reecrire(p1,
    fr="Quand la cellule se divise, la chromatine devient des chromosomes. Combien ? Chez l'homme, chaque cellule du corps en a quarante-six, qui vont par deux : vingt-trois paires. Dans chaque paire, un chromosome vient de la mère et un du père. Les deux chromosomes d'une paire sont homologues. On écrit : 2n = 46, et n = 23 paires. On dit que la cellule est diploïde. Si on déroule un chromosome, on trouve un fil très long et très fin : l'ADN, enroulé autour de protéines. Autrement dit : le noyau est comme une bibliothèque de quarante-six livres rangés par paires : un livre de la mère, un livre du père. Mais une question reste : l'information est-elle écrite dans l'ADN, ou dans les protéines ? Nous y répondrons plus tard, par des expériences.",
    mixed="شفنا بلي ملي الخلية كتقسم، la chromatine كتولي des chromosomes. شحال من chromosome؟ عند الإنسان، كل خلية ديال الجسم فيها quarante-six chromosomes. وكيمشيو جوج بجوج: vingt-trois paires. ف كل paire، chromosome جا من الأم، و chromosome جا من الأب. هادو جوج chromosomes homologues. ونكتبو: deux n égale quarante-six، و n égale vingt-trois paires. نقولو: la cellule diploïde. ويلا شفنا داخل chromosome واحد، كنلقاو خيط طويل بزاف ورقيق: هادا هو l'A D N، ملفوف على des protéines. نعاودوها بطريقة أخرى. تخيل le noyau بحال بلاصة فيها quarante-six كتاب، جوج بجوج: كتاب من الأم، وكتاب من الأب. ولكن بقا سؤال: l'information، واش مكتوبة ف l'A D N، ولا ف les protéines؟ غادي نجاوبو عليه من بعد، ب des expériences.",
    pointage=[
        {"mot": "شفنا بلي ملي", "commande": "play_until", "parametres": {"moment": "k_noyau"}},
        {"mot": "شفنا بلي ملي", "repere": "noyau"},
        {"mot": "شحال من chromosome؟", "commande": "play_until", "parametres": {"moment": "k_chromosomes"}},
        {"mot": "وكيمشيو جوج بجوج:", "repere": "chromosomes"},
        {"mot": "ف كل paire،", "commande": "play_until", "parametres": {"moment": "k_paire"}},
        {"mot": "chromosome جا من الأم،", "repere": "mere"},
        {"mot": "chromosome جا من الأب.", "repere": "pere"},
        {"mot": "ويلا شفنا داخل chromosome", "commande": "play_until", "parametres": {"moment": "k_adn"}},
        {"mot": "هادا هو l'A D N،", "repere": "adn"},
        {"mot": "نعاودوها بطريقة أخرى", "commande": "play_until", "parametres": {"moment": "k_livres"}},
        {"mot": "تخيل le noyau بحال", "repere": "livres"}])
p1["screen_content"]["lead"] = "Dans le noyau, 46 chromosomes en 23 paires ; un chromosome déroulé est un long fil d’ADN, enroulé autour de protéines."
p1["screen_content"]["bullets"] = [
    "Une cellule humaine du corps a 46 chromosomes, rangés en 23 paires.",
    "Dans chaque paire : un chromosome venu de la mère, un venu du père : deux chromosomes homologues.",
    "On écrit 2n = 46 (n = 23 paires) : la cellule est diploïde.",
    "Un chromosome déroulé est un très long fil fin : l’ADN, enroulé autour de protéines.",
    "Question pour plus tard : l’information est-elle dans l’ADN ou dans les protéines ?"]
p1["screen_content"]["student_trace"] = "Noyau humain : 46 chromosomes = 23 paires de chromosomes homologues (un de la mère, un du père) ; 2n = 46 : la cellule est diploïde. Un chromosome = ADN + protéines."
p1["concentration"]["cahier"] = p1["screen_content"]["student_trace"]

# ---------------------------------------------------------------- III. durée du cycle : la question avant le calcul
c6 = D["ig_c6_durees"]
centre = c6["concentration"]["centre"]
reecrire(c6,
    fr="Exercice de calcul, comme à l'examen. À zéro heure, 2,5 fois dix puissance trois cellules ; à quarante heures, dix fois dix puissance trois. À chaque cycle, chaque cellule en donne deux : le nombre double. Question : combien de cycles en quarante heures, et combien dure un cycle ?",
    mixed="تمرين ديال الحساب، بحال ف l'examen. ف zéro heure، deux virgule cinq fois dix puissance trois cellules. ف quarante heures، dix fois dix puissance trois. ف كل cycle، كل خلية كتعطي جوج: العدد كيولي deux fois. سؤال: شحال من cycle دازو ف quarante heures، وشحال كياخد cycle واحد؟",
    pointage=[
        {"mot": "ف zéro heure،", "commande": "play_until", "parametres": {"moment": "depart"}},
        {"mot": "deux virgule cinq fois", "repere": "boite"},
        {"mot": "ف quarante heures،", "commande": "play_until", "parametres": {"moment": "quarante_heures"}}])
c6["title"] = "Calculer la durée du cycle"
c6["concentration"].pop("centre", None)
c6["screen_content"] = {
    "lead": "En 40 h, le nombre de cellules passe de 2,5·10³ à 10·10³ : combien de cycles ?",
    "bullets": ["À chaque cycle, chaque cellule en donne deux : le nombre double.",
                "Compter les doublements, pas le rapport 10·10³ / 2,5·10³."],
    "student_trace": "Durée du cycle : compter les doublements (2,5·10³ → 5·10³ → 10·10³ : 2 cycles en 40 h), donc durée d'un cycle = 40 h / 2 = 20 h."}
c6["concentration"]["cahier"] = c6["screen_content"]["student_trace"]

c6b = nouvelle(c6, "ig_c6b_phases", "Calculer la durée d'une phase")
c6b["slide_type"] = "exercise"
c6b["speech_text"] = {
    "fr": "Un cycle dure vingt heures. Et chaque phase ? Voici le pourcentage de cellules dans chaque phase. La relation : la durée d'une phase égale le pourcentage de cellules dans cette phase, sur cent, fois la durée du cycle. G1 : 45 sur 100, soit 0,45, fois vingt heures : neuf heures. G2 : 20 sur 100, soit 0,2, fois vingt heures : quatre heures. M : 5 sur 100, soit 0,05, fois vingt heures : une heure. Phase S : vingt heures moins la somme neuf plus quatre plus un, soit vingt moins quatorze : six heures. Donc la phase S dure six heures. Attention : n'oublie pas M dans la somme.",
    "mixed": "دابا عرفنا: cycle واحد كياخد vingt heures. وكل phase، شحال كتاخد؟ هاد المرة عندنا le pourcentage ديال الخلايا ف كل phase. la relation: la durée d'une phase، égale le pourcentage de cellules dans cette phase، sur cent، fois la durée du cycle. G un: quarante-cinq sur cent، égale zéro virgule quarante-cinq، fois vingt heures، égale neuf heures. G deux: vingt sur cent، égale zéro virgule deux، fois vingt heures، égale quatre heures. M: cinq sur cent، égale zéro virgule zéro cinq، fois vingt heures، égale une heure. و la phase S: vingt heures، moins la somme، neuf plus quatre plus un، يعني vingt moins quatorze، égale six heures. إذن la phase S كتاخد six heures. رد البال: ما تنساش M ف la somme."}
c6b["concentration"]["pointage"] = [
    {"mot": "دابا عرفنا:", "commande": "play_until", "parametres": {"moment": "duree_cycle"}},
    {"mot": "هاد المرة عندنا", "commande": "play_until", "parametres": {"moment": "pourcentages"}},
    {"mot": "la durée d'une phase", "repere": "phases"},
    {"mot": "G un: quarante-cinq", "commande": "play_until", "parametres": {"moment": "duree_g1"}},
    {"mot": "و la phase", "commande": "play_until", "parametres": {"moment": "duree_s"}},
    {"mot": "و la phase", "repere": "resultat"}]
c6b["concentration"]["centre"] = [x for x in centre if x["mot"] not in ("deux virgule cinq fois dix puissance trois، fois deux", "la durée d'un cycle، égale")]
for x in c6b["concentration"]["centre"]:
    if x["mot"] == "إذن la phase S dure":
        x["mot"] = "إذن la phase S كتاخد"
c6b["screen_content"] = {
    "lead": "Le pourcentage de cellules dans une phase donne la durée de cette phase.",
    "bullets": ["durée d'une phase = (% de cellules dans la phase)/100 × durée du cycle.",
                "G1 = 9 h ; G2 = 4 h ; M = 1 h ; S = 20 h − (9 + 4 + 1) h = 6 h.",
                "Ne pas oublier M dans la somme."],
    "student_trace": "durée d'une phase = (% de cellules dans la phase)/100 × durée du cycle ; exemple (cycle de 20 h) : G1 = 45/100 × 20 h = 9 h ; G2 = 20/100 × 20 h = 4 h ; M = 5/100 × 20 h = 1 h ; S = 20 h − (9 + 4 + 1) h = 6 h."}
c6b["concentration"]["cahier"] = c6b["screen_content"]["student_trace"]
c6b["concentration"]["observation"] = observation(
    "fois vingt heures، égale une heure.",
    "Le pourcentage de la phase S n'est pas donné. Comment trouver sa durée ?",
    "le pourcentage ديال la phase S ما كاينش. كيفاش نلقاو la durée ديالها؟",
    [("Le cycle entier dure 20 h : G1 + S + G2 + M = 20 h.", "le cycle كامل كياخد vingt heures: G un، و S، و G deux، و M.", None),
     ("On connaît G1, G2 et M. Que reste-t-il pour S ?", "عرفنا G un، و G deux، و M. شنو بقا ل S؟", None)],
    ["S = 20 h − (9 + 4 + 1) h = 6 h", "S = 9 + 4 + 1 = 14 h", "S = 20 h − (9 + 4) h = 7 h"],
    0,
    [("Oui : le cycle dure 20 h ; on retire les trois phases connues, M comprise : S = 6 h.",
      "مزيان! le cycle كياخد vingt heures، كنحيدو منو التلاتة اللي عرفنا، حتى M: S كتاخد six heures."),
     ("14 h, c'est la somme des trois autres phases, pas la phase S. Que reste-t-il sur les 20 h ?",
      "quatorze heures هي la somme ديال التلاتة الآخرين، ماشي la phase S. شحال بقا من vingt heures؟"),
     ("Tu as oublié M dans la somme. Réessaie avec les trois phases.",
      "نسيتي M ف la somme. عاود ب التلاتة ديال les phases.")],
    ("S = 20 h − (9 h + 4 h + 1 h) = 20 h − 14 h = 6 h : on retire du cycle les trois phases connues, sans oublier M.",
     "S كتساوي vingt heures، moins neuf plus quatre plus un، يعني vingt moins quatorze، égale six heures. ما تنساش M."))
c6b["visual"] = dict(c6b["visual"], url=c6b["visual"]["url"] + "&diapo=c6b_phases")
D[c6b["id"]] = c6b

# ---------------------------------------------------------------- IV. anaphase : l'élève voit la migration avant qu'on la dise
m4 = D["ig_m4_anaphase"]
fig_telo = m4["concentration"].pop("cahier_figures", None)
reecrire(m4,
    fr="La troisième phase : l'anaphase. Le centromère se coupe : les deux chromatides de chaque chromosome se séparent. Regarde où part chaque chromatide. Les chromatides d'un même chromosome vont-elles au même pôle ?",
    mixed="la troisième phase: l'anaphase. le centromère كيتقسم: les deux chromatides ديال كل chromosome كيمشيو كل وحدة بوحدها. شوف مزيان فين كتمشي كل chromatide. سؤال: واش les chromatides ديال نفس le chromosome كيمشيو ل نفس le pôle؟",
    pointage=[
        {"mot": "la troisième phase", "commande": "set_time", "parametres": {"time_s": 13.2}},
        {"mot": "le centromère كيتقسم:", "commande": "play_until", "parametres": {"moment": "clivage_centromere"}},
        {"mot": "شوف مزيان فين", "commande": "play_until", "parametres": {"moment": "migration"}},
        {"mot": "شوف مزيان فين", "repere": "chromatides"}])
m4["title"] = "L'anaphase"
m4["screen_content"] = {
    "lead": "Le centromère se coupe : les deux chromatides de chaque chromosome se séparent.",
    "bullets": ["Anaphase : clivage du centromère.",
                "Les chromatides sœurs (devenues chromosomes fils à une chromatide) migrent vers les pôles opposés."],
    "student_trace": "Anaphase : clivage du centromère, migration des chromatides (chromosomes fils) vers les pôles opposés."}
m4["concentration"]["cahier"] = m4["screen_content"]["student_trace"]

m4b = nouvelle(m4, "ig_m4b_telophase", "La télophase")
m4b["speech_text"] = {
    "fr": "Les chromatides sont arrivées aux pôles. La dernière phase : la télophase. La cellule se resserre au milieu : l'étranglement. Les chromosomes deviennent des fils : la décondensation. L'enveloppe nucléaire et le nucléole réapparaissent : deux noyaux se forment. Et le fuseau disparaît. Pour reconnaître : s'il y a deux noyaux, c'est la télophase. À la fin, deux cellules filles.",
    "mixed": "les chromatides وصلو ل les pôles. la dernière phase: la télophase. الخلية كتنقص ف الوسط: l'étranglement. les chromosomes كيوليو خيوط: la décondensation. l'enveloppe nucléaire و le nucléole كيرجعو: كيتكونو جوج ديال les noyaux. و le fuseau كيمشي. باش تعرف: يلا كاينين جوج noyaux، هادي la télophase. وفاللخر، جوج cellules filles."}
m4b["concentration"]["pointage"] = [
    {"mot": "les chromatides وصلو", "commande": "set_time", "parametres": {"time_s": 13.2}},
    {"mot": "les chromatides وصلو", "commande": "play_until", "parametres": {"moment": "migration"}},
    {"mot": "la dernière phase:", "commande": "play_until", "parametres": {"moment": "etranglement"}},
    {"mot": "الخلية كتنقص ف", "repere": "etranglement"},
    {"mot": "les chromosomes كيوليو", "commande": "play_until", "parametres": {"moment": "deux_noyaux"}},
    {"mot": "جوج ديال les noyaux", "repere": "noyaux_fils"}]
m4b["screen_content"] = {
    "lead": "Étranglement, décondensation, deux noyaux : deux cellules filles.",
    "bullets": ["Télophase : étranglement équatorial ; les chromosomes se décondensent.",
                "L'enveloppe nucléaire et le nucléole réapparaissent ; le fuseau disparaît.",
                "Deux noyaux visibles et un étranglement : c'est la télophase ; puis deux cellules filles."],
    "student_trace": "Télophase : décondensation des chromosomes, réapparition de l'enveloppe nucléaire et du nucléole, disparition du fuseau, étranglement : deux cellules filles. Schéma titré « Télophase d'une cellule animale (2n = 4) », légendes : étranglement, enveloppe nucléaire, nucléole, chromatine."}
m4b["concentration"]["cahier"] = m4b["screen_content"]["student_trace"]
if fig_telo:
    m4b["concentration"]["cahier_figures"] = fig_telo
m4b["visual"] = dict(m4b["visual"], url="/media/simulations/svt/notion_information_genetique-tableau/mitose.html?vue=animale&diapo=m4b_telophase")
D[m4b["id"]] = m4b

# ---------------------------------------------------------------- V. Griffith : le bilan après la dernière expérience, sans redite de l'ouverture
t1f = D["ig_t1f_bilan"]
reecrire(t1f,
    fr="Mettons les quatre expériences ensemble. Il y a deux formes de pneumocoques : la forme S, avec une capsule, qui tue ; et la forme R, sans capsule, qui ne tue pas. S vivants : la souris meurt. R vivants : la souris vit. S tués par la chaleur : elle vit. Mais R vivants avec des S tués : la souris meurt ! Et dans son sang, on trouve des S vivants. Quelque chose des S morts a transformé des R en S : on l'appelle le principe transformant.",
    mixed="دابا نجمعو التجارب الربعة. عندنا جوج ديال les pneumocoques: la forme S، عندها capsule، خطيرة. و la forme R، بلا capsule، ماشي خطيرة. S vivants: la souris كتولي ميتة. R vivants: la souris كتبقى مزيانة. S ميتين ب الحرارة: كتبقى مزيانة. ولكن R vivants مع S ميتين: la souris كتولي ميتة! وف الدم ديالها كنلقاو S vivants. يعني شي حاجة من S اللي ميتين، بدلات R ل S. كنسميوها le principe transformant.")

# ---------------------------------------------------------------- VI. Chargaff : la déduction posée en question
D["ig_s2_chargaff"]["concentration"]["observation"] = observation(
    "عند le mouton و le poulet، نفس الشي.",
    "Chez l'Homme, le mouton et le poulet : A/T ≈ 1 et C/G ≈ 1. Qu'en déduis-tu ?",
    "عند الإنسان، و le mouton، و le poulet: A sur T تقريبا un، و C sur G تقريبا un. شنو نقدرو نقولو؟",
    [("A/T ≈ 1 veut dire : il y a autant de A que de T.", "A sur T تقريبا un، يعني نفس العدد ديال A و T.", "rapport_at"),
     ("Si chaque A a toujours un T, et chaque C un G, que font ces bases ?", "يلا كل A عندو T، و كل C عندو G، شنو كيديرو هاد les bases؟", None)],
    ["Autant de A que de T, autant de C que de G : A s'associe à T, C à G",
     "A s'associe à G, et C à T",
     "Les quatre bases ont le même pourcentage"],
    0,
    [("Oui ! A = T et C = G chez toutes les espèces : A s'associe à T, et C à G.",
      "مزيان! A كيساوي T، و C كيساوي G عند جميع les espèces. إذن A كيتجمع مع T، و C مع G."),
     ("Compare les pourcentages : A (30,9 %) est proche de T (29,4 %), pas de G (19,9 %). Réessaie.",
      "قارن les pourcentages: A، trente virgule neuf، قريب من T، vingt-neuf virgule quatre، ماشي من G. عاود جاوب."),
     ("Non : chez l'Homme, A fait 30,9 % et G 19,9 %. Ce ne sont pas les mêmes. Quelles bases sont égales deux à deux ?",
      "لا، عند الإنسان A فيها trente virgule neuf، و G فيها dix-neuf virgule neuf. ماشي بحال بحال. أشمن جوج bases اللي متساويين؟")],
    ("A/T ≈ 1 et C/G ≈ 1 : il y a autant de A que de T, et autant de C que de G. On en déduit que A s'associe à T, et C à G.",
     "A sur T تقريبا un، و C sur G تقريبا un: نفس العدد ديال A و T، ونفس العدد ديال C و G. إذن A كيتجمع مع T، و C مع G."),
    gestes=[{"repere": "rapport_cg"}])

# ---------------------------------------------------------------- VII. Meselson et Stahl : chaque génération posée en question
D["ig_r3_g1"]["concentration"]["observation"] = observation(
    "lourde، un virgule sept cent vingt-quatre.",
    "On passe en génération 1, sur azote léger. Combien de bandes dans le tube, et où ?",
    "دابا génération un، ف l'azote léger. شوف le tube: شحال من bande، وفين؟",
    [("Compare avec les deux tubes repères : ADN léger en haut, ADN lourd en bas.",
      "قارن مع جوج tubes: l'A D N léger الفوق، و l'A D N lourd التحت.", "tube_g1"),
     ("La bande n'est ni en haut ni en bas.", "la bande ماشي الفوق، و ماشي التحت.", None)],
    ["Deux bandes : une lourde et une légère", "Une seule bande, au milieu, entre léger et lourd",
     "Une seule bande, lourde, comme en génération 0"],
    1,
    [("C'est ce que prévoyait l'hypothèse conservative. Mais regarde le tube : combien de bandes vois-tu ?",
      "هادا هو اللي كانت كتقول la conservative. ولكن شوف le tube: شحال من bande كتشوف؟"),
     ("Oui ! Une seule bande, au milieu : un ADN hybride, entre léger et lourd.",
      "مزيان! bande وحدة، ف الوسط: A D N hybride، بين léger و lourd."),
     ("Non : la bande est montée. Elle n'est plus au niveau de l'ADN lourd. Où est-elle ?",
      "لا، la bande طلعات. ماشي ف البلاصة ديال l'A D N lourd. فين هي؟")],
    ("Une seule bande, au milieu (1,717 g·cm⁻³) : entre l'ADN léger (1,710) et l'ADN lourd (1,724). C'est un ADN hybride.",
     "bande وحدة، ف الوسط، un virgule sept cent dix-sept. بين l'A D N léger و l'A D N lourd. هادا A D N hybride."),
    gestes=[{"commande": "play_until", "parametres": {"moment": "g1_bande"}}, {"repere": "tube_g1"}])

r4 = D["ig_r4_g2"]
t4 = r4["speech_text"]["mixed"].replace("غير la semi-conservative اللي كتفسر هاد النتيجة.", "بقات غير la semi-conservative: هي اللي صحيحة.")
assert "بقات غير la semi-conservative" in t4
reecrire(r4,
    fr="Après la génération un, il reste deux hypothèses : la semi-conservative et la dispersive. Pour les départager, il faut la génération deux. Regarde le tube. " + r4["speech_text"]["fr"],
    mixed="من بعد génération un، بقاو جوج hypothèses: la semi-conservative و la dispersive. باش نفرقو بيناتهم، خاصنا génération deux. شوف le tube. " + t4,
    pointage=[{"mot": "من بعد génération un،", "commande": "set_time", "parametres": {"time_s": 20.4}}] +
             [p for p in r4["concentration"]["pointage"] if p.get("commande") != "set_time"])
r4["concentration"]["observation"] = observation(
    "خاصنا génération deux. شوف le tube.",
    "Génération 2 : combien de bandes ? Laquelle des deux hypothèses restantes est rejetée ?",
    "génération deux: شحال من bande كتشوف؟ وأشمن hypothèse ماشي صحيحة؟",
    [("La dispersive mélange l'ancien et le nouveau dans chaque brin : elle donne toujours une seule bande.",
      "ف la dispersive، القديم و الجديد مخلطين ف كل brin: ديما bande وحدة.", "h_dispersive"),
     ("Compte les bandes dans le tube de la génération 2.", "حسب les bandes ف le tube ديال génération deux.", "tube_g2")],
    ["Une seule bande : la dispersive est confirmée",
     "Deux bandes, hybride et légère : la dispersive est rejetée",
     "Deux bandes, lourde et légère : la semi-conservative est rejetée"],
    1,
    [("Regarde le tube : il y a deux bandes, pas une. Que prévoyait la dispersive ?",
      "شوف le tube: كاينين جوج bandes، ماشي وحدة. شنو كانت كتقول la dispersive؟"),
     ("Oui ! Deux bandes, hybride et légère : la dispersive, qui prévoyait une seule bande, est rejetée.",
      "مزيان! جوج bandes، hybride و légère. la dispersive كانت كتقول bande وحدة: إذن ماشي صحيحة."),
     ("Il n'y a plus d'ADN lourd : aucune bande en bas. Regarde où sont les deux bandes.",
      "ما بقاش A D N lourd: حتى bande ما كاينة التحت. شوف فين كاينين جوج bandes.")],
    ("Deux bandes de même quantité, hybride et légère. La dispersive prévoyait une seule bande : elle est rejetée. Seule la semi-conservative reste.",
     "جوج bandes بنفس الكمية، hybride و légère. la dispersive كانت كتقول bande وحدة: ماشي صحيحة. بقات غير la semi-conservative."),
    gestes=[{"commande": "play_until", "parametres": {"moment": "g2_bandes"}}, {"repere": "tube_g2"}])

# ---------------------------------------------------------------- les compétences des nouvelles diapositives
d6["competence_ids"] = ["C1"]
c6b["competence_ids"] = ["C3"]
m4b["competence_ids"] = ["C4"]

# ---------------------------------------------------------------- l'ordre : parties, séances, blocs
recouper(m, [
    ("ig_ouverture", None, None, ["ig_o1_ressemblance", "ig_o2_rappel"]),
    ("ig_partie1", None, 35, ["ig_l1_amibe", "ig_l2_acetabulaire", "ig_l3_section", "ig_l4_greffe", "ig_l5_gurdon", "ig_l6_definition"]),
    ("ig_partie2", "II. Dans le noyau : chromatine, chromosomes, et la mitose en une idée", 25,
     ["ig_n1_noyau", "ig_n2_condensation", "ig_n1b_feulgen", "ig_p1_chromosomes", "ig_p2_mitose", "ig_p3_mitose_corps", "ig_n3_chromatides"]),
    ("ig_partie3", None, 40, ["ig_c1_cycle", "ig_c3_courbe", "ig_c2_pourquoi", "ig_c4_aspect", "ig_c5_decrire", "ig_c6_durees", "ig_c6b_phases"]),
    ("ig_partie4", None, 45, ["ig_m1_mitose", "ig_m2_prophase", "ig_m3_metaphase", "ig_m4_anaphase", "ig_m4b_telophase", "ig_m5_vegetale", "ig_m6_photo", "ig_m7_schema", "ig_m7b_legender"]),
    ("ig_partie5", None, 25, ["ig_t1_griffith", "ig_t1b_exp1", "ig_t1c_exp2", "ig_t1d_exp3", "ig_t1e_exp4", "ig_t1f_bilan", "ig_t2_avery", "ig_t2b_avery_resultats", "ig_t3_support"]),
    ("ig_partie6", None, None, ["ig_s1_nucleotide", "ig_s2_chargaff", "ig_s3_antiparalleles", "ig_s4_helice", "ig_s5_complementaire", "ig_s5b_legender"]),
    ("ig_partie7", None, None, ["ig_r1_hypotheses", "ig_r2_experience", "ig_r3_g1", "ig_r4_g2", "ig_r5_semi", "ig_r6_rediger", "ig_r7_thymidine1", "ig_r8_thymidine2", "ig_r9_yeux", "ig_r10_polymerase", "ig_r11_deux_molecules", "ig_r11b_legender", "ig_r12_conservation"]),
    ("ig_partie8", None, None, ["ig_x1_restitution", "ig_x2_exercice"]),
    ("ig_bilan", None, None, ["ig_b1_bilan", "ig_b2_carte"]),
], [
    ("ig_s1", "Séance 1 — Où est l'information génétique ? Le noyau", [
        ("ig_s1_b1", "Une information transmise ; la cellule ; l’amibe coupée en deux", ["ig_o1_ressemblance", "ig_o2_rappel", "ig_l1_amibe"]),
        ("ig_s1_b2", "L'acétabulaire : une hypothèse, puis sa vérification", ["ig_l2_acetabulaire", "ig_l3_section", "ig_l4_greffe"]),
        ("ig_s1_b3", "Gurdon, et la définition de l'information génétique", ["ig_l5_gurdon", "ig_l6_definition"])]),
    ("ig_s2", "Séance 2 — Dans le noyau : chromatine, chromosomes, mitose", [
        ("ig_s2_b1", "Chromatine et chromosome : le même ADN", ["ig_n1_noyau", "ig_n2_condensation", "ig_n1b_feulgen"]),
        ("ig_s2_b2", "46 chromosomes, et la mitose en une idée", ["ig_p1_chromosomes", "ig_p2_mitose", "ig_p3_mitose_corps"]),
        ("ig_s2_b3", "Une ou deux chromatides ; le cycle cellulaire", ["ig_n3_chromatides", "ig_c1_cycle"])]),
    ("ig_s3", "Séance 3 — La quantité d'ADN au cours du cycle", [
        ("ig_s3_b1", "La courbe de la quantité d'ADN, et pourquoi doubler", ["ig_c3_courbe", "ig_c2_pourquoi", "ig_c4_aspect"]),
        ("ig_s3_b2", "Comme à l'examen : décrire la courbe, calculer les durées", ["ig_c5_decrire", "ig_c6_durees", "ig_c6b_phases"]),
        ("ig_s3_b3", "La mitose : définition, prophase, métaphase", ["ig_m1_mitose", "ig_m2_prophase", "ig_m3_metaphase"])]),
    ("ig_s4", "Séance 4 — La mitose, puis Griffith", [
        ("ig_s4_b1", "Anaphase, télophase, cellule végétale", ["ig_m4_anaphase", "ig_m4b_telophase", "ig_m5_vegetale"]),
        ("ig_s4_b2", "Reconnaître, dessiner et légender une phase", ["ig_m6_photo", "ig_m7_schema", "ig_m7b_legender"]),
        ("ig_s4_b3", "Griffith : le principe, puis deux expériences", ["ig_t1_griffith", "ig_t1b_exp1", "ig_t1c_exp2"])]),
    ("ig_s5", "Séance 5 — L'ADN porte l'information ; sa composition", [
        ("ig_s5_b1", "Griffith : les S tués, puis la souris 4", ["ig_t1d_exp3", "ig_t1e_exp4", "ig_t1f_bilan"]),
        ("ig_s5_b2", "Avery : l'ADN est le support de l'information", ["ig_t2_avery", "ig_t2b_avery_resultats", "ig_t3_support"]),
        ("ig_s5_b3", "Le nucléotide, Chargaff, deux brins antiparallèles", ["ig_s1_nucleotide", "ig_s2_chargaff", "ig_s3_antiparalleles"])]),
    ("ig_s6", "Séance 6 — La double hélice, et Meselson et Stahl", [
        ("ig_s6_b1", "La double hélice et le brin complémentaire", ["ig_s4_helice", "ig_s5_complementaire", "ig_s5b_legender"]),
        ("ig_s6_b2", "Meselson et Stahl : les hypothèses, la génération 1", ["ig_r1_hypotheses", "ig_r2_experience", "ig_r3_g1"]),
        ("ig_s6_b3", "Génération 2 : la réplication est semi-conservative", ["ig_r4_g2", "ig_r5_semi", "ig_r6_rediger"])]),
    ("ig_s7", "Séance 7 — Le mécanisme de la réplication, et l’examen", [
        ("ig_s7_b1", "Thymidine radioactive et yeux de réplication", ["ig_r7_thymidine1", "ig_r8_thymidine2", "ig_r9_yeux"]),
        ("ig_s7_b2", "L'ADN polymérase et la conservation de l'information", ["ig_r10_polymerase", "ig_r11_deux_molecules", "ig_r11b_legender", "ig_r12_conservation"]),
        ("ig_s7_b3", "Comme à l'examen, et le bilan du chapitre", ["ig_x1_restitution", "ig_x2_exercice", "ig_b1_bilan", "ig_b2_carte"])]),
], D)

m["note"] += (" — 18 novembre 2026 (skill logique-de-cours) : logique refaite, voir "
              "backend/data/curriculum/architecture/svt_ch3_notion_information_genetique.md. Cas décisifs posés en question "
              "(section et greffe de l'acétabulaire, Gurdon, Chargaff, Meselson génération 1 et 2, durée de la phase S) ; "
              "définition de l'information génétique après les trois expériences (ig_l6) ; chromatine avant chromosome, "
              "l'ADN n'est plus dit porteur de l'information avant Avery ; courbe avant « pourquoi doubler » ; durée du cycle "
              "demandée avant le calcul (ig_c6 / ig_c6b) ; anaphase et télophase séparées (ig_m4 / ig_m4b) ; sept séances.")
sortie = R / f"backend/data/courses/en_attente/{DECK}.json"
json.dump(m, open(sortie, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print("écrit", sortie, len(D), "diapositives")
