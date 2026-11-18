"""2ᵉ passe de la logique du cours SVT ch4 « Expression de l'information génétique » (18 novembre 2026).

Lit la version EN ATTENTE (1re passe faite par refaire_svt_ch4.py) et y applique la 2ᵉ passe :
  1. les cinq documents encore lus en tableau naissent d'une animation (documents.html : albinisme, beadle, in_vitro,
     arbre_noel, nirenberg) — texte et voix des diapositives inchangés, seuls `visual` et `pointage` changent ;
  2. les observations de rg_m2 et rg_m3 taisent la conclusion de mutation.html jusqu'à la réponse ({conclusions: false}) ;
  3. le sujet 2024 N joué une consigne à la fois (examen.html?vue=amelogenine_pas) : rg_e5a_document (nouvelle) puis
     rg_e5_national (réécrite ; sa question et son exercice gardent leurs voix) ;
  4. deux cas types du national qui manquaient : hypothèse à vérifier par les séquences (2020 N, moustiques résistants :
     rg_e7_moustiques, rg_e7b_hypothese, rg_e7c_verifier) et document sur le ribosome (2022 N, Blackfan-Diamond :
     rg_e8_ribosomes, rg_e8b_hemoglobine), sur national.html ;
  5. séances (une séance 8), compétences, durée.
Ne touche jamais au cours en ligne. Refuse de tourner deux fois (rg_e5a_document déjà présent).
Ensuite : python3 -X utf8 scripts/logique/lister_voix.py svt_ch4_relation_gene_proteine
"""
import json, sys
from pathlib import Path

R = Path(__file__).resolve().parents[2]
P = R / "backend/data/courses/en_attente/svt_ch4_relation_gene_proteine.json"
m = json.load(open(P, encoding="utf-8"))
SL = {s["id"]: s for a in m["activities"] for s in a["slides"]}
if "rg_e5a_document" in SL:
    sys.exit("2ᵉ passe déjà appliquée")
SIM = "/media/simulations/svt/relation_gene_proteine-tableau/"


def pu(mot, moment):
    return {"mot": mot, "commande": "play_until", "parametres": {"moment": moment}}


def rp(mot, repere):
    return {"mot": mot, "repere": repere}


def verifier_mots(s):
    t = s["speech_text"]["mixed"]
    pos = 0
    for p in s["concentration"].get("pointage", []):
        assert p["mot"] in t, (s["id"], p["mot"])
    o = s["concentration"].get("observation")
    if o and o.get("apres_mot"):
        assert o["apres_mot"] in t, (s["id"], o["apres_mot"])
    for q in [s.get("question")] + list(s.get("exercises") or []):
        d = (q or {}).get("demonstration")
        if d:
            for l in d["lignes"]:
                assert l["mot"] in d["parole"], (s["id"], l["mot"])


# ── 1. Les documents naissent d'une animation (texte et voix gardés) ──────────────────────────────────────────────
DOCS = {
    "rg_p4b_albinisme": ("albinisme", "Albinisme : la tyrosine devient mélanine dans la cellule saine, pas chez l'albinos ; puis le tableau",
                         "Deux cellules de la peau : la tyrosinase fonctionnelle produit la mélanine, la tyrosinase non fonctionnelle non ; peau et cheveux colorés ou très clairs ; le tableau ligne par ligne",
                         [pu("مثال ثاني: l'albinisme.", "cellules"), rp("l'enzyme tyrosinase", "enzyme_saine"),
                          pu("هنا la tyrosine كتولي mélanine", "reaction"), rp("هنا la tyrosine كتولي mélanine", "melanine"),
                          rp("شوف le tableau.", "tableau"), pu("السطر اللول، l'enzyme:", "ligne_enzyme"),
                          rp("la tyrosinase non fonctionnelle", "enzyme_albinos"), pu("السطر الثاني، le pigment:", "ligne_pigment"),
                          pu("السطر الثالث، le phénotype:", "ligne_phenotype"), rp("وبيض بزاف", "peau_albinos"),
                          pu("إذن بحال le récepteur LDL", "tableau")]),
    "rg_p5_beadle_tatum": ("beadle", "Beadle et Tatum : Neurospora pousse ou non selon le milieu",
                           "La chaîne précurseur → ornithine → citrulline → arginine, puis seize boîtes de culture : le champignon pousse (+) ou non (−) ; la case du mutant 3 reste à trouver",
                           [pu("précurseur، ornithine، citrulline، arginine", "chaine"), rp("E un، E deux، E trois", "chaine"),
                            pu("le milieu minimum، يعني", "milieux"), rp("شوف le tableau.", "grille"),
                            pu("السطر اللول، la souche", "sauvage"), pu("السطر الثاني، le mutant", "mutant1"),
                            pu("إذن الخدمة اللي ناقصاه", "e1"), pu("السطر الثالث، le mutant", "mutant2"),
                            pu("إذن l'enzyme E deux", "e2"), pu("السطر الرابع، le mutant", "mutant3"), rp("سؤال:", "ligne_mutant3")]),
    "rg_a5_in_vitro": ("in_vitro", "Synthèse in vitro : les deux courbes naissent des injections d'ARNm",
                       "Le tube (extrait de cellules sans ADN ni ARNm, acides aminés radioactifs), puis deux injections d'ARNm : l'incorporation monte, l'ARNm baisse",
                       [pu("ف الأنبوب حطو", "tube"), rp("ولكن ما فيهش l'A D N", "tube"), rp("شوف le tableau.", "graphe"),
                        pu("السطر اللول: قبل", "avant"), pu("السطر الثاني: من بعد", "injection1"),
                        rp("l'A R N messager كينقص", "graphe"), pu("السطر الثالث: injection", "injection2")]),
    "rg_t2b_arbre_noel": ("arbre_noel", "L'arbre de Noël : l'électronographie, puis chaque objet nommé",
                          "Une électronographie qui se développe : le tronc (ADN), les branches (ARN), les points (ARN polymérases) ; branches courtes d'un côté, longues de l'autre",
                          [pu("هادي صورة ديال la transcription", "image"), rp("شوف le tableau.", "tableau"),
                           pu("السطر اللول: واحد", "adn"), rp("بحال الجذع", "adn"), pu("السطر الثاني: خيوط", "arn"),
                           pu("السطر الثالث: ف الراس", "polymerase"), rp("هي l'A R N polymérase", "polymerase"),
                           pu("السطر الرابع: الغصون", "longueurs"), rp("الغصون قصار", "courtes")]),
    "rg_c1b_nirenberg": ("nirenberg", "Nirenberg et Matthaei : le ribosome lit l'ARNm de synthèse par trois",
                         "Trois ARNm de synthèse : poly-U donne Phe – Phe…, UG répété donne Cys – Val…, poly-C donne Pro – Pro… ; le codon de la proline reste à trouver",
                         [rp("شوف le tableau.", "rangee_u"), pu("السطر اللول: A R N", "poly_u"), rp("هادا أول codon", "chaine_u"),
                          pu("السطر الثاني: U G U", "ug"), rp("la cystéine و la valine", "chaine_ug"),
                          pu("يلا كان le codon ب جوج حروف", "par_deux"), pu("السطر الثالث: A R N", "poly_c"),
                          rp("كيعطي chaîne فيها غير la proline", "chaine_c")]),
}
for sid, (vue, cap, alt, pt) in DOCS.items():
    s = SL[sid]
    s["visual"] = {"kind": "simulation", "url": f"{SIM}documents.html?vue={vue}", "caption": cap, "alt": alt}
    s["concentration"]["pointage"] = pt
    verifier_mots(s)

