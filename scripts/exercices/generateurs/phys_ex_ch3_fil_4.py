# Exercice de physique, ch. 3 (propagation d'une onde lumineuse), niveau moyen : le diamètre d'un cheveu par diffraction.
# Sources comparées (skill exercices § 2) :
#  - exploration ondes_lumineuses.json : cas_types « fil_cheveu » (d = 2λD/L, même laser donc même λ), « variation »
#    (L proportionnelle à λ, conclure par une inégalité), « rapport » (λ₂/λ₁ = L₂/L₁) ; pieges « pour un fil, remplace D
#    par d », « prend L entière comme côté opposé », « croit que λ change quand on change le fil » ; erreurs_examen
#    « établir L sans les étapes », « longueurs laissées en mm/cm » ; vidéos Driss DOTCOM (fil, cheveu), Boujaada
#    (piège d et D), Ghaloumi (deuxième expérience par le rapport) ; erreur d'un prof : « tan θ = θ » écrit au tableau.
#  - nationaux comparés : 2017 R (fil d = 0,1 mm donné, D = 3,5 m, L = 56 mm → λ, puis source violette : comment varie
#    L), 2021 N (cheveu après une courbe L = f(D)), 2023 R (fente, a à trouver, puis radiation rouge). Ici la chaîne est
#    inverse de 2017 R (λ connue, d cherché), avec θ calculé d'abord, la direction de la figure à justifier et un
#    laser vert dont L₂ se déduit par le rapport : situation, données et chaîne différentes de tout national.
#  - séries en ligne : recherche web (talamidi séries 1 et 2, moutamadris « fils calibrés 60 et 80 µm », série
#    Google Docs laser 632 nm) : seuls les titres et extraits des résultats ont été lus, les sites eux-mêmes sont
#    bloqués par le réseau de la session (talamidi.com, moutamadris.ma non résolus).
import sys, os, math, importlib.util
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _outils import *
from _outils import _RACINE

_sp = importlib.util.spec_from_file_location("tp", _RACINE / "backend" / "kaggle_tts" / "texte_parle.py")
tp = importlib.util.module_from_spec(_sp); _sp.loader.exec_module(tp)


def mots(s):
    """« 3,7 » -> « trois virgule sept » (nombre déjà écrit avec fr())."""
    s = str(s).replace("−", "-").replace(" ", "")
    neg = s.startswith("-"); s = s.lstrip("-")
    if "," in s:
        e, d = s.split(","); r = d.lstrip("0"); z = len(d) - len(r)
        w = tp.nombre_fr(int(e)) + " virgule" + " zéro" * z + (" " + tp.nombre_fr(int(r)) if r else "")
    else:
        w = tp.nombre_fr(int(s))
    return ("moins " if neg else "") + w


def msci(x, ch=3):
    """3,7e-2 -> « trois virgule sept fois dix puissance moins deux »."""
    e = math.floor(math.log10(abs(x))); m = round(x / 10 ** e, ch - 1)
    if abs(m) >= 10: m /= 10; e += 1
    t = mots(fr(m, ch - 1))
    return t if e == 0 else f"{t} fois dix puissance {mots(str(e))}"


SIM = "/media/simulations/physics/ondes-lumineuses-tableau/"


def montage(lam_nm, D, L_cm, vertical=True):
    """Schéma du montage (vue de dessus) et de l'écran vu de face ; fil vertical → taches sur une ligne horizontale."""
    el = [
        {"f": "rect", "de": [0.2, 3.55], "a": [1.5, 4.05], "couleur": "blanc", "remplir": "faible"},
        {"f": "texte", "at": [0.85, 4.35], "t": f"laser λ = {lam_nm} nm", "couleur": "rouge", "ancre": "centre", "taille": "petit"},
        {"f": "ligne", "pts": [[1.5, 3.8], [3.6, 3.8]], "couleur": "rouge", "epais": True},
        {"f": "ligne", "pts": [[3.6, 3.3], [3.6, 4.3]], "couleur": "jaune", "epais": True},
        {"f": "texte", "at": [3.6, 4.6], "t": "cheveu (d)" if vertical else "cheveu horizontal (d)", "couleur": "jaune", "ancre": "centre", "taille": "petit"},
        {"f": "ligne", "pts": [[3.6, 3.8], [9.2, 4.45]], "couleur": "rouge", "trait": "pointille"},
        {"f": "ligne", "pts": [[3.6, 3.8], [9.2, 3.15]], "couleur": "rouge", "trait": "pointille"},
        {"f": "ligne", "pts": [[3.6, 3.8], [9.2, 3.8]], "couleur": "faible", "trait": "pointille"},
        {"f": "ligne", "pts": [[9.2, 2.7], [9.2, 4.9]], "couleur": "blanc", "epais": True},
        {"f": "texte", "at": [9.55, 4.95], "t": "écran", "couleur": "blanc", "ancre": "centre", "taille": "petit"},
        {"f": "cote", "de": [3.6, 2.55], "a": [9.2, 2.55], "t": f"D = {fr(D, 2)} m", "couleur": "cyan", "pos": "s"},
        {"f": "texte", "at": [5.0, 1.95], "t": "Écran vu de face", "couleur": "cyan", "ancre": "centre", "taille": "petit"},
        {"f": "rect", "de": [2.0, 0.1], "a": [8.0, 1.75], "couleur": "blanc"},
    ]
    if vertical:
        el += [
            {"f": "ellipse", "c": [5.0, 0.9], "rx": 0.9, "ry": 0.32, "couleur": "rouge", "remplir": "rouge"},
            {"f": "ellipse", "c": [3.65, 0.9], "rx": 0.38, "ry": 0.22, "couleur": "rouge", "trait": "pointille"},
            {"f": "ellipse", "c": [6.35, 0.9], "rx": 0.38, "ry": 0.22, "couleur": "rouge", "trait": "pointille"},
            {"f": "ellipse", "c": [2.75, 0.9], "rx": 0.3, "ry": 0.18, "couleur": "faible", "trait": "pointille"},
            {"f": "ellipse", "c": [7.25, 0.9], "rx": 0.3, "ry": 0.18, "couleur": "faible", "trait": "pointille"},
            {"f": "cote", "de": [4.1, 1.45], "a": [5.9, 1.45], "t": f"L = {fr(L_cm, 2)} cm", "couleur": "jaune", "pos": "n"},
        ]
    else:
        el += [
            {"f": "ellipse", "c": [5.0, 0.92], "rx": 0.3, "ry": 0.62, "couleur": "rouge", "remplir": "rouge"},
            {"f": "ellipse", "c": [5.0, 0.12], "rx": 0.2, "ry": 0.12, "couleur": "faible", "trait": "pointille"},
            {"f": "ellipse", "c": [5.0, 1.68], "rx": 0.2, "ry": 0.12, "couleur": "faible", "trait": "pointille"},
            {"f": "cote", "de": [5.8, 0.3], "a": [5.8, 1.54], "t": f"L = {fr(L_cm, 2)} cm", "couleur": "jaune", "pos": "e"},
        ]
    return {"type": "schema", "titre": "Montage (vue de dessus, angle exagéré) et écran vu de face", "cadre": {"l": 10, "h": 5.2},
            "legende": "Le schéma n'est pas à l'échelle : l'angle est exagéré pour être visible.", "elements": el}


