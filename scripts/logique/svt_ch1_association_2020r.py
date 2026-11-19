"""SVT ch1, national 2020 rattrapage, question III : « Reliez chaque phénomène à la réaction bilan qui lui convient ».
Les trois QCM de `svt_ch1_appariement.py` (le_x1d_reactions, le_x1e_reactions_c, le_x1f_reactions_krebs) deviennent UNE
question d'association (19 novembre 2026, demande de l'utilisateur : « pour les questions d'association, ne pas les
transformer en QCM ; les mettre en association avec un feedback à chaque réponse, correcte ou fausse »).
Écrit le cours en ligne et sa copie en attente. Usage : python -X utf8 scripts/logique/svt_ch1_association_2020r.py"""
import json
from pathlib import Path

R = Path(__file__).resolve().parents[2]
DECK = "svt_ch1_reactions_responsables_liberation_energie"
GARDE, RETIRES = "le_x1d_reactions", ["le_x1e_reactions_c", "le_x1f_reactions_krebs"]

GAUCHE = [{"id": "1", "texte": "La glycolyse"}, {"id": "2", "texte": "Le cycle de Krebs"},
          {"id": "3", "texte": "La fermentation lactique"}, {"id": "4", "texte": "La fermentation alcoolique"}]
DROITE = [
    {"id": "a", "texte": "C₆H₁₂O₆ + 2 ADP + 2 Pi → 2 CH₃CH₂OH + 2 CO₂ + 2 ATP"},
    {"id": "b", "texte": "C₆H₁₂O₆ + 2 ADP + 2 Pi → 2 CH₃CHOHCOOH + 2 ATP"},
    {"id": "c", "texte": "C₆H₁₂O₆ + 2 ADP + 2 Pi + 2 NAD⁺ → 2 CH₃COCOOH + 2 ATP + 2 NADH,H⁺"},
    {"id": "d", "texte": "CH₃COCOOH + 2 ATP → CH₃COOH + 2 ADP + 2 Pi"},
    {"id": "e", "texte": "CH₃CO-SCoA + 3 NAD⁺ + 3 H₂O + FAD + GDP + Pi → 2 CO₂ + HSCoA + 3 NADH,H⁺ + FADH₂ + GTP"},
]
COUPLES = {"1": "c", "2": "e", "3": "b", "4": "a"}

# le nom du phénomène (écrit, dit)
PHEN = {"1": ("la glycolyse", "la glycolyse"), "2": ("le cycle de Krebs", "le cycle de Krebs"),
        "3": ("la fermentation lactique", "la fermentation lactique"), "4": ("la fermentation alcoolique", "la fermentation alcoolique")}
