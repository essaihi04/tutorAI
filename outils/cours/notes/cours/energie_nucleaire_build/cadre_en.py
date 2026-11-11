"""Ajoute (ou remplace) la seule clé chapitres.energie_nucleaire : relit, ajoute, réécrit aussitôt (indent 2, ensure_ascii=False)."""
import json, copy, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from explo import cadre
REPO = Path(r"backend/data/curriculum")
fiche = copy.deepcopy(cadre)
fiche["_note"] = ("Fiche ajoutée le 11 novembre 2026 depuis exploration/energie_nucleaire.json (dix professeurs, nationaux PC "
                  "2016-2025, perimetre.json). Le texte officiel du cadre n'a pas été relu mot à mot : capacités EN1 à EN8 à confirmer. "
                  "Lectures (dit) écrites comme la voix les dit (E l, delta m, c au carré, méga électron volt).")
F = []
def f(ecr, cap, dit, **kw):
    d = {"ecriture": ecr, "capacite": cap, "dit": dit}; d.update(kw); F.append(d)
f("E = m·c²", "EN1", "E égale m fois c au carré", unites="E en J, m en kg, c = 3,00·10⁸ m/s", variantes_admises=["E = m × c²", "E = mc²"])
f("1 u = 1,66·10⁻²⁷ kg", "EN1", "un u égale un virgule soixante six fois dix puissance moins vingt sept kilogramme")
f("1 eV = 1,6·10⁻¹⁹ J", "EN1", "un électron volt égale un virgule six fois dix puissance moins dix neuf joule")
f("1 MeV = 1,6·10⁻¹³ J", "EN1", "un méga électron volt égale un virgule six fois dix puissance moins treize joule", variantes_admises=["1 MeV = 10⁶ eV"])
f("1 u = 931,5 MeV/c²", "EN1", "un u égale neuf cent trente et un virgule cinq méga électron volt sur c au carré",
  variantes_admises=["1 u·c² = 931,5 MeV", "1 u = 931,5 MeV·c⁻²", "1 u = 931,41 MeV/c²", "1 u = 931,49 MeV/c²"])
f("N = A − Z", "EN2", "N égale A moins Z")
f("Δm = Z·m_p + (A − Z)·m_n − m(ᴬ_ZX)", "EN2", "delta m égale Z m p plus A moins Z m n moins m du noyau",
  contexte="défaut de masse d'un noyau, toujours positif",
  variantes_admises=["Δm = Z·m_p + N·m_n − m(ᴬ_ZX)", "Δm = [Z·m_p + (A − Z)·m_n] − m(ᴬ_ZX)", "Δm = Z·m_p + (A − Z)·m_n − m(X)",
                     "Δm = E_ℓ / c²", "Δm = E_ℓ/c²"])
f("E_ℓ = Δm·c²", "EN3", "E l égale delta m fois c au carré", unites="E_ℓ en MeV si Δm en u (× 931,5) ; en J si Δm en kg",
  variantes_admises=["E_ℓ(ᴬ_ZX) = Δm·c²", "E_ℓ = Δm × c²"])
f("E_ℓ/A", "EN3", "E l sur A", unites="MeV/nucléon", variantes_admises=["ξ = E_ℓ/A", "ξ = E_ℓ / A"])
f("E_ℓ = A·(E_ℓ/A)", "EN7", "E l égale A fois E l sur A", variantes_admises=["E_ℓ = A·ξ", "E_ℓ = A × (E_ℓ/A)"])
f("Δm = Σm(produits) − Σm(réactifs)", "EN6", "delta m égale la somme des masses des produits moins la somme des masses des réactifs",
  contexte="variation de masse d'une réaction, négative quand elle libère de l'énergie")
f("ΔE = Δm·c²", "EN6", "delta E égale delta m fois c au carré",
  variantes_admises=["ΔE = [Σm(produits) − Σm(réactifs)]·c²", "ΔE = Δm × c²", "ΔE = E_f − E_i"])
f("E_lib = |ΔE|", "EN6", "E libérée égale la valeur absolue de delta E", variantes_admises=["E_libérée = |ΔE|"])
f("ΔE = ΣE_ℓ(réactifs) − ΣE_ℓ(produits)", "EN7", "delta E égale la somme des E l des réactifs moins la somme des E l des produits",
  variantes_admises=["ΔE = Σ E_ℓ(réactifs) − Σ E_ℓ(produits)", "ΔE = E_f − E_i"])
f("N = m·N_A/M", "EN8", "N égale m fois N A sur M", unites="m en g, M en g/mol", variantes_admises=["N = m·N_A / M"])
f("E = N·E_lib", "EN8", "E égale N fois E libérée", variantes_admises=["E = N × E_lib"])
fiche["formules"] = F
fiche["decisions"] = [
 "Fission de l'uranium 235 et courbe d'Aston : au programme (perimetre.json) mais jamais au national PC 2016-2025 → enseignées dans le corps du cours (C4, C5), exercices construits, présentés comme tels.",
 "E = hν (national 2016 seulement) et rendement d'une centrale (un seul professeur) : non retenus.",
 "Δm garde le même symbole pour le noyau (> 0) et la réaction (< 0), comme les énoncés ; le cours dit toujours lequel.",
 "Énergie de liaison par nucléon écrite E_ℓ/A (ξ admis en variante).",
]
p = REPO / "cadre_reference_2bac_pc.json"
d = json.loads(p.read_text(encoding="utf-8"))
d["chapitres"]["energie_nucleaire"] = fiche
p.write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("ok", list(d["chapitres"].keys()))
