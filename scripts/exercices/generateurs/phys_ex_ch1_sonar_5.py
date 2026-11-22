# Exercice de physique (ch. 1, ondes mécaniques progressives), niveau MOYEN : le sonar d'un bateau de pêche.
# Sources comparées (skill exercices § 2) :
# - exploration ondes_mecaniques_periodiques.json (partie ch1 : cas_types oscillogramme / sensibilité, pieges
#   « T = 4 (des divisions) sans multiplier par la sensibilité », « confond ms et µs », erreurs_examen) ;
# - experience_profs.json « ondes_mecaniques » : cas type « echo » (d = v·t/2, dessiner l'aller et le retour),
#   pièges « écho : prendre d au lieu de 2d », « double le temps de l'écho », « compter les carreaux au lieu des
#   divisions », « ms → s avant le calcul » ; insistance « le son a besoin d'un milieu matériel » ;
# - nationaux comparés : 2020 R ex. 2 (échographie du fœtus : deux échos, d₁ = v·t₁/2 puis épaisseur
#   d₂ = v(t₂ − t₁)/2, v = 1540 m/s), 2018 N ex. 2 (ultrasons dans le pétrole, oscillogramme 2 ms/div),
#   2022 N ex. 2 (oscillogramme 0,5 ms/div, v = L/Δt), 2024 R ex. 2 (deux micros). Le nôtre : un sonar de bateau
#   dans l'eau de mer (v = 1500 m/s), lecture en divisions à 10 ms/div, « montrer que d = v·τ/2 », puis un second
#   oscillogramme à deux échos où il faut RECONNAÎTRE l'écho du banc (le plus proche) et calculer sa distance
#   directe (pas d'épaisseur par différence comme en 2020 R) : autre situation, autres données, autre chaîne ;
# - séries en ligne (talamidi « ondes mécaniques progressives » séries 1 et 5, moutamadris « 2bac international »,
#   série Jenkal (scribd), dreamjob « exercices corrigés ») : repérées par recherche, mais la lecture a été bloquée
#   par le réseau de la session (talamidi.com, moutamadris.ma, dreamjob.ma non résolus) ; d'après les extraits,
#   le sonar / l'écho est un classique des devoirs. Rien n'a été recopié.
# Simulation : ondes-tableau/sonar.html (eau de mer V = 1500 m/s, d de 10 à 75 m par pas de 7,5 m ; d = 60 m donne
# τ = 80 ms, d = 30 m donne τ = 40 ms : les données de l'exercice sont prises sur ces valeurs).
import sys, os, re, importlib.util
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _outils import *

_TP = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "backend", "kaggle_tts", "texte_parle.py")
_sp = importlib.util.spec_from_file_location("tp", _TP); tp = importlib.util.module_from_spec(_sp); _sp.loader.exec_module(tp)


def dire(x, dec=3):
    """Le nombre en lettres françaises, à partir de son écriture fr() (calculé, jamais tapé à la main)."""
    s = fr(x, dec)
    m = re.match(r"(\d+),(\d+)$", s)
    return tp._decimal_fr(m) if m else tp.nombre_fr(int(s))


SIM = "/media/simulations/physics/ondes-tableau/sonar.html"


# ---------- données (calculées) ----------
def donnees(N_khz, sh_ms, n1, n2, v=1500):
    tau1 = n1 * sh_ms            # ms
    tau2 = n2 * sh_ms
    d1 = v * tau1 / 1000 / 2
    d2 = v * tau2 / 1000 / 2
    return dict(N=N_khz, sh=sh_ms, n1=n1, n2=n2, v=v, tau1=tau1, tau2=tau2, d1=d1, d2=d2)


A = donnees(50, 10, 8, 4)        # exercice : τ = 80 ms → 60 m ; banc τ' = 40 ms → 30 m
B = donnees(40, 20, 4.5, 1.5)    # semblable : τ = 90 ms → 67,5 m ; banc τ' = 30 ms → 22,5 m
assert abs(A["d1"] - 60) < 1e-9 and abs(A["d2"] - 30) < 1e-9


def salve(x0, amp, base, larg=0.7, n=40):
    """Même salve amortie que le graphe de sonar.html (exp(−3u)·sin(22u))."""
    return [[round(x0 + larg * i / n, 3), round(base + amp * math.exp(-3 * i / n) * math.sin(22 * i / n), 3)] for i in range(n + 1)]


