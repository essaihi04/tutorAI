# Exercice SVT ch. 2 (rôle du muscle strié squelettique) — niveau facile : légender un sarcomère.
# Entraîne : légender le schéma du bac en partant des stries Z (strie Z, actine, myosine, bande claire I, bande sombre A,
# zone H, accolade « sarcomère »), réciter la définition du sarcomère, relier chaque bande à ses filaments, et dire
# QUALITATIVEMENT ce qui raccourcit à la contraction (lecture de schéma, sans tableau de mesures : les mesures et le
# glissement chiffré sont dans svt_ex_ch2_glissement_1).
# Sources comparées (lecture seule, rien de copié) :
# - exploration du cours (cas_types « legender » et « qcm_sarcomere » ; pieges « zone H / bande sombre »,
#   « sarcomère délimité par la bande sombre » ; a_ne_pas_dire « unité du muscle », « les filaments raccourcissent » ;
#   exclus : strie M, titine, isotrope/anisotrope : non légendés) ;
# - nationaux : 2021 N (électronographie à légender, 5 légendes, 1,25 pt) et 2023 R (1 pt) ; QCM « raccourcissement »
#   2017 N, 2020 R, 2022 N, 2024 N — on garde la forme (numéros à nommer, QCM), pas leurs documents ;
# - séries en ligne : recherche faite (cours moutamadris BIOF « sarcomère … délimité par deux stries Z », recueil Charif
#   Al Idrissi, dyrassa PDF 8, alloschool) mais pages inaccessibles depuis cette session (réseau refusé) : seuls les
#   extraits du moteur de recherche ont été lus.
# Le schéma suit les valeurs de sarcomere.html (actine 1,0 µm, myosine 1,5 µm, sarcomère relâché 2,5 µm) ; aucune
# valeur n'est demandée. L'exercice semblable : sarcomère plus court (2,2 µm) et numéros dans un autre ordre.
import sys
from _commun_svt import rep, qcm_facile, vrai_faux, association, ecrire

SIM_C = "/media/simulations/svt/role_muscle_strie_squelettique-tableau/sarcomere.html?vue=construire&attente=1"
SIM_K = "/media/simulations/svt/role_muscle_strie_squelettique-tableau/sarcomere.html?vue=contraction&attente=1"
SIM_S = "/media/simulations/svt/role_muscle_strie_squelettique-tableau/structure.html?attente=1"


def schema(L, num, titre):
    """Sarcomère de longueur L (µm), avec le début des sarcomères voisins ; num = {élément: numéro}."""
    k, cx = 3.0, 6.0
    zl, zr = cx - L / 2 * k, cx + L / 2 * k
    m0, m1 = cx - 0.75 * k, cx + 0.75 * k          # myosine 1,5 µm, fixe au centre
    al, ar = zl + 1.0 * k, zr - 1.0 * k            # bouts des actines (1,0 µm depuis chaque strie Z)
    vg, vd = zl - (L / 2 - 0.75) * k, zr + (L / 2 - 0.75) * k   # myosines des sarcomères voisins
    r = lambda v: round(v, 2)
    ya1, ya2, ym0, ym1 = 3.2, 4.8, 3.65, 4.35
    el = [
        # myosine du sarcomère et bouts des myosines voisines
        {"f": "rect", "de": [r(m0), ym0], "a": [r(m1), ym1], "couleur": "bleu", "remplir": "bleu"},
        {"f": "rect", "de": [0.15, ym0], "a": [r(vg), ym1], "couleur": "bleu", "remplir": "bleu"},
        {"f": "rect", "de": [r(vd), ym0], "a": [11.85, ym1], "couleur": "bleu", "remplir": "bleu"},
        # stries Z
        {"f": "ligne", "pts": [[r(zl), 2.75], [r(zl), 5.25]], "epais": True},
        {"f": "ligne", "pts": [[r(zr), 2.75], [r(zr), 5.25]], "epais": True},
    ]
    for y in (ya1, ya2):    # actines : de chaque strie Z vers le centre, et vers les sarcomères voisins
        el += [{"f": "ligne", "pts": [[r(zl), y], [r(al), y]], "couleur": "orange", "epais": True},
               {"f": "ligne", "pts": [[r(ar), y], [r(zr), y]], "couleur": "orange", "epais": True},
               {"f": "ligne", "pts": [[r(max(0.15, zl - k)), y], [r(zl), y]], "couleur": "orange", "epais": True},
               {"f": "ligne", "pts": [[r(zr), y], [r(min(11.85, zr + k)), y]], "couleur": "orange", "epais": True}]
    # numéros : flèches pour strie Z, actine, myosine ; cotes pour les bandes et le sarcomère
    xa = (m1 + zr) / 2
    el += [
        {"f": "texte", "at": [r(zl), 6.15], "t": str(num["strie"]), "couleur": "jaune"},
        {"f": "fleche", "de": [r(zl), 5.95], "a": [r(zl), 5.35], "couleur": "jaune"},
        {"f": "texte", "at": [r(xa), 6.15], "t": str(num["actine"]), "couleur": "jaune"},
        {"f": "fleche", "de": [r(xa), 5.95], "a": [r(xa), 4.95], "couleur": "jaune"},
        {"f": "texte", "at": [cx, 6.15], "t": str(num["myosine"]), "couleur": "jaune"},
        {"f": "fleche", "de": [cx, 5.95], "a": [cx, 4.45], "couleur": "jaune"},
        {"f": "cote", "de": [r(zl), 6.85], "a": [r(zr), 6.85], "t": str(num["sarcomere"]), "couleur": "jaune"},
        {"f": "cote", "de": [r(m0), 0.8], "a": [r(m1), 0.8], "t": str(num["sombre"]), "couleur": "jaune"},
        {"f": "cote", "de": [r(al), 1.85], "a": [r(ar), 1.85], "t": str(num["h"]), "couleur": "jaune"},
        {"f": "cote", "de": [r(m1), 1.85], "a": [r(vd), 1.85], "t": str(num["claire"]), "couleur": "jaune"},
    ]
    return {"type": "schema", "titre": titre, "cadre": {"l": 12, "h": 7.4}, "elements": el,
            "legende": "Schéma d'interprétation d'une portion de myofibrille (filaments fins en orange, filaments épais en bleu)."}


