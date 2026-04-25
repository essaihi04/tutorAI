"""
Topic Atlas Service — Historical BAC topic coverage matrix (2016-2025).

Builds and queries a structured map of which topics have been tested in each
BAC national exam, broken down by year × session × part × exercise. Used to:

  1. Predict which topics are most likely in BAC 2026 (gap analysis for PC/Math,
     format rotation analysis for SVT).
  2. Inject balanced priorities into the LLM coaching/diagnostic/study_plan
     prompts (rule 50/30/20: high priority / regular / minimum coverage).
  3. Guide students implicitly without them having to ask.

Pedagogical principle — the two logics are different:

  • SVT: ALL 6-8 domains are tested EVERY year. What varies is the FORMAT
    (Part 1 Restitution vs Part 2 Exercise 1/2/3 Raisonnement). We track
    format rotation per domain and predict "this year Géologie will be an
    Ex1 profond, not a Part1 restitution".

  • Physics/Chemistry/Math: the exam picks a SUBSET of the cadre's topics.
    We track coverage gaps: topics tested long ago but absent recently are
    strong 2026 candidates.
"""
from __future__ import annotations

import json
import logging
import re
from pathlib import Path
from typing import Optional

_log = logging.getLogger(__name__)

EXAMS_DIR = Path(__file__).resolve().parent.parent.parent / "data" / "exams"
ATLAS_PATH = EXAMS_DIR / "topic_atlas.json"


# ══════════════════════════════════════════════════════════════════════════════
#  TAXONOMIE OFFICIELLE — strictement alignée sur les cadres de référence
#  BAC marocain 2BAC PC (Sciences Physiques, option internationale française).
#
#  Sources (backend/cours 2bac pc/cadres de references 2BAC PC/) :
#   • SVT : 4 grands domaines
#   • Physique-Chimie : 4 sous-domaines physique (67%) + 4 sous-domaines chimie (33%)
#   • Mathématiques : 3 domaines principaux (Analyse 55% / Algèbre-Géo 15% / Proba-Complexes 30%)
#
#  Les mots-clés sont pensés pour couvrir tout le vocabulaire présent dans les
#  sujets BAC 2016-2025. ON N'AJOUTE AUCUN DOMAINE ABSENT DU CADRE OFFICIEL.
# ══════════════════════════════════════════════════════════════════════════════

# ─── SVT (4 domaines, 100%) ────────────────────────────────────────────────
SVT_DOMAINS: dict[str, list[str]] = {
    "Domaine 1 — Consommation de la matière organique et flux d'énergie": [
        # Respiration cellulaire / métabolisme
        "respiration cellulaire", "respiration", "fermentation",
        "glycolyse", "cycle de krebs", "chaîne respiratoire",
        "mitochondrie", "atp", "adp", "nadh", "fadh", "nad",
        "pyruvate", "acide pyruvique", "aérobie", "anaérobie",
        "phosphorylation oxydative", "bilan énergétique",
        "rendement énergétique",
        # Muscle strié squelettique
        "muscle strié", "fibre musculaire", "contraction musculaire",
        "myofibrille", "sarcomère", "actine", "myosine",
        "conversion d'énergie", "énergie mécanique", "régénération de l'atp",
        "créatine phosphate", "phosphocréatine",
    ],
    "Domaine 2 — Information génétique et lois statistiques de transmission": [
        # Nature et expression de l'information génétique
        "adn", "acide désoxyribonucléique", "réplication",
        "transcription", "traduction", "arn messager", "arnm",
        "code génétique", "codon", "anticodon", "ribosome",
        "synthèse des protéines", "synthèse protéique",
        "cycle cellulaire", "mitose", "méiose", "caryotype",
        "chromosome", "chromatide", "centromère",
        "gène", "allèle", "mutation", "exon", "intron",
        # Transmission / lois statistiques (Mendel)
        "lois de mendel", "mendel", "monohybridisme", "dihybridisme",
        "génotype", "phénotype", "lignée pure", "hybridation",
        "brassage génétique", "brassage intrachromosomique",
        "brassage interchromosomique", "crossing-over", "crossing over",
        "gènes liés", "gènes indépendants", "ségrégation",
        "arbre généalogique", "pedigree", "hérédité", "héréditaire",
        "allèle dominant", "allèle récessif", "maladie génétique",
        "chromosome sexuel", "autosome", "test-cross",
    ],
    "Domaine 3 — Utilisation des matières organiques et inorganiques (pollution, déchets, radioactivité)": [
        # Ordures ménagères
        "ordure", "ordures ménagères", "déchet", "déchets ménagers",
        "tri sélectif", "tri des déchets", "recyclage", "valorisation",
        "compostage", "méthanisation", "biogaz",
        # Pollution
        "pollution", "polluant", "pollutant", "contamination",
        "pollution atmosphérique", "pollution des eaux", "pollution du sol",
        "impact environnemental", "dégradation de l'environnement",
        "développement durable", "biodiversité",
        # Matières énergétiques fossiles / climat
        "matière énergétique", "combustible fossile", "énergie fossile",
        "effet de serre", "gaz à effet de serre", "réchauffement climatique",
        "changement climatique", "climat", "giec",
        "co2", "co₂", "dioxyde de carbone", "atmosphère",
        "océan", "réservoir de carbone", "cycle du carbone",
        "émissions", "anthropique", "empreinte carbone",
        # Matières radioactives / énergie nucléaire
        "radioactivité", "matière radioactive", "énergie nucléaire",
        "déchet radioactif", "centrale nucléaire",
        "alternative écologique", "énergie renouvelable",
        # Contrôle qualité
        "qualité des milieux", "salubrité", "norme scientifique",
        "contrôle de la qualité",
    ],
    "Domaine 4 — Géodynamique interne et formation des chaînes de montagnes": [
        # Tectonique des plaques
        "tectonique", "tectonique des plaques", "plaque tectonique",
        "plaque lithosphérique", "lithosphère", "asthénosphère",
        "dorsale", "dorsale océanique", "rift",
        "convergence", "divergence", "accrétion",
        # Chaînes de montagnes (subduction/obduction/collision)
        "chaîne de montagnes", "chaînes de montagnes", "orogenèse",
        "subduction", "obduction", "collision",
        "fosse océanique", "prisme d'accrétion",
        "volcanisme de subduction", "volcanisme andésitique",
        # Déformations tectoniques
        "déformation tectonique", "déformations tectoniques",
        "pli", "plissement", "faille", "faille inverse",
        "chevauchement", "nappe de charriage", "contrainte",
        # Métamorphisme
        "métamorphisme", "métamorphique", "minéral index",
        "série métamorphique", "métamorphisme dynamique",
        "métamorphisme thermodynamique", "faciès métamorphique",
        "gneiss", "schiste", "foliation", "schistosité",
        "ophiolite", "éclogite", "amphibolite",
        # Granitisation
        "granitisation", "granite", "granite d'anatexie",
        "granite intrusif", "anatexie", "migmatite",
        "métamorphisme général", "métamorphisme de contact",
    ],
}

