"""SVT ch3, national 2024 normale, question IV : « Recopier les couples … et adresser à chaque numéro de l'ensemble A la
lettre correspondante dans l'ensemble B ». Les deux QCM de `passe2b_svt_ch3_associer.py` (ig_x1e_associer : « l'ADN
polymérase va avec quelle proposition ? », ig_x1f_associer_couples : « les couples de 2 et 3 ») deviennent UNE question
d'association (19 novembre 2026, demande de l'utilisateur : « pour les questions d'association, ne pas les transformer en
QCM ; les mettre en association avec un feedback à chaque réponse, correcte ou fausse »).
Le cours garde son cadre : les trois éléments du chapitre (1 à 3) et les propositions a, d, e, comme la simulation
`documents.html?vue=associer` ; le ribosome (4, b) et c reviennent au chapitre 4.
Écrit le cours en ligne et sa copie en attente. Usage : python -X utf8 scripts/logique/svt_ch3_association_2024n.py"""
import json
from pathlib import Path

R = Path(__file__).resolve().parents[2]
DECK = "svt_ch3_notion_information_genetique"
GARDE, RETIRES = "ig_x1e_associer", ["ig_x1f_associer_couples"]

QUESTION = {
    "type": "association",
    "prompt": "Recopier les couples (1, ...), (2, ...), (3, ...) et adresser à chaque numéro de l'ensemble A la lettre correspondante dans l'ensemble B. (2024 N)",
    "timeout_seconds": 150,
    "enonce_dit": "سؤال: كل numéro ديال l'ensemble A، مع أشمن lettre ف l'ensemble B؟",
    "association": {
        "gauche": [{"id": "1", "texte": "ADN polymérase."}, {"id": "2", "texte": "Centromère."}, {"id": "3", "texte": "Nucléosome."}],
        "droite": [{"id": "a", "texte": "Complexe formé par l'association Histones – ADN."},
                   {"id": "d", "texte": "Structure reliant les deux chromatides du même chromosome."},
                   {"id": "e", "texte": "Enzyme qui intervient dans la réplication de l'ADN."}],
        "couples": {"1": "e", "2": "d", "3": "a"},
        "melanger": False,
        "essais": 2,
        "retours": {
            "1-e": {"juste": True, "texte": "L'ADN polymérase est l'enzyme qui intervient dans la réplication : à la fourche, elle allonge le brin nouveau. (1, e)",
                    "dit": "مزيان! l'ADN polymérase enzyme، و كتخدم ف la réplication: ف la fourche، كتزيد le brin nouveau."},
            "1-a": {"juste": False, "texte": "Histones et ADN : c'est un autre élément de l'ensemble A. Regarde la première figure : que fait l'enzyme à la fourche ? Réessaie.",
                    "dit": "les histones و l'A D N، هادي حاجة أخرى ف l'ensemble A. شوف la figure اللولة: l'enzyme شنو كتدير ف la fourche؟ عاود جرب."},
            "1-d": {"juste": False, "texte": "Ce qui relie les deux chromatides est un autre élément de l'ensemble A. Où travaille l'ADN polymérase ? Regarde la fourche. Réessaie.",
                    "dit": "اللي كيجمع les deux chromatides عنصر آخر ف l'ensemble A. l'ADN polymérase فين كتخدم؟ شوف la fourche. عاود جرب."},
            "2-d": {"juste": True, "texte": "Le centromère relie les deux chromatides du même chromosome. (2, d)",
                    "dit": "مزيان! le centromère كيربط les deux chromatides ديال نفس le chromosome."},
            "2-a": {"juste": False, "texte": "a parle d'histones et d'ADN : c'est un autre élément. Regarde le chromosome : le point du milieu relie les deux chromatides. Quelle proposition parle de chromatides ?",
                    "dit": "a فيها les histones و l'A D N: هادي حاجة أخرى. شوف le chromosome: النقطة اللي ف الوسط كتجمع جوج chromatides. أشمن proposition فيها chromatides؟"},
            "2-e": {"juste": False, "texte": "e est une enzyme de la réplication : le centromère n'est pas une enzyme. Regarde le chromosome : que relie le point du milieu ?",
                    "dit": "e هي enzyme ديال la réplication، و le centromère ماشي enzyme. شوف le chromosome: النقطة اللي ف الوسط شنو كتجمع؟"},
            "3-a": {"juste": True, "texte": "Le nucléosome est formé par l'association de l'ADN et des histones. (3, a)",
                    "dit": "مزيان! le nucléosome فيه l'A D N و les histones."},
            "3-d": {"juste": False, "texte": "d parle des deux chromatides d'un chromosome : c'est un autre élément. Regarde le nucléosome : de quoi est-il fait ?",
                    "dit": "d فيها les deux chromatides: هادا عنصر آخر. شوف le nucléosome: شنو فيه؟"},
            "3-e": {"juste": False, "texte": "e est une enzyme de la réplication : le nucléosome n'est pas une enzyme. Regarde de quoi il est fait.",
                    "dit": "e هي enzyme ديال la réplication، و le nucléosome ماشي enzyme. شوف شنو فيه."},
        },
        "bilan": {"texte": "Sur la copie, on écrit seulement les couples.",
                  "dit": "ف الورقة نكتبو: un، e. deux، d. trois، a. كنكتبو غير les couples."},
    },
}