QUESTIONS = [
  {"id": "1", "texte": "Donner le nom de chacun des éléments numérotés de 1 à 7.",
   "texte_dit": "السؤال numéro un: عطي السمية ديال les éléments numérotés، de un à sept.",
   "reponse": {"type": "phrase", "attendu": "1 : strie Z ; 2 : filament fin d'actine ; 3 : filament épais de myosine ; 4 : bande claire (I) ; 5 : bande sombre (A) ; 6 : zone H ; 7 : sarcomère."},
   "clavier": {"aides": ["strie Z", "actine", "myosine", "bande claire (I)", "bande sombre (A)", "zone H", "sarcomère"], "pieges": ["strie M", "fibre musculaire", "myofibrille"]},
   "aides": [
     {"texte": "Commence par les traits verticaux épais : ce sont eux qui limitent le motif qui se répète. Finis par l'accolade du haut.",
      "dit": "بدا ب les traits verticaux الغلاظ: هوما اللي كيحددو الشكل اللي كيتعاود. وسالي ب la cote اللي الفوق."},
     {"texte": "Filament fin attaché aux stries Z, filament épais au centre ; puis chaque bande se nomme d'après les filaments qu'elle contient.",
      "dit": "le filament الرقيق مربوط ب les stries Z، و le filament الغليظ ف الوسط. ومن بعد، كل bande كتسمى على حساب les filaments اللي فيها."}],
   "correction": {"lignes": [
       {"texte": "1 : 1 strie Z ; 2 filament d'actine ; 3 filament de myosine", "mot": "un، la strie Z"},
       {"texte": "4 bande claire (I) ; 5 bande sombre (A) ; 6 zone H", "mot": "quatre، la bande claire"},
       {"texte": "7 sarcomère (d'une strie Z à la suivante)", "mot": "sept، le sarcomère"}],
     "parole": "السؤال numéro un. un، la strie Z. deux، le filament d'actine، الرقيق. trois، le filament de myosine، الغليظ. quatre، la bande claire، I. cinq، la bande sombre، A. six، la zone H. sept، le sarcomère، من strie Z ل strie Z."},
   "explication": "ex_s1", "facile": "fa_s1"},
  {"id": "2", "texte": "Définir le sarcomère.",
   "texte_dit": "السؤال numéro deux: عرف le sarcomère.",
   "reponse": {"type": "phrase", "attendu": "Le sarcomère est l'unité structurale et fonctionnelle de la myofibrille, délimitée par deux stries Z ; il comprend une bande sombre et deux demi-bandes claires."},
   "clavier": {"aides": ["unité structurale et fonctionnelle", "myofibrille", "délimitée par"], "pieges": ["unité du muscle", "deux zones H", "deux bandes sombres"]},
   "aides": [
     {"texte": "Le sarcomère est le motif qui se répète le long de quelle structure de la fibre ?",
      "dit": "le sarcomère هو الشكل اللي كيتعاود، على الطول ديال أشمن structure ف la fibre؟"},
     {"texte": "Une définition d'examen : « l'unité structurale et fonctionnelle de … », puis ce qui la délimite.",
      "dit": "la définition ديال l'examen: l'unité structurale et fonctionnelle ديال شنو؟ ومن بعد، شنو اللي كيحدها؟"}],
   "correction": {"lignes": [
       {"texte": "2 : le sarcomère est l'unité structurale et fonctionnelle de la myofibrille,", "mot": "l'unité structurale et fonctionnelle de la myofibrille"},
       {"texte": "délimitée par deux stries Z (une bande sombre + deux demi-bandes claires).", "mot": "délimitée par deux stries Z"}],
     "parole": "السؤال numéro deux. نعاود نقرا: le sarcomère, est l'unité structurale et fonctionnelle de la myofibrille, délimitée par deux stries Z. il contient une bande sombre، et deux demi-bandes claires."},
   "explication": "ex_s2", "facile": "fa_s2"},
  {"id": "3", "texte": "Préciser le ou les filaments présents dans la bande claire, dans la bande sombre et dans la zone H.",
   "texte_dit": "السؤال numéro trois: حدد أشمن filaments كاينين ف la bande claire، ف la bande sombre، و ف la zone H.",
   "reponse": {"type": "phrase", "attendu": "Bande claire (I) : filaments d'actine seuls. Bande sombre (A) : filaments de myosine sur toute leur longueur, avec les extrémités des filaments d'actine engagées sur ses bords. Zone H : filaments de myosine seuls (l'actine n'y arrive pas)."},
   "clavier": {"aides": ["actine seule", "myosine seule", "actine et myosine"], "pieges": ["zone H : actine seule", "bande claire : myosine"]},
   "aides": [
     {"texte": "Sur le schéma, monte verticalement depuis chaque bande et regarde quels filaments elle traverse.",
      "dit": "ف le schéma، طلع من كل bande ل الفوق، وشوف أشمن filaments كتلقى."},
     {"texte": "La bande sombre a exactement la longueur du filament de myosine ; la zone H est son centre.",
      "dit": "la bande sombre عندها نفس الطول ديال le filament de myosine، و la zone H هي الوسط ديالها."}],
   "correction": {"lignes": [
       {"texte": "3 : bande claire (I) : actine seule", "mot": "la bande claire: غير l'actine"},
       {"texte": "bande sombre (A) : toute la myosine (+ l'actine sur ses bords)", "mot": "la bande sombre: la myosine كاملة"},
       {"texte": "zone H : myosine seule", "mot": "la zone H: غير la myosine"}],
     "parole": "السؤال numéro trois. la bande claire: غير l'actine. la bande sombre: la myosine كاملة، و l'actine كتدخل ف الجناب ديالها. la zone H: غير la myosine، ف الوسط، فين ما كتوصلش l'actine."},
   "explication": "ex_s3", "facile": "fa_s3"},
  {"id": "4", "texte": "Lors de la contraction du muscle, le sarcomère raccourcit. Indiquer, parmi les éléments 4, 5, 6 et 7, ceux qui raccourcissent et celui qui garde la même longueur, puis dire ce que deviennent les longueurs des filaments.",
   "texte_dit": "السؤال numéro quatre: ف la contraction، le sarcomère كيولي قصير. من بين les éléments quatre، cinq، six et sept، شكون اللي كيوليو قصار، وشكون اللي كيبقى بنفس الطول؟ ومن بعد، شنو كيوقع ل الطول ديال les filaments؟",
   "reponse": {"type": "phrase", "attendu": "Raccourcissent : le sarcomère (7), la bande claire (4) et la zone H (6). Garde la même longueur : la bande sombre (5). Les filaments d'actine et de myosine gardent leur longueur : ils glissent les uns entre les autres, l'actine avançant vers le centre du sarcomère."},
   "clavier": {"aides": ["raccourcit", "garde sa longueur", "glissement"], "pieges": ["la bande sombre raccourcit", "la myosine glisse"]},
   "aides": [
     {"texte": "Pendant la contraction, les stries Z se rapprochent. Quels éléments vont jusqu'aux stries Z, et lequel a la longueur d'un filament ?",
      "dit": "ف la contraction، les stries Z كيتقربو. أشمن éléments كيوصلو ل les stries Z، و أشمن élément عندو الطول ديال filament؟"},
     {"texte": "Règle du cours : trois éléments raccourcissent, un seul reste constant ; aucun filament ne change de longueur.",
      "dit": "تفكر: trois éléments كيوليو قصار، و élément واحد كيبقى ثابت. و حتى filament ما كيتبدل الطول ديالو."}],
   "correction": {"lignes": [
       {"texte": "4 : raccourcissent : 7 sarcomère, 4 bande claire, 6 zone H", "mot": "كيوليو قصار"},
       {"texte": "constante : 5 bande sombre (longueur de la myosine)", "mot": "la bande sombre كتبقى بنفس الطول"},
       {"texte": "filaments : même longueur, l'actine glisse vers le centre", "mot": "les filaments كيبقاو بنفس الطول"}],
     "parole": "السؤال numéro quatre. le sarcomère، la bande claire، و la zone H كيوليو قصار. la bande sombre كتبقى بنفس الطول، حيت هي الطول ديال la myosine. و les filaments كيبقاو بنفس الطول: l'actine كتمشي بين la myosine، نحو الوسط ديال le sarcomère."},
   "explication": "ex_s4", "facile": "fa_s4"},
]