# ─── PHYSIQUE (4 sous-domaines officiels, 67% du total PC) ─────────────────
PHYSIQUE_DOMAINS: dict[str, list[str]] = {
    "Physique — Sous-domaine 1 : Ondes (11%)": [
        # Ondes mécaniques
        "onde mécanique", "onde progressive", "ondes mécaniques",
        "célérité", "propagation", "corde vibrante", "ressort longitudinal",
        "onde transversale", "onde longitudinale",
        "onde sonore", "ondes sonores", "son",
        # Ondes lumineuses
        "diffraction", "interférence", "interférences",
        "laser", "lumière monochromatique", "lumière polychromatique",
        "frange", "fente", "réseau", "longueur d'onde",
        "indice de réfraction", "dispersion",
    ],
    "Physique — Sous-domaine 2 : Transformations nucléaires (8%)": [
        "désintégration", "radioactivité", "radioactif",
        "alpha", "α", "bêta", "β", "gamma", "γ",
        "demi-vie", "période radioactive", "constante radioactive",
        "noyau", "nucléide", "nucléon", "isotope",
        "fission nucléaire", "fusion nucléaire",
        "datation", "datation radioactive", "carbone 14",
        "cadmium", "uranium", "polonium", "plutonium", "iode 131",
        "tritium", "becquerel", "activité",
        "défaut de masse", "énergie de liaison",
    ],
    "Physique — Sous-domaine 3 : Électricité (21%)": [
        # Dipôle RC
        "condensateur", "dipôle rc", "charge du condensateur",
        "décharge du condensateur", "constante de temps τ",
        "capacité", "farad", "échelon de tension",
        # Dipôle RL
        "bobine", "auto-induction", "dipôle rl",
        "inductance", "henry",
        # RLC
        "rlc", "circuit rlc", "dipôle rlc",
        "oscillations libres", "oscillations forcées",
        "résonance électrique", "pulsation propre",
        "période propre électrique", "circuit lc",
        # Modulation (inclus dans Électricité au cadre)
        "modulation d'amplitude", "modulation am", "détection",
        "porteuse",
    ],
    "Physique — Sous-domaine 4 : Mécanique (27%)": [
        # Lois de Newton + mouvements rectilignes/paraboliques
        "chute libre", "chute verticale", "mouvement d'un projectile",
        "mouvement parabolique", "deuxième loi de newton",
        "2e loi de newton", "mouvement rectiligne", "référentiel",
        "accélération", "vitesse", "force",
        # Mouvements dans champs
        "champ magnétique uniforme", "champ électrique uniforme",
        "champ de pesanteur", "champ gravitationnel", "satellite",
        "lois de kepler", "force de lorentz",
        "mouvement circulaire uniforme", "trajectoire circulaire",
        # Systèmes oscillants
        "pendule pesant", "pendule simple", "pendule élastique",
        "pendule de torsion", "système masse-ressort",
        "oscillation mécanique", "oscillateur harmonique",
        "oscillations mécaniques",
    ],
}

