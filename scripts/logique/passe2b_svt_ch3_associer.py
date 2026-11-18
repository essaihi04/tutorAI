"""SVT ch3, 2ᵉ passe (suite, 18 novembre 2026) : la question d'association du national 2024 N jouée pas à pas.

National 2024 N, première partie, IV : « recopier les couples (1,…), (2,…), (3,…), (4,…) » — 1. ADN polymérase,
2. centromère, 3. nucléosome, 4. ribosome ; a. histones – ADN, b. synthèse des protéines, c. synthèse de l'ARNm,
d. relie les deux chromatides, e. enzyme de la réplication. Corrigé : (1, e) ; (2, d) ; (3, a) ; (4, b).
Le ribosome (4, b) et la proposition c (ARNm) sont du chapitre 4 : ils ne sont ni joués ni écrits (règle 27).

Deux diapositives sur la vue `documents.html?vue=associer`, une consigne chacune, la réponse avant le lien :
  - ig_x1e_associer : les trois structures peintes l'une après l'autre, les propositions a, d, e ; question : le numéro 1 ;
    après la réponse, le lien (1, e) se trace (`apres_reponse`, `{conclusions: false}` tant que la question est ouverte) ;
  - ig_x1f_associer_couples : (1, e) au tableau ; question : les couples de 2 et 3 ; après la réponse, (2, d), (3, a)
    et la réponse du barème se tracent, puis la démonstration écrit les couples comme le barème.
Sur la copie en attente seulement ; idempotent. Puis : python3 -X utf8 scripts/logique/lister_voix.py svt_ch3_notion_information_genetique
"""
import json
from pathlib import Path

R = Path(__file__).resolve().parents[2]
F = R / "backend/data/courses/en_attente/svt_ch3_notion_information_genetique.json"
SIM = "/media/simulations/svt/notion_information_genetique-tableau/"
m = json.load(open(F, encoding="utf-8"))
ACT = {a["id"]: a for a in m["activities"]}
S = {s["id"]: s for a in m["activities"] for s in a["slides"]}


def rea(parole, ecrit):
    return {"parole": parole, "ecrit": ecrit}


def geste(mot, moment=None, temps=None, repere=None):
    out = []
    if moment: out.append({"mot": mot, "commande": "play_until", "parametres": {"moment": moment}})
    if temps is not None: out.append({"mot": mot, "commande": "set_time", "parametres": {"time_s": temps}})
    if repere: out.append({"mot": mot, "repere": repere})
    return out


PROPS = ["a. Complexe formé par l'association Histones – ADN.", "d. Structure reliant les deux chromatides du même chromosome.",
         "e. Enzyme qui intervient dans la réplication de l'ADN."]

# ── ig_x1e_associer : le document, puis la consigne 1 (le numéro 1) ──
mx1 = ("دابا سؤال آخر بحال la première partie ديال l'examen، من le national deux mille vingt-quatre: associer. "
       "على اليسار، l'ensemble A. اللول: l'ADN polymérase، هنا ف une fourche de réplication. "
       "التاني: le centromère، ف هاد le chromosome اللي فيه deux chromatides. التالت: le nucléosome. "
       "على اليمين، l'ensemble B: trois propositions، a و d و e. قرا كل proposition حتى للكلمة اللخرة. "
       "نبداو ب le numéro un: l'ADN polymérase، مع أشمن lettre؟")
fr1 = ("Encore une question comme dans la première partie de l'examen, du national deux mille vingt-quatre : associer. À gauche, l'ensemble A. "
       "Le premier : l'ADN polymérase, ici sur une fourche de réplication. Le deuxième : le centromère, sur ce chromosome à "
       "deux chromatides. Le troisième : le nucléosome. À droite, l'ensemble B : trois propositions, a, d et e. Lis chaque "
       "proposition jusqu'au dernier mot. Commençons par le numéro un : l'ADN polymérase va avec quelle lettre ?")
