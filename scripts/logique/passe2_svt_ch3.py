"""2ᵉ passe du cours SVT ch3 « Notion de l'information génétique » (18 novembre 2026, skill logique-de-cours).

Travaille sur la copie en attente (backend/data/courses/en_attente/svt_ch3_notion_information_genetique.json), jamais
sur le cours en ligne. Idempotent : relancé, il ne refait que ce qui manque.
  - les cas types du national joués pas à pas : QCM de restitution posés AVANT leur corrigé joué (2024 R, 2018 R),
    la courbe de l'ADN décrite puis expliquée par l'élève (une consigne par diapositive), l'exercice de la thymidine
    radioactive (2017 R) en quatre temps : décrire, expliquer le 1er cycle, expliquer le 2e, le schéma et la conclusion ;
  - rien de décisif avant la réponse : meselson.html {conclusions: false} sur les observations de G1 et G2 ;
  - la vue « trois expériences côte à côte » (noyau.html?vue=trois) sur ig_l6_definition (texte et voix inchangés) ;
  - la phrase du barème de l'anaphase (2018 R) en démonstration de la question d'ig_m4_anaphase.
Un texte de voix changé perd son `audio` ; une diapositive dont le texte et l'id restent gardent leur voix.
Puis : python3 -X utf8 scripts/logique/lister_voix.py svt_ch3_notion_information_genetique
"""
import copy, json
from pathlib import Path

R = Path(__file__).resolve().parents[2]
F = R / "backend/data/courses/en_attente/svt_ch3_notion_information_genetique.json"
SIM = "/media/simulations/svt/notion_information_genetique-tableau/"
m = json.load(open(F, encoding="utf-8"))
ACT = {a["id"]: a for a in m["activities"]}
S = {s["id"]: s for a in m["activities"] for s in a["slides"]}


def pt(mot, **k):
    d = {"mot": mot}
    if "moment" in k: d.update(commande="play_until", parametres={"moment": k["moment"]})
    if "temps" in k: d.update(commande="set_time", parametres={"time_s": k["temps"]})
    if "repere" in k: d["repere"] = k["repere"]
    return d


def pts(*spec):
    """spec : (mot, {moment, repere, temps}) → un geste par commande puis un repère (comme les diapositives existantes)."""
    out = []
    for mot, k in spec:
        if "moment" in k: out.append(pt(mot, moment=k["moment"]))
        if "temps" in k: out.append(pt(mot, temps=k["temps"]))
        if "repere" in k: out.append(pt(mot, repere=k["repere"]))
    return out


def rea(parole, ecrit):
    return {"parole": parole, "ecrit": ecrit}


def reponses(bonne, juste, faux):
    """faux : {option: (indice parole, indice écrit, réponse parole, réponse écrit)}."""
    r = {str(bonne): {"juste": rea(*juste)}}
    for o, (p1, e1, p2, e2) in faux.items():
        r[str(o)] = {"1": rea(p1, e1), "2": rea(p2, e2)}
    return r


def diapo(id_, titre, url, fr, mixed, pointage, lead, bullets, trace, caption, alt, question=None, rep=None,
          competences=("C8",), type_="exercise"):
    s = {"id": id_, "slide_type": type_, "title": titre,
         "screen_content": {"lead": lead, "bullets": bullets, "student_trace": trace},
         "visual": {"kind": "simulation", "url": SIM + url, "caption": caption, "alt": alt},
         "speech_text": {"fr": fr, "mixed": mixed},
         "concentration": {"pointage": pointage, "cahier": trace, "reponses": {"q": rep} if rep else {}},
         "competence_ids": list(competences)}
    if question: s["question"] = question
    return s


def qcm(prompt, options, correct, dit, demo=None):
    q = {"type": "qcm", "prompt": prompt, "options": options, "timeout_seconds": 40, "correct": correct, "enonce_dit": dit}
    if demo: q["demonstration"] = demo
    return q


def demo(parole, lignes):
    for texte, mot in lignes: assert mot in parole, (mot, parole)
    return {"parole": parole, "lignes": [{"texte": t, "mot": w} for t, w in lignes]}


fait = []

# ── 1. ig_l6_definition : les trois expériences côte à côte (le texte ne change pas : la voix reste) ──
l6 = S["ig_l6_definition"]
if "vue=trois" not in l6["visual"]["url"]:
    l6["visual"].update(url=SIM + "noyau.html?vue=trois", caption="Les trois expériences côte à côte",
                        alt="L'amibe coupée, l'acétabulaire greffée, la grenouille de Gurdon ; sous chacune : le caractère suit le noyau")
    l6["concentration"]["pointage"] = pts(("تلاتة ديال التجارب:", {"moment": "amibe", "repere": "exp_amibe"}),
                                          ("l'acétabulaire، و", {"moment": "acetabulaire", "repere": "exp_acetabulaire"}),
                                          ("و Gurdon. ف", {"moment": "gurdon", "repere": "exp_gurdon"}),
                                          ("ف كل مرة، الصفة", {"moment": "commun", "repere": "commun"}))
    fait.append("ig_l6_definition : vue trois")

# ── 2. Meselson : la conclusion se tait pendant les observations de G1 et G2 ──
for i in ("ig_r3_g1", "ig_r4_g2"):
    o = S[i]["concentration"]["observation"]
    if "sim_avant" not in o:
        o["sim_avant"], o["sim_apres"] = {"conclusions": False}, {"conclusions": True}
        fait.append(i + " : conclusions false pendant l'observation")

# ── 2b. ig_c6b_phases : la page est rechargée (&diapo=c6b_phases) ; elle saute au moment `duree_cycle` (déjà vu en
# ig_c6_durees, écrit d'un coup) au lieu de rejouer 20 s d'animation sous la voix ──
p6 = S["ig_c6b_phases"]["concentration"]["pointage"]
if p6[0].get("commande") == "play_until" and p6[0]["parametres"].get("moment") == "duree_cycle":
    p6[0] = {"mot": p6[0]["mot"], "commande": "set_time", "parametres": {"time_s": 19.6}}
    fait.append("ig_c6b_phases : départ par set_time sur duree_cycle")

