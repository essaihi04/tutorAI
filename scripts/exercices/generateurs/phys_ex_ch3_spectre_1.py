# Exercice facile de physique, ch. 3 (propagation d'une onde lumineuse) : une radiation monochromatique,
# sa fréquence ν = c/λ₀, visible ou non, sa couleur, et la propagation dans le vide.
#
# Sources comparées (skill exercices § 2) :
# - exploration backend/data/curriculum/exploration/ondes_lumineuses.json : cas_types « frequence » (ν = c/λ₀ avec λ₀ en m,
#   visible si 400 nm ≤ λ₀ ≤ 800 nm écrit en encadrement), pieges (λ₀ laissée en nm ; 400 µm au lieu de 400 nm ;
#   « la lumière est une onde mécanique »), erreurs_examen « fréquence et milieu », a_ne_pas_dire (lumière = onde mécanique).
# - vidéos des 10 profs (sources.videos) : Bazhar et Rahou (ν = c/λ₀, ordre 10¹⁴ Hz), Driss (rappel cloche à vide / Soleil).
# - nationaux comparés : 2021 N ex. 2 (ν_j = c/λ₀ pour la raie jaune 589 nm dans un prisme), 2023 R et 2025 R (QCM :
#   la fréquence caractérise la radiation, la lumière n'est pas une onde mécanique), 2024 R (vrai/faux « les ondes
#   lumineuses sont des ondes mécaniques »). Le nôtre : raie verte du mercure 546 nm (et infrarouge 1064 nm dans le
#   semblable), sans prisme ; la propagation dans le vide est demandée par une situation (la Lune), pas en QCM.
# - séries en ligne : recherche web faite (talamidi « propagation des ondes lumineuses, série corrigée 1 », moutamadris
#   séries 1 et 2 BIOF, une série Google Docs « ondes lumineuses 2 Bac ») : seuls les titres et extraits des moteurs
#   étaient lisibles, l'ouverture des PDF est bloquée par le réseau de la session (talamidi.com, moutamadris.ma) ;
#   situations classiques notées : laser, λ dans le vide → couleur et fréquence. Rien n'est copié.
import sys, os, math, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _outils import *
# ---------- nombres dits en mots français (calculés, jamais tapés à la main) ----------
_U = ["zéro", "un", "deux", "trois", "quatre", "cinq", "six", "sept", "huit", "neuf", "dix", "onze", "douze", "treize",
      "quatorze", "quinze", "seize"]
_D = {2: "vingt", 3: "trente", 4: "quarante", 5: "cinquante", 6: "soixante"}


def entier(n):
    """Un entier (0 ≤ n < 10⁶) en mots français."""
    if n < 17:
        return _U[n]
    if n < 20:
        return "dix-" + _U[n - 10]
    if n < 70:
        d, u = divmod(n, 10)
        return _D[d] + ("" if u == 0 else " et un" if u == 1 else "-" + _U[u])
    if n < 80:
        return "soixante" + (" et onze" if n == 71 else "-" + entier(n - 60))
    if n < 100:
        return "quatre-vingts" if n == 80 else "quatre-vingt-" + entier(n - 80)
    if n < 1000:
        c, r = divmod(n, 100)
        tete = "cent" if c == 1 else _U[c] + (" cents" if r == 0 else " cent")
        return tete if r == 0 else tete + " " + entier(r)
    m, r = divmod(n, 1000)
    tete = "mille" if m == 1 else entier(m) + " mille"
    return tete if r == 0 else tete + " " + entier(r)


def dit(x, decimales=2):
    """5.49 -> « cinq virgule quarante-neuf » ; 0.08 -> « zéro virgule zéro huit » (même arrondi que fr())."""
    s = fr(x, decimales).replace("−", "-")
    neg = s.startswith("-")
    s = s.lstrip("-")
    e, _, f = s.partition(",")
    out = entier(int(e))
    if f:
        if f.startswith("0") or len(f) > 2:
            out += " virgule " + " ".join(_U[int(c)] for c in f)
        else:
            out += " virgule " + entier(int(f))
    return ("moins " if neg else "") + out