# ── 2. Rien de décisif avant la réponse : mutation.html se tait pendant les observations ─────────────────────────
for sid in ("rg_m2_substitution", "rg_m3_non_sens"):
    o = SL[sid]["concentration"]["observation"]
    o["sim_avant"] = {"conclusions": False}
    o["sim_apres"] = {"conclusions": True}


def reac(parole, ecrit):
    return {"parole": parole, "ecrit": ecrit}


def slide(sid, titre, lead, bullets, trace, url, cap, alt, fr, mixed, pointage, question, reponses, competences, cahier, exercises=None, stype="exercise"):
    s = {"id": sid, "stable_id": sid, "slide_type": stype, "title": titre,
         "screen_content": {"lead": lead, "bullets": bullets, "student_trace": trace},
         "visual": {"kind": "simulation", "url": url, "caption": cap, "alt": alt},
         "speech_text": {"fr": fr, "mixed": mixed},
         "question": question,
         "concentration": {"pointage": pointage, "cahier": cahier, "reponses": reponses},
         "competence_ids": competences}
    if exercises:
        s["exercises"] = exercises
    verifier_mots(s)
    return s


# ── 3. Le sujet 2024 N, une consigne à la fois ──────────────────────────────────────────────────────────────────
A24 = f"{SIM}examen.html?vue=amelogenine_pas"
e5a = slide(
    "rg_e5a_document", "Sujet 2024 N : le document, puis la consigne 1",
    "L'amélogénèse imparfaite : on lit le document, puis une seule consigne — la relation protéine – caractère.",
    ["Personne saine : amélogénine normale → minéralisation normale → émail normal.",
     "Personne malade : amélogénine anormale → minéralisation faible → émail atteint.",
     "Consigne 1 : montrez la relation protéine – caractère (deux lignes parallèles, puis « d'où la relation »)."],
    "Relation protéine – caractère (2024 N) : amélogénine normale → minéralisation normale → émail normal ; amélogénine anormale → minéralisation faible → émail atteint ; d'où la relation protéine – caractère.",
    A24, "Sujet 2024 N : le document et la consigne 1", "Le document 1 redessiné (améloblastes, amélogénine, dents), puis la consigne 1 seule",
    "Un sujet entier du national deux mille vingt-quatre : l'amélogénèse imparfaite, une maladie de l'émail des dents. On le fait question par question. D'abord le document. En haut, la personne saine : les améloblastes sécrètent une protéine, l'amélogénine normale ; la minéralisation est normale, l'émail est normal. En bas, la personne malade : l'amélogénine est anormale, la minéralisation faible, l'émail atteint. Question un : montrez la relation protéine, caractère. Avant de répondre : qu'est-ce qui change dans la protéine, et qu'est-ce qui change dans le caractère ?",
    "sujet كامل ديال le national، deux mille vingt-quatre: l'amélogénèse imparfaite، مرض ف l'émail ديال الأسنان. غادي نديروه سؤال ب سؤال. اللول، le document. الفوق: la personne saine. les améloblastes كيخرجو واحد la protéine: l'amélogénine normale. la minéralisation normale، و l'émail normal. التحت: la personne malade. l'amélogénine anormale، la minéralisation faible، و l'émail atteint. السؤال اللول: montrez la relation protéine caractère. قبل ما تجاوب، فكر: شنو اللي تبدل ف la protéine، و شنو اللي تبدل ف le caractère؟",
    [pu("اللول، le document.", "document"), rp("الفوق: la personne saine.", "dent_saine"),
     rp("التحت: la personne malade.", "dent_atteinte"), pu("السؤال اللول:", "q1"), rp("montrez la relation protéine caractère", "consigne_q1")],
    {"type": "qcm", "prompt": "Q1 – Quelle réponse montre la relation protéine – caractère comme le barème ?",
     "options": ["La personne malade a un émail atteint.",
                 "Saine : amélogénine normale → minéralisation normale → émail normal ; malade : amélogénine anormale → minéralisation faible → émail atteint ; d'où la relation protéine – caractère.",
                 "L'émail atteint rend l'amélogénine anormale."],
     "timeout_seconds": 45, "correct": 1,
     "enonce_dit": "شوف هاد السؤال: شمن جواب كيبين la relation protéine caractère، بحال le barème؟",
     "demonstration": {
         "parole": "كنكتبو سطر لكل personne. السطر ديال la personne saine: amélogénine normale، minéralisation normale، émail normal. السطر ديال la personne malade: amélogénine anormale، minéralisation faible، émail atteint. و ف اللخر: d'où la relation protéine caractère.",
         "lignes": [{"texte": "Personne saine : amélogénine normale → minéralisation normale de l'émail → émail normal", "mot": "السطر ديال la personne saine"},
                    {"texte": "Personne malade : amélogénine anormale → minéralisation faible → émail atteint (amélogénèse imparfaite)", "mot": "السطر ديال la personne malade"},
                    {"texte": "d'où la relation protéine – caractère", "mot": "و ف اللخر"}]}},
    {"q": {
        "1": {"juste": reac("مزيان، جواب صحيح. سطر لكل personne: la protéine، من بعد la minéralisation، من بعد le caractère. و ف اللخر: d'où la relation protéine caractère.",
                            "Correct : deux lignes parallèles, protéine → minéralisation → caractère, puis « d'où la relation protéine – caractère ».")},
        "0": {"1": reac("صحيح، l'émail atteint. ولكن هادا غير le caractère. le barème كيطلب la protéine حتى هي. شنو تبدل ف l'amélogénine؟ عاود جرب.",
                        "C'est vrai, mais tu ne donnes que le caractère. Le barème veut aussi la protéine : qu'est-ce qui change dans l'amélogénine ? Réessaie."),
              "2": reac("لا، ناقص. خاص la protéine و le caractère، عند جوج: amélogénine normale، minéralisation normale، émail normal. amélogénine anormale، minéralisation faible، émail atteint. الجواب الصحيح هو B.",
                        "Incomplet : il faut la protéine et le caractère, chez les deux personnes. Saine : amélogénine normale → minéralisation normale → émail normal ; malade : amélogénine anormale → minéralisation faible → émail atteint. Bonne réponse : B.")},
        "2": {"1": reac("الكلمات صحيحة، ولكن الترتيب مقلوب. شكون اللي كيجي اللول: la protéine ولا l'émail؟ عاود جرب.",
                        "Les mots sont justes, mais l'ordre est inversé : qu'est-ce qui vient d'abord, la protéine ou l'émail ? Réessaie."),
              "2": reac("لا، مقلوب. la protéine هي اللي كتجي اللول: l'amélogénine anormale كتعطي minéralisation faible، و هي اللي كتعطي l'émail atteint. الجواب الصحيح هو B.",
                        "Non, c'est inversé : la protéine vient d'abord. L'amélogénine anormale donne une minéralisation faible, qui donne l'émail atteint. Bonne réponse : B.")}}},
    ["C2", "C8"],
    "Relation protéine – caractère (2024 N) : amélogénine normale → minéralisation normale → émail normal ; amélogénine anormale → minéralisation faible → émail atteint ; d'où la relation protéine – caractère.")

