# -*- coding: utf-8 -*-
"""Banc d'essai du moteur de visuels scientifiques.

Chaque cas est une figure qu'un tuteur 2BAC PC produirait vraiment, écrite
comme un LLM l'écrit — y compris ses tics (notation Python, ids accentués,
types inventés). On mesure ce qui SURVIT au normaliseur, pas ce qui est sûr :
la sécurité est déjà testée ailleurs.
"""
import sys, io, json, re
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "backend"))

from app.services.scientific_visual_skill import normalize_scientific_visual as N

CAS = []


def cas(matiere, intention, spec, attendu):
    CAS.append((matiere, intention, spec, attendu))


# ── JSXGraph : maths et physique ────────────────────────────────────
cas("Maths", "Parabole f(x)=x²", {
    "engine": "jsxgraph", "title": "f(x) = x²", "boundingBox": [-4, 10, 4, -2],
    "elements": [{"type": "function", "expression": "x^2", "color": "blue", "label": "f"}],
}, "1 courbe")

cas("Maths", "Parabole écrite en Python (x**2)", {
    "engine": "jsxgraph", "elements": [{"type": "function", "expression": "x**2"}],
}, "1 courbe")

cas("Maths", "Multiplication implicite 2x+1", {
    "engine": "jsxgraph", "elements": [{"type": "function", "expression": "2x + 1"}],
}, "refus attendu (documenté)")

cas("Maths", "Exponentielle décroissante", {
    "engine": "jsxgraph", "boundingBox": [-1, 3, 6, -1],
    "elements": [{"type": "function", "expression": "exp(-x/2)", "color": "green"}],
}, "1 courbe")

cas("Maths", "Logarithme népérien", {
    "engine": "jsxgraph", "elements": [{"type": "function", "expression": "ln(x)"}],
}, "1 courbe")

cas("Maths", "Étude de fonction : courbe + asymptote + point", {
    "engine": "jsxgraph", "boundingBox": [-6, 6, 6, -6], "grid": True,
    "elements": [
        {"type": "function", "expression": "1/x", "color": "blue"},
        {"type": "line", "points": [{"x": 0, "y": -6}, {"x": 0, "y": 6}], "dashed": True, "color": "red", "label": "Asymptote"},
        {"type": "point", "points": [{"x": 1, "y": 1}], "label": "A(1;1)"},
    ],
}, "3 éléments")

cas("Maths", "Tangente annotée avec un texte libre", {
    "engine": "jsxgraph", "elements": [
        {"type": "function", "expression": "x^2"},
        {"type": "text", "points": [{"x": 2, "y": 5}], "label": "f'(2) = 4"},
    ],
}, "2 éléments")

cas("Maths", "Triangle rectangle (polygone)", {
    "engine": "jsxgraph", "elements": [
        {"type": "polygon", "points": [{"x": 0, "y": 0}, {"x": 3, "y": 0}, {"x": 0, "y": 4}], "label": "ABC"},
    ],
}, "1 triangle")

cas("Physique", "Bilan des forces sur un solide", {
    "engine": "jsxgraph", "title": "Bilan des forces", "boundingBox": [-5, 5, 5, -5], "axis": False,
    "elements": [
        {"type": "point", "points": [{"x": 0, "y": 0}], "label": "S", "color": "cyan"},
        {"type": "arrow", "points": [{"x": 0, "y": 0}, {"x": 0, "y": -3}], "label": "P", "color": "red"},
        {"type": "arrow", "points": [{"x": 0, "y": 0}, {"x": 0, "y": 3}], "label": "R", "color": "green"},
    ],
}, "3 éléments")

cas("Physique", "Cercle trigonométrique (centre/rayon)", {
    "engine": "jsxgraph", "elements": [{"type": "circle", "center": {"x": 0, "y": 0}, "radius": 1}],
}, "1 cercle")

cas("Physique", "Cercle écrit avec points (comme les autres éléments)", {
    "engine": "jsxgraph", "elements": [{"type": "circle", "points": [{"x": 0, "y": 0}, {"x": 1, "y": 0}], "label": "C"}],
}, "1 cercle")

