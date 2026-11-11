"""Ajoute (ou remplace) la seule clé chapitres.limites_continuite : relit, ajoute, réécrit aussitôt."""
import json, copy
from pathlib import Path
REPO = Path(r"backend/data/curriculum")
fiche = copy.deepcopy(json.loads((REPO / "exploration/limites_continuite.json").read_text(encoding="utf-8"))["cadre"])
fiche["_note"] = ("Fiche ajoutée le 11 novembre 2026 depuis exploration/limites_continuite.json (dix professeurs, nationaux PC 2016-2025, "
                  "perimetre.json etude_fonction et fonction_reciproque). Identifiants LC1 à LC12 provisoires, à collationner sur le texte officiel.")
for c in fiche["capacites"]:
    if c["id"] == "LC7":
        c["texte"] = "Utiliser la dichotomie pour encadrer la solution α avec une amplitude donnée (sans algorithme, sans nombre d'itérations formel, sans majoration d'erreur)."
        c["statut"] = "programme, hors examen national"
    if c["id"] == "LC11":
        c["texte"] = "Connaître la puissance rationnelle d'un réel strictement positif, x^(p/q) = ᑫ√(xᵖ), et appliquer les règles des puissances."
F = fiche["formules"]
def add(ecr, cap, dit, **kw):
    d = {"ecriture": ecr, "capacite": cap, "dit": dit}; d.update(kw); F.append(d)
add("x² − 9 = (x − 3)(x + 3)", "LC1", "x carré moins neuf égale x moins trois, fois x plus trois", contexte="rappel de factorisation (o2)", variantes_admises=["x² − 9 = x² − 3²", "x³ − 1 = (x − 1)(x² + x + 1)", "x² − 1 = (x − 1)(x + 1)", "x² − 4 = (x − 2)(x + 2)"])
add("lim (x² − 9)/(x² − 4x + 3) = lim (x + 3)/(x − 1) = 3", "LC1", "la limite de x carré moins neuf, sur x carré moins quatre x plus trois", variantes_admises=["(x² − 9)/(x² − 4x + 3)", "lim 3x²/x² = 3", "lim 1/(√(x + 3) + 2) = 1/4", "lim 1/(x + 1) = 1/2"])
add("f([a ; b]) = [m ; M]", "LC4", "l'image du segment a b est le segment m, M", contexte="f continue non monotone")
add("x^(1/n) = ⁿ√x", "LC11", "x puissance un sur n égale racine n-ième de x", condition="x > 0", variantes_admises=["x^{1/n} = ⁿ√x", "8^(1/3) = ∛8 = 2", "8^{1/3} = ∛8 = 2"])
add("m = (a + b)/2", "LC7", "m égale a plus b sur deux", contexte="milieu de [a ; b]")
add("f(α) = 0", "LC6", "f de alpha égale zéro", variantes_admises=["α³ + α − 1 = 0", "α³ = 1 − α"])
add("f⁻¹(x) = √(x + 4) − 1", "LC8", "f moins un de x égale racine de x plus quatre, moins un", contexte="exemple x² + 2x − 3 sur ]−1 ; +∞[", variantes_admises=["f⁻¹(x) = x² + 1", "(y + 1)² = x + 4", "|y + 1| = √(x + 4)", "y + 1 = √(x + 4)", "y = x² + 1", "y − 1 = x²"])
fiche["hors_cadre"]["_note"] = "Mots qui n'apparaissent ni à l'écrit ni dans la voix pour la filière PC. « Prolongement par continuité » : on pose seulement « quelle valeur donner à f(a) pour que f soit continue en a ? »."
fiche["decisions"] = [
  "Dichotomie (LC7) : gardée en bloc court d1–d4 « pour les devoirs, pas demandé au national » ; mot « dichotomie » permis ; perimetre.json non modifié (motif « méthode de dichotomie » à restreindre : décision à valider) — agent maths, 10 novembre 2026.",
  "« Prolongement par continuité » : ni écrit ni dit (hors_cadre.mots).",
  "Puissances rationnelles (LC11) : trois diapositives courtes p1–p3, toujours avec x > 0.",
  "Clé du chapitre limites_continuite : créée ici ; sa création dans perimetre.json reste à valider.",
]
p = REPO / "cadre_reference_2bac_pc.json"
d = json.loads(p.read_text(encoding="utf-8"))
d["chapitres"]["limites_continuite"] = fiche
p.write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("ok", list(d["chapitres"].keys()))