def sci_dit(x, chiffres=3):
    """5.4945e14 -> « cinq virgule quarante-neuf fois dix puissance quatorze » (comme sci())."""
    e = math.floor(math.log10(abs(x)))
    m = round(x / 10 ** e, chiffres - 1)
    if abs(m) >= 10:
        m /= 10; e += 1
    t = dit(m, chiffres - 1)
    if e == 0:
        return t
    return t + " fois dix puissance " + ("moins " + entier(-e) if e < 0 else entier(e))


_NOMBRES = set(_U[1:]) | {"zéro", "vingt", "trente", "quarante", "cinquante", "soixante", "cent", "cents", "mille",
                           "dix-sept", "dix-huit", "dix-neuf", "quatre-vingts"}
_AR = re.compile(r"[؀-ۿ]")


def controle_voix(EX):
    """Aucun mot arabe juste avant un nombre français ; aucun chiffre dans une voix."""
    pb = []
    champs = {"mixed", "dit", "parole", "intro_dit", "texte_dit", "enonce_dit", "mot"}

    def walk(o, k=""):
        if isinstance(o, dict):
            for kk, v in o.items():
                walk(v, kk)
        elif isinstance(o, list):
            for v in o:
                walk(v, k)
        elif isinstance(o, str) and k in champs:
            if re.search(r"\d", o):
                pb.append(("chiffre", o[:80]))
            toks = o.split()
            for a, b in zip(toks, toks[1:]):
                b0 = b.strip("،,.:;!?()«»").split("-")[0]
                if _AR.search(a.strip("،؟:.")) and (b0 in _NOMBRES or b.strip("،,.:;!?") in _NOMBRES):
                    pb.append(("arabe+nombre", a + " " + b, o[:60]))
    walk(EX)
    if pb:
        raise AssertionError("\n".join(map(str, pb)))


# ---------- données ----------
C = 3.00e8
SIM = "/media/simulations/physics/ondes-lumineuses-tableau/"


def couleur(l):
    """Mêmes bornes que spectre.html (nomCouleur)."""
    if l < 400 or l > 800: return None
    return "violet" if l < 445 else "bleu" if l < 490 else "vert" if l < 570 else "jaune" if l < 590 else "orange" if l < 620 else "rouge"


def figure_spectre():
    """Les domaines du spectre (longueurs d'onde dans le vide), 300 → 0,5 ; 900 → 9,5 (1,5 unité pour 100 nm)."""
    X = lambda nm: round(0.5 + (nm - 300) * 0.015, 3)
    el = [{"f": "rect", "de": [X(300), 1.6], "a": [X(400), 2.4], "couleur": "violet", "remplir": "faible"},
          {"f": "rect", "de": [X(400), 1.6], "a": [X(800), 2.4], "couleur": "vert"},
          {"f": "rect", "de": [X(800), 1.6], "a": [X(900), 2.4], "couleur": "rouge", "remplir": "faible"},
          {"f": "texte", "at": [X(350), 2.75], "t": "ultraviolet", "couleur": "violet", "ancre": "centre", "taille": "petit"},
          {"f": "texte", "at": [X(600), 2.75], "t": "visible", "couleur": "vert", "ancre": "centre"},
          {"f": "texte", "at": [X(850), 2.75], "t": "infrarouge", "couleur": "rouge", "ancre": "centre", "taille": "petit"},
          {"f": "fleche", "de": [X(300), 0.7], "a": [X(900) + 0.3, 0.7], "couleur": "blanc"},
          {"f": "texte", "at": [X(900) + 0.2, 0.25], "t": "λ₀ (nm)", "couleur": "blanc", "ancre": "droite", "taille": "petit"}]
    for nm in (400, 500, 600, 700, 800):
        el.append({"f": "ligne", "pts": [[X(nm), 0.6], [X(nm), 0.8]], "couleur": "blanc"})
        el.append({"f": "texte", "at": [X(nm), 1.1], "t": str(nm), "couleur": "jaune" if nm in (400, 800) else "faible", "ancre": "centre", "taille": "petit"})
    el.append({"f": "texte", "at": [X(400), 3.35], "t": "violet", "couleur": "violet", "ancre": "centre", "taille": "petit"})
    el.append({"f": "texte", "at": [X(800), 3.35], "t": "rouge", "couleur": "rouge", "ancre": "centre", "taille": "petit"})
    return {"type": "schema", "titre": "Les domaines du spectre de la lumière", "cadre": {"l": 10, "h": 3.7},
            "legende": "Longueurs d'onde dans le vide : le visible va de 400 nm (violet) à 800 nm (rouge).", "elements": el}