# ── 3. ig_m4_anaphase : la phrase du barème (national 2018 R, « citez deux caractéristiques ») ──
q4 = S["ig_m4_anaphase"]["question"]
if "demonstration" not in q4:
    q4["demonstration"] = demo(
        "le barème كيطلب جوج caractéristiques ديال l'anaphase. الأولى: كل chromosome فيه chromatide وحدة، من بعد ما تقسم le centromère. "
        "الثانية: les deux chromatides ديال كل chromosome، كل وحدة كتمشي ل pôle، pôle opposé ديال الخلية.",
        [("Caractéristique 1 : chaque chromosome est formé d'une seule chromatide (après la division du centromère)", "الأولى:"),
         ("Caractéristique 2 : les deux chromatides de chaque chromosome se séparent et migrent vers les pôles opposés de la cellule", "الثانية:")])
    fait.append("ig_m4_anaphase : démonstration du barème")

# ── 4. Restitution : le QCM posé (x1), puis corrigé leurre par leurre (x1b, l'ancien texte et sa voix) ──
nouvelles = []
x1 = S["ig_x1_restitution"]
if "ig_x1b_corrige" not in S:
    x1b = copy.deepcopy(x1)
    x1b["id"], x1b["title"], x1b["slide_type"] = "ig_x1b_corrige", "Le corrigé : un leurre après l'autre", "evaluation"
    x1b.pop("exercices_fin_de_cours", None); x1b.pop("stable_id", None)
    x1b["screen_content"] = {"lead": "Le corrigé, comme le barème : chaque leurre barré avec sa raison, puis la bonne réponse.",
                             "bullets": ["a) condensé : c'est en mitose.", "c) deux chromatides : après la phase S.", "d) deux chromatides et condensé : prophase ou métaphase.",
                                         "Réponse : b) à une chromatide et non condensé."],
                             "student_trace": x1["screen_content"]["student_trace"]}
    x1b["visual"].update(caption="Le QCM corrigé leurre par leurre")
    nouvelles.append(x1b)
    x1["title"] = "Restitution : un QCM à toi d'abord"
    x1["screen_content"] = {"lead": "National 2024 R : lis la question jusqu'au dernier mot, puis choisis.",
                            "bullets": ["Pour chaque proposition : juste ou fausse, et pourquoi.", "Puis une seule réponse."],
                            "student_trace": x1["screen_content"]["student_trace"]}
    x1["visual"].update(caption="Un QCM du national : à toi de répondre", alt="La carte de QCM sur la phase G1, aucune proposition barrée")
    x1["speech_text"] = {
        "fr": "Comme dans la première partie de l'examen : un QCM. Lis la question jusqu'au dernier mot : au cours de la phase G1, chaque chromosome est… Quatre propositions. Prends ton temps : pour chacune, dis-toi si elle est juste ou fausse, et pourquoi. Puis choisis.",
        "mixed": "دابا بحال la première partie ديال l'examen: QCM. قرا السؤال حتى للكلمة اللخرة: au cours de la phase G un، chaque chromosome est... "
                 "وعندك ربعة ديال الأجوبة. خود الوقت ديالك: كل جواب، قول واش صحيح ولا غالط، وعلاش. ومن بعد اختار."}
    x1.pop("audio", None)
    x1["concentration"]["pointage"] = pts(("قرا السؤال حتى", {"moment": "carte"}), ("au cours de la phase", {"repere": "carte"}))
    x1["question"] = qcm("Au cours de la phase G1, chaque chromosome est :",
                         ["à une chromatide et condensé", "à une chromatide et non condensé", "à deux chromatides et non condensé", "à deux chromatides et condensé"], 1,
                         "سؤال: au cours de la phase G un، chaque chromosome est... اختار الجواب الصحيح.")
    x1["concentration"]["reponses"] = {"q": reponses(1,
        ("مزيان! ف G un، قبل la réplication: chromatide وحدة، و l'A D N ماشي condensé. دابا نصححو مع بعض، جواب بجواب.",
         "Oui : en G1, avant la réplication, chaque chromosome a une seule chromatide, et il n'est pas condensé."),
        {0: ("chromatide وحدة صحيحة. ولكن condensé؟ فوقاش كيولي le chromosome condensé؟ عاود جرب.",
             "Une chromatide : oui. Mais condensé ? Quand le chromosome se condense-t-il ? Réessaie.",
             "لا، condensé كيكون غير ف la mitose. ف G un، ماشي condensé. الجواب هو b: à une chromatide et non condensé.",
             "Non : le chromosome n'est condensé qu'en mitose. En G1 : une chromatide, non condensé (b)."),
         2: ("non condensé صحيحة. ولكن deux chromatides؟ فوقاش كيولي عندو جوج chromatides؟ عاود جرب.",
             "Non condensé : oui. Mais deux chromatides ? Quand le chromosome en a-t-il deux ? Réessaie.",
             "لا، deux chromatides كيكونو غير من بعد la phase S، ملي كتوقع la réplication. G un قبل S: chromatide وحدة. الجواب هو b.",
             "Non : deux chromatides seulement après la phase S (la réplication). G1 vient avant S : une chromatide (b)."),
         3: ("deux chromatides و condensé: هادا chromosome ديال la prophase ولا la métaphase. واش G un فيها la mitose؟ عاود جرب.",
             "Deux chromatides et condensé : c'est le chromosome de la prophase ou de la métaphase. G1 fait-elle partie de la mitose ? Réessaie.",
             "لا، هادا كيكون ف la mitose. ف G un: chromatide وحدة، ماشي condensé. الجواب هو b.",
             "Non : c'est le chromosome de la mitose. En G1 : une chromatide, non condensé (b).")})}
    fait.append("ig_x1_restitution réécrite (question avant le corrigé), ig_x1b_corrige (ancien texte et voix)")

