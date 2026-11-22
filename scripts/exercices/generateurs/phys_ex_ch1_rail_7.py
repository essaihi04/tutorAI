# Exercice de physique (ch. 1, ondes mécaniques progressives), niveau DIFFICILE (« Supérieur ») : deux sons, un rail.
# Sources comparées (skill exercices § 2) :
# - experience_profs.json « ondes_mecaniques » : cas type « deux_milieux » (t₁ = L/v₁, t₂ = L/v₂ ; le milieu le plus
#   lent arrive en dernier : τ = L(1/v_lent − 1/v_rapide) > 0 ; mettre au même dénominateur avant d'inverser),
#   pièges « retard négatif entre deux milieux », « inverser une différence de fractions terme à terme »,
#   insistance « la célérité dépend du milieu, jamais de l'amplitude », valeurs repères (air ≈ 340 m/s vers 20 °C,
#   métal de 4000 à 6000 m/s), a_ne_pas_dire « plus dense donc plus rapide » et « 340 m/s toujours » ;
# - exploration ondes_mecaniques_periodiques.json (partie ch1, cadre et pièges d'unités) ;
# - le cours phys_ch1_waves_exemple, diapos wx_c2_facteurs et wx_c2b_temperature (milieux.html) : nature du milieu,
#   température de l'air (qualitatif : air chaud → son plus rapide ; 340 m/s vers 20 °C), frappe plus forte sans
#   effet sur v : la question 6 n'utilise que ce qui y est enseigné ;
# - nationaux comparés : 2018 N ex. 2 (ultrasons dans l'air et le pétrole, même L = 1,84 m connue, « montrer que
#   τ = L(1/V_air − 1/V_p) » puis trouver V_p), 2021 R ex. 2 (barre métallique, droite Δt = f(d), identifier le
#   métal). Le nôtre : un coup de marteau sur un rail, l'inconnue est la DISTANCE d (vitesses connues), puis les
#   deux dates d'arrivée, l'effet de l'amplitude et une lecture critique sur la température : autre situation,
#   autres données, autre chaîne ;
# - séries en ligne : la recherche signale l'exercice classique « l'oreille contre le rail » (moutamadris, série
#   « 2bac international », v_acier = 5000 m/s, v_air ≈ 343 m/s) et un corrigé à 5600 m/s ; lecture des pages
#   bloquée par le réseau de la session (talamidi.com, moutamadris.ma, dreamjob.ma non résolus) ; rien recopié.
# Simulation : ondes-tableau/milieux.html (d = 1 km ; acier 5000 m/s → 0,20 s ; air v ≈ 331,3·√(1 + θ/273,15),
# 343 m/s à 20 °C → 2,9 s ; 355 m/s à 40 °C → 2,8 s ; piste « air frappé plus fort ») : la voix décrit la
# simulation avec SES valeurs, puis « فالتمرين » applique celles de l'exercice (340 et 5000 m/s).
import sys, os, re, importlib.util
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _outils import *

_TP = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "backend", "kaggle_tts", "texte_parle.py")
_sp = importlib.util.spec_from_file_location("tp", _TP); tp = importlib.util.module_from_spec(_sp); _sp.loader.exec_module(tp)


def dire(x, dec=3):
    s = fr(x, dec)
    m = re.match(r"(\d+),(\d+)$", s)
    return tp._decimal_fr(m) if m else tp.nombre_fr(int(s))


SIM = "/media/simulations/physics/ondes-tableau/milieux.html"
# valeurs affichées par la simulation (mêmes formules que milieux.html)
SIM_D = 1000
SIM_VACIER = 5000
sim_vair = lambda th: round(331.3 * math.sqrt(1 + th / 273.15))
SIM_TACIER = SIM_D / SIM_VACIER                 # 0,2 s
SIM_TAIR20 = SIM_D / sim_vair(20)               # 2,9 s affiché
SIM_TAIR40 = SIM_D / sim_vair(40)               # 2,8 s affiché
assert fr(SIM_TACIER, 2) == "0,2" and fr(SIM_TAIR20, 1) == "2,9" and fr(SIM_TAIR40, 1) == "2,8" and sim_vair(40) == 355


def donnees(d, va=340, vs=5000):
    D = dict(va=va, vs=vs)
    D["dt"] = round(d * (1 / va - 1 / vs), 2)              # la donnée mesurée (2 décimales)
    D["d"] = round(D["dt"] / (1 / va - 1 / vs), 6)                  # ce que l'élève retrouve
    D["ts"] = D["d"] / vs
    D["ta"] = D["ts"] + D["dt"]
    assert abs(D["d"] - d) < 0.5 and abs(D["ta"] - d / va) < 1e-6
    return D


A = donnees(850)      # Δt = 2,33 s ; t_acier = 0,17 s ; t_air = 2,5 s
B = donnees(1700)     # Δt = 4,66 s ; t_acier = 0,34 s ; t_air = 5 s