e5 = SL["rg_e5_national"]
e5["title"] = "Sujet 2024 N : les séquences, puis l'origine génétique"
e5["slide_type"] = "exercise"
e5["screen_content"] = {
    "lead": "Consigne 2 : l'ARNm et les acides aminés du triplet qui change ; consigne 3 : l'origine génétique.",
    "bullets": ["Brin non transcrit (triplets 1 à 5) : normal AAT CAT CCC CGT GCT ; muté AAT CAT CTC CGT GCT.",
                "Brin non transcrit → l'ARNm a la même séquence, U à la place de T : CCC (Pro) ; CUC (Leu).",
                "Origine génétique : substitution du 2e nucléotide C par T au triplet 3 du brin non transcrit du gène AMELX → CCC devient CUC → Pro remplacé par Leu → amélogénine anormale → minéralisation faible → amélogénèse imparfaite."],
    "student_trace": "2024 N : triplet 3, CCC → CTC (brin non transcrit) → codon CCC devient CUC → Pro remplacé par Leu → amélogénine anormale → minéralisation faible → amélogénèse imparfaite."}
e5["visual"] = {"kind": "simulation", "url": A24, "caption": "Sujet 2024 N : les consignes 2 et 3", "alt": "La réponse 1 écrite, puis les deux brins non transcrits ; le triplet 3 change"}
e5["speech_text"] = {
    "fr": "Retour au sujet. La réponse à la question un s'écrit ainsi : personne saine, amélogénine normale, minéralisation normale, émail normal ; personne malade, amélogénine anormale, minéralisation faible, émail atteint ; d'où la relation protéine, caractère. Question deux : les séquences. Le document donne le brin non transcrit, triplets un à cinq. Allèle normal : A A T, C A T, C C C, C G T, G C T. Allèle muté : la même chose, sauf le triplet trois : C T C. Écris l'ARN messager et l'acide aminé du triplet trois. Rappelle-toi : brin non transcrit, fait-on la complémentarité ?",
    "mixed": "نرجعو ل le sujet. الجواب ديال السؤال اللول كيتكتب هكا: personne saine، amélogénine normale، minéralisation normale، émail normal. personne malade، amélogénine anormale، minéralisation faible، émail atteint. d'où la relation protéine caractère. السؤال الثاني: les séquences. le document كيعطينا le brin non transcrit، triplets un حتى ل cinq. allèle normal: A A T، C A T، C C C، C G T، G C T. allèle muté: نفس الشي، غير le triplet trois: C T C. كتب l'A R N messager و l'acide aminé ديال le triplet trois. تفكر: brin non transcrit، واش كنديرو la complémentarité؟"}
e5.pop("audio", None)
e5["concentration"]["pointage"] = [
    {"mot": "نرجعو ل le sujet.", "commande": "set_time", "parametres": {"time_s": 5.4}},
    pu("الجواب ديال السؤال اللول", "q1_reponse"), rp("personne saine، amélogénine normale", "relation"),
    pu("السؤال الثاني: les séquences.", "q2"), rp("allèle normal: A A T", "brins"), rp("غير le triplet trois", "triplet3")]
e5["concentration"]["cahier"] = "2024 N : triplet 3, CCC → CTC (brin non transcrit) → codon CCC devient CUC → Pro remplacé par Leu → amélogénine anormale → minéralisation faible → amélogénèse imparfaite."
e5["competence_ids"] = ["C5", "C8"]
verifier_mots(e5)

