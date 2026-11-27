"""Construit le cours de référence SVT à partir de cours_diapos.py et cours_questions.py.

    python -I scripts/reference/construire_cours.py

Écrit :
  backend/data/courses/svt_ch1_reference_consommation_mo.json   (le cours, mode concentration, brouillon)
  docs/reference-svt/voix_a_generer.json                         (toutes les pistes à mettre en voix)
et imprime les contrôles : chaque `mot` est un extrait exact du texte dit, aucun passage de plus de 40 mots sans
geste, nombre de mots par diapositive, premiers mots.
"""
from __future__ import annotations

import collections
import copy
import json
import re
import sys
from pathlib import Path

ICI = Path(__file__).resolve().parent
RACINE = ICI.parents[1]
sys.path.insert(0, str(ICI))
import cours_diapos as CD  # noqa: E402
import cours_questions as CQ  # noqa: E402

DECK = "svt_ch1_reference_consommation_mo"
SORTIE = RACINE / "backend/data/courses" / f"{DECK}.json"
VOIX = RACINE / "docs/reference-svt/voix_a_generer.json"
MODELE = RACINE / "backend/data/courses/en_attente/svt_ch1_reactions_responsables_liberation_energie.json"

BALISE = re.compile(r"<([mrc]):([^>]*)>")
PONCT = "،,:.!؟?;"
alertes: list[str] = []


def mots(t):
    return re.findall(r"\S+", t or "")


def gestes(ident, brut):
    """Retire les balises ; rend (texte, pointage, centre, positions des gestes)."""
    texte, marques, fin = "", [], 0
    for m in BALISE.finditer(brut):
        texte += brut[fin:m.start()]
        marques.append((len(texte), m.group(1), m.group(2)))
        fin = m.end()
    texte += brut[fin:]
    assert "<" not in texte and ">" not in texte, ident
    assert "  " not in texte, f"{ident} : double espace"
    pointage, centre, positions = [], [], []
    for pos, genre, val in marques:
        suite = mots(texte[pos:])
        assert texte[pos] != " ", f"{ident} : balise suivie d'une espace ({val})"
        mot = None
        for k in range(2, 9):
            cand = " ".join(suite[:k]).rstrip(PONCT)
            # le texte garde ses espaces simples : l'extrait se retrouve tel quel
            if cand and texte.find(cand) == pos:
                mot = cand
                break
        if mot is None:
            alertes.append(f"{ident} : pas d'extrait unique pour {genre}:{val} à « {' '.join(suite[:5])} »")
            mot = " ".join(suite[:4])
        positions.append(pos)
        if genre == "c":
            centre.append({"texte": val, "mot": mot})
        elif genre == "r":
            pointage.append({"mot": mot, "repere": val})
        else:
            moment, _, duree = val.partition(":")
            par = {"moment": moment}
            if duree:
                par["duree_s"] = float(duree)
            pointage.append({"mot": mot, "commande": "play_until", "parametres": par})
    return texte, pointage, centre, positions


# ───────────────────────── Figures du cahier ─────────────────────────

def chaine(x0, y, n, pas=0.62, r=0.26):
    return [{"f": "cercle", "c": [round(x0 + i * pas, 2), y], "r": r, "remplir": "jaune", "couleur": "jaune"}
            for i in range(n)]