# ─── CHIMIE (4 sous-domaines officiels, 33% du total PC) ───────────────────
CHIMIE_DOMAINS: dict[str, list[str]] = {
    "Chimie — Sous-domaine 1 : Transformations rapides et lentes d'un système chimique (6%)": [
        "transformation lente", "transformation rapide",
        "cinétique", "cinétique chimique", "vitesse de réaction",
        "vitesse volumique", "vitesse instantanée",
        "suivi cinétique", "loi de vitesse",
        "catalyseur", "catalyse",
        "temps de demi-réaction", "t1/2", "avancement",
        "concentration initiale",
    ],
    "Chimie — Sous-domaine 2 : Transformations non totales d'un système chimique (10%)": [
        # Équilibre chimique
        "quotient de réaction", "qr",
        "constante d'équilibre", "k = ", "loi d'action de masse",
        "état d'équilibre", "taux d'avancement final",
        "τ", "tau",
        # Acide-base (réactions non totales)
        "acide-base", "acide base", "ph",
        "ka", "pka", "kb", "pkb",
        "acide fort", "acide faible", "base forte", "base faible",
        "couple acide/base", "dosage acide", "titrage",
        "équivalence", "indicateur coloré",
        "solution aqueuse d'acide", "solution aqueuse d'une base",
        "acide méthanoïque", "acide éthanoïque", "acide propanoïque",
        "méthanoate", "éthanoate", "propanoate", "ammoniac",
    ],
    "Chimie — Sous-domaine 3 : Sens d'évolution d'un système chimique (10%)": [
        "sens d'évolution", "évolution spontanée",
        "critère d'évolution", "sens d'évolution spontanée",
        # Piles / oxydoréduction (sens d'évolution imposé)
        "pile", "piles", "accumulateur",
        "pile daniell", "pile fer-zinc", "pile nickel-argent",
        "anode", "cathode", "oxydoréduction", "oxydation", "réduction",
        "quantité d'électricité",
    ],
    "Chimie — Sous-domaine 4 : Méthode de contrôle de l'évolution des systèmes chimiques (7%)": [
        # Électrolyse (contrôle d'évolution)
        "électrolyse", "électrolyseur", "chromage",
        # Estérification / hydrolyse (contrôle du sens)
        "estérification", "hydrolyse", "ester", "acide carboxylique",
        "rendement", "contrôle du sens", "anhydride d'acide",
        "réaction d'estérification", "réaction d'hydrolyse",
    ],
}

# ─── MATHÉMATIQUES (3 domaines principaux, sous-domaines officiels) ────────
MATH_DOMAINS: dict[str, list[str]] = {
    "Analyse — Suites numériques": [
        "suite numérique", "suite récurrente", "suite",
        "u_{n+1}", "un+1", "u(n+1)",
        "suite arithmétique", "suite géométrique",
        "convergence", "limite d'une suite",
        "raisonnement par récurrence", "récurrence",
        "majoration", "minoration", "monotone", "croissante", "décroissante",
    ],
    "Analyse — Continuité, dérivation et étude de fonctions (inclut log/exp/équations différentielles)": [
        # Continuité / dérivation
        "continuité", "continue sur", "théorème des valeurs intermédiaires",
        "tvi", "bijection", "bijective",
        "dérivée", "dérivation", "dérivable",
        "étude de fonction", "tableau de variation",
        "sens de variation", "extremum", "maximum", "minimum",
        "point d'inflexion", "concavité", "convexité",
        "asymptote", "asymptote verticale", "asymptote horizontale", "asymptote oblique",
        # Logarithme & exponentielle
        "logarithme népérien", "logarithme", "ln(", "ln ",
        "équation logarithmique", "inéquation logarithmique",
        "exponentielle", "exp(", "e^x", "e^(", "fonction exp",
        "équation exponentielle", "limite exponentielle",
        # Équations différentielles (dans ce sous-domaine selon le cadre)
        "équation différentielle", "y' = ay", "y'=ay+b", "y''+ay'+by",
        "solution générale", "condition initiale",
        # Primitives (pont vers calcul intégral mais souvent dans ce sous-domaine)
        "primitive", "primitives",
    ],
    "Analyse — Calcul intégral": [
        "intégrale", "calcul intégral", "calcul d'une intégrale",
        "intégration par parties", "ipp",
        "changement de variable",
        "aire d'un domaine", "aire sous la courbe",
        "volume d'un solide", "solide de révolution",
    ],
    "Algèbre-Géométrie — Produit scalaire et géométrie dans l'espace": [
        "produit scalaire", "produit vectoriel",
        "géométrie dans l'espace", "vecteur normal",
        "équation d'un plan", "équation du plan",
        "équation cartésienne", "représentation paramétrique",
        "plan et droite", "droite orthogonale",
        "sphère", "équation d'une sphère",
        "distance d'un point à un plan", "distance d'un point à une droite",
        "orthogonalité", "vecteurs orthogonaux",
        "aire d'un triangle",
    ],
    "Algèbre-Géométrie — Nombres complexes": [
        "nombre complexe", "nombres complexes",
        "forme algébrique", "forme trigonométrique", "forme exponentielle",
        "module", "argument", "affixe",
        "conjugué", "racine n-ième", "racine carrée complexe",
        "z^2", "az^2 + bz + c",
        "rotation complexe", "translation complexe", "homothétie complexe",
    ],
    "Probabilités — Calcul de probabilités": [
        "probabilité", "probabilités",
        "probabilités conditionnelles", "probabilité conditionnelle",
        "variable aléatoire", "loi de probabilité",
        "loi binomiale", "binomiale",
        "espérance", "variance", "écart-type",
        "événement", "événements indépendants",
        "intersection d'événements", "union d'événements",
        "tirage", "épreuve de bernoulli", "bernoulli",
        "dénombrement", "combinaison", "arrangement",
    ],
}