def convertir(m):
    for a in m["activities"]:
        ids = [s["id"] for s in a["slides"]]
        if GARDE not in ids:
            continue
        s = a["slides"][ids.index(GARDE)]
        s["title"] = "Associer, comme au national 2024 N"
        s["screen_content"]["lead"] = "National 2024 N : relie chaque élément de l'ensemble A à sa proposition de l'ensemble B."
        s["screen_content"]["bullets"] = ["1. ADN polymérase ; 2. Centromère ; 3. Nucléosome.", "a, d, e : lis chaque proposition jusqu'au dernier mot."]
        s["speech_text"]["fr"] = s["speech_text"]["fr"].replace(
            "Commençons par le numéro un : l'ADN polymérase va avec quelle lettre ?", "À toi : relie chaque numéro à sa lettre.")
        s["speech_text"]["mixed"] = s["speech_text"]["mixed"].replace(
            "نبداو ب le numéro un: l'ADN polymérase، مع أشمن lettre؟", "دابا نتا: كل numéro، مع أشمن lettre؟")
        c = s["concentration"]
        c["pointage"] = [p for p in c["pointage"] if p.get("mot") != "نبداو ب le numéro"]
        c["apres_reponse"] = {"question": "q", "sim_avant": {"conclusions": False}, "duree_s": 8,
                              "etapes": [{"commande": "set_parameters", "parametres": {"conclusions": True}},
                                         {"commande": "play_until", "parametres": {"moment": "couples"}},
                                         {"repere": "reponse"}]}
        c.pop("reponses", None)
        s["question"] = QUESTION
        s["competence_ids"] = ["C7", "C8", "C2"]
        s["visual"]["alt"] = ("À gauche, l'ADN polymérase sur une fourche, un chromosome à deux chromatides, un fil de nucléosomes ; "
                              "à droite, les propositions a, d, e ; après la réponse, les liens (1, e), (2, d), (3, a) et la réponse comme le barème")
        a["slides"] = [x for x in a["slides"] if x["id"] not in RETIRES]
    for cp in m.get("competences") or []:
        ids = cp.get("slide_ids") or []
        if any(x in ids for x in RETIRES):
            ids = [x for x in ids if x not in RETIRES]
            if GARDE not in ids:
                ids.append(GARDE)
            cp["slide_ids"] = ids
    for se in m.get("seances") or []:
        for b in se.get("blocs") or []:
            if b.get("slide_ids"):
                b["slide_ids"] = [x for x in b["slide_ids"] if x not in RETIRES]
    return m


if __name__ == "__main__":
    for p in (R / f"backend/data/courses/{DECK}.json", R / f"backend/data/courses/en_attente/{DECK}.json"):
        m = convertir(json.load(open(p, encoding="utf-8")))
        p.write_bytes((json.dumps(m, ensure_ascii=False, indent=2) + chr(10)).encode("utf-8"))
        print("écrit", p.relative_to(R))
