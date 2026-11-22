# Exercice SVT ch. 2 (rôle du muscle strié squelettique) — niveau moyen (national) : intensité et fréquence des excitations.
# Entraîne : « décrire puis déduire » une courbe amplitude = f(intensité) avec les valeurs (seuil, amplitude maximale),
# expliquer par le recrutement des fibres, calculer l'intervalle T = 1/f, situer chaque excitation dans la phase de la
# secousse précédente pour nommer secousses isolées / tétanos imparfait / tétanos parfait, comparer les amplitudes
# et définir le tétanos parfait.
# Sources comparées (lecture seule, rien de copié) :
# - exploration du cours (cas_types « nommer_myogrammes », « myogramme_document », « definir » ; pieges « seuil ≠ amplitude
#   maximale », « la seconde stimulation n'est pas plus forte », « fusion pour deux, tétanos pour une série »,
#   « imparfait / parfait » ; erreurs_examen « décrire sans valeur ») ;
# - nationaux : 2020 R (quatre myogrammes à nommer, 1 pt), 2018 N (association myogramme / état des deux stimulations),
#   2017 N (QCM sur le tétanos parfait) — forme des questions reprise (nommer, justifier par la phase), aucun de leurs
#   documents ni de leurs propositions ;
# - séries en ligne : recherche faite (cours moutamadris BIOF « loi de recrutement, sommation, tétanos », recueil Charif
#   Al Idrissi « secousses isolées, tétanos imparfait et parfait », devoir N. Bahsina, dyrassa PDF 8, alloschool) mais
#   pages inaccessibles depuis cette session (réseau refusé) : seuls les extraits du moteur de recherche ont été lus.
# Données = modèles des simulations du cours : intensite.html (seuil 4 mV, maximum 9 mV, 20 mm) et sommation.html
# (vue serie : 12 excitations, 5 / 15 / 40 Hz ; secousse 10 / 40 / 50 ms ; plateau dentelé 14–32 mm, plateau lisse ≈ 60 mm).
# Les tracés sont calculés ici avec la formule de myogramme.js (superposition + saturation douce).
import math, sys
from _commun_svt import rep, qcm_facile, vrai_faux, association, ecrire

SI = "/media/simulations/svt/role_muscle_strie_squelettique-tableau/intensite.html?attente=1"
SS = "/media/simulations/svt/role_muscle_strie_squelettique-tableau/sommation.html?vue=serie&attente=1"

# ── modèle de myogramme.js ───────────────────────────────────────────
GAIN, PLAFOND, QUEUE = 0.7, 62, 1.6


def unite(tau, lat, con, rel):
    if not tau > lat:
        return 0.0
    u = tau - lat
    if u < con:
        return (1 - math.cos(math.pi * u / con)) / 2
    v = (u - con) / rel
    if v >= 1:
        return 0.0
    return (1 + math.cos(math.pi * v)) / 2 * (1 + QUEUE * v * v)


def sat0(L):
    return L / (1 + (L / PLAFOND) ** 4) ** 0.25


def train(stims, lat, con, rel, amp):
    ef = []
    for s in sorted(stims):
        if ef and s - ef[-1][0] < lat:
            continue
        r = sum(unite(s - t, lat, con, rel) for t, _ in ef)
        ef.append((s, 1 + GAIN * r))
    return lambda t: amp / 20 * sat0(sum(20 * g * unite(t - s, lat, con, rel) for s, g in ef)) * 20 / sat0(20)


def fr(v, d=2):
    s = f"{v:.{d}f}".rstrip("0").rstrip(".")
    return s.replace(".", ",")


def doc_intensite(seuil, imax, amax, titre):
    A = lambda i: 0 if i < seuil else amax if i >= imax else amax * (i - (seuil - 1)) / (imax - seuil + 1)
    pts = [[i, round(A(i), 2)] for i in range(1, 12)]
    el = [{"f": "ligne", "pts": pts, "couleur": "cyan", "epais": True}]
    el += [{"f": "point", "at": p, "couleur": "cyan"} for p in pts]
    pas = 5 if amax <= 20 else 4
    return {"type": "courbe", "titre": titre, "ratio": 0.6,
            "axes": {"x": {"min": 0, "max": 14.5, "nom": "intensité", "unite": "mV", "graduations": list(range(0, 12))},
                     "y": {"min": 0, "max": amax + 6, "nom": "amplitude", "unite": "mm", "graduations": list(range(0, amax + 1, pas))}},
            "legende": "Document 1 : amplitude de la réponse du muscle à des excitations isolées d'intensité croissante.",
            "elements": el}, A


def doc_serie(lettre, f, lat, con, rel, amp, ymax):
    stims = [k / f for k in range(12)]
    y = train(stims, lat, con, rel, amp)
    span = 11 / f + lat + con + rel + 0.04
    dt = 0.004 if span > 1 else 0.002
    n = int(span / dt) + 1
    pts = [[round(i * dt, 4), round(y(i * dt), 2)] for i in range(n)]
    # graduations du temps
    pas = 0.4 if span > 1.5 else 0.2 if span > 0.6 else 0.1
    grads, v = [], 0.0
    while v <= span + 1e-9:
        grads.append([round(v, 2), fr(v, 1)])
        v += pas
    el = [{"f": "ligne", "pts": pts, "couleur": "blanc", "epais": True}]
    for s in stims:   # les 12 excitations sous l'axe
        el.append({"f": "ligne", "pts": [[round(s, 4), -ymax * 0.12], [round(s, 4), -ymax * 0.04]], "couleur": "jaune"})
    el.append({"f": "texte", "at": [round(span * 0.06, 3), round(ymax * 0.9, 1)], "t": lettre, "couleur": "jaune", "taille": "grand"})
    return {"type": "courbe", "titre": f"Document 2, enregistrement {lettre} : {f} Hz", "ratio": 0.42,
            "axes": {"x": {"min": 0, "max": round(span * 1.12, 3), "nom": "t", "unite": "s", "graduations": grads},
                     "y": {"min": round(-ymax * 0.15, 1), "max": ymax, "nom": "amplitude", "unite": "mm",
                           "graduations": list(range(0, ymax, 20))}},
            "legende": "Douze excitations de même intensité (traits jaunes sous l'axe).",
            "elements": el}, y