if "ig_x1c_metaphase" not in S:
    opts = ["d'une seule chromatide constituée de deux brins d'ADN.", "de deux chromatides constituées chacune d'un brin d'ADN.",
            "de deux chromatides constituées chacune de deux brins d'ADN.", "de deux chromatides, l'une constituée d'un seul brin d'ADN et l'autre de deux brins d'ADN."]
    x1c = diapo("ig_x1c_metaphase", "QCM du national 2018 R : le chromosome en métaphase", "documents.html?vue=metaphase",
        "Un autre QCM, du national 2018. Durant la métaphase de la mitose, chaque chromosome est formé… Attention : deux mots comptent, chromatide et brin d'ADN. Réponds à chacun séparément : combien de chromatides ? Et combien de brins dans chaque chromatide ? Puis choisis.",
        "QCM آخر، من le national deux mille dix-huit. durant la métaphase de la mitose، chaque chromosome est formé... "
        "رد البال: جوج ديال الكلمات مهمين: chromatide، و brin d'A D N. جاوب على كل وحدة بوحدها: شحال من chromatide؟ و شحال من brin ف كل chromatide؟ ومن بعد اختار.",
        pts(("QCM آخر، من", {"moment": "carte"}), ("durant la métaphase", {"repere": "carte"})),
        "National 2018 R : une seule suggestion est correcte.", ["Combien de chromatides en métaphase ?", "Combien de brins d'ADN dans chaque chromatide ?"],
        "Métaphase : chaque chromosome est formé de deux chromatides, chacune une molécule d'ADN à deux brins.",
        "Le QCM du national 2018 R", "La carte du QCM : le chromosome en métaphase, quatre propositions, aucune barrée",
        qcm("Durant la métaphase de la mitose, chaque chromosome est formé :", opts, 2,
            "سؤال: durant la métaphase de la mitose، chaque chromosome est formé... اختار الجواب الصحيح."),
        reponses(2, ("مزيان! ف la métaphase، deux chromatides، حيت la réplication وقعات ف la phase S. وكل chromatide فيها molécule d'A D N، بجوج brins. دابا نصححو جواب بجواب.",
                     "Oui : en métaphase, deux chromatides (la réplication a eu lieu en phase S), et chaque chromatide est une molécule d'ADN à deux brins."),
                 {0: ("deux brins صحيحة. ولكن chromatide وحدة؟ la métaphase جات قبل ولا من بعد la phase S؟ عاود جرب.",
                      "Deux brins : oui. Mais une seule chromatide ? La métaphase vient-elle avant ou après la phase S ? Réessaie.",
                      "لا، chromatide وحدة كتكون ف G un ولا من بعد l'anaphase. ف la métaphase: deux chromatides، كل وحدة بجوج brins. الجواب هو c.",
                      "Non : une seule chromatide, c'est en G1 ou après l'anaphase. En métaphase : deux chromatides de deux brins chacune (c)."),
                  1: ("deux chromatides صحيحة. ولكن brin واحد؟ molécule d'A D N، شحال فيها من brin؟ عاود جرب.",
                      "Deux chromatides : oui. Mais un seul brin ? Combien de brins a une molécule d'ADN ? Réessaie.",
                      "لا، molécule d'A D N ديما فيها جوج brins، حتى من بعد la réplication. الجواب هو c: deux chromatides، كل وحدة بجوج brins.",
                      "Non : une molécule d'ADN a toujours deux brins, même après la réplication. Réponse : c."),
                  3: ("شوف: les deux chromatides جاو من la réplication ديال نفس la molécule. واش كيكونو مختلفين؟ عاود جرب.",
                      "Les deux chromatides viennent de la réplication de la même molécule. Peuvent-elles être différentes ? Réessaie.",
                      "لا، les deux chromatides بحال بحال: كل وحدة فيها molécule d'A D N بجوج brins. الجواب هو c.",
                      "Non : les deux chromatides sont identiques, chacune une molécule d'ADN à deux brins (c).")}),
        type_="evaluation")
    x1d = diapo("ig_x1d_corrige_metaphase", "Le corrigé du QCM 2018 R", "documents.html?vue=metaphase",
        "On corrige proposition par proposition. a : une seule chromatide ? Non : une chromatide, c'est en G1 ou en anaphase. b : un seul brin ? Non : une molécule d'ADN a toujours deux brins. d : une chromatide d'un brin, l'autre de deux ? Non : les deux chromatides sont identiques. Donc c : deux chromatides, et chaque chromatide a deux brins d'ADN, car la réplication a eu lieu en phase S.",
        "نصححو جواب بجواب. a: chromatide وحدة؟ لا، chromatide وحدة كتكون ف G un ولا ف l'anaphase. b: brin واحد؟ لا، molécule d'A D N ديما فيها جوج brins. "
        "d: chromatide فيها brin واحد، والأخرى فيها جوج؟ لا، les deux chromatides بحال بحال. إذن c: deux chromatides، و كل chromatide فيها جوج brins d'A D N، حيت la réplication وقعات ف la phase S.",
        pts(("a: chromatide وحدة؟", {"moment": "elimine_a", "repere": "a"}), ("b: brin واحد؟", {"moment": "elimine_b", "repere": "b"}),
            ("d: chromatide فيها", {"moment": "elimine_d", "repere": "d"}), ("إذن c: deux", {"moment": "reponse", "repere": "c"})),
        "Le corrigé, comme le barème : chaque leurre barré avec sa raison.",
        ["a) une seule chromatide : en G1 ou en anaphase.", "b) un seul brin : jamais, l'ADN a deux brins.", "d) les deux chromatides sont identiques.",
         "Réponse : c) deux chromatides de deux brins d'ADN chacune."],
        "Métaphase : deux chromatides (après la phase S), chacune une molécule d'ADN à deux brins.",
        "Le QCM 2018 R corrigé leurre par leurre", "La carte du QCM ; a, b, d barrés avec leur raison, c entourée", type_="evaluation")
    nouvelles += [x1c, x1d]
    fait.append("ig_x1c_metaphase, ig_x1d_corrige_metaphase (national 2018 R)")