SUBJECT_DOMAINS: dict[str, dict[str, list[str]]] = {
    "SVT": SVT_DOMAINS,
    "Physique": PHYSIQUE_DOMAINS,
    "Chimie": CHIMIE_DOMAINS,
    "Physique-Chimie": {**PHYSIQUE_DOMAINS, **CHIMIE_DOMAINS},
    "Mathematiques": MATH_DOMAINS,
    "Mathématiques": MATH_DOMAINS,
}


# ─── Poids officiels du cadre (utilisés pour booster les prédictions) ──────
#
#  Les topics à fort poids au BAC doivent recevoir plus d'attention même
#  s'ils ont été testés récemment, et leur absence récente est un très fort
#  signal. Ces poids sont extraits directement des cadres JSON.

OFFICIAL_WEIGHTS: dict[str, dict[str, float]] = {
    "SVT": {
        # Cadre SVT ne donne pas de poids explicites par domaine (chaque
        # examen répartit librement les 20 points). On suppose ~25% chacun.
        "Domaine 1 — Consommation de la matière organique et flux d'énergie": 25.0,
        "Domaine 2 — Information génétique et lois statistiques de transmission": 25.0,
        "Domaine 3 — Utilisation des matières organiques et inorganiques (pollution, déchets, radioactivité)": 25.0,
        "Domaine 4 — Géodynamique interne et formation des chaînes de montagnes": 25.0,
    },
    "Physique": {
        "Physique — Sous-domaine 1 : Ondes (11%)": 11.0,
        "Physique — Sous-domaine 2 : Transformations nucléaires (8%)": 8.0,
        "Physique — Sous-domaine 3 : Électricité (21%)": 21.0,
        "Physique — Sous-domaine 4 : Mécanique (27%)": 27.0,
    },
    "Chimie": {
        "Chimie — Sous-domaine 1 : Transformations rapides et lentes d'un système chimique (6%)": 6.0,
        "Chimie — Sous-domaine 2 : Transformations non totales d'un système chimique (10%)": 10.0,
        "Chimie — Sous-domaine 3 : Sens d'évolution d'un système chimique (10%)": 10.0,
        "Chimie — Sous-domaine 4 : Méthode de contrôle de l'évolution des systèmes chimiques (7%)": 7.0,
    },
    "Mathematiques": {
        # Domaine Analyse : 55% (réparti sur ses 3 sous-domaines)
        "Analyse — Suites numériques": 15.0,
        "Analyse — Continuité, dérivation et étude de fonctions (inclut log/exp/équations différentielles)": 25.0,
        "Analyse — Calcul intégral": 15.0,
        # Algèbre-Géométrie : 15% + 30% = 45%
        "Algèbre-Géométrie — Produit scalaire et géométrie dans l'espace": 15.0,
        "Algèbre-Géométrie — Nombres complexes": 20.0,
        # Probabilités (dans le domaine "Algèbre et géométrie suite") : ~10%
        "Probabilités — Calcul de probabilités": 10.0,
    },
}
# Aliases with accents
OFFICIAL_WEIGHTS["Physique-Chimie"] = {**OFFICIAL_WEIGHTS["Physique"], **OFFICIAL_WEIGHTS["Chimie"]}
OFFICIAL_WEIGHTS["Mathématiques"] = OFFICIAL_WEIGHTS["Mathematiques"]


def _official_weight(subject: str, domain: str) -> float:
    """Return the official cadre weight for a (subject, domain) — 0 if unknown."""
    return OFFICIAL_WEIGHTS.get(subject, {}).get(domain, 0.0)


# ══════════════════════════════════════════════════════════════════════════════
#  FORMAT — comment un topic est testé (SVT spécifique)
# ══════════════════════════════════════════════════════════════════════════════

FORMAT_PART1_RESTITUTION = "part1_restitution"  # QCM + définitions
FORMAT_EX1_PROFOND = "ex1_profond"              # Exercice 1 (≥ 5 pts)
FORMAT_EX2_PROFOND = "ex2_profond"              # Exercice 2 (≥ 6 pts)
FORMAT_EX3_LEGER = "ex3_leger"                  # Exercice 3 (≤ 4 pts)
FORMAT_EX_MEDIUM = "ex_medium"                  # fallback 5 pts


