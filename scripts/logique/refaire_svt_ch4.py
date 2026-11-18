"""SVT ch4 — relation gène – protéine : la logique refaite (18 novembre 2026).
Lit le cours en ligne, écrit backend/data/courses/en_attente/svt_ch4_relation_gene_proteine.json.
Architecture et raisons : backend/data/curriculum/architecture/svt_ch4_relation_gene_proteine.md"""
import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from outils import *

R = Path(__file__).resolve().parents[2]
DECK = "svt_ch4_relation_gene_proteine"
m = charger(R / f"backend/data/courses/{DECK}.json")
D = diapos(m)

# ---------------------------------------------------------------- ouverture : la question, pas la réponse
o1 = D["rg_o1_caracteres"]
reecrire(o1,
    fr="Ton groupe sanguin, la forme de tes hématies : ce sont des caractères héréditaires : un caractère héréditaire est transmis de génération en génération. La forme que prend ce caractère chez toi, groupe A, B, AB ou O, c'est ton phénotype : le phénotype est l'ensemble des caractères observables d'un individu. Au chapitre précédent, nous avons vu que l'information génétique est dans le noyau, portée par l'ADN. Mais le caractère, on le voit dans tout le corps : dans le sang, dans les yeux. Alors la question du chapitre : comment l'information du noyau devient-elle un caractère ? Regarde cette image : nous ne l'expliquons pas maintenant. À la fin du chapitre, c'est toi qui sauras l'expliquer en entier.",
    mixed="ل groupe sanguin ديالك، والشكل ديال les hématies ديالك: هادو des caractères héréditaires. un caractère héréditaire، هو حاجة فيك كتجيك من الوالدين، وكتمشي من جيل ل جيل. نعاود نقرا: caractère héréditaire، caractère transmis de génération en génération. والشكل اللي كيبان بيه هاد le caractère عندك، كنسميوه le phénotype: مثلا le groupe A، ولا B، ولا A B، ولا O. نعاود نقرا: le phénotype، ensemble des caractères observables d'un individu. ف le chapitre اللي فات، شفنا بلي l'information génétique كاينة ف le noyau، ف l'A D N. ولكن le caractère كيبان ف الجسم كامل: ف الدم، ف العينين. إذن السؤال ديال هاد le chapitre: كيفاش l'information اللي ف le noyau، كتولي caractère؟ شوف هاد الصورة: دابا ما غاديش نشرحوها. ف اللخر ديال le chapitre، نتا اللي غادي تشرح هاد الصورة كاملة.",
    pointage=[{"mot": "شوف هاد الصورة:", "cible": "visuel"}])
o1["visual"]["caption"] = "Une image à expliquer à la fin du chapitre"
o1["visual"]["alt"] = "Illustration : un noyau avec de l'ADN, une molécule orange, une machine dans le cytoplasme, une chaîne de perles"

# ---------------------------------------------------------------- III. l'ARN : le problème d'abord, puis la molécule, puis les expériences
a2 = D["rg_a2_usine"]
reecrire(a2,
    fr="Regarde la cellule en coupe. Au centre, le noyau, bleuté, avec l'ADN : l'information. Autour, le cytoplasme, rosé, avec de petits grains : les ribosomes. L'ADN ne sort jamais du noyau. Et les protéines : où sont-elles fabriquées, dans le noyau ou dans le cytoplasme ? Et si c'est hors du noyau, comment l'ordre de l'ADN y arrive-t-il ? Pense à un livre important rangé à l'école : on ne le sort pas, on photocopie une page, et c'est la photocopie qui sort. La cellule fait-elle pareil ? Des expériences de marquage vont nous le dire.",
    mixed="شوف la cellule من الداخل. ف الوسط le noyau، اللون ديالو زرق، وفيه l'A D N: هي l'information. دايرين بيه le cytoplasme، اللون ديالو rose، فيه نقط صغار: les ribosomes. l'A D N عمرو ما كيخرج من le noyau. و les protéines، فين كيتكونو: ف le noyau، ولا ف le cytoplasme؟ ويلا كانو كيتكونو برا le noyau، إذن كيفاش كيوصل الأمر ديال l'A D N ل تما؟ تخيل واحد الكتاب مهم ف المدرسة: الكتاب كيبقى ف المدرسة، كنديرو photocopie ديال جزء منو، و la photocopie هي اللي كتخرج. واش الخلية كدير بحال هكا؟ des expériences de marquage غادي يقولو لينا.",
    pointage=a2["concentration"]["pointage"])