# ---------------------------------------------------------------- données et calculs
C = 3.00e8
LAM1_NM, D, L1_CM, LAM2_NM = 650, 2.00, 3.7, 520
LAM1, L1 = LAM1_NM * 1e-9, L1_CM * 1e-2
TH1 = L1 / (2 * D)                       # 9,25e-3 rad
DD = 2 * LAM1 * D / L1                   # 7,03e-5 m
DD_UM = DD * 1e6                         # 70,3 µm
L2_CM = L1_CM * LAM2_NM / LAM1_NM        # 2,96 cm
LV_CM = L1_CM * 400 / LAM1_NM            # 2,28 cm (violet, version facile)

s_th1, s_d, s_dum, s_l2 = sci(TH1), sci(DD), fr(DD_UM, 1), fr(L2_CM, 2)

EX = {
  "id": "phys_ex_ch3_fil_4", "type": "exercice", "version": 1, "status": "published",
  "matiere": "physique", "chapitre": "ondes_lumineuses", "cours": "phys_ch3_ondes_lumineuses",
  "titre": "Mesurer le diamètre d'un cheveu par diffraction", "niveau": "moyen", "duree_min": 25,
  "origine": "Exercice original écrit pour Moalim (ni sujet du national, ni copie d'un livre).",
  "competences": ["Reconnaître la diffraction et la direction de la figure", "Calculer θ = L/(2D) (θ petit, en radian)",
                  "Établir et utiliser d = 2λD/L pour un fil", "Comparer deux largeurs : L proportionnelle à λ"],
  "enonce": {
    "intro": (f"Pour mesurer le diamètre d d'un cheveu, Salma le tend verticalement devant un laser rouge de longueur d'onde "
              f"λ₁ = {LAM1_NM} nm. Sur un écran placé à la distance D = {fr(D, 2)} m du cheveu, elle observe des taches lumineuses "
              f"séparées par des taches sombres. Elle mesure la largeur de la tache centrale : L₁ = {fr(L1_CM, 2)} cm. "
              "On suppose l'écart angulaire θ petit : tan θ ≈ θ, avec θ en radian."),
    "intro_dit": (f"نقراو l'énoncé. سلمى بغات تعرف le diamètre d ديال واحد الشعرة. كتمدها بالطول، قدام واحد le laser حمر، "
                  f"la longueur d'onde ديالو lambda un égale {mots(LAM1_NM)} nanomètres. فوق l'écran، اللي بعيد على الشعرة ب D égale "
                  f"{mots(fr(D, 2))} mètres، كتشوف des taches ضاويين، وبيناتهم des taches كحلين. كتقيس la largeur ديال la tache centrale: "
                  f"L un égale {mots(fr(L1_CM, 2))} centimètres. teta صغيرة، إذن tangente teta تقريبا teta، و teta en radian."),
    "figures": [montage(LAM1_NM, D, L1_CM, True)],
    "donnees": [f"λ₁ = {LAM1_NM} nm (laser rouge)", f"D = {fr(D, 2)} m (distance cheveu – écran)",
                f"L₁ = {fr(L1_CM, 2)} cm (largeur de la tache centrale)", f"λ₂ = {LAM2_NM} nm (laser vert, question 4)",
                "θ petit : tan θ ≈ θ (θ en radian)"],
    "questions": [
      {"id": "1", "texte": "Nommer le phénomène observé, puis justifier la direction dans laquelle les taches sont alignées sur l'écran.",
       "texte_dit": "السؤال un: سمي le phénomène اللي كنشوفو، ومن بعد justifier: علاش les taches جاو على هاد الخط فوق l'écran؟",
       "reponse": phrase("C'est la diffraction de la lumière. Le cheveu est vertical ; la lumière s'étale perpendiculairement au cheveu : "
                         "les taches sont donc alignées sur une ligne horizontale (une tache centrale large et lumineuse, des taches "
                         "secondaires plus petites, séparées par des extinctions)."),
       "clavier": {"aides": ["diffraction", "perpendiculairement au cheveu", "ligne horizontale"],
                   "pieges": ["dispersion", "réfraction", "parallèlement au cheveu"]},
       "aides": [aide("Comparez la direction du cheveu et la direction de la ligne des taches sur la figure.",
                      "شوف la figure: الشعرة ممدودة كيفاش؟ و les taches جاو على أنهي خط؟ قارن بيناتهم."),
                 aide("Derrière une fente ou un fil, la lumière s'étale perpendiculairement à l'objet qui la diffracte.",
                      "من بعد la fente ولا le fil، الضو كيتفرق perpendiculairement، يعني عمودي على الشي اللي فرقو.")],
       "correction": correction([("1 : le phénomène est la diffraction de la lumière", "le phénomène هو la diffraction"),
                                 ("La lumière s'étale perpendiculairement au cheveu.", "perpendiculairement au cheveu"),
                                 ("Cheveu vertical → taches alignées sur une ligne horizontale.", "على خط أفقي")],
                                "السؤال un. le phénomène هو la diffraction de la lumière. الضو كيتفرق perpendiculairement au cheveu. "
                                "الشعرة عمودية، إذن les taches كيجيو على خط أفقي."),
       "explication": "ex_f1", "facile": "fa_f1"},
      {"id": "2", "texte": "Calculer l'écart angulaire θ₁ à partir des mesures de Salma.",
       "texte_dit": "السؤال deux: حسب l'écart angulaire teta un، من القياسات ديال سلمى.",
       "reponse": valeur("θ₁", round(TH1, 6), "rad",
                         f"θ₁ = L₁/(2D) = {sci(L1, 2)}/(2 × {fr(D, 2)}) ≈ {s_th1} rad"),
       "clavier": {"aides": ["tan θ = L/(2D)", "tan θ ≈ θ", "rad", "A.N. : θ₁ = 3,7×10⁻²/(2 × 2)"],
                   "pieges": ["θ = L/D", "θ = 2D/L", "°"]},
       "aides": [aide("Dans le triangle, le côté opposé à θ est la moitié de la tache, L₁/2 ; le côté adjacent est D.",
                      "فle triangle، الضلع المقابل ل teta هو نص la tache، L un sur deux. والضلع المجاور هو D."),
                 aide("tan θ₁ = (L₁/2)/D = L₁/(2D), et θ petit donc θ₁ ≈ tan θ₁. Mettre L₁ en mètre.",
                      "tangente teta un égale L un sur deux D. teta صغيرة، إذن teta un تقريبا tangente teta un. رد البال: L un en mètre.")],
       "correction": correction([("2 : tan θ₁ = (L₁/2)/D = L₁/(2D)", "tangente teta un égale L un sur deux D"),
                                 ("θ petit : θ₁ ≈ tan θ₁ = L₁/(2D)", "teta صغيرة"),
                                 (f"θ₁ = {sci(L1, 2)}/(2 × {fr(D, 2)})", "l'application numérique"),
                                 (f"θ₁ ≈ {s_th1} rad", f"teta un égale {msci(TH1)} radian")],
                                f"السؤال deux. d'après la figure، tangente teta un égale L un sur deux D. teta صغيرة، إذن teta un تقريبا tangente teta un. "
                                f"l'application numérique: {msci(L1, 2)} mètre، sur deux fois {mots(fr(D, 2))}. teta un égale {msci(TH1)} radian."),
       "explication": "ex_f2", "facile": "fa_f2"},
      {"id": "3", "texte": "Montrer que le diamètre du cheveu s'écrit d = 2λ₁D/L₁, puis calculer d en micromètre (µm).",
       "texte_dit": "السؤال trois: montrer que le diamètre d égale deux lambda un D sur L un، ومن بعد حسب d en micro mètre.",
       "reponse": valeur("d", round(DD_UM, 2), "µm",
                         f"d = 2λ₁D/L₁ = (2 × {LAM1_NM}×10⁻⁹ × {fr(D, 2)})/({sci(L1, 2)}) ≈ {s_d} m = {s_dum} µm"),
       "clavier": {"aides": ["θ = λ/d", "θ = L/(2D)", "d = 2λD/L", "1 µm = 10⁻⁶ m", "A.N. : d = (2 × 650×10⁻⁹ × 2)/(3,7×10⁻²)"],
                   "pieges": ["D = 2λd/L", "d = λL/(2D)", "nm"]},
       "aides": [aide("Le cheveu donne la même figure qu'une fente de largeur d : dans θ = λ/a, d prend la place de a (pas de D).",
                      "الشعرة كتعطي نفس la figure ديال fente عندها la largeur d. إذن فteta égale lambda sur a، d كتاخد البلاصة ديال a، ماشي ديال D."),
                 aide("Égaler θ₁ = λ₁/d et θ₁ = L₁/(2D), puis isoler d ; tout en mètre, puis 1 µm = 10⁻⁶ m.",
                      "كتب teta un égale lambda un sur d، و teta un égale L un sur deux D. ساوي بيناتهم، وخرج d. كلشي en mètre، et un micro mètre égale dix puissance moins six mètre.")],
       "correction": correction([("3 : θ₁ = λ₁/d (le cheveu remplace la fente)", "teta un égale lambda un sur d"),
                                 ("et θ₁ = L₁/(2D), donc λ₁/d = L₁/(2D)", "donc lambda un sur d égale L un sur deux D"),
                                 ("d = 2λ₁D/L₁", "d égale deux lambda un D sur L un"),
                                 (f"d = (2 × {LAM1_NM}×10⁻⁹ × {fr(D, 2)})/({sci(L1, 2)})", "l'application numérique"),
                                 (f"d ≈ {s_d} m = {s_dum} µm", f"d égale {mots(s_dum)} micro mètre")],
                                f"السؤال trois. الشعرة كتاخد البلاصة ديال la fente، إذن teta un égale lambda un sur d. ومن la figure، teta un égale L un sur deux D. "
                                f"donc lambda un sur d égale L un sur deux D، و d égale deux lambda un D sur L un. l'application numérique: deux fois "
                                f"{mots(LAM1_NM)} fois dix puissance moins neuf، fois {mots(fr(D, 2))}، sur {msci(L1, 2)}. "
                                f"d égale {msci(DD)} mètre، يعني d égale {mots(s_dum)} micro mètre."),
       "explication": "ex_f3", "facile": "fa_f3"},
      {"id": "4", "texte": (f"Salma remplace le laser rouge par un laser vert (λ₂ = {LAM2_NM} nm), sans toucher au cheveu ni à l'écran. "
                            "Comment varie la largeur de la tache centrale ? Justifier, puis calculer la nouvelle largeur L₂."),
       "texte_dit": (f"السؤال quatre: سلمى كتبدل le laser الحمر بواحد le laser خضر، lambda deux égale {mots(LAM2_NM)} nanomètres، "
                     "بلا ما تقيس الشعرة ولا l'écran. كيفاش كتبدل la largeur ديال la tache centrale؟ justifier، ومن بعد حسب L deux."),
       "reponse": valeur("L₂", round(L2_CM, 3), "cm",
                         f"L₂/L₁ = λ₂/λ₁ donc L₂ = L₁·λ₂/λ₁ = {fr(L1_CM, 2)} × {LAM2_NM}/{LAM1_NM} ≈ {s_l2} cm"),
       "clavier": {"aides": ["L = 2λD/d", "L₂/L₁ = λ₂/λ₁", "cm", f"A.N. : L₂ = 3,7 × {LAM2_NM}/{LAM1_NM}"],
                   "pieges": ["L₂ = L₁·λ₁/λ₂", "L augmente"]},
       "aides": [aide("Qu'est-ce qui a changé entre les deux expériences : λ, D ou d ? Regardez où λ se trouve dans L = 2λD/d.",
                      "شنو اللي تبدل بين les deux expériences: lambda، D ولا d؟ شوف فين كاينة lambda فL égale deux lambda D sur d."),
                 aide("Écrire L₁ = 2λ₁D/d et L₂ = 2λ₂D/d, puis diviser : L₂/L₁ = λ₂/λ₁.",
                      "كتب L un égale deux lambda un D sur d، و L deux égale deux lambda deux D sur d. قسم وحدة على الأخرى: L deux sur L un égale lambda deux sur lambda un.")],
       "correction": correction([("4 : L = 2λD/d : D et d n'ont pas changé, L est proportionnelle à λ", "L proportionnelle à lambda"),
                                 (f"λ₂ < λ₁ donc L₂ < L₁ : la tache centrale se rétrécit", "la tache centrale كتصغار"),
                                 ("L₂/L₁ = λ₂/λ₁, donc L₂ = L₁·λ₂/λ₁", "L deux sur L un égale lambda deux sur lambda un"),
                                 (f"L₂ = {fr(L1_CM, 2)} × {LAM2_NM}/{LAM1_NM} ≈ {s_l2} cm", f"L deux égale {mots(s_l2)} centimètres")],
                                "السؤال quatre. L égale deux lambda D sur d، و D و d ما تبدلوش: إذن L proportionnelle à lambda. "
                                "lambda deux صغر من lambda un، إذن la tache centrale كتصغار. L deux sur L un égale lambda deux sur lambda un. "
                                f"إذن L deux égale {mots(fr(L1_CM, 2))} fois {mots(LAM2_NM)} sur {mots(LAM1_NM)}. L deux égale {mots(s_l2)} centimètres."),
       "explication": "ex_f4", "facile": "fa_f4"},
    ]
  },
}