# ── 5. La courbe de l'ADN : décrire (x2), puis expliquer (x2b, l'ancienne question et ses voix) ──
x2 = S["ig_x2_exercice"]
if "ig_x2b_expliquer" not in S:
    ancienne_q, anciennes_rep = x2["question"], x2["concentration"].get("reponses", {})
    x2b = diapo("ig_x2b_expliquer", "Deuxième consigne : expliquer", "documents.html?vue=courbe&reponse=decrire&diapo=x2b_expliquer",
        "La description est écrite. Deuxième consigne : expliquer, c'est-à-dire dire pourquoi. L'augmentation de 8 à 14 h, on la connaît : la réplication de l'ADN en phase S. Maintenant, regarde cette partie : de 19 à 20 h, la quantité revient de 6 à 3 UA. Pourquoi revient-elle de 2q à q ?",
        "دابا la description مكتوبة. السؤال الثاني: expliquer، يعني علاش. l'augmentation de huit à quatorze heures عرفناها: la réplication de l'A D N ف la phase S. "
        "دابا ركز على هاد الجزء: de dix-neuf à vingt heures، la quantité كترجع من six ل trois U A. علاش كترجع من deux q ل q؟",
        pts(("دابا la description", {"temps": 13.0, "repere": "reponse"}), ("l'augmentation de huit", {"repere": "montee_s"}), ("دابا ركز على", {"repere": "chute_m"})),
        "Deuxième consigne : expliquer chaque variation par sa cause.", ["8 à 14 h : la réplication de l'ADN (phase S).", "19 à 20 h : pourquoi de 2q à q ?"],
        x2["screen_content"]["student_trace"], "La courbe décrite : à toi d'expliquer", "La courbe et sa description écrite ; la chute de 19 à 20 h en jaune, l'explication pas encore écrite",
        ancienne_q, anciennes_rep.get("q"), competences=("C3", "C8"))
    nouvelles.append(x2b)
    x2["title"] = "Un exercice complet : d'abord décrire"
    x2["visual"].update(url=SIM + "documents.html?vue=courbe&reponse=rien", caption="La courbe d'examen : à toi de décrire",
                        alt="La courbe de la quantité d'ADN, sans réponse écrite ; la montée de 8 à 14 h en jaune")
    x2["screen_content"] = {"lead": "Courbe de l'ADN : une consigne à la fois. D'abord décrire, avec les valeurs.",
                            "bullets": ["Lire les axes : q = 3 UA, 2q = 6 UA.", "Décrire = ce qu'on voit, avec les valeurs, sans expliquer."],
                            "student_trace": "Décrire : de 0 à 8 h, la quantité d'ADN reste constante (3 UA) ; de 8 à 14 h, elle augmente de 3 à 6 UA (elle double) ; de 14 à 19 h, elle reste constante (6 UA) ; de 19 à 20 h, elle chute de 6 à 3 UA."}
    x2["concentration"]["cahier"] = x2["screen_content"]["student_trace"]
    x2["speech_text"] = {
        "fr": "Un exercice complet, comme à l'examen. Voici la courbe : la quantité d'ADN dans une cellule en fonction du temps. Avant tout : les axes et les valeurs. q vaut 3 UA et 2q vaut 6 UA. Première consigne : décrire, c'est-à-dire dire ce qu'on voit, avec les valeurs, sans expliquer. Regarde la partie de 8 à 14 heures. Comment l'écrire comme le barème ?",
        "mixed": "تمرين كامل، بحال l'examen. هادي la courbe: la quantité d'A D N ف خلية، en fonction du temps. قبل كلشي: les axes والقيم. q كتساوي trois U A، و deux q كتساوي six U A. "
                 "أول سؤال: décrire. يعني نقولو شنو كنشوفو، مع les valeurs، بلا ما نشرحو. شوف الجزء de huit à quatorze heures. كيفاش نكتبو هادشي بحال le barème؟"}
    x2.pop("audio", None)
    x2["concentration"]["pointage"] = pts(("هادي la courbe:", {"moment": "document", "repere": "courbe"}), ("قبل كلشي: les", {"moment": "lecture_axes", "repere": "axe_adn"}),
                                          ("شوف الجزء de", {"moment": "decrire_s", "repere": "montee_s"}))
    x2["question"] = qcm("De 8 à 14 h, la description rédigée comme le barème est :",
                         ["La quantité d'ADN augmente.", "La quantité d'ADN augmente de 3 à 6 UA : elle double.", "C'est la réplication de l'ADN."], 1,
                         "سؤال: de huit à quatorze heures، أشمن description مكتوبة بحال le barème؟",
                         demo("نوصفو la courbe كاملة، مرحلة بمرحلة، مع les valeurs. de zéro à huit heures: la quantité d'A D N ثابتة، trois U A. "
                              "de huit à quatorze heures: كتزاد من trois ل six U A، يعني كتولي جوج مرات. de quatorze à dix-neuf heures: ثابتة، six U A. "
                              "de dix-neuf à vingt heures: كتنقص من six ل trois U A.",
                              [("de 0 à 8 h : la quantité d'ADN reste constante, 3 UA", "de zéro à huit"),
                               ("de 8 à 14 h : elle augmente de 3 à 6 UA : elle double", "de huit à quatorze heures:"),
                               ("de 14 à 19 h : elle reste constante, 6 UA", "de quatorze à dix-neuf"),
                               ("de 19 à 20 h : elle chute de 6 à 3 UA", "de dix-neuf à vingt")]))
    x2["concentration"]["reponses"] = {"q": reponses(1,
        ("مزيان! فيها شنو وقع، كتزاد، ومع les valeurs: من trois ل six U A. هادا هو décrire.",
         "Oui : ce qui se passe (elle augmente) avec les valeurs (de 3 à 6 UA). C'est cela, décrire."),
        {0: ("صحيح، كتزاد. ولكن le barème كيطلب les valeurs. من شحال لشحال؟ عاود جرب.",
             "Juste : elle augmente. Mais le barème demande les valeurs : de combien à combien ? Réessaie.",
             "ناقصة: بلا les valeurs كتضيع النقطة. خاصك تكتب: la quantité d'A D N كتزاد من trois ل six U A، يعني كتولي جوج مرات.",
             "Incomplet : sans les valeurs, le point est perdu. Il faut écrire : elle augmente de 3 à 6 UA, elle double."),
         2: ("هادي صحيحة، ولكن هادا شرح، ماشي وصف. décrire هو شنو كنشوفو ف la courbe. عاود جرب.",
             "C'est vrai, mais c'est une explication, pas une description. Décrire, c'est dire ce qu'on voit sur la courbe. Réessaie.",
             "هادا شرح، كيجي من بعد. الوصف هو: la quantité d'A D N كتزاد من trois ل six U A، كتولي جوج مرات.",
             "C'est l'explication : elle vient après. La description : la quantité augmente de 3 à 6 UA, elle double.")})}
    x2["competence_ids"] = ["C3", "C8"]
    fait.append("ig_x2_exercice réécrite (décrire), ig_x2b_expliquer (l'ancienne question)")

