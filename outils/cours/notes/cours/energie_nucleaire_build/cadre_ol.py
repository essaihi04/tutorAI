"""Ajoute (ou remplace) la seule clé chapitres.ondes_lumineuses : relit, ajoute, réécrit aussitôt."""
import json, copy
from pathlib import Path
REPO = Path(r"backend/data/curriculum")
ex = json.loads((REPO / "exploration/ondes_lumineuses.json").read_text(encoding="utf-8"))["cadre"]
fiche = copy.deepcopy(ex)
fiche["_note"] = ("Fiche ajoutée le 10 novembre 2026 depuis exploration/ondes_lumineuses.json (dix professeurs, nationaux PC "
                  "2016-2025, perimetre.json). Le texte officiel du cadre n'a pas été relu mot à mot : capacités OL1 à OL11 à confirmer. "
                  "Lectures (dit) écrites comme le corpus de la voix (teta, nu, lambda zéro).")
for c in fiche["capacites"]:
    if c["id"] == "OL11":
        c["statut"] = "programme, hors examen national (aucun national PC 2016-2025) ; partie courte « pour le devoir » à la fin du cours"
F = []
def f(ecr, cap, dit, **kw):
    d = {"ecriture": ecr, "capacite": cap, "dit": dit}; d.update(kw); F.append(d)
f("θ = λ / a", "OL3", "teta égale lambda sur a", unites="θ en rad, λ et a en m", variantes_admises=["θ = λ / d (fil de diamètre d)"])
f("tan θ = L / (2D)", "OL4", "tangente teta égale L sur deux D", contexte="d'après la figure : côté opposé L/2, côté adjacent D",
  variantes_admises=["tan θ = (L/2) / D", "tan θ = (L/2) / D = L / (2D)", "tan θ ≈ θ"])
f("θ = L / (2D)", "OL4", "teta égale L sur deux D", contexte="θ petit, tan θ ≈ θ, θ en rad")
f("λ / a = L / (2D)", "OL4", "lambda sur a égale L sur deux D")
f("L = 2·λ·D / a", "OL4", "L égale deux lambda D sur a", unites="tout en m",
  variantes_admises=["L = 2λD / a", "L' = 2λD / a", "L = 2λD·(1/a)", "L = (2λ/a)·D", "L₂ / L₁ = λ₂ / λ₁", "L₂ / L₁ = a / d", "λ × 2D = a × L", "λ·2D = a·L"])
f("λ = a·L / (2D)", "OL4", "lambda égale a L sur deux D", variantes_admises=["λ = aL / (2D)", "λ₀ = a·L / (2D)"])
f("a = 2·λ·D / L", "OL4", "a égale deux lambda D sur L", variantes_admises=["a = 2λD / L", "a = 2λ₀D / L"])
f("d = 2·λ·D / L", "OL4", "d égale deux lambda D sur L", variantes_admises=["d = 2λD / L", "d = 2λD / L'", "d = 2λD₁ / L₁", "d = 2·λ·D₁ / L₁", "θ = λ / d"])
f("D = a·L / (2λ)", "OL4", "D égale a L sur deux lambda", variantes_admises=["D = aL / (2λ)"])
f("λ₂ / λ₁ = L₂ / L₁", "OL4", "lambda deux sur lambda un égale L deux sur L un", contexte="deux expériences, même fente, même D",
  variantes_admises=["λ₁ / a = L₁ / (2D)", "λ₂ / a = L₂ / (2D)", "λ₀R / λ₀j = L_R / L_j"])
f("λ₂ = L₂·λ₁ / L₁", "OL4", "lambda deux égale L deux fois lambda un sur L un", variantes_admises=["λ₂ = L₂ · λ₁ / L₁", "λ₀R = L_R·λ₀j / L_j"])
f("n = L / L'", "OL9", "n égale L sur L prime", contexte="même expérience dans l'air puis dans un liquide d'indice n",
  variantes_admises=["L' = L / n", "L' = 2λD / a"])
