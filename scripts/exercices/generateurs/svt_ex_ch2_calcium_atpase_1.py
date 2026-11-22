# Exercice SVT ch. 2 (rôle du muscle strié squelettique), niveau difficile (« Supérieur ») : Ca²⁺, ATP et activité ATPasique.
# Ce qu'il entraîne : comparer des milieux à un milieu de référence et en déduire les conditions de la contraction (Ca²⁺,
# ATP, hydrolyse de l'ATP) ; expliquer d'où vient l'énergie de la contraction (hydrolyse par la tête de myosine, ATPase) ;
# expliquer une hydrolyse faible SANS contraction (myosine seule, sites cachés) en mobilisant l'activité ATPasique activée
# par l'actine ; exploiter un second document (filaments fins avec ou sans troponine-tropomyosine) pour montrer que le
# Ca²⁺ agit par la troponine et la tropomyosine, non sur la myosine ; relier la chaleur dégagée à l'hydrolyse de l'ATP et
# à la chaleur initiale d'un muscle entier (et l'absence de chaleur retardée sans dioxygène) : deux notions combinées.
# Sources comparées (lecture seulement, rien de copié) :
# - exploration du cours : cas_types « associer_roles » (Ca²⁺ ↔ troponine ; hydrolyse ↔ rotation ; chaleur initiale ↔
#   phosphocréatine ; chaleur retardée ↔ réactions aérobies), « hypothese » ; pièges « Ca²⁺ sur l'actine ou la tropomyosine »,
#   « le Ca²⁺ donne l'énergie », « inverse les deux chaleurs » ; a_ne_pas_dire (énergie de l'ATP qui « enlève » la
#   troponine, coup de force, rigor) ; exclus_hors_programme (pas de tubules T, pas d'états ADP·Pi, pas de rigidité
#   cadavérique, pas de chaleur de maintien) vérifiés ;
# - cours : fibre glycérinée (exigences.html), myofibrille + salyrgan / chélateur (ms_c1c), trois tubes de l'ATPase
#   (atpase.html : actine 0, myosine 4, actine + myosine 40), Ca²⁺ et troponine (calcium.html), chaleurs (chaleur.html) ;
# - nationaux : 2016 N (⁴⁵Ca²⁺, équorine), associations Ca²⁺ / ATP (2021 N, 2022 N, 2024 R), chaleur (associations) :
#   aucun ne donne nos deux documents (Pi + chaleur par milieu ; filaments sans troponine-tropomyosine) ;
# - séries en ligne : recherche du 22/11/2026 : seuls les extraits des résultats ont pu être lus (moutamadris.ma et
#   dreamjob.ma bloqués par le réseau de la session) ; comparaison faite avec les vidéos (exploration) et les nationaux.
# Valeurs de Pi choisies pour coller à atpase.html (myosine seule : 4 UA ; myosine liée à l'actine : 40 UA).
import sys
sys.path.insert(0, __import__("os").path.dirname(__file__))
from _commun import rep, qcm_facile, vrai_faux, association, ecrire

D = "/media/simulations/svt/role_muscle_strie_squelettique-tableau/"
EXIG = D + "exigences.html?attente=1"
CYCLE = D + "cycle.html?vue=cycle&attente=1"
ATPASE = D + "atpase.html"
CALC = D + "calcium.html?vue=acces&attente=1"
CHAL = D + "chaleur.html?attente=1"


def tableau(titre, legende, entetes, lignes, larg, h_ligne=0.8):
    """Un tableau dessiné (schema à cadre) : rect + lignes + texte. Une cellule peut tenir sur deux lignes (« \\n »)."""
    toutes = [entetes] + lignes
    hs = [h_ligne * max(len(c.split("\n")) for c in r) for r in toutes]
    l, h = sum(larg), sum(hs)
    el = [{"f": "rect", "de": [0, 0], "a": [l, h], "couleur": "blanc"}]
    y = h
    for k, r in enumerate(toutes):
        y_bas = y - hs[k]
        if k < len(toutes) - 1:
            el.append({"f": "ligne", "pts": [[0, round(y_bas, 3)], [l, round(y_bas, 3)]], "couleur": "blanc" if k == 0 else "faible"})
        x = 0
        for j, cel in enumerate(r):
            morceaux = cel.split("\n")
            for m, t in enumerate(morceaux):
                yc = y - hs[k] / 2 + (len(morceaux) - 1) * h_ligne * 0.32 - m * h_ligne * 0.64
                el.append({"f": "texte", "at": [round(x + larg[j] / 2, 3), round(yc, 3)], "t": t, "taille": "petit",
                           "couleur": "cyan" if k == 0 or j == 0 else "blanc", "ancre": "centre"})
            x += larg[j]
        y = y_bas
    x = 0
    for w in larg[:-1]:
        x += w
        el.append({"f": "ligne", "pts": [[round(x, 3), 0], [round(x, 3), h]], "couleur": "faible"})
    return {"type": "schema", "titre": titre, "legende": legende, "cadre": {"l": l, "h": round(h, 3)}, "elements": el}


def doc1(pi):
    return tableau("Document 1 : myofibrilles isolées dans quatre milieux",
                   "Pi : phosphate libéré en une minute (unités arbitraires) ; il mesure l'ATP hydrolysé. Salyrgan : bloque l'hydrolyse de l'ATP.",
                   ["Milieu", "Contenu", "Contraction", "Pi libéré\n(UA)", "Chaleur"],
                   [["1", "ATP + Ca²⁺", "oui", str(pi[0]), "forte"],
                    ["2", "ATP, sans Ca²⁺", "non", str(pi[1]), "très faible"],
                    ["3", "Ca²⁺, sans ATP", "non", str(pi[2]), "nulle"],
                    ["4", "ATP + Ca²⁺\n+ salyrgan", "non", str(pi[3]), "nulle"]],
                   [1.5, 3.9, 2.2, 2.2, 2.2])


def doc2(pi):
    return tableau("Document 2 : activité ATPasique de la myosine en tube (ATP dans chaque tube)",
                   "Pi libéré en une minute (UA). Filament fin complet : actine + troponine + tropomyosine.",
                   ["Tube", "Contenu", "Pi (UA)"],
                   [["A", "myosine + actine pure, sans Ca²⁺\n(ni troponine, ni tropomyosine)", str(pi[0])],
                    ["B", "myosine + filaments fins complets,\nsans Ca²⁺", str(pi[1])],
                    ["C", "comme B, avec des ions Ca²⁺", str(pi[2])]],
                   [1.4, 8.4, 2.2])