# ---------------------------------------------------------------- explication animée (simulations du cours)
d_sim, L_sim = 0.07, 2 * LAM1 * 2.0 / 0.07e-3 * 100          # fil 0,07 mm, λ 650 nm, D 2 m → L = 3,71 cm (affiché par diffraction.html)
m1 = ("شوف la simulation: le laser كيضوي على واحد le fil رقيق، بحال الشعرة. le fil ممدود عموديا. شوف l'écran: الضو ما بقاش نقطة، تفرق. "
      "هادي هي la diffraction. les taches جاو على خط أفقي. علاش؟ الضو كيتفرق perpendiculairement au fil. le fil عمودي، إذن les taches على خط أفقي. "
      "فالوسط la tache centrale كبيرة وضاوية، وفالجناب des taches صغار، وبيناتهم des extinctions.")
m2 = ("هادا le montage من الفوق. le rayon اللي كيمشي للوسط ديال la tache، و le rayon اللي كيمشي للحاشية ديالها. الزاوية بيناتهم هي l'écart angulaire teta. "
      "كنشوفو le triangle: الضلع المقابل هو L sur deux، والضلع المجاور هو D. إذن tangente teta égale L sur deux D. teta صغيرة en radian، إذن tangente teta تقريبا teta. "
      "فla simulation، L égale deux virgule six centimètres، و D égale deux mètres: teta égale six virgule cinq fois dix puissance moins trois radian. "
      f"فالتمرين، L un égale {mots(fr(L1_CM, 2))} centimètres. إذن teta un égale {msci(L1, 2)}، sur deux fois {mots(fr(D, 2))}. "
      f"teta un égale {msci(TH1)} radian.")