def q_frequence(l0):
    nu = C / (l0 * 1e-9)
    lm = l0 * 1e-9
    att = f"ν = c/λ₀ = 3,00 × 10⁸/({sci(lm, 4)}) ≈ {sci(nu)} Hz"
    parole = (f"Question un. كنحولو lambda zéro en mètre: {entier(l0)} nanomètres، soit {sci_dit(lm, 4)} mètre. "
              f"nu égale c sur lambda zéro، soit trois fois dix puissance huit، sur {sci_dit(lm, 4)}. "
              f"nu égale environ {sci_dit(nu)} hertz.")
    return nu, {
        "reponse": valeur("ν", float(f"{nu:.3g}"), "Hz", att),
        "clavier": {"aides": ["ν = c/λ₀", "c = 3,00 × 10⁸ m/s", "1 nm = 10⁻⁹ m", "A.N. :", "Hz"],
                    "pieges": ["ν = λ₀/c", "ν = c·λ₀", "λ₀ en nm dans le calcul"]},
        "correction": correction([
            (f"1 : λ₀ = {l0} nm = {sci(lm, 4)} m", "lambda zéro en mètre"),
            (f"ν = c/λ₀ = 3,00 × 10⁸/({sci(lm, 4)})", "nu égale c sur lambda zéro"),
            (f"ν ≈ {sci(nu)} Hz", "nu égale environ")], parole)}


def q_visible(l0):
    coul = couleur(l0)
    if coul:
        att = (f"400 nm ≤ λ₀ = {l0} nm ≤ 800 nm : la radiation appartient au domaine visible ; dans l'ordre violet, bleu, "
               f"vert, jaune, orange, rouge, {l0} nm est dans le {coul} : sa couleur est le {coul}.")
        lignes = [(f"2 : 400 nm ≤ λ₀ = {l0} nm ≤ 800 nm", f"inférieur ou égal à {entier(l0)}"),
                  ("donc la radiation est visible", "إذن la radiation visible"),
                  (f"sa couleur : le {coul}", f"فle {coul}")]
        parole = (f"Question deux. quatre cents nanomètres, inférieur ou égal à {entier(l0)} nanomètres, inférieur ou égal à "
                  f"huit cents nanomètres. إذن la radiation visible. وفle spectre، {entier(l0)} nanomètres كاينة فle {coul}: "
                  f"اللون ديالها le {coul}.")
    else:
        dom = "infrarouge" if l0 > 800 else "ultraviolet"
        signe, borne = (">", "800") if l0 > 800 else ("<", "400")
        att = (f"λ₀ = {l0} nm {signe} {borne} nm : λ₀ est en dehors de l'intervalle [400 nm ; 800 nm], la radiation n'est pas "
               f"visible ; elle appartient à l'{dom} et n'a pas de couleur pour l'œil.")
        mot_b = "supérieur à huit cents" if l0 > 800 else "inférieur à quatre cents"
        lignes = [(f"2 : λ₀ = {l0} nm {signe} {borne} nm", mot_b),
                  ("donc la radiation n'est pas visible", "إذن la radiation ما كتبانش"),
                  (f"elle appartient à l'{dom} : pas de couleur", f"هي فl'{dom}")]
        parole = (f"Question deux. lambda zéro égale {entier(l0)} nanomètres، {mot_b} nanomètres. "
                  f"إذن la radiation ما كتبانش. هي فl'{dom}، وما عندهاش لون للعين.")
    return {"reponse": phrase(att),
            "clavier": {"aides": ["400 nm ≤ λ₀ ≤ 800 nm", "visible", "violet, bleu, vert, jaune, orange, rouge"],
                        "pieges": ["400 µm ≤ λ₀ ≤ 800 µm", "ultraviolet", "infrarouge"]},
            "correction": correction(lignes, parole)}