# ── 4a. 2020 N : moustiques résistants (hypothèse à vérifier) ───────────────────────────────────────────────────
MO = f"{SIM}national.html?vue=moustiques"
e7 = slide(
    "rg_e7_moustiques", "Sujet 2020 N : des moustiques résistants — la relation",
    "L'acétylcholinestérase (AChE), le carbamate, puis l'activité de l'enzyme et la mortalité des souches S et R.",
    ["Document 1 : l'AChE hydrolyse l'acétylcholine ; le carbamate occupe son site actif et la bloque.",
     "Document 2 : activité de l'AChE pour 0, 10⁻², 1 mg/L : S 97, 8, 0 % ; R 32, 32, 28 %.",
     "Mortalité : S 100 % dès 1 mg/L ; R seulement à partir de 2·10² mg/L, 100 % vers 10³ mg/L.",
     "Consigne : montrez la relation entre la mortalité et l'activité de l'AChE."],
    "2020 N, relation : chez S, l'activité de l'AChE baisse (97 → 0 %) quand la concentration en carbamate augmente, et la mortalité atteint 100 % à 1 mg/L ; chez R, l'activité reste presque stable (32 → 28 %) et la mortalité ne commence que vers 2·10² mg/L : la mort suit l'arrêt de l'AChE.",
    MO, "Sujet 2020 N : documents 1 et 2", "L'AChE et le carbamate ; l'activité de l'AChE des souches S et R ; les courbes de mortalité",
    "Un autre sujet, le national deux mille vingt : des moustiques, Culex, devenus résistants à un insecticide, le carbamate. D'abord le document un. L'enzyme acétylcholinestérase, A C h E, coupe l'acétylcholine dans les synapses : c'est nécessaire au bon travail du système nerveux. Le carbamate vient se placer dans son site actif, et l'enzyme ne travaille plus. Maintenant le document deux. L'activité de l'enzyme chez la souche S : quatre-vingt-dix-sept, puis huit, puis zéro, quand la concentration augmente. Chez la souche R : trente-deux, trente-deux, vingt-huit : presque pas de changement. Et la mortalité : la souche S meurt toute à un milligramme par litre. La souche R ne commence à mourir que vers cent milligrammes par litre, et meurt toute près de mille. La question : montrez la relation entre la mortalité et l'activité de l'enzyme.",
    "sujet آخر، le national ديال deux mille vingt: des moustiques، Culex، ولاو résistants ل واحد insecticide: le carbamate. اللول، le document un. l'enzyme acétylcholinestérase، A C h E، كتقطع l'acétylcholine ف les synapses. هادشي ضروري باش le système nerveux يخدم مزيان. le carbamate كيدخل ف le site actif ديالها، و l'enzyme كتوقف. دابا le document deux. l'activité ديال l'enzyme عند la souche S: quatre-vingt-dix-sept، من بعد huit، من بعد zéro، ملي la concentration كتزاد. عند la souche R: trente-deux، trente-deux، vingt-huit: تقريبا ثابتة. و la mortalité: عند la souche S، كتوصل cent pour cent ف un milligramme par litre. عند la souche R، ما كتبدا غير قريب من cent milligrammes par litre، و كتوصل cent pour cent قريب من mille. السؤال: montrez la relation entre la mortalité et l'activité de l'enzyme.",
    [pu("اللول، le document un.", "enzyme"), rp("كتقطع l'acétylcholine", "enzyme"), pu("le carbamate كيدخل", "carbamate"),
     rp("le site actif ديالها", "site_actif"), pu("دابا le document deux.", "activite"), rp("عند la souche S: quatre-vingt-dix-sept", "activite"),
     pu("و la mortalité:", "mortalite_s"), rp("عند la souche S، كتوصل", "courbe_s"), pu("عند la souche R، ما كتبدا", "mortalite_r"),
     rp("قريب من mille", "courbe_r")],
    {"type": "qcm", "prompt": "Quelle phrase montre la relation entre la mortalité et l'activité de l'AChE ?",
     "options": ["Chez S, quand la concentration augmente, l'activité de l'AChE diminue (97 → 0 %) et la mortalité augmente (100 % à 1 mg/L) ; chez R, l'activité reste presque stable (32 → 28 %) et la mortalité n'apparaît qu'à de fortes concentrations (vers 10² mg/L).",
                 "La souche R meurt plus vite que la souche S.",
                 "Chez S, l'activité de l'AChE augmente avec la concentration en insecticide."],
     "timeout_seconds": 50, "correct": 0,
     "enonce_dit": "شوف هاد السؤال: شمن جملة كتبين la relation بين la mortalité و l'activité ديال l'enzyme؟",
     "demonstration": {
         "parole": "عند la souche S: ملي la concentration كتزاد، l'activité كتنقص، من quatre-vingt-dix-sept ل zéro. و la mortalité كتطلع، حتى ل cent pour cent ف un milligramme par litre. عند la souche R: l'activité تقريبا ثابتة، من trente-deux ل vingt-huit. و la mortalité ما كتبدا غير من cent milligrammes par litre. إذن la mort كتجي ملي l'enzyme كتوقف.",
         "lignes": [{"texte": "Souche S : concentration ↑ → activité de l'AChE ↓ (97 → 0 %) → mortalité ↑ (100 % à 1 mg/L)", "mot": "عند la souche S:"},
                    {"texte": "Souche R : activité presque stable (32 → 28 %) → mortalité seulement à partir de 10² mg/L environ", "mot": "عند la souche R:"},
                    {"texte": "La mortalité suit l'arrêt de l'AChE par le carbamate", "mot": "إذن la mort"}]}},
    {"q": {
        "0": {"juste": reac("مزيان، جواب صحيح. عند S، l'activité كتنقص و la mortalité كتطلع. عند R، l'activité تقريبا ثابتة، و la mortalité ما كتبدا غير ف concentrations كبار.",
                            "Correct : chez S, l'activité baisse et la mortalité monte ; chez R, l'activité reste presque stable et la mortalité n'apparaît qu'à de fortes concentrations.")},
        "1": {"1": reac("شوف مزيان la courbe ديال la mortalité: شمن souche اللي كتوصل cent pour cent ف un milligramme par litre؟ عاود جرب.",
                        "Regarde la courbe de mortalité : quelle souche meurt toute à 1 mg/L ? Réessaie."),
              "2": reac("لا، العكس: la souche S هي اللي كتوصل cent pour cent ف un milligramme par litre. la souche R خاصها تقريبا mille. الجواب الصحيح هو A.",
                        "Non, c'est l'inverse : la souche S meurt toute à 1 mg/L ; la souche R a besoin d'environ 10³ mg/L. Bonne réponse : A.")},
        "2": {"1": reac("قرا الأرقام ديال S مرة أخرى: quatre-vingt-dix-sept، huit، zéro. واش كتطلع ولا كتنقص؟ عاود جرب.",
                        "Relis les valeurs de S : 97, 8, 0. Augmentent-elles ou diminuent-elles ? Réessaie."),
              "2": reac("لا، l'activité عند S كتنقص: quatre-vingt-dix-sept، huit، zéro. و la mortalité كتطلع. الجواب الصحيح هو A.",
                        "Non : chez S, l'activité diminue (97, 8, 0 %) pendant que la mortalité augmente. Bonne réponse : A.")}}},
    ["C2", "C8"],
    "2020 N, relation : chez S, l'activité de l'AChE baisse (97 → 0 %) et la mortalité atteint 100 % à 1 mg/L ; chez R, l'activité reste presque stable (32 → 28 %) et la mortalité ne commence que vers 2·10² mg/L.")

e7b = slide(
    "rg_e7b_hypothese", "Sujet 2020 N : proposer une hypothèse",
    "Pourquoi la souche R résiste-t-elle ? Une hypothèse, au conditionnel, qui s'appuie sur les documents.",
    ["Chez S, le carbamate bloque le site actif de l'AChE.",
     "Chez R, l'AChE reste active malgré le carbamate.",
     "Une protéine est déterminée par un gène : une mutation peut la modifier.",
     "Consigne : proposez une hypothèse pour expliquer la résistance des souches R."],
    "Hypothèse (au conditionnel) : la résistance de R serait due à une mutation du gène de l'AChE qui modifie son site actif : le carbamate ne s'y fixerait plus.",
    MO, "Sujet 2020 N : l'hypothèse", "Les documents 1 et 2 au tableau : le site actif, l'activité de l'AChE",
    "Deuxième partie de la question : proposez une hypothèse. Pourquoi la souche R ne meurt-elle pas ? Regarde l'enzyme : chez S, le carbamate entre dans le site actif et l'arrête. Chez R, l'enzyme reste active. L'enzyme de R pourrait-elle être différente ? Et une protéine, qu'est-ce qui décide de sa structure ? Le gène. L'hypothèse s'écrit au conditionnel : « serait due à ». Réfléchis, puis choisis.",
    "دابا الجزء الثاني ديال السؤال: proposez une hypothèse. علاش la souche R مقاومة ل le carbamate؟ شوف l'enzyme: عند S، le carbamate كيدخل ف le site actif، و l'enzyme كتوقف. عند R، l'enzyme كتبقى خدامة. واش يمكن l'enzyme ديال R تكون مختلفة؟ و la protéine، شكون اللي كيحدد la structure ديالها؟ le gène. l'hypothèse، كنكتبو ب le conditionnel: serait due à. فكر، ومن بعد اختار.",
    [{"mot": "دابا الجزء الثاني", "commande": "set_time", "parametres": {"time_s": 14.4}},
     rp("عند S، le carbamate", "site_actif"), rp("عند R، l'enzyme كتبقى خدامة", "activite"), rp("le conditionnel", "courbe_r")],
    {"type": "qcm", "prompt": "Quelle hypothèse explique la résistance des souches R ?",
     "options": ["La souche R produirait plus d'acétylcholinestérase que la souche S.",
                 "La résistance serait due à une mutation du gène de l'AChE qui modifie son site actif : le carbamate ne s'y fixerait plus.",
                 "Le carbamate détruirait l'acétylcholine chez R."],
     "timeout_seconds": 45, "correct": 1,
     "enonce_dit": "شوف هاد السؤال: شمن hypothèse كتبين علاش la souche R مقاومة؟",
     "demonstration": {
         "parole": "عند R، l'enzyme كتبقى خدامة مع le carbamate. إذن يمكن le site actif ديالها تبدل. و le gène هو اللي كيحدد la protéine. كنكتبو ب le conditionnel: la résistance serait due à une mutation du gène de l'enzyme، qui modifie son site actif.",
         "lignes": [{"texte": "Chez R, le carbamate n'arrête pas l'AChE → son site actif serait différent", "mot": "عند R، l'enzyme كتبقى"},
                    {"texte": "la structure d'une protéine est déterminée par un gène", "mot": "و le gène هو اللي"},
                    {"texte": "Hypothèse : la résistance serait due à une mutation du gène de l'AChE qui modifie son site actif (le carbamate ne s'y fixerait plus)", "mot": "كنكتبو ب le conditionnel"}]}},
    {"q": {
        "1": {"juste": reac("مزيان، hypothèse صحيحة و مكتوبة ب le conditionnel. mutation ف le gène، le site actif تبدل، و le carbamate ما بقاش كيدخل.",
                            "Correct, et bien au conditionnel : une mutation du gène modifierait le site actif ; le carbamate ne s'y fixerait plus.")},
        "0": {"1": reac("قارن l'activité ديال R ب S بلا insecticide: trente-deux و quatre-vingt-dix-sept. واش R عندها كثر ديال l'enzyme؟ عاود جرب.",
                        "Compare l'activité de R et de S sans insecticide : 32 et 97 %. R a-t-elle plus d'enzyme ? Réessaie."),
              "2": reac("لا، le document كيبين العكس: l'activité عند R غير trente-deux، أقل من S. الجواب الصحيح هو B: mutation ف le gène كتبدل le site actif.",
                        "Non, le document montre l'inverse : l'activité de R (32 %) est plus faible que celle de S (97 %). Bonne réponse : B, une mutation du gène modifie le site actif.")},
        "2": {"1": reac("le carbamate كيخدم على l'enzyme، ماشي على l'acétylcholine. شوف le document un. عاود جرب.",
                        "Le carbamate agit sur l'enzyme, pas sur l'acétylcholine : relis le document 1. Réessaie."),
              "2": reac("لا، le carbamate كيدخل ف le site actif ديال l'enzyme. إذن l'hypothèse على l'enzyme: mutation ف le gène ديالها. الجواب الصحيح هو B.",
                        "Non : le carbamate se fixe sur le site actif de l'enzyme. L'hypothèse porte donc sur l'enzyme et son gène. Bonne réponse : B.")}}},
    ["C8"],
    "Hypothèse (au conditionnel) : la résistance de R serait due à une mutation du gène de l'AChE qui modifie son site actif : le carbamate ne s'y fixerait plus.")