x1e = {
    "id": "ig_x1e_associer", "slide_type": "evaluation", "title": "Associer, comme au national 2024 N",
    "screen_content": {"lead": "National 2024 N : relie chaque élément de l'ensemble A à sa proposition de l'ensemble B.",
                       "bullets": ["1. ADN polymérase ; 2. Centromère ; 3. Nucléosome.", "a, d, e : lis chaque proposition jusqu'au dernier mot."],
                       "student_trace": "Associer : chercher dans chaque proposition le mot qui dit le rôle ou la composition ; une lettre par numéro ; recopier les couples."},
    "visual": {"kind": "simulation", "url": SIM + "documents.html?vue=associer", "caption": "National 2024 N : associer",
               "alt": "À gauche, l'ADN polymérase sur une fourche, un chromosome à deux chromatides, un fil de nucléosomes ; à droite, les propositions a, d, e ; aucun lien tracé"},
    "speech_text": {"fr": fr1, "mixed": mx1},
    "concentration": {
        "demarrer": "reset",
        "pointage": geste("على اليسار، l'ensemble", moment="ensembles")
        + geste("اللول: l'ADN polymérase", moment="polymerase", repere="structure_1")
        + geste("التاني: le centromère", moment="centromere", repere="structure_2")
        + geste("التالت: le nucléosome", moment="nucleosome", repere="structure_3")
        + geste("على اليمين، l'ensemble B", moment="propositions")
        + geste("قرا كل proposition", repere="a")
        + geste("نبداو ب le numéro", repere="structure_1"),
        "apres_reponse": {"sim_avant": {"conclusions": False},
                          "etapes": [{"commande": "set_parameters", "parametres": {"conclusions": True}},
                                     {"commande": "play_until", "parametres": {"moment": "lien_1"}}, {"repere": "lien_1"}]},
        "cahier": "Associer : chercher dans chaque proposition le mot qui dit le rôle ou la composition ; une lettre par numéro ; recopier les couples.",
        "reponses": {"q": {
            "2": {"juste": rea("مزيان! l'ADN polymérase enzyme، و كتخدم ف la réplication: ف la fourche، كتزيد le brin nouveau. le couple: un، e.",
                               "Oui : l'ADN polymérase est l'enzyme qui intervient dans la réplication ; à la fourche, elle allonge le brin nouveau. Couple (1, e).")},
            "0": {"1": rea("les histones و l'A D N، هادي حاجة أخرى ف l'ensemble A. شوف la figure اللولة: l'enzyme شنو كتدير ف la fourche؟ عاود جرب.",
                           "Histones et ADN : c'est un autre élément de l'ensemble A. Regarde la première figure : que fait l'enzyme à la fourche ? Réessaie."),
                  "2": rea("لا، a هي le nucléosome. l'ADN polymérase هي l'enzyme ديال la réplication: e.",
                           "Non : a, c'est le nucléosome. L'ADN polymérase est l'enzyme de la réplication : e.")},
            "1": {"1": rea("اللي كيجمع les deux chromatides عنصر آخر ف l'ensemble A. l'ADN polymérase فين كتخدم؟ شوف la fourche. عاود جرب.",
                           "Ce qui relie les deux chromatides est un autre élément de l'ensemble A. Où travaille l'ADN polymérase ? Regarde la fourche. Réessaie."),
                  "2": rea("لا، d هو le centromère. l'ADN polymérase هي l'enzyme ديال la réplication: e.",
                           "Non : d, c'est le centromère. L'ADN polymérase est l'enzyme de la réplication : e.")}}}},
    "question": {"type": "qcm", "prompt": "L'ADN polymérase (numéro 1) va avec quelle proposition ?", "options": PROPS,
                 "timeout_seconds": 40, "correct": 2, "enonce_dit": "سؤال: l'ADN polymérase، le numéro un، مع أشمن proposition؟"},
    "competence_ids": ["C7", "C8"],
}