m3 = (f"دابا كنقلبو على le diamètre d. فla simulation، le laser الحمر: lambda égale {mots(LAM1_NM)} nanomètres، و D égale deux mètres. "
      "le fil كيعطي نفس la figure ديال fente عندها la largeur d. إذن d كتاخد البلاصة ديال a، ماشي ديال D: teta égale lambda sur d. "
      "ومن la figure، teta égale L sur deux D. إذن lambda sur d égale L sur deux D، و d égale deux lambda D sur L. "
      f"هنا le fil فيه d égale zéro virgule zéro sept millimètre، و L environ {mots(fr(L_sim, 1))} centimètres. "
      f"فالتمرين، L un égale {mots(fr(L1_CM, 2))} centimètres: d égale deux fois {mots(LAM1_NM)} fois dix puissance moins neuf، fois deux، "
      f"sur {msci(L1, 2)}. النتيجة: d égale {mots(s_dum)} micro mètre.")
m4 = (f"نفس le fil، ونفس l'écran. le laser الحمر: lambda un égale {mots(LAM1_NM)} nanomètres. شوف la tache centrale الحمرا. "
      f"دابا كنبدلو غير le laser: laser خضر، lambda deux égale {mots(LAM2_NM)} nanomètres. الخط ديال النقط هو la tache الحمرا اللي كانت. "
      "la tache الخضرا صغر منها. علاش؟ L égale deux lambda D sur d، و D و d ما تبدلوش: L proportionnelle à lambda. "
      "كنكتبو la relation deux fois، وكنقسمو: L deux sur L un égale lambda deux sur lambda un. "
      f"فالتمرين، L deux égale {mots(fr(L1_CM, 2))} fois {mots(LAM2_NM)} sur {mots(LAM1_NM)}. L deux égale {mots(s_l2)} centimètres.")
