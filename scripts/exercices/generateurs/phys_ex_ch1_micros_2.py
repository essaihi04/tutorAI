# Exercice de physique (ch. 1, ondes mécaniques progressives), niveau facile : le son entre deux micros (TP du cours).
# Sources comparées (skill exercices § 2) :
#  - exploration ondes_mecaniques_periodiques.json (partie ch1 : pièges « T = 4 divisions sans × sensibilité »,
#    « ms et µs », valeur repère 340 m/s) et experience_profs.json « ondes_mecaniques » (cas types « oscillogramme » :
#    début avec début, τ = n × S_H, conversion ms → s ; « géométrie » : récepteur éloigné ; insistance « le son a besoin
#    d'un milieu matériel, longitudinal dans l'air » ; piège « compter les carreaux au lieu des divisions »).
#  - Nationaux comparés : 2022 N ex. 2 (émetteur E et récepteur R à L = 85 cm, signal émis/reçu, Δt puis v, vrai/faux
#    « transversale ») ; 2024 R ex. 2 (deux micros, émetteur ENTRE eux, d − 2ℓ) ; 2021 R ex. 2 (barre, Δt = f(d)).
#    Ici : un clap AVANT deux micros alignés, d = 1,02 m, 0,5 ms/div, 6 divisions, puis M₂ reculé (nouveau retard) :
#    ni la situation ni les données ni l'enchaînement d'un national.
#  - Séries en ligne : recherche faite (talamidi « ondes mécaniques progressives, série corrigée 1 » : ultrasons ondes
#    mécaniques ; moutamadris 2BAC international « exercices PC 1-4 » ; alloschool élément 119785 ; Google Docs
#    « correction de la série 2BAC BIOF » : ondes sonores) mais la lecture des PDF est bloquée par le réseau de la
#    session (talamidi.com, moutamadris.ma, alloschool.com non résolus) : on s'appuie sur l'exploration et les nationaux.
#  - Simulation : micros.html (V = 340 m/s, S_H = 0,5 ms/div, set_parameters d_m par pas de 0,17 m) : d = 1,02 m donne
#    exactement 6 divisions et d' = 1,36 m 8 divisions, la simulation montre donc les valeurs de l'exercice.
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _outils import *

# ---------- les nombres en mots (voix) ----------
_U = "zéro un deux trois quatre cinq six sept huit neuf dix onze douze treize quatorze quinze seize dix-sept dix-huit dix-neuf".split()
_D = {2: "vingt", 3: "trente", 4: "quarante", 5: "cinquante", 6: "soixante"}


def _ent(n):
    if n < 20: return _U[n]
    if n < 70:
        d, u = divmod(n, 10)
        return _D[d] + ("" if u == 0 else " et un" if u == 1 else "-" + _U[u])
    if n < 80: return "soixante" + (" et onze" if n == 71 else "-" + _U[n - 60])
    if n < 100:
        u = n - 80
        return "quatre-vingt" + ("s" if u == 0 else "-" + _U[u])
    if n < 1000:
        c, r = divmod(n, 100)
        t = ("cent" if c == 1 else _U[c] + " cent" + ("s" if r == 0 else ""))
        return t + ("" if r == 0 else " " + _ent(r))
    m, r = divmod(n, 1000)
    t = "mille" if m == 1 else _ent(m) + " mille"
    return t + ("" if r == 0 else " " + _ent(r))


def mots(x, decimales=3):
    s = fr(x, decimales).replace("−", "-")
    neg = s.startswith("-"); s = s.lstrip("-")
    e, _, d = s.partition(",")
    t = _ent(int(e))
    if d:
        z = len(d) - len(d.lstrip("0"))
        t += " virgule " + " ".join(["zéro"] * z + ([_ent(int(d))] if d.strip("0") else []))
    return ("moins " if neg else "") + t


SIM = "/media/simulations/physics/ondes-tableau/micros.html"
TYPES = "/media/simulations/physics/ondes-tableau/types.html?depart=corde"


def donnees(d, SH, d2, v_reel):
    n = round(d / v_reel * 1000 / SH)           # divisions entre les deux débuts
    tau = n * SH * 1e-3                          # s
    v = d / tau
    tau2 = d2 / v
    return n, tau, v, tau2