EXPLICATION = [
  {"id": "ex_s1", "slide_type": "simulation", "title": "Question 1 : légender en partant des stries Z",
   "screen_content": {"lead": "Stries Z, actine, myosine, puis les bandes, et l'accolade du sarcomère en dernier."},
   "visual": {"kind": "simulation", "url": SIM_C, "caption": "Le sarcomère se construit, élément par élément"},
   "speech_text": {"mixed": "نبنيو le sarcomère خطوة بخطوة. اللول، deux stries Z: هوما الحدود. على كل strie Z مربوطين des filaments رقاق: l'actine. ف الوسط، des filaments غلاظ: la myosine. فين كاينة la myosine، la bande sombre، A. فين كاينة غير l'actine، la bande claire، I، من الجيهتين ديال la strie Z. ف الوسط ديال la bande sombre، غير la myosine: la zone H. ومن strie Z ل strie Z: le sarcomère."},
   "concentration": {"demarrer": "reset",
     "centre": [{"texte": "1 strie Z · 2 actine · 3 myosine", "mot": "des filaments غلاظ: la myosine"},
                {"texte": "4 bande claire (I) · 5 bande sombre (A) · 6 zone H", "mot": "غير la myosine: la zone H"},
                {"texte": "7 sarcomère : de strie Z à strie Z", "mot": "ومن strie Z ل strie Z"}],
     "pointage": [{"mot": "اللول، deux stries Z", "commande": "play_until", "parametres": {"moment": "stries_z"}},
                  {"mot": "هوما الحدود", "repere": "strie_z"},
                  {"mot": "على كل strie Z", "commande": "play_until", "parametres": {"moment": "filaments_fins"}},
                  {"mot": "des filaments رقاق: l'actine", "repere": "actine"},
                  {"mot": "ف الوسط، des filaments غلاظ", "commande": "play_until", "parametres": {"moment": "filaments_epais"}},
                  {"mot": "des filaments غلاظ: la myosine", "repere": "myosine"},
                  {"mot": "des filaments غلاظ: la myosine", "cible": "centre:0"},
                  {"mot": "فين كاينة la myosine", "commande": "play_until", "parametres": {"moment": "bande_sombre"}},
                  {"mot": "la bande sombre، A", "repere": "bande_sombre"},
                  {"mot": "فين كاينة غير l'actine", "commande": "play_until", "parametres": {"moment": "bandes_claires"}},
                  {"mot": "la bande claire، I", "repere": "bande_claire"},
                  {"mot": "ف الوسط ديال la bande sombre", "commande": "play_until", "parametres": {"moment": "zone_h"}},
                  {"mot": "غير la myosine: la zone H", "repere": "zone_h"},
                  {"mot": "غير la myosine: la zone H", "cible": "centre:1"},
                  {"mot": "ومن strie Z ل strie Z", "commande": "play_until", "parametres": {"moment": "accolade_sarcomere"}},
                  {"mot": "ومن strie Z ل strie Z", "repere": "sarcomere"},
                  {"mot": "ومن strie Z ل strie Z", "cible": "centre:2"}]}},
  {"id": "ex_s2", "slide_type": "simulation", "title": "Question 2 : le sarcomère, motif répété de la myofibrille",
   "screen_content": {"lead": "Le sarcomère : unité structurale et fonctionnelle de la myofibrille, entre deux stries Z."},
   "visual": {"kind": "simulation", "url": SIM_S, "caption": "Du muscle à la myofibrille, puis au sarcomère"},
   "speech_text": {"mixed": "داخل la fibre musculaire، كاينين des myofibrilles. على الطول ديال myofibrille، نفس الشكل كيتعاود: des bandes كحلين و بيضين. الشكل اللي كيتعاود، كيبدا ف strie Z، وكيسالي ف la strie Z اللي من بعد: هادا هو le sarcomère. نعاود نقرا: le sarcomère, est l'unité structurale et fonctionnelle de la myofibrille, délimitée par deux stries Z."},
   "concentration": {"demarrer": "reset",
     "centre": [{"texte": "motif répété de la myofibrille", "mot": "نفس الشكل كيتعاود"},
                {"texte": "Sarcomère : unité structurale et fonctionnelle de la myofibrille, délimitée par deux stries Z", "mot": "نعاود نقرا"}],
     "pointage": [{"mot": "داخل la fibre musculaire", "commande": "set_time", "parametres": {"time_s": 9.6}},
                  {"mot": "كاينين des myofibrilles", "commande": "play_until", "parametres": {"moment": "myofibrille"}},
                  {"mot": "نفس الشكل كيتعاود", "repere": "myofibrille"},
                  {"mot": "نفس الشكل كيتعاود", "cible": "centre:0"},
                  {"mot": "الشكل اللي كيتعاود،", "commande": "play_until", "parametres": {"moment": "sarcomere"}},
                  {"mot": "كيبدا ف strie Z", "repere": "strie_z"},
                  {"mot": "هادا هو le sarcomère", "repere": "sarcomere"},
                  {"mot": "نعاود نقرا", "cible": "centre:1"}]}},
  {"id": "ex_s3", "slide_type": "simulation", "title": "Question 3 : chaque bande vient de ses filaments",
   "screen_content": {"lead": "Bande sombre : la myosine ; bande claire : l'actine seule ; zone H : la myosine seule."},
   "visual": {"kind": "simulation", "url": SIM_C, "caption": "Les bandes naissent des filaments"},
   "speech_text": {"mixed": "les bandes كيجيو من les filaments. la bande sombre عندها نفس الطول ديال la myosine: فيها la myosine كاملة، و l'actine كتدخل ف الجناب ديالها. la bande claire، فيها غير l'actine، من الجيهتين ديال la strie Z. و la zone H، ف الوسط ديال la bande sombre: فيها غير la myosine، حيت l'actine ما كتوصلش ل تما."},
   "concentration": {"demarrer": "reset",
     "centre": [{"texte": "bande sombre (A) : toute la myosine (+ l'actine sur ses bords)", "mot": "فيها la myosine كاملة"},
                {"texte": "bande claire (I) : l'actine seule", "mot": "فيها غير l'actine"},
                {"texte": "zone H : la myosine seule", "mot": "فيها غير la myosine"}],
     "pointage": [{"mot": "la bande sombre عندها", "commande": "play_until", "parametres": {"moment": "bande_sombre"}},
                  {"mot": "la bande sombre عندها", "repere": "bande_sombre"},
                  {"mot": "فيها la myosine كاملة", "cible": "centre:0"},
                  {"mot": "la bande claire، فيها", "commande": "play_until", "parametres": {"moment": "bandes_claires"}},
                  {"mot": "la bande claire، فيها", "repere": "bande_claire"},
                  {"mot": "فيها غير l'actine", "cible": "centre:1"},
                  {"mot": "و la zone H", "commande": "play_until", "parametres": {"moment": "zone_h"}},
                  {"mot": "و la zone H", "repere": "zone_h"},
                  {"mot": "فيها غير la myosine", "cible": "centre:2"}]}},
  {"id": "ex_s4", "slide_type": "simulation", "title": "Question 4 : ce qui change quand le sarcomère se contracte",
   "screen_content": {"lead": "Le sarcomère, la bande claire et la zone H raccourcissent ; la bande sombre et les filaments gardent leur longueur."},
   "visual": {"kind": "simulation", "url": SIM_K, "caption": "Sarcomère relâché (en gris) et sarcomère contracté"},
   "speech_text": {"mixed": "الفوق، le sarcomère relâché، بالرمادي. دابا كيتقلص: les stries Z كيتقربو، و l'actine كتمشي بين la myosine، نحو الوسط. قارن: le sarcomère ولا قصير، la bande claire ولات قصيرة، و la zone H ولات قصيرة حتى تختفي. ولكن la bande sombre بقات بنفس الطول، حيت هي الطول ديال la myosine. و les filaments؟ كيبقاو بنفس الطول: كيتحركو، ولكن ما كيوليوش قصار."},
   "concentration": {"demarrer": "reset",
     "centre": [{"texte": "raccourcissent : sarcomère, bande claire, zone H", "mot": "la zone H ولات قصيرة"},
                {"texte": "constante : bande sombre", "mot": "la bande sombre بقات بنفس الطول"},
                {"texte": "filaments : même longueur, l'actine glisse", "mot": "كيبقاو بنفس الطول"}],
     "pointage": [{"mot": "الفوق، le sarcomère relâché", "commande": "play_until", "parametres": {"moment": "relache"}},
                  {"mot": "بالرمادي", "repere": "etat_relache"},
                  {"mot": "دابا كيتقلص", "commande": "play_until", "parametres": {"moment": "glissement"}},
                  {"mot": "les stries Z كيتقربو", "repere": "strie_z_gauche"},
                  {"mot": "و l'actine كتمشي", "commande": "play_until", "parametres": {"moment": "contracte"}},
                  {"mot": "قارن:", "commande": "play_until", "parametres": {"moment": "mesure_contracte"}},
                  {"mot": "le sarcomère ولا قصير", "repere": "sarcomere"},
                  {"mot": "la bande claire ولات قصيرة", "repere": "bande_claire"},
                  {"mot": "la zone H ولات قصيرة", "repere": "zone_h"},
                  {"mot": "la zone H ولات قصيرة", "cible": "centre:0"},
                  {"mot": "la bande sombre بقات بنفس الطول", "repere": "bande_sombre"},
                  {"mot": "la bande sombre بقات بنفس الطول", "cible": "centre:1"},
                  {"mot": "و les filaments؟", "commande": "play_until", "parametres": {"moment": "filaments_mesures"}},
                  {"mot": "كيبقاو بنفس الطول", "repere": "myosine"},
                  {"mot": "كيبقاو بنفس الطول", "cible": "centre:2"}]}},
]