def figures(D):
    f1 = {"type": "schema", "titre": "Le dispositif", "cadre": {"l": 10, "h": 4},
          "legende": "Le coup de marteau en A, à t = 0 ; en B, un capteur fixé sur le rail et un microphone dans l'air.",
          "elements": [
              {"f": "rect", "de": [0.8, 1.2], "a": [9.2, 1.5], "couleur": "blanc", "remplir": "faible"},
              {"f": "texte", "at": [0.4, 1.35], "t": "A", "couleur": "jaune", "taille": "grand"},
              {"f": "texte", "at": [9.6, 1.35], "t": "B", "couleur": "jaune", "taille": "grand"},
              {"f": "fleche", "de": [0.3, 2.6], "a": [0.85, 1.6], "couleur": "orange", "texte": "marteau", "pos": "n"},
              {"f": "fleche", "de": [1.2, 1.0], "a": [8.8, 1.0], "couleur": "cyan", "texte": "son dans le rail (acier)", "pos": "s"},
              {"f": "fleche", "de": [1.2, 2.5], "a": [8.8, 2.5], "couleur": "jaune", "texte": "son dans l'air", "pos": "n"},
              {"f": "point", "at": [9.2, 1.5], "couleur": "vert", "t": "capteur", "pos": "se"},
              {"f": "point", "at": [9.2, 2.5], "couleur": "vert", "t": "micro", "pos": "ne"},
              {"f": "cote", "de": [0.8, 0.3], "a": [9.2, 0.3], "t": "d = AB", "couleur": "blanc", "pos": "n"}]}
    X = lambda t: 0.6 + t * 8.4 / D["ta"]
    def salve(t, y, a):
        return [[round(X(t) + 0.5 * i / 30, 3), round(y + a * math.exp(-3 * i / 30) * math.sin(22 * i / 30), 3)] for i in range(31)]
    y1, y2 = 2.6, 1.3
    el = [{"f": "ligne", "pts": [[0.6, y1], [X(D["ts"]), y1]] + salve(D["ts"], y1, 0.5) + [[9.6, y1]], "couleur": "cyan", "epais": True},
          {"f": "ligne", "pts": [[0.6, y2], [X(D["ta"]), y2]] + salve(D["ta"], y2, 0.5) + [[9.6, y2]], "couleur": "jaune", "epais": True},
          {"f": "texte", "at": [0.6, y1 + 0.75], "t": "capteur sur le rail", "couleur": "cyan", "ancre": "gauche", "taille": "petit"},
          {"f": "texte", "at": [0.6, y2 + 0.75], "t": "microphone dans l'air", "couleur": "jaune", "ancre": "gauche", "taille": "petit"},
          {"f": "ligne", "pts": [[X(D["ts"]), y1], [X(D["ts"]), 0.4]], "couleur": "faible", "trait": "pointille"},
          {"f": "ligne", "pts": [[X(D["ta"]), y2], [X(D["ta"]), 0.4]], "couleur": "faible", "trait": "pointille"},
          {"f": "cote", "de": [X(D["ts"]), 0.4], "a": [X(D["ta"]), 0.4], "t": f"Δt = {fr(D['dt'])} s", "couleur": "vert", "pos": "n"},
          {"f": "fleche", "de": [0.6, 0.1], "a": [9.7, 0.1], "couleur": "blanc", "texte": "t", "pos": "s"}]
    f2 = {"type": "schema", "titre": "Les deux arrivées en B", "cadre": {"l": 10, "h": 3.6},
          "legende": "L'enregistrement ne donne que la durée Δt entre les deux arrivées.", "elements": el}
    return [f1, f2]


def intro(D):
    return ("Un ouvrier donne, à la date t = 0, un coup de marteau sur l'extrémité A d'un long rail d'acier rectiligne. "
            "À l'autre extrémité B, à la distance d = AB inconnue, un capteur fixé sur le rail et un microphone placé dans "
            "l'air, tout près, enregistrent l'arrivée du son. Le son arrive deux fois en B : une fois par le rail, une fois "
            f"par l'air. La durée qui sépare les deux arrivées est Δt = {fr(D['dt'])} s.")


def donnees_txt(D):
    return [f"Célérité du son dans l'acier : v_acier = {D['vs']} m/s",
            f"Célérité du son dans l'air (vers 20 °C) : v_air = {D['va']} m/s",
            f"Durée entre les deux arrivées : Δt = {fr(D['dt'])} s"]


ATT1 = ("Le son du rail arrive le premier : les deux sons parcourent la même distance d, et t = d/v ; "
        "comme v_acier > v_air, la durée dans l'acier est la plus petite.")
ATT2 = ("t_acier = d/v_acier et t_air = d/v_air. Le son de l'air arrive en dernier : Δt = t_air − t_acier = d/v_air − d/v_acier, "
        "donc Δt = d·(1/v_air − 1/v_acier).")


def att3(D):
    return f"d = Δt/(1/v_air − 1/v_acier) = {fr(D['dt'])}/(1/{D['va']} − 1/{D['vs']}) = {fr(D['d'], 0)} m"


def att4(D):
    return (f"t_acier = d/v_acier = {fr(D['d'], 0)}/{D['vs']} = {fr(D['ts'])} s ; "
            f"t_air = t_acier + Δt = {fr(D['ts'])} + {fr(D['dt'])} = {fr(D['ta'])} s")


ATT5 = ("Non. La célérité dépend du milieu (acier, air), pas de l'amplitude de la perturbation : frapper plus fort ne change "
        "ni v_acier ni v_air, donc ni t_acier, ni t_air, ni Δt.")


def att6(D):
    return ("Le raisonnement est faux : le rail n'a pas changé de longueur. Dans l'air plus chaud, le son va plus vite : "
            f"v_air est plus grande que {D['va']} m/s, donc t_air = d/v_air diminue et Δt' < Δt. La valeur {D['va']} m/s n'est valable "
            "que vers 20 °C ; en la gardant, l'élève attribue à d une baisse qui vient de v_air.")