FIG1, A1 = doc_intensite(4, 9, 20, "Document 1 : amplitude en fonction de l'intensité")
FA, ya = doc_serie("a", 5, 0.01, 0.04, 0.05, 20, 70)
FB, yb = doc_serie("b", 15, 0.01, 0.04, 0.05, 20, 70)
FC, yc = doc_serie("c", 40, 0.01, 0.04, 0.05, 20, 70)
FIG1B, A1B = doc_intensite(3, 8, 24, "Document 1 : amplitude en fonction de l'intensité")
FAB, yab = doc_serie("a", 4, 0.015, 0.045, 0.06, 24, 80)
FBB, ybb = doc_serie("b", 12, 0.015, 0.045, 0.06, 24, 80)
FCB, ycb = doc_serie("c", 30, 0.015, 0.045, 0.06, 24, 80)


def plateau(y, f):
    a, b = 5 / f, 10 / f
    v = [y(a + i * 0.0005) for i in range(int((b - a) / 0.0005))]
    return min(v), max(v)


# contrôles : les valeurs de l'attendu sont celles des tracés
assert abs(A1(4) - 3.33) < 0.01 and A1(3) == 0 and A1(9) == 20 and A1(11) == 20
assert abs(plateau(ya, 5)[1] - 20) < 0.1 and plateau(ya, 5)[0] < 0.1
assert 13.5 < plateau(yb, 15)[0] < 15 and 31 < plateau(yb, 15)[1] < 33
assert 58.5 < plateau(yc, 40)[0] and plateau(yc, 40)[1] < 61
assert A1B(3) == 4 and A1B(2) == 0 and A1B(8) == 24
assert 67 < plateau(ycb, 30)[0] and plateau(ycb, 30)[1] < 70
assert abs(1000 / 15 - 66.67) < 0.01 and abs(1000 / 12 - 83.33) < 0.01