G = [("4", "4 : de part et d'autre de la strie Z"), ("5", "5 : toute la longueur de la myosine"), ("6", "6 : le centre, myosine sans actine"), ("7", "7 : de strie Z à strie Z")]
D = [("a", "bande claire (I)"), ("b", "bande sombre (A)"), ("c", "zone H"), ("d", "sarcomère")]
NOM = {"a": ("la bande claire", "l'actine seule, autour de la strie Z"), "b": ("la bande sombre", "toute la longueur de la myosine"),
       "c": ("la zone H", "le centre, où il n'y a que la myosine"), "d": ("le sarcomère", "d'une strie Z à la suivante")}
NOM_DIT = {"a": ("la bande claire", "غير l'actine، حدا la strie Z"), "b": ("la bande sombre", "الطول ديال la myosine كاملة"),
           "c": ("la zone H", "الوسط، فين كاينة غير la myosine"), "d": ("le sarcomère", "من strie Z ل strie Z")}
BON = {"4": "a", "5": "b", "6": "c", "7": "d"}
NUM_DIT = {"4": "quatre", "5": "cinq", "6": "six", "7": "sept"}
RETOURS = {}
for g, _ in G:
    for d, _ in D:
        if BON[g] == d:
            RETOURS[f"{g}-{d}"] = (True, f"Oui : {g}, c'est {NOM[d][0]} ({NOM[d][1]}).",
                                   f"برافو: l'élément {NUM_DIT[g]}، c'est {NOM_DIT[d][0]}، {NOM_DIT[d][1]}.")
        else:
            RETOURS[f"{g}-{d}"] = (False, f"Non : {NOM[d][0]}, c'est {NOM[d][1]}. Regarde où se trouve {g}.",
                                   f"لا، {NOM_DIT[d][0]} هي {NOM_DIT[d][1]}. شوف فين كاين l'élément {NUM_DIT[g]}.")