def corr1(D):
    return correction([
        ("1 : même distance d pour les deux sons, et t = d/v", "t égale d sur v"),
        ("v_acier > v_air, donc t_acier < t_air", "v acier كبيرة"),
        ("le son du rail arrive le premier", "le son ديال le rail كيوصل اللول")],
        "la question un. les deux sons كيقطعو نفس la distance d، وt égale d sur v. "
        "v acier كبيرة بزاف من v air، إذن t acier صغير. إذن le son ديال le rail كيوصل اللول.")


def corr2():
    return correction([
        ("2 : t_acier = d/v_acier ; t_air = d/v_air", "t acier égale d sur v acier"),
        ("Δt = t_air − t_acier = d/v_air − d/v_acier", "delta t égale t air moins t acier"),
        ("Δt = d·(1/v_air − 1/v_acier)", "delta t égale d fois")],
        "la question deux. t acier égale d sur v acier، وt air égale d sur v air. "
        "le son ديال الهوا كيوصل اللخر، إذن delta t égale t air moins t acier، égale d sur v air moins d sur v acier. "
        "ونخرجو d: delta t égale d fois، un sur v air، moins un sur v acier.")


def corr3(D):
    return correction([
        ("3 : d = Δt/(1/v_air − 1/v_acier)", "d égale delta t sur"),
        (f"d = {fr(D['dt'])}/(1/{D['va']} − 1/{D['vs']})", f"égale {dire(D['dt'])} sur"),
        (f"d = {fr(D['d'], 0)} m", f"d égale {dire(round(D['d']), 0)} mètres")],
        "la question trois. من la relation، d égale delta t sur، un sur v air moins un sur v acier. "
        f"d égale {dire(D['dt'])} sur، un sur {dire(D['va'])} moins un sur {dire(D['vs'])}. "
        f"d égale {dire(round(D['d']), 0)} mètres.")


def corr4(D):
    return correction([
        (f"4 : t_acier = d/v_acier = {fr(D['d'], 0)}/{D['vs']} = {fr(D['ts'])} s", f"t acier égale {dire(round(D['d']), 0)} sur {dire(D['vs'])}"),
        ("le son de l'air arrive Δt plus tard : t_air = t_acier + Δt", "t air égale t acier plus delta t"),
        (f"t_air = {fr(D['ts'])} + {fr(D['dt'])} = {fr(D['ta'])} s", f"t air égale {dire(D['ta'])} secondes")],
        f"la question quatre. t acier égale d sur v acier: t acier égale {dire(round(D['d']), 0)} sur {dire(D['vs'])}، "
        f"égale {dire(D['ts'])} seconde. le son ديال الهوا كيوصل من بعد ب delta t. إذن t air égale t acier plus delta t، "
        f"égale {dire(D['ts'])} plus {dire(D['dt'])}. t air égale {dire(D['ta'])} secondes.")


def corr5():
    return correction([
        ("5 : la célérité dépend du milieu, pas de l'amplitude", "la célérité كتبدل مع le milieu"),
        ("v_acier et v_air ne changent pas : t_acier, t_air et Δt non plus", "delta t كتبقى هي هي"),
        ("Δt ne change pas.", "إذن non")],
        "la question cinq. la célérité كتبدل مع le milieu، ماشي مع l'amplitude. ملي كنضربو بزاف، v acier وv air ما كيتبدلوش. "
        "إذن t acier وt air ما كيتبدلوش، وdelta t كتبقى هي هي. إذن non، delta t ما كتبدلش.")


def corr6(D):
    return correction([
        ("6 : le rail n'a pas changé : d est la même", "le rail ما تبدلش"),
        (f"air plus chaud : v_air > {D['va']} m/s, t_air = d/v_air diminue, donc Δt' < Δt", "v air كتكبر"),
        (f"{D['va']} m/s ne vaut que vers 20 °C : l'erreur vient de v_air, pas de d", "الغلط ماشي فd")],
        "la question six. le rail ما تبدلش، إذن d هي هي. فالهوا السخون، le son كيمشي بالزربة: v air كتكبر. "
        "إذن t air égale d sur v air كيصغر، وdelta t كيصغر. "
        f"la valeur {dire(D['va'])} mètres par seconde، valable vers vingt degrés Celsius. "
        "التلميذ خدم بها à quarante degrés: الغلط ماشي فd، الغلط فv air. إذن le raisonnement est faux.")


CL1 = {"aides": ["t = d/v", "v_acier", "v_air", "même distance"], "pieges": ["v_air > v_acier", "plus dense"]}
CL2 = {"aides": ["t_acier = d/v_acier", "t_air = d/v_air", "Δt = t_air − t_acier"], "pieges": ["Δt = t_acier − t_air", "Δt = d/(v_air − v_acier)"]}
CL3 = {"aides": ["Δt = d·(1/v_air − 1/v_acier)", "A.N. :", "m"], "pieges": ["d = Δt·(1/v_air − 1/v_acier)", "d = Δt·v_air"]}
CL4 = {"aides": ["t_acier = d/v_acier", "t_air = t_acier + Δt", "A.N. :", "s"], "pieges": ["t_air = t_acier − Δt", "t_air = Δt"]}
CL5 = {"aides": ["célérité", "milieu", "amplitude"], "pieges": ["Δt diminue", "plus fort donc plus vite"]}
CL6 = {"aides": ["température", "v_air", "t_air = d/v_air", "20 °C"], "pieges": ["le rail est plus court", "340 m/s toujours"]}