def montage(d, titre):
    """Figure 1 : le clap, M₁ puis M₂ alignés, la distance d."""
    return {"type": "schema", "titre": titre, "cadre": {"l": 10, "h": 3.2},
            "legende": "Le clap est à gauche de M₁ : le son atteint M₁, puis M₂.",
            "elements": [
                {"f": "rect", "de": [0.4, 1.3], "a": [1.4, 1.8], "couleur": "orange", "remplir": "orange", "arrondi": True},
                {"f": "texte", "at": [0.9, 2.2], "t": "clap", "couleur": "orange"},
                {"f": "ligne", "pts": [[2.0, 1.55], [9.6, 1.55]], "couleur": "faible", "trait": "pointille"},
                {"f": "cercle", "c": [3.0, 1.55], "r": 0.22, "couleur": "cyan", "remplir": "cyan"},
                {"f": "ligne", "pts": [[3.0, 1.33], [3.0, 0.5]], "couleur": "cyan"},
                {"f": "texte", "at": [3.0, 2.2], "t": "M₁", "couleur": "cyan"},
                {"f": "cercle", "c": [8.0, 1.55], "r": 0.22, "couleur": "jaune", "remplir": "jaune"},
                {"f": "ligne", "pts": [[8.0, 1.33], [8.0, 0.5]], "couleur": "jaune"},
                {"f": "texte", "at": [8.0, 2.2], "t": "M₂", "couleur": "jaune"},
                {"f": "cote", "de": [3.0, 0.3], "a": [8.0, 0.3], "t": f"d = {fr(d)} m", "couleur": "blanc", "pos": "n"},
                {"f": "fleche", "de": [4.5, 2.75], "a": [6.5, 2.75], "texte": "sens de propagation du son", "couleur": "vert", "pos": "n"},
                {"f": "texte", "at": [5.5, 1.0], "t": "vers l'oscilloscope (voies 1 et 2)", "couleur": "faible", "taille": "petit"}]}


def oscillo(SH, n, titre):
    """Figure 2 : l'oscillogramme, 10 divisions × 6 ; voie 1 (M₁) commence à 0,5 div, voie 2 (M₂) n divisions plus tard."""
    el = []
    for i in range(11):
        el.append({"f": "ligne", "pts": [[i, 0], [i, 6]], "couleur": "faible", "trait": "pointille" if 0 < i < 10 else "plein"})
    for j in range(7):
        el.append({"f": "ligne", "pts": [[0, j], [10, j]], "couleur": "faible", "trait": "pointille" if 0 < j < 6 else "plein"})

    def voie(y0, x0, couleur):
        pts = [[0, y0], [x0, y0]]
        for k in range(1, 121):
            u = k / 120 * 2.2                                  # 2,2 divisions de signal
            a = math.exp(-u / 0.7) * math.sin(2 * math.pi * 3.2 * u / 2.2 * 1.0)
            if x0 + u <= 10:
                pts.append([round(x0 + u, 3), round(y0 + 0.9 * a, 3)])
        if pts[-1][0] < 10:
            pts.append([10, y0])
        return {"f": "ligne", "pts": pts, "couleur": couleur, "epais": True}
    el.append(voie(4.5, 0.5, "cyan"))
    el.append(voie(1.5, 0.5 + n, "jaune"))
    el += [{"f": "texte", "at": [0.6, 5.55], "t": "voie 1 : M₁", "couleur": "cyan", "ancre": "gauche", "taille": "petit"},
           {"f": "texte", "at": [0.6, 2.55], "t": "voie 2 : M₂", "couleur": "jaune", "ancre": "gauche", "taille": "petit"},
           {"f": "texte", "at": [7.6, 5.55], "t": f"S_H = {fr(SH)} ms/div", "couleur": "blanc", "taille": "petit"}]
    return {"type": "schema", "titre": titre, "cadre": {"l": 10, "h": 6}, "ratio": 0.6,
            "legende": "Chaque carreau est une division ; on compare le début d'un signal avec le début de l'autre.",
            "elements": el}