QUESTIONS = [
  {"id": "1", "texte": "En exploitant le document 1, décrire l'évolution de l'amplitude de la réponse en fonction de l'intensité de l'excitation, puis déduire la valeur du seuil d'excitation.",
   "texte_dit": "السؤال numéro un: ب le document un، وصف l'évolution ديال l'amplitude ديال la réponse، en fonction de l'intensité ديال l'excitation. ومن بعد، استنتج la valeur ديال le seuil d'excitation.",
   "reponse": {"type": "phrase", "attendu": "De 1 à 3 mV, l'amplitude est nulle : les excitations sont inefficaces. À 4 mV, une première réponse apparaît (≈ 3 mm). De 4 à 9 mV, l'amplitude augmente, de ≈ 3 mm à 20 mm. Au-delà de 9 mV (10 et 11 mV), elle reste constante à 20 mm : c'est l'amplitude maximale. On en déduit que le seuil d'excitation est 4 mV (la plus petite intensité qui provoque une réponse)."},
   "clavier": {"aides": ["l'amplitude est nulle", "augmente", "reste constante", "seuil d'excitation", "mV", "mm"], "pieges": ["seuil = 9 mV", "seuil = 3 mV", "diminue"]},
   "aides": [
     {"texte": "Découpe la courbe en trois parties : où l'amplitude est nulle, où elle augmente, où elle ne change plus. Note les intensités qui les séparent.",
      "dit": "قسم la courbe: فين l'amplitude nulle، فين كتزاد، وفين ما بقاتش كتتبدل. وقرا les intensités اللي كيفرقو بيناتهم."},
     {"texte": "Pour chaque partie : « De … à … mV, l'amplitude … » avec les valeurs. Le seuil est la PREMIÈRE intensité qui donne une réponse.",
      "dit": "ف كل partie، قول: de tant à tant de millivolts، l'amplitude شنو كدير، مع les valeurs. و le seuil، هو أول intensité اللي كتعطي réponse."}],
   "correction": {"lignes": [
       {"texte": "1 : de 1 à 3 mV : amplitude nulle (excitations inefficaces)", "mot": "l'amplitude est nulle"},
       {"texte": "de 4 à 9 mV : l'amplitude augmente, de ≈ 3 à 20 mm", "mot": "l'amplitude كتزاد"},
       {"texte": "au-delà de 9 mV : constante, 20 mm (amplitude maximale)", "mot": "كتبقى ثابتة"},
       {"texte": "donc : seuil d'excitation = 4 mV", "mot": "le seuil d'excitation، c'est quatre millivolts"}],
     "parole": "السؤال numéro un. de un à trois millivolts، l'amplitude est nulle: les excitations inefficaces. à quatre millivolts، كتبان أول réponse، environ trois millimètres. de quatre à neuf millivolts، l'amplitude كتزاد، jusqu'à vingt millimètres. après neuf millivolts، كتبقى ثابتة، à vingt millimètres: c'est l'amplitude maximale. إذن le seuil d'excitation، c'est quatre millivolts."},
   "explication": "ex_s1", "facile": "fa_s1"},
  {"id": "2", "texte": "Expliquer l'augmentation de l'amplitude entre 4 mV et 9 mV, puis sa constance au-delà de 9 mV.",
   "texte_dit": "السؤال numéro deux: فسر علاش l'amplitude كتزاد entre quatre et neuf millivolts، وعلاش كتبقى ثابتة après neuf millivolts.",
   "reponse": {"type": "phrase", "attendu": "Le muscle est formé de nombreuses fibres musculaires. Au-dessus du seuil, plus l'intensité augmente, plus le nombre de fibres excitées augmente : c'est le recrutement des fibres. Chaque fibre ne répond pas plus fort, c'est leur nombre qui augmente, donc l'amplitude augmente. À 9 mV, toutes les fibres répondent : l'amplitude est maximale et ne peut plus augmenter."},
   "clavier": {"aides": ["fibres musculaires", "nombre de fibres excitées", "recrutement", "toutes les fibres"], "pieges": ["chaque fibre se contracte plus fort", "fatigue"]},
   "aides": [
     {"texte": "Un muscle n'est pas une seule cellule : de quoi est-il formé ?",
      "dit": "le muscle ماشي خلية وحدة: من شنو مكون؟"},
     {"texte": "Quand l'intensité augmente, chaque fibre répond-elle plus fort, ou d'autres fibres se mettent-elles à répondre ?",
      "dit": "ملي l'intensité كتزاد، واش كل fibre كتجاوب أقوى، ولا des fibres أخرين كيبداو يجاوبو؟"}],
   "correction": {"lignes": [
       {"texte": "2 : le muscle est formé de nombreuses fibres", "mot": "بزاف ديال les fibres"},
       {"texte": "intensité ↑ → nombre de fibres excitées ↑ : recrutement", "mot": "هادا هو le recrutement"},
       {"texte": "à 9 mV, toutes les fibres répondent : amplitude maximale", "mot": "جميع les fibres كيجاوبو"}],
     "parole": "السؤال numéro deux. le muscle فيه بزاف ديال les fibres musculaires. فوق le seuil، ملي l'intensité كتزاد، العدد ديال les fibres اللي كيجاوبو كيزيد: هادا هو le recrutement. كل fibre ما كتجاوبش أقوى، العدد هو اللي كيزيد، إذن l'amplitude كتزاد. à neuf millivolts، جميع les fibres كيجاوبو: c'est l'amplitude maximale، وما بقاتش تقدر تزيد."},
   "explication": "ex_s2", "facile": "fa_s2"},
  {"id": "3", "texte": "Calculer, pour l'enregistrement b (15 Hz), l'intervalle de temps T entre deux excitations successives (en ms).",
   "texte_dit": "السؤال numéro trois: حسب، ف l'enregistrement b، l'intervalle de temps T entre deux excitations successives، ب les millisecondes.",
   "reponse": {"type": "valeur", "grandeur": "T", "valeur": 66.7, "unite": "ms", "tolerance": 0.02,
               "attendu": "T = 1/f = 1/15 ≈ 0,067 s ≈ 67 ms"},
   "clavier": {"aides": ["T = 1/f", "1/15", "× 1000", "ms"], "pieges": ["T = 15 ms", "T = 6,7 ms"]},
   "aides": [
     {"texte": "15 Hz veut dire 15 excitations par seconde.",
      "dit": "quinze hertz، c'est quinze excitations par seconde."},
     {"texte": "T = 1/f donne T en secondes ; multiplie par 1000 pour l'avoir en millisecondes.",
      "dit": "T égale un sur f، كتعطي T ب les secondes. ومن بعد، fois mille، باش تحصل على les millisecondes."}],
   "correction": {"lignes": [
       {"texte": "3 : T = 1/f = 1/15", "mot": "T égale un sur f"},
       {"texte": "T ≈ 0,067 s ≈ 67 ms", "mot": "environ soixante-sept millisecondes"}],
     "parole": "السؤال numéro trois. T égale un sur f، égale un sur quinze، environ zéro virgule zéro six sept seconde، soit environ soixante-sept millisecondes."},
   "explication": "ex_s3", "facile": "fa_s3"},
  {"id": "4", "texte": "En comparant T à la durée des phases d'une secousse isolée, préciser pour a, b et c dans quelle phase de la secousse précédente tombe chaque excitation, puis nommer chacun des trois enregistrements.",
   "texte_dit": "السؤال numéro quatre: قارن T مع la durée ديال les phases ديال secousse isolée. ف a، b و c، حدد ف أشمن phase ديال la secousse اللي قبلها كتجي كل excitation، ومن بعد سمي كل enregistrement.",
   "reponse": {"type": "phrase", "attendu": "a : T = 1/5 = 0,2 s = 200 ms, plus long que la secousse (100 ms) : chaque excitation arrive après la fin de la secousse précédente → secousses isolées. b : T ≈ 67 ms, entre 50 et 100 ms : chaque excitation arrive pendant le relâchement de la secousse précédente → tétanos imparfait (plateau dentelé, entre ≈ 14 et 32 mm). c : T = 1/40 = 0,025 s = 25 ms, entre 10 et 50 ms : chaque excitation arrive pendant la contraction de la secousse précédente → tétanos parfait (plateau lisse)."},
   "clavier": {"aides": ["après la fin", "pendant le relâchement", "pendant la contraction", "secousses isolées", "tétanos imparfait", "tétanos parfait"], "pieges": ["fusion incomplète", "excitations plus intenses"]},
   "aides": [
     {"texte": "Une excitation arrive T ms après la précédente. Compare T à 10 ms (fin de la latence), 50 ms (sommet) et 100 ms (fin de la secousse).",
      "dit": "l'excitation الجاية كتجي من بعد T. قارن T مع هاد les instants: dix millisecondes، c'est la fin de la latence. cinquante millisecondes، c'est le sommet. et cent millisecondes، c'est la fin de la secousse."},
     {"texte": "Après la fin → secousses isolées ; pendant le relâchement → tétanos imparfait ; pendant la contraction → tétanos parfait. Ici c'est une série d'excitations : on parle de tétanos, pas de fusion de deux secousses.",
      "dit": "من بعد la fin: des secousses isolées. ف le relâchement: le tétanos imparfait. ف la contraction: le tétanos parfait. ورد البال: هنا، une série d'excitations، إذن tétanos، ماشي fusion de deux secousses."}],
   "correction": {"lignes": [
       {"texte": "4 : a : T = 200 ms > 100 ms : après la fin → secousses isolées", "mot": "des secousses isolées"},
       {"texte": "b : 50 ms < T ≈ 67 ms < 100 ms : pendant le relâchement → tétanos imparfait (plateau dentelé)", "mot": "le tétanos imparfait"},
       {"texte": "c : 10 ms < T = 25 ms < 50 ms : pendant la contraction → tétanos parfait (plateau lisse)", "mot": "le tétanos parfait"}],
     "parole": "السؤال numéro quatre. ف a، T égale deux cents millisecondes، c'est plus que cent millisecondes: l'excitation كتجي من بعد la fin ديال la secousse: des secousses isolées. ف b، T environ soixante-sept millisecondes، entre cinquante et cent: كتجي ف le relâchement: le tétanos imparfait، plateau dentelé. ف c، T égale vingt-cinq millisecondes، entre dix et cinquante: كتجي ف la contraction: le tétanos parfait، plateau lisse."},
   "explication": "ex_s4", "facile": "fa_s4"},
  {"id": "5", "texte": "Comparer l'amplitude de l'enregistrement c à celle d'une secousse isolée (enregistrement a), puis définir le tétanos parfait.",
   "texte_dit": "السؤال numéro cinq: قارن l'amplitude ديال l'enregistrement c مع l'amplitude ديال secousse isolée ف a، ومن بعد عرف le tétanos parfait.",
   "reponse": {"type": "phrase", "attendu": "Dans c, le plateau atteint environ 60 mm, contre 20 mm pour une secousse isolée (a) : 60/20 = 3, l'amplitude est environ 3 fois plus grande, car les secousses s'additionnent (sommation) ; c'est la contraction la plus forte du muscle. Le tétanos parfait est une contraction soutenue du muscle, au tracé en plateau lisse, obtenue par une série d'excitations efficaces dont chacune arrive pendant la phase de contraction de la secousse précédente."},
   "clavier": {"aides": ["plateau lisse", "60/20 = 3", "série d'excitations efficaces", "pendant la contraction"], "pieges": ["pendant le relâchement", "excitations plus intenses"]},
   "aides": [
     {"texte": "Lis la hauteur du plateau de c et la hauteur d'une secousse de a, puis divise l'une par l'autre.",
      "dit": "قرا الطول ديال le plateau ف c، و الطول ديال secousse ف a، ومن بعد قسم واحد على الآخر."},
     {"texte": "La définition contient : une série d'excitations efficaces ; chacune pendant la contraction de la précédente ; un plateau lisse.",
      "dit": "la définition: une série d'excitations efficaces، كل وحدة كتجي ف la contraction ديال اللي قبلها، و le tracé كيولي plateau lisse."}],
   "correction": {"lignes": [
       {"texte": "5 : c : plateau ≈ 60 mm ; secousse isolée (a) : 20 mm", "mot": "environ soixante millimètres"},
       {"texte": "60/20 = 3 : environ 3 fois plus grande (les secousses s'additionnent)", "mot": "environ trois fois"},
       {"texte": "tétanos parfait : contraction soutenue en plateau lisse, due à une série d'excitations efficaces, chacune pendant la contraction de la secousse précédente", "mot": "نعاود نقرا"}],
     "parole": "السؤال numéro cinq. ف c، le plateau كيوصل environ soixante millimètres، و la secousse isolée: vingt millimètres. soixante sur vingt، égale trois: environ trois fois، حيت les secousses كيتزادو. نعاود نقرا: le tétanos parfait, est une contraction soutenue du muscle, en plateau lisse, obtenue par une série d'excitations efficaces, dont chacune arrive pendant la contraction, de la secousse précédente."},
   "explication": "ex_s5", "facile": "fa_s5"},
]