def questions(D, sim=False):
    return [
      {"id": "1", "texte": "Lequel des deux sons arrive le premier en B ? Justifier sans calcul."},
      {"id": "2", "texte": "Exprimer les durées de propagation t_acier et t_air en fonction de d, puis montrer que Δt = d·(1/v_air − 1/v_acier)."},
      {"id": "3", "texte": "Calculer la longueur d du rail."},
      {"id": "4", "texte": "Calculer la durée t_acier, puis en déduire la date t_air d'arrivée du son dans l'air."},
      {"id": "5", "texte": "L'ouvrier refait l'expérience en frappant beaucoup plus fort. La durée Δt mesurée change-t-elle ? Justifier."},
      {"id": "6", "texte": (f"Un jour d'été, l'air est à 40 °C. Avec le même rail, on mesure une durée Δt' un peu plus petite que {fr(D['dt'])} s. "
                            f"Un élève refait le calcul de la question 3 avec v_air = {D['va']} m/s et conclut que le rail est plus court. Critiquer ce raisonnement.")},
    ]


Q = questions(A)
Q[0].update({"texte_dit": "la question un: شكون من les deux sons كيوصل اللول ل B؟ justifier بلا حساب.",
             "reponse": phrase(ATT1), "clavier": CL1,
             "aides": [aide("Les deux sons partent ensemble de A et font la même distance d : qu'est-ce qui les distingue ?",
                            "les deux sons كيخرجو فنفس الوقت من A، وكيقطعو نفس la distance d. شنو اللي مختلف بيناتهم؟"),
                       aide("t = d/v : pour la même distance, la plus grande célérité donne la plus petite durée.",
                            "t égale d sur v. فنفس la distance، اللي عندو la célérité كبيرة، كياخد وقت صغير.")],
             "correction": corr1(A), "explication": "ex_r1", "facile": "fa_r1"})
Q[1].update({"texte_dit": "la question deux: كتب t acier وt air en fonction de d، ومن بعد بين بلي delta t égale d fois، un sur v air، moins un sur v acier.",
             "reponse": phrase(ATT2), "clavier": CL2,
             "aides": [aide("Pour chaque milieu, v = d/t : isole t.",
                            "فكل milieu، v égale d sur t. خرج t."),
                       aide("Le son de l'air arrive en dernier : Δt = t_air − t_acier, puis mets d en facteur.",
                            "le son ديال الهوا كيوصل اللخر: delta t égale t air moins t acier. ومن بعد خرج d facteur.")],
             "correction": corr2(), "explication": "ex_r2", "facile": "fa_r2"})
Q[2].update({"texte_dit": "la question trois: حسب la longueur d ديال le rail.",
             "reponse": valeur("d", A["d"], "m", att3(A)), "clavier": CL3,
             "aides": [aide("Dans la relation de la question 2, tout est connu sauf d.",
                            "فla relation ديال la question deux، كلشي معروف من غير d."),
                       aide("Divise Δt par la parenthèse entière (1/v_air − 1/v_acier) ; n'inverse pas chaque fraction séparément.",
                            "قسم delta t على la parenthèse كاملة، un sur v air moins un sur v acier. ما تقلبش كل fraction بوحدها.")],
             "correction": corr3(A), "explication": "ex_r3", "facile": "fa_r3"})
Q[3].update({"texte_dit": "la question quatre: حسب la durée t acier، ومن بعد déduire t air.",
             "reponse": valeur("t_air", A["ta"], "s", att4(A)), "clavier": CL4,
             "aides": [aide("t_acier = d/v_acier avec le d trouvé.",
                            "t acier égale d sur v acier، بd اللي لقيتي."),
                       aide("Le son de l'air arrive Δt après celui du rail.",
                            "le son ديال الهوا كيوصل من بعد le son ديال le rail ب delta t.")],
             "correction": corr4(A), "explication": "ex_r4", "facile": "fa_r4"})
Q[4].update({"texte_dit": "la question cinq: التلميذ ضرب le rail بزاف. واش delta t كتبدل؟ justifier.",
             "reponse": phrase(ATT5), "clavier": CL5,
             "aides": [aide("Frapper plus fort change l'amplitude de la perturbation. Est-ce que la célérité dépend de l'amplitude ?",
                            "ملي كنضربو بزاف، كتبدل l'amplitude. واش la célérité كتبدل مع l'amplitude؟"),
                       aide("La célérité dépend du milieu : t_acier et t_air dépendent de d et de v seulement.",
                            "la célérité كتبدل مع le milieu. t acier وt air كيتبدلو غير مع d وv.")],
             "correction": corr5(), "explication": "ex_r5", "facile": "fa_r5"})