FIL = SIM + "diffraction.html?vue=fil"
EX["explication"] = {"activities": [{"id": "explication", "title": "Explication animée", "slides": [
  diapo_sim("ex_f1", "Question 1 : la figure s'étale perpendiculairement au cheveu", "Fil vertical → taches sur une ligne horizontale.",
            FIL, "Un fil fin éclairé par un laser", m1,
            [("Diffraction : la lumière s'étale perpendiculairement au fil", "الضو كيتفرق perpendiculairement au fil"),
             ("Fil vertical → taches sur une ligne horizontale", "إذن les taches على خط أفقي")],
            [dict(mot="le laser كيضوي", repere="laser"), dict(mot="le fil ممدود عموديا", repere="fente"),
             dict(mot="شوف l'écran:", commande="play_until", parametres={"moment": "tache_s_etale"}),
             dict(mot="الضو كيتفرق perpendiculairement au fil", cible="centre:0"),
             dict(mot="إذن les taches على خط أفقي", cible="centre:1"),
             dict(mot="فالوسط la tache centrale", commande="play_until", parametres={"moment": "tache_centrale"}),
             dict(mot="وبيناتهم des extinctions", commande="play_until", parametres={"moment": "extinctions"})]),
  diapo_sim("ex_f2", "Question 2 : θ dans le triangle", "tan θ = L/(2D) ≈ θ (en radian).",
            SIM + "ecart-angulaire.html", "L'angle θ, du centre de la tache à son bord", m2,
            [("tan θ = L/(2D) ≈ θ", "إذن tangente teta égale L sur deux D"),
             (f"θ₁ = {sci(L1, 2)}/(2 × {fr(D, 2)}) ≈ {s_th1} rad", f"teta un égale {msci(TH1)} radian")],
            [dict(mot="هادا le montage", repere="vue_montage"),
             dict(mot="le rayon اللي كيمشي للوسط", commande="play_until", parametres={"moment": "rayon_centre"}),
             dict(mot="و le rayon اللي كيمشي للحاشية", commande="play_until", parametres={"moment": "rayon_bord"}),
             dict(mot="الزاوية بيناتهم", commande="play_until", parametres={"moment": "angle_theta"}),
             dict(mot="كنشوفو le triangle", commande="play_until", parametres={"moment": "triangle_isole"}),
             dict(mot="إذن tangente teta égale L sur deux D", commande="play_until", parametres={"moment": "tan_ecrit"}),
             dict(mot="teta صغيرة en radian", commande="play_until", parametres={"moment": "petit_angle"}),
             dict(mot=f"teta un égale {msci(TH1)} radian", cible="centre:1")]),
  diapo_sim("ex_f3", "Question 3 : d prend la place de a", "λ/d = L/(2D) donc d = 2λD/L.",
            FIL, "Le fil de diamètre d et la tache de largeur L", m3,
            [("λ/d = L/(2D) ⇒ d = 2λD/L", "و d égale deux lambda D sur L"),
             (f"d ≈ {s_d} m = {s_dum} µm", f"النتيجة: d égale {mots(s_dum)} micro mètre")],
            [dict(mot="فla simulation، le laser الحمر", commande="set_parameters", parametres={"lambda_nm": LAM1_NM, "a_mm": d_sim, "D_m": 2.0}),
             dict(mot="le fil كيعطي نفس la figure", repere="fente"),
             dict(mot="ومن la figure، teta", commande="play_until", parametres={"moment": "mesure_L"}),
             dict(mot="و d égale deux lambda D sur L", cible="centre:0"),
             dict(mot="هنا le fil فيه", repere="L"),
             dict(mot=f"النتيجة: d égale {mots(s_dum)} micro mètre", cible="centre:1")]),
  diapo_sim("ex_f4", "Question 4 : laser vert, tache plus étroite", "L proportionnelle à λ : L₂/L₁ = λ₂/λ₁.",
            FIL, "Même fil, même écran : on change seulement le laser", m4,
            [("L₂/L₁ = λ₂/λ₁", "L deux sur L un égale lambda deux sur lambda un"),
             (f"L₂ = {fr(L1_CM, 2)} × {LAM2_NM}/{LAM1_NM} ≈ {s_l2} cm", f"L deux égale {mots(s_l2)} centimètres")],
            [dict(mot="le laser الحمر: lambda un", commande="set_parameters", parametres={"lambda_nm": LAM1_NM, "a_mm": d_sim, "D_m": 2.0, "trace_precedente": True}),
             dict(mot="شوف la tache centrale الحمرا", commande="play_until", parametres={"moment": "mesure_L"}),
             dict(mot="دابا كنبدلو غير le laser", commande="set_parameters", parametres={"lambda_nm": LAM2_NM}),
             dict(mot="الخط ديال النقط", repere="tache_avant"),
             dict(mot="la tache الخضرا صغر منها", repere="L"),
             dict(mot="L deux sur L un égale lambda deux sur lambda un", cible="centre:0"),
             dict(mot=f"L deux égale {mots(s_l2)} centimètres", cible="centre:1")]),
]}]}