EXPLICATION = [
  {"id": "ex_s1", "slide_type": "simulation", "title": "Question 1 : du tracé plat à l'amplitude maximale",
   "screen_content": {"lead": "1 à 3 mV : rien ; 4 mV : seuil ; jusqu'à 9 mV : l'amplitude augmente ; au-delà : 20 mm."},
   "visual": {"kind": "simulation", "url": SI, "caption": "Des excitations de plus en plus intenses"},
   "speech_text": {"mixed": "كنصيفطو des excitations، de un à onze millivolts. un، deux، trois millivolts: le tracé كيبقى plat، les excitations inefficaces. à quatre millivolts، أول réponse صغيرة: هادا هو le seuil d'excitation. من بعد، les réponses كيكبرو، jusqu'à neuf millivolts. après neuf millivolts، الطول ما بقاش كيتبدل: vingt millimètres، c'est l'amplitude maximale."},
   "concentration": {"demarrer": "reset",
     "centre": [{"texte": "1 à 3 mV : excitations inefficaces (0 mm)", "mot": "les excitations inefficaces"},
                {"texte": "seuil d'excitation = 4 mV", "mot": "هادا هو le seuil d'excitation"},
                {"texte": "à partir de 9 mV : amplitude maximale, 20 mm", "mot": "c'est l'amplitude maximale"}],
     "pointage": [{"mot": "un، deux، trois millivolts", "commande": "play_until", "parametres": {"moment": "inefficace"}},
                  {"mot": "le tracé كيبقى plat", "repere": "inefficaces"},
                  {"mot": "les excitations inefficaces", "cible": "centre:0"},
                  {"mot": "à quatre millivolts", "commande": "play_until", "parametres": {"moment": "seuil"}},
                  {"mot": "هادا هو le seuil d'excitation", "repere": "seuil"},
                  {"mot": "هادا هو le seuil d'excitation", "cible": "centre:1"},
                  {"mot": "les réponses كيكبرو", "commande": "play_until", "parametres": {"moment": "recrutement"}},
                  {"mot": "jusqu'à neuf millivolts", "commande": "play_until", "parametres": {"moment": "amplitude_max"}},
                  {"mot": "après neuf millivolts", "commande": "play_until", "parametres": {"moment": "au_dela"}},
                  {"mot": "c'est l'amplitude maximale", "repere": "amplitude_max"},
                  {"mot": "c'est l'amplitude maximale", "cible": "centre:2"}]}},
  {"id": "ex_s2", "slide_type": "simulation", "title": "Question 2 : le recrutement des fibres",
   "screen_content": {"lead": "Plus l'intensité augmente, plus de fibres répondent ; à 9 mV, toutes répondent."},
   "visual": {"kind": "simulation", "url": SI, "caption": "La coupe du muscle : les fibres excitées s'allument"},
   "speech_text": {"mixed": "شوف la coupe ديال le muscle على اليمين: فيها بزاف ديال les fibres. فوق le seuil، ملي l'intensité كتزاد، كيتشعلو les fibres كثر وكثر. كل fibre ما كتوليش أقوى: العدد ديال les fibres هو اللي كيزيد. هادا هو le recrutement. à neuf millivolts، جميع les fibres كيجاوبو، إذن l'amplitude ما بقاتش تقدر تزيد."},
   "concentration": {"demarrer": "reset",
     "centre": [{"texte": "intensité ↑ → nombre de fibres excitées ↑ : recrutement", "mot": "هادا هو le recrutement"},
                {"texte": "9 mV : toutes les fibres répondent → amplitude maximale", "mot": "جميع les fibres كيجاوبو"}],
     "pointage": [{"mot": "la coupe ديال le muscle", "repere": "coupe"},
                  {"mot": "فوق le seuil", "commande": "play_until", "parametres": {"moment": "recrutement"}},
                  {"mot": "هادا هو le recrutement", "cible": "centre:0"},
                  {"mot": "à neuf millivolts", "commande": "play_until", "parametres": {"moment": "amplitude_max"}},
                  {"mot": "جميع les fibres كيجاوبو", "repere": "amplitude_max"},
                  {"mot": "جميع les fibres كيجاوبو", "cible": "centre:1"}]}},
  {"id": "ex_s3", "slide_type": "simulation", "title": "Question 3 : l'intervalle entre deux excitations",
   "screen_content": {"lead": "15 Hz : T = 1/15 ≈ 0,067 s ≈ 67 ms."},
   "visual": {"kind": "simulation", "url": SS, "caption": "Une série de 12 excitations à 15 Hz"},
   "speech_text": {"mixed": "هنا، une série de douze excitations، à quinze hertz، c'est-à-dire quinze excitations par seconde. إذن l'intervalle entre deux excitations: T égale un sur quinze، environ zéro virgule zéro six sept seconde، soit soixante-sept millisecondes. شوف المكتوب الفوق: une stimulation toutes les zéro virgule zéro six sept seconde."},
   "concentration": {"demarrer": "reset",
     "centre": [{"texte": "T = 1/f = 1/15", "mot": "T égale un sur quinze"},
                {"texte": "T ≈ 0,067 s ≈ 67 ms", "mot": "soit soixante-sept millisecondes"}],
     "pointage": [{"mot": "هنا، une série", "commande": "play_until", "parametres": {"moment": "tetanos_imparfait"}},
                  {"mot": "une série de douze excitations", "repere": "stimulations"},
                  {"mot": "l'intervalle entre deux excitations", "repere": "s2"},
                  {"mot": "T égale un sur quinze", "cible": "centre:0"},
                  {"mot": "soit soixante-sept millisecondes", "cible": "centre:1"}]}},
  {"id": "ex_s4", "slide_type": "simulation", "title": "Question 4 : où tombe chaque excitation ?",
   "screen_content": {"lead": "Après la fin : secousses isolées ; pendant le relâchement : tétanos imparfait ; pendant la contraction : tétanos parfait."},
   "visual": {"kind": "simulation", "url": SS, "caption": "La même série à 5, 15 puis 40 Hz"},
   "speech_text": {"mixed": "نقارنو les trois séries، ب نفس l'intensité. à cinq hertz، T égale deux cents millisecondes: كل excitation كتجي من بعد la fin ديال la secousse اللي قبلها: des secousses isolées. à quinze hertz، كل excitation كتجي ف le relâchement ديال اللي قبلها: les secousses كيتزادو، والقمة فيها السنان: le tétanos imparfait. à quarante hertz، T égale vingt-cinq millisecondes: كل excitation كتجي ف la contraction: plateau lisse، le tétanos parfait."},
   "concentration": {"demarrer": "reset",
     "centre": [{"texte": "a : 5 Hz, T = 200 ms : secousses isolées", "mot": "des secousses isolées"},
                {"texte": "b : 15 Hz, pendant le relâchement : tétanos imparfait", "mot": "le tétanos imparfait"},
                {"texte": "c : 40 Hz, pendant la contraction : tétanos parfait", "mot": "le tétanos parfait"}],
     "pointage": [{"mot": "à cinq hertz", "commande": "play_until", "parametres": {"moment": "secousses_isolees"}},
                  {"mot": "des secousses isolées", "repere": "nom_trace"},
                  {"mot": "des secousses isolées", "cible": "centre:0"},
                  {"mot": "à quinze hertz", "commande": "play_until", "parametres": {"moment": "tetanos_imparfait"}},
                  {"mot": "والقمة فيها السنان", "repere": "plateau"},
                  {"mot": "le tétanos imparfait", "cible": "centre:1"},
                  {"mot": "à quarante hertz", "commande": "play_until", "parametres": {"moment": "tetanos_parfait"}},
                  {"mot": "plateau lisse، le tétanos parfait", "repere": "plateau"},
                  {"mot": "le tétanos parfait", "cible": "centre:2"}]}},
  {"id": "ex_s5", "slide_type": "simulation", "title": "Question 5 : le tétanos parfait, la contraction la plus forte",
   "screen_content": {"lead": "Plateau lisse ≈ 60 mm, environ 3 fois la secousse isolée (20 mm)."},
   "visual": {"kind": "simulation", "url": SS, "caption": "Série à 40 Hz : plateau lisse"},
   "speech_text": {"mixed": "à quarante hertz، le muscle ما عندو الوقت يرتاح: le plateau lisse، environ soixante millimètres. و la secousse isolée: vingt millimètres. إذن environ trois fois. هادي أقوى contraction ديال le muscle. نعاود نقرا: le tétanos parfait, est une contraction soutenue du muscle, en plateau lisse, obtenue par une série d'excitations efficaces, dont chacune arrive pendant la contraction, de la secousse précédente."},
   "concentration": {"demarrer": "reset",
     "centre": [{"texte": "c : plateau ≈ 60 mm = 3 × 20 mm", "mot": "إذن environ trois fois"},
                {"texte": "Tétanos parfait : série d'excitations efficaces, chacune pendant la contraction de la précédente ; plateau lisse", "mot": "نعاود نقرا"}],
     "pointage": [{"mot": "à quarante hertz", "commande": "play_until", "parametres": {"moment": "tetanos_parfait"}},
                  {"mot": "le plateau lisse", "repere": "plateau"},
                  {"mot": "إذن environ trois fois", "cible": "centre:0"},
                  {"mot": "أقوى contraction", "repere": "nom_trace"},
                  {"mot": "نعاود نقرا", "cible": "centre:1"}]}},
]