a2["screen_content"]["bullets"] = [
    "L'ADN est dans le noyau ; il ne le quitte jamais.",
    "Les protéines : fabriquées dans le noyau, ou dans le cytoplasme ?",
    "Si c'est dans le cytoplasme, il faut un messager : une copie qui sort du noyau ?",
    "Image : on ne sort pas le livre de l'école, on en photocopie une page."]
a2["screen_content"]["student_trace"] = "L'information génétique (ADN) est dans le noyau et ne le quitte jamais. Question : où sont fabriquées les protéines, et comment l'information y arrive-t-elle ?"
a2["concentration"]["cahier"] = a2["screen_content"]["student_trace"]

a1 = D["rg_a1_arn"]
t = a1["speech_text"]["mixed"]
ancien = "باش نمشيو من le noyau حتى ل le caractère، الخلية كتخدم ب molécule أخرى: l'A R N."
assert ancien in t
reecrire(a1,
    fr=a1["speech_text"]["fr"].replace(
        "Pour aller du noyau au caractère, la cellule utilise une autre molécule : l'ARN.",
        "Avant les expériences, une molécule à connaître : l'ARN, très proche de l'ADN."),
    mixed=t.replace(ancien, "قبل التجارب، خاصنا نعرفو واحد la molécule أخرى: l'A R N، قريبة بزاف من l'A D N.").replace("شوف السطر البرتقالي، l'A R N:", "شوف السطر ديال l'A R N، باللون orange:"))
for p in a1["concentration"]["pointage"]:
    if p["mot"] == "شوف السطر البرتقالي":
        p["mot"] = "شوف السطر ديال l'A R N"
assert "Avant les expériences" in a1["speech_text"]["fr"], a1["speech_text"]["fr"][:120]

# ---------------------------------------------------------------- VI. la traduction : le codon suivant posé en question
D["rg_r3_elongation"]["concentration"]["observation"] = observation(
    "le codon اللي من بعد هو C G C.",
    "Le codon suivant est CGC. Quel ARNt vient se placer en face ?",
    "le codon اللي من بعد هو C G C. أشمن A R N de transfert غادي يجي قدامو؟",
    [("L'anticodon de l'ARNt est complémentaire du codon.", "l'anticodon ديال l'A R N de transfert، complémentaire ديال le codon.", "codon_2"),
     ("En face de C, on met G ; en face de G, on met C.", "مقابل C كنحطو G، و مقابل G كنحطو C.", None)],
    ["L'ARNt dont l'anticodon est GCG", "L'ARNt dont l'anticodon est CGC", "L'ARNt dont l'anticodon est UAC"],
    0,
    [("Oui ! GCG est complémentaire de CGC : cet ARNt s'apparie, et il apporte son acide aminé.",
      "مزيان! G C G complémentaire ديال C G C. هاد l'A R N de transfert كيجي، وكيجيب معاه acide aminé ديالو."),
     ("CGC, c'est le codon lui-même. L'anticodon doit être complémentaire : en face de C, quoi ?",
      "C G C هو le codon براسو. l'anticodon خاصو يكون complémentaire: مقابل C، شنو كنحطو؟"),
     ("UAC, c'est l'anticodon de la méthionine, pour AUG. Le codon a changé : CGC.",
      "U A C هو l'anticodon ديال la méthionine، مقابل A U G. دابا le codon هو C G C.")],
    ("L'ARNt dont l'anticodon est GCG : il est complémentaire du codon CGC ; il apporte l'arginine.",
     "l'A R N de transfert اللي l'anticodon ديالو G C G، حيت complémentaire ديال C G C. وكيجيب l'arginine."),
    gestes=[{"repere": "codon_2"}])