# ── ig_x1f_associer_couples : (1, e) au tableau, puis la consigne 2 (les numéros 2 et 3) ──
mx2 = ("le premier couple: un، e. l'ADN polymérase هي l'enzyme ديال la réplication: ف la fourche، كتزيد le brin nouveau. "
       "بقاو جوج: le centromère و le nucléosome، و جوج propositions، a و d. "
       "شوف le chromosome: le centromère شنو كيدير؟ شوف le nucléosome: شنو فيه؟ "
       "قلب ف كل proposition على الكلمة اللي كتقول هادشي.")
fr2 = ("Le premier couple : un, e. L'ADN polymérase est l'enzyme de la réplication : sur la fourche, elle allonge le brin "
       "nouveau. Il reste deux numéros, le centromère et le nucléosome, et deux propositions, a et d. Regarde le "
       "chromosome : que fait le centromère ? Regarde le nucléosome : de quoi est-il fait ? Cherche dans chaque proposition "
       "le mot qui le dit.")
demo2 = ("نكتبو بحال le barème. un، e: l'ADN polymérase، l'enzyme ديال la réplication. "
         "deux، d: le centromère كيربط les deux chromatides. trois، a: le nucléosome، les histones و l'A D N. "
         "ف la copie، كنكتبو غير les couples.")
lignes2 = [("(1, e) : l'ADN polymérase, enzyme de la réplication de l'ADN", "un، e:"),
           ("(2, d) : le centromère relie les deux chromatides du même chromosome", "deux، d:"),
           ("(3, a) : le nucléosome, association histones – ADN", "trois، a:"),
           ("Sur la copie : (1, e) ; (2, d) ; (3, a)", "ف la copie")]
for _, mot in lignes2: assert mot in demo2, mot
x1f = {
    "id": "ig_x1f_associer_couples", "slide_type": "evaluation", "title": "Associer : les deux derniers couples",
    "screen_content": {"lead": "(1, e) est trouvé : il reste le centromère et le nucléosome, a et d.",
                       "bullets": ["Le centromère : que relie-t-il ?", "Le nucléosome : de quoi est-il fait ?"],
                       "student_trace": "(1, e) ADN polymérase : enzyme de la réplication ; (2, d) centromère : relie les deux chromatides ; (3, a) nucléosome : histones + ADN. Réponse : (1, e) ; (2, d) ; (3, a)."},
    "visual": {"kind": "simulation", "url": SIM + "documents.html?vue=associer&diapo=x1f", "caption": "Les couples, comme le barème",
               "alt": "Le lien (1, e) tracé ; le centromère et le nucléosome attendent leur lettre"},
    "speech_text": {"fr": fr2, "mixed": mx2},
    "concentration": {
        "pointage": geste("le premier couple", temps=12.4, repere="lien_1")
        + geste("بقاو جوج: le centromère", repere="structure_2")
        + geste("و جوج propositions، a", repere="a")
        + geste("شوف le chromosome", repere="structure_2")
        + geste("شوف le nucléosome", repere="structure_3"),
        "apres_reponse": {"etapes": [{"commande": "play_until", "parametres": {"moment": "lien_2"}},
                                     {"commande": "play_until", "parametres": {"moment": "lien_3"}},
                                     {"commande": "play_until", "parametres": {"moment": "couples"}}, {"repere": "reponse"}]},
        "cahier": "(1, e) ADN polymérase : enzyme de la réplication ; (2, d) centromère : relie les deux chromatides ; (3, a) nucléosome : histones + ADN. Réponse : (1, e) ; (2, d) ; (3, a).",
        "reponses": {"q": {
            "0": {"juste": rea("مزيان! le centromère كيربط les deux chromatides: d. le nucléosome فيه l'A D N و les histones: a. دابا نكتبو الجواب بحال le barème.",
                               "Oui : le centromère relie les deux chromatides (d) ; le nucléosome est formé d'ADN et d'histones (a).")},
            "1": {"1": rea("شوف مزيان le chromosome: النقطة اللي ف الوسط كتجمع جوج chromatides. أشمن proposition فيها chromatides؟ عاود جرب.",
                           "Regarde le chromosome : le point du milieu relie les deux chromatides. Quelle proposition parle de chromatides ? Réessaie."),
                  "2": rea("لا، قلبتي. le centromère كيربط les deux chromatides: هادي d. le nucléosome فيه les histones و l'A D N: هادي a.",
                           "Non, c'est inversé : le centromère relie les deux chromatides (d) ; le nucléosome est formé d'histones et d'ADN (a). Réponse : (2, d) ; (3, a).")},
            "2": {"1": rea("e خديناها: l'ADN polymérase. كل lettre كتمشي مع numéro واحد. بقاو غير a و d. عاود جرب.",
                           "La lettre e est déjà prise par l'ADN polymérase : chaque lettre va avec un seul numéro. Il ne reste que a et d. Réessaie."),
                  "2": rea("لا، e ديال l'ADN polymérase. le centromère: d، حيت كيربط les deux chromatides. le nucléosome: a، les histones و l'A D N.",
                           "Non : e est l'ADN polymérase. Le centromère : d (il relie les deux chromatides) ; le nucléosome : a (histones et ADN).")}}}},
    "question": {"type": "qcm", "prompt": "Quels sont les couples des numéros 2 (centromère) et 3 (nucléosome) ?",
                 "options": ["(2, d) ; (3, a)", "(2, a) ; (3, d)", "(2, e) ; (3, a)"], "timeout_seconds": 40, "correct": 0,
                 "enonce_dit": "سؤال: le centromère و le nucléosome، أشمن couples؟",
                 "demonstration": {"parole": demo2, "lignes": [{"texte": t, "mot": w} for t, w in lignes2]}},
    "competence_ids": ["C2", "C8"],
}
for s in (x1e, x1f):
    for p in s["concentration"]["pointage"]: assert p["mot"] in s["speech_text"]["mixed"], p["mot"]