ASSO_G = [("a", "a : 5 Hz, chaque excitation après la fin de la secousse précédente"),
          ("b", "b : 15 Hz, chaque excitation pendant le relâchement"),
          ("c", "c : 40 Hz, chaque excitation pendant la contraction")]
ASSO_D = [("x", "secousses isolées"), ("y", "tétanos imparfait"), ("z", "tétanos parfait"), ("w", "fusion incomplète de deux secousses")]
ASSO_R = {
  "a-x": (True, "Oui : la secousse précédente est finie, chaque secousse reste seule.", "برافو: la secousse اللي قبلها سالات، إذن des secousses isolées."),
  "a-y": (False, "Le tétanos imparfait demande des excitations pendant le relâchement ; ici elles arrivent après la fin.", "لا، le tétanos imparfait، l'excitation كتجي ف le relâchement. وهنا كتجي من بعد la fin."),
  "a-z": (False, "Le tétanos parfait demande des excitations pendant la contraction ; ici elles arrivent après la fin.", "لا، le tétanos parfait، l'excitation كتجي ف la contraction. وهنا كتجي من بعد la fin."),
  "a-w": (False, "La fusion concerne deux excitations ; ici chaque secousse est séparée.", "لا، la fusion de deux excitations برك، وهنا les secousses بعاد على بعضياتهم."),
  "b-x": (False, "Les excitations arrivent avant la fin de la secousse précédente : les secousses ne sont pas isolées.", "لا، l'excitation كتجي قبل ما تسالي la secousse اللي قبلها، إذن ماشي isolées."),
  "b-y": (True, "Oui : une série, chaque excitation pendant le relâchement : plateau dentelé, tétanos imparfait.", "برافو: une série، و كل excitation ف le relâchement: plateau فيه السنان، le tétanos imparfait."),
  "b-z": (False, "Le tétanos parfait demande des excitations pendant la contraction ; ici c'est pendant le relâchement.", "لا، le tétanos parfait ف la contraction. وهنا ف le relâchement."),
  "b-w": (False, "Pendant le relâchement, oui, mais ici c'est une série d'excitations : on parle de tétanos.", "قريب، ف le relâchement. ولكن هنا، une série، إذن tétanos، ماشي fusion."),
  "c-x": (False, "Les excitations arrivent pendant la contraction : les secousses fusionnent.", "لا، l'excitation كتجي ف la contraction، إذن les secousses كيتزادو."),
  "c-y": (False, "Le tétanos imparfait correspond au relâchement ; ici c'est pendant la contraction.", "لا، le tétanos imparfait ف le relâchement. وهنا ف la contraction."),
  "c-z": (True, "Oui : une série, chaque excitation pendant la contraction : plateau lisse, tétanos parfait.", "برافو: une série، و كل excitation ف la contraction: plateau lisse، le tétanos parfait."),
  "c-w": (False, "La fusion concerne deux excitations ; ici c'est une série : on parle de tétanos.", "لا، la fusion de deux excitations برك. وهنا، une série، إذن tétanos."),
}