cas("Physique", "Onde sinusoïdale amortie", {
    "engine": "jsxgraph", "boundingBox": [0, 3, 10, -3],
    "elements": [{"type": "function", "expression": "3*exp(-x/5)*sin(2*x)", "color": "cyan"}],
}, "1 courbe")

cas("Physique", "Vecteur vitesse (type 'vector')", {
    "engine": "jsxgraph", "elements": [
        {"type": "vector", "points": [{"x": 0, "y": 0}, {"x": 2, "y": 2}], "label": "v"},
    ],
}, "1 vecteur")

# ── Cytoscape : SVT ─────────────────────────────────────────────────
cas("SVT", "Glycolyse (ids ASCII)", {
    "engine": "cytoscape", "title": "Glycolyse", "layout": "breadthfirst",
    "nodes": [{"id": "glucose", "label": "Glucose (C6)"}, {"id": "g6p", "label": "Glucose-6-P"},
              {"id": "pyruvate", "label": "2 Pyruvate (C3)"}],
    "edges": [{"from": "glucose", "to": "g6p", "label": "ATP → ADP"},
              {"from": "g6p", "to": "pyruvate", "label": "+ 4 ATP"}],
}, "3 nœuds / 2 flèches")

cas("SVT", "Respiration avec ids accentués (français naturel)", {
    "engine": "cytoscape", "title": "Respiration cellulaire",
    "nodes": [{"id": "acétyl_coa", "label": "Acétyl-CoA"}, {"id": "cycle_krebs", "label": "Cycle de Krebs"},
              {"id": "chaîne", "label": "Chaîne respiratoire"}],
    "edges": [{"from": "acétyl_coa", "to": "cycle_krebs"}, {"from": "cycle_krebs", "to": "chaîne"}],
}, "3 nœuds / 2 flèches")

cas("SVT", "Ids avec espaces", {
    "engine": "cytoscape",
    "nodes": [{"id": "ADN nucléaire", "label": "ADN"}, {"id": "ARN m", "label": "ARNm"}],
    "edges": [{"from": "ADN nucléaire", "to": "ARN m", "label": "Transcription"}],
}, "2 nœuds / 1 flèche")

cas("SVT", "Synthèse protéique (ids ASCII)", {
    "engine": "cytoscape", "layout": "breadthfirst",
    "nodes": [{"id": "adn", "label": "ADN"}, {"id": "arnm", "label": "ARN messager"},
              {"id": "prot", "label": "Protéine"}],
    "edges": [{"from": "adn", "to": "arnm", "label": "Transcription"},
              {"from": "arnm", "to": "prot", "label": "Traduction"}],
}, "3 nœuds / 2 flèches")

cas("SVT", "Croisement génétique avec source=/target=", {
    "engine": "cytoscape",
    "nodes": [{"id": "p1", "label": "P1 [vg+]"}, {"id": "f1", "label": "F1 100% hybride"}],
    "edges": [{"source": "p1", "target": "f1", "label": "×"}],
}, "2 nœuds / 1 flèche")

# ── Matter : mécanique ──────────────────────────────────────────────
cas("Physique", "Chute libre + sol", {
    "engine": "matter", "title": "Chute verticale", "width": 600, "height": 320,
    "gravity": {"x": 0, "y": 1}, "autoplay": True,
    "bodies": [{"id": "sol", "shape": "rectangle", "x": 300, "y": 305, "width": 580, "height": 20, "isStatic": True, "label": "Sol"},
               {"id": "balle", "shape": "circle", "x": 300, "y": 60, "radius": 22, "label": "Balle", "color": "orange", "restitution": 0.5}],
}, "2 corps")

cas("Physique", "Plan incliné (rectangle tourné de 30°)", {
    "engine": "matter", "title": "Plan incliné",
    "bodies": [{"id": "plan", "shape": "rectangle", "x": 300, "y": 250, "width": 400, "height": 16,
                "angle": 0.52, "isStatic": True, "label": "Plan (30°)"},
               {"id": "caisse", "shape": "rectangle", "x": 180, "y": 150, "width": 40, "height": 40, "label": "m"}],
}, "2 corps + inclinaison")