def figures():
    modele = json.loads(MODELE.read_text(encoding="utf-8"))
    mito = next(s for a in modele["activities"] for s in a["slides"] if s["id"] == "le_m2_legender")
    fig_mito = copy.deepcopy(mito["concentration"]["cahier_figures"][0])
    fig_mito["titre"] = "La mitochondrie en coupe"
    fig_mito["legende"] = ("Deux membranes séparées par l'espace intermembranaire ; la membrane interne forme des "
                           "crêtes, qui portent les sphères pédonculées ; au centre, la matrice.")
    voyage = {
        "type": "schema", "titre": "La carte du voyage du glucose",
        "legende": "La glycolyse est commune ; ensuite, le dioxygène décide de la route de l'acide pyruvique.",
        "cadre": {"l": 10, "h": 6.4},
        "elements": chaine(3.45, 5.8, 6) + [
            {"f": "texte", "at": [7.3, 5.8], "t": "glucose (6 C)", "ancre": "gauche", "couleur": "jaune"},
            {"f": "fleche", "de": [5, 5.4], "a": [5, 4.25], "texte": "glycolyse (hyaloplasme)", "pos": "e"},
        ] + chaine(4.38, 3.85, 3) + [
            {"f": "texte", "at": [3.9, 3.85], "t": "2 ×", "ancre": "droite", "couleur": "jaune"},
            {"f": "texte", "at": [6.2, 3.85], "t": "acide pyruvique (3 C)", "ancre": "gauche", "couleur": "jaune"},
            {"f": "fleche", "de": [4.0, 3.4], "a": [2.4, 2.2], "texte": "avec O₂", "pos": "o"},
            {"f": "fleche", "de": [6.0, 3.4], "a": [7.6, 2.2], "texte": "sans O₂", "pos": "e"},
            {"f": "ellipse", "c": [2.2, 1.5], "rx": 1.7, "ry": 0.62, "couleur": "orange"},
            {"f": "texte", "at": [2.2, 1.5], "t": "mitochondrie", "couleur": "orange"},
            {"f": "texte", "at": [2.2, 0.4], "t": "CO₂ : respiration", "couleur": "vert"},
            {"f": "texte", "at": [7.7, 1.6], "t": "éthanol + CO₂", "couleur": "rose"},
            {"f": "texte", "at": [7.7, 0.4], "t": "fermentation", "couleur": "vert"},
        ]}
    glyco = {
        "type": "schema", "titre": "Les trois phases de la glycolyse",
        "legende": "2 ATP consommés, puis 4 ATP formés : la glycolyse fait gagner 2 ATP, et réduit 2 NAD⁺.",
        "cadre": {"l": 10, "h": 6.6},
        "elements": [
            {"f": "rect", "de": [0.2, 4.6], "a": [9.8, 6.4], "couleur": "faible", "arrondi": True},
            {"f": "texte", "at": [0.45, 6.05], "t": "1. Activation", "ancre": "gauche", "couleur": "jaune"},
            {"f": "texte", "at": [0.45, 5.15], "t": "glucose (C6) → fructose diphosphate (P-C6-P)", "ancre": "gauche"},
            {"f": "texte", "at": [9.55, 6.05], "t": "− 2 ATP", "ancre": "droite", "couleur": "rose"},
            {"f": "rect", "de": [0.2, 2.4], "a": [9.8, 4.2], "couleur": "faible", "arrondi": True},
            {"f": "texte", "at": [0.45, 3.85], "t": "2. Scission", "ancre": "gauche", "couleur": "jaune"},
            {"f": "texte", "at": [0.45, 2.95], "t": "P-C6-P → 2 C3-P → 2 P-C3-P", "ancre": "gauche"},
            {"f": "texte", "at": [9.55, 3.85], "t": "2 NADH,H⁺", "ancre": "droite", "couleur": "cyan"},
            {"f": "rect", "de": [0.2, 0.2], "a": [9.8, 2.0], "couleur": "faible", "arrondi": True},
            {"f": "texte", "at": [0.45, 1.65], "t": "3. Formation d'énergie", "ancre": "gauche", "couleur": "jaune"},
            {"f": "texte", "at": [0.45, 0.75], "t": "2 P-C3-P → 2 acides pyruviques (C3)", "ancre": "gauche"},
            {"f": "texte", "at": [9.55, 1.65], "t": "+ 4 ATP", "ancre": "droite", "couleur": "vert"},
        ]}
    return {"voyage": voyage, "glycolyse": glyco, "mitochondrie": fig_mito}


FIG_DIAPO = {"rf_a3_voyage1": "voyage", "rf_g4_bilan": "glycolyse", "rf_m3_legender": "mitochondrie"}