def _classify_format_svt(exercise_name: str, points: float, part_name: str) -> str:
    """Classify an SVT exercise by its pedagogical format (restitution vs raisonnement)."""
    pname = (part_name or "").lower()
    ename = (exercise_name or "").lower()
    if "restitution" in pname or "première partie" in pname or "premiere partie" in pname:
        return FORMAT_PART1_RESTITUTION
    # Part 2 — classify by exercise position and point weight
    if "exercice 1" in ename or "exercice i" in ename:
        return FORMAT_EX1_PROFOND
    if "exercice 2" in ename or "exercice ii" in ename:
        return FORMAT_EX2_PROFOND
    if "exercice 3" in ename or "exercice iii" in ename:
        return FORMAT_EX3_LEGER if points <= 4 else FORMAT_EX_MEDIUM
    if points <= 4:
        return FORMAT_EX3_LEGER
    if points >= 6:
        return FORMAT_EX2_PROFOND
    return FORMAT_EX_MEDIUM


# ══════════════════════════════════════════════════════════════════════════════
#  CLASSIFIEUR — détection de topic via mots-clés
# ══════════════════════════════════════════════════════════════════════════════

def _normalize(text: str) -> str:
    return (text or "").lower()


def _score_domain(text_lc: str, keywords: list[str]) -> tuple[float, list[str]]:
    """Return (score, matched_keywords) for a domain given lowercased text."""
    hits = []
    for kw in keywords:
        if kw in text_lc:
            hits.append(kw)
    # Score = number of distinct matches, with a weight boost for multi-word keywords
    score = sum(1.5 if " " in kw else 1.0 for kw in hits)
    return score, hits


def classify_topic(text: str, subject: str) -> tuple[str, float, list[str]]:
    """Classify the primary topic of an exam text for a given subject.

    Returns (domain_name, confidence_score, matched_keywords). If no domain
    matches, returns ("Non classé", 0.0, []).
    """
    domains = SUBJECT_DOMAINS.get(subject) or SUBJECT_DOMAINS.get(subject.replace("é", "e"))
    if not domains:
        return ("Non classé", 0.0, [])

    text_lc = _normalize(text)
    if not text_lc:
        return ("Non classé", 0.0, [])

    best_name = "Non classé"
    best_score = 0.0
    best_hits: list[str] = []
    for name, keywords in domains.items():
        score, hits = _score_domain(text_lc, keywords)
        if score > best_score:
            best_name, best_score, best_hits = name, score, hits

    return (best_name, best_score, best_hits)


# ══════════════════════════════════════════════════════════════════════════════
#  BUILDER — parcourt data/exams/ et génère l'atlas JSON
# ══════════════════════════════════════════════════════════════════════════════

def _collect_exercise_text(ex: dict) -> str:
    """Flatten all text of an exercise (context + all questions + choices)."""
    parts = [ex.get("context") or "", ex.get("name") or "", ex.get("topic") or ""]
    for q in ex.get("questions") or []:
        parts.append(q.get("content") or "")
        for sq in q.get("sub_questions") or []:
            parts.append(sq.get("content") or "")
            for c in sq.get("choices") or []:
                parts.append(c.get("text") or "")
        for c in q.get("choices") or []:
            parts.append(c.get("text") or "")
    return " ".join(parts)


def _collect_part1_text(part: dict) -> str:
    """Flatten Part 1 (Restitution) text — questions without exercises."""
    parts = [part.get("name") or ""]
    for q in part.get("questions") or []:
        parts.append(q.get("content") or "")
        for sq in q.get("sub_questions") or []:
            parts.append(sq.get("content") or "")
            for c in sq.get("choices") or []:
                parts.append(c.get("text") or "")
    return " ".join(parts)


def _sum_points(items: list[dict]) -> float:
    total = 0.0
    for it in items:
        p = it.get("points")
        if isinstance(p, (int, float)):
            total += p
        for sq in it.get("sub_questions") or []:
            sp = sq.get("points")
            if isinstance(sp, (int, float)):
                total += sp
    return round(total, 2)