SQ = f"{SIM}national.html?vue=moustiques_seq"
e7c = slide(
    "rg_e7c_verifier", "Sujet 2020 N : vérifier l'hypothèse par les séquences",
    "Les allèles Ace-S et Ace-R, triplets 243 à 251 : une seule différence. L'ARNm et l'acide aminé, puis la vérification.",
    ["Brin non transcrit : Ace-S … GGT GGC TTC … ; Ace-R … GGT AGC TTC … (triplet 247).",
     "ARNm : même séquence que le brin non transcrit, U à la place de T.",
     "Vérifier : mutation → codon → acide aminé → enzyme modifiée → caractère ; « l'hypothèse est vérifiée »."],
    "Vérifier (2020 N) : triplet 247, GGC (Gly) chez S, AGC (Ser) chez R : substitution G → A → Gly remplacé par Ser → AChE modifiée, le carbamate ne s'y fixe plus → résistance ; l'hypothèse est vérifiée.",
    SQ, "Sujet 2020 N : document 3", "Les triplets 243 à 251 des allèles Ace-S et Ace-R ; le triplet 247 encadré",
    "Question trois : vérifions l'hypothèse avec les séquences. Le document trois : le brin non transcrit, du triplet deux cent quarante-trois au triplet deux cent cinquante et un. D'abord l'allèle de S. Puis l'allèle de R. Compare triplet par triplet. Une seule différence : le triplet deux cent quarante-sept : G G C chez S, A G C chez R. À toi : quel est le codon de l'ARN messager, et quel est l'acide aminé, à ce triplet, chez S et chez R ?",
    "السؤال الثالث: نتأكدو من l'hypothèse ب les séquences. le document trois: le brin non transcrit، من le triplet deux cent quarante-trois حتى ل deux cent cinquante et un. اللول l'allèle ديال S. من بعد l'allèle ديال R. قارن triplet ب triplet. فرق واحد: le triplet deux cent quarante-sept: G G C عند S، و A G C عند R. دابا نتا: شنو هو le codon ديال l'A R N messager، و شنو هو l'acide aminé، ف هاد le triplet، عند S و عند R؟",
    [pu("le document trois:", "triplets"), pu("اللول l'allèle ديال S.", "allele_s"), pu("من بعد l'allèle ديال R.", "allele_r"),
     pu("فرق واحد:", "difference"), rp("G G C عند S", "triplet_247")],
    {"type": "qcm", "prompt": "Triplet 247 : les codons de l'ARNm et les acides aminés sont…",
     "options": ["S : GGC → Gly ; R : AGC → Ser", "S : CCG → Pro ; R : UCG → Ser", "S : GGC → Gly ; R : AGC → Gly"],
     "timeout_seconds": 45, "correct": 0,
     "enonce_dit": "شوف هاد السؤال: ف le triplet deux cent quarante-sept، شنو هوما les codons ديال l'A R N messager و les acides aminés؟",
     "demonstration": {
         "parole": "le brin non transcrit: l'A R N messager عندو نفس la séquence، غير T كتولي U. هنا ما كاينش T: G G C كيبقى G G C، و A G C كيبقى A G C. le tableau: G G C، la glycine. A G C، la sérine.",
         "lignes": [{"texte": "brin non transcrit → ARNm : même séquence, U à la place de T", "mot": "le brin non transcrit:"},
                    {"texte": "triplet 247 : S GGC → ARNm GGC ; R AGC → ARNm AGC", "mot": "هنا ما كاينش T"},
                    {"texte": "tableau du code : GGC = Gly ; AGC = Ser", "mot": "le tableau:"}]}},
    {"q": {
        "0": {"juste": reac("مزيان، جواب صحيح. le brin non transcrit: نفس la séquence. G G C كيعطي la glycine، و A G C كيعطي la sérine.",
                            "Correct : à partir du brin non transcrit, l'ARNm garde la même séquence ; GGC code Gly, AGC code Ser.")},
        "1": {"1": reac("درتي la complémentarité. ولكن قرا السمية ديال le brin: non transcrit. واش كنديرو عليه la complémentarité؟ عاود جرب.",
                        "Tu as fait la complémentarité. Mais relis le nom du brin : non transcrit. Fait-on la complémentarité sur ce brin ? Réessaie."),
              "2": reac("لا، مع le brin non transcrit ما كاينش la complémentarité: l'A R N messager هو G G C و A G C، glycine و sérine. الجواب الصحيح هو A.",
                        "Non : pas de complémentarité sur le brin non transcrit. L'ARNm est GGC et AGC : Gly et Ser. Bonne réponse : A.")},
        "2": {"1": reac("les codons مزيانين. ولكن شوف le tableau مرة أخرى: A G C واش هو la glycine؟ عاود جرب.",
                        "Les codons sont justes. Mais relis le tableau : AGC code-t-il Gly ? Réessaie."),
              "2": reac("لا، A G C كيعطي la sérine، ماشي la glycine. إذن l'acide aminé تبدل. الجواب الصحيح هو A.",
                        "Non : AGC code la sérine, pas la glycine ; l'acide aminé change. Bonne réponse : A.")}},
     "e0": {
        "0": {"juste": reac("مزيان، هادي هي الجملة ديال le barème: la mutation، le codon، l'acide aminé، l'enzyme، le caractère، و ف اللخر: l'hypothèse est vérifiée.",
                            "Correct : mutation → codon → acide aminé → enzyme modifiée → résistance, puis « l'hypothèse est vérifiée ».")},
        "1": {"1": reac("قارن الطول ديال les triplets: واش مشى شي nucléotide؟ عاود جرب.",
                        "Compare la longueur des triplets : un nucléotide a-t-il disparu ? Réessaie."),
              "2": reac("لا، ماشي délétion: le triplet مازال فيه trois nucléotides، G ولات A. هادي substitution. الجواب الصحيح هو A.",
                        "Non, pas de délétion : le triplet garde trois nucléotides, G est remplacé par A. C'est une substitution. Bonne réponse : A.")},
        "2": {"1": reac("A G C واش كيعطي la glycine؟ شوف le tableau. عاود جرب.",
                        "AGC code-t-il la glycine ? Relis le tableau. Réessaie."),
              "2": reac("لا، la glycine ولات la sérine: l'enzyme تبدلات، و هادشي علاش le carbamate ما بقاش كيدخل. الجواب الصحيح هو A.",
                        "Non : Gly est remplacé par Ser ; l'enzyme est modifiée, et le carbamate ne s'y fixe plus. Bonne réponse : A.")}}},
    ["C5", "C8"],
    "Vérifier (2020 N) : triplet 247, GGC (Gly) chez S, AGC (Ser) chez R : substitution du 1er nucléotide G par A → Gly remplacé par Ser → AChE modifiée, le carbamate ne s'y fixe plus → résistance ; l'hypothèse est vérifiée.",
    exercises=[{
        "type": "qcm", "prompt": "Vérifiez l'hypothèse : quelle rédaction est juste ?",
        "choices": ["Substitution du 1er nucléotide G par A au triplet 247 du brin non transcrit du gène de l'AChE → le codon GGC devient AGC → Gly remplacé par Ser → AChE modifiée, sur laquelle le carbamate ne se fixe plus → résistance : l'hypothèse est vérifiée.",
                    "Délétion au triplet 247 → décalage du cadre de lecture → AChE absente → résistance : l'hypothèse est vérifiée.",
                    "Substitution au triplet 247 → Gly reste Gly → AChE identique → l'hypothèse est vérifiée."],
        "correct": 0,
        "explanation": "Un seul nucléotide change (G par A) : substitution ; Gly devient Ser, l'AChE est modifiée et le carbamate ne s'y fixe plus.",
        "enonce_dit": "شوف هاد السؤال: كيفاش كنكتبو la vérification ديال l'hypothèse؟",
        "demonstration": {
            "parole": "اللول les séquences. l'A R N messager ديال S: نفس le brin، غير T كتولي U. ف le triplet deux cent quarante-sept: G G C، la glycine. عند R، نفس الشي، غير le triplet deux cent quarante-sept: A G C، la sérine. كنكتبو: mutation par substitution du premier nucléotide، G par A، au triplet deux cent quarante-sept، du brin non transcrit. le codon G G C ولا A G C، la glycine تبدلات ب la sérine. l'enzyme تبدلات، و le carbamate ما بقاش كيدخل ف le site actif: les moustiques R résistants. إذن l'hypothèse est vérifiée.",
            "lignes": [{"texte": "ARNm S : AUC UUC GGG GGU GGC UUC UAC UCC GGG → Ile – Phe – Gly – Gly – Gly – Phe – Tyr – Ser – Gly", "mot": "اللول les séquences."},
                       {"texte": "ARNm R : AUC UUC GGG GGU AGC UUC UAC UCC GGG → Ile – Phe – Gly – Gly – Ser – Phe – Tyr – Ser – Gly", "mot": "عند R، نفس الشي"},
                       {"texte": "Mutation par substitution du 1er nucléotide G par A au triplet 247 du brin non transcrit du gène de l'AChE", "mot": "كنكتبو: mutation par"},
                       {"texte": "→ le codon GGC devient AGC → Gly est remplacé par Ser", "mot": "le codon G G C ولا"},
                       {"texte": "→ AChE modifiée : le carbamate ne se fixe plus sur son site actif → moustiques R résistants", "mot": "l'enzyme تبدلات"},
                       {"texte": "→ l'hypothèse est vérifiée", "mot": "إذن l'hypothèse est vérifiée"}]}}])