# « le sarcomère هي » : accorder au masculin
RETOURS = {k: (j, t, x.replace("le sarcomère هي", "le sarcomère هو")) for k, (j, t, x) in RETOURS.items()}

FACILE = [
  association("fa_s1", "Plus facile : nommer les bandes", "Relie chaque numéro à son nom.",
    "نتمرنو على les bandes: ربط كل numéro مع السمية ديالو.",
    "Relie chaque élément numéroté du schéma à son nom.", G, D, BON, RETOURS,
    ("4 : bande claire ; 5 : bande sombre ; 6 : zone H ; 7 : sarcomère.",
     "quatre، la bande claire. cinq، la bande sombre. six، la zone H. sept، le sarcomère.")),
  vrai_faux("fa_s2", "Plus facile : la définition du sarcomère", "Vrai ou faux : le sarcomère.",
    "سؤال ساهل: قرا كل جملة، وقول vrai ولا faux.",
    [("Le sarcomère est l'unité structurale et fonctionnelle de la myofibrille.", True,
      "Vrai : c'est le motif qui se répète le long de la myofibrille, et c'est lui qui se contracte."),
     ("Le sarcomère va d'une zone H à la zone H suivante.", False,
      "Faux : le sarcomère est délimité par deux stries Z."),
     ("Un sarcomère contient une bande sombre et deux demi-bandes claires.", True,
      "Vrai : la bande sombre au centre, une demi-bande claire contre chaque strie Z.")]),
  qcm_facile("fa_s3", "Plus facile : la zone H", "سؤال ساهل على la zone H.",
    "La zone H contient…", ["seulement des filaments d'actine", "seulement des filaments de myosine", "de l'actine et de la myosine"], 1, {
      "1": {"juste": rep("برافو! la zone H هي الوسط ديال la bande sombre، فيها غير la myosine، حيت l'actine ما كتوصلش ل تما.", "Juste : la zone H ne contient que la myosine.")},
      "0": {"1": rep("ما تقلقش. غير l'actine، هادي la bande claire. la zone H كاينة فين؟ ف الوسط ديال أشمن bande؟ عاود اختار.", "L'actine seule, c'est la bande claire. Où est la zone H ? Réessaie."),
            "2": rep("الجواب الصحيح: غير la myosine. l'actine بوحدها، هادي la bande claire.", "Réponse : la myosine seule ; l'actine seule forme la bande claire.")},
      "2": {"1": rep("قريب. l'actine و la myosine معا، هادي الجناب ديال la bande sombre. ولكن ف الوسط، واش كتوصل l'actine؟ عاود اختار.", "Actine et myosine ensemble : les bords de la bande sombre. L'actine arrive-t-elle au centre ? Réessaie."),
            "2": rep("الجواب الصحيح: غير la myosine. l'actine ما كتوصلش ل الوسط.", "Réponse : la myosine seule ; l'actine n'atteint pas le centre.")}},
    "La zone H contient quels filaments ?"),
  qcm_facile("fa_s4", "Plus facile : ce qui raccourcit", "سؤال ساهل: شنو اللي كيولي قصير ف la contraction؟",
    "Lors de la contraction, on observe au niveau du sarcomère un raccourcissement…",
    ["de la bande sombre et de la zone H", "du sarcomère, de la bande claire et de la zone H", "de toutes les bandes et des filaments"], 1, {
      "1": {"juste": rep("برافو! le sarcomère، la bande claire، و la zone H كيوليو قصار. la bande sombre كتبقى بنفس الطول.", "Juste : sarcomère, bande claire et zone H ; la bande sombre reste constante.")},
      "0": {"1": rep("ما تقلقش. la bande sombre عندها الطول ديال la myosine، و la myosine ما كتتبدلش. عاود اختار.", "La bande sombre a la longueur de la myosine, qui ne change pas. Réessaie."),
            "2": rep("الجواب الصحيح: le sarcomère، la bande claire، و la zone H. la bande sombre كتبقى ثابتة.", "Réponse : sarcomère, bande claire, zone H ; la bande sombre est constante.")},
      "2": {"1": rep("لا، les filaments ما كيتبدلش الطول ديالهم، كيتحركو برك. عاود اختار.", "Les filaments gardent leur longueur, ils glissent. Réessaie."),
            "2": rep("الجواب الصحيح: le sarcomère، la bande claire، و la zone H. les filaments و la bande sombre كيبقاو بنفس الطول.", "Réponse : sarcomère, bande claire, zone H ; filaments et bande sombre gardent leur longueur.")}},
    "Pendant la contraction, quels éléments du sarcomère raccourcissent ?"),
]