# ---------------------------------------------------------------- version facile
EX["facile"] = {"activities": [{"id": "facile", "title": "Plus facile, pour s'entraîner", "slides": [
  vf_facile("fa_f1", "Plus facile : la direction de la figure", "سؤال ساهل: قول واش كل جملة صحيحة ولا غالطة.",
            "Un cheveu tendu verticalement est éclairé par un laser.", [
              ("Les taches sont alignées sur une ligne horizontale, perpendiculaire au cheveu.", True,
               "La lumière s'étale perpendiculairement à l'objet qui la diffracte : cheveu vertical, ligne horizontale."),
              ("Les taches sont alignées verticalement, le long du cheveu.", False,
               "La figure ne suit pas le cheveu : elle s'étale perpendiculairement à lui, donc horizontalement."),
              ("Le phénomène observé est la dispersion de la lumière.", False,
               "C'est la diffraction. La dispersion, c'est le prisme qui sépare les couleurs de la lumière blanche.")]),
  qcm_facile("fa_f2", "Plus facile : la relation de θ", "نتمرنو: اختار la bonne relation.",
             f"L₁ = {fr(L1_CM, 2)} cm et D = {fr(D, 2)} m. Quelle relation donne θ₁ (θ petit, en radian) ?",
             ["θ₁ = L₁/D", "θ₁ = L₁/(2D)", "θ₁ = 2D/L₁"], 1, {
               "1": {"juste": rep("برافو! الضلع المقابل هو L un sur deux، والمجاور هو D: teta un égale L un sur deux D.",
                                  f"Juste : θ₁ = L₁/(2D) = {s_th1} rad.")},
               "0": {"1": rep("قريب! ولكن teta كتبدا من الوسط ديال la tache، ماشي من الحاشية. الضلع المقابل ماشي L كاملة. عاود اختار.",
                              "θ va du centre au bord de la tache : le côté opposé n'est pas L entière. Réessaie."),
                     "2": rep("الجواب هو teta un égale L un sur deux D. الضلع المقابل هو نص la tache، L un sur deux.",
                              "Réponse : θ₁ = L₁/(2D) : le côté opposé est L₁/2.")},
               "2": {"1": rep("شوف: tangente هي المقابل على المجاور. واش D هو المقابل؟ عاود اختار.",
                              "tan θ = côté opposé / côté adjacent. Lequel est en face de θ ? Réessaie."),
                     "2": rep("الجواب هو teta un égale L un sur deux D: المقابل L un sur deux، على المجاور D. هنا قلبتي la fraction.",
                              "Réponse : θ₁ = L₁/(2D) ; 2D/L₁ est la fraction inversée.")}},
             f"L un égale {mots(fr(L1_CM, 2))} centimètres et D égale {mots(fr(D, 2))} mètres. Quelle relation donne teta un ?"),
  qcm_facile("fa_f3", "Plus facile : la relation du fil", "سؤال ساهل على le fil. اختار الجواب الصحيح.",
             "Un cheveu de diamètre d remplace la fente. Quelle relation donne d ?",
             ["d = λL/(2D)", "D = 2λd/L", "d = 2λD/L"], 2, {
               "2": {"juste": rep("برافو! lambda sur d égale L sur deux D، إذن d égale deux lambda D sur L.",
                                  "Juste : λ/d = L/(2D), donc d = 2λD/L.")},
               "0": {"1": rep("شوف: d كانت فالتحت، فteta égale lambda sur d. ملي كنخرجوها، واش كتطلع فوق مع L؟ عاود اختار.",
                              "Isole d dans λ/d = L/(2D) avec soin : L passe au dénominateur. Réessaie."),
                     "2": rep("الجواب هو d égale deux lambda D sur L. من lambda sur d égale L sur deux D، كنضربو فd وفdeux D، وكنقسمو على L.",
                              "Réponse : d = 2λD/L.")},
               "1": {"1": rep("رد البال: d صغيرة هي le diamètre، و D كبيرة هي la distance حتى ل l'écran. شكون اللي كيتقلب عليه؟ عاود اختار.",
                              "Attention : d (petit) est le diamètre, D (grand) la distance à l'écran. Réessaie."),
                     "2": rep("الجواب هو d égale deux lambda D sur L. d كتاخد البلاصة ديال a، ماشي ديال D.",
                              "Réponse : d = 2λD/L : d remplace a, pas D.")}},
             "Un cheveu de diamètre d remplace la fente. Quelle relation donne d ?"),
  assoc_facile("fa_f4", "Plus facile : chaque laser, sa tache",
               "نتمرنو: نفس الشعرة ونفس l'écran، كنبدلو غير le laser. ربط كل laser مع la largeur ديال la tache ديالو.",
               "Même cheveu, même écran : seul le laser change.", "Relie chaque laser à la largeur L de sa tache centrale.",
               [("1", f"Rouge, λ = {LAM1_NM} nm"), ("2", f"Vert, λ = {LAM2_NM} nm"), ("3", "Violet, λ = 400 nm")],
               [("a", f"L = {fr(L1_CM, 2)} cm"), ("b", f"L = {s_l2} cm"), ("c", f"L = {fr(LV_CM, 2)} cm")],
               {"1": "a", "2": "b", "3": "c"}, {
                 "1-a": (True, "Oui : la plus grande λ donne la tache la plus large.", "برافو: lambda الكبيرة كتعطي la tache الكبيرة."),
                 "1-b": (False, "L est proportionnelle à λ : le rouge, de plus grande λ, a la tache la plus large.", "لا، L proportionnelle à lambda. le rouge عندو أكبر lambda، إذن أكبر tache."),
                 "1-c": (False, "La plus petite tache va avec la plus petite λ, pas avec le rouge.", "لا، أصغر tache كتمشي مع أصغر lambda، ماشي مع le rouge."),
                 "2-a": (False, "Le vert a une λ plus petite que le rouge : sa tache est moins large.", "لا، le vert عندو lambda صغر من le rouge، إذن la tache ديالو صغر."),
                 "2-b": (True, f"Oui : L₂ = {fr(L1_CM, 2)} × {LAM2_NM}/{LAM1_NM} ≈ {s_l2} cm.", "برافو: le vert فالوسط، لا كبيرة لا صغيرة."),
                 "2-c": (False, "Le vert est entre le rouge et le violet : sa tache est entre les deux.", "لا، le vert بين le rouge و le violet، إذن la tache ديالو بيناتهم."),
                 "3-a": (False, "Le violet a la plus petite λ : sa tache est la plus étroite.", "لا، le violet عندو أصغر lambda، إذن أصغر tache."),
                 "3-b": (False, "Plus petite λ que le vert : la tache du violet est encore plus étroite.", "لا، lambda ديال le violet صغر من le vert، إذن la tache صغر."),
                 "3-c": (True, f"Oui : L = {fr(L1_CM, 2)} × 400/{LAM1_NM} ≈ {fr(LV_CM, 2)} cm, la plus étroite.", "برافو: أصغر lambda، أصغر tache.")},
               ("L est proportionnelle à λ (même d, même D) : rouge, vert, violet, du plus large au plus étroit.",
                "L proportionnelle à lambda: le rouge الكبير، من بعد le vert، ومن بعد le violet.")),
]}]}