def oscillogramme(titre, sh, echos, legende):
    """Écran d'oscilloscope 10 × 6 divisions ; émission à la division 1 ; echos = [(division, amplitude, texte)]."""
    base = 3.0
    el = []
    for i in range(11):
        el.append({"f": "ligne", "pts": [[i, 0], [i, 6]], "couleur": "faible", "trait": "pointille"})
    for j in range(7):
        el.append({"f": "ligne", "pts": [[0, j], [10, j]], "couleur": "faible", "trait": "pointille"})
    # trace : ligne de base, salve émise, échos
    pts = [[0, base], [1, base]] + salve(1, 2.2, base)
    for (x, a, _) in echos:
        pts += [[x, base]] + salve(x, a, base)
    pts.append([10, base])
    el.append({"f": "ligne", "pts": pts, "couleur": "jaune", "epais": True})
    el.append({"f": "texte", "at": [1.4, 5.6], "t": "émission", "couleur": "jaune", "taille": "petit"})
    for (x, a, t) in echos:
        el.append({"f": "texte", "at": [x + 0.35, base + a + 0.6], "t": t, "couleur": "vert", "taille": "petit"})
    el.append({"f": "texte", "at": [7.6, 0.45], "t": f"{fr(sh)} ms/div", "couleur": "cyan", "taille": "petit"})
    return {"type": "schema", "titre": titre, "cadre": {"l": 10, "h": 6}, "legende": legende, "elements": el}


def figures(D):
    return [
        oscillogramme("Document 1 : au-dessus du fond", D["sh"], [(1 + D["n1"], 0.9, "écho")],
                      "Une division horizontale = " + fr(D["sh"]) + " ms. Le signal émis part à la première division."),
        oscillogramme("Document 2 : au-dessus d'un banc de poissons", D["sh"],
                      [(1 + D["n2"], 1.1, "écho 1"), (1 + D["n1"], 0.6, "écho 2")],
                      "Deux échos reviennent au sonar."),
    ]


def intro(D):
    return ("Un bateau de pêche est équipé d'un sonar : sous la coque, un émetteur-récepteur envoie verticalement vers le bas, "
            f"à la date t = 0, une salve d'ultrasons de fréquence N = {fr(D['N'])} kHz. L'onde se réfléchit sur le premier obstacle "
            "qu'elle rencontre (le fond, ou un banc de poissons) et revient vers le sonar, qui reçoit l'écho. "
            "Un oscilloscope affiche le signal émis et le signal reçu. Le document 1 est obtenu au-dessus d'un fond plat ; "
            "le document 2 plus loin, au-dessus d'un banc de poissons.")


def donnees_txt(D):
    return [f"Célérité des ultrasons dans l'eau de mer : v = {D['v']} m/s",
            f"Sensibilité horizontale de l'oscilloscope : {fr(D['sh'])} ms/div",
            "Domaine des sons audibles : de 20 Hz à 20 kHz"]


# ---------- réponses (écrites à partir des calculs) ----------
def att2(D):
    return f"τ = {fr(D['n1'])} div × {fr(D['sh'])} ms/div = {fr(D['tau1'])} ms"


def att4(D):
    return f"τ = {fr(D['tau1'])} ms = {fr(D['tau1'] / 1000, 3)} s ; d = v·τ/2 = {D['v']} × {fr(D['tau1'] / 1000, 3)}/2 = {fr(D['d1'])} m"


def att5(D):
    return (f"le banc est plus proche que le fond : son écho est le premier ; τ' = {fr(D['n2'])} × {fr(D['sh'])} = {fr(D['tau2'])} ms "
            f"= {fr(D['tau2'] / 1000, 3)} s ; d' = v·τ'/2 = {D['v']} × {fr(D['tau2'] / 1000, 3)}/2 = {fr(D['d2'])} m")


ATT1 = ("N = {N} kHz > 20 kHz : ce sont des ultrasons, l'oreille humaine ne les entend pas. Ce sont des ondes mécaniques : "
        "elles ont besoin d'un milieu matériel, elles ne se propagent pas dans le vide.")
ATT3 = ("Pendant τ, l'onde descend jusqu'au fond (distance d) puis remonte (distance d) : elle parcourt 2d. "
        "Donc v = 2d/τ, soit 2d = v·τ et d = v·τ/2.")


def corr1(D):
    return correction([
        (f"1 : N = {fr(D['N'])} kHz > 20 kHz", f"N égale {dire(D['N'])} kilohertz"),
        ("ce sont des ultrasons : l'oreille ne les entend pas", "هادو des ultrasons"),
        ("onde mécanique : il faut un milieu matériel, pas de propagation dans le vide", "خاصهم un milieu matériel")],
        f"la question un. N égale {dire(D['N'])} kilohertz، supérieure à vingt kilohertz. إذن هادو des ultrasons، الودن ما كتسمعهمش. "
        "وles ultrasons هوما des ondes mécaniques: خاصهم un milieu matériel، إذن ما كيمشيوش فle vide.")


def corr2(D):
    return correction([
        (f"2 : de l'émission à l'écho : {fr(D['n1'])} divisions", f"le nombre de divisions égale {dire(D['n1'])}"),
        (f"τ = {fr(D['n1'])} × {fr(D['sh'])} ms", f"tau égale {dire(D['n1'])} fois {dire(D['sh'])} millisecondes"),
        (f"τ = {fr(D['tau1'])} ms", f"donc tau égale {dire(D['tau1'])} millisecondes")],
        f"la question deux. بين البداية ديال l'émission والبداية ديال l'écho، le nombre de divisions égale {dire(D['n1'])}. "
        f"une division égale {dire(D['sh'])} millisecondes. tau égale {dire(D['n1'])} fois {dire(D['sh'])} millisecondes، "
        f"donc tau égale {dire(D['tau1'])} millisecondes.")