# ---------------------------------------------------------------- VII. les mutations : l'effet sur la protéine posé en question
D["rg_m2_substitution"]["concentration"]["observation"] = observation(
    "C T G ولات C T A.",
    "Le codon CUG (leucine) devient CUA. Avec le tableau du code : quel acide aminé donne CUA ?",
    "le codon C U G، اللي كيعطي la leucine، ولا C U A. شوف le tableau: C U A شنو كيعطي؟",
    [("CUG et CUA commencent tous les deux par CU : même ligne, même colonne du tableau.",
      "C U G و C U A بجوج كيبداو ب C U: نفس السطر، و نفس العمود ف le tableau.", "codon_mute"),
     ("Dans la case CU, les quatre codons CUU, CUC, CUA, CUG donnent le même acide aminé.",
      "ف la case ديال C U، الربعة codons كيعطيو نفس acide aminé.", None)],
    ["La leucine, comme avant", "La valine", "Aucun : c'est un codon stop"],
    0,
    [("Oui ! CUA donne encore la leucine : la protéine ne change pas. Le code est redondant.",
      "مزيان! C U A مازال كيعطي la leucine. la protéine بقات كيف ما هي، حيت le code redondant."),
     ("La valine, c'est GUG ou GUA, avec G en première lettre. CUA commence par C : relis la case.",
      "la valine، هي G U G ولا G U A، كتبدا ب G. ولكن C U A كتبدا ب C. عاود شوف la case."),
     ("Les codons stop sont UAA, UAG et UGA. CUA n'en fait pas partie. Relis la case CU.",
      "les codons stop هما U A A، و U A G، و U G A. C U A ماشي منهم. عاود شوف la case ديال C U.")],
    ("CUA donne la leucine, comme CUG : même acide aminé, la protéine ne change pas. C'est une mutation silencieuse, grâce à la redondance du code.",
     "C U A كيعطي la leucine، بحال C U G. نفس acide aminé، la protéine بقات كيف ما هي. هادي mutation silencieuse، بسبب la redondance ديال le code."),
    gestes=[{"repere": "codon_mute"}])

D["rg_m3_non_sens"]["concentration"]["observation"] = observation(
    "ف le triplet quatre.",
    "Au triplet 4, TGG devient TAG : le codon UGG devient UAG. Que se passe-t-il à ce codon ?",
    "ف le triplet quatre، T G G ولات T A G. يعني le codon U G G ولا U A G. شنو كيوقع ف هاد le codon؟",
    [("Cherche UAG dans le tableau du code : que dit sa case ?", "قلب على U A G ف le tableau: شنو مكتوب ف la case ديالو؟", "codon_stop"),
     ("UAA, UAG, UGA : ces trois codons ne donnent aucun acide aminé.", "U A A، و U A G، و U G A: هادو ما كيعطيو حتى acide aminé.", None)],
    ["Le tryptophane est remplacé par un autre acide aminé", "UAG est un codon stop : la traduction s'arrête", "Rien : la protéine ne change pas"],
    1,
    [("Si UAG donnait un acide aminé, ce serait un faux-sens. Mais que dit la case de UAG dans le tableau ?",
      "يلا كان U A G كيعطي acide aminé، غادي تكون faux-sens. ولكن شنو مكتوب ف la case ديال U A G؟"),
     ("Oui ! UAG est un codon stop : la traduction s'arrête trop tôt, la protéine est raccourcie.",
      "مزيان! U A G codon stop. la traduction كتوقف بكري، و la protéine كتولي قصيرة."),
     ("Le codon a changé, et UAG n'est pas un codon comme les autres. Relis le tableau.",
      "le codon تبدل، و U A G ماشي codon بحال الآخرين. عاود شوف le tableau.")],
    ("UAG est un codon stop : aucun acide aminé ; la traduction s'arrête au triplet 4 et la protéine est raccourcie.",
     "U A G codon stop: حتى acide aminé. la traduction كتوقف ف le triplet quatre، و la protéine كتولي قصيرة."))