# ---------------------------------------------------------------- exercice semblable
B_LAM1, B_D, B_L1, B_LAM2 = 633, 1.50, 2.5, 532
b_l1 = B_L1 * 1e-2
b_th = b_l1 / (2 * B_D); b_d = 2 * B_LAM1 * 1e-9 * B_D / b_l1; b_dum = b_d * 1e6; b_l2 = B_L1 * B_LAM2 / B_LAM1
EX["similaire"] = {"id": "phys_ex_ch3_fil_4_b", "titre": "Même exercice, autres données", "enonce": {
  "intro": (f"Yassine tend cette fois un cheveu horizontalement devant un laser de longueur d'onde λ₁ = {B_LAM1} nm. L'écran est à "
            f"D = {fr(B_D, 2)} m du cheveu ; la tache centrale mesure L₁ = {fr(B_L1, 2)} cm. On suppose θ petit : tan θ ≈ θ (en radian)."),
  "intro_dit": (f"نفس التمرين، بقيم أخرى. ياسين كيمد الشعرة بالعرض، قدام le laser، lambda un égale {mots(B_LAM1)} nanomètres. "
                f"l'écran بعيد ب D égale {mots(fr(B_D, 2))} mètre، و la tache centrale فيها L un égale {mots(fr(B_L1, 2))} centimètres."),
  "figures": [montage(B_LAM1, B_D, B_L1, False)],
  "donnees": [f"λ₁ = {B_LAM1} nm", f"D = {fr(B_D, 2)} m", f"L₁ = {fr(B_L1, 2)} cm", f"λ₂ = {B_LAM2} nm (question 4)"],
  "questions": [
    {"id": "1", "texte": "Nommer le phénomène observé, puis justifier la direction dans laquelle les taches sont alignées sur l'écran.",
     "reponse": phrase("La diffraction. Le cheveu est horizontal ; la lumière s'étale perpendiculairement au cheveu : les taches sont alignées sur une ligne verticale."),
     "clavier": {"aides": ["diffraction", "perpendiculairement au cheveu", "ligne verticale"], "pieges": ["dispersion", "ligne horizontale"]},
     "correction": correction([("1 : diffraction de la lumière", "la diffraction"),
                               ("Cheveu horizontal → taches sur une ligne verticale (perpendiculaire au cheveu)", "على خط عمودي")],
                              "السؤال un. هادي la diffraction. الشعرة أفقية، والضو كيتفرق perpendiculairement، إذن les taches على خط عمودي.")},
    {"id": "2", "texte": "Calculer l'écart angulaire θ₁.",
     "reponse": valeur("θ₁", round(b_th, 6), "rad", f"θ₁ = L₁/(2D) = {sci(b_l1, 2)}/(2 × {fr(B_D, 2)}) ≈ {sci(b_th)} rad"),
     "clavier": {"aides": ["tan θ = L/(2D)", "tan θ ≈ θ", "rad"], "pieges": ["θ = L/D"]},
     "correction": correction([("2 : θ₁ ≈ tan θ₁ = L₁/(2D)", "teta un égale L un sur deux D"), (f"θ₁ ≈ {sci(b_th)} rad", f"{msci(b_th)} radian")],
                              f"السؤال deux. teta un égale L un sur deux D. l'application numérique: {msci(b_l1, 2)} sur {mots(fr(2 * B_D, 2))}. teta un égale {msci(b_th)} radian.")},
    {"id": "3", "texte": "Montrer que d = 2λ₁D/L₁, puis calculer d en µm.",
     "reponse": valeur("d", round(b_dum, 2), "µm", f"d = 2λ₁D/L₁ = (2 × {B_LAM1}×10⁻⁹ × {fr(B_D, 2)})/({sci(b_l1, 2)}) ≈ {sci(b_d)} m = {fr(b_dum, 1)} µm"),
     "clavier": {"aides": ["θ = λ/d", "d = 2λD/L", "1 µm = 10⁻⁶ m"], "pieges": ["D = 2λd/L"]},
     "correction": correction([("3 : λ₁/d = L₁/(2D) donc d = 2λ₁D/L₁", "d égale deux lambda un D sur L un"),
                               (f"d ≈ {sci(b_d)} m = {fr(b_dum, 1)} µm", f"d égale {mots(fr(b_dum, 1))} micro mètre")],
                              f"السؤال trois. lambda un sur d égale L un sur deux D، إذن d égale deux lambda un D sur L un. d égale {mots(fr(b_dum, 1))} micro mètre.")},
    {"id": "4", "texte": f"On remplace le laser par un laser vert (λ₂ = {B_LAM2} nm), sans rien changer d'autre. Comment varie L ? Justifier, puis calculer L₂.",
     "reponse": valeur("L₂", round(b_l2, 3), "cm", f"L₂ = L₁·λ₂/λ₁ = {fr(B_L1, 2)} × {B_LAM2}/{B_LAM1} ≈ {fr(b_l2, 2)} cm"),
     "clavier": {"aides": ["L₂/L₁ = λ₂/λ₁", "cm"], "pieges": ["L₂ = L₁·λ₁/λ₂"]},
     "correction": correction([("4 : L proportionnelle à λ ; λ₂ < λ₁ donc L₂ < L₁", "L proportionnelle à lambda"),
                               (f"L₂ = L₁·λ₂/λ₁ ≈ {fr(b_l2, 2)} cm", f"L deux égale {mots(fr(b_l2, 2))} centimètres")],
                              f"السؤال quatre. L proportionnelle à lambda، و lambda deux صغر، إذن la tache كتصغار. L deux égale {mots(fr(b_l2, 2))} centimètres.")},
  ]}}

ecrire(EX)