def build_atlas() -> dict:
    """Scan backend/data/exams/ and build the full topic coverage atlas."""
    index_path = EXAMS_DIR / "index.json"
    if not index_path.exists():
        _log.error("[Atlas] No index.json found")
        return {}

    with open(index_path, "r", encoding="utf-8") as f:
        catalog = json.load(f)

    atlas: dict = {}  # subject -> years -> session -> {...}

    for meta in catalog:
        exam_file = EXAMS_DIR / meta["path"] / "exam.json"
        if not exam_file.exists():
            continue
        try:
            # Tolerate UTF-8 BOM
            raw_bytes = exam_file.read_bytes()
            if raw_bytes.startswith(b"\xef\xbb\xbf"):
                raw_bytes = raw_bytes[3:]
            raw = json.loads(raw_bytes.decode("utf-8"))
        except Exception as e:
            _log.warning(f"[Atlas] skip {meta['id']}: {e}")
            continue

        subject = meta["subject"]
        year = str(meta["year"])
        session = str(meta["session"]).lower()

        subject_entry = atlas.setdefault(subject, {"years": {}, "domains_seen": set()})
        year_entry = subject_entry["years"].setdefault(year, {})
        session_entry: dict = {
            "exam_id": meta["id"],
            "exam_path": meta["path"],
            "total_points": raw.get("total_points"),
            "duration_minutes": raw.get("duration_minutes"),
            "parts": [],
        }

        # Parse all parts and their exercises/questions
        for part in raw.get("parts") or []:
            part_name = part.get("name") or ""
            part_points = _sum_points(part.get("questions") or [])

            part_data: dict = {
                "name": part_name,
                "points": part.get("points") or part_points,
            }

            # Direct questions under the part (= Part 1 Restitution)
            if part.get("questions"):
                text = _collect_part1_text(part)
                domain, score, hits = classify_topic(text, subject)
                subject_entry["domains_seen"].add(domain)
                part_data["direct_questions"] = {
                    "primary_domain": domain,
                    "match_score": round(score, 2),
                    "keywords_hit": hits[:6],
                    "format": FORMAT_PART1_RESTITUTION if subject == "SVT" else "restitution",
                }

            # Exercises (= Part 2 Raisonnement)
            exercises_out = []
            for ex in part.get("exercises") or []:
                text = _collect_exercise_text(ex)
                domain, score, hits = classify_topic(text, subject)
                subject_entry["domains_seen"].add(domain)
                ex_points = _sum_points(ex.get("questions") or []) or (ex.get("points") or 0)
                fmt = _classify_format_svt(ex.get("name") or "", ex_points, part_name) \
                    if subject == "SVT" else "raisonnement"
                exercises_out.append({
                    "name": ex.get("name", ""),
                    "stated_topic": ex.get("topic") or "",
                    "primary_domain": domain,
                    "match_score": round(score, 2),
                    "keywords_hit": hits[:6],
                    "points": ex_points,
                    "format": fmt,
                })
            part_data["exercises"] = exercises_out
            session_entry["parts"].append(part_data)

        year_entry[session] = session_entry

    # Convert domains_seen sets to sorted lists
    for subject, entry in atlas.items():
        entry["domains_seen"] = sorted(entry["domains_seen"])

    # Build rotation analysis
    for subject, entry in atlas.items():
        entry["rotation"] = _build_rotation_analysis(subject, entry)

    return atlas


def _build_rotation_analysis(subject: str, entry: dict) -> dict:
    """For each domain, compute: years tested, formats used, years since last heavy.

    Output format per domain:
      {
        "total_appearances": 5,
        "years_by_format": {"ex1_profond": [2016, 2019, 2024], ...},
        "last_tested_year": 2024,
        "years_since_last": 1,
        "last_heavy_year": 2019,   # SVT only
        "years_since_heavy": 6,    # SVT only
        "prediction_2026": {"level": "HIGH|MEDIUM|LOW", "reason": "..."}
      }
    """
    domains = SUBJECT_DOMAINS.get(subject) or SUBJECT_DOMAINS.get(subject.replace("é", "e")) or {}
    all_domains = list(domains.keys())

    rotation: dict = {d: {
        "total_appearances": 0,
        "years_by_format": {},
        "years_tested": [],
        "last_tested_year": None,
        "last_heavy_year": None,
    } for d in all_domains}

    # Walk years
    for year, sessions in entry["years"].items():
        yr = int(year)
        for sess, session_data in sessions.items():
            for part in session_data.get("parts") or []:
                # Direct questions (Part 1)
                dq = part.get("direct_questions")
                if dq:
                    d = dq["primary_domain"]
                    if d in rotation:
                        _record_appearance(rotation[d], yr, dq["format"])
                # Exercises (Part 2)
                for ex in part.get("exercises") or []:
                    d = ex["primary_domain"]
                    if d in rotation:
                        _record_appearance(rotation[d], yr, ex["format"])
                        # Track heavy (Ex1/Ex2 profond) for SVT
                        if ex["format"] in (FORMAT_EX1_PROFOND, FORMAT_EX2_PROFOND):
                            cur = rotation[d]["last_heavy_year"]
                            if cur is None or yr > cur:
                                rotation[d]["last_heavy_year"] = yr

    # Compute "years since" metrics + prediction
    all_years = [int(y) for y in entry["years"].keys()]
    latest_exam_year = max(all_years) if all_years else 2025

    for domain, data in rotation.items():
        yrs = sorted(set(data["years_tested"]))
        data["years_tested"] = yrs
        if yrs:
            data["last_tested_year"] = max(yrs)
            data["years_since_last"] = latest_exam_year - max(yrs)
        if data["last_heavy_year"]:
            data["years_since_heavy"] = latest_exam_year - data["last_heavy_year"]
        # Temporarily attach domain name so _predict_2026 can look up the cadre weight
        data["_domain_name"] = domain
        data["prediction_2026"] = _predict_2026(subject, data, latest_exam_year)
        data.pop("_domain_name", None)

    return rotation


def _record_appearance(domain_data: dict, year: int, fmt: str):
    domain_data["total_appearances"] += 1
    domain_data["years_tested"].append(year)
    domain_data["years_by_format"].setdefault(fmt, []).append(year)