Q[5].update({"texte_dit": "la question six: فالصيف، الهوا فquarante degrés Celsius. نفس le rail، ولكن delta t prime صغر شوية. التلميذ عاود الحساب بtrois cent quarante، وقال le rail قصر. critiquer.".replace("فquarante", "à quarante").replace("بtrois", "avec trois"),
             "reponse": phrase(att6(A)), "clavier": CL6,
             "aides": [aide("Le rail a-t-il pu changer de longueur ? Qu'est-ce qui change dans l'air quand il fait chaud ?",
                            "واش le rail يقدر يتبدل؟ وشنو اللي كيتبدل فالهوا ملي كيسخن؟"),
                       aide(f"Dans l'air chaud le son va plus vite ; la valeur {A['va']} m/s vaut vers 20 °C seulement.",
                            "فالهوا السخون، le son كيمشي بالزربة. trois cent quarante mètres par seconde، valable vers vingt degrés Celsius.")],
             "correction": corr6(A), "explication": "ex_r6", "facile": "fa_r6"})

# ---------- explication animée (milieux.html) ----------
M1 = ("فla simulation، نفس la frappe، فنفس اللحظة، dans les quatre pistes، sur un kilomètre. "
      f"شوف: le son فl'acier وصل اللول، après {dire(SIM_TACIER, 1)} seconde. "
      f"فالهوا، وصل اللخر، après {dire(SIM_TAIR20, 1)} seconde. "
      "نفس la distance d، إذن t égale d sur v: اللي عندو v كبيرة كيوصل قبل. "
      f"فالتمرين، v acier égale {dire(A['vs'])} mètres par seconde، و v air égale {dire(A['va'])} mètres par seconde. "
      "إذن le son ديال le rail كيوصل اللول.").replace("و v air", "et v air")
M2 = ("كل piste عندها نفس la distance d. فكل milieu، t égale d sur v. "
      "إذن t acier égale d sur v acier، وt air égale d sur v air. "
      "شوف: l'acier كيوصل، ومن بعد الهوا. delta t هو الفرق بين les deux arrivées: delta t égale t air moins t acier. "
      "إذن delta t égale d sur v air، moins d sur v acier. ونخرجو d: delta t égale d fois، un sur v air، moins un sur v acier.")
M3 = (f"فla simulation، d égale un kilomètre. l'acier وصل après {dire(SIM_TACIER, 1)} seconde، والهوا après {dire(SIM_TAIR20, 1)} seconde. "
      f"delta t égale environ {dire(SIM_TAIR20 - SIM_TACIER, 1)} seconde. "
      "فالتمرين، كنعرفو delta t، وباغيين d. من la relation: d égale delta t sur، un sur v air moins un sur v acier. "
      f"d égale {dire(A['dt'])} sur، un sur {dire(A['va'])} moins un sur {dire(A['vs'])}. d égale {dire(round(A['d']), 0)} mètres.")
M4 = (f"فla simulation، sur un kilomètre d'acier، t égale mille sur cinq mille، égale {dire(SIM_TACIER, 1)} seconde. "
      f"فالتمرين، t acier égale {dire(round(A['d']), 0)} sur {dire(A['vs'])}، égale {dire(A['ts'])} seconde. "
      "le son ديال الهوا كيوصل من بعد ب delta t. "
      f"إذن t air égale t acier plus delta t، égale {dire(A['ts'])} plus {dire(A['dt'])}، égale {dire(A['ta'])} secondes. "
      f"ونتأكدو: d sur v air، {dire(round(A['d']), 0)} sur {dire(A['va'])}، égale {dire(A['ta'])}.")
M5 = ("شوف la piste اللي لتحت: نفس الهوا، ولكن la frappe قوية بزاف. "
      "شوف: le son ديال la frappe القوية كيوصل فنفس الوقت ديال la frappe الضعيفة. "
      "la célérité كتبدل مع le milieu، ماشي مع l'amplitude ديال la perturbation. "
      "إذن t acier وt air ما كيتبدلوش، وdelta t كتبقى هي هي.")
M6 = ("دابا نسخنو الهوا: la température égale quarante degrés Celsius. "
      f"شوف: le son فالهوا كيوصل قبل، après {dire(SIM_TAIR40, 1)} seconde، et non pas {dire(SIM_TAIR20, 1)}. "
      f"فالهوا السخون، v air supérieure à {dire(A['va'])} mètres par seconde. إذن t air كيصغر، وdelta t كيصغر. "
      f"ولكن le rail ما تبدلش. {dire(A['va'])} mètres par seconde، valable vers vingt degrés Celsius. "
      f"التلميذ خدم avec {dire(A['va'])}، إذن الغلط ماشي فd، الغلط فv air.")

