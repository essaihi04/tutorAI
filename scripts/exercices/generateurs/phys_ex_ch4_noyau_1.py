# Exercice facile de physique (ch. 4, décroissance radioactive) : composition, isotopes, équation et type.
# Sources comparées (skill exercices § 2) :
# - exploration radioactivite.json : cas_types composition / isotopes / equation / type ; pieges « N = A + Z »,
#   « isotopes = même Z seulement », « élément trouvé par A », « le nombre de protons se conserve » ; erreurs_examen
#   « lois de Soddy non citées » ; exclus : neutrino, capture électronique (absents ici).
# - nationaux comparés : 2017 R (cobalt 60, β⁻ : équation et type), 2021 R (phosphore 32 → soufre 32, tableau),
#   2024 N (iridium 192 : composition), 2025 N (cadmium 107 : particule ᴬ_Z e à trouver), 2022 R (QCM composition C14).
#   Ici : l'azote 13, émetteur β⁺ (aucun national), trois noyaux dont un intrus de même A (¹³₆C) pour les isotopes,
#   la particule trouvée par Soddy à partir du noyau fils donné : autre noyau, autres données, autre chaîne.
# - séries en ligne : recherche web faite (séries Talamidi, moutamadris, kezakoo de 2ᵉ Bac BIOF listées) mais les pages
#   sont bloquées par le réseau de la session (talamidi.com, kezakoo.com introuvables) : seuls les titres et extraits
#   des résultats ont été lus ; l'exercice s'appuie sur le fichier d'exploration et les nationaux.
# - simulations du cours : noyau.html (vue notation, noyau=C14 ; vue isotopes), desintegration.html?type=beta_plus.
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _outils import *

SIM = "/media/simulations/physics/radioactivite-tableau/"

# ---------- données (calculées, puis écrites) ----------
def noyau(A, Z, X):
    sup = str(A).translate(str.maketrans("0123456789", "⁰¹²³⁴⁵⁶⁷⁸⁹"))
    sub = str(Z).translate(str.maketrans("-0123456789", "₋₀₁₂₃₄₅₆₇₈₉"))
    return f"{sup}{sub}{X}"

# exercice : azote 13 (β⁺) ; similaire : radium 226 (α)
P = dict(A=13, Z=7, X="N", nom="azote 13", iso=(14, 7, "N"), intrus=(13, 6, "C"), fils=(13, 6, "C"))
Pb = dict(A=226, Z=88, X="Ra", nom="radium 226", iso=(228, 88, "Ra"), intrus=(226, 90, "Th"), fils=(222, 86, "Rn"))
for d in (P, Pb):
    d["N"] = d["A"] - d["Z"]
    d["Ap"] = d["A"] - d["fils"][0]          # Soddy : A = A_fils + A_particule
    d["Zp"] = d["Z"] - d["fils"][1]
assert (P["N"], P["Ap"], P["Zp"]) == (6, 0, 1) and (Pb["N"], Pb["Ap"], Pb["Zp"]) == (138, 4, 2)
NP = noyau(13, 7, "N"); N14 = noyau(14, 7, "N"); C13 = noyau(13, 6, "C"); POS = noyau(0, 1, "e")


def schema(pere, fils, autres, titre):
    """Le père, la flèche de désintégration, le fils et la particule inconnue ; les autres noyaux de l'énoncé dessous."""
    return {"type": "schema", "titre": titre, "cadre": {"l": 4.2, "h": 2.2},
            "legende": "Le noyau père se désintègre : il donne le noyau fils et une particule ᴬ_Z x à identifier.",
            "elements": [
                {"f": "cercle", "c": [0.75, 1.35], "r": 0.42, "couleur": "orange", "remplir": "faible"},
                {"f": "texte", "at": [0.75, 1.3], "t": pere, "couleur": "blanc", "taille": "grand", "ancre": "centre"},
                {"f": "texte", "at": [0.75, 0.7], "t": "noyau père", "couleur": "faible", "taille": "petit", "ancre": "centre"},
                {"f": "fleche", "de": [1.3, 1.35], "a": [2.3, 1.35], "couleur": "jaune", "texte": "désintégration", "pos": "n"},
                {"f": "cercle", "c": [2.85, 1.35], "r": 0.42, "couleur": "cyan", "remplir": "faible"},
                {"f": "texte", "at": [2.85, 1.3], "t": fils, "couleur": "blanc", "taille": "grand", "ancre": "centre"},
                {"f": "texte", "at": [2.85, 0.7], "t": "noyau fils", "couleur": "faible", "taille": "petit", "ancre": "centre"},
                {"f": "fleche", "de": [3.3, 1.55], "a": [3.85, 1.95], "couleur": "rose"},
                {"f": "texte", "at": [3.9, 1.6], "t": "ᴬ_Z x ?", "couleur": "rose", "ancre": "centre"},
                {"f": "texte", "at": [2.1, 0.2], "t": autres, "couleur": "vert", "ancre": "centre"}]}