def _predict_2026(subject: str, data: dict, latest_year: int) -> dict:
    """Predict the probability a domain appears in BAC 2026.

    SVT logic: every domain appears every year → predict WHICH FORMAT.
    PC/Math logic: predict WHETHER the topic is tested (gap analysis).
    """
    if subject == "SVT":
        # All domains always tested → predict format rotation
        last_heavy = data.get("last_heavy_year")
        last_tested = data.get("last_tested_year")

        if not last_tested:
            return {"level": "MEDIUM", "reason": "Domaine rarement testé, format imprévisible."}

        since_heavy = (latest_year - last_heavy) if last_heavy else 99
        if since_heavy >= 2:
            return {
                "level": "HIGH",
                "format_probable": "ex1_profond / ex2_profond",
                "reason": f"Format profond absent depuis {since_heavy} an(s) (dernier Ex1/Ex2 en {last_heavy}) — forte probabilité de revenir en raisonnement lourd.",
            }
        if since_heavy == 1:
            return {
                "level": "MEDIUM",
                "format_probable": "part1_restitution / ex3_leger",
                "reason": f"Testé en format profond en {last_heavy} — probablement format léger en 2026.",
            }
        return {
            "level": "LOW",
            "format_probable": "part1_restitution",
            "reason": f"Testé en profond très récemment ({last_heavy}) — probable restitution légère en 2026.",
        }

    # Physics/Chem/Math: gap analysis + official cadre weight
    last = data.get("last_tested_year")
    total = data.get("total_appearances", 0)
    # Retrieve official weight via the domain name (stored in parent context)
    domain_name = data.get("_domain_name", "")
    weight = _official_weight(subject, domain_name)
    weight_tag = f" [poids cadre {weight:.0f}%]" if weight else ""

    if not last:
        return {
            "level": "HIGH",
            "reason": f"Jamais détecté dans l'échantillon 2016-2025{weight_tag} — candidat très probable pour 2026.",
            "cadre_weight_pct": weight,
        }
    gap = latest_year - last

    # A high-weight topic absent for 2+ years = guaranteed HIGH
    if weight >= 15 and gap >= 2:
        return {
            "level": "HIGH",
            "reason": f"Poids cadre élevé ({weight:.0f}%) + absent depuis {gap} an(s) (dernière apparition {last}) — candidat très fort pour 2026.",
            "cadre_weight_pct": weight,
        }
    if gap >= 3:
        return {
            "level": "HIGH",
            "reason": f"Absent depuis {gap} an(s) (dernière apparition {last}){weight_tag} — forte probabilité 2026.",
            "cadre_weight_pct": weight,
        }
    if gap == 2:
        return {
            "level": "MEDIUM",
            "reason": f"Absent depuis 2 ans{weight_tag} — candidat sérieux.",
            "cadre_weight_pct": weight,
        }
    # High weight + tested recently → still MEDIUM (it recurs every year)
    if weight >= 20 and gap <= 1:
        return {
            "level": "MEDIUM",
            "reason": f"Poids cadre très élevé ({weight:.0f}%) et testé en {last} — récurrent chaque année, à maîtriser absolument.",
            "cadre_weight_pct": weight,
        }
    if total >= 5 and gap <= 1:
        return {
            "level": "LOW",
            "reason": f"Testé très régulièrement ({total} fois) et encore en {last}{weight_tag} — moins prioritaire mais à maîtriser.",
            "cadre_weight_pct": weight,
        }
    return {
        "level": "MEDIUM",
        "reason": f"Testé en {last} (il y a {gap} an){weight_tag} — toujours possible.",
        "cadre_weight_pct": weight,
    }


# ══════════════════════════════════════════════════════════════════════════════
#  SERVICE — API d'accès à l'atlas
# ══════════════════════════════════════════════════════════════════════════════