def corr3():
    return correction([
        ("3 : pendant τ, l'onde fait l'aller et le retour : elle parcourt 2d", "قطعات la distance deux d"),
        ("v = 2d/τ, donc 2d = v·τ", "deux d égale v fois tau"),
        ("d = v·τ/2", "d égale v fois tau sur deux")],
        "la question trois. فla durée tau، l'onde كتهبط للأرض وكترجع: قطعات la distance deux d. "
        "إذن v égale deux d sur tau، donc deux d égale v fois tau. ونقسمو par deux: d égale v fois tau sur deux.")


def corr4(D):
    t = D["tau1"] / 1000
    return correction([
        (f"4 : τ = {fr(D['tau1'])} ms = {fr(t, 3)} s", f"tau égale {dire(t)} seconde"),
        (f"d = v·τ/2 = {D['v']} × {fr(t, 3)}/2", "d égale v fois tau sur deux"),
        (f"d = {fr(D['d1'])} m", f"d égale {dire(D['d1'])} mètres")],
        f"la question quatre. أولا نحولو la durée: {dire(D['tau1'])} millisecondes، donc tau égale {dire(t)} seconde. "
        f"d égale v fois tau sur deux، égale {dire(D['v'])} fois {dire(t)}، sur deux. d égale {dire(D['d1'])} mètres.")


def corr5(D):
    t = D["tau2"] / 1000
    return correction([
        ("5 : le banc est plus proche que le fond : son écho arrive le premier", "l'écho ديال le banc كيوصل اللول"),
        (f"τ' = {fr(D['n2'])} × {fr(D['sh'])} ms = {fr(D['tau2'])} ms = {fr(t, 3)} s", f"tau prime égale {dire(D['tau2'])} millisecondes"),
        (f"d' = v·τ'/2 = {D['v']} × {fr(t, 3)}/2", "d prime égale v fois tau prime sur deux"),
        (f"d' = {fr(D['d2'])} m", f"d prime égale {dire(D['d2'])} mètres")],
        f"la question cinq. le banc قريب من le bateau كثر من الأرض، إذن l'écho ديال le banc كيوصل اللول. "
        f"le nombre de divisions égale {dire(D['n2'])}، إذن tau prime égale {dire(D['tau2'])} millisecondes، soit {dire(t)} seconde. "
        f"d prime égale v fois tau prime sur deux، égale {dire(D['v'])} fois {dire(t)}، sur deux. d prime égale {dire(D['d2'])} mètres.")


CL1 = {"aides": ["N", "kHz", "20 kHz", "milieu matériel", "onde mécanique"], "pieges": ["onde électromagnétique", "20 Hz"]}
CL2 = {"aides": ["τ = n × S_h", "div", "ms/div", "ms"], "pieges": ["τ = n/S_h", "s"]}
CL3 = {"aides": ["2d", "v = distance/τ", "aller", "retour"], "pieges": ["d = v·τ", "v = d/τ"]}
CL4 = {"aides": ["d = v·τ/2", "1 ms = 10⁻³ s", "A.N. :", "m"], "pieges": ["d = v·τ", "τ = 80 s"]}
CL5 = {"aides": ["d' = v·τ'/2", "τ'", "ms/div", "A.N. :", "m"], "pieges": ["d' = v·τ'", "écho 2"]}