def q_vide():
    att = ("Le son est une onde mécanique : il a besoin d'un milieu matériel (l'air…) et ne se propage pas dans le vide. "
           "La lumière se propage dans le vide : c'est une onde électromagnétique, elle n'a pas besoin de milieu matériel.")
    parole = ("Question trois. le son onde mécanique: محتاج milieu matériel بحال الهوا، وما كيدوزش فle vide. "
              "الضو كيدوز فle vide، حيت هو onde électromagnétique، ماشي onde mécanique.")
    return {"reponse": phrase(att),
            "clavier": {"aides": ["onde mécanique", "onde électromagnétique", "milieu matériel", "le vide"],
                        "pieges": ["la lumière est une onde mécanique", "le son se propage dans le vide"]},
            "correction": correction([
                ("3 : le son est une onde mécanique : il ne se propage pas dans le vide", "le son onde mécanique"),
                ("la lumière, elle, se propage dans le vide", "الضو كيدوز فle vide"),
                ("donc la lumière est une onde électromagnétique", "onde électromagnétique، ماشي")], parole)}


L0 = 546                                      # raie verte du mercure (nm)
NU, Q1 = q_frequence(L0)
L0B = 1064                                    # semblable : laser infrarouge (nm)
_, Q1B = q_frequence(L0B)
NU_NM = C / L0                                # piège : λ₀ laissée en nm
NU_INV = (L0 * 1e-9) / C                      # piège : fraction inversée
LM = L0 * 1e-9