EXPL = [
  diapo_sim("ex_r1", "Question 1 : qui arrive le premier ?", "Même distance : t = d/v ; le milieu le plus rapide arrive le premier.",
            SIM, "La même frappe dans l'acier, l'eau et l'air", M1,
            [("même d : t = d/v", "إذن t égale d sur v"), ("v_acier > v_air : le rail d'abord", "إذن le son ديال le rail كيوصل اللول")],
            [dict(mot="فla simulation، نفس la frappe", commande="play_until", parametres={"moment": "depart"}),
             dict(mot="شوف: le son فl'acier", commande="play_until", parametres={"moment": "acier_arrive"}),
             dict(mot="شوف: le son فl'acier", repere="acier"),
             dict(mot="فالهوا، وصل اللخر", commande="play_until", parametres={"moment": "air_arrive"}),
             dict(mot="فالهوا، وصل اللخر", repere="air"),
             dict(mot="إذن t égale d sur v", cible="centre:0"),
             dict(mot="إذن le son ديال le rail كيوصل اللول", cible="centre:1")]),
  diapo_sim("ex_r2", "Question 2 : la relation de Δt", "Δt = t_air − t_acier = d·(1/v_air − 1/v_acier).",
            SIM, "Deux arrivées, une même distance", M2,
            [("t_acier = d/v_acier ; t_air = d/v_air", "إذن t acier égale d sur v acier"),
             ("Δt = t_air − t_acier", "delta t égale t air moins t acier"),
             ("Δt = d·(1/v_air − 1/v_acier)", "ونخرجو d: delta t égale d fois")],
            [dict(mot="إذن t acier égale d sur v acier", cible="centre:0"),
             dict(mot="شوف: l'acier كيوصل", commande="play_until", parametres={"moment": "acier_arrive"}),
             dict(mot="ومن بعد الهوا", commande="play_until", parametres={"moment": "air_arrive"}),
             dict(mot="delta t égale t air moins t acier", cible="centre:1"),
             dict(mot="ونخرجو d: delta t égale d fois", cible="centre:2")]),
  diapo_sim("ex_r3", "Question 3 : de Δt à la distance", "d = Δt/(1/v_air − 1/v_acier) : on divise par la parenthèse entière.",
            SIM, "Sur 1 km : 0,20 s dans l'acier, 2,9 s dans l'air", M3,
            [("d = Δt/(1/v_air − 1/v_acier)", "d égale delta t sur، un sur v air"),
             (f"d = {fr(A['dt'])}/(1/{A['va']} − 1/{A['vs']}) = {fr(A['d'], 0)} m", f"d égale {dire(round(A['d']), 0)} mètres")],
            [dict(mot="فla simulation، d égale un kilomètre", commande="play_until", parametres={"moment": "air_arrive"}),
             dict(mot="l'acier وصل", repere="acier"),
             dict(mot="والهوا après", repere="air"),
             dict(mot="d égale delta t sur، un sur v air", cible="centre:0"),
             dict(mot=f"d égale {dire(round(A['d']), 0)} mètres", cible="centre:1")]),
  diapo_sim("ex_r4", "Question 4 : les deux dates d'arrivée", "t_acier = d/v_acier ; t_air = t_acier + Δt.",
            SIM, "Le son arrive au bout de l'acier", M4,
            [(f"t_acier = {fr(A['d'], 0)}/{A['vs']} = {fr(A['ts'])} s", f"égale {dire(A['ts'])} seconde"),
             (f"t_air = {fr(A['ts'])} + {fr(A['dt'])} = {fr(A['ta'])} s", "إذن t air égale t acier plus delta t")],
            [dict(mot="sur un kilomètre d'acier", commande="play_until", parametres={"moment": "acier_arrive"}),
             dict(mot="sur un kilomètre d'acier", repere="acier"),
             dict(mot=f"égale {dire(A['ts'])} seconde", cible="centre:0"),
             dict(mot="إذن t air égale t acier plus delta t", cible="centre:1")]),
  diapo_sim("ex_r5", "Question 5 : frapper plus fort", "La célérité dépend du milieu, pas de l'amplitude.",
            SIM, "Air frappé fort, air frappé doucement : même arrivée", M5,
            [("v dépend du milieu, pas de l'amplitude", "la célérité كتبدل مع le milieu"), ("Δt inchangée", "وdelta t كتبقى هي هي")],
            [dict(mot="شوف la piste اللي لتحت", repere="air_fort"),
             dict(mot="شوف: le son ديال la frappe القوية", commande="play_until", parametres={"moment": "air_arrive"}),
             dict(mot="كيوصل فنفس الوقت", repere="meme_v"),
             dict(mot="la célérité كتبدل مع le milieu", cible="centre:0"),
             dict(mot="وdelta t كتبقى هي هي", cible="centre:1")]),
  diapo_sim("ex_r6", "Question 6 : l'air chaud", "Dans l'air chaud, le son va plus vite : t_air et Δt diminuent, d ne change pas.",
            SIM, "L'air à 40 °C : le son arrive plus tôt", M6,
            [("air chaud : v_air ↑, t_air ↓, Δt ↓", "إذن t air كيصغر"), ("d inchangée : l'erreur est sur v_air", "الغلط فv air")],
            [dict(mot="دابا نسخنو الهوا", repere="temperature"),
             dict(mot="la température égale quarante degrés Celsius", commande="set_parameters", parametres={"temperature_c": 40}),
             dict(mot="شوف: le son فالهوا كيوصل قبل", commande="play_until", parametres={"moment": "air_arrive"}),
             dict(mot="شوف: le son فالهوا كيوصل قبل", repere="air"),
             dict(mot="إذن t air كيصغر", cible="centre:0"),
             dict(mot="الغلط فv air", cible="centre:1")]),
]