Q = [
  {"id": "1", "texte": "Les ondes émises par le sonar sont-elles audibles par l'oreille humaine ? Peuvent-elles se propager dans le vide ? Justifier.",
   "texte_dit": "la question un: واش هاد les ondes اللي كيصيفط le sonar كنسمعوهم؟ وواش يقدرو يمشيو فle vide؟ justifier.",
   "reponse": phrase(ATT1.format(N=fr(A["N"]))), "clavier": CL1,
   "aides": [aide("Compare la fréquence N du sonar au domaine des sons audibles (de 20 Hz à 20 kHz).",
                  "قارن la fréquence ديال le sonar مع le domaine audible، de vingt hertz à vingt kilohertz."),
             aide("Une onde ultrasonore est une onde mécanique : de quoi a-t-elle besoin pour se propager ?",
                  "les ultrasons هوما des ondes mécaniques. شنو خاصهم باش يمشيو؟")],
   "correction": corr1(A), "explication": "ex_s1", "facile": "fa_s1"},
  {"id": "2", "texte": "Lire sur le document 1 la durée τ qui sépare l'émission de la réception de l'écho.",
   "texte_dit": "la question deux: قرا على le document un la durée tau، بين l'émission ووصول l'écho.",
   "reponse": valeur("τ", A["tau1"], "ms", att2(A)), "clavier": CL2,
   "aides": [aide("Compte les divisions entre le début de la salve émise et le début de l'écho (début avec début).",
                  "حسب les divisions بين البداية ديال l'émission والبداية ديال l'écho. البداية مع البداية."),
             aide(f"Chaque division vaut la sensibilité horizontale : τ = nombre de divisions × {fr(A['sh'])} ms/div.",
                  f"une division égale {dire(A['sh'])} millisecondes. إذن tau égale le nombre de divisions fois {dire(A['sh'])} millisecondes.")],
   "correction": corr2(A), "explication": "ex_s2", "facile": "fa_s2"},
  {"id": "3", "texte": "Montrer que la profondeur d du fond s'exprime par d = v·τ/2.",
   "texte_dit": "la question trois: بين بلي la profondeur d كتكتب d égale v fois tau sur deux.",
   "reponse": phrase(ATT3), "clavier": CL3,
   "aides": [aide("Pendant τ, l'onde descend jusqu'au fond puis remonte jusqu'au sonar : quelle distance parcourt-elle en tout ?",
                  "فla durée tau، l'onde كتهبط حتى للأرض، ومن بعد كترجع ل le sonar. شحال قطعات ديال la distance كاملة؟"),
             aide("Écris v = distance parcourue / τ avec cette distance, puis isole d.",
                  "كتب v égale la distance sur tau، بهاد la distance، ومن بعد خرج d.")],
   "correction": corr3(), "explication": "ex_s3", "facile": "fa_s3"},
  {"id": "4", "texte": "Calculer la profondeur d du fond.",
   "texte_dit": "la question quatre: حسب la profondeur d.",
   "reponse": valeur("d", A["d1"], "m", att4(A)), "clavier": CL4,
   "aides": [aide("Convertis d'abord τ en secondes : 1 ms = 10⁻³ s.",
                  "أولا حول tau للseconde: une milliseconde égale dix puissance moins trois seconde."),
             aide(f"Applique d = v·τ/2 avec v = {A['v']} m/s.",
                  f"عوض فd égale v fois tau sur deux، مع v égale {dire(A['v'])} mètres par seconde.")],
   "correction": corr4(A), "explication": "ex_s4", "facile": "fa_s4"},
  {"id": "5", "texte": "Au-dessus du banc de poissons, l'écran affiche le document 2 : deux échos. Justifier lequel des deux échos provient du banc, puis déterminer la distance d' entre le sonar et le banc.",
   "texte_dit": "la question cinq: فوق le banc ديال الحوت، l'écran كيبين le document deux، avec deux échos. justifier شكون فيهم جا من le banc، ومن بعد déterminer la distance d prime بين le sonar وle banc.",
   "reponse": valeur("d'", A["d2"], "m", att5(A)), "clavier": CL5,
   "aides": [aide("Le banc est entre le bateau et le fond : son écho revient-il avant ou après celui du fond ?",
                  "le banc كاين بين le bateau والأرض. l'écho ديالو، واش كيرجع قبل ولا من بعد l'écho ديال الأرض؟"),
             aide(f"Lis τ' pour cet écho (divisions × {fr(A['sh'])} ms/div), convertis-le en s, puis d' = v·τ'/2.",
                  "قرا tau prime ديال هاد l'écho، حولو للseconde، ومن بعد d prime égale v fois tau prime sur deux.")],
   "correction": corr5(A), "explication": "ex_s5", "facile": "fa_s5"},
]

# ---------- explication animée (sonar.html : V = 1500 m/s ; d = 60 m → τ = 80 ms ; d = 30 m → τ = 40 ms) ----------
M1 = ("شوف le bateau. تحت la coque كاين le sonar. le sonar كيصيفط واحد la salve ديال les ultrasons لتحت، فالما. "
      "la fréquence ديال les ultrasons supérieure à vingt kilohertz، إذن الودن ما كتسمعهمش. "
      "شوف la salve كتمشي فالما حتى للأرض ديال البحر. l'onde mécanique كتحتاج un milieu matériel: هنا le milieu هو الما. "
      "فle vide، ما كاين حتى شي حاجة تتحرك، إذن l'onde ما كتمشيش. "
      f"فالتمرين، N égale {dire(A['N'])} kilohertz، supérieure à vingt kilohertz: إذن des ultrasons، ما كنسمعوهمش، وما كيمشيوش فle vide.")
M2 = ("دابا نقراو le temps. نديرو le fond à soixante mètres. على اليمين، la courbe ديال les signaux en fonction de t. "
      "شوف: l'émission فاللول. la salve كتهبط، كتضرب فالأرض، وكترجع. ملي كترجع، كيبان l'écho. "
      "tau هو la durée بين l'émission وl'écho: البداية مع البداية. هنا l'axe بالmilliseconde، وtau égale quatre-vingts millisecondes. "
      "فالتمرين، ما عندناش des graduations، عندنا des divisions. "
      f"le nombre de divisions égale {dire(A['n1'])}، et une division égale {dire(A['sh'])} millisecondes. "
      f"إذن tau égale {dire(A['n1'])} fois {dire(A['sh'])}، donc tau égale {dire(A['tau1'])} millisecondes.")