FACILE = [
  qcm_facile("fa_s1", "Plus facile : lire le seuil", "سؤال ساهل على le seuil d'excitation.",
    "D'après le document 1, le seuil d'excitation vaut…", ["3 mV", "4 mV", "9 mV"], 1, {
      "1": {"juste": rep("برافو! à quatre millivolts كتبان أول réponse، إذن le seuil، c'est quatre millivolts.", "Juste : première réponse à 4 mV, seuil = 4 mV.")},
      "0": {"1": rep("ما تقلقش. شوف la courbe à trois millivolts: واش كاينة réponse؟ عاود اختار.", "À 3 mV, y a-t-il une réponse ? Réessaie."),
            "2": rep("الجواب الصحيح: quatre millivolts. à trois millivolts، l'amplitude est nulle.", "Réponse : 4 mV ; à 3 mV l'amplitude est encore nulle.")},
      "2": {"1": rep("لا، neuf millivolts، c'est l'amplitude maximale، ماشي le seuil. le seuil هو أول réponse. عاود اختار.", "9 mV donne l'amplitude maximale ; le seuil est la première réponse. Réessaie."),
            "2": rep("الجواب الصحيح: quatre millivolts. neuf millivolts، c'est le début de l'amplitude maximale.", "Réponse : 4 mV ; 9 mV est le début de l'amplitude maximale.")}},
    "Le seuil d'excitation vaut combien ?"),
  qcm_facile("fa_s2", "Plus facile : pourquoi l'amplitude augmente", "سؤال ساهل: علاش l'amplitude كتزاد؟",
    "Entre 4 et 9 mV, l'amplitude augmente parce que…", ["chaque fibre se contracte plus fort", "les excitations arrivent plus rapprochées", "le nombre de fibres excitées augmente"], 2, {
      "2": {"juste": rep("برافو! ملي l'intensité كتزاد، العدد ديال les fibres اللي كيجاوبو كيزيد: le recrutement.", "Juste : le nombre de fibres excitées augmente (recrutement).")},
      "0": {"1": rep("ما تقلقش. كل fibre ما كتوليش أقوى. فكر ف العدد ديال les fibres. عاود اختار.", "Une fibre ne répond pas plus fort. Pense au nombre de fibres. Réessaie."),
            "2": rep("الجواب الصحيح: le nombre de fibres excitées كيزيد. هادا هو le recrutement.", "Réponse : le nombre de fibres excitées augmente (recrutement).")},
      "1": {"1": rep("لا، ف التجربة اللولى، les excitations isolées، وغير l'intensité اللي كتتبدل. عاود اختار.", "Dans l'expérience 1, les excitations sont isolées ; seule l'intensité change. Réessaie."),
            "2": rep("الجواب الصحيح: le nombre de fibres excitées كيزيد. الفرق ف l'intensité، ماشي ف la fréquence.", "Réponse : le nombre de fibres excitées augmente ; seule l'intensité change ici.")}},
    "Pourquoi l'amplitude augmente entre quatre et neuf millivolts ?"),
  qcm_facile("fa_s3", "Plus facile : l'intervalle T", "سؤال ساهل: حسب T.",
    "Pour 15 excitations par seconde (15 Hz), l'intervalle T entre deux excitations vaut…", ["15 ms", "67 ms", "6,7 ms"], 1, {
      "1": {"juste": rep("برافو! T égale un sur quinze، environ zéro virgule zéro six sept seconde، soit soixante-sept millisecondes.", "Juste : T = 1/15 ≈ 0,067 s ≈ 67 ms.")},
      "0": {"1": rep("ما تقلقش. quinze، c'est la fréquence، ماشي T. T égale un sur f. عاود اختار.", "15 est la fréquence, pas T : T = 1/f. Réessaie."),
            "2": rep("الجواب الصحيح: soixante-sept millisecondes. T égale un sur quinze، fois mille.", "Réponse : T = 1/15 s ≈ 67 ms.")},
      "2": {"1": rep("قريب، ولكن تحويل ل les millisecondes ما صحيحش. une seconde، c'est mille millisecondes. عاود اختار.", "Presque : 1 s = 1000 ms, vérifie la conversion. Réessaie."),
            "2": rep("الجواب الصحيح: soixante-sept millisecondes. zéro virgule zéro six sept seconde، fois mille.", "Réponse : 0,067 s × 1000 ≈ 67 ms.")}},
    "Pour quinze hertz, l'intervalle entre deux excitations vaut combien ?"),
  association("fa_s4", "Plus facile : nommer les trois enregistrements", "Relie chaque enregistrement à son nom.",
    "نتمرنو: ربط كل enregistrement مع السمية ديالو.",
    "Relie chaque enregistrement au nom du tracé.", ASSO_G, ASSO_D, {"a": "x", "b": "y", "c": "z"}, ASSO_R,
    ("a : secousses isolées ; b : tétanos imparfait ; c : tétanos parfait. La fusion ne concerne que deux excitations.",
     "a، des secousses isolées. b، le tétanos imparfait. c، le tétanos parfait. و la fusion، غير de deux excitations.")),
  vrai_faux("fa_s5", "Plus facile : le tétanos parfait", "Vrai ou faux : le tétanos parfait.",
    "سؤال ساهل: قرا كل جملة، وقول vrai ولا faux.",
    [("Dans c, le plateau vaut environ 3 fois l'amplitude d'une secousse isolée.", True,
      "Vrai : environ 60 mm contre 20 mm, 60/20 = 3."),
     ("Le tétanos parfait est obtenu avec des excitations plus intenses que le tétanos imparfait.", False,
      "Faux : les excitations ont la même intensité ; seule la fréquence change (elles sont plus rapprochées)."),
     ("Dans le tétanos parfait, chaque excitation arrive pendant la contraction de la secousse précédente.", True,
      "Vrai : elles arrivent avant le sommet, le muscle n'a pas le temps de se relâcher : plateau lisse."),
     ("Le tracé du tétanos parfait est un plateau dentelé.", False,
      "Faux : un plateau dentelé, c'est le tétanos imparfait ; le tétanos parfait donne un plateau lisse.")]),
]