# ---------- version facile ----------
FAC = [
  qcm_facile("fa_r1", "Plus facile : le premier son", "سؤال ساهل: شكون كيوصل اللول؟",
             "Les deux sons parcourent la même distance d. Lequel arrive le premier ?",
             [f"Celui de l'air ({A['va']} m/s)", f"Celui du rail d'acier ({A['vs']} m/s)", "Les deux en même temps"], 1, {
               "1": {"juste": rep("برافو! نفس la distance، وt égale d sur v: v acier كبيرة، إذن كيوصل اللول.",
                                  "Juste : même d, et t = d/v est plus petit dans l'acier.")},
               "0": {"1": rep("ما تقلقش. t égale d sur v: شكون عندو v كبيرة؟ عاود اختار.",
                              "t = d/v : qui a la plus grande célérité ? Réessaie."),
                     "2": rep("la réponse est le rail. v acier كبيرة بزاف، إذن t acier صغير.",
                              "Réponse : le son du rail, car v_acier > v_air.")},
               "2": {"1": rep("قريب! ولكن la célérité ماشي هي هي dans les deux milieux. عاود اختار.",
                              "Les deux milieux n'ont pas la même célérité. Réessaie."),
                     "2": rep("la réponse est le rail. la célérité كتبدل مع le milieu، وفl'acier كبيرة.",
                              "Réponse : le son du rail arrive le premier.")}},
             "Les deux sons parcourent la même distance d. Lequel arrive le premier ?"),
  assoc_facile("fa_r2", "Plus facile : les durées", "سؤال ساهل: ربط كل durée مع la relation ديالها.",
               "Relie chaque durée à son expression.", "Relie chaque durée à son expression.",
               [("1", "t_acier"), ("2", "t_air"), ("3", "Δt")],
               [("a", "d/v_acier"), ("b", "d/v_air"), ("c", "t_air − t_acier")],
               {"1": "a", "2": "b", "3": "c"},
               {"1-a": (True, "Oui : dans l'acier, t = d/v_acier.", "صحيح: فl'acier، t égale d sur v acier."),
                "1-b": (False, "d/v_air est la durée dans l'air, pas dans l'acier.", "d sur v air هي la durée فالهوا، ماشي فl'acier."),
                "1-c": (False, "t_air − t_acier est l'écart entre les arrivées, pas la durée dans l'acier.", "t air moins t acier هو الفرق، ماشي la durée فl'acier."),
                "2-a": (False, "d/v_acier est la durée dans l'acier.", "d sur v acier هي la durée فl'acier."),
                "2-b": (True, "Oui : dans l'air, t = d/v_air.", "صحيح: فالهوا، t égale d sur v air."),
                "2-c": (False, "C'est Δt, l'écart, pas la durée dans l'air.", "هادا delta t، الفرق، ماشي la durée فالهوا."),
                "3-a": (False, "Δt n'est pas une durée de parcours, c'est un écart.", "delta t ماشي durée ديال الطريق، هو الفرق."),
                "3-b": (False, "Δt est la différence des deux durées.", "delta t هو الفرق بين les deux durées."),
                "3-c": (True, "Oui : le son de l'air arrive en dernier : Δt = t_air − t_acier.", "صحيح: الهوا كيوصل اللخر، إذن delta t égale t air moins t acier.")},
               ("Couples : (1 ; a) (2 ; b) (3 ; c).", "t acier égale d sur v acier، t air égale d sur v air، وdelta t égale t air moins t acier.")),
  qcm_facile("fa_r3", "Plus facile : isoler d", "سؤال ساهل: خرج d من la relation.",
             "Δt = d·(1/v_air − 1/v_acier). On en déduit…",
             ["d = Δt·(1/v_air − 1/v_acier)", "d = Δt/(1/v_air − 1/v_acier)", "d = Δt·v_air"], 1, {
               "1": {"juste": rep(f"برافو! كنقسمو delta t على la parenthèse كاملة. هنا d égale {dire(round(A['d']), 0)} mètres.",
                                  f"Juste : d = Δt/(1/v_air − 1/v_acier) = {fr(A['d'], 0)} m.")},
               "0": {"1": rep("ما تقلقش. d مضروبة فla parenthèse: باش نخرجوها، كنقسمو. عاود اختار.",
                              "d est multipliée par la parenthèse : il faut diviser. Réessaie."),
                     "2": rep("la réponse est d égale delta t sur la parenthèse. كنقسمو، ماشي كنضربو.",
                              "Réponse : d = Δt/(1/v_air − 1/v_acier).")},
               "2": {"1": rep("قريب! ولكن نسيتي le son ديال l'acier. delta t فيه le milieu acier et le milieu air. عاود اختار.",
                              "Tu as oublié le son de l'acier. Réessaie."),
                     "2": rep("la réponse est d égale delta t sur، un sur v air moins un sur v acier.",
                              "Réponse : d = Δt/(1/v_air − 1/v_acier).")}},
             "Delta t égale d fois, un sur v air, moins un sur v acier. On en déduit ?"),
  vf_facile("fa_r4", "Plus facile : les dates d'arrivée", "سؤال ساهل: قول واش كل جملة صحيحة ولا غالطة.",
            f"d = {fr(A['d'], 0)} m, Δt = {fr(A['dt'])} s.", [
              (f"t_acier = {fr(A['d'], 0)}/{A['vs']} = {fr(A['ts'])} s.", True, "t_acier = d/v_acier."),
              ("t_air = t_acier − Δt.", False, "Le son de l'air arrive APRÈS : t_air = t_acier + Δt."),
              (f"t_air = d/v_air = {fr(A['ta'])} s.", True, f"{fr(A['d'], 0)}/{A['va']} = {fr(A['ta'])} s, le même résultat que t_acier + Δt.")]),
  qcm_facile("fa_r5", "Plus facile : frapper plus fort", "سؤال ساهل: واش delta t كتبدل؟",
             "On frappe le rail beaucoup plus fort. La durée Δt…",
             ["augmente", "diminue", "ne change pas"], 2, {
               "2": {"juste": rep("برافو! la célérité كتبدل مع le milieu، ماشي مع l'amplitude. إذن delta t هي هي.",
                                  "Juste : v dépend du milieu, pas de l'amplitude.")},
               "0": {"1": rep("ما تقلقش. واش la frappe القوية كتبدل le milieu؟ عاود اختار.",
                              "Frapper fort change-t-il le milieu ? Réessaie."),
                     "2": rep("la réponse est ne change pas. la célérité ما كتبدلش مع l'amplitude.",
                              "Réponse : Δt ne change pas.")},
               "1": {"1": rep("قريب! ولكن le son ما كيمشيش بالزربة ملي كنضربو بزاف. عاود اختار.",
                              "Le son ne va pas plus vite quand on frappe fort. Réessaie."),
                     "2": rep("la réponse est ne change pas: v acier وv air هوما هوما.",
                              "Réponse : Δt ne change pas, v_acier et v_air restent les mêmes.")}},
             "On frappe le rail beaucoup plus fort. La durée delta t ?"),
  vf_facile("fa_r6", "Plus facile : la température", "سؤال ساهل: قول واش كل جملة صحيحة ولا غالطة.",
            "Un jour chaud, avec le même rail.", [
              ("Dans l'air plus chaud, le son va plus vite.", True, "La célérité du son dans l'air augmente avec la température."),
              ("Si Δt diminue un jour chaud, c'est que le rail est plus court.", False, "Le rail ne change pas : c'est v_air qui a augmenté."),
              (f"{A['va']} m/s est la célérité du son dans l'air vers 20 °C.", True, "Ce n'est pas une valeur valable à toute température.")]),
]

