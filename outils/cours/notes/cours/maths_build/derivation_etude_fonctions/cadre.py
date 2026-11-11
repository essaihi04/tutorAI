"""Ajoute (ou remplace) la seule clé chapitres.derivation_etude_fonctions : relit, ajoute, réécrit aussitôt."""
import json, copy
from pathlib import Path
REPO = Path(r"backend/data/curriculum")
ex = json.loads((REPO / "exploration/derivation_etude_fonctions.json").read_text(encoding="utf-8"))["cadre"]
fiche = copy.deepcopy(ex)
fiche["_note"] = ("Fiche ajoutée le 11 novembre 2026 depuis exploration/derivation_etude_fonctions.json (dix professeurs, nationaux PC "
                  "2016-2025, perimetre.json clés etude_fonction et fonction_reciproque). Texte officiel du cadre non relu mot à mot : "
                  "capacités DEF1 à DEF10 à confirmer. Lectures (dit) écrites comme le corpus de la voix (f prime de x zéro, f seconde).")
liste_hors = fiche.pop("hors_cadre")
F = fiche["formules"]
def f(ecr, cap, dit, **kw):
    d = {"ecriture": ecr, "capacite": cap, "dit": dit}; d.update(kw); F.append(d)
# compléments : les écritures du cours qui ne sont pas déjà des formules de l'exploration
f("(T) : y = f'(x₀)(x − x₀) + f(x₀)", "DEF2", "y égale f prime de x zéro, facteur de x moins x zéro, plus f de x zéro",
  variantes_admises=["y = f'(x₀)(x − x₀) + f(x₀)", "y = f′(x_0)(x − x_0) + f(x_0)", "y = f'(2)(x − 2) + f(2)", "y = f′(2)(x − 2) + f(2)", "y = f′(1)(x − 1) + f(1)",
                     "y = f'(a)(x − a) + f(a)", "y = f(x₀)", "f'(x₀) = 0"])
f("lim (f(x) − f(x₀)) / (x − x₀) = l ∈ ℝ", "DEF1", "la limite, quand x tend vers x zéro, de f de x moins f de x zéro, sur x moins x zéro, égale l",
  variantes_admises=["lim (f(x) − f(x₀))/(x − x₀) = l ∈ ℝ  (x → x₀)", "l = f'(x₀) : le nombre dérivé", "lim (f(x) − f(x_0))/(x − x_0) = f'(x_0)",
                     "taux = (f(x) − f(1)) / (x − 1)", "pente de (AM) = (f(3) − f(1)) / (3 − 1)", "f_d'(1) = lim (f(x) − f(1))/(x − 1)", "f_g'(1) = lim (f(x) − f(1))/(x − 1)"])
f("f_d'(x₀) = f_g'(x₀)", "DEF1", "f prime à droite de x zéro égale f prime à gauche de x zéro",
  variantes_admises=["f dérivable en x₀ ⟺ f_d'(x₀) = f_g'(x₀)", "f_d′(1) ≠ f_g′(1)", "f_d′(0) ≠ f_g′(0)"])
f("(u·v)' = u'v + uv'", "DEF3", "u prime v plus u v prime", variantes_admises=["(u·v)′ = u′v + uv′"])
f("(u/v)' = (u'v − uv')/v²", "DEF3", "u prime v moins u v prime, sur v au carré", variantes_admises=["(u/v)′ = (u′v − uv′) / v²"])
f("(xⁿ)' = n·xⁿ⁻¹", "DEF3", "n fois x puissance n moins un", variantes_admises=["xⁿ → n·xⁿ⁻¹"])
f("(1/x)' = −1/x²", "DEF3", "moins un sur x au carré", variantes_admises=["1/x → −1/x²"])
f("(√x)' = 1/(2√x)", "DEF3", "un sur deux racine de x", variantes_admises=["√x → 1/(2√x)"])
f("(u + v)' = u' + v'", "DEF3", "u prime plus v prime", variantes_admises=["(u + v)′ = u′ + v′", "(k·u)′ = k·u′", "(k·u)' = k·u'"])
f("(uⁿ)' = n·u'·uⁿ⁻¹", "DEF3", "n fois u prime fois u puissance n moins un", variantes_admises=["(uⁿ)′ = n · u′ · uⁿ⁻¹"])
f("(√u)' = u'/(2√u)", "DEF3", "u prime, sur deux racine de u", variantes_admises=["(√u)′ = u′ / (2√u)"])
f("(ⁿ√u)' = u'/(n(ⁿ√u)ⁿ⁻¹)", "DEF3", "u prime, sur n fois racine n-ième de u, puissance n moins un",
  variantes_admises=["(ⁿ√u)′ = u′ / (n · (ⁿ√u)ⁿ⁻¹)", "(³√x)' = 1/(3(³√x)²)", "(³√x)′ = 1 / (3 (³√x)²)"])