cas("Physique", "Pendule simple", {
    "engine": "matter", "title": "Pendule",
    "bodies": [{"id": "masse", "shape": "circle", "x": 420, "y": 220, "radius": 20, "label": "m"}],
    "constraints": [{"toBody": "masse", "pointA": {"x": 300, "y": 40}, "length": 180, "stiffness": 1}],
}, "1 corps + 1 fil")

cas("Physique", "Tir de projectile (vitesse initiale)", {
    "engine": "matter", "title": "Projectile",
    "bodies": [{"id": "sol", "shape": "rectangle", "x": 300, "y": 310, "width": 580, "height": 20, "isStatic": True},
               {"id": "obus", "shape": "circle", "x": 40, "y": 280, "radius": 10, "velocity": {"x": 12, "y": -12}, "label": "v0"}],
}, "2 corps + v0")

cas("Chimie", "Modèle moléculaire (atomes liés)", {
    "engine": "matter", "title": "Molécule d'eau", "gravity": {"x": 0, "y": 0},
    "bodies": [{"id": "o", "shape": "circle", "x": 300, "y": 160, "radius": 26, "label": "O", "color": "red"},
               {"id": "h1", "shape": "circle", "x": 240, "y": 220, "radius": 16, "label": "H"},
               {"id": "h2", "shape": "circle", "x": 360, "y": 220, "radius": 16, "label": "H"}],
    "constraints": [{"fromBody": "o", "toBody": "h1", "length": 85, "stiffness": 0.9},
                    {"fromBody": "o", "toBody": "h2", "length": 85, "stiffness": 0.9}],
}, "3 corps + 2 liaisons")


def resume(spec, sortie):
    if sortie is None:
        return "REFUSÉ (rien ne s'affiche)"
    moteur = sortie["engine"]
    if moteur == "jsxgraph":
        entree = len(spec.get("elements", []))
        garde = len(sortie["elements"])
        detail = ", ".join(e["type"] for e in sortie["elements"])
        return f"{garde}/{entree} éléments — {detail}"
    if moteur == "cytoscape":
        n_in, e_in = len(spec.get("nodes", [])), len(spec.get("edges", []))
        return (f"{len(sortie['nodes'])}/{n_in} nœuds, {len(sortie['edges'])}/{e_in} flèches"
                f" — ids={[n['id'] for n in sortie['nodes']]}")
    b_in = len(spec.get("bodies", []))
    c_in = len(spec.get("constraints", []))
    perdus = []
    for src, out in zip(spec.get("bodies", []), sortie["bodies"]):
        perdus += [k for k in src if k not in out and k != "shape"]
    return (f"{len(sortie['bodies'])}/{b_in} corps, {len(sortie.get('constraints', []))}/{c_in} liaisons"
            + (f" — champs ignorés: {sorted(set(perdus))}" if perdus else ""))


complets = partiels = refuses = 0
print(f"{'MATIÈRE':<9} {'INTENTION':<50} RÉSULTAT")
print("-" * 120)
for matiere, intention, spec, _attendu in CAS:
    sortie = N(json.loads(json.dumps(spec)))
    texte = resume(spec, sortie)
    fractions = re.findall(r"(\d+)/(\d+)", texte)
    if sortie is None:
        marque, refuses = "✗", refuses + 1
    elif any(garde != total for garde, total in fractions):
        # Le cas le plus dangereux : la figure s'affiche, amputée, et personne
        # ne le sait — ni le tuteur qui l'a annoncée, ni l'élève qui la lit.
        marque, partiels = "~", partiels + 1
    else:
        marque, complets = "✓", complets + 1
    print(f"{matiere:<9} {intention:<50} {marque} {texte}")
print("-" * 120)
print(f"{len(CAS)} cas — {complets} intacts, {partiels} amputés, {refuses} refusés")