# ── 6. La thymidine radioactive, national 2017 R : quatre temps ──
if "ig_x3_thymidine_doc" not in S:
    TH = ("C7", "C8")
    x3 = diapo("ig_x3_thymidine_doc", "National 2017 R : d'abord le document", "thymidine.html?vue=document&conclusions=false",
        "Un exercice du national 2017. On lit le document pas à pas. Des cellules de racine de fève, dans un milieu à thymidine radioactive, pendant un cycle. Ensuite, le chromosome en métaphase : les deux chromatides sont marquées, couvertes de grains noirs. Puis on transfère la plantule dans un milieu normal, pour un deuxième cycle. Regarde le chromosome en métaphase maintenant. Première consigne : décrire. Que vois-tu ?",
        "تمرين من le national deux mille dix-sept. نقراو le document خطوة بخطوة. خلايا ديال la racine ديال la fève، ف milieu فيه la thymidine radioactive، مدة cycle واحد. "
        "من بعد، le chromosome ف la métaphase: les deux chromatides marquées، فيهم نقط كحلين. من بعد كندوزو la plantule ل milieu normal، مدة cycle ثاني. "
        "شوف le chromosome ف la métaphase دابا. أول سؤال: نوصفو. شنو كتشوف؟",
        pts(("خلايا ديال la", {"moment": "cycle_1", "repere": "milieu"}), ("من بعد، le chromosome", {"moment": "metaphase_1", "repere": "chromosome_1"}),
            ("من بعد كندوزو", {"moment": "transfert"}), ("شوف le chromosome ف", {"moment": "metaphase_2", "repere": "chromosome_2"})),
        "National 2017 R : un cycle en milieu à thymidine radioactive, puis un cycle en milieu normal.", ["1re consigne : décrire les résultats."],
        "1er cycle (milieu radioactif) : les deux chromatides du chromosome métaphasique sont marquées. 2e cycle (milieu normal) : une chromatide marquée sur deux.",
        "Le document du national 2017 R", "La plantule de fève, le chromosome métaphasique après chaque cycle ; le 2e résultat sans légende",
        qcm("Après le 2e cycle en milieu normal, le chromosome métaphasique a :",
            ["ses deux chromatides marquées", "une chromatide marquée et une chromatide non marquée", "aucune chromatide marquée"], 1,
            "سؤال: من بعد le deuxième cycle ف milieu normal، le chromosome métaphasique شنو فيه؟"),
        reponses(1, ("مزيان! chromatide وحدة فيها نقط كحلين، والأخرى ما فيها والو: une chromatide marquée sur deux. هادا هو الوصف. دابا نشرحو علاش.",
                     "Oui : une chromatide couverte de grains noirs, l'autre sans grains : une chromatide marquée sur deux."),
                 {0: ("شوف مزيان: واش les deux chromatides فيهم نقط كحلين؟ قارن بيناتهم. عاود جرب.",
                      "Regarde bien : les deux chromatides ont-elles des grains noirs ? Compare les deux côtés. Réessaie.",
                      "لا، هادا كان من بعد le premier cycle. من بعد le deuxième: chromatide وحدة marquée، والأخرى لا.",
                      "Non : c'était après le 1er cycle. Après le 2e : une chromatide marquée, l'autre non."),
                  2: ("شوف مزيان: كاين نقط كحلين ف واحد الجيهة. عاود جرب.",
                      "Regarde bien : il y a des grains noirs d'un côté. Réessaie.",
                      "لا، chromatide وحدة باقا marquée: une chromatide marquée sur deux.",
                      "Non : une chromatide reste marquée : une chromatide marquée sur deux.")}), competences=TH)
    x3b = diapo("ig_x3b_cycle1", "Expliquer le 1er cycle", "thymidine.html?vue=document",
        "Deuxième consigne : expliquer. Commençons par le premier cycle. La thymidine radioactive n'entre que dans l'ADN, pendant la réplication. Pourquoi les deux chromatides sont-elles marquées ? Pense à l'ADN de chaque chromatide : un brin ancien, et un brin nouveau.",
        "دابا السؤال الثاني: expliquer. نبداو ب le premier cycle. la thymidine radioactive كتدخل غير ف l'A D N، ملي كتوقع la réplication. "
        "علاش les deux chromatides marquées؟ فكر ف l'A D N ديال كل chromatide: brin قديم، و brin جديد.",
        pts(("نبداو ب le premier", {"moment": "metaphase_1", "repere": "chromosome_1"})),
        "Expliquer le 1er cycle, en flèches, comme le barème.", ["La thymidine radioactive n'entre que dans l'ADN, à la réplication."],
        "Milieu radioactif → la thymidine entre dans l'ADN à la réplication → chaque molécule : un brin ancien + un brin nouveau radioactif → les deux chromatides marquées.",
        "Le 1er cycle : à toi d'expliquer", "Le chromosome métaphasique après le 1er cycle, ses deux chromatides marquées",
        qcm("Après le 1er cycle, les deux chromatides sont marquées parce que :",
            ["chaque molécule d'ADN garde un brin ancien et reçoit un brin nouveau radioactif : chaque chromatide a un brin radioactif",
             "la thymidine radioactive se fixe sur les protéines du chromosome",
             "une molécule d'ADN fille est toute radioactive, l'autre ne l'est pas"], 0,
            "سؤال: علاش les deux chromatides marquées من بعد le premier cycle؟",
            demo("نكتبو بحال le barème، بالflèches. milieu فيه la thymidine radioactive: la thymidine كتدخل ف l'A D N ف la réplication. "
                 "كل molécule fille: brin قديم ماشي radioactif، و brin جديد radioactif. كل chromatide فيها وحدة من هاد les molécules. "
                 "إذن les deux chromatides ديال le chromosome métaphasique marquées.",
                 [("milieu à thymidine radioactive → la thymidine entre dans l'ADN pendant la réplication (phase S)", "milieu فيه la thymidine"),
                  ("→ chaque molécule d'ADN fille : un brin ancien non radioactif + un brin nouveau radioactif", "كل molécule fille:"),
                  ("→ chaque chromatide contient une de ces molécules", "كل chromatide فيها"),
                  ("→ les deux chromatides du chromosome métaphasique sont radioactives", "إذن les deux chromatides")])),
        reponses(0, ("مزيان! كل molécule كيبقى فيها brin قديم، وكتاخد brin جديد radioactif. إذن كل chromatide فيها brin radioactif: les deux chromatides marquées.",
                     "Oui : chaque molécule fille garde un brin ancien et reçoit un brin nouveau radioactif ; chaque chromatide a donc un brin radioactif : les deux sont marquées."),
                 {1: ("la thymidine كتدخل غير ف l'A D N، ماشي ف les protéines. فين كتدخل؟ عاود جرب.",
                      "La thymidine n'entre que dans l'ADN, pas dans les protéines. Où entre-t-elle ? Réessaie.",
                      "لا، la thymidine كتدخل غير ف l'A D N، ف la réplication. كل molécule: brin قديم و brin جديد radioactif، إذن les deux chromatides marquées.",
                      "Non : elle n'entre que dans l'ADN, lors de la réplication. Chaque molécule : un brin ancien, un brin nouveau radioactif ; les deux chromatides sont marquées."),
                  2: ("يلا كانت molécule وحدة radioactive والأخرى لا، شحال من chromatide غادي تكون marquée؟ قارن مع le document. عاود جرب.",
                      "Si une molécule était toute radioactive et l'autre non, combien de chromatides seraient marquées ? Compare avec le document. Réessaie.",
                      "لا، هادي la conservative: كانت غادي تعطي chromatide وحدة marquée. le document فيه جوج: كل molécule فيها brin radioactif.",
                      "Non : c'est le modèle conservatif, il donnerait une seule chromatide marquée. Le document en montre deux : chaque molécule a un brin radioactif.")}),
        competences=TH)
    x3c = diapo("ig_x3c_cycle2", "Expliquer le 2e cycle", "thymidine.html?vue=document",
        "Maintenant le deuxième cycle, dans un milieu normal, sans radioactivité. Regarde le résultat : une chromatide marquée sur deux. Pourquoi ? Suis chaque brin : que lui arrive-t-il à la deuxième réplication ?",
        "دابا le deuxième cycle، ف milieu normal، بلا radioactivité. شوف النتيجة: une chromatide marquée sur deux. علاش؟ تبع كل brin: شنو كيوقع ليه ف la réplication الثانية؟",
        pts(("دابا le deuxième cycle", {"moment": "transfert"}), ("شوف النتيجة:", {"moment": "metaphase_2", "repere": "chromosome_2"}),
            ("تبع كل brin", {"repere": "chromatide_marquee"})),
        "Expliquer le 2e cycle, brin par brin.", ["Milieu normal : le brin nouveau n'est pas radioactif."],
        "Milieu normal → chaque brin sert de modèle à un brin nouveau non radioactif → une molécule garde le brin radioactif, l'autre non → une chromatide marquée sur deux.",
        "Le 2e cycle : à toi d'expliquer", "Le chromosome métaphasique après le 2e cycle : une chromatide marquée, l'autre non",
        qcm("Après le 2e cycle en milieu normal, une seule chromatide sur deux est marquée parce que :",
            ["la radioactivité disparaît de la moitié de l'ADN avec le temps",
             "chaque brin sert de modèle à un brin nouveau non radioactif : une molécule garde le brin radioactif, l'autre n'en a aucun",
             "le brin radioactif est détruit pendant la mitose"], 1,
            "سؤال: علاش chromatide وحدة marquée من جوج، من بعد le deuxième cycle؟",
            demo("نكملو بالflèches. ف milieu normal، le brin جديد ماشي radioactif. كل brin ديال la molécule كيولي modèle. "
                 "molécule: brin radioactif و brin جديد، إذن radioactive. والأخرى: brin قديم و brin جديد، إذن ماشي radioactive. "
                 "إذن ف كل chromosome métaphasique، une chromatide marquée sur deux.",
                 [("milieu normal → le brin nouveau n'est pas radioactif", "ف milieu normal،"),
                  ("→ chaque brin de la molécule sert de modèle (réplication semi-conservative)", "كل brin ديال"),
                  ("→ une molécule : brin radioactif + brin nouveau → radioactive", "molécule: brin radioactif"),
                  ("→ l'autre : brin ancien non radioactif + brin nouveau → non radioactive", "والأخرى: brin قديم"),
                  ("→ une chromatide marquée sur deux dans chaque chromosome métaphasique", "إذن ف كل")])),
        reponses(1, ("مزيان! كل brin كيولي modèle ل brin جديد ماشي radioactif. molécule فيها le brin radioactif: marquée. والأخرى ما فيهاش: ماشي marquée. إذن une chromatide marquée sur deux.",
                     "Oui : chaque brin sert de modèle à un brin nouveau non radioactif. Une molécule garde le brin radioactif (chromatide marquée), l'autre n'en a aucun (chromatide non marquée)."),
                 {0: ("le brin radioactif كيبقى. تبع شنو كيوقع ف la réplication. عاود جرب.",
                      "Le brin radioactif ne disparaît pas. Suis ce qui se passe à la réplication. Réessaie.",
                      "لا، la radioactivité كتبقى. ف la réplication، كل brin كياخد brin جديد ماشي radioactif: molécule وحدة باقا فيها le brin radioactif، والأخرى لا.",
                      "Non : la radioactivité ne disparaît pas. À la réplication, chaque brin reçoit un brin nouveau non radioactif : une molécule garde le brin radioactif, l'autre non."),
                  2: ("يلا مشا le brin radioactif، واش غادي تبقى chromatide marquée؟ عاود جرب.",
                      "Si le brin radioactif était détruit, resterait-il une chromatide marquée ? Réessaie.",
                      "لا، حتى brin ما كيمشي. كل brin كيولي modèle: molécule فيها le brin radioactif، والأخرى لا. إذن chromatide وحدة marquée.",
                      "Non : aucun brin n'est détruit. Chaque brin sert de modèle : une molécule a le brin radioactif, l'autre non : une chromatide marquée sur deux.")}),
        competences=TH)
    x3d = diapo("ig_x3d_schema", "Le schéma demandé, puis la conclusion", "thymidine.html?vue=experience&diapo=x3d_schema",
        "Le barème demande aussi un schéma. Le voici : chaque molécule a deux brins. Bleu : brin ancien. Rouge : brin radioactif. Blanc : brin nouveau non radioactif. Premier cycle : deux molécules, chacune un brin bleu et un brin rouge. Deuxième cycle : une molécule bleue et blanche, et une molécule blanche et rouge. Maintenant la conclusion : ces résultats montrent que la réplication est… ?",
        "le barème كيطلب حتى schéma. هادا هو: كل molécule فيها جوج brins. الزرق: brin قديم. الأحمر: brin radioactif. الأبيض: brin جديد ماشي radioactif. "
        "le premier cycle: جوج molécules، كل وحدة فيها brin زرق و brin حمر. le deuxième cycle: molécule فيها الزرق و الأبيض، و molécule فيها الأبيض و الأحمر. "
        "دابا الخلاصة: هاد النتائج كتبين بلي la réplication est... شنو؟",
        pts(("هادا هو:", {"moment": "replication_1", "repere": "molecules"}), ("le premier cycle:", {"moment": "metaphase_1"}),
            ("le deuxième cycle:", {"moment": "replication_2", "repere": "molecules"})),
        "Le schéma des brins, puis la conclusion.", ["bleu : brin ancien ; rouge : brin radioactif ; blanc : brin nouveau non radioactif"],
        "Schéma : 1er cycle, deux molécules bleu + rouge ; 2e cycle, une molécule bleu + blanc et une blanc + rouge. Conclusion : la réplication est semi-conservative.",
        "Le schéma des brins (national 2017 R)", "Les molécules d'ADN du chromosome suivi, cycle après cycle, leurs brins en couleur",
        qcm("Ces résultats montrent que la réplication de l'ADN est :", ["conservative", "semi-conservative", "dispersive"], 1,
            "سؤال: هاد النتائج كتبين بلي la réplication de l'A D N est... شنو؟"),
        reponses(1, ("مزيان! كل molécule fille كيبقى فيها brin من la molécule mère: la réplication est semi-conservative. هادي هي الخلاصة اللي كتكتب ف الآخر.",
                     "Oui : chaque molécule fille garde un brin de la molécule mère : la réplication est semi-conservative."),
                 {0: ("la conservative: molécule فيها غير les brins القدام، و molécule فيها غير les brins الجداد. واش هادا اللي ف le schéma؟ عاود جرب.",
                      "Conservative : une molécule toute ancienne, une toute nouvelle. Est-ce ce que montre le schéma ? Réessaie.",
                      "لا، ف le schéma، كل molécule فيها brin قديم و brin جديد: semi-conservative.",
                      "Non : dans le schéma, chaque molécule a un brin ancien et un brin nouveau : semi-conservative."),
                  2: ("la dispersive: القديم و الجديد مخلطين ف كل brin. واش هادا اللي ف le schéma؟ عاود جرب.",
                      "Dispersive : ancien et nouveau mélangés dans chaque brin. Est-ce ce que montre le schéma ? Réessaie.",
                      "لا، les brins ماشي مخلطين: كل brin يا قديم يا جديد. كل molécule: brin قديم و brin جديد: semi-conservative.",
                      "Non : les brins ne sont pas mélangés ; chaque molécule a un brin ancien et un brin nouveau : semi-conservative.")}),
        competences=TH)
    for s in (x3, x3d): s["concentration"]["demarrer"] = "reset"
    nouvelles += [x3, x3b, x3c, x3d]
    fait.append("ig_x3_thymidine_doc, ig_x3b_cycle1, ig_x3c_cycle2, ig_x3d_schema (national 2017 R)")