EX = {
  "id": "phys_ex_ch4_noyau_1", "type": "exercice", "version": 1, "status": "published",
  "matiere": "physique", "chapitre": "radioactivite", "cours": "phys_ch4_radioactivite",
  "titre": "L'azote 13 : composition, isotopes et désintégration", "niveau": "facile", "duree_min": 15,
  "origine": "Exercice original écrit pour Moalim (ni sujet du national, ni copie d'un livre).",
  "competences": ["Donner la composition d'un noyau ᴬ_Z X", "Reconnaître des isotopes", "Écrire une équation de désintégration avec les lois de Soddy et en déduire le type"],
  "enonce": {
    "intro": f"L'azote 13, de symbole {NP}, est un noyau radioactif utilisé en imagerie médicale. En se désintégrant, il donne un noyau de carbone {C13} et une particule ᴬ_Z x. On considère aussi le noyau d'azote {N14}, stable.",
    "intro_dit": "دابا نقراو l'énoncé. l'azote treize، noyau radioactif، كيستعملوه فالتصوير الطبي. ملي كيتفكك، كيعطي noyau de carbone treize، و واحد la particule ما عرفناهاش. وعندنا حتى l'azote quatorze، اللي هو stable.",
    "figures": [schema(NP, C13, f"Autres noyaux :  {N14} (stable)   {C13} (stable)", "La désintégration de l'azote 13")],
    "donnees": [f"Azote 13 : {NP}", f"Azote 14 : {N14} (stable)", f"Carbone 13 : {C13} (stable)", "Particules : ⁴₂He, ⁰₋₁e, ⁰₁e"],
    "questions": [
      {"id": "1", "texte": f"Donner la composition du noyau {NP}.",
       "texte_dit": "Question un: عطي la composition ديال le noyau d'azote treize.",
       "reponse": valeur("N", P["N"], "neutrons", f"Z = {P['Z']} protons ; N = A − Z = {P['A']} − {P['Z']} = {P['N']} neutrons"),
       "clavier": {"aides": ["Z", "A", "N = A − Z", "protons", "neutrons"], "pieges": ["N = A + Z", "N = Z"]},
       "aides": [
         aide(f"Dans {NP}, le nombre du haut est A (les nucléons), celui du bas est Z (les protons).",
              "شوف la notation: العدد اللي الفوق هو A، les nucléons. العدد اللي التحت هو Z، les protons."),
         aide("Les neutrons sont les nucléons qui ne sont pas des protons : N = A − Z.",
              "les neutrons هوما les nucléons اللي ماشي protons. إذن N égale A moins Z.")],
       "correction": correction([
           ("1 : Z = 7 protons", "Z égale sept protons"),
           ("N = A − Z = 13 − 7", "N égale A moins Z"),
           ("N = 6 neutrons", "N égale six neutrons")],
         "Question un. le noyau d'azote treize: Z égale sept protons. و les neutrons، N égale A moins Z، soit treize moins sept. N égale six neutrons."),
       "explication": "ex_n1", "facile": "fa_n1"},
      {"id": "2", "texte": f"Parmi les noyaux {NP}, {N14} et {C13}, lesquels sont des isotopes ? Justifier.",
       "texte_dit": "Question deux: من بين هاد les noyaux التلاتة، شكون هوما les isotopes؟ علل الجواب ديالك.",
       "reponse": phrase(f"{NP} et {N14} sont isotopes : même nombre de charge Z = 7, et nombres de nucléons différents (13 et 14). {C13} n'est pas un isotope de {NP} : même A = 13, mais Z différent (6 ≠ 7)."),
       "clavier": {"aides": ["même Z", "A différents", "isotopes", "Z = 7"], "pieges": ["même A", "même N"]},
       "aides": [
         aide("Compare d'abord les nombres du bas (Z), puis ceux du haut (A).",
              "قارن الأول الأعداد اللي التحت، Z. من بعد قارن الأعداد اللي الفوق، A."),
         aide("Des isotopes ont le même Z et des A différents. Même A ne suffit pas : c'est Z qui fait l'élément.",
              "les isotopes عندهم نفس Z، و A مختلف. نفس A ما كافيش: Z هو اللي كيحدد l'élément.")],
       "correction": correction([
           (f"2 : {NP} et {N14} : même Z = 7, A différents (13 et 14)", "نفس Z égale sept"),
           ("donc ce sont des isotopes de l'azote", "إذن هوما des isotopes"),
           (f"{C13} : Z = 6 ≠ 7 : pas un isotope de l'azote", "Z égale six، et pas sept")],
         "Question deux. l'azote treize و l'azote quatorze: نفس Z égale sept، et A différent، treize et quatorze. إذن هوما des isotopes. أما le carbone treize، عندو نفس A، ولكن Z égale six، et pas sept. ماشي نفس l'élément، إذن ماشي isotope."),
       "explication": "ex_n2", "facile": "fa_n2"},
      {"id": "3", "texte": f"Écrire l'équation de la désintégration de {NP} en précisant les lois utilisées, puis identifier la particule émise et le type de cette désintégration.",
       "texte_dit": "Question trois: كتب l'équation ديال la désintégration ديال l'azote treize، وقول شنو هوما les lois اللي استعملتي. من بعد عرف la particule، و le type ديال la désintégration.",
       "reponse": phrase(f"{NP} → {C13} + ᴬ_Z x. Lois de Soddy : conservation de A : 13 = 13 + A, donc A = 0 ; conservation de Z : 7 = 6 + Z, donc Z = 1. La particule est le positon {POS} : {NP} → {C13} + {POS}. C'est une désintégration β⁺."),
       "clavier": {"aides": ["A = A₁ + A₂", "Z = Z₁ + Z₂", "⁰₁e", "⁰₋₁e", "⁴₂He", "β⁺", "→"], "pieges": ["⁰₋₁e (β⁻)", "conservation des protons"]},
       "aides": [
         aide(f"Écris {NP} → {C13} + ᴬ_Z x, puis applique les deux lois de Soddy : une ligne pour A, une ligne pour Z.",
              "كتب l'azote treize كيعطي le carbone treize، plus x. من بعد طبق les lois de Soddy: سطر ل A، وسطر ل Z."),
         aide("A et Z de la particule disent son nom : ⁴₂He → α ; ⁰₋₁e → β⁻ ; ⁰₁e → β⁺.",
              "A و Z ديال la particule كيعطيوك السمية ديالها: noyau d'hélium هو alpha، l'électron هو bêta moins، le positon هو bêta plus.")],
       "correction": correction([
           (f"3 : {NP} → {C13} + ᴬ_Z x", "l'azote treize كيعطي le carbone treize"),
           ("Soddy, A : 13 = 13 + A ⇒ A = 0", "A égale zéro"),
           ("Soddy, Z : 7 = 6 + Z ⇒ Z = 1", "Z égale un"),
           (f"{NP} → {C13} + {POS} : positon, désintégration β⁺", "désintégration bêta plus")],
         "Question trois. l'azote treize كيعطي le carbone treize، plus x. d'après les lois de Soddy: pour A، treize égale treize plus A، إذن A égale zéro. pour Z، sept égale six plus Z، إذن Z égale un. la particule هي le positon. إذن هادي désintégration bêta plus."),
       "explication": "ex_n3", "facile": "fa_n3"}
    ]
  },
  "explication": {"activities": [{"id": "explication", "title": "Explication animée", "slides": [
    diapo_sim("ex_n1", "Question 1 : la composition d'un noyau",
      "En haut A (nucléons), en bas Z (protons) : N = A − Z.",
      SIM + "noyau.html?vue=notation&noyau=C14", "La notation ᴬ_Z X, puis l'exemple du carbone 14",
      "شوف كيفاش كنكتبو le noyau. الحرف X هو le symbole. الفوق على اليسار، A: les nucléons. التحت على اليسار، Z: les protons. و les neutrons، كنحسبوهم: N égale A moins Z. فالسبورة، l'exemple ديال le carbone quatorze: six protons، et quatorze moins six، huit neutrons. فالتمرين، l'azote treize: Z égale sept protons. إذن N égale treize moins sept، soit six neutrons.",
      [("N = A − Z", "N égale A moins Z"), ("N = 13 − 7 = 6 neutrons", "soit six neutrons")],
      [dict(mot="شوف كيفاش كنكتبو", commande="start"),
       dict(mot="الفوق على اليسار", commande="play_until", parametres={"moment": "nombre_A"}),
       dict(mot="التحت على اليسار", commande="play_until", parametres={"moment": "nombre_Z"}),
       dict(mot="كنحسبوهم", commande="play_until", parametres={"moment": "formule_N"}),
       dict(mot="N égale A moins Z", cible="centre:0"),
       dict(mot="فالسبورة، l'exemple", commande="play_until", parametres={"moment": "exemple_U"}),
       dict(mot="soit six neutrons", cible="centre:1")]),
    diapo_sim("ex_n2", "Question 2 : reconnaître des isotopes",
      "Isotopes : même Z, A différents.",
      SIM + "noyau.html?vue=isotopes", "Les isotopes de l'hydrogène et du carbone",
      "شوف هاد les noyaux ديال l'hydrogène. كلهم عندهم proton واحد: نفس Z. ولكن ماعندهومش نفس العدد ديال les neutrons: A مختلف. نفس الشي ل le carbone douze و le carbone quatorze. هادو des isotopes. فالتمرين، l'azote treize و l'azote quatorze: نفس Z égale sept، و A مختلف. إذن هوما des isotopes. le carbone treize عندو نفس A، ولكن Z égale six: ماشي نفس l'élément، ماشي isotope.",
      [("Isotopes : même Z, A différents", "هادو des isotopes"), ("¹³₇N et ¹⁴₇N : isotopes", "إذن هوما des isotopes")],
      [dict(mot="شوف هاد les noyaux", commande="start"),
       dict(mot="كلهم عندهم proton", commande="play_until", parametres={"moment": "meme_Z"}),
       dict(mot="ولكن ماعندهومش", commande="play_until", parametres={"moment": "A_different"}),
       dict(mot="نفس الشي ل le carbone", commande="play_until", parametres={"moment": "carbone"}),
       dict(mot="هادو des isotopes", commande="play_until", parametres={"moment": "definition"}),
       dict(mot="هادو des isotopes", cible="centre:0"),
       dict(mot="إذن هوما des isotopes", cible="centre:1")]),
    diapo_sim("ex_n3", "Question 3 : l'équation et le type",
      "Soddy : A puis Z ; la particule donne le type.",
      SIM + "desintegration.html?type=beta_plus", "La désintégration β⁺ du phosphore 30",
      "شوف le phosphore trente. لداخل le noyau، proton كيولي neutron، وكيخرج le positon. l'équation: le phosphore trente كيعطي le silicium trente، plus le positon. Soddy pour A: trente égale trente plus zéro. pour Z: quinze égale quatorze plus un. فالتمرين، l'azote treize كيعطي le carbone treize. pour A: treize égale treize plus A، إذن A égale zéro. pour Z: sept égale six plus Z، إذن Z égale un. هادا هو le positon: désintégration bêta plus.",
      [("13 = 13 + A ⇒ A = 0 ; 7 = 6 + Z ⇒ Z = 1", "إذن Z égale un"), ("¹³₇N → ¹³₆C + ⁰₁e : β⁺", "désintégration bêta plus")],
      [dict(mot="شوف le phosphore trente", commande="start"),
       dict(mot="proton كيولي neutron", commande="play_until", parametres={"moment": "transformation"}),
       dict(mot="وكيخرج le positon", commande="play_until", parametres={"moment": "emission"}),
       dict(mot="l'équation:", commande="play_until", parametres={"moment": "equation"}),
       dict(mot="Soddy pour A", commande="play_until", parametres={"moment": "soddy_A"}),
       dict(mot="pour Z: quinze", commande="play_until", parametres={"moment": "soddy_Z"}),
       dict(mot="إذن Z égale un", cible="centre:0"),
       dict(mot="désintégration bêta plus", commande="play_until", parametres={"moment": "conclusion"}),
       dict(mot="désintégration bêta plus", cible="centre:1")]),
  ]}]},
  "facile": {"activities": [{"id": "facile", "title": "Plus facile, pour s'entraîner", "slides": [
    qcm_facile("fa_n1", "Plus facile : la composition", "نتمرنو بسؤال ساهل. اختار الجواب الصحيح.",
      f"Le noyau {NP} contient…", ["7 protons et 13 neutrons", "13 protons et 7 neutrons", "7 protons et 6 neutrons"], 2, {
        "2": {"juste": rep("مزيان! Z égale sept protons، et N égale treize moins sept، soit six neutrons.", "Juste : Z = 7 protons, N = 13 − 7 = 6 neutrons.")},
        "0": {"1": rep("ما تقلقش. treize هو A، يعني كاع les nucléons، ماشي غير les neutrons. عاود اختار.", "13, c'est A : tous les nucléons, pas seulement les neutrons. Réessaie."),
              "2": rep("la réponse: sept protons et six neutrons. N égale A moins Z، soit treize moins sept.", "Réponse : 7 protons et 6 neutrons (N = A − Z = 13 − 7).")},
        "1": {"1": rep("رد البال: العدد اللي التحت هو Z، les protons. واش c'est sept ou treize؟ عاود اختار.", "Le nombre du bas, Z, compte les protons. Réessaie."),
              "2": rep("la réponse: sept protons et six neutrons. قلبتي A و Z.", "Réponse : 7 protons et 6 neutrons ; tu as inversé A et Z.")}},
      f"Le noyau d'azote treize contient ?"),
    vf_facile("fa_n2", "Plus facile : vrai ou faux", "سؤال ساهل: قول واش كل جملة صحيحة ولا غالطة.",
      f"Les noyaux {NP}, {N14} et {C13}.", [
        (f"{NP} et {N14} sont des isotopes.", True, "Même Z = 7 et A différents (13 et 14) : ce sont des isotopes."),
        (f"{NP} et {C13} sont des isotopes, car ils ont le même A.", False, "Des isotopes ont le même Z ; ici Z = 7 et Z = 6 : deux éléments différents.")]),
    assoc_facile("fa_n3", "Plus facile : la particule et le type", "سؤال ساهل: ربط كل particule مع le type ديالها.",
      "Relie chaque particule émise au type de désintégration.", "Relie chaque particule au type de désintégration.",
      [("1", "⁰₁e (positon)"), ("2", "⁰₋₁e (électron)"), ("3", "⁴₂He (noyau d'hélium)")],
      [("a", "β⁺"), ("b", "β⁻"), ("c", "α")],
      {"1": "a", "2": "b", "3": "c"},
      {"1-a": (True, "Oui : un positon émis, c'est β⁺.", "مزيان: le positon، هو bêta plus."),
       "1-b": (False, "β⁻ émet un électron, de charge −1 ; le positon a la charge +1.", "لا، bêta moins كتخرج l'électron. le positon عندو charge plus."),
       "1-c": (False, "α émet un noyau d'hélium (A = 4) ; le positon a A = 0.", "لا، alpha كتخرج noyau d'hélium. le positon ماعندو حتى nucléon."),
       "2-a": (False, "β⁺ émet un positon (charge +1) ; l'électron a la charge −1.", "لا، bêta plus كتخرج le positon. l'électron عندو charge moins."),
       "2-b": (True, "Oui : un électron émis, c'est β⁻.", "مزيان: l'électron، هو bêta moins."),
       "2-c": (False, "α émet un noyau d'hélium, pas un électron.", "لا، alpha كتخرج noyau d'hélium، ماشي électron."),
       "3-a": (False, "β⁺ émet un positon ; ⁴₂He, c'est un noyau d'hélium.", "لا، bêta plus كتخرج le positon، ماشي noyau d'hélium."),
       "3-b": (False, "β⁻ émet un électron ; ⁴₂He a 4 nucléons.", "لا، bêta moins كتخرج l'électron. noyau d'hélium فيه A égale quatre."),
       "3-c": (True, "Oui : un noyau d'hélium émis, c'est α.", "مزيان: noyau d'hélium، هو alpha.")},
      ("⁰₁e → β⁺ ; ⁰₋₁e → β⁻ ; ⁴₂He → α. Pour l'azote 13 : positon, donc β⁺.",
       "le positon هو bêta plus، l'électron هو bêta moins، و noyau d'hélium هو alpha. l'azote treize كيخرج le positon: bêta plus.")),
  ]}]},
  "similaire": {
    "id": "phys_ex_ch4_noyau_1_b", "titre": "Même exercice, autres données",
    "enonce": {
      "intro": f"Le radium 226, de symbole {noyau(226, 88, 'Ra')}, est radioactif. En se désintégrant, il donne un noyau de radon {noyau(222, 86, 'Rn')} et une particule ᴬ_Z x. On considère aussi les noyaux {noyau(228, 88, 'Ra')} et {noyau(226, 90, 'Th')}.",
      "intro_dit": "نفس التمرين، بقيم أخرى. le radium deux cent vingt-six كيتفكك، وكيعطي noyau de radon deux cent vingt-deux، و واحد la particule. وعندنا حتى le radium deux cent vingt-huit، و le thorium deux cent vingt-six.",
      "figures": [schema(noyau(226, 88, "Ra"), noyau(222, 86, "Rn"), f"Autres noyaux :  {noyau(228, 88, 'Ra')}   {noyau(226, 90, 'Th')}", "La désintégration du radium 226")],
      "donnees": [f"Radium 226 : {noyau(226, 88, 'Ra')}", f"Radium 228 : {noyau(228, 88, 'Ra')}", f"Thorium 226 : {noyau(226, 90, 'Th')}", "Particules : ⁴₂He, ⁰₋₁e, ⁰₁e"],
      "questions": [
        {"id": "1", "texte": f"Donner la composition du noyau {noyau(226, 88, 'Ra')}.",
         "reponse": valeur("N", Pb["N"], "neutrons", f"Z = {Pb['Z']} protons ; N = A − Z = {Pb['A']} − {Pb['Z']} = {Pb['N']} neutrons"),
         "clavier": {"aides": ["Z", "A", "N = A − Z"], "pieges": ["N = A + Z"]},
         "correction": correction([("1 : Z = 88 protons", "Z égale quatre-vingt-huit protons"),
                                   ("N = A − Z = 226 − 88 = 138 neutrons", "N égale cent trente-huit neutrons")],
                                  "Z égale quatre-vingt-huit protons. N égale A moins Z، soit deux cent vingt-six moins quatre-vingt-huit. N égale cent trente-huit neutrons.")},
        {"id": "2", "texte": f"Parmi les noyaux {noyau(226, 88, 'Ra')}, {noyau(228, 88, 'Ra')} et {noyau(226, 90, 'Th')}, lesquels sont des isotopes ? Justifier.",
         "reponse": phrase(f"{noyau(226, 88, 'Ra')} et {noyau(228, 88, 'Ra')} sont isotopes : même Z = 88, A différents (226 et 228). {noyau(226, 90, 'Th')} n'est pas un isotope du radium : même A = 226 mais Z = 90 ≠ 88."),
         "clavier": {"aides": ["même Z", "A différents"], "pieges": ["même A"]},
         "correction": correction([("2 : ²²⁶₈₈Ra et ²²⁸₈₈Ra : même Z = 88, A différents : isotopes", "نفس Z"),
                                   ("²²⁶₉₀Th : Z = 90 ≠ 88 : pas un isotope du radium", "Z égale quatre-vingt-dix")],
                                  "le radium deux cent vingt-six و le radium deux cent vingt-huit: نفس Z، و A مختلف: des isotopes. le thorium عندو Z égale quatre-vingt-dix: ماشي isotope ديال le radium.")},
        {"id": "3", "texte": f"Écrire l'équation de la désintégration de {noyau(226, 88, 'Ra')} en précisant les lois utilisées, puis identifier la particule émise et le type de cette désintégration.",
         "reponse": phrase(f"{noyau(226, 88, 'Ra')} → {noyau(222, 86, 'Rn')} + ᴬ_Z x. Soddy : 226 = 222 + A, donc A = 4 ; 88 = 86 + Z, donc Z = 2. La particule est ⁴₂He : {noyau(226, 88, 'Ra')} → {noyau(222, 86, 'Rn')} + ⁴₂He. Désintégration α."),
         "clavier": {"aides": ["A = A₁ + A₂", "Z = Z₁ + Z₂", "⁴₂He", "α"], "pieges": ["⁰₋₁e"]},
         "correction": correction([("3 : ²²⁶₈₈Ra → ²²²₈₆Rn + ᴬ_Z x", "le radium كيعطي le radon"),
                                   ("226 = 222 + A ⇒ A = 4 ; 88 = 86 + Z ⇒ Z = 2", "A égale quatre"),
                                   ("²²⁶₈₈Ra → ²²²₈₆Rn + ⁴₂He : désintégration α", "désintégration alpha")],
                                  "le radium كيعطي le radon، plus x. Soddy: A égale quatre، و Z égale deux. la particule هي noyau d'hélium: désintégration alpha.")}
      ]}}
}

ecrire(EX)