# ── 4b. 2022 N : Blackfan-Diamond (document sur le ribosome) ─────────────────────────────────────────────────────
BF = f"{SIM}national.html?vue=blackfan"
e8 = slide(
    "rg_e8_ribosomes", "Sujet 2022 N : un document sur le ribosome",
    "L'anémie de Blackfan-Diamond : la quantité des deux sous-unités du ribosome, chez un sain et chez un malade.",
    ["Un ribosome = une grande et une petite sous-unité.",
     "Individu sain : grandes 46 UA, petites 46 UA.",
     "Individu malade : grandes 46 UA, petites 23 UA.",
     "Consigne : comparez la quantité des petites sous-unités à celle des grandes, chez le sain puis chez le malade."],
    "2022 N, comparer : chez le sain, petites = grandes sous-unités (46 UA) ; chez le malade, petites (23 UA) = la moitié des grandes (46 UA).",
    BF, "Sujet 2022 N : document 1, figure a", "L'histogramme des grandes et petites sous-unités des ribosomes, sain puis malade",
    "Le sujet de deux mille vingt-deux : l'anémie de Blackfan-Diamond, une maladie où il manque beaucoup de globules rouges et d'hémoglobine. Document un, figure a : la quantité des sous-unités du ribosome. Rappelle-toi : le ribosome est fait de deux parties, la grande sous-unité et la petite sous-unité. Chez l'individu sain : la grande, quarante-six ; la petite, quarante-six. Chez l'individu malade : la grande, quarante-six ; la petite, vingt-trois. La question : comparez, chez chacun, la quantité des petites sous-unités à celle des grandes.",
    "le sujet ديال deux mille vingt-deux: l'anémie de Blackfan-Diamond، مرض فيه نقص كبير ف les globules rouges و ف l'hémoglobine. le document un، la figure a: la quantité ديال les sous-unités ديال le ribosome. تفكر: le ribosome فيه جوج: la grande sous-unité، و la petite sous-unité. عند l'individu sain: la grande quarante-six، و la petite quarante-six. عند l'individu malade: la grande quarante-six، و la petite vingt-trois. السؤال: comparez، عند كل واحد، la quantité ديال les petites sous-unités ب les grandes.",
    [pu("la figure a:", "axes"), rp("la grande sous-unité، و la petite", "histogramme"), pu("عند l'individu sain:", "saine"),
     rp("عند l'individu sain:", "barres_sain"), pu("عند l'individu malade:", "malade"), rp("و la petite vingt-trois", "barres_malade")],
    {"type": "qcm", "prompt": "Quelle comparaison est juste ?",
     "options": ["Chez le malade, il y a moins de grandes sous-unités que de petites.",
                 "Le sain et le malade ont la même quantité de petites sous-unités.",
                 "Sain : petites = grandes (46 UA) ; malade : les petites (23 UA) ne sont que la moitié des grandes (46 UA)."],
     "timeout_seconds": 40, "correct": 2,
     "enonce_dit": "شوف هاد السؤال: شمن مقارنة صحيحة؟",
     "demonstration": {
         "parole": "عند l'individu sain: les petites قد les grandes، quarante-six و quarante-six. عند l'individu malade: les petites غير vingt-trois، يعني النص ديال les grandes، اللي هوما quarante-six.",
         "lignes": [{"texte": "Individu sain : petites sous-unités = grandes sous-unités = 46 UA", "mot": "عند l'individu sain:"},
                    {"texte": "Individu malade : petites (23 UA) = la moitié des grandes (46 UA)", "mot": "عند l'individu malade:"}]}},
    {"q": {
        "2": {"juste": reac("مزيان، جواب صحيح. عند sain، قد قد. عند malade، les petites غير النص.",
                            "Correct : chez le sain, autant de petites que de grandes (46 UA) ; chez le malade, les petites (23 UA) sont la moitié des grandes.")},
        "0": {"1": reac("شوف مزيان شمن barre اللي قصيرة عند le malade: la grande ولا la petite؟ عاود جرب.",
                        "Regarde quelle barre est courte chez le malade : la grande ou la petite ? Réessaie."),
              "2": reac("لا، العكس: عند le malade، les grandes quarante-six، و les petites غير vingt-trois. الجواب الصحيح هو C.",
                        "Non, c'est l'inverse : chez le malade, 46 UA de grandes et seulement 23 UA de petites. Bonne réponse : C.")},
        "1": {"1": reac("قارن la petite ديال sain ب la petite ديال malade: quarante-six و vingt-trois. واش قد قد؟ عاود جرب.",
                        "Compare les petites du sain et du malade : 46 et 23 UA. Est-ce la même quantité ? Réessaie."),
              "2": reac("لا، les petites: quarante-six عند sain، و vingt-trois عند malade. عند malade، les petites هوما النص ديال les grandes. الجواب الصحيح هو C.",
                        "Non : 46 UA de petites chez le sain, 23 UA chez le malade, soit la moitié des grandes. Bonne réponse : C.")}}},
    ["C6", "C8"],
    "2022 N, comparer : chez le sain, petites = grandes sous-unités (46 UA) ; chez le malade, petites (23 UA) = la moitié des grandes (46 UA).")