# ---------------------------------------------------------------- l'ordre : parties, séances, blocs
recouper(m, [
    ("rg_partie1", "I. Caractère, gène, allèle, mutation", 22, ["rg_o1_caracteres", "rg_d1_adn", "rg_g1_gene", "rg_g2_allele", "rg_g3_mutation", "rg_g3b_mutation"]),
    ("rg_partie2", None, 39, ["rg_d2_proteine", "rg_p1_organisme", "rg_p2_cellule", "rg_p3_proteine", "rg_p4_document", "rg_p4b_albinisme", "rg_p5_beadle_tatum"]),
    ("rg_partie3", None, None, ["rg_a2_usine", "rg_a1_arn", "rg_a3_uracile", "rg_a4_acides_amines", "rg_a5_in_vitro"]),
    ("rg_partie4", None, None, ["rg_t1_rappel", "rg_t2_definition", "rg_t2b_arbre_noel", "rg_t3_bases", "rg_t4_sens", "rg_t5_non_transcrit", "rg_t5b_legender", "rg_t6_bareme"]),
    ("rg_partie5", None, None, ["rg_c1_codon", "rg_c1b_nirenberg", "rg_c2_tableau", "rg_c3_initiation_stop", "rg_c4_traduire", "rg_c5_proprietes"]),
    ("rg_partie6", None, None, ["rg_r1_acteurs", "rg_r2_initiation", "rg_r3_elongation", "rg_r4_terminaison", "rg_r5_polysome", "rg_r6_legender"]),
    ("rg_partie7", None, None, ["rg_m1_comparer", "rg_m2_substitution", "rg_m2b_faux_sens", "rg_m3_non_sens", "rg_m4_decalage", "rg_m5_trois", "rg_m6_juger"]),
    ("rg_partie8", None, None, ["rg_s1_gpc", "rg_s2_schema", "rg_s3_construire", "rg_s4_trans_trad", "rg_s5_etapes"]),
    ("rg_partie9", None, None, ["rg_e1_restitution", "rg_e2_reperages", "rg_e3_lignes", "rg_e4_phrase", "rg_e5_national", "rg_e6_drepanocytose"]),
    ("rg_bilan", None, None, ["rg_b1_bilan", "rg_b2_carte"]),
], [
    ("rg_s1", "Séance 1 — Caractère, gène, allèle, mutation", [
        ("rg_s1_b1", "La question du chapitre ; l'ADN, rappel", ["rg_o1_caracteres", "rg_d1_adn"]),
        ("rg_s1_b2", "Le gène et l'allèle", ["rg_g1_gene", "rg_g2_allele"]),
        ("rg_s1_b3", "Une mutation crée un nouvel allèle", ["rg_g3_mutation", "rg_g3b_mutation"])]),
    ("rg_s2", "Séance 2 — La protéine et le caractère", [
        ("rg_s2_b1", "Une protéine ; la drépanocytose, de l'organisme à la cellule", ["rg_d2_proteine", "rg_p1_organisme", "rg_p2_cellule"]),
        ("rg_s2_b2", "La protéine en cause ; lire un document", ["rg_p3_proteine", "rg_p4_document"]),
        ("rg_s2_b3", "Albinisme, Beadle et Tatum : un gène, une enzyme", ["rg_p4b_albinisme", "rg_p5_beadle_tatum"])]),
    ("rg_s3", "Séance 3 — L'ARN messager, puis la transcription", [
        ("rg_s3_b1", "Le problème, l'ARN, l'uracile radioactif", ["rg_a2_usine", "rg_a1_arn", "rg_a3_uracile"]),
        ("rg_s3_b2", "Les protéines au cytoplasme : l'ARNm est nécessaire", ["rg_a4_acides_amines", "rg_a5_in_vitro"]),
        ("rg_s3_b3", "La transcription : définition et arbre de Noël", ["rg_t1_rappel", "rg_t2_definition", "rg_t2b_arbre_noel"])]),
    ("rg_s4", "Séance 4 — La transcription comme le barème, puis le code", [
        ("rg_s4_b1", "Base après base, le sens, le brin non transcrit", ["rg_t3_bases", "rg_t4_sens", "rg_t5_non_transcrit"]),
        ("rg_s4_b2", "Légender, puis écrire l'ARNm comme le barème", ["rg_t5b_legender", "rg_t6_bareme"]),
        ("rg_s4_b3", "Le codon, Nirenberg, le tableau", ["rg_c1_codon", "rg_c1b_nirenberg", "rg_c2_tableau"])]),
    ("rg_s5", "Séance 5 — Le code, puis la traduction", [
        ("rg_s5_b1", "Initiation, stop, traduire, propriétés du code", ["rg_c3_initiation_stop", "rg_c4_traduire", "rg_c5_proprietes"]),
        ("rg_s5_b2", "Les acteurs, l'initiation, l'élongation", ["rg_r1_acteurs", "rg_r2_initiation", "rg_r3_elongation"]),
        ("rg_s5_b3", "Terminaison, polysome, légender", ["rg_r4_terminaison", "rg_r5_polysome", "rg_r6_legender"])]),
    ("rg_s6", "Séance 6 — Les mutations, et le schéma bilan", [
        ("rg_s6_b1", "Comparer les allèles ; silencieuse, faux-sens, non-sens", ["rg_m1_comparer", "rg_m2_substitution", "rg_m2b_faux_sens", "rg_m3_non_sens"]),
        ("rg_s6_b2", "Délétion, insertion : le cadre de lecture", ["rg_m4_decalage", "rg_m5_trois", "rg_m6_juger"]),
        ("rg_s6_b3", "Du gène au caractère : le schéma", ["rg_s1_gpc", "rg_s2_schema", "rg_s3_construire"])]),
    ("rg_s7", "Séance 7 — Rédiger comme le barème, l'exercice national et le bilan", [
        ("rg_s7_b1", "Transcription ou traduction ? et la restitution", ["rg_s4_trans_trad", "rg_s5_etapes", "rg_e1_restitution"]),
        ("rg_s7_b2", "Les repérages, les lignes alignées, la phrase", ["rg_e2_reperages", "rg_e3_lignes", "rg_e4_phrase"]),
        ("rg_s7_b3", "Un exercice national complet, et le bilan", ["rg_e5_national", "rg_e6_drepanocytose", "rg_b1_bilan", "rg_b2_carte"])]),
], D)

m["note"] += (" — 18 novembre 2026 (skill logique-de-cours) : logique refaite, voir "
              "backend/data/curriculum/architecture/svt_ch4_relation_gene_proteine.md. L'ouverture pose la question sans "
              "donner le mécanisme ; la protéine enseignée au début de la partie II, où elle sert ; le problème (ADN au "
              "noyau, protéines où ?) avant la molécule d'ARN et avant les marquages, sans affirmer le lieu de synthèse ; "
              "questions d'observation sur le codon suivant de l'élongation, la mutation silencieuse et la non-sens ; "
              "sept séances.")
sortie = R / f"backend/data/courses/en_attente/{DECK}.json"
json.dump(m, open(sortie, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print("écrit", sortie, len(D), "diapositives, ", m["estimated_minutes"], "min")