SIM_Q = [
  {"id": "1", "texte": "En exploitant le document 1, décrire l'évolution de l'amplitude de la réponse en fonction de l'intensité de l'excitation, puis déduire la valeur du seuil d'excitation.",
   "reponse": {"type": "phrase", "attendu": "De 1 à 2 mV, l'amplitude est nulle (excitations inefficaces). À 3 mV, une première réponse apparaît (4 mm). De 3 à 8 mV, l'amplitude augmente, de 4 à 24 mm. Au-delà de 8 mV, elle reste constante à 24 mm (amplitude maximale). On en déduit que le seuil d'excitation est 3 mV."},
   "clavier": {"aides": ["l'amplitude est nulle", "augmente", "reste constante", "seuil d'excitation"], "pieges": ["seuil = 8 mV"]},
   "correction": {"lignes": [{"texte": "1 : 1 à 2 mV : nulle ; 3 à 8 mV : augmente de 4 à 24 mm", "mot": "l'amplitude كتزاد"},
                             {"texte": "au-delà de 8 mV : constante, 24 mm ; seuil = 3 mV", "mot": "le seuil d'excitation، c'est trois millivolts"}],
                  "parole": "السؤال numéro un. de un à deux millivolts، l'amplitude est nulle. de trois à huit millivolts، l'amplitude كتزاد، de quatre à vingt-quatre millimètres. après huit millivolts، كتبقى ثابتة. إذن le seuil d'excitation، c'est trois millivolts."}},
  {"id": "2", "texte": "Expliquer l'augmentation de l'amplitude entre 3 mV et 8 mV, puis sa constance au-delà de 8 mV.",
   "reponse": {"type": "phrase", "attendu": "Au-dessus du seuil, plus l'intensité augmente, plus le nombre de fibres musculaires excitées augmente (recrutement) ; chaque fibre ne répond pas plus fort. À 8 mV, toutes les fibres répondent : l'amplitude est maximale."},
   "clavier": {"aides": ["nombre de fibres excitées", "recrutement", "toutes les fibres"], "pieges": ["chaque fibre se contracte plus fort"]},
   "correction": {"lignes": [{"texte": "2 : intensité ↑ → nombre de fibres excitées ↑ : recrutement", "mot": "هادا هو le recrutement"},
                             {"texte": "à 8 mV, toutes les fibres répondent : amplitude maximale", "mot": "جميع les fibres كيجاوبو"}],
                  "parole": "السؤال numéro deux. ملي l'intensité كتزاد، العدد ديال les fibres اللي كيجاوبو كيزيد: هادا هو le recrutement. à huit millivolts، جميع les fibres كيجاوبو: c'est l'amplitude maximale."}},
  {"id": "3", "texte": "Calculer, pour l'enregistrement b (12 Hz), l'intervalle de temps T entre deux excitations successives (en ms).",
   "reponse": {"type": "valeur", "grandeur": "T", "valeur": 83.3, "unite": "ms", "tolerance": 0.02, "attendu": "T = 1/f = 1/12 ≈ 0,083 s ≈ 83 ms"},
   "clavier": {"aides": ["T = 1/f", "× 1000", "ms"], "pieges": ["T = 12 ms"]},
   "correction": {"lignes": [{"texte": "3 : T = 1/f = 1/12", "mot": "T égale un sur f"},
                             {"texte": "T ≈ 0,083 s ≈ 83 ms", "mot": "environ quatre-vingt-trois millisecondes"}],
                  "parole": "السؤال numéro trois. T égale un sur f، égale un sur douze، environ zéro virgule zéro huit trois seconde، soit environ quatre-vingt-trois millisecondes."}},
  {"id": "4", "texte": "En comparant T à la durée des phases d'une secousse isolée, préciser pour a, b et c dans quelle phase de la secousse précédente tombe chaque excitation, puis nommer chacun des trois enregistrements.",
   "reponse": {"type": "phrase", "attendu": "a : T = 1/4 = 250 ms, plus long que la secousse (120 ms) : après la fin → secousses isolées. b : T ≈ 83 ms, entre 60 et 120 ms : pendant le relâchement → tétanos imparfait (plateau dentelé). c : T = 1/30 ≈ 33 ms, entre 15 et 60 ms : pendant la contraction → tétanos parfait (plateau lisse)."},
   "clavier": {"aides": ["après la fin", "pendant le relâchement", "pendant la contraction"], "pieges": ["fusion incomplète"]},
   "correction": {"lignes": [{"texte": "4 : a : 250 ms > 120 ms → secousses isolées", "mot": "des secousses isolées"},
                             {"texte": "b : 60 < 83 < 120 ms, relâchement → tétanos imparfait", "mot": "le tétanos imparfait"},
                             {"texte": "c : 15 < 33 < 60 ms, contraction → tétanos parfait", "mot": "le tétanos parfait"}],
                  "parole": "السؤال numéro quatre. ف a، T égale deux cent cinquante millisecondes، c'est plus que la secousse: des secousses isolées. ف b، T environ quatre-vingt-trois millisecondes، ف le relâchement: le tétanos imparfait. ف c، T environ trente-trois millisecondes، ف la contraction: le tétanos parfait."}},
  {"id": "5", "texte": "Comparer l'amplitude de l'enregistrement c à celle d'une secousse isolée (enregistrement a), puis définir le tétanos parfait.",
   "reponse": {"type": "phrase", "attendu": "Dans c, le plateau atteint environ 70 mm contre 24 mm pour une secousse isolée : 70/24 ≈ 2,9, soit environ 3 fois plus (sommation des secousses). Le tétanos parfait est une contraction soutenue du muscle, au tracé en plateau lisse, obtenue par une série d'excitations efficaces dont chacune arrive pendant la phase de contraction de la secousse précédente."},
   "clavier": {"aides": ["plateau lisse", "pendant la contraction"], "pieges": ["pendant le relâchement"]},
   "correction": {"lignes": [{"texte": "5 : c ≈ 70 mm, a : 24 mm, environ 3 fois plus", "mot": "environ trois fois"},
                             {"texte": "tétanos parfait : série d'excitations efficaces, chacune pendant la contraction de la précédente ; plateau lisse", "mot": "نعاود نقرا"}],
                  "parole": "السؤال numéro cinq. ف c، le plateau environ soixante-dix millimètres، و la secousse isolée: vingt-quatre millimètres: environ trois fois. نعاود نقرا: le tétanos parfait, est une contraction soutenue du muscle, en plateau lisse, obtenue par une série d'excitations efficaces, dont chacune arrive pendant la contraction, de la secousse précédente."}},
]