# ce que fait la réaction (écrit, dit)
DONNE = {
    "a": ("a donne de l'éthanol (CH₃CH₂OH) et du CO₂", "A كتعطي l'éthanol و CO deux"),
    "b": ("b donne l'acide lactique (CH₃CHOHCOOH)", "B كتعطي l'acide lactique"),
    "c": ("c part du glucose et donne l'acide pyruvique (CH₃COCOOH) et du NADH,H⁺", "C كتبدا من le glucose، وكتعطي l'acide pyruvique و NADH,H plus"),
    "d": ("d consomme de l'ATP et donne l'acide acétique (CH₃COOH)", "D كتاكل ATP، وكتعطي l'acide acétique"),
    "e": ("e part de l'acétyl-CoA et donne du CO₂, du NADH,H⁺ et du FADH₂", "E كتبدا من l'acétyl-CoA، وكتعطي CO deux و NADH,H plus و FADH deux"),
}
# l'indice pour le phénomène, sans donner la lettre (écrit, dit)
INDICE = {
    "1": ("La glycolyse part du glucose et donne l'acide pyruvique : cherche la réaction qui fait ça.",
          "la glycolyse كتبدا من le glucose، وكتعطي l'acide pyruvique. شوف أشمن réaction اللي كتدير هادشي."),
    "2": ("Le cycle de Krebs part de l'acétyl-CoA, dans la matrice, et libère du CO₂ : cherche cette réaction.",
          "le cycle de Krebs كيبدا من l'acétyl-CoA، فla matrice، وكيخرج CO deux. شوف أشمن réaction اللي كتدير هادشي."),
    "3": ("La fermentation lactique donne l'acide lactique : cherche-le après la flèche.",
          "la fermentation lactique كتعطي l'acide lactique. شوف فين كاين، من بعد la flèche."),
    "4": ("La fermentation alcoolique donne de l'éthanol et du CO₂ : cherche-les après la flèche.",
          "la fermentation alcoolique كتعطي l'éthanol و CO deux. شوف فين كاينين، من بعد la flèche."),
}
JUSTE = {
    "1-c": ("c part du glucose et donne 2 acides pyruviques, 2 ATP et 2 NADH,H⁺ : c'est la glycolyse. (1 ; c)",
            "مزيان! C كتبدا من le glucose، وكتعطي l'acide pyruvique، و ATP، و NADH,H plus. هادي la glycolyse."),
    "2-e": ("e part de l'acétyl-CoA et donne 2 CO₂, 3 NADH,H⁺, FADH₂ et GTP : c'est le cycle de Krebs, dans la matrice. (2 ; e)",
            "مزيان! E كتبدا من l'acétyl-CoA، وكتعطي CO deux، و NADH,H plus، و FADH deux. هادا le cycle de Krebs."),
    "3-b": ("b donne l'acide lactique (CH₃CHOHCOOH) : c'est la fermentation lactique. (3 ; b)",
            "مزيان! B كتعطي l'acide lactique. و l'acide lactique كتعطيه la fermentation lactique."),
    "4-a": ("a donne de l'éthanol et du CO₂ : c'est la fermentation alcoolique. (4 ; a)",
            "مزيان! A كتعطي l'éthanol و CO deux. هادي la fermentation alcoolique."),
}


def retours():
    out = {}
    for g in COUPLES:
        for d in "abcde":
            k = f"{g}-{d}"
            if COUPLES[g] == d:
                t, dit = JUSTE[k]
                out[k] = {"juste": True, "texte": t, "dit": dit}
                continue
            ecrit_d, dit_d = DONNE[d]
            nom_e, nom_d = PHEN[g]
            if d == "d":
                t = f"Pas encore : {ecrit_d} ; elle ne correspond à aucun des quatre phénomènes. {INDICE[g][0]}"
                dit = f"{dit_d}: ما كتمشي مع حتى phénomène، هي اللي زايدة. {INDICE[g][1]}"
            else:
                t = f"Pas encore : {ecrit_d}, ce n'est pas {nom_e}. {INDICE[g][0]}"
                dit = f"{dit_d}، ماشي {nom_d}. {INDICE[g][1]}"
            out[k] = {"juste": False, "texte": t, "dit": dit}
    return out


QUESTION = {
    "type": "association",
    "prompt": "Reliez chaque phénomène à la réaction bilan qui lui convient. (2020 R, 1 pt)",
    "timeout_seconds": 180,
    "enonce_dit": "سؤال: كل phénomène، مع أشمن réaction bilan كيمشي؟",
    "association": {
        "gauche": GAUCHE, "droite": DROITE, "couples": COUPLES, "melanger": False, "essais": 2,
        "retours": retours(),
        "bilan": {
            "texte": "d est la réaction de trop : elle ne correspond à aucun des quatre phénomènes.",
            "dit": "إذن فالورقة كنكتبو: un، C. deux، E. trois، B. quatre، A. و D هي اللي زايدة، ما كتمشي مع حتى phénomène.",
        },
    },
}

MIXED = ("دابا سؤال آخر ديال الدرس، من deux mille vingt: نربطو كل phénomène ب la réaction bilan ديالو، وعليه un point. "
         "عندنا ربعة ديال les phénomènes: la glycolyse، le cycle de Krebs، la fermentation lactique، و la fermentation alcoolique. "
         "وعندنا خمسة ديال les réactions، من A حتى ل E. يعني كاينة وحدة زايدة، ما كتمشي مع حتى phénomène. "
         "الطريقة: ما غاديش نقراو la réaction كاملة. نشوفو من فين كتبدا، وشنو كتعطي، من بعد la flèche. "
         "مثلا، l'éthanol و CO deux، كيجيو من la fermentation alcoolique. "
         "دابا نتا: كل phénomène، مع أشمن réaction كيمشي؟")