SQ = questions(B)
for q, (rp, cl, co) in zip(SQ, [(phrase(ATT1), CL1, corr1(B)), (phrase(ATT2), CL2, corr2()), (valeur("d", B["d"], "m", att3(B)), CL3, corr3(B)),
                                 (valeur("t_air", B["ta"], "s", att4(B)), CL4, corr4(B)), (phrase(ATT5), CL5, corr5()), (phrase(att6(B)), CL6, corr6(B))]):
    q.update({"reponse": rp, "clavier": cl, "correction": co})

EX = {
  "id": "phys_ex_ch1_rail_7", "type": "exercice", "version": 1, "status": "published",
  "matiere": "physique", "chapitre": "ondes_mecaniques", "cours": "phys_ch1_waves_exemple",
  "titre": "Deux sons, un seul coup de marteau", "niveau": "difficile", "duree_min": 30,
  "origine": "Exercice original écrit pour Moalim (ni sujet du national, ni copie d'un livre ou d'une série).",
  "competences": ["Exploiter t = d/v dans deux milieux", "Établir Δt = d·(1/v_air − 1/v_acier) et en tirer d",
                  "Justifier que la célérité dépend du milieu (et de la température de l'air), pas de l'amplitude"],
  "enonce": {
    "intro": intro(A),
    "intro_dit": ("دابا نقراو l'énoncé. واحد العامل كيضرب بالمطرقة le rail d'acier فالطرف A، فt égale zéro. "
                  "فالطرف الآخر B، la distance d ما معروفاش. فB، كاين un capteur فوق le rail، et un microphone فالهوا. "
                  "le son كيوصل ل B deux fois، une fois من le rail، et une fois من الهوا. "
                  f"الوقت بين les deux arrivées، delta t égale {dire(A['dt'])} secondes. "
                  f"v acier égale {dire(A['vs'])} mètres par seconde، et v air égale {dire(A['va'])} mètres par seconde.").replace("ل B deux fois", "ل B، deux fois"),
    "figures": figures(A), "donnees": donnees_txt(A), "questions": Q},
  "explication": {"activities": [{"id": "explication", "title": "Explication animée", "slides": EXPL}]},
  "facile": {"activities": [{"id": "facile", "title": "Plus facile, pour s'entraîner", "slides": FAC}]},
  "similaire": {"id": "phys_ex_ch1_rail_7_b", "titre": "Même exercice, autres données",
    "enonce": {"intro": intro(B),
               "intro_dit": ("نفس التمرين، بقيم أخرى. le rail أطول، والوقت بين les deux arrivées، "
                             f"delta t égale {dire(B['dt'])} secondes."),
               "figures": figures(B), "donnees": donnees_txt(B), "questions": SQ}},
}

_NB = set("deux trois quatre cinq six sept huit neuf dix onze douze treize quatorze quinze seize vingt trente quarante cinquante soixante cent cents mille zéro quatre-vingts".split())
_AR = re.compile(r"[؀-ۿ]")


def controle_voix(o, k=""):
    pb = []
    if isinstance(o, dict):
        for kk, vv in o.items():
            pb += controle_voix(vv, kk)
    elif isinstance(o, list):
        for vv in o:
            pb += controle_voix(vv, k)
    elif isinstance(o, str) and k in {"mixed", "dit", "parole", "intro_dit", "texte_dit", "enonce_dit", "mot"}:
        if re.search(r"\d", o):
            pb.append(("chiffre", o[:60]))
        mots = o.split()
        for a, b in zip(mots, mots[1:]):
            if _AR.search(a) and not re.search(r"[،,.;!?؟]$", a) and b.strip("،,.:;!?؟").split("-")[0] in _NB:
                pb.append(("darija+nombre", a + " " + b))
    return pb


_pb = controle_voix(EX)
assert not _pb, _pb
ecrire(EX)