EX = {
  "id": "svt_ex_ch2_sommation_1", "type": "exercice", "version": 1, "status": "published",
  "matiere": "svt", "chapitre": "role_muscle_strie_squelettique", "cours": "svt_ch2_role_muscle_strie_squelettique",
  "titre": "Intensité et fréquence des excitations : recrutement, secousses isolées et tétanos", "niveau": "moyen", "duree_min": 25,
  "origine": "Exercice original écrit pour Moalim (ni sujet du national, ni copie d'un livre).",
  "competences": ["Décrire une courbe avec ses valeurs puis déduire le seuil", "Expliquer le recrutement des fibres",
                  "Situer une excitation dans les phases de la secousse précédente", "Nommer secousses isolées, tétanos imparfait et parfait", "Définir le tétanos parfait"],
  "enonce": {
    "intro": "On étudie la réponse du muscle gastrocnémien d'une grenouille relié à un myographe. Expérience 1 : on applique des excitations isolées d'intensité croissante, de 1 à 11 mV ; le document 1 donne l'amplitude de chaque réponse. Expérience 2 : on applique trois séries de 12 excitations de même intensité (10 mV), à trois fréquences différentes : 5 Hz (a), 15 Hz (b) et 40 Hz (c) ; le document 2 représente les trois enregistrements obtenus.",
    "intro_dit": "نقراو l'énoncé. عندنا le muscle gastrocnémien ديال الضفدعة، مربوط ب le myographe. التجربة اللولى: des excitations isolées، l'intensité ديالهم كتزاد، de un à onze millivolts. le document un، كيعطي l'amplitude ديال كل réponse. التجربة الثانية: trois séries de douze excitations، ب نفس l'intensité، dix millivolts، ولكن à trois fréquences: cinq hertz، quinze hertz، et quarante hertz. le document deux، فيه les trois enregistrements: a، b، و c.",
    "figures": [FIG1, FA, FB, FC],
    "donnees": ["Secousse isolée de ce muscle : latence 10 ms, contraction 40 ms, relâchement 50 ms (durée totale 100 ms)",
                "f excitations par seconde (f en Hz) : intervalle entre deux excitations T = 1/f",
                "Document 2 : même échelle d'amplitude pour a, b et c"],
    "questions": QUESTIONS},
  "explication": {"activities": [{"id": "explication", "title": "Explication animée", "slides": EXPLICATION}]},
  "facile": {"activities": [{"id": "facile", "title": "Plus facile, pour s'entraîner", "slides": FACILE}]},
  "similaire": {
    "id": "svt_ex_ch2_sommation_1_b", "titre": "Même exercice, autres données",
    "enonce": {
      "intro": "Mêmes expériences sur un autre muscle de grenouille. Expérience 1 : excitations isolées de 1 à 11 mV (document 1). Expérience 2 : trois séries de 12 excitations de même intensité (10 mV), à 4 Hz (a), 12 Hz (b) et 30 Hz (c) (document 2).",
      "intro_dit": "نفس التجارب، ب muscle آخر. التجربة اللولى: des excitations isolées، de un à onze millivolts. التجربة الثانية: trois séries de douze excitations، à quatre hertz، douze hertz، et trente hertz.",
      "figures": [FIG1B, FAB, FBB, FCB],
      "donnees": ["Secousse isolée de ce muscle : latence 15 ms, contraction 45 ms, relâchement 60 ms (durée totale 120 ms)",
                  "Intervalle entre deux excitations : T = 1/f", "Document 2 : même échelle d'amplitude pour a, b et c"],
      "questions": SIM_Q}},
}

if __name__ == "__main__":
    ecrire(EX, sys.argv[1])