EX = {
  "id": "phys_ex_ch3_spectre_1", "type": "exercice", "version": 1, "status": "published",
  "matiere": "physique", "chapitre": "ondes_lumineuses", "cours": "phys_ch3_ondes_lumineuses",
  "titre": "La raie verte d'une lampe à mercure", "niveau": "facile", "duree_min": 12,
  "origine": "Exercice original écrit pour Moalim (ni sujet du national, ni copie d'un livre).",
  "competences": ["Calculer la fréquence ν = c/λ₀ d'une radiation", "Dire si une radiation est visible (400 nm ≤ λ₀ ≤ 800 nm) et donner sa couleur",
                   "Savoir que la lumière, onde électromagnétique, se propage dans le vide"],
  "enonce": {
    "intro": f"Une lampe à vapeur de mercure, munie d'un filtre, émet une lumière monochromatique : une seule radiation, de longueur d'onde dans le vide λ₀ = {L0} nm. Le document rappelle les domaines du spectre de la lumière.",
    "intro_dit": f"دابا نقراو l'énoncé. واحد la lampe à vapeur de mercure، مع واحد le filtre، كتعطي une lumière monochromatique: radiation وحدة. la longueur d'onde ديالها dans le vide: lambda zéro égale {entier(L0)} nanomètres. والوثيقة كتفكرنا ب les domaines ديال le spectre.",
    "figures": [figure_spectre()],
    "donnees": [f"λ₀ = {L0} nm (longueur d'onde dans le vide)", "c = 3,00 × 10⁸ m/s (célérité de la lumière dans le vide)", "1 nm = 10⁻⁹ m"],
    "questions": [
      {"id": "1", "texte": "Calculer la fréquence ν de cette radiation.",
       "texte_dit": "Question un: حسب la fréquence nu ديال هاد la radiation.", **Q1,
       "aides": [aide("La fréquence se calcule avec c et λ₀. Mais avant le calcul : dans quelle unité doit être λ₀ ?",
                      "عندك c وعندك lambda zéro. ولكن قبل الحساب، lambda zéro خاصها تكون بأي وحدة؟"),
                 aide(f"ν = c/λ₀, avec λ₀ en mètre : {L0} nm = {sci(LM, 4)} m.",
                      f"nu égale c sur lambda zéro، و lambda zéro en mètre: {entier(L0)} nanomètres، soit {sci_dit(LM, 4)} mètre.")],
       "explication": "ex_s1", "facile": "fa_s1"},
      {"id": "2", "texte": "Cette radiation est-elle visible ? Justifier, puis donner sa couleur.",
       "texte_dit": "Question deux: واش هاد la radiation كتبان؟ علل، ومن بعد عطي اللون ديالها.", **q_visible(L0),
       "aides": [aide("Compare λ₀ aux deux bornes du visible écrites sur le document.",
                      "قارن lambda zéro مع les deux bornes ديال le visible اللي فالوثيقة."),
                 aide("Visible si 400 nm ≤ λ₀ ≤ 800 nm. Les couleurs vont du violet (400 nm) au rouge (800 nm) : violet, bleu, vert, jaune, orange, rouge.",
                      "la radiation visible يلا كانت lambda zéro supérieure ou égale à quatre cents nanomètres، et inférieure ou égale à huit cents nanomètres. واللون كيمشي من le violet حتى le rouge: violet، bleu، vert، jaune، orange، rouge.")],
       "explication": "ex_s2", "facile": "fa_s2"},
      {"id": "3", "texte": "Sur la Lune, il n'y a pas d'air : c'est le vide. Un astronaute voit la lampe allumée de son camarade, mais il n'entend pas le choc quand ce camarade frappe une roche avec un marteau. Expliquer cette observation, puis préciser la nature de l'onde lumineuse.",
       "texte_dit": "Question trois: فوق la Lune ما كاينش الهوا: كاين le vide. واحد l'astronaute كيشوف الضو ديال la lampe ديال صاحبو، ولكن ما كيسمعش الصوت ملي صاحبو كيضرب الحجرة بالمطرقة. فسر علاش، ومن بعد عطي la nature ديال l'onde lumineuse.",
       **q_vide(),
       "aides": [aide("Le son et la lumière traversent-ils tous les deux le vide ? Pense à la lumière du Soleil qui arrive sur la Terre.",
                      "واش الصوت والضو بجوج كيدوزو فle vide؟ تفكر الضو ديال الشمس اللي كيوصل للأرض."),
                 aide("Une onde mécanique a besoin d'un milieu matériel ; une onde électromagnétique se propage aussi dans le vide.",
                      "une onde mécanique محتاجة milieu matériel. و une onde électromagnétique كتمشي حتى فle vide.")],
       "explication": "ex_s3", "facile": "fa_s3"},
    ]},
  "explication": {"activities": [{"id": "explication", "title": "Explication animée", "slides": [
    diapo_sim("ex_s1", "Question 1 : la fréquence ν = c/λ₀", "λ₀ en mètre, puis ν = c/λ₀.",
      f"{SIM}spectre.html?lambda_nm={L0}", "Le curseur sur λ₀ : la simulation écrit λ₀ en m et ν",
      f"هادا هو le spectre، de trois cents à neuf cents nanomètres. دابا le curseur كيمشي ل la valeur ديال التمرين: lambda zéro égale {entier(L0)} nanomètres. "
      f"تحت، la simulation كتكتبها en mètre: {sci_dit(LM, 4)} mètre، حيت le nanomètre égale dix puissance moins neuf mètre. "
      f"ومن بعد la fréquence: nu égale c sur lambda zéro. nu égale trois fois dix puissance huit، sur {sci_dit(LM, 4)}. "
      f"nu égale environ {sci_dit(NU)} hertz.",
      [("ν = c/λ₀", "nu égale c sur lambda zéro"), (f"ν = 3,00 × 10⁸/({sci(LM, 4)}) ≈ {sci(NU)} Hz", "nu égale environ")],
      [dict(mot="هادا هو le spectre", commande="play_until", parametres={"moment": "bande_peinte"}),
       dict(mot="دابا le curseur كيمشي", commande="play_until", parametres={"moment": "valeur"}),
       dict(mot="تحت، la simulation", repere="valeur_m"),
       dict(mot="ومن بعد la fréquence", repere="frequence"),
       dict(mot="nu égale c sur lambda zéro", cible="centre:0"),
       dict(mot="nu égale environ", cible="centre:1")]),
    diapo_sim("ex_s2", "Question 2 : visible ou non, et quelle couleur ?", "Visible si 400 nm ≤ λ₀ ≤ 800 nm.",
      f"{SIM}spectre.html?lambda_nm={L0}", "Les bornes du visible, puis λ₀ et sa couleur",
      f"le curseur كيدوز على le spectre. la borne violette، quatre cents nanomètres. la borne rouge، huit cents nanomètres. "
      f"بيناتهم، le visible: العين كتشوف. قبل la borne violette، l'ultraviolet. ومن بعد la borne rouge، l'infrarouge: العين ما كتشوفش. "
      f"دابا le curseur كيرجع ل lambda zéro égale {entier(L0)} nanomètres: هي بين les deux bornes، إذن la radiation visible. "
      f"واللون اللي كتكتب la simulation: {couleur(L0)}.",
      [(f"400 nm ≤ {L0} nm ≤ 800 nm : visible", "هي بين les deux bornes"), (f"couleur : {couleur(L0)}", "واللون اللي كتكتب")],
      [dict(mot="le curseur كيدوز", commande="play_until", parametres={"moment": "violet_400"}),
       dict(mot="la borne violette، quatre", repere="borne_400"),
       dict(mot="la borne rouge، huit", commande="play_until", parametres={"moment": "rouge_800"}),
       dict(mot="بيناتهم، le visible", repere="visible"),
       dict(mot="دابا le curseur كيرجع", commande="play_until", parametres={"moment": "valeur"}),
       dict(mot="هي بين les deux bornes", cible="centre:0"),
       dict(mot="واللون اللي كتكتب", repere="couleur"),
       dict(mot="la simulation: ", cible="centre:1")]),
    diapo_sim("ex_s3", "Question 3 : la lumière traverse le vide, le son non", "Le son : onde mécanique. La lumière : onde électromagnétique.",
      f"{SIM}figures.html?fig=fig_soleil_vide", "La lumière du Soleil traverse le vide ; la sonnette sous la cloche vide",
      "فهاد la figure، الضو ديال الشمس كيدوز le vide، وكيوصل للأرض. ومن جهة أخرى، واحد la sonnette تحت واحد الكاس، حيدنا منو الهوا: "
      "كنشوفوها، ولكن ما كنسمعوهاش. الصوت onde mécanique: محتاج milieu matériel. والضو onde électromagnétique: كيدوز فle vide. "
      "فالتمرين، فوق la Lune نفس الشي: l'astronaute كيشوف الضو، ولكن الصوت ما كيوصلش ليه.",
      [("son : onde mécanique, pas de propagation dans le vide", "الصوت onde mécanique"),
       ("lumière : onde électromagnétique, elle traverse le vide", "والضو onde électromagnétique")],
      [dict(mot="الضو ديال الشمس كيدوز", commande="play_until", parametres={"moment": "lumiere"}),
       dict(mot="واحد la sonnette", commande="play_until", parametres={"moment": "son"}),
       dict(mot="الصوت onde mécanique", commande="play_until", parametres={"moment": "conclusion"}),
       dict(mot="الصوت onde mécanique", cible="centre:0"),
       dict(mot="والضو onde électromagnétique", cible="centre:1")]),
  ]}]},
  "facile": {"activities": [{"id": "facile", "title": "Plus facile, pour s'entraîner", "slides": [
    qcm_facile("fa_s1", "Plus facile : le bon calcul de ν", "سؤال ساهل: اختار le bon calcul.",
      f"λ₀ = {L0} nm. Quel calcul donne la fréquence ν ?",
      [f"ν = 3,00 × 10⁸/{L0} ≈ {sci(NU_NM)} Hz", f"ν = 3,00 × 10⁸/({sci(LM, 4)}) ≈ {sci(NU)} Hz", f"ν = {sci(LM, 4)}/(3,00 × 10⁸) ≈ {sci(NU_INV)} Hz"], 1, {
        "1": {"juste": rep(f"برافو! lambda zéro en mètre، و nu égale c sur lambda zéro. nu égale environ {sci_dit(NU)} hertz.",
                           f"Juste : ν = c/λ₀ avec λ₀ en m : ν ≈ {sci(NU)} Hz.")},
        "0": {"1": rep("ما تقلقش. la relation صحيحة، ولكن شوف lambda zéro: خليتيها en nanomètre. فالحساب خاصها en mètre. عاود اختار.",
                       "La relation est bonne, mais λ₀ est restée en nm : elle doit être en m. Réessaie."),
              "2": rep(f"الجواب: lambda zéro égale {sci_dit(LM, 4)} mètre. إذن nu égale environ {sci_dit(NU)} hertz.",
                       f"Réponse : {L0} nm = {sci(LM, 4)} m, donc ν ≈ {sci(NU)} Hz.")},
        "2": {"1": rep("قريب! ولكن قلبتي la relation: nu égale c sur lambda zéro، ماشي lambda zéro sur c. عاود اختار.",
                       "La fraction est inversée : ν = c/λ₀, pas λ₀/c. Réessaie."),
              "2": rep(f"الجواب: nu égale c sur lambda zéro، soit environ {sci_dit(NU)} hertz. la fréquence ديال الضو كبيرة بزاف.",
                       f"Réponse : ν = c/λ₀ ≈ {sci(NU)} Hz (de l'ordre de 10¹⁴ Hz pour le visible).")}},
      f"lambda zéro égale {entier(L0)} nanomètres. Quel calcul donne la fréquence nu ?"),
    vf_facile("fa_s2", "Plus facile : vrai ou faux", "سؤال ساهل: قول واش كل جملة صحيحة ولا غالطة.",
      f"λ₀ = {L0} nm ; le visible va de 400 nm à 800 nm.", [
        (f"λ₀ = {L0} nm est comprise entre 400 nm et 800 nm : la radiation est visible.", True,
         f"400 nm ≤ {L0} nm ≤ 800 nm : elle est dans le domaine visible."),
        (f"Une radiation de {L0} nm appartient à l'infrarouge.", False,
         "L'infrarouge commence après 800 nm ; 546 nm est dans le visible."),
        (f"{L0} nm est entre le bleu et le jaune : la radiation est verte.", True,
         "Dans l'ordre violet, bleu, vert, jaune, orange, rouge, 546 nm tombe dans le vert.")]),
    assoc_facile("fa_s3", "Plus facile : associer", "سؤال ساهل: ربط كل onde مع la nature ديالها.",
      "Relie chaque onde à sa nature.", "Relie chaque onde à ce qui la caractérise.",
      [("1", "La lumière du Soleil"), ("2", "Le son d'une sonnette"), ("3", "Une perturbation le long d'une corde")],
      [("a", "Onde électromagnétique : elle traverse le vide"), ("b", "Onde mécanique : elle a besoin de l'air (ou d'un autre milieu matériel)"),
       ("c", "Onde mécanique : elle a besoin de la corde")],
      {"1": "a", "2": "b", "3": "c"},
      {"1-a": (True, "Oui : la lumière du Soleil traverse le vide : onde électromagnétique.", "برافو: الضو ديال الشمس كيدوز le vide: onde électromagnétique."),
       "1-b": (False, "La lumière n'a pas besoin d'air : elle traverse le vide entre le Soleil et la Terre.", "لا، الضو ما محتاجش الهوا: كيدوز le vide بين الشمس والأرض. قلب على la nature ديالو."),
       "1-c": (False, "La lumière n'est pas une onde mécanique et n'a pas besoin de corde.", "لا، الضو ماشي onde mécanique، وما محتاجش la corde."),
       "2-a": (False, "Le son ne traverse pas le vide : pense à la sonnette sous la cloche vide.", "لا، الصوت ما كيدوزش فle vide: تفكر la sonnette تحت الكاس."),
       "2-b": (True, "Oui : le son est une onde mécanique, il a besoin d'un milieu matériel.", "برافو: الصوت onde mécanique، محتاج الهوا ولا milieu matériel آخر."),
       "2-c": (False, "Le son est bien mécanique, mais il se propage dans l'air, pas dans une corde.", "الصوت onde mécanique، صحيح، ولكن ما محتاجش la corde: كيمشي فالهوا."),
       "3-a": (False, "La perturbation d'une corde est une onde mécanique, pas électromagnétique.", "لا، la perturbation فla corde ماشي onde électromagnétique: هي onde mécanique."),
       "3-b": (False, "Onde mécanique, oui, mais elle se propage le long de la corde, pas dans l'air.", "onde mécanique، صحيح، ولكن هاد la perturbation كتمشي فla corde، ماشي فالهوا."),
       "3-c": (True, "Oui : la perturbation se propage le long de la corde : onde mécanique.", "برافو: la perturbation كتمشي فla corde: onde mécanique، محتاجة la corde.")},
      ("(1 ; a) (2 ; b) (3 ; c) : seule la lumière se propage dans le vide.",
       "غير الضو اللي كيدوز فle vide: onde électromagnétique. الصوت و la perturbation فla corde: ondes mécaniques.")),
  ]}]},
  "similaire": {
    "id": "phys_ex_ch3_spectre_1_b", "titre": "Même exercice, autres données",
    "enonce": {
      "intro": f"Un laser utilisé dans l'industrie émet une lumière monochromatique de longueur d'onde dans le vide λ₀ = {L0B} nm. Le document rappelle les domaines du spectre de la lumière.",
      "intro_dit": f"نفس التمرين، بقيم أخرى. واحد le laser ديال l'industrie كيعطي une lumière monochromatique. la longueur d'onde ديالها dans le vide: lambda zéro égale {entier(L0B)} nanomètres.",
      "figures": [figure_spectre()],
      "donnees": [f"λ₀ = {L0B} nm", "c = 3,00 × 10⁸ m/s", "1 nm = 10⁻⁹ m"],
      "questions": [
        {"id": "1", "texte": "Calculer la fréquence ν de cette radiation.", **Q1B},
        {"id": "2", "texte": "Cette radiation est-elle visible ? Justifier, puis donner sa couleur si elle en a une.", **q_visible(L0B)},
        {"id": "3", "texte": "Entre la Terre et la Lune, c'est le vide. Un faisceau laser envoyé depuis la Terre atteint la Lune, alors que le bruit d'une explosion sur la Terre ne l'atteint jamais. Expliquer, puis préciser la nature de l'onde lumineuse.", **q_vide()},
      ]}},
}
controle_voix(EX)
ecrire(EX)