NUM_B = {"sarcomere": 1, "h": 2, "strie": 3, "sombre": 4, "myosine": 5, "claire": 6, "actine": 7}
SIM_Q = [
  {"id": "1", "texte": "Donner le nom de chacun des éléments numérotés de 1 à 7.",
   "reponse": {"type": "phrase", "attendu": "1 : sarcomère ; 2 : zone H ; 3 : strie Z ; 4 : bande sombre (A) ; 5 : filament épais de myosine ; 6 : bande claire (I) ; 7 : filament fin d'actine."},
   "clavier": {"aides": ["strie Z", "actine", "myosine", "bande claire (I)", "bande sombre (A)", "zone H", "sarcomère"], "pieges": ["strie M", "myofibrille"]},
   "correction": {"lignes": [{"texte": "1 : 1 sarcomère ; 2 zone H ; 3 strie Z", "mot": "un، le sarcomère"},
                             {"texte": "4 bande sombre (A) ; 5 filament de myosine", "mot": "quatre، la bande sombre"},
                             {"texte": "6 bande claire (I) ; 7 filament d'actine", "mot": "six، la bande claire"}],
                  "parole": "السؤال numéro un. un، le sarcomère. deux، la zone H. trois، la strie Z. quatre، la bande sombre. cinq، le filament de myosine. six، la bande claire. sept، le filament d'actine."}},
  {"id": "2", "texte": "Définir le sarcomère.",
   "reponse": {"type": "phrase", "attendu": "Le sarcomère est l'unité structurale et fonctionnelle de la myofibrille, délimitée par deux stries Z."},
   "clavier": {"aides": ["unité structurale et fonctionnelle", "myofibrille"], "pieges": ["unité du muscle"]},
   "correction": {"lignes": [{"texte": "2 : unité structurale et fonctionnelle de la myofibrille", "mot": "l'unité structurale et fonctionnelle de la myofibrille"},
                             {"texte": "délimitée par deux stries Z", "mot": "délimitée par deux stries Z"}],
                  "parole": "السؤال numéro deux. le sarcomère, est l'unité structurale et fonctionnelle de la myofibrille, délimitée par deux stries Z."}},
  {"id": "3", "texte": "Préciser le ou les filaments présents dans la bande claire, dans la bande sombre et dans la zone H.",
   "reponse": {"type": "phrase", "attendu": "Bande claire (6) : actine seule. Bande sombre (4) : toute la myosine, avec l'actine sur ses bords. Zone H (2) : myosine seule."},
   "clavier": {"aides": ["actine seule", "myosine seule"], "pieges": ["zone H : actine seule"]},
   "correction": {"lignes": [{"texte": "3 : bande claire : actine seule", "mot": "la bande claire: غير l'actine"},
                             {"texte": "bande sombre : myosine (+ actine sur ses bords) ; zone H : myosine seule", "mot": "la zone H: غير la myosine"}],
                  "parole": "السؤال numéro trois. la bande claire: غير l'actine. la bande sombre: la myosine كاملة، مع l'actine ف الجناب. la zone H: غير la myosine."}},
  {"id": "4", "texte": "Lors de la contraction du muscle, le sarcomère raccourcit. Indiquer, parmi les éléments 1, 2, 4 et 6, ceux qui raccourcissent et celui qui garde la même longueur, puis dire ce que deviennent les longueurs des filaments.",
   "reponse": {"type": "phrase", "attendu": "Raccourcissent : le sarcomère (1), la zone H (2) et la bande claire (6). Garde la même longueur : la bande sombre (4). Les filaments gardent leur longueur : l'actine glisse entre la myosine vers le centre du sarcomère."},
   "clavier": {"aides": ["raccourcit", "garde sa longueur", "glissement"], "pieges": ["la bande sombre raccourcit"]},
   "correction": {"lignes": [{"texte": "4 : raccourcissent : 1, 2 et 6", "mot": "كيوليو قصار"},
                             {"texte": "constante : 4 (bande sombre) ; filaments de même longueur", "mot": "la bande sombre كتبقى بنفس الطول"}],
                  "parole": "السؤال numéro quatre. le sarcomère، la zone H، و la bande claire كيوليو قصار. la bande sombre كتبقى بنفس الطول، و les filaments حتى هوما."}},
]