M3 = ("تبع la salve. هي هابطة من le bateau حتى للأرض: هادي la distance d. "
      "من بعد، كترجع من الأرض ل le bateau: la distance d مرة أخرى. "
      "إذن فla durée tau، l'onde قطعات la distance deux d. la célérité هي la distance على la durée: v égale deux d sur tau. "
      "donc deux d égale v fois tau، وd égale v fois tau sur deux. يلا نسيتي la division par deux، كتلقى الضعف ديال la profondeur.")
M4 = ("نديرو le fond à soixante mètres. شوف: l'émission، ومن بعد l'écho. le sonar قرا tau égale quatre-vingts millisecondes. "
      "قبل الحساب، ديما نحولو la durée: quatre-vingts millisecondes égale zéro virgule zéro huit seconde. "
      "من بعد: d égale v fois tau sur deux، وv égale mille cinq cents mètres par seconde فالما ديال البحر. "
      "إذن d égale mille cinq cents fois zéro virgule zéro huit، sur deux. d égale soixante mètres، كيف مكتوب فla simulation. "
      "ورد البال: بلا ما تقسم par deux، كتلقى le double، cent vingt mètres، وهادا غلط.")
M5 = ("دابا le bateau فوق le banc ديال الحوت. la salve كتلقى le banc قبل الأرض، وجزء منها كيرجع. "
      "فla simulation، غادي نحطو le fond à trente mètres، بحال le banc. شوف: l'écho رجع après quarante millisecondes. "
      "l'obstacle قريب، إذن l'écho كيرجع بكري: هادا هو l'écho اللول. l'écho اللي من بعد هو ديال الأرض، à soixante mètres. "
      f"فالتمرين، l'écho اللول، à {dire(A['n2'])} divisions: tau prime égale {dire(A['tau2'])} millisecondes. "
      f"d prime égale {dire(A['v'])} fois {dire(A['tau2'] / 1000)}، sur deux، égale {dire(A['d2'])} mètres.")
assert A["tau1"] == 80 and A["d2"] == 30   # M2, M4, M5 décrivent la simulation avec ces valeurs

EXPL = [
  diapo_sim("ex_s1", "Question 1 : des ultrasons, une onde mécanique", "Au-delà de 20 kHz : ultrasons, non audibles ; une onde mécanique a besoin d'un milieu.",
            SIM, "Le sonar envoie une salve d'ultrasons dans l'eau", M1,
            [(f"N = {fr(A['N'])} kHz > 20 kHz : ultrasons", f"N égale {dire(A['N'])} kilohertz"), ("onde mécanique : milieu matériel", "كتحتاج un milieu matériel")],
            [dict(mot="كاين le sonar", repere="sonar"),
             dict(mot="le sonar كيصيفط", commande="play_until", parametres={"moment": "salve_descend"}),
             dict(mot="شوف la salve كتمشي", commande="play_until", parametres={"moment": "fond_atteint"}),
             dict(mot="كتحتاج un milieu matériel", cible="centre:1"),
             dict(mot=f"N égale {dire(A['N'])} kilohertz", cible="centre:0")]),
  diapo_sim("ex_s2", "Question 2 : lire τ, début avec début", "τ = nombre de divisions × sensibilité horizontale.",
            SIM, "L'émission, puis l'écho : τ entre les deux débuts", M2,
            [(f"τ = {fr(A['n1'])} div × {fr(A['sh'])} ms/div", f"إذن tau égale {dire(A['n1'])} fois {dire(A['sh'])}"),
             (f"τ = {fr(A['tau1'])} ms", f"donc tau égale {dire(A['tau1'])} millisecondes")],
            [dict(mot="نديرو le fond", commande="set_parameters", parametres={"d_m": 60}),
             dict(mot="شوف: l'émission فاللول", commande="play_until", parametres={"moment": "echo_recu"}),
             dict(mot="tau هو la durée", repere="tau"),
             dict(mot="هنا l'axe بالmilliseconde", repere="axe_t"),
             dict(mot=f"إذن tau égale {dire(A['n1'])} fois {dire(A['sh'])}", cible="centre:0"),
             dict(mot=f"donc tau égale {dire(A['tau1'])} millisecondes", cible="centre:1")]),
  diapo_sim("ex_s3", "Question 3 : l'aller et le retour", "Pendant τ, l'onde parcourt 2d : 2d = v·τ.",
            SIM, "La salve descend, se réfléchit, remonte", M3,
            [("aller + retour : 2d = v·τ", "v égale deux d sur tau"), ("d = v·τ/2", "وd égale v fois tau sur deux")],
            [dict(mot="هي هابطة", commande="play_until", parametres={"moment": "fond_atteint"}),
             dict(mot="هادي la distance d", repere="profondeur"),
             dict(mot="من بعد، كترجع", commande="play_until", parametres={"moment": "echo_recu"}),
             dict(mot="فla durée tau", repere="tau"),
             dict(mot="v égale deux d sur tau", cible="centre:0"),
             dict(mot="وd égale v fois tau sur deux", cible="centre:1"),
             dict(mot="وd égale v fois tau sur deux", repere="formule")]),
  diapo_sim("ex_s4", "Question 4 : la profondeur du fond", "τ en secondes, puis d = v·τ/2.",
            SIM, "Fond à 60 m : écho après 80 ms", M4,
            [("τ = 80 ms = 0,08 s", "quatre-vingts millisecondes égale zéro virgule zéro huit seconde"),
             (f"d = {A['v']} × 0,08/2 = {fr(A['d1'])} m", "d égale soixante mètres")],
            [dict(mot="نديرو le fond", commande="set_parameters", parametres={"d_m": 60}),
             dict(mot="شوف: l'émission", commande="play_until", parametres={"moment": "echo_recu"}),
             dict(mot="le sonar قرا tau", repere="tau"),
             dict(mot="quatre-vingts millisecondes égale zéro virgule zéro huit seconde", cible="centre:0"),
             dict(mot="d égale soixante mètres", cible="centre:1"),
             dict(mot="d égale soixante mètres", repere="formule")]),
  diapo_sim("ex_s5", "Question 5 : deux échos, lequel vient du banc ?", "L'obstacle le plus proche renvoie le premier écho.",
            SIM, "Obstacle à 30 m : écho après 40 ms", M5,
            [("1ᵉʳ écho : le banc, plus proche que le fond", "هادا هو l'écho اللول"),
             (f"d' = {A['v']} × {fr(A['tau2'] / 1000, 3)}/2 = {fr(A['d2'])} m", f"égale {dire(A['d2'])} mètres")],
            [dict(mot="غادي نحطو le fond", commande="set_parameters", parametres={"d_m": 30}),
             dict(mot="شوف: l'écho رجع", commande="play_until", parametres={"moment": "echo_recu"}),
             dict(mot="شوف: l'écho رجع", repere="tau"),
             dict(mot="هادا هو l'écho اللول", cible="centre:0"),
             dict(mot=f"égale {dire(A['d2'])} mètres", cible="centre:1")]),
]