ACTIVITES = [
    ("rf_ouverture", "Ouverture — une question et trois rappels", "situation", 0, 5),
    ("rf_activite1", "I. Activité 1 : mettre en évidence la respiration et la fermentation", "explanation", 5, 14),
    ("rf_activite1_suite", "I (suite). Où se passe chaque réaction, et que devient le glucose ?", "explanation", 14, 23),
    ("rf_activite2", "II. Activité 2 : la glycolyse", "explanation", 23, 29),
    ("rf_activite3", "III. Activité 3 : la mitochondrie, siège de la respiration", "explanation", 29, 38),
    ("rf_bilan", "Bilan du chapitre", "synthesis", 38, 41),
]


def construire():
    figs = figures()
    slides, positions_par_diapo = [], {}
    for d in CD.D:
        i = d["id"]
        texte, pointage, centre, pos = gestes(i, d["mx"])
        s = {"id": i, "slide_type": d["type"], "title": d["titre"],
             "screen_content": {"lead": d["lead"], "bullets": d.get("bullets", []),
                                "student_trace": d["cahier"].replace("\n", " ")}}
        if d.get("page"):
            s["visual"] = {"kind": "simulation", "url": d["page"], "caption": d.get("legende", d["titre"]),
                           "alt": d.get("alt", "")}
        else:
            s["visual"] = {"kind": "none"}
        s["speech_text"] = {"fr": d["fr"], "mixed": texte}
        c = {}
        if d.get("page"):
            c["demarrer"] = "reset"
        if pointage:
            c["pointage"] = pointage
        if centre:
            c["centre"] = centre
        c["cahier"] = d["cahier"]
        if i in FIG_DIAPO:
            c["cahier_figures"] = [figs[FIG_DIAPO[i]]]
        if d.get("acquis"):
            c["acquis"] = True
        if d.get("obs"):
            o = CQ.OBS[d["obs"]]
            assert texte.count(o["apres_mot"]) == 1, f"{i} : apres_mot absent ou répété"
            pos.append(texte.find(o["apres_mot"]))
            c["observation"] = o
        c["reponses"] = {}
        if d.get("question"):
            if d["question"] in CQ.ASSOCIATION:
                s["question"] = CQ.ASSOCIATION[d["question"]]
            else:
                q, rep = CQ.Q[d["question"]]
                s["question"] = q
                c["reponses"] = {"q": rep}
                demo = q.get("demonstration")
                if demo:
                    for l in demo["lignes"]:
                        assert l["mot"] in demo["parole"], f"{i} : ligne de démonstration « {l['mot']} »"
        if d.get("legende_eleve"):
            c["legende"] = {"reactions": CQ.LEGENDE}
            c["variante"] = {"apres_s": 5, "etapes": [{"commande": "set_parameters", "parametres": {"corrige": True}},
                                                      {"repere": "medaillon"}]}
        s["concentration"] = c
        s["competence_ids"] = d.get("comp", [])
        if d.get("demarche"):
            s["demarche"] = {"etape": d["demarche"], "nom": CD.DEMARCHE[d["demarche"]]}
        if d.get("etoile"):
            s["notion_importante"] = True
        s["ce_que_montre_l_animation"] = d["montre"]
        if d.get("ouverture"):
            s["ouverture_cours"] = True
        if d.get("fermeture"):
            s["fermeture_cours"] = True
        slides.append(s)
        positions_par_diapo[i] = sorted(pos)

    activites = [{"id": a, "stable_id": a, "title": t, "phase": ph, "duration_minutes": 2 * (f - de),
                  "slides": slides[de:f]} for a, t, ph, de, f in ACTIVITES]

    competences = []
    for comp in CQ.COMPETENCES:
        c = dict(comp)
        c["slide_ids"] = [s["id"] for s in slides if comp["id"] in s["competence_ids"]]
        competences.append({k: c[k] for k in ("id", "label", "slide_ids", "cadre_ids", "dit", "rappels")})

    seances = copy.deepcopy(CQ.SEANCES)
    vus = []
    for se in seances:
        for b in se["blocs"]:
            vus += b["slide_ids"]
            if "cahier_figures" in b:
                b["cahier_figures"] = [figs[n] for n in b["cahier_figures"]]
    assert vus == [s["id"] for s in slides], "chaque diapositive dans un bloc, dans l'ordre"

    deck = {
        "id": DECK, "stable_id": DECK,
        "title": "Consommation de la matière organique et flux d'énergie",
        "version": 1, "status": "draft", "language": "mixed", "mode": "concentration",
        "subject": "svt", "niveau": "2ᵉ Bac PC BIOF", "estimated_minutes": 100,
        "lesson_match": [],
        "catalog": {
            "summary": "Cours de référence, en mode concentration : le voyage d'une molécule de glucose, de la cuve "
                       "de levures jusqu'à la matrice de la mitochondrie — respiration et fermentation mises en "
                       "évidence par ExAO, glycolyse en trois phases, mitochondrie isolée, légendée et analysée.",
            "essential_topics": [
                "C₆H₁₂O₆ + 6 O₂ → 6 CO₂ + 6 H₂O + énergie", "C₆H₁₂O₆ → 2 C₂H₅OH + 2 CO₂ + énergie",
                "Glycolyse : 2 acides pyruviques, 2 ATP, 2 NADH,H⁺ (hyaloplasme)",
                "La mitochondrie utilise l'acide pyruvique, pas le glucose",
                "Ultrastructure et composition de la mitochondrie"],
        },
        "note": "Cours de référence SVT pour l'inspecteur (27 novembre 2026). Contrat : "
                "docs/reference-svt/ARCHITECTURE.md. Généré par scripts/reference/construire_cours.py à partir de "
                "cours_diapos.py et cours_questions.py : modifier ces fichiers, puis relancer le générateur. "
                "Brouillon (lien libre seulement) ; aucune voix générée : pistes dans "
                "docs/reference-svt/voix_a_generer.json. Cadre officiel : domaine 1, sous-domaine 1.1 (réactions "
                "responsables de la libération de l'énergie emmagasinée dans la matière organique).",
        "activities": activites, "competences": competences, "seances": seances,
    }
    return deck, positions_par_diapo