class TopicAtlasService:
    def __init__(self):
        self._atlas: Optional[dict] = None

    def _ensure_loaded(self) -> dict:
        if self._atlas is not None:
            return self._atlas
        if ATLAS_PATH.exists():
            try:
                with open(ATLAS_PATH, "r", encoding="utf-8") as f:
                    self._atlas = json.load(f)
                return self._atlas
            except Exception as e:
                _log.warning(f"[Atlas] Failed to load {ATLAS_PATH}: {e}")
        _log.info("[Atlas] No cached atlas, building from scratch…")
        self._atlas = build_atlas()
        self.save()
        return self._atlas

    def save(self):
        if self._atlas is None:
            return
        ATLAS_PATH.parent.mkdir(parents=True, exist_ok=True)
        with open(ATLAS_PATH, "w", encoding="utf-8") as f:
            json.dump(self._atlas, f, ensure_ascii=False, indent=2)
        _log.info(f"[Atlas] Saved to {ATLAS_PATH}")

    def rebuild(self) -> dict:
        """Force a full rebuild from the exam JSON files."""
        self._atlas = build_atlas()
        self.save()
        return self._atlas

    # ── Query API ────────────────────────────────────────────────────────────

    def get_subject_atlas(self, subject: str) -> dict:
        """Return the full atlas entry for one subject (years + rotation)."""
        atlas = self._ensure_loaded()
        return atlas.get(subject, {}) or atlas.get(subject.replace("é", "e"), {})

    def get_rotation(self, subject: str) -> dict:
        """Return {domain: rotation_data} for a subject."""
        return self.get_subject_atlas(subject).get("rotation", {})

    def get_topics_by_year(self, subject: str, year: str | int) -> dict:
        """Return per-session breakdown for a given year+subject."""
        return self.get_subject_atlas(subject).get("years", {}).get(str(year), {})

    def get_topics_not_tested_recently(
        self, subject: str, min_gap_years: int = 2
    ) -> list[dict]:
        """Return domains whose last appearance is at least `min_gap_years` ago.

        Only relevant for PC/Math (gap analysis). For SVT, every domain appears
        every year — use `get_svt_format_predictions()` instead.
        """
        rotation = self.get_rotation(subject)
        out = []
        for domain, data in rotation.items():
            last = data.get("last_tested_year")
            if last is None:
                out.append({"domain": domain, "last": None, "gap": 99, "prediction": data.get("prediction_2026")})
                continue
            gap = data.get("years_since_last", 0)
            if gap >= min_gap_years:
                out.append({
                    "domain": domain,
                    "last": last,
                    "gap": gap,
                    "prediction": data.get("prediction_2026"),
                    "total_appearances": data.get("total_appearances", 0),
                })
        out.sort(key=lambda x: (x["gap"] is not None, x.get("gap", 0)), reverse=True)
        return out

    def get_svt_format_predictions(self) -> dict:
        """For each SVT domain, predict its format for 2026."""
        rotation = self.get_rotation("SVT")
        return {
            d: data.get("prediction_2026", {})
            for d, data in rotation.items()
        }

    def predict_2026_priorities(self, subject: str) -> dict:
        """Return HIGH / MEDIUM / LOW priority lists for BAC 2026.

        Output: {"HIGH": [...], "MEDIUM": [...], "LOW": [...], "total_time_split": {...}}
        Used to drive the 50/30/20 rule in study plans and prompts.
        """
        rotation = self.get_rotation(subject)
        buckets: dict[str, list[dict]] = {"HIGH": [], "MEDIUM": [], "LOW": []}
        for domain, data in rotation.items():
            pred = data.get("prediction_2026") or {}
            level = pred.get("level") or "MEDIUM"
            buckets.setdefault(level, []).append({
                "domain": domain,
                "reason": pred.get("reason", ""),
                "format_probable": pred.get("format_probable"),
                "last_tested": data.get("last_tested_year"),
                "total_appearances": data.get("total_appearances", 0),
            })
        # Sort each bucket by total_appearances desc (most established first)
        for k in buckets:
            buckets[k].sort(key=lambda x: x["total_appearances"], reverse=True)
        return {
            "HIGH": buckets["HIGH"],
            "MEDIUM": buckets["MEDIUM"],
            "LOW": buckets["LOW"],
            "time_split_rule": {"HIGH": "50%", "MEDIUM": "30%", "LOW": "20%"},
            "balance_principle": (
                "Prioriser HIGH sans jamais négliger LOW : toute matière "
                "doit recevoir au minimum 20% du temps de révision."
            ),
        }

    def build_historical_context_for_prompt(
        self, subject: str, max_years: int = 5
    ) -> str:
        """Return a compact text block injectable in LLM prompts.

        Includes: recent topic coverage + 2026 predictions + balance rule.
        """
        sub = self.get_subject_atlas(subject)
        if not sub:
            return ""

        years = sub.get("years", {})
        recent_years = sorted(years.keys(), reverse=True)[:max_years]
        priorities = self.predict_2026_priorities(subject)

        lines = [
            f"═══ HISTORIQUE BAC {subject.upper()} (dernières {len(recent_years)} années) ═══",
        ]
        for yr in recent_years:
            for sess, data in years[yr].items():
                topics_this_exam = []
                for part in data.get("parts") or []:
                    if dq := part.get("direct_questions"):
                        topics_this_exam.append(f"P1:{dq['primary_domain']}")
                    for ex in part.get("exercises") or []:
                        nm = ex.get("name", "Ex?").replace("Exercice ", "E")
                        topics_this_exam.append(f"{nm}({int(ex.get('points',0))}p):{ex['primary_domain']}")
                lines.append(f"  {yr} {sess}: {' | '.join(topics_this_exam)}")

        lines.append("")
        lines.append(f"═══ PRÉDICTIONS BAC 2026 pour {subject.upper()} (basées sur la rotation historique) ═══")

        for level, label in [("HIGH", "🔴 HAUTE priorité (50% du temps)"),
                             ("MEDIUM", "🟠 MOYENNE priorité (30%)"),
                             ("LOW", "🟢 Couverture minimale (20%, à NE PAS négliger)")]:
            items = priorities.get(level) or []
            if not items:
                continue
            lines.append(f"\n{label}:")
            for it in items[:5]:
                extra = f" [format probable: {it['format_probable']}]" if it.get("format_probable") else ""
                lines.append(f"  • {it['domain']}{extra}")
                if it.get("reason"):
                    lines.append(f"      → {it['reason']}")

        lines.append("")
        lines.append(
            "⚖️ RÈGLE D'ÉQUILIBRE : prioriser HIGH+MEDIUM mais GARANTIR 20% min pour LOW. "
            "Aucun domaine ne doit être ignoré — tout peut tomber au BAC."
        )
        return "\n".join(lines)


# Singleton
topic_atlas = TopicAtlasService()