e8b = slide(
    "rg_e8b_hemoglobine", "Sujet 2022 N : expliquer le manque d'hémoglobine",
    "Figure b : les sous-unités s'assemblent en ribosomes sur l'ARNm de l'hémoglobine.",
    ["Un ribosome fonctionnel demande une petite ET une grande sous-unité.",
     "Malade : moitié moins de petites sous-unités → moitié moins de ribosomes ; des grandes restent seules.",
     "Consigne : expliquez le manque d'hémoglobine chez le malade (en flèches)."],
    "Expliquer (2022 N) : manque de petites sous-unités → peu de ribosomes fonctionnels → faible traduction de l'ARNm de l'hémoglobine → faible quantité d'hémoglobine → anémie.",
    BF, "Sujet 2022 N : document 1, figure b", "Les sous-unités s'assemblent sur l'ARNm de l'hémoglobine : 4 ribosomes chez le sain, 2 chez le malade",
    "Maintenant la figure b. Dans chaque cellule, l'ARN messager de l'hémoglobine. Pour faire un ribosome, il faut une petite et une grande sous-unité. Regarde chez l'individu sain : les sous-unités s'assemblent. Chez l'individu malade : regarde combien de ribosomes se forment. Et les grandes qui restent ? Sans petite, elles ne travaillent pas. La question : expliquez le manque d'hémoglobine chez l'individu malade.",
    "دابا la figure b. ف كل cellule، كاين l'A R N messager ديال l'hémoglobine. باش يتكون ribosome، خاص petite sous-unité و grande sous-unité. شوف عند l'individu sain: les sous-unités كيتجمعو. عند l'individu malade: شوف شحال من ribosome تكون. و les grandes اللي بقاو؟ بلا petite، ما كيديرو والو. السؤال: expliquez le manque d'hémoglobine chez l'individu malade.",
    [pu("دابا la figure b.", "assemblage"), rp("شوف عند l'individu sain:", "cellule_saine"),
     rp("شوف شحال من ribosome", "ribosomes_malade"), pu("السؤال: expliquez", "hemoglobine"), rp("le manque d'hémoglobine", "hemoglobine")],
    {"type": "qcm", "prompt": "Quelle explication est rédigée comme le barème ?",
     "options": ["Manque de petites sous-unités → formation d'une faible quantité de ribosomes fonctionnels → faible traduction de l'ARNm de l'hémoglobine → faible quantité d'hémoglobine.",
                 "Manque de grandes sous-unités → pas de ribosomes → pas d'hémoglobine.",
                 "L'ARNm de l'hémoglobine est absent chez le malade → pas d'hémoglobine."],
     "timeout_seconds": 45, "correct": 0,
     "enonce_dit": "شوف هاد السؤال: شمن تفسير مكتوب بحال le barème؟",
     "demonstration": {
         "parole": "نقص ف les petites sous-unités: ribosomes fonctionnels قلال. إذن la traduction ديال l'A R N messager ديال l'hémoglobine ضعيفة. إذن l'hémoglobine قليلة: هادي هي la maladie.",
         "lignes": [{"texte": "Manque de petites sous-unités → faible quantité de ribosomes fonctionnels", "mot": "نقص ف les petites"},
                    {"texte": "→ faible traduction de l'ARNm de l'hémoglobine", "mot": "إذن la traduction"},
                    {"texte": "→ faible quantité d'hémoglobine → anémie de Blackfan-Diamond", "mot": "إذن l'hémoglobine قليلة"}]}},
    {"q": {
        "0": {"juste": reac("مزيان، جواب صحيح: petites قلال، ribosomes قلال، traduction ضعيفة، hémoglobine قليلة.",
                            "Correct : moins de petites sous-unités → moins de ribosomes fonctionnels → traduction faible → peu d'hémoglobine.")},
        "1": {"1": reac("شوف la figure a مرة أخرى: شمن sous-unité اللي ناقصة عند le malade؟ عاود جرب.",
                        "Revois la figure a : quelle sous-unité manque chez le malade ? Réessaie."),
              "2": reac("لا، les grandes كاملين، quarante-six. اللي ناقصين هوما les petites. و كاينين شي ribosomes، إذن شوية ديال l'hémoglobine. الجواب الصحيح هو A.",
                        "Non : les grandes sont normales (46 UA) ; ce sont les petites qui manquent, et il reste quelques ribosomes, donc un peu d'hémoglobine. Bonne réponse : A.")},
        "2": {"1": reac("شوف la figure b: واش l'A R N messager كاين عند le malade؟ عاود جرب.",
                        "Regarde la figure b : l'ARNm de l'hémoglobine est-il présent chez le malade ? Réessaie."),
              "2": reac("لا، l'A R N messager كاين. اللي ناقص هوما les ribosomes، حيت les petites sous-unités قلال. الجواب الصحيح هو A.",
                        "Non : l'ARNm est bien là ; ce qui manque, ce sont les ribosomes, faute de petites sous-unités. Bonne réponse : A.")}}},
    ["C6", "C8"],
    "Expliquer (2022 N) : manque de petites sous-unités → peu de ribosomes fonctionnels → faible traduction de l'ARNm de l'hémoglobine → faible quantité d'hémoglobine → anémie.")