EX = {
  "id": "svt_ex_ch2_sarcomere_1", "type": "exercice", "version": 1, "status": "published",
  "matiere": "svt", "chapitre": "role_muscle_strie_squelettique", "cours": "svt_ch2_role_muscle_strie_squelettique",
  "titre": "Légender un sarcomère, puis prévoir ce qui change à la contraction", "niveau": "facile", "duree_min": 15,
  "origine": "Exercice original écrit pour Moalim (ni sujet du national, ni copie d'un livre).",
  "competences": ["Légender le schéma d'un sarcomère", "Définir le sarcomère", "Relier les bandes aux myofilaments", "Dire ce qui raccourcit à la contraction"],
  "enonce": {
    "intro": "L'observation au microscope électronique d'une myofibrille de muscle strié squelettique, au repos, a permis de réaliser le schéma d'interprétation ci-dessous. Les éléments sont numérotés de 1 à 7.",
    "intro_dit": "نقراو l'énoncé. شفنا myofibrille ديال le muscle strié squelettique، ف الراحة، ب le microscope électronique، ورسمنا هاد le schéma. les éléments numérotés، de un à sept.",
    "figures": [schema(2.5, {"strie": 1, "actine": 2, "myosine": 3, "claire": 4, "sombre": 5, "h": 6, "sarcomere": 7},
                       "Schéma d'interprétation d'une myofibrille au repos")],
    "donnees": ["Filaments fins (orange) et filaments épais (bleu)", "Muscle au repos (sarcomère relâché)"],
    "questions": QUESTIONS},
  "explication": {"activities": [{"id": "explication", "title": "Explication animée", "slides": EXPLICATION}]},
  "facile": {"activities": [{"id": "facile", "title": "Plus facile, pour s'entraîner", "slides": FACILE}]},
  "similaire": {
    "id": "svt_ex_ch2_sarcomere_1_b", "titre": "Même exercice, autres données",
    "enonce": {
      "intro": "Schéma d'interprétation d'une autre myofibrille, observée au microscope électronique ; les numéros sont placés dans un autre ordre.",
      "intro_dit": "schéma ديال myofibrille أخرى، ب le microscope électronique. les numéros ف ترتيب آخر.",
      "figures": [schema(2.2, NUM_B, "Schéma d'interprétation d'une autre myofibrille")],
      "donnees": ["Filaments fins (orange) et filaments épais (bleu)"],
      "questions": SIM_Q}},
}

if __name__ == "__main__":
    ecrire(EX, sys.argv[1])