PI1, PI2 = (40, 4, 0, 0), (40, 4, 40)
PI1B, PI2B = (30, 3, 0, 0), (30, 3, 30)
assert PI1[1] == 4 and PI1[0] == 40  # valeurs de atpase.html : myosine seule 4 ; myosine + actine 40

EX = {
  "id": "svt_ex_ch2_calcium_atpase_1", "type": "exercice", "version": 1, "status": "published",
  "matiere": "svt", "chapitre": "role_muscle_strie_squelettique", "cours": "svt_ch2_role_muscle_strie_squelettique",
  "titre": "Ca²⁺, ATP et activité ATPasique de la myosine", "niveau": "difficile", "duree_min": 35,
  "origine": "Exercice original écrit pour Moalim (ni sujet du national, ni copie d'un livre).",
  "competences": ["Déduire les conditions de la contraction", "Expliquer l'origine de l'énergie de la contraction",
                  "Relier activité ATPasique, Ca²⁺ et troponine-tropomyosine", "Relier l'hydrolyse de l'ATP à la chaleur initiale"],
  "enonce": {
    "intro": "On isole des myofibrilles d'un muscle squelettique : elles n'ont plus ni réserve d'ATP ni ions Ca²⁺. On les place dans quatre milieux différents, puis on note si elles se contractent, on mesure le phosphate (Pi) libéré et la chaleur dégagée (document 1). Dans une seconde expérience, on mesure l'activité ATPasique de la myosine purifiée, mélangée à différents filaments fins, dans des tubes contenant de l'ATP (document 2).",
    "intro_dit": "دابا نقراو l'énoncé. خرجنا des myofibrilles من muscle: ما بقا فيهم لا A T P لا calcium. حطيناهم dans quatre milieux، وكل مرة شفنا واش كيتقلصو، قسنا le phosphate P i اللي خرج، و la chaleur. هادا le document un. ف تجربة ثانية، قسنا l'activité A T P asique ديال la myosine، مخلطة مع des filaments fins مختلفين، ف des tubes فيهم l'A T P: هادا le document deux.",
    "figures": [doc1(PI1), doc2(PI2)],
    "donnees": ["Pi libéré : mesure la quantité d'ATP hydrolysé (ATP + H₂O → ADP + Pi + énergie)",
                "Salyrgan : substance qui bloque l'hydrolyse de l'ATP",
                "Filament fin complet : actine + troponine + tropomyosine ; actine pure : sans troponine ni tropomyosine"],
    "questions": [
      {"id": "1", "texte": "Comparer les résultats des milieux 2, 3 et 4 à ceux du milieu 1, puis en déduire les conditions nécessaires à la contraction.",
       "texte_dit": "Question un : قارن les résultats ديال les milieux deux، trois et quatre، مع le milieu un، ومن بعد استنتج الشروط اللي محتاجاها la contraction.",
       "reponse": {"type": "phrase", "attendu": "Milieu 1 (ATP + Ca²⁺) : contraction, Pi élevé (40 UA). Milieu 2 (sans Ca²⁺) : pas de contraction et Pi faible (4 UA contre 40). Milieu 3 (sans ATP) : pas de contraction et pas de Pi (0). Milieu 4 (salyrgan) : malgré l'ATP et le Ca²⁺, pas de contraction et pas de Pi (0). On en déduit que la contraction nécessite des ions Ca²⁺, de l'ATP, et l'hydrolyse de cet ATP."},
       "clavier": {"aides": ["contre 40 UA", "pas de Pi", "ions Ca²⁺", "ATP", "hydrolyse de l'ATP"], "pieges": ["le Ca²⁺ suffit", "l'ATP suffit"]},
       "aides": [
         {"texte": "Chaque milieu diffère du milieu 1 par une seule chose : repère-la, puis compare contraction et Pi.",
          "dit": "كل milieu كيختلف على le milieu un ب حاجة وحدة: لقاها، ومن بعد قارن la contraction و P i."},
         {"texte": "Ce qui manque (ou est bloqué) dans un milieu sans contraction est nécessaire : Ca²⁺ (milieu 2), ATP (milieu 3), hydrolyse (milieu 4).",
          "dit": "اللي ناقص ولا مسدود ف milieu بلا contraction، هو ضروري: le calcium ف le milieu deux، l'A T P ف le milieu trois، و l'hydrolyse ف le milieu quatre."}],
       "correction": {"lignes": [
           {"texte": "1 : milieu 1 : contraction, Pi = 40 UA (référence)", "mot": "le milieu un"},
           {"texte": "milieu 2 (sans Ca²⁺) : pas de contraction, Pi = 4 UA contre 40", "mot": "le milieu deux"},
           {"texte": "milieux 3 (sans ATP) et 4 (salyrgan) : pas de contraction, Pi = 0", "mot": "le milieu trois"},
           {"texte": "conditions : ions Ca²⁺ + ATP + hydrolyse de l'ATP", "mot": "la contraction محتاجة"}],
         "parole": "Question un. le milieu un، فيه l'A T P و le calcium: كاينة la contraction، و P i égale quarante. le milieu deux، بلا calcium: ما كايناش contraction، و P i faible، quatre contre quarante. le milieu trois، بلا A T P: لا contraction لا P i. و le milieu quatre، avec le salyrgan: واخا كاين l'A T P و le calcium، لا contraction لا P i. إذن la contraction محتاجة les ions calcium، l'A T P، و l'hydrolyse ديال l'A T P."},
       "explication": "ex_s1", "facile": "fa_s1"},
      {"id": "2", "texte": "Expliquer l'absence de contraction dans les milieux 3 et 4, en précisant d'où vient l'énergie de la contraction.",
       "texte_dit": "Question deux : شرح علاش ما كايناش contraction ف les milieux trois et quatre، وقول منين كتجي l'énergie ديال la contraction.",
       "reponse": {"type": "phrase", "attendu": "L'énergie de la contraction vient de l'hydrolyse de l'ATP par la tête de myosine, qui est une ATPase : ATP + H₂O → ADP + Pi + énergie. Cette énergie fait tourner les têtes de myosine fixées à l'actine, qui font glisser l'actine vers le centre du sarcomère. Dans le milieu 3, il n'y a pas d'ATP ; dans le milieu 4, l'ATP n'est pas hydrolysé (salyrgan) : dans les deux cas, pas de Pi, pas d'énergie libérée, pas de rotation des têtes, donc pas de glissement ni de contraction."},
       "clavier": {"aides": ["hydrolyse de l'ATP", "ATP + H₂O → ADP + Pi + énergie", "ATPase", "rotation des têtes", "glissement"], "pieges": ["le Ca²⁺ fournit l'énergie", "le salyrgan enlève le Ca²⁺"]},
       "aides": [
         {"texte": "Point commun des milieux 3 et 4 : Pi = 0. Que veut dire « pas de Pi » ?",
          "dit": "الحاجة اللي مشتركة بين le milieu trois et quatre: P i égale zéro. شنو معناها ما خرجش P i؟"},
         {"texte": "Pas de Pi = pas d'hydrolyse = pas d'énergie. Or c'est l'énergie de l'hydrolyse qui fait tourner les têtes de myosine.",
          "dit": "ما كاينش P i، يعني ما كايناش l'hydrolyse، يعني ما كايناش l'énergie. و l'énergie ديال l'hydrolyse هي اللي كتدور les têtes de myosine."}],
       "correction": {"lignes": [
           {"texte": "2 : énergie : hydrolyse de l'ATP par la tête de myosine (ATPase) : ATP + H₂O → ADP + Pi + énergie", "mot": "A T P plus H deux O"},
           {"texte": "cette énergie fait tourner les têtes → glissement de l'actine", "mot": "هاد l'énergie كتدور les têtes"},
           {"texte": "milieu 3 : pas d'ATP ; milieu 4 : ATP non hydrolysé → Pi = 0, pas d'énergie, pas de contraction", "mot": "ف le milieu trois"}],
         "parole": "Question deux. l'énergie ديال la contraction كتجي من l'hydrolyse ديال l'A T P، و la tête de myosine هي اللي كتديرها: est une A T P ase. A T P plus H deux O donne A D P plus P i plus énergie. هاد l'énergie كتدور les têtes اللي لاصقين ف l'actine، و l'actine كتزلق نحو الوسط ديال le sarcomère. ف le milieu trois، ما كاينش l'A T P. ف le milieu quatre، l'A T P كاين، ولكن le salyrgan كيمنع l'hydrolyse. ف جوج الحالات: ما خرجش P i، ما كايناش l'énergie، les têtes ما كيدوروش، إذن ما كايناش contraction."},
       "explication": "ex_s2", "facile": "fa_s2"},
      {"id": "3", "texte": "Dans le milieu 2, un peu d'ATP est hydrolysé (Pi = 4 UA) mais les myofibrilles ne se contractent pas. En exploitant tes connaissances sur l'activité ATPasique de la myosine, expliquer ce résultat.",
       "texte_dit": "Question trois : ف le milieu deux، شوية ديال l'A T P وقع ليه l'hydrolyse، P i égale quatre، ولكن les myofibrilles ما تقلصوش. ب الدروس ديالك على l'activité A T P asique ديال la myosine، شرح هاد le résultat.",
       "reponse": {"type": "phrase", "attendu": "Sans Ca²⁺, la tropomyosine cache les sites de fixation de l'actine : les têtes de myosine ne peuvent pas se fixer sur l'actine, il ne se forme pas de complexe actomyosine. La myosine seule hydrolyse l'ATP faiblement (4 UA) ; liée à l'actine, son activité ATPasique est beaucoup plus forte (40 UA dans le milieu 1). L'énergie de cette faible hydrolyse ne peut pas tirer l'actine, puisque les têtes ne sont pas fixées dessus : pas de glissement, pas de contraction."},
       "clavier": {"aides": ["tropomyosine", "sites de fixation cachés", "pas de complexe actomyosine", "myosine seule : hydrolyse faible", "activée par l'actine"], "pieges": ["le Ca²⁺ est l'enzyme", "l'actine hydrolyse l'ATP"]},
       "aides": [
         {"texte": "Rappelle-toi les trois tubes du cours : actine seule, myosine seule, actine + myosine. Lequel ressemble au milieu 2 ?",
          "dit": "تفكر les trois tubes ديال الدرس: l'actine بوحدها، la myosine بوحدها، و l'actine مع la myosine. شمن tube كيشبه le milieu deux؟"},
         {"texte": "Sans Ca²⁺, la tropomyosine cache les sites de l'actine : les têtes restent détachées, comme une myosine seule.",
          "dit": "بلا calcium، la tropomyosine كتغطي les sites ديال l'actine: les têtes كيبقاو مطلوقين، بحال la myosine بوحدها."}],
       "correction": {"lignes": [
           {"texte": "3 : sans Ca²⁺, la tropomyosine cache les sites de l'actine : pas de complexe actomyosine", "mot": "la tropomyosine كتغطي les sites"},
           {"texte": "myosine non liée à l'actine : hydrolyse faible (4 UA) ; liée à l'actine : forte (40 UA)", "mot": "la myosine بوحدها"},
           {"texte": "têtes non fixées : l'énergie ne tire pas l'actine → pas de contraction", "mot": "ما تقدرش تجر l'actine"}],
         "parole": "Question trois. بلا calcium، la tropomyosine كتغطي les sites ديال l'actine: les têtes de myosine ما يقدروش يتشدو، وما كيتكونش le complexe actomyosine. la myosine بوحدها كتدير l'hydrolyse ضعيفة: quatre unités، بحال le tube ديال la myosine ف الدرس. ملي كتلصق ف l'actine، كتولي قوية: quarante unités. و l'énergie ديال هاد l'hydrolyse الضعيفة ما تقدرش تجر l'actine، حيت les têtes ما لاصقينش فيها: إذن ما كايناش contraction."},
       "explication": "ex_s3", "facile": "fa_s3"},
      {"id": "4", "texte": "En exploitant le document 2, comparer les tubes A et B, puis les tubes B et C. En déduire comment les ions Ca²⁺ permettent l'activité ATPasique forte de la myosine et la contraction.",
       "texte_dit": "Question quatre : ب le document deux، قارن le tube A مع le tube B، ومن بعد le tube B مع le tube C. استنتج كيفاش les ions calcium كيخليو l'activité A T P asique ديال la myosine قوية، و la contraction ممكنة.",
       "reponse": {"type": "phrase", "attendu": "A / B (tous deux sans Ca²⁺) : avec l'actine pure, sans troponine ni tropomyosine, l'hydrolyse est forte (40 UA) ; avec des filaments fins complets, elle est faible (4 UA). La troponine et la tropomyosine empêchent donc la myosine de se lier à l'actine en l'absence de Ca²⁺. B / C : l'ajout de Ca²⁺ rend l'hydrolyse forte (4 → 40 UA). Le Ca²⁺ n'agit donc pas sur la myosine elle-même (sans troponine ni tropomyosine, elle n'en a pas besoin) : il lève le blocage. Il se fixe sur la troponine, la tropomyosine se déplace et libère les sites de fixation de l'actine ; les têtes de myosine se fixent (complexe actomyosine), leur activité ATPasique devient forte et la contraction est possible."},
       "clavier": {"aides": ["troponine", "tropomyosine", "lève le blocage", "sites de fixation libérés", "complexe actomyosine"], "pieges": ["le Ca²⁺ active la myosine directement", "le Ca²⁺ se fixe sur la tropomyosine"]},
       "aides": [
         {"texte": "A et B sont tous deux sans Ca²⁺ : qu'est-ce qui les distingue ? B et C ne diffèrent que par le Ca²⁺.",
          "dit": "le tube A و le tube B، جوج بلا calcium: شنو اللي كيفرقهم؟ و le tube B و le tube C، ما كيختلفوش غير ف le calcium."},
         {"texte": "Si la myosine fonctionne bien sans Ca²⁺ quand il n'y a ni troponine ni tropomyosine, alors le Ca²⁺ agit sur… quoi ? Rappelle où il se fixe.",
          "dit": "يلا la myosine خدامة مزيان بلا calcium، ملي ما كايناش لا la troponine لا la tropomyosine، إذن le calcium كيخدم على شنو؟ تفكر فين كيلصق."}],
       "correction": {"lignes": [
           {"texte": "4 : A : 40 UA contre B : 4 UA sans Ca²⁺ → troponine + tropomyosine bloquent la liaison actine-myosine", "mot": "le tube A"},
           {"texte": "B : 4 UA contre C : 40 UA → le Ca²⁺ lève ce blocage", "mot": "le tube C"},
           {"texte": "le Ca²⁺ n'agit pas sur la myosine : il se fixe sur la troponine, la tropomyosine libère les sites", "mot": "كيلصق على la troponine"},
           {"texte": "complexe actomyosine → hydrolyse forte → contraction", "mot": "le complexe actomyosine"}],
         "parole": "Question quatre. le tube A و le tube B، جوج بلا calcium. ف A، l'actine pure، بلا troponine وبلا tropomyosine: l'hydrolyse قوية، quarante. ف B، des filaments fins complets: l'hydrolyse ضعيفة، quatre. إذن la troponine و la tropomyosine كيمنعو la myosine تتشد ف l'actine. le tube C، نفس B مع le calcium: l'hydrolyse رجعات قوية، quarante. إذن le calcium ما كيخدمش على la myosine: كيحيد هاد المنع. كيلصق على la troponine، la tropomyosine كتزاح، و les sites كيتحررو. les têtes كيتشدو: le complexe actomyosine. l'hydrolyse كتولي قوية، و la contraction ممكنة."},
       "explication": "ex_s4", "facile": "fa_s4"},
      {"id": "5", "texte": "Les myofibrilles du milieu 1 dégagent de la chaleur ; celles des milieux 3 et 4 n'en dégagent pas. Relier ce résultat à la chaleur initiale d'un muscle entier, puis expliquer pourquoi un muscle entier privé de dioxygène dégage encore une chaleur initiale mais pas de chaleur retardée.",
       "texte_dit": "Question cinq : les myofibrilles ديال le milieu un كيطلقو la chaleur، و ديال les milieux trois et quatre لا. ربط هاد le résultat مع la chaleur initiale ديال muscle كامل، ومن بعد شرح علاش muscle بلا dioxygène كيعطي ديما la chaleur initiale، ولكن ما كيعطيش la chaleur retardée.",
       "reponse": {"type": "phrase", "attendu": "La chaleur n'apparaît que lorsque l'ATP est hydrolysé (milieu 1) : une partie de l'énergie libérée par l'hydrolyse de l'ATP est perdue sous forme de chaleur. Dans un muscle entier, la chaleur initiale, dégagée pendant la secousse, vient de cette hydrolyse de l'ATP et de sa régénération rapide par la phosphocréatine (PC + ADP → C + ATP) : ces réactions n'utilisent pas de dioxygène, donc la chaleur initiale existe encore sans dioxygène. La chaleur retardée, après la secousse, vient de la régénération de l'ATP par la respiration (réactions aérobies) : sans dioxygène, pas de respiration, donc pas de chaleur retardée."},
       "clavier": {"aides": ["hydrolyse de l'ATP", "chaleur initiale", "phosphocréatine", "sans dioxygène", "chaleur retardée : respiration"], "pieges": ["chaleur initiale = respiration", "chaleur retardée = phosphocréatine"]},
       "aides": [
         {"texte": "Dans quels milieux l'ATP est-il hydrolysé ? Et dans lesquels y a-t-il de la chaleur ? Compare.",
          "dit": "ف شمن milieux l'A T P وقع ليه l'hydrolyse؟ وف شمن milieux كاينة la chaleur؟ قارن."},
         {"texte": "Chaleur initiale : hydrolyse de l'ATP et phosphocréatine (sans O₂). Chaleur retardée : respiration (avec O₂).",
          "dit": "la chaleur initiale: l'hydrolyse ديال l'A T P و la phosphocréatine، بلا dioxygène. la chaleur retardée: la respiration، مع le dioxygène."}],
       "correction": {"lignes": [
           {"texte": "5 : chaleur seulement quand l'ATP est hydrolysé : une partie de l'énergie part en chaleur", "mot": "كتخرج غير ملي"},
           {"texte": "chaleur initiale : hydrolyse de l'ATP + régénération par la phosphocréatine, sans O₂", "mot": "la chaleur initiale"},
           {"texte": "chaleur retardée : régénération de l'ATP par la respiration (aérobie)", "mot": "la chaleur retardée"},
           {"texte": "sans O₂ : chaleur initiale présente, pas de chaleur retardée", "mot": "بلا dioxygène"}],
         "parole": "Question cinq. la chaleur كتخرج غير ملي l'A T P كيوقع ليه l'hydrolyse، ف le milieu un. جزء من l'énergie ديال l'hydrolyse كيمشي chaleur. ف muscle كامل، la chaleur initiale كتجي من l'hydrolyse ديال l'A T P، ومن la régénération السريعة ديالو ب la phosphocréatine: des réactions بلا dioxygène. la chaleur retardée كتجي من la régénération ديال l'A T P ب la respiration، des réactions aérobies. إذن بلا dioxygène: la chaleur initiale كتبقى، ولكن la chaleur retardée ما كتجيش."},
       "explication": "ex_s5", "facile": "fa_s5"}
    ]
  },
  "explication": {"activities": [{"id": "explication", "title": "Explication animée", "slides": [
    {"id": "ex_s1", "slide_type": "simulation", "title": "Question 1 : un milieu, une seule différence",
     "screen_content": {"lead": "Sans Ca²⁺, sans ATP ou sans hydrolyse : pas de contraction."},
     "visual": {"kind": "simulation", "url": EXIG, "caption": "Une fibre sans réserves : on choisit ce qu'on lui donne"},
     "speech_text": {"mixed": "هاد la fibre ما فيها لا A T P لا calcium، بحال les myofibrilles ديال le document. avec l'A T P et le calcium: le levier كيطلع، كاينة la contraction. هادا هو المرجع، بحال le milieu un. l'A T P بلا calcium: ما كايناش contraction، بحال le milieu deux. le calcium بلا A T P: حتى هنا ما كايناش contraction، بحال le milieu trois. و le milieu quatre؟ l'A T P كاين، ولكن le salyrgan كيمنع l'hydrolyse ديالو: ما كايناش contraction. إذن خاص les ions calcium، l'A T P، و l'hydrolyse ديالو."},
     "concentration": {"demarrer": "reset",
       "centre": [{"texte": "ATP + Ca²⁺ : contraction (référence)", "mot": "هادا هو المرجع"},
                  {"texte": "sans Ca²⁺ ou sans ATP : pas de contraction", "mot": "بحال le milieu trois"},
                  {"texte": "salyrgan : ATP non hydrolysé → pas de contraction", "mot": "و le milieu quatre؟"},
                  {"texte": "conditions : Ca²⁺ + ATP + hydrolyse", "mot": "إذن خاص les ions calcium"}],
       "pointage": [{"mot": "هاد la fibre", "repere": "fibre"},
                    {"mot": "avec l'A T P et le calcium", "commande": "play_until", "parametres": {"moment": "ca_et_atp"}},
                    {"mot": "le levier كيطلع", "repere": "levier"},
                    {"mot": "l'A T P بلا calcium", "commande": "play_until", "parametres": {"moment": "sans_ca"}},
                    {"mot": "le calcium بلا A T P", "commande": "play_until", "parametres": {"moment": "sans_atp"}},
                    {"mot": "إذن خاص les ions calcium", "repere": "tableau"}]}},
    {"id": "ex_s2", "slide_type": "simulation", "title": "Question 2 : l'énergie vient de l'hydrolyse de l'ATP",
     "screen_content": {"lead": "ATP + H₂O → ADP + Pi + énergie : l'énergie fait tourner la tête de myosine."},
     "visual": {"kind": "simulation", "url": CYCLE, "caption": "La tête de myosine hydrolyse son ATP et tourne"},
     "speech_text": {"mixed": "la tête de myosine لاصقة ف l'actine. l'A T P ديالها كيوقع ليه l'hydrolyse: A T P plus H deux O donne A D P plus P i plus énergie. شوف: كيخرج P i. هاد l'énergie كتدور la tête، و la tête كتجر l'actine. بلا A T P، ولا يلا l'hydrolyse مسدودة ب le salyrgan، ما كيخرجش P i، ما كايناش l'énergie، و la tête ما كتدورش. هادشي اللي وقع ف les milieux trois et quatre."},
     "concentration": {"demarrer": "reset",
       "centre": [{"texte": "ATP + H₂O → ADP + Pi + énergie", "mot": "A T P plus H deux O"},
                  {"texte": "énergie → rotation de la tête → glissement", "mot": "هاد l'énergie كتدور la tête"},
                  {"texte": "milieux 3 et 4 : pas de Pi, pas d'énergie", "mot": "ما كيخرجش P i"}],
       "pointage": [{"mot": "la tête de myosine لاصقة", "commande": "play_until", "parametres": {"moment": "attachement"}},
                    {"mot": "la tête de myosine لاصقة", "repere": "tete_myosine"},
                    {"mot": "l'A T P ديالها كيوقع", "commande": "play_until", "parametres": {"moment": "hydrolyse_atp"}},
                    {"mot": "شوف: كيخرج P i", "repere": "adp_pi"},
                    {"mot": "هاد l'énergie كتدور la tête", "commande": "play_until", "parametres": {"moment": "rotation"}},
                    {"mot": "و la tête كتجر l'actine", "commande": "play_until", "parametres": {"moment": "glissement"}},
                    {"mot": "و la tête كتجر l'actine", "repere": "sens_glissement"}]}},
    {"id": "ex_s3", "slide_type": "simulation", "title": "Question 3 : la myosine seule hydrolyse peu",
     "screen_content": {"lead": "Myosine seule : Pi faible (4) ; myosine + actine : Pi fort (40). Sans Ca²⁺, les têtes restent seules."},
     "visual": {"kind": "simulation", "url": ATPASE, "caption": "Les trois tubes du cours : actine seule, myosine seule, actine + myosine"},
     "speech_text": {"mixed": "تفكر les trois tubes ديال الدرس. le tube un، l'actine بوحدها: P i égale zéro. le tube deux، la myosine بوحدها: P i égale quatre، hydrolyse ضعيفة. le tube trois، l'actine مع la myosine: P i égale quarante، hydrolyse قوية. ف le milieu deux، بلا calcium، la tropomyosine كتغطي les sites ديال l'actine. les têtes ما يقدروش يتشدو: كيخدمو بحال la myosine بوحدها، P i égale quatre. وحيت ما لاصقينش ف l'actine، ما يقدروش يجروها: ما كايناش contraction."},
     "concentration": {"demarrer": "reset",
       "centre": [{"texte": "myosine seule : Pi = 4 (faible)", "mot": "P i égale quatre، hydrolyse ضعيفة"},
                  {"texte": "myosine + actine : Pi = 40 (forte)", "mot": "P i égale quarante"},
                  {"texte": "milieu 2 : sites cachés → têtes seules → Pi = 4, pas de contraction", "mot": "ف le milieu deux"}],
       "pointage": [{"mot": "تفكر les trois tubes", "commande": "play_until", "parametres": {"moment": "principe"}},
                    {"mot": "le tube un، l'actine", "commande": "play_until", "parametres": {"moment": "tube1"}},
                    {"mot": "le tube un، l'actine", "repere": "tube1"},
                    {"mot": "le tube deux، la myosine", "commande": "play_until", "parametres": {"moment": "tube2"}},
                    {"mot": "le tube deux، la myosine", "repere": "tube2"},
                    {"mot": "le tube trois، l'actine", "commande": "play_until", "parametres": {"moment": "tube3"}},
                    {"mot": "le tube trois، l'actine", "repere": "tube3"},
                    {"mot": "ف le milieu deux", "repere": "tube2"}]}},
    {"id": "ex_s4", "slide_type": "simulation", "title": "Question 4 : le Ca²⁺ lève le blocage de la troponine et de la tropomyosine",
     "screen_content": {"lead": "Sans troponine ni tropomyosine, pas besoin de Ca²⁺ ; avec elles, le Ca²⁺ libère les sites de l'actine."},
     "visual": {"kind": "simulation", "url": CALC, "caption": "La troponine, la tropomyosine et les ions Ca²⁺"},
     "speech_text": {"mixed": "شوف le filament fin complet: l'actine، la tropomyosine، و la troponine. ف الراحة، la tropomyosine كتغطي les sites ديال l'actine: la tête de myosine ما تقدرش تتشد. هادا هو le tube B: hydrolyse ضعيفة. ف le tube A، ما كايناش la tropomyosine: les sites ديما حرين، و l'hydrolyse قوية حتى بلا calcium. دابا le calcium كيوصل: كيلصق على la troponine. la tropomyosine كتزاح، و les sites كيتحررو: هادا هو le tube C، hydrolyse قوية. إذن le calcium ما كيخدمش على la myosine، كيحيد المنع."},
     "concentration": {"demarrer": "reset",
       "centre": [{"texte": "B : sites cachés par la tropomyosine → Pi faible", "mot": "هادا هو le tube B"},
                  {"texte": "A : sans tropomyosine, sites libres → Pi fort sans Ca²⁺", "mot": "ف le tube A"},
                  {"texte": "C : Ca²⁺ sur la troponine → sites libérés → Pi fort", "mot": "هادا هو le tube C"},
                  {"texte": "le Ca²⁺ lève le blocage, il n'active pas la myosine", "mot": "كيحيد المنع"}],
       "pointage": [{"mot": "شوف le filament fin complet", "commande": "play_until", "parametres": {"moment": "repos_sites_caches"}},
                    {"mot": "شوف le filament fin complet", "repere": "actine"},
                    {"mot": "ف الراحة، la tropomyosine", "repere": "tropomyosine"},
                    {"mot": "دابا le calcium كيوصل", "commande": "play_until", "parametres": {"moment": "ca_sur_troponine"}},
                    {"mot": "كيلصق على la troponine", "repere": "troponine"},
                    {"mot": "la tropomyosine كتزاح", "commande": "play_until", "parametres": {"moment": "sites_liberes"}},
                    {"mot": "و les sites كيتحررو", "repere": "site_actine"}]}},
    {"id": "ex_s5", "slide_type": "simulation", "title": "Question 5 : l'hydrolyse de l'ATP et la chaleur initiale",
     "screen_content": {"lead": "Chaleur initiale : hydrolyse de l'ATP + phosphocréatine (sans O₂). Chaleur retardée : respiration."},
     "visual": {"kind": "simulation", "url": CHAL, "caption": "La chaleur d'un muscle entier, avec puis sans dioxygène"},
     "speech_text": {"mixed": "ف muscle كامل، pendant la secousse، كتخرج la chaleur initiale. هي كتجي من l'hydrolyse ديال l'A T P، بحال ف le milieu un، ومن la régénération السريعة ب la phosphocréatine. من بعد la secousse، كتخرج la chaleur retardée: كتجي من la respiration. دابا بلا dioxygène: la chaleur initiale هي هي، حيت هاد les réactions ما محتاجينش le dioxygène. ولكن la chaleur retardée ما جاتش، حيت la respiration محتاجة le dioxygène."},
     "concentration": {"demarrer": "reset",
       "centre": [{"texte": "chaleur initiale : hydrolyse de l'ATP + phosphocréatine", "mot": "كتخرج la chaleur initiale"},
                  {"texte": "chaleur retardée : respiration", "mot": "كتخرج la chaleur retardée"},
                  {"texte": "sans O₂ : initiale seule", "mot": "دابا بلا dioxygène"}],
       "pointage": [{"mot": "ف muscle كامل", "commande": "play_until", "parametres": {"moment": "origines"}},
                    {"mot": "كتخرج la chaleur initiale", "repere": "chaleur_initiale"},
                    {"mot": "ومن la régénération السريعة", "repere": "origine_initiale"},
                    {"mot": "كتخرج la chaleur retardée", "repere": "origine_retardee"},
                    {"mot": "دابا بلا dioxygène", "commande": "play_until", "parametres": {"moment": "sans_dioxygene"}},
                    {"mot": "ولكن la chaleur retardée ما جاتش", "repere": "chaleur_retardee"}]}}
  ]}]},
  "facile": {"activities": [{"id": "facile", "title": "Plus facile, pour s'entraîner", "slides": [
    vrai_faux("fa_s1", "Plus facile : lire le document 1", "Vrai ou faux, d'après le document 1.",
      "نتمرنو على le document un: قول واش صحيح ولا خطأ.",
      [("Sans ions Ca²⁺ (milieu 2), les myofibrilles ne se contractent pas.", True, "Vrai : milieu 2, pas de contraction."),
       ("L'ATP seul suffit à la contraction.", False, "Faux : le milieu 2 a de l'ATP mais pas de Ca²⁺, et ne se contracte pas."),
       ("Dans le milieu 4, il y a de l'ATP et du Ca²⁺, mais pas de contraction.", True, "Vrai : le salyrgan bloque l'hydrolyse de l'ATP."),
       ("Le milieu 3 libère du Pi.", False, "Faux : sans ATP, rien à hydrolyser : Pi = 0.")]),
    qcm_facile("fa_s2", "Plus facile : d'où vient l'énergie ?", "سؤال ساهل على l'énergie.",
      "L'énergie qui fait tourner les têtes de myosine vient…", ["des ions Ca²⁺ fixés sur la troponine", "de l'hydrolyse de l'ATP", "du salyrgan"], 1, {
        "1": {"juste": rep("برافو! l'hydrolyse ديال l'A T P كتعطي l'énergie اللي كتدور la tête.", "Juste : l'hydrolyse de l'ATP.")},
        "0": {"1": rep("ما تقلقش. le calcium كيحل les sites، ولكن واش كيعطي l'énergie؟ عاود اختار.", "Le Ca²⁺ libère les sites, mais donne-t-il l'énergie ? Réessaie."),
              "2": rep("الجواب هو l'hydrolyse ديال l'A T P. le calcium autorise، ما كيعطيش l'énergie.", "Réponse : l'hydrolyse de l'ATP ; le Ca²⁺ autorise seulement.")},
        "2": {"1": rep("لا، le salyrgan كيمنع l'hydrolyse، ما كيعطيش l'énergie. عاود اختار.", "Le salyrgan bloque l'hydrolyse. Réessaie."),
              "2": rep("الجواب هو l'hydrolyse ديال l'A T P.", "Réponse : l'hydrolyse de l'ATP.")}},
      "L'énergie qui fait tourner les têtes de myosine vient ?"),
    qcm_facile("fa_s3", "Plus facile : la myosine seule", "سؤال ساهل على l'activité A T P asique.",
      "Une myosine qui n'est pas fixée à l'actine hydrolyse l'ATP…", ["faiblement", "fortement", "pas du tout"], 0, {
        "0": {"juste": rep("برافو! la myosine بوحدها كتدير hydrolyse ضعيفة، وملي كتلصق ف l'actine كتولي قوية.", "Juste : faiblement ; fixée à l'actine, fortement.")},
        "1": {"1": rep("ما تقلقش. تفكر le tube ديال la myosine بوحدها ف الدرس: شحال كان P i؟ عاود اختار.", "Pense au tube « myosine seule » du cours. Réessaie."),
              "2": rep("الجواب هو ضعيفة. قوية غير ملي كتلصق ف l'actine.", "Réponse : faiblement ; fortement seulement liée à l'actine.")},
        "2": {"1": rep("لا، l'actine بوحدها هي اللي ما كتديرش hydrolyse. la myosine بوحدها؟ عاود اختار.", "C'est l'actine seule qui n'hydrolyse pas. Réessaie."),
              "2": rep("الجواب هو ضعيفة: la myosine est une A T P ase، حتى بوحدها.", "Réponse : faiblement.")}},
      "Une myosine qui n'est pas fixée à l'actine hydrolyse l'ATP ?"),
    association("fa_s4", "Plus facile : chaque tube et son explication", "Relie chaque tube du document 2 à son explication.",
      "سؤال ساهل: ربط كل tube مع الشرح ديالو.", "Relie chaque tube à ce qui explique son résultat.",
      [("A", "Tube A : actine pure, sans Ca²⁺ → Pi fort"), ("B", "Tube B : filaments complets, sans Ca²⁺ → Pi faible"), ("C", "Tube C : filaments complets, avec Ca²⁺ → Pi fort")],
      [("a", "Pas de tropomyosine : les sites de l'actine sont toujours libres"), ("b", "La tropomyosine cache les sites de l'actine"), ("c", "Le Ca²⁺ se fixe sur la troponine : la tropomyosine libère les sites")],
      {"A": "a", "B": "b", "C": "c"},
      {"A-a": (True, "Oui : sans tropomyosine, rien ne cache les sites : la myosine se fixe, même sans Ca²⁺.", "برافو: بلا tropomyosine، les sites ديما حرين."),
       "A-b": (False, "Non : dans le tube A, il n'y a pas de tropomyosine.", "لا، ف le tube A ما كايناش la tropomyosine."),
       "A-c": (False, "Non : le tube A n'a pas de Ca²⁺.", "لا، le tube A ما فيهش le calcium."),
       "B-a": (False, "Non : le tube B a de la tropomyosine.", "لا، le tube B فيه la tropomyosine."),
       "B-b": (True, "Oui : sans Ca²⁺, la tropomyosine cache les sites : la myosine reste seule, hydrolyse faible.", "برافو: la tropomyosine كتغطي les sites، و l'hydrolyse ضعيفة."),
       "B-c": (False, "Non : le tube B n'a pas de Ca²⁺.", "لا، le tube B ما فيهش le calcium."),
       "C-a": (False, "Non : le tube C contient la tropomyosine.", "لا، le tube C فيه la tropomyosine."),
       "C-b": (False, "Non : dans le tube C, le Ca²⁺ a libéré les sites.", "لا، ف le tube C، le calcium حرر les sites."),
       "C-c": (True, "Oui : le Ca²⁺ sur la troponine déplace la tropomyosine : sites libres, hydrolyse forte.", "برافو: le calcium على la troponine، و les sites كيتحررو.")},
      ("(A ; a) (B ; b) (C ; c) : le Ca²⁺ lève le blocage de la troponine et de la tropomyosine.",
       "le calcium كيحيد المنع ديال la troponine و la tropomyosine.")),
    association("fa_s5", "Plus facile : chaque chaleur et son origine", "Relie chaque chaleur à son origine.",
      "سؤال ساهل: ربط كل chaleur مع منين كتجي.", "Relie chaque chaleur à son origine.",
      [("1", "Chaleur initiale (pendant la secousse)"), ("2", "Chaleur retardée (après la secousse)")],
      [("a", "Hydrolyse de l'ATP et phosphocréatine, sans O₂"), ("b", "Respiration, avec O₂"), ("c", "Fermentation alcoolique")],
      {"1": "a", "2": "b"},
      {"1-a": (True, "Oui : réactions rapides sans dioxygène : elle existe même sans O₂.", "برافو: des réactions سريعة بلا dioxygène."),
       "1-b": (False, "Non : la respiration donne la chaleur retardée, pas l'initiale.", "لا، la respiration كتعطي la chaleur retardée."),
       "1-c": (False, "Non : le muscle ne fait pas de fermentation alcoolique.", "لا، le muscle ما كيديرش la fermentation alcoolique."),
       "2-a": (False, "Non : la phosphocréatine agit pendant la secousse : chaleur initiale.", "لا، la phosphocréatine كتخدم ف la secousse: la chaleur initiale."),
       "2-b": (True, "Oui : la chaleur retardée vient de la respiration ; elle disparaît sans O₂.", "برافو: la chaleur retardée كتجي من la respiration."),
       "2-c": (False, "Non : le muscle ne fait pas de fermentation alcoolique.", "لا، le muscle ما كيديرش la fermentation alcoolique.")},
      ("(1 ; a) (2 ; b) ; la fermentation alcoolique est en trop.", "la chaleur initiale: l'A T P و la phosphocréatine. la chaleur retardée: la respiration."))
  ]}]},
  "similaire": {
    "id": "svt_ex_ch2_calcium_atpase_1_b", "titre": "Même exercice, autres données",
    "enonce": {
      "intro": "Mêmes expériences avec des myofibrilles et une myosine extraites d'un autre muscle. Les documents 1 et 2 donnent les résultats.",
      "intro_dit": "نفس التجارب، ب des myofibrilles و la myosine ديال muscle آخر. le document un و le document deux فيهم les résultats.",
      "figures": [doc1(PI1B), doc2(PI2B)],
      "donnees": ["Pi libéré : mesure l'ATP hydrolysé", "Salyrgan : bloque l'hydrolyse de l'ATP"],
      "questions": [
        {"id": "1", "texte": "Comparer les résultats des milieux 2, 3 et 4 à ceux du milieu 1, puis en déduire les conditions nécessaires à la contraction.",
         "reponse": {"type": "phrase", "attendu": "Milieu 1 : contraction, Pi = 30 UA. Milieu 2 (sans Ca²⁺) : pas de contraction, Pi = 3 UA contre 30. Milieux 3 (sans ATP) et 4 (salyrgan) : pas de contraction, Pi = 0. Conditions : ions Ca²⁺, ATP et hydrolyse de l'ATP."},
         "clavier": {"aides": ["contre 30 UA", "Ca²⁺", "ATP", "hydrolyse"], "pieges": ["l'ATP suffit"]},
         "correction": {"lignes": [{"texte": "1 : milieu 2 : Pi 3 contre 30, pas de contraction ; milieux 3 et 4 : Pi = 0, pas de contraction", "mot": "le milieu deux"},
                                   {"texte": "conditions : Ca²⁺ + ATP + hydrolyse de l'ATP", "mot": "محتاجة"}],
                        "parole": "Question un. le milieu deux، بلا calcium: P i égale trois contre trente، وما كايناش contraction. les milieux trois et quatre: P i égale zéro، ما كايناش contraction. إذن la contraction محتاجة le calcium، l'A T P، و l'hydrolyse ديالو."}},
        {"id": "2", "texte": "Expliquer l'absence de contraction dans les milieux 3 et 4, en précisant d'où vient l'énergie de la contraction.",
         "reponse": {"type": "phrase", "attendu": "L'énergie vient de l'hydrolyse de l'ATP par la tête de myosine (ATPase) : ATP + H₂O → ADP + Pi + énergie, qui fait tourner les têtes et glisser l'actine. Milieu 3 : pas d'ATP ; milieu 4 : ATP non hydrolysé ; donc pas de Pi, pas d'énergie, pas de contraction."},
         "clavier": {"aides": ["hydrolyse", "ATPase", "rotation des têtes"], "pieges": ["le Ca²⁺ donne l'énergie"]},
         "correction": {"lignes": [{"texte": "2 : énergie : ATP + H₂O → ADP + Pi + énergie (tête de myosine)", "mot": "A T P plus H deux O"},
                                   {"texte": "milieux 3 et 4 : pas d'hydrolyse → pas d'énergie → pas de contraction", "mot": "ما كايناش l'énergie"}],
                        "parole": "Question deux. A T P plus H deux O donne A D P plus P i plus énergie، و هاد l'énergie كتدور les têtes. ف les milieux trois et quatre، ما كايناش l'hydrolyse: ما كايناش l'énergie، وما كايناش contraction."}},
        {"id": "3", "texte": "Dans le milieu 2, un peu d'ATP est hydrolysé (Pi = 3 UA) sans contraction. Expliquer ce résultat.",
         "reponse": {"type": "phrase", "attendu": "Sans Ca²⁺, la tropomyosine cache les sites de l'actine : pas de complexe actomyosine. La myosine seule hydrolyse faiblement l'ATP (3 UA, contre 30 UA liée à l'actine) ; ses têtes non fixées ne peuvent pas tirer l'actine : pas de contraction."},
         "clavier": {"aides": ["tropomyosine", "myosine seule", "hydrolyse faible"], "pieges": ["l'actine hydrolyse l'ATP"]},
         "correction": {"lignes": [{"texte": "3 : sites cachés → pas de complexe actomyosine → myosine seule : hydrolyse faible (3 UA)", "mot": "la tropomyosine"},
                                   {"texte": "têtes non fixées → pas de glissement → pas de contraction", "mot": "ما كايناش contraction"}],
                        "parole": "Question trois. بلا calcium، la tropomyosine كتغطي les sites: la myosine كتبقى بوحدها، و l'hydrolyse ضعيفة. les têtes ما لاصقينش ف l'actine، إذن ما كايناش contraction."}},
        {"id": "4", "texte": "En exploitant le document 2, comparer les tubes A et B, puis B et C. En déduire comment agissent les ions Ca²⁺.",
         "reponse": {"type": "phrase", "attendu": "A (actine pure, sans Ca²⁺) : 30 UA contre B (filaments complets, sans Ca²⁺) : 3 UA : la troponine et la tropomyosine bloquent la liaison actine-myosine. B : 3 UA contre C (avec Ca²⁺) : 30 UA : le Ca²⁺ lève ce blocage. Le Ca²⁺ n'agit pas sur la myosine : il se fixe sur la troponine, la tropomyosine libère les sites, le complexe actomyosine se forme et l'hydrolyse devient forte."},
         "clavier": {"aides": ["troponine", "tropomyosine", "lève le blocage"], "pieges": ["le Ca²⁺ active la myosine"]},
         "correction": {"lignes": [{"texte": "4 : A 30 contre B 3 : troponine + tropomyosine bloquent ; B 3 contre C 30 : le Ca²⁺ lève le blocage", "mot": "le tube A"},
                                   {"texte": "Ca²⁺ sur la troponine → sites libérés → complexe actomyosine", "mot": "la troponine"}],
                        "parole": "Question quatre. le tube A، trente، contre le tube B، trois: la troponine و la tropomyosine كيمنعو la liaison. le tube C، trente: le calcium كيحيد المنع، كيلصق على la troponine، و les sites كيتحررو."}},
        {"id": "5", "texte": "Relier la chaleur dégagée dans le milieu 1 à la chaleur initiale d'un muscle entier, puis expliquer pourquoi un muscle privé de dioxygène ne dégage pas de chaleur retardée.",
         "reponse": {"type": "phrase", "attendu": "La chaleur vient de l'hydrolyse de l'ATP (une partie de l'énergie libérée). Chaleur initiale : hydrolyse de l'ATP et régénération par la phosphocréatine, sans dioxygène. Chaleur retardée : régénération de l'ATP par la respiration ; sans dioxygène, pas de respiration, donc pas de chaleur retardée."},
         "clavier": {"aides": ["chaleur initiale", "phosphocréatine", "respiration"], "pieges": ["chaleur initiale = respiration"]},
         "correction": {"lignes": [{"texte": "5 : chaleur initiale : hydrolyse de l'ATP + phosphocréatine (sans O₂)", "mot": "la chaleur initiale"},
                                   {"texte": "chaleur retardée : respiration → absente sans O₂", "mot": "la chaleur retardée"}],
                        "parole": "Question cinq. la chaleur initiale كتجي من l'hydrolyse ديال l'A T P و la phosphocréatine، بلا dioxygène. la chaleur retardée كتجي من la respiration، إذن بلا dioxygène ما كتجيش."}}
      ]}}
}
ecrire(EX, sys.argv[1])