fait = []
p8 = ACT["ig_partie8"]
if "ig_x1e_associer" not in S:
    i = next(k for k, s in enumerate(p8["slides"]) if s["id"] == "ig_x1d_corrige_metaphase")
    p8["slides"][i + 1:i + 1] = [x1e, x1f]
    p8["duration_minutes"] = p8.get("duration_minutes", 50) + 5
    m["estimated_minutes"] = sum(a.get("duration_minutes", 0) for a in m["activities"])
    fait.append("ig_x1e_associer, ig_x1f_associer_couples (partie VIII, après ig_x1d)")
else:   # relancé : les textes du script font foi
    for s in (x1e, x1f):
        for a in m["activities"]:
            a["slides"] = [s if t["id"] == s["id"] else t for t in a["slides"]]

b3 = next(b for se in m["seances"] for b in se["blocs"] if b["id"] == "ig_s7_b3")
if "ig_x1e_associer" not in b3["slide_ids"]:
    j = b3["slide_ids"].index("ig_x1d_corrige_metaphase")
    b3["slide_ids"][j + 1:j + 1] = ["ig_x1e_associer", "ig_x1f_associer_couples"]
    b3["titre"] = "Comme à l'examen : la restitution, QCM et association posés puis corrigés"
    b3["cahier"].append({"texte": "Associer (2024 N) : (1, e) ADN polymérase, enzyme de la réplication ; (2, d) centromère, relie les deux chromatides ; (3, a) nucléosome, histones + ADN."})
    fait.append("ig_s7_b3 : + l'association")

C = {c["id"]: c for c in m["competences"]}
ordre = [s["id"] for a in m["activities"] for s in a["slides"]]
for cid, ids in (("C7", ["ig_x1e_associer"]), ("C2", ["ig_x1f_associer_couples"]), ("C8", ["ig_x1e_associer", "ig_x1f_associer_couples"])):
    for i in ids:
        if i not in C[cid]["slide_ids"]: C[cid]["slide_ids"].append(i)
    C[cid]["slide_ids"].sort(key=ordre.index)

json.dump(m, open(F, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print("\n".join(fait) or "rien à faire (textes remis à jour)")