# ---------- version facile ----------
FAC = [
  vf_facile("fa_s1", "Plus facile : ultrasons et milieu", "سؤال ساهل: قول واش كل جملة صحيحة ولا غالطة.",
            f"Le sonar émet une onde de fréquence {fr(A['N'])} kHz.", [
              (f"Une onde de fréquence {fr(A['N'])} kHz est audible par l'oreille humaine.", False, f"{fr(A['N'])} kHz > 20 kHz : c'est un ultrason, l'oreille ne l'entend pas."),
              ("Les ultrasons sont des ondes mécaniques : ils ne se propagent pas dans le vide.", True, "Une onde mécanique a besoin d'un milieu matériel (ici, l'eau de mer)."),
              ("Le sonar fonctionnerait aussi bien dans le vide.", False, "Sans milieu matériel, l'onde mécanique ne se propage pas.")]),
  qcm_facile("fa_s2", "Plus facile : lire τ", "سؤال ساهل: حسب tau من les divisions.",
             f"L'écho est à {fr(A['n1'])} divisions de l'émission ; sensibilité {fr(A['sh'])} ms/div. τ vaut…",
             [f"{fr(A['n1'])} ms", f"{fr(A['tau1'])} ms", f"{fr(A['n1'] / A['sh'], 2)} ms"], 1, {
               "1": {"juste": rep(f"برافو! tau égale {dire(A['n1'])} fois {dire(A['sh'])}، donc {dire(A['tau1'])} millisecondes.",
                                  f"Juste : τ = {fr(A['n1'])} × {fr(A['sh'])} = {fr(A['tau1'])} ms.")},
               "0": {"1": rep("ما تقلقش. هادا غير le nombre de divisions. شحال كتساوي une division؟ عاود اختار.",
                              "Ce sont des divisions, pas des ms : combien vaut une division ? Réessaie."),
                     "2": rep(f"la réponse est {dire(A['tau1'])} millisecondes. خاصك تضرب le nombre de divisions فla sensibilité، {dire(A['sh'])} millisecondes par division.",
                              f"Réponse : {fr(A['tau1'])} ms ; on multiplie les divisions par {fr(A['sh'])} ms/div.")},
               "2": {"1": rep("قريب! ولكن قسمتي. la sensibilité كتقول شحال فكل division، إذن كنضربو. عاود اختار.",
                              "Tu as divisé ; il faut multiplier par la sensibilité. Réessaie."),
                     "2": rep(f"la réponse est {dire(A['tau1'])} millisecondes: tau égale le nombre de divisions fois la sensibilité.",
                              f"Réponse : τ = {fr(A['n1'])} × {fr(A['sh'])} = {fr(A['tau1'])} ms.")}},
             f"L'écho est à {dire(A['n1'])} divisions de l'émission, sensibilité {dire(A['sh'])} millisecondes par division. Tau vaut ?"),
  assoc_facile("fa_s3", "Plus facile : l'aller-retour", "سؤال ساهل: ربط كل grandeur مع اللي كيناسبها.",
               "Relie chaque grandeur à ce qu'elle représente.", "Relie chaque grandeur à ce qu'elle représente.",
               [("1", "la durée τ mesurée"), ("2", "la distance parcourue pendant τ"), ("3", "la profondeur d")],
               [("a", "l'aller et le retour de l'onde"), ("b", "2d"), ("c", "v·τ/2")],
               {"1": "a", "2": "b", "3": "c"},
               {"1-a": (True, "Oui : τ va de l'émission à l'écho, aller et retour compris.", "صحيح: tau من l'émission حتى l'écho، فيه l'aller وle retour."),
                "1-b": (False, "2d est une distance, pas une durée. Cherche ce que dure τ.", "deux d هي distance، ماشي durée. tau شنو كيدوم؟"),
                "1-c": (False, "v·τ/2 est la profondeur, pas une durée.", "v fois tau sur deux هي la profondeur، ماشي durée."),
                "2-a": (False, "C'est une durée qui couvre l'aller et le retour ; ici on cherche une distance.", "l'aller et le retour هنا كيوصفو la durée. حنا باغيين la distance."),
                "2-b": (True, "Oui : la descente fait d et la remontée d : 2d en tout.", "صحيح: الهبوط d، والرجوع d، donc deux d."),
                "2-c": (False, "v·τ/2 est la moitié du chemin : c'est d, pas la distance totale.", "v fois tau sur deux هي النص، يعني d، ماشي la distance كاملة."),
                "3-a": (False, "La profondeur est une distance, pas l'aller-retour en temps.", "la profondeur هي distance، ماشي durée."),
                "3-b": (False, "2d, c'est le double de la profondeur : l'aller ET le retour.", "deux d هي الضعف ديال la profondeur."),
                "3-c": (True, "Oui : 2d = v·τ, donc d = v·τ/2.", "صحيح، car deux d égale v fois tau، إذن d égale v fois tau sur deux.")},
               ("Couples : (1 ; a) (2 ; b) (3 ; c).", "إذن tau هي durée ديال l'aller et le retour، la distance égale deux d، وla profondeur هي v fois tau sur deux.")),
  qcm_facile("fa_s4", "Plus facile : la profondeur", "سؤال ساهل: اختار la bonne profondeur.",
             f"τ = {fr(A['tau1'])} ms et v = {A['v']} m/s. La profondeur d vaut…",
             [f"{fr(2 * A['d1'])} m", f"{fr(A['d1'])} m", f"{fr(A['v'] * A['tau1'] / 2)} m"], 1, {
               "1": {"juste": rep(f"برافو! d égale {dire(A['v'])} fois {dire(A['tau1'] / 1000)}، sur deux، égale {dire(A['d1'])} mètres.",
                                  f"Juste : d = {A['v']} × {fr(A['tau1'] / 1000, 3)}/2 = {fr(A['d1'])} m.")},
               "0": {"1": rep("ما تقلقش. هادي la distance ديال l'aller et le retour. la profondeur شحال منها؟ عاود اختار.",
                              "C'est la distance aller-retour (2d). Réessaie."),
                     "2": rep(f"la réponse est {dire(A['d1'])} mètres. نسيتي la division par deux: l'onde مشات ورجعات.",
                              f"Réponse : {fr(A['d1'])} m ; il fallait diviser par 2 (aller et retour).")},
               "2": {"1": rep("قريب! ولكن tau بقات بالmilliseconde. حولها للseconde قبل الحساب. عاود اختار.",
                              "τ est resté en ms : convertis-le en s. Réessaie."),
                     "2": rep(f"la réponse est {dire(A['d1'])} mètres. tau égale {dire(A['tau1'] / 1000)} seconde، et non pas {dire(A['tau1'])}.",
                              f"Réponse : {fr(A['d1'])} m, avec τ = {fr(A['tau1'] / 1000, 3)} s.")}},
             f"Tau égale {dire(A['tau1'])} millisecondes et v égale {dire(A['v'])} mètres par seconde. La profondeur d vaut ?"),
  qcm_facile("fa_s5", "Plus facile : l'écho du banc", "سؤال ساهل: شكون l'écho ديال le banc؟",
             "Sur le document 2, quel écho vient du banc de poissons ?",
             [f"Le second (à {fr(A['n1'])} divisions)", f"Le premier (à {fr(A['n2'])} divisions)", "Les deux"], 1, {
               "1": {"juste": rep("برافو! le banc قريب من le bateau، إذن l'écho ديالو كيرجع اللول.",
                                  "Juste : le banc est plus proche que le fond, son écho revient le premier.")},
               "0": {"1": rep("ما تقلقش. شكون قريب ل le bateau: le banc ولا الأرض؟ اللي قريب كيرجع l'écho ديالو بكري. عاود اختار.",
                              "Qui est le plus proche du bateau ? Son écho revient plus tôt. Réessaie."),
                     "2": rep("الجواب هو l'écho اللول. l'écho الثاني جا من الأرض، اللي بعيدة.",
                              "Réponse : le premier écho ; le second vient du fond, plus loin.")},
               "2": {"1": rep("قريب! ولكن le banc et le fond، ce sont deux obstacles مختلفين. كل واحد عندو l'écho ديالو. عاود اختار.",
                              "Il y a deux obstacles : le banc et le fond, un écho chacun. Réessaie."),
                     "2": rep("الجواب هو l'écho اللول، ديال le banc. الثاني ديال الأرض.",
                              "Réponse : le premier écho vient du banc, le second du fond.")}},
             "Sur le document deux, quel écho vient du banc de poissons ?"),
]