# ---------- données de l'exercice (= la simulation) ----------
V_AIR = 340
D, SH, D2 = 1.02, 0.5, 1.36
N, TAU, VV, TAU2 = donnees(D, SH, D2, V_AIR)
assert N == 6 and abs(VV - 340) < 1e-9 and abs(TAU2 - 4e-3) < 1e-12
tau_ms, tau2_ms = TAU * 1000, TAU2 * 1000

# ---------- similaire ----------
Db, SHb, D2b = 0.69, 0.25, 1.38
Nb, TAUb, VVb, TAU2b = donnees(Db, SHb, D2b, 345)
assert Nb == 8 and abs(VVb - 345) < 1e-9
taub_ms, tau2b_ms = TAUb * 1000, TAU2b * 1000

EX = {
  "id": "phys_ex_ch1_micros_2", "type": "exercice", "version": 1, "status": "published",
  "matiere": "physique", "chapitre": "ondes_mecaniques", "cours": "phys_ch1_waves_exemple",
  "titre": "Le son entre deux micros", "niveau": "facile", "duree_min": 15,
  "origine": "Exercice original écrit pour Moalim (ni sujet du national, ni copie d'un livre).",
  "competences": ["Reconnaître le son comme une onde mécanique longitudinale",
                  "Lire un retard sur un oscillogramme : τ = n × S_H, puis v = d/τ",
                  "Calculer le retard pour une autre distance : τ' = d'/v"],
  "enonce": {
    "intro": (f"Pour mesurer la célérité du son dans l'air, on place deux microphones M₁ et M₂ sur une même droite, à la distance "
              f"d = {fr(D)} m l'un de l'autre (figure 1). On frappe un clap devant M₁ : le son arrive d'abord en M₁, puis en M₂. "
              f"Les deux micros sont reliés aux voies 1 et 2 d'un oscilloscope ; la figure 2 montre l'enregistrement obtenu, "
              f"avec la sensibilité horizontale S_H = {fr(SH)} ms/div."),
    "intro_dit": (f"دابا نقراو l'énoncé. باش نقيسو la célérité ديال الصوت فالهوا، حطينا les deux micros، M un وM deux، على نفس الخط. "
                  f"la distance بيناتهم، d égale {mots(D)} mètre. كنضربو بيدينا قدام M un: الصوت كيوصل اللول ل M un، ومن بعد ل M deux. "
                  f"les deux micros مربوطين ب l'oscilloscope، وla figure deux كتبين l'enregistrement. "
                  f"la sensibilité horizontale، S H égale {mots(SH)} milliseconde par division."),
    "figures": [montage(D, "Figure 1 : le montage"), oscillo(SH, N, "Figure 2 : l'oscillogramme")],
    "donnees": [f"d = M₁M₂ = {fr(D)} m", f"Sensibilité horizontale : S_H = {fr(SH)} ms/div",
                f"Question 3 : M₂ est reculé, d' = M₁M₂ = {fr(D2)} m"],
    "questions": [
      {"id": "1", "texte": "Le son est-il une onde mécanique ? Est-il une onde transversale ou longitudinale ? Justifier.",
       "texte_dit": "la question un: واش الصوت onde mécanique؟ واش هو transversale ولا longitudinale؟ justifier.",
       "reponse": phrase("Le son est une onde mécanique : il a besoin d'un milieu matériel (ici l'air) pour se propager, il ne se propage pas "
                         "dans le vide. Il est longitudinal : l'air se déplace en avant et en arrière dans la même direction que la "
                         "propagation (direction de la perturbation parallèle à la direction de propagation)."),
       "clavier": {"aides": ["milieu matériel", "direction de la perturbation", "direction de propagation", "parallèle"],
                   "pieges": ["perpendiculaire", "se propage dans le vide"]},
       "aides": [
         aide("Deux idées : de quoi le son a-t-il besoin pour avancer ? Et comment bouge l'air quand le son passe, par rapport au sens où le son avance ?",
              "جوج أفكار: شنو خاص الصوت باش يمشي؟ وكيفاش كيتحرك الهوا ملي كيدوز الصوت، بالمقارنة مع الاتجاه اللي كيمشي فيه الصوت؟"),
         aide("Mécanique : il faut un milieu matériel. Pour le type, compare la direction de la perturbation et la direction de propagation : parallèles → longitudinale, perpendiculaires → transversale.",
              "onde mécanique: خاصها un milieu matériel. وباش تعرف النوع، قارن la direction de la perturbation مع la direction de propagation: يلا كانو فنفس الخط، longitudinale. يلا كانو perpendiculaires، transversale.")],
       "correction": correction([
           ("1 : le son a besoin d'un milieu matériel (l'air) : il ne se propage pas dans le vide, c'est une onde mécanique.", "خاصو un milieu matériel"),
           ("L'air se déplace dans la direction de propagation : la direction de la perturbation est parallèle à la direction de propagation.", "فنفس الاتجاه اللي كيمشي فيه الصوت"),
           ("Donc le son est une onde longitudinale.", "إذن الصوت onde longitudinale")],
           "la question un. الصوت خاصو un milieu matériel، هنا الهوا. فالفراغ ما كيمشيش، إذن هو onde mécanique. "
           "ملي كيدوز الصوت، الهوا كيتحرك للقدام وكيرجع، فنفس الاتجاه اللي كيمشي فيه الصوت. "
           "إذن الصوت onde longitudinale، ماشي transversale."),
       "explication": "ex_m1", "facile": "fa_m1"},
      {"id": "2", "texte": "Déterminer, à partir de la figure 2, le retard τ du signal de M₂ par rapport à celui de M₁, puis calculer la célérité v du son dans l'air.",
       "texte_dit": "la question deux: من la figure deux، حدد le retard tau ديال le signal ديال M deux بالنسبة ل M un، ومن بعد حسب la célérité v ديال الصوت فالهوا.",
       "reponse": valeur("v", VV, "m/s", f"τ = {N} × {fr(SH)} = {fr(tau_ms)} ms = {sci(TAU)} s ; v = d/τ = {fr(D)}/({sci(TAU)}) = {fr(VV, 0)} m/s"),
       "clavier": {"aides": ["τ = n × S_H", "v = d/τ", "1 ms = 10⁻³ s", "m/s", "A.N. :"],
                   "pieges": ["v = τ/d", "τ en ms dans v = d/τ"]},
       "aides": [
         aide("Compte les divisions entre le DÉBUT du signal de la voie 1 et le DÉBUT du signal de la voie 2, puis multiplie par la valeur d'une division.",
              "حسب les divisions بين البداية ديال le signal فla voie un، والبداية ديال le signal فla voie deux. البداية مع البداية، ماشي مع القمة. ومن بعد ضرب فla sensibilité."),
         aide("τ = n × S_H, converti en secondes (1 ms = 10⁻³ s). Pendant τ, le son parcourt d : v = d/τ.",
              "tau égale le nombre de divisions fois S H، ومن بعد حولها لla seconde: une milliseconde égale dix puissance moins trois seconde. فهاد la durée، الصوت كيقطع d. إذن v égale d sur tau.")],
       "correction": correction([
           (f"2 : entre les deux débuts, n = {N} divisions : τ = n × S_H = {N} × {fr(SH)} = {fr(tau_ms)} ms = {sci(TAU)} s", "tau égale n fois S H"),
           ("Pendant τ, le son parcourt d : v = d/τ", "v égale d sur tau"),
           (f"v = {fr(D)}/({sci(TAU)}) = {fr(VV, 0)} m/s", f"v égale {mots(VV)} mètres par seconde")],
           f"la question deux. بين البداية ديال les deux signaux، le nombre de divisions égale {mots(N)}. إذن tau égale n fois S H، c'est-à-dire {mots(N)} fois {mots(SH)}، "
           f"égale {mots(tau_ms)} millisecondes، c'est-à-dire {mots(tau_ms)} fois dix puissance moins trois seconde. "
           f"فهاد la durée، الصوت قطع d. إذن v égale d sur tau، c'est-à-dire {mots(D)} sur {mots(tau_ms)} fois dix puissance moins trois. "
           f"v égale {mots(VV)} mètres par seconde. هادي هي la valeur ديال الصوت فالهوا."),
       "explication": "ex_m2", "facile": "fa_m2"},
      {"id": "3", "texte": f"On recule M₂ sur la même droite : la distance devient d' = {fr(D2)} m. Calculer le nouveau retard τ' entre les deux signaux.",
       "texte_dit": f"la question trois: كنبعدو M deux على نفس الخط، وla distance كتولي d prime égale {mots(D2)} mètre. حسب le nouveau retard tau prime.",
       "reponse": valeur("τ'", TAU2, "s", f"τ' = d'/v = {fr(D2)}/{fr(VV, 0)} = {sci(TAU2)} s"),
       "clavier": {"aides": ["τ' = d'/v", "d'", "v", "s", "A.N. :"],
                   "pieges": ["τ' = v/d'", "τ' = τ (le retard ne change pas)"]},
       "aides": [
         aide("La célérité dépend du milieu (l'air), pas de la distance : v ne change pas. Quelle distance le son parcourt-il maintenant entre M₁ et M₂ ?",
              "la célérité كتبقى هي هي، حيت le milieu هو نفسو، الهوا. دابا شحال من distance كيقطع الصوت بين M un وM deux؟"),
         aide("Le son parcourt d' pendant τ' à la même célérité v : τ' = d'/v.",
              "الصوت كيقطع d prime فla durée tau prime، بنفس la célérité v. إذن tau prime égale d prime sur v.")],
       "correction": correction([
           ("3 : le milieu est le même, donc v ne change pas ; le son parcourt d' pendant τ'", "v ما كتبدلش"),
           (f"τ' = d'/v = {fr(D2)}/{fr(VV, 0)}", "tau prime égale d prime sur v"),
           (f"τ' = {sci(TAU2)} s = {fr(tau2_ms)} ms", f"tau prime égale {mots(tau2_ms)} millisecondes")],
           f"la question trois. le milieu هو نفسو، إذن v ما كتبدلش. دابا الصوت كيقطع d prime. "
           f"إذن tau prime égale d prime sur v، c'est-à-dire {mots(D2)} sur {mots(VV)}. "
           f"tau prime égale {mots(tau2_ms)} fois dix puissance moins trois seconde، يعني tau prime égale {mots(tau2_ms)} millisecondes. "
           f"على l'oscilloscope، c'est {mots(round(tau2_ms / SH))} divisions."),
       "explication": "ex_m3", "facile": "fa_m3"}
    ]
  },
  "explication": {"activities": [{"id": "explication", "title": "Explication animée", "slides": [
    diapo_sim("ex_m1", "Question 1 : le son, une onde mécanique longitudinale",
      "L'air bouge dans la direction où le son avance : onde longitudinale ; sans air, pas de son.",
      TYPES, "Le son dans l'air : compressions et dilatations",
      "شوف فالتجربة. هنا الصوت فالهوا. الهوا كيتحرك للقدام وكيرجع، فالاتجاه اللي كيمشي فيه الصوت. "
      "la direction de la perturbation، parallèle à la direction de propagation. إذن الصوت onde longitudinale. "
      "وفالفراغ ما كاينش الصوت، حيت خاصو الهوا باش يتحرك. إذن الصوت onde mécanique، خاصو un milieu matériel. "
      "فالتمرين، الصوت ديال اليد كيمشي فالهوا حتى ل les micros، إذن هو onde mécanique longitudinale.",
      [("Perturbation ∥ propagation → longitudinale", "parallèle à la direction de propagation"),
       ("Besoin d'un milieu matériel → onde mécanique", "خاصو un milieu matériel")],
      [dict(mot="هنا الصوت فالهوا", commande="play_until", parametres={"moment": "son"}),
       dict(mot="الهوا كيتحرك للقدام وكيرجع", repere="son_type"),
       dict(mot="parallèle à la direction de propagation", cible="centre:0"),
       dict(mot="خاصو un milieu matériel", cible="centre:1")]),
    diapo_sim("ex_m2", "Question 2 : τ sur l'oscillogramme, puis v",
      "Début avec début : τ = n × S_H ; puis v = d/τ.",
      SIM, "Deux micros et un oscilloscope",
      f"شوف الصوت. كنضرب بيدي، والصوت كيوصل اللول ل M un، ومن بعد ل M deux. "
      f"فالتجربة بعدنا M deux، وla distance دابا d égale {mots(D)} mètre، بحال التمرين. "
      f"شوف l'oscilloscope: la sensibilité horizontale, de {mots(SH)} milliseconde par division. "
      f"كنحسبو les divisions من البداية ديال le signal اللول، حتى البداية ديال le signal الثاني. le nombre de divisions égale {mots(N)}. "
      f"إذن tau égale {mots(N)} fois {mots(SH)}، c'est-à-dire {mots(tau_ms)} millisecondes. "
      f"ومن بعد v égale d sur tau، c'est-à-dire {mots(D)} sur {mots(tau_ms)} fois dix puissance moins trois. v égale {mots(VV)} mètres par seconde.",
      [("τ = n × S_H = " + f"{N} × {fr(SH)} = {fr(tau_ms)} ms", f"إذن tau égale {mots(N)} fois {mots(SH)}"),
       (f"v = d/τ = {fr(D)}/({sci(TAU)}) = {fr(VV, 0)} m/s", f"v égale {mots(VV)} mètres par seconde")],
      [dict(mot="شوف الصوت", commande="set_parameters", parametres={"d_m": D}),
       dict(mot="كنضرب بيدي", commande="play_until", parametres={"moment": "son_part"}),
       dict(mot="كيوصل اللول ل M un", commande="play_until", parametres={"moment": "m1_atteint"}),
       dict(mot="ومن بعد ل M deux", commande="play_until", parametres={"moment": "m2_atteint"}),
       dict(mot="ومن بعد ل M deux", repere="micro_2"),
       dict(mot="la sensibilité horizontale", repere="sensibilite"),
       dict(mot="كنحسبو les divisions", commande="play_until", parametres={"moment": "mesure"}),
       dict(mot=f"le nombre de divisions égale {mots(N)}", repere="retard"),
       dict(mot=f"إذن tau égale {mots(N)} fois {mots(SH)}", cible="centre:0"),
       dict(mot=f"v égale {mots(VV)} mètres par seconde", cible="centre:1")]),
    diapo_sim("ex_m3", "Question 3 : on recule M₂",
      "Même air, même célérité : le retard grandit avec la distance, τ' = d'/v.",
      SIM, "M₂ reculé : le retard augmente",
      f"دابا بعدنا M deux أكثر. la distance devient {mots(D2)} mètre. الهوا هو نفسو، إذن la célérité reste {mots(VV)} mètres par seconde. "
      f"شوف: الصوت كيوصل ل M deux من بعد. على l'oscilloscope، le signal الثاني بعد أكثر: maintenant {mots(round(tau2_ms / SH))} divisions. "
      f"إذن tau prime égale d prime sur v، c'est-à-dire {mots(D2)} sur {mots(VV)}. tau prime égale {mots(tau2_ms)} millisecondes.",
      [("τ' = d'/v", "إذن tau prime égale d prime sur v"),
       (f"τ' = {fr(D2)}/{fr(VV, 0)} = {fr(tau2_ms)} ms", f"tau prime égale {mots(tau2_ms)} millisecondes")],
      [dict(mot="دابا بعدنا M deux أكثر", commande="set_parameters", parametres={"d_m": D2}),
       dict(mot="دابا بعدنا M deux أكثر", repere="micro_2"),
       dict(mot="الصوت كيوصل ل M deux من بعد", commande="play_until", parametres={"moment": "m2_atteint"}),
       dict(mot="على l'oscilloscope", commande="play_until", parametres={"moment": "mesure"}),
       dict(mot="على l'oscilloscope", repere="retard"),
       dict(mot="إذن tau prime égale d prime sur v", cible="centre:0"),
       dict(mot=f"tau prime égale {mots(tau2_ms)} millisecondes", cible="centre:1")]),
  ]}]},
  "facile": {"activities": [{"id": "facile", "title": "Plus facile, pour s'entraîner", "slides": [
    vf_facile("fa_m1", "Plus facile : vrai ou faux sur le son", "سؤال ساهل: قول واش كل جملة صحيحة ولا غالطة.",
      "Le son d'un clap arrive à deux micros, à travers l'air.", [
        ("Le son peut se propager dans le vide.", False, "Faux : le son est une onde mécanique, il lui faut un milieu matériel (l'air, l'eau, un solide)."),
        ("Dans l'air, le son est une onde longitudinale.", True, "Vrai : l'air bouge en avant et en arrière, dans la direction de propagation."),
        ("Dans l'air, le son est une onde transversale.", False, "Faux : la perturbation n'est pas perpendiculaire à la propagation, elle lui est parallèle.")]),
    qcm_facile("fa_m2", "Plus facile : lire τ", "سؤال ساهل: نقراو tau.",
      f"Entre les débuts des deux signaux, il y a {N} divisions ; S_H = {fr(SH)} ms/div. Le retard τ vaut…",
      [f"τ = {N} ms", f"τ = {fr(tau_ms)} ms", f"τ = {fr(N / SH)} ms"], 1, {
        "1": {"juste": rep(f"برافو! tau égale le nombre de divisions fois S H, c'est-à-dire {mots(N)} fois {mots(SH)}, égale {mots(tau_ms)} millisecondes.",
                           f"Juste : τ = {N} × {fr(SH)} = {fr(tau_ms)} ms.")},
        "0": {"1": rep(f"ما تقلقش. {mots(N)} هو عدد les divisions، ماشي le temps. شحال كتساوي la division؟ عاود اختار.",
                       f"{N}, ce sont des divisions, pas des millisecondes. Combien vaut une division ? Réessaie."),
              "2": rep(f"la réponse est {mots(tau_ms)} millisecondes. خاصك تضرب les {mots(N)} divisions fois la sensibilité, de {mots(SH)} milliseconde par division.",
                       f"Réponse : τ = {N} × {fr(SH)} = {fr(tau_ms)} ms : on multiplie par la sensibilité.")},
        "2": {"1": rep("قريب! ولكن قسمتي على la sensibilité. la sensibilité كتقول شحال فيها la division. واش كنضربو ولا كنقسمو؟ عاود اختار.",
                       "Tu as divisé par la sensibilité. Une division vaut 0,5 ms : on multiplie. Réessaie."),
              "2": rep(f"la réponse est {mots(tau_ms)} millisecondes. tau égale n fois S H، ماشي n sur S H.",
                       f"Réponse : τ = n × S_H = {fr(tau_ms)} ms (et non n/S_H).")}},
      f"Entre les débuts des deux signaux, il y a {mots(N)} divisions, et S H égale {mots(SH)} milliseconde par division. Le retard tau vaut ?"),
    assoc_facile("fa_m3", "Plus facile : relier", f"سؤال ساهل: ربط كل حالة مع le retard ديالها. v égale {mots(VV)} mètres par seconde.",
      f"Le son va à v = {fr(VV, 0)} m/s dans l'air.", "Relie chaque distance M₁M₂ au retard τ entre les deux signaux.",
      [("1", f"d = {fr(D)} m"), ("2", f"d' = {fr(D2)} m")],
      [("a", f"{fr(tau_ms)} ms"), ("b", f"{fr(tau2_ms)} ms"), ("c", f"{fr(D2 * VV, 1)} ms")],
      {"1": "a", "2": "b"},
      {"1-a": (True, f"Oui : τ = d/v = {fr(D)}/{fr(VV, 0)} = {fr(tau_ms)} ms.", f"برافو: tau égale d sur v، c'est-à-dire {mots(tau_ms)} millisecondes."),
       "1-b": (False, f"{fr(tau2_ms)} ms, c'est pour une distance plus grande ; pour d = {fr(D)} m, calcule d/v.", "لا، هادا le retard ديال distance كبر. حسب d sur v."),
       "1-c": (False, "Ce nombre vient de d × v : le retard est d/v, pas d × v.", "لا، هادا d fois v. le retard هو d sur v."),
       "2-a": (False, "Plus loin, le retard est plus grand : il ne peut pas être le même que pour d.", "لا، ملي كنبعدو M deux، le retard كيكبر."),
       "2-b": (True, f"Oui : τ' = d'/v = {fr(D2)}/{fr(VV, 0)} = {fr(tau2_ms)} ms.", f"برافو: tau prime égale d prime sur v، c'est-à-dire {mots(tau2_ms)} millisecondes."),
       "2-c": (False, "Ce nombre vient de d' × v : le retard est d'/v.", "لا، هادا d prime fois v. le retard هو d prime sur v.")},
      ("(1 ; a) (2 ; b) : τ = d/v, le retard grandit avec la distance ; c est le piège d × v.",
       "le retard كيكبر مع la distance: tau égale d sur v. والجواب c هو le piège ديال d fois v.")),
  ]}]},
  "similaire": {
    "id": "phys_ex_ch1_micros_2_b", "titre": "Même exercice, autres données",
    "enonce": {
      "intro": (f"Même expérience un jour plus chaud. Les micros M₁ et M₂ sont à d = {fr(Db)} m l'un de l'autre. "
                f"L'oscillogramme (figure 2) est enregistré avec S_H = {fr(SHb)} ms/div."),
      "intro_dit": (f"نفس التجربة، بقيم أخرى، فنهار سخون. d égale {mots(Db)} mètre، وla sensibilité horizontale "
                    f"S H égale {mots(SHb)} milliseconde par division."),
      "figures": [montage(Db, "Figure 1 : le montage"), oscillo(SHb, Nb, "Figure 2 : l'oscillogramme")],
      "donnees": [f"d = {fr(Db)} m", f"S_H = {fr(SHb)} ms/div", f"Question 3 : d' = {fr(D2b)} m"],
      "questions": [
        {"id": "1", "texte": "Le son est-il une onde mécanique ? Transversale ou longitudinale ? Justifier.",
         "reponse": phrase("Onde mécanique : il lui faut un milieu matériel (l'air), pas de son dans le vide. Longitudinale : la direction de "
                           "la perturbation (l'air avance et recule) est parallèle à la direction de propagation."),
         "clavier": {"aides": ["milieu matériel", "parallèle", "direction de propagation"], "pieges": ["perpendiculaire"]},
         "correction": correction([("1 : besoin d'un milieu matériel : onde mécanique", "خاصو un milieu matériel"),
                                   ("perturbation parallèle à la propagation : onde longitudinale", "إذن onde longitudinale")],
                                  "الصوت خاصو un milieu matériel، إذن onde mécanique. الهوا كيتحرك فنفس الاتجاه ديال la propagation، إذن onde longitudinale.")},
        {"id": "2", "texte": "Déterminer le retard τ sur la figure 2, puis calculer la célérité v du son.",
         "reponse": valeur("v", VVb, "m/s", f"τ = {Nb} × {fr(SHb)} = {fr(taub_ms)} ms = {sci(TAUb)} s ; v = d/τ = {fr(Db)}/({sci(TAUb)}) = {fr(VVb, 0)} m/s"),
         "clavier": {"aides": ["τ = n × S_H", "v = d/τ", "1 ms = 10⁻³ s"], "pieges": ["v = τ/d"]},
         "correction": correction([(f"2 : τ = {Nb} × {fr(SHb)} = {fr(taub_ms)} ms", "tau égale n fois S H"),
                                   (f"v = d/τ = {fr(Db)}/({sci(TAUb)}) = {fr(VVb, 0)} m/s", "v égale d sur tau")],
                                  f"tau égale n fois S H، c'est-à-dire {mots(Nb)} fois {mots(SHb)}، égale {mots(taub_ms)} millisecondes. "
                                  f"v égale d sur tau، c'est-à-dire {mots(Db)} sur {mots(taub_ms)} fois dix puissance moins trois. v égale {mots(VVb)} mètres par seconde.")},
        {"id": "3", "texte": f"On recule M₂ : d' = {fr(D2b)} m. Calculer le nouveau retard τ'.",
         "reponse": valeur("τ'", TAU2b, "s", f"τ' = d'/v = {fr(D2b)}/{fr(VVb, 0)} = {sci(TAU2b)} s"),
         "clavier": {"aides": ["τ' = d'/v", "s"], "pieges": ["τ' = v/d'"]},
         "correction": correction([(f"3 : τ' = d'/v = {fr(D2b)}/{fr(VVb, 0)}", "tau prime égale d prime sur v"),
                                   (f"τ' = {sci(TAU2b)} s = {fr(tau2b_ms)} ms", f"égale {mots(tau2b_ms)} millisecondes")],
                                  f"v ما كتبدلش. tau prime égale d prime sur v، c'est-à-dire {mots(D2b)} sur {mots(VVb)}، "
                                  f"égale {mots(tau2b_ms)} millisecondes.")}
      ]}}
}

ecrire(EX)