FR = ("Une autre question de restitution, 2020 R : relier chaque phénomène à sa réaction bilan, un point. "
      "Quatre phénomènes : la glycolyse, le cycle de Krebs, la fermentation lactique et la fermentation alcoolique. "
      "Cinq réactions, de a à e : une est de trop. La méthode : on ne lit pas toute la réaction, on regarde d'où elle part "
      "et ce qu'elle donne, après la flèche. Par exemple, l'éthanol et le CO₂, c'est la fermentation alcoolique. "
      "À toi : relie chaque phénomène à sa réaction, en glissant l'un sur l'autre ou en touchant l'un puis l'autre.")


def diapo(ancienne):
    s = {
        "id": GARDE, "slide_type": "evaluation", "title": "Relier phénomène et réaction bilan (2020 R)",
        "screen_content": {
            "lead": "2020 R : « Reliez chaque phénomène à la réaction bilan qui lui convient » (1 pt). Quatre phénomènes, cinq réactions : une est de trop.",
            "bullets": ["La méthode : d'où part la réaction, et ce qu'elle donne (après la flèche)."],
            "student_trace": "Relier une réaction à son phénomène : regarder d'où elle part et ce qu'elle donne (après la flèche). Réponse : (1 ; c) (2 ; e) (3 ; b) (4 ; a) ; d est de trop.",
        },
        "visual": {
            "kind": "simulation",
            "url": "/media/simulations/svt/reactions_responsables_liberation_energie-tableau/national.html?vue=reactions&cacher=a_produit",
            "caption": "Examen 2020 R : relier chaque phénomène à sa réaction bilan",
            "alt": "Les quatre phénomènes à gauche, les cinq réactions a à e à droite ; après la réponse de l'élève, ce que donne chaque réaction est souligné et les quatre liens sont tracés, d reste seule",
        },
        "speech_text": {"fr": FR, "mixed": MIXED},
        "concentration": {
            "demarrer": "reset",
            "pointage": [
                {"mot": "دابا سؤال آخر", "commande": "play_until", "parametres": {"moment": "enonce"}},
                {"mot": "عندنا ربعة ديال les phénomènes", "commande": "play_until", "parametres": {"moment": "phenomenes"}},
                {"mot": "وعندنا خمسة ديال les réactions", "commande": "play_until", "parametres": {"moment": "reactions"}},
                {"mot": "نشوفو من فين كتبدا", "repere": "reactions"},
            ],
            "cahier": "Relier une réaction à son phénomène : regarder d'où elle part et ce qu'elle donne (après la flèche). Éthanol + CO₂ → fermentation alcoolique.",
            "apres_reponse": {
                "question": "q", "sim_avant": {"conclusions": False}, "duree_s": 8,
                "etapes": [{"commande": "set_parameters", "parametres": {"conclusions": True}},
                           {"commande": "play_until", "parametres": {"moment": "couples"}}],
            },
        },
        "question": QUESTION,
        "competence_ids": ["C7", "C3", "C5"],
    }
    if ancienne.get("stable_id"):
        s["stable_id"] = ancienne["stable_id"]
    return s


def convertir(m):
    for a in m["activities"]:
        ids = [s["id"] for s in a["slides"]]
        if GARDE in ids:
            i = ids.index(GARDE)
            a["slides"][i] = diapo(a["slides"][i])
            a["slides"] = [s for s in a["slides"] if s["id"] not in RETIRES]
    for c in m.get("competences") or []:
        ids = c.get("slide_ids") or []
        if any(x in ids for x in RETIRES):
            ids = [x for x in ids if x not in RETIRES]
            if GARDE not in ids:
                ids.append(GARDE)
            c["slide_ids"] = ids
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