f("(f∘g)'(x) = g'(x)·f'(g(x))", "DEF3", "g prime de x fois f prime de g de x", variantes_admises=["(f∘g)′(x) = g′(x) · f′(g(x))"])
f("f''(x) = (f'(x))'", "DEF6", "f seconde de x", variantes_admises=["f'(x) = 3x² − 3 ;  f''(x) = 6x", "f'' ≥ 0 : ∪ ;  f'' ≤ 0 : ∩", "f'' ≥ 0 : ∪", "f'' ≤ 0 : ∩"])
f("f(x) − (ax + b)", "DEF7", "f de x moins a x plus b", variantes_admises=["f(x) − y = 1/x", "f(x) − (2x + 1) = 1/x", "f(x) − (x − 1) = 1/(x − 1)", "f(x) − x = 4/x",
                                                                       "lim [f(x) − (ax + b)] = 0", "y = ax + b", "y = ax", "y = 2x + 1", "y = x − 1", "y = x", "x = a", "y = b", "x = 2", "y = 1"])
f("f(2a − x) = f(x)", "DEF8", "f de deux a moins x égale f de x", variantes_admises=["f(4 − x) = f(x)", "f(2a − x) + f(x) = 2b", "f(4 − x) + f(x) = 2", "f(−x) = f(x)", "f(−x) = −f(x)"])
f("f(x₀) = y₀ ⟺ f⁻¹(y₀) = x₀", "DEF10", "f moins un de y zéro égale x zéro", variantes_admises=["f(2) = 5 ⟺ f⁻¹(5) = 2", "J = f(I)"])
f("(f⁻¹)'(y₀) = 1 / f'(x₀)", "DEF10", "f moins un prime de y zéro égale un sur f prime de x zéro",
  variantes_admises=["(f⁻¹)'(y₀) = 1 / f'(x₀),  y₀ = f(x₀),  f'(x₀) ≠ 0", "(f⁻¹)'(5) = 1/f'(2) = 1/4", "(f⁻¹)′(2) = 1/f′(1) = 1/4", "(f⁻¹)′(y_0) = 1/f′(x_0)"])
fiche["formules"] = F
fiche["hors_cadre"] = {
    "_note": "Hors programme PC (perimetre.json, exploration) : ni à l'écrit ni dans la voix. « convexe » (courbe tournée vers le haut) est au programme ; « convexité » au sens de l'inégalité ne l'est pas.",
    "mots": ["bijection", "bijective", "injecti", "surjecti", "L'Hôpital", "l’Hôpital", "Rolle", "accroissements finis", "développement limité",
             "approximation affine", "division euclidienne", "arctan", "arcsin", "arccos", "Jensen", "inégalité de convexité", "convexité"],
    "tolere_si_annonce": [],
    "detail": liste_hors,
}
fiche["decisions"] = [
    "Pas d'approximation affine chiffrée : seulement l'idée que la courbe se confond avec sa tangente près du point (1re bac, absente des nationaux 2016-2025).",
    "Asymptote oblique : on part de la droite donnée par l'énoncé (une seule limite) ; pas de division euclidienne imposée.",
    "Dérivée de ⁿ√u gardée (une diapositive, df_dv5) : au programme (perimetre), absente des nationaux récents.",
    "Les mots « bijection, bijective » ne sont jamais employés : « f continue et strictement monotone sur I ».",
    "Fonctions des exemples : polynômes, rationnelles, racines ; ln et exp viennent aux chapitres suivants.",
    "Notation des dérivées latérales f_d'(x₀), f_g'(x₀) ; branche parabolique « de direction l'axe des ordonnées » (formule des énoncés nationaux).",
]
p = REPO / "cadre_reference_2bac_pc.json"
d = json.loads(p.read_text(encoding="utf-8"))
d["chapitres"]["derivation_etude_fonctions"] = fiche
p.write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("ok", list(d["chapitres"].keys()))