# ---------- exercice semblable ----------
SQ = [
  {"id": "1", "texte": Q[0]["texte"], "reponse": phrase(ATT1.format(N=fr(B["N"]))), "clavier": CL1, "correction": corr1(B)},
  {"id": "2", "texte": Q[1]["texte"], "reponse": valeur("τ", B["tau1"], "ms", att2(B)), "clavier": CL2, "correction": corr2(B)},
  {"id": "3", "texte": Q[2]["texte"], "reponse": phrase(ATT3), "clavier": CL3, "correction": corr3()},
  {"id": "4", "texte": Q[3]["texte"], "reponse": valeur("d", B["d1"], "m", att4(B)), "clavier": CL4, "correction": corr4(B)},
  {"id": "5", "texte": Q[4]["texte"], "reponse": valeur("d'", B["d2"], "m", att5(B)), "clavier": CL5, "correction": corr5(B)},
]

EX = {
  "id": "phys_ex_ch1_sonar_5", "type": "exercice", "version": 1, "status": "published",
  "matiere": "physique", "chapitre": "ondes_mecaniques", "cours": "phys_ch1_waves_exemple",
  "titre": "Le sonar d'un bateau de pêche", "niveau": "moyen", "duree_min": 20,
  "origine": "Exercice original écrit pour Moalim (ni sujet du national, ni copie d'un livre ou d'une série).",
  "competences": ["Reconnaître un ultrason et le besoin d'un milieu matériel", "Lire une durée sur un oscillogramme (divisions × sensibilité)",
                  "Établir et appliquer d = v·τ/2 (écho)"],
  "enonce": {
    "intro": intro(A),
    "intro_dit": ("دابا نقراو l'énoncé. عندنا واحد le bateau ديال الصيد، فيه le sonar. تحت la coque، le sonar كيصيفط لتحت، "
                  f"فt égale zéro، واحد la salve ديال les ultrasons، la fréquence ديالها N égale {dire(A['N'])} kilohertz. "
                  "l'onde كتضرب فأول obstacle، الأرض ولا le banc ديال الحوت، وكترجع ل le sonar: هادا هو l'écho. "
                  "l'oscilloscope كيبين l'émission وl'écho. le document un فوق الأرض، وle document deux فوق le banc ديال الحوت. "
                  f"la célérité فالما ديال البحر، v égale {dire(A['v'])} mètres par seconde، وla sensibilité horizontale، {dire(A['sh'])} millisecondes par division."),
    "figures": figures(A), "donnees": donnees_txt(A), "questions": Q},
  "explication": {"activities": [{"id": "explication", "title": "Explication animée", "slides": EXPL}]},
  "facile": {"activities": [{"id": "facile", "title": "Plus facile, pour s'entraîner", "slides": FAC}]},
  "similaire": {"id": "phys_ex_ch1_sonar_5_b", "titre": "Même exercice, autres données",
    "enonce": {"intro": intro(B),
               "intro_dit": ("نفس التمرين، بقيم أخرى. le sonar كيصيفط des ultrasons، "
                             f"la fréquence N égale {dire(B['N'])} kilohertz. la sensibilité horizontale، {dire(B['sh'])} millisecondes par division، "
                             f"وv égale {dire(B['v'])} mètres par seconde."),
               "figures": figures(B), "donnees": donnees_txt(B), "questions": SQ}},
}


# ---------- contrôle des voix : jamais un mot darija juste avant un nombre français, aucun chiffre ----------
_NB = set("deux trois quatre cinq six sept huit neuf dix onze douze treize quatorze quinze seize vingt trente quarante cinquante soixante cent cents mille zéro quatre-vingts".split())
_AR = re.compile(r"[؀-ۿ]")


def controle_voix(o, k=""):
    pb = []
    if isinstance(o, dict):
        for kk, v in o.items():
            pb += controle_voix(v, kk)
    elif isinstance(o, list):
        for v in o:
            pb += controle_voix(v, k)
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