# ───────────────────────── Pistes de voix ─────────────────────────

def pistes(deck):
    out = []

    def p(typ, dossier, ident, texte):
        out.append({"type": typ, "dossier": dossier, "id": ident, "texte": texte})

    def reactions(prefixe, rep):
        for o, qr in (rep or {}).items():
            for quoi, r in qr.items():
                p("reaction", "reponses", f"{prefixe}_{o}_{quoi}", r["parole"])

    for a in deck["activities"]:
        for s in a["slides"]:
            i = s["id"]
            p("diapositive", "mixed", i, s["speech_text"]["mixed"])
            q = s.get("question") or {}
            if q.get("enonce_dit"):
                p("enonce", "reponses", f"enonce_{i}_q", q["enonce_dit"])
            reactions(f"{i}__q", s["concentration"].get("reponses", {}).get("q"))
            if q.get("demonstration"):
                p("demonstration", "demos", f"{i}__demo_q", q["demonstration"]["parole"])
            asso = q.get("association")
            if asso:
                for k, r in asso["retours"].items():
                    p("association", "reponses", f"{i}__q_assoc_{k.replace('*', 'autre')}", r["dit"])
                p("association", "reponses", f"{i}__q_assoc_bilan", asso["bilan"]["dit"])
            for k, r in ((s["concentration"].get("legende") or {}).get("reactions") or {}).items():
                p("legende", "reponses", f"{i}__legende_{k}", r["parole"])
            o = s["concentration"].get("observation")
            if o:
                p("observation", "observations", f"enonce_obs_{i}_q", o["enonce_dit"])
                for k, ind in enumerate(o["indices"]):
                    p("indice", "observations", f"enonce_obs_{i}_i{k}", ind["dit"])
                for k, r in enumerate(o["retours"]):
                    p("observation", "observations", f"enonce_obs_{i}_r{k}", r["parole"])
                p("observation", "observations", f"enonce_obs_{i}_s", o["solution"]["parole"])
    for c in deck["competences"]:
        for r in c["rappels"]:
            p("rappel", "reponses", f"enonce_rappel_{r['id']}", r["enonce_dit"])
            reactions(f"rappel_{r['id']}", r.get("reponses"))
    for se in deck["seances"]:
        for b in se["blocs"]:
            if b.get("retrouver"):
                p("bloc", "reponses", f"enonce_bloc_{b['id']}_retrouver", b["retrouver"]["enonce_dit"])
            ex = b.get("exercice")
            if ex:
                p("bloc", "reponses", f"enonce_bloc_{b['id']}_exercice", ex["enonce_dit"])
                reactions(f"bloc_{b['id']}__ex", ex["reponses"])
    return out