# ── Placement dans la partie IX ───────────────────────────────────────────────────────────────────────────────────
p9 = next(a for a in m["activities"] if a["id"] == "rg_partie9")
ids = [s["id"] for s in p9["slides"]]
i5 = ids.index("rg_e5_national")
p9["slides"][i5:i5 + 1] = [e5a, e5, e7, e7b, e7c, e8, e8b]
p9["title"] = "IX. L'exercice national : rédiger comme le barème, une consigne à la fois"
p9["duration_minutes"] = 75
m["estimated_minutes"] = m.get("estimated_minutes", 365) + 30

# ── Séances ──────────────────────────────────────────────────────────────────────────────────────────────────────
s7 = next(x for x in m["seances"] if x["id"] == "rg_s7")
b3 = next(b for b in s7["blocs"] if b["id"] == "rg_s7_b3")
ancien = json.loads(json.dumps(b3))
s7["titre"] = "Séance 7 — Rédiger comme le barème, puis le sujet 2024 N pas à pas"
b3.update({
    "titre": "Le sujet 2024 N, une consigne à la fois",
    "slide_ids": ["rg_e5a_document", "rg_e5_national"],
    "cahier": [{"texte": e5a["concentration"]["cahier"]}, {"texte": e5["concentration"]["cahier"]}],
    "retrouver": {"prompt": "Cahier fermé : écris la relation protéine – caractère de l'amélogénèse imparfaite.",
                  "attendu": "Amélogénine normale → minéralisation normale → émail normal ; amélogénine anormale → minéralisation faible → émail atteint ; d'où la relation protéine – caractère.",
                  "competence_id": "C2",
                  "enonce_dit": "شوف هاد السؤال: سد الكراس، و كتب la relation protéine caractère ديال l'amélogénèse imparfaite."},
    "exercice": {"type": "libre",
                 "prompt": "Brin transcrit : TAC CTT GCA. Écris l'ARNm, puis la séquence d'acides aminés.",
                 "attendu": "ARNm : AUG GAA CGU → Met – Glu – Arg.",
                 "demonstration": {
                     "parole": "هنا le brin transcrit: كنديرو la complémentarité، و ف بلاصة T كنكتبو U. T A C كيعطي A U G، C T T كيعطي G A A، G C A كيعطي C G U. le tableau: A U G، la méthionine. G A A، l'acide glutamique. C G U، l'arginine.",
                     "lignes": [{"texte": "brin transcrit → complémentarité (A→U, T→A, C→G, G→C)", "mot": "هنا le brin transcrit"},
                                {"texte": "TAC CTT GCA → ARNm AUG GAA CGU", "mot": "T A C كيعطي"},
                                {"texte": "→ Met – Glu – Arg", "mot": "le tableau:"}]},
                 "enonce_dit": "شوف هاد السؤال: brin transcrit، T A C، C T T، G C A. كتب l'A R N messager، و من بعد les acides aminés."}})
s8 = {"id": "rg_s8", "titre": "Séance 8 — Le national pas à pas : hypothèse, ribosome, puis le bilan", "blocs": [
    {"id": "rg_s8_b1", "titre": "2020 N : la relation, l'hypothèse, la vérification",
     "slide_ids": ["rg_e7_moustiques", "rg_e7b_hypothese", "rg_e7c_verifier"],
     "cahier": [{"texte": e7["concentration"]["cahier"]}, {"texte": e7b["concentration"]["cahier"]}, {"texte": e7c["concentration"]["cahier"]}],
     "retrouver": {"prompt": "Cahier fermé : comment écrit-on une hypothèse, puis sa vérification ?",
                   "attendu": "Hypothèse au conditionnel (« serait due à… ») ; vérification : mutation → codon → acide aminé → protéine modifiée → caractère, puis « l'hypothèse est vérifiée ».",
                   "competence_id": "C8",
                   "enonce_dit": "شوف هاد السؤال: سد الكراس. كيفاش كنكتبو l'hypothèse، و كيفاش كنتأكدو منها؟"},
     "exercice": {"type": "qcm", "prompt": "Une hypothèse s'écrit…",
                  "options": ["au conditionnel : « la résistance serait due à… »", "au présent, comme un résultat sûr", "sous forme de question"],
                  "correct": 0, "explanation": "L'hypothèse n'est pas encore prouvée : on l'écrit au conditionnel.",
                  "enonce_dit": "شوف هاد السؤال: l'hypothèse كيفاش كتتكتب؟"}},
    {"id": "rg_s8_b2", "titre": "2022 N : un document sur le ribosome",
     "slide_ids": ["rg_e8_ribosomes", "rg_e8b_hemoglobine"],
     "cahier": [{"texte": e8["concentration"]["cahier"]}, {"texte": e8b["concentration"]["cahier"]}],
     "retrouver": {"prompt": "Cahier fermé : de quoi est fait un ribosome, et que se passe-t-il s'il manque des petites sous-unités ?",
                   "attendu": "Une grande et une petite sous-unité ; s'il manque des petites sous-unités, peu de ribosomes fonctionnels → faible traduction → peu de protéine.",
                   "competence_id": "C6",
                   "enonce_dit": "شوف هاد السؤال: سد الكراس. le ribosome فيه شنو؟ و يلا نقصو les petites sous-unités، شنو كيوقع؟"},
     "exercice": {"type": "qcm", "prompt": "Il manque la moitié des petites sous-unités. Le nombre de ribosomes fonctionnels…",
                  "options": ["est divisé par deux environ", "ne change pas", "double"],
                  "correct": 0, "explanation": "Chaque ribosome demande une petite sous-unité : moitié moins de petites, moitié moins de ribosomes.",
                  "enonce_dit": "شوف هاد السؤال: النص ديال les petites sous-unités ناقص. شحال كيبقاو ديال les ribosomes؟"}},
    {"id": "rg_s8_b3", "titre": "Retour à la drépanocytose, et le bilan",
     "slide_ids": ["rg_e6_drepanocytose", "rg_b1_bilan", "rg_b2_carte"],
     "cahier": ancien["cahier"][1:], "retrouver": ancien["retrouver"], "exercice": ancien["exercice"]}]}
m["seances"].append(s8)

# ── Compétences ──────────────────────────────────────────────────────────────────────────────────────────────────
for s in (e5a, e7, e7b, e7c, e8, e8b, e5):
    for cid in s["competence_ids"]:
        c = next(x for x in m["competences"] if x["id"] == cid)
        if s["id"] not in c["slide_ids"]:
            c["slide_ids"].append(s["id"])

json.dump(m, open(P, "w", encoding="utf-8"), ensure_ascii=False, indent=2)

print("2ᵉ passe appliquée :", P)