f("L = k·(1/a)", "OL5", "L égale k fois un sur a", contexte="courbe L = f(1/a) : droite passant par l'origine")
f("k = 2·λ·D", "OL5", "k égale deux lambda D", variantes_admises=["k = 2λD", "λ = k / (2D)"])
f("θ = λ·(1/a)", "OL5", "teta égale lambda fois un sur a", contexte="courbe θ = f(1/a) : k = λ", variantes_admises=["θ = k·(1/a)", "k = λ"])
f("L = k·D", "OL5", "L égale k fois D", contexte="courbe L = f(D)", variantes_admises=["k = 2λ / a", "λ = a·k / 2", "y = k·x"])
f("k = ΔL / Δ(1/a)", "OL5", "k égale delta L sur delta un sur a", variantes_admises=["k = Δy / Δx", "k = ΔL / ΔD"])
f("λ₀ = c / ν", "OL8", "lambda zéro égale c sur nu", unites="λ₀ en m, c en m/s, ν en Hz",
  variantes_admises=["c = λ₀·ν", "λ₀ = c·T"])
f("ν = c / λ₀", "OL8", "nu égale c sur lambda zéro", variantes_admises=["ν = c / λ₀j"])
f("v = λ·ν", "OL9", "v égale lambda fois nu", contexte="dans un milieu transparent", variantes_admises=["v = λ · ν", "λ = v / ν"])
f("n = c / v", "OL9", "n égale c sur v", unites="n sans unité, n ≥ 1", variantes_admises=["n ≥ 1"])
f("v = c / n", "OL9", "v égale c sur n")
f("λ = λ₀ / n", "OL9", "lambda égale lambda zéro sur n", variantes_admises=["n = λ₀ / λ"])
f("sin i = n·sin r", "OL11", "sinus i égale n sinus r", contexte="première face du prisme, prisme dans l'air",
  variantes_admises=["sin r = sin i / n"])
f("sin i' = n·sin r'", "OL11", "sinus i prime égale n sinus r prime", contexte="deuxième face")
f("A = r + r'", "OL11", "A égale r plus r prime", variantes_admises=["r' = A − r"])
f("D = i + i' − A", "OL11", "D égale i plus i prime moins A", contexte="angle de déviation")
f("L = 2λD·(1/a)", "OL5", "L égale deux lambda D fois un sur a", contexte="relation du cours écrite sous la forme de la courbe L = f(1/a)")
f("L = (2λ/a)·D", "OL5", "L égale deux lambda sur a", contexte="relation du cours écrite sous la forme de la courbe L = f(D) (« … fois D »)")
f("k = 2λ / a", "OL5", "k égale deux lambda sur a")
f("k = λ", "OL5", "k égale lambda", contexte="courbe θ = f(1/a)")
f("λ = k / (2D)", "OL5", "lambda égale k sur deux D")
f("λ = a·k / 2", "OL5", "lambda égale a fois k sur deux")
f("ν = v / λ", "OL9", "nu égale v sur lambda", contexte="la fréquence est la même dans le vide et dans le milieu")
f("tan θ = (L/2) / D", "OL4", "tangente teta égale L sur deux", contexte="« … divisé par D », avant simplification")
fiche["formules"] = F
fiche["hors_cadre"]["tolere_si_annonce"] = []
fiche["hors_cadre"]["_note"] = "La réfraction (rappel du collège) et le trou circulaire (figure sans formule) sont admis sans annonce : ils ne sont pas dans la liste des mots."
fiche["decisions"] = ["Relations du prisme (OL11) : au programme, jamais au national PC 2016-2025 → partie finale courte C9 annoncée « pour le devoir » (agent physique-chimie, 10 novembre 2026)."]
p = REPO / "cadre_reference_2bac_pc.json"
d = json.loads(p.read_text(encoding="utf-8"))
d["chapitres"]["ondes_lumineuses"] = fiche
p.write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("ok", list(d["chapitres"].keys()))