# ───────────────────────── Contrôles ─────────────────────────

def controles(deck, positions):
    slides = [s for a in deck["activities"] for s in a["slides"]]
    print(f"{len(slides)} diapositives, {sum(len(se['blocs']) for se in deck['seances'])} blocs, "
          f"{len(deck['seances'])} séances, {len(deck['competences'])} compétences")
    longs, premiers, avant = [], collections.Counter(), None
    for s in slides:
        t = s["speech_text"]["mixed"]
        c = s["concentration"]
        for g in (c.get("pointage") or []) + (c.get("centre") or []):
            if g["mot"] not in t:
                alertes.append(f"{s['id']} : mot introuvable « {g['mot']} »")
        ordre = [t.find(g["mot"]) for g in c.get("pointage") or []]
        if ordre != sorted(ordre):
            alertes.append(f"{s['id']} : pointage dans le désordre")
        bornes = [0] + positions[s["id"]] + [len(t)]
        trou = max(len(mots(t[bornes[k]:bornes[k + 1]])) for k in range(len(bornes) - 1))
        if trou > 40:
            alertes.append(f"{s['id']} : {trou} mots sans geste")
        n = len(mots(t))
        if not 50 <= n <= 110:
            longs.append((s["id"], n))
        if re.search(r"\d", t) or re.search(r"[₀-₉⁰-⁹→+=%]", t):
            alertes.append(f"{s['id']} : chiffre ou symbole dans le texte dit")
        w = mots(t)[0].strip(PONCT)
        premiers[w] += 1
        if w == avant:
            alertes.append(f"{s['id']} : même premier mot que la diapositive d'avant (« {w} »)")
        avant = w
    print("mots par diapo : min", min(len(mots(s["speech_text"]["mixed"])) for s in slides),
          "max", max(len(mots(s["speech_text"]["mixed"])) for s in slides),
          "moyenne", round(sum(len(mots(s["speech_text"]["mixed"])) for s in slides) / len(slides)))
    if longs:
        print("hors 50–110 mots :", longs)
    print("premiers mots les plus fréquents :", premiers.most_common(4))
    # paroles : ni chiffre ni symbole
    for p in pistes(deck):
        if re.search(r"\d", p["texte"]) or re.search(r"[₀-₉⁰-⁹→+=%×−]", p["texte"]):
            alertes.append(f"piste {p['id']} : chiffre ou symbole dans le texte dit")
    for a in alertes:
        print("ALERTE", a)
    return not alertes


def main():
    deck, positions = construire()
    ok = controles(deck, positions)
    SORTIE.write_text(json.dumps(deck, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    liste = pistes(deck)
    VOIX.parent.mkdir(parents=True, exist_ok=True)
    VOIX.write_text(json.dumps({
        "deck": DECK,
        "_note": "Toutes les pistes du cours de référence (backend/data/courses/" + DECK + ".json), à mettre en voix "
                 "Bodi : aucune n'existe encore. Chaque texte est exactement celui du champ du cours. Les pistes de "
                 "type « bloc » (retrouver et exercice de fin de bloc) ne sont pas jouées aujourd'hui "
                 "(FIN_DE_BLOC_COMPLETE = False) : à générer en dernier. Fichier écrit par "
                 "scripts/reference/construire_cours.py.",
        "pistes": liste}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(len(liste), "pistes :", dict(collections.Counter(p["type"] for p in liste)))
    print("écrit :", SORTIE.relative_to(RACINE), "et", VOIX.relative_to(RACINE))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