# ── place dans la partie VIII, dans l'ordre ──
ORDRE = ["ig_x1_restitution", "ig_x1b_corrige", "ig_x1c_metaphase", "ig_x1d_corrige_metaphase", "ig_x2_exercice", "ig_x2b_expliquer",
         "ig_x3_thymidine_doc", "ig_x3b_cycle1", "ig_x3c_cycle2", "ig_x3d_schema"]
if nouvelles:
    p8 = ACT["ig_partie8"]
    tous = {s["id"]: s for s in p8["slides"] + nouvelles}
    p8["slides"] = [tous[i] for i in ORDRE] + [s for s in p8["slides"] if s["id"] not in ORDRE]
    p8["title"] = "VIII. Comme à l'examen, pas à pas"
    p8["duration_minutes"] = 50
    m["estimated_minutes"] = sum(a.get("duration_minutes", 0) for a in m["activities"])

# ── séances : la restitution ferme la séance 7 ; une séance 8 pour les exercices du national et le bilan ──
if not any(se["id"] == "ig_s8" for se in m["seances"]):
    s7 = next(se for se in m["seances"] if se["id"] == "ig_s7")
    b3 = s7["blocs"][-1]
    ancien = copy.deepcopy(b3)
    b3.update(titre="Comme à l'examen : la restitution, QCM posés puis corrigés", slide_ids=ORDRE[:4])
    b3["cahier"] = [{"texte": "Restitution : lire jusqu'au dernier mot, éliminer chaque leurre avec sa raison, répondre avec les mots du cours."},
                    {"texte": "G1 : chaque chromosome a une chromatide, non condensé. Métaphase : deux chromatides, chacune une molécule d'ADN à deux brins."}]
    b3["retrouver"] = {"prompt": "Cahier fermé : en métaphase, de quoi est formé chaque chromosome ?",
                       "attendu": "De deux chromatides, chacune formée d'une molécule d'ADN à deux brins.", "competence_id": "C8",
                       "enonce_dit": "شوف هاد السؤال: cahier fermé، ف la métaphase، chaque chromosome est formé de quoi ?"}
    s7["titre"] = "Séance 7 — Le mécanisme de la réplication, et la restitution"
    m["seances"].append({"id": "ig_s8", "titre": "Séance 8 — Les exercices du national pas à pas, et le bilan", "blocs": [
        {"id": "ig_s8_b1", "titre": "La courbe de l'ADN : décrire, puis expliquer", "slide_ids": ORDRE[4:6],
         "cahier": [{"texte": "Décrire : ce qu'on voit, avec les valeurs (de 8 à 14 h, la quantité d'ADN augmente de 3 à 6 UA : elle double)."},
                    ancien["cahier"][1]],
         "retrouver": ancien["retrouver"],
         "exercice": {"type": "qcm", "prompt": "« De 0 à 8 h, la quantité d'ADN reste constante, 3 UA. » Cette phrase est…",
                      "choices": ["une description", "une explication", "une conclusion"], "correct": 0,
                      "explanation": "Elle dit ce qu'on voit, avec la valeur : c'est une description.",
                      "enonce_dit": "شوف هاد السؤال: de zéro à huit heures، la quantité d'ADN reste constante، trois U A. هاد الجملة شنو هي؟"}},
        {"id": "ig_s8_b2", "titre": "La thymidine radioactive (national 2017 R), pas à pas", "slide_ids": ORDRE[6:10],
         "cahier": [{"texte": "1er cycle (thymidine radioactive) : chaque molécule = un brin ancien + un brin radioactif → les deux chromatides marquées."},
                    {"texte": "2e cycle (milieu normal) : chaque brin sert de modèle à un brin non radioactif → une chromatide marquée sur deux : réplication semi-conservative."}],
         "retrouver": {"prompt": "Cahier fermé : pourquoi, après le 2e cycle en milieu normal, une chromatide sur deux seulement est-elle marquée ?",
                       "attendu": "Chaque brin sert de modèle à un brin nouveau non radioactif : une molécule garde le brin radioactif, l'autre n'en a aucun.",
                       "competence_id": "C7",
                       "enonce_dit": "شوف هاد السؤال: cahier fermé، علاش من بعد le deuxième cycle، chromatide وحدة marquée من جوج؟"},
         "exercice": {"type": "qcm", "prompt": "Si la réplication était conservative, après le 1er cycle en milieu radioactif…",
                      "choices": ["les deux chromatides seraient marquées", "une seule chromatide serait marquée", "aucune chromatide ne serait marquée"], "correct": 1,
                      "explanation": "Conservative : une molécule toute ancienne (non marquée), une toute nouvelle (marquée) : une seule chromatide marquée.",
                      "enonce_dit": "شوف هاد السؤال: يلا كانت la réplication conservative، من بعد le premier cycle، شحال من chromatide غادي تكون marquée؟"}},
        {"id": "ig_s8_b3", "titre": "Le bilan du chapitre", "slide_ids": ["ig_b1_bilan", "ig_b2_carte"],
         "cahier": ancien["cahier"][2:], "retrouver": {"prompt": "Cahier fermé : cite les quatre questions du chapitre et leur réponse en une phrase.",
                                                       "attendu": "L'information génétique est dans le noyau ; elle passe aux cellules filles par la mitose ; elle est portée par l'ADN ; elle se copie par réplication semi-conservative.",
                                                       "competence_id": "C8",
                                                       "enonce_dit": "شوف هاد السؤال: cahier fermé، عاود الربعة ديال الأسئلة ديال le chapitre، و الجواب ديال كل سؤال ف جملة."},
         "exercice": ancien["exercice"]}]})
    fait.append("séances : ig_s7_b3 recoupé, ig_s8 (trois blocs)")

# ── compétences ──
C = {c["id"]: c for c in m["competences"]}
for cid, ids in (("C3", ["ig_x2_exercice", "ig_x2b_expliquer"]), ("C7", ORDRE[6:10]), ("C8", ORDRE)):
    for i in ids:
        if i not in C[cid]["slide_ids"]: C[cid]["slide_ids"].append(i)
ordre_global = [s["id"] for a in m["activities"] for s in a["slides"]]
for c in m["competences"]:
    c["slide_ids"] = sorted(c["slide_ids"], key=ordre_global.index)

json.dump(m, open(F, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print("\n".join(fait) or "rien à faire")
