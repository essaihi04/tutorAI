"""Le dossier du cours de référence SVT, pour l'inspecteur (docs/reference-svt/ARCHITECTURE.md, § 8).

    python -I scripts/reference/dossier_inspecteur.py

Lit backend/data/courses/svt_ch1_reference_consommation_mo.json et écrit un seul fichier autonome, sobre et
imprimable : frontend/public/media/simulations/svt/reference_consommation_mo-tableau/dossier.html
(fiche pédagogique, correspondance avec le diaporama du professeur, puis chaque diapositive : étape de la démarche,
ce que montre l'animation, texte dit en français et en darija, piste audio quand elle existe, question, réactions,
lignes du cahier). À relancer après chaque changement du cours ou après la pose des voix.
"""
from __future__ import annotations

import html
import json
import sys
from pathlib import Path

RACINE = Path(__file__).resolve().parents[2]
DECK = "svt_ch1_reference_consommation_mo"
COURS = RACINE / "backend/data/courses" / f"{DECK}.json"
SORTIE = RACINE / "frontend/public/media/simulations/svt/reference_consommation_mo-tableau/dossier.html"
LIEN = f"/cours-ondes/?cours={DECK}"

# Diaporama du professeur (parties 1 et 2) → nos diapositives
CORRESPONDANCE = [
    ("Introduction : la matière organique, source d'énergie de la cellule",
     ["rf_ouverture_cours", "rf_o1_pate", "rf_r1_cellule", "rf_r2_glucose", "rf_r3_levure"],
     "Situation de départ concrète (la pâte à pain) et trois rappels enseignés depuis zéro."),
    ("Partie 1, activité 1 — Mise en évidence de la respiration et de la fermentation (ExAO, levures)",
     ["rf_a1_montage", "rf_a1_exp1_avant", "rf_a1_exp1_injection", "rf_a1_exp1_deduire", "rf_a1_equation_respi",
      "rf_a1_exp2_axes", "rf_a1_exp2_phase1", "rf_a1_exp2_phase2", "rf_a1_equation_ferm"],
     "Chaque document est joué : le montage, puis la courbe qui se trace en même temps que le phénomène dans la cuve."),
    ("Partie 1, activité 1 — Localisation : deux levures au microscope électronique ; tableau comparatif",
     ["rf_a2_deux_levures", "rf_a2_localisation", "rf_a2_tableau", "rf_a2_definitions"],
     "Le tableau du professeur est construit ligne par ligne ; les définitions sont construites par trois questions."),
    ("Partie 1, activité 1 — Devenir du glucose : glucose marqué au ¹⁴C ; schéma bilan",
     ["rf_a3_marquage", "rf_a3_glycolyse", "rf_a3_sans_o2", "rf_a3_avec_o2", "rf_a3_voyage1"],
     "Le tableau T0…T5 devient une animation, puis redevient le tableau du document ; le schéma bilan est la « carte du voyage »."),
    ("Partie 2, activité 2 — Les phases de la glycolyse et son bilan",
     ["rf_g0_atp", "rf_g0_taxi", "rf_g1_activation", "rf_g2_scission", "rf_g3_oxydation", "rf_g4_bilan"],
     "Deux rappels (ATP, transporteur d'hydrogène) placés juste avant leur usage, puis une phase par diapositive."),
    ("Partie 2, activité 3 — La mitochondrie : centrifugation fractionnée, mitochondries isolées (ExAO)",
     ["rf_m1_principe", "rf_m1_etapes", "rf_m2_glucose", "rf_m2_pyruvate"],
     "Le principe d'abord, puis les étapes ; le résultat décisif est trouvé par l'élève."),
    ("Partie 2, activité 3 — Ultrastructure et composition de la mitochondrie",
     ["rf_m3_zoom", "rf_m3_legender", "rf_m3_construire", "rf_m4_membranes", "rf_m4_matrice"],
     "Les électronographies sont recréées en zoom animé ; l'élève légende lui-même le schéma."),
    ("Bilan",
     ["rf_b1_bilan", "rf_b2_voyage", "rf_fermeture_cours"],
     "Fiche « Ce qu'il faut retenir », carte complète, conseils de révision."),
]

CSS = """
:root{--encre:#1f2937;--gris:#6b7280;--trait:#d1d5db;--fond:#f9fafb;--accent:#0f766e}
*{box-sizing:border-box}
body{margin:0;background:#fff;color:var(--encre);font:15px/1.55 Georgia,'Times New Roman',serif}
main{max-width:920px;margin:0 auto;padding:28px 20px 60px}
h1{font-size:26px;margin:0 0 4px}h2{font-size:20px;margin:34px 0 10px;border-bottom:2px solid var(--accent);padding-bottom:4px}
h3{font-size:17px;margin:0 0 6px}h4{font-size:13px;margin:12px 0 3px;color:var(--accent);text-transform:uppercase;letter-spacing:.04em;font-family:system-ui,sans-serif}
p{margin:4px 0}.sous{color:var(--gris);margin:0 0 14px}
table{border-collapse:collapse;width:100%;margin:8px 0;font-size:14px}
th,td{border:1px solid var(--trait);padding:6px 8px;text-align:left;vertical-align:top}th{background:var(--fond)}
.diapo{border:1px solid var(--trait);border-radius:6px;padding:14px 16px;margin:16px 0;break-inside:avoid-page}
.entete{display:flex;gap:10px;align-items:baseline;flex-wrap:wrap}
.num{font:700 13px system-ui,sans-serif;color:#fff;background:var(--accent);border-radius:4px;padding:1px 7px}
.pastille{font:12px system-ui,sans-serif;border:1px solid var(--accent);color:var(--accent);border-radius:10px;padding:0 8px}
.etoile{font:12px system-ui,sans-serif;background:#fef3c7;border:1px solid #f59e0b;border-radius:10px;padding:0 8px}
.ar{direction:rtl;text-align:right;font:16px/1.9 'Noto Naskh Arabic','Amiri','Segoe UI',Tahoma,sans-serif;background:var(--fond);padding:8px 10px;border-radius:4px}
.fr{background:var(--fond);padding:8px 10px;border-radius:4px}
.cahier{border-left:3px solid var(--accent);padding:2px 10px;white-space:pre-line}
.petit{font-size:13px;color:var(--gris)}audio{width:100%;margin:6px 0}
ul{margin:4px 0 4px 20px;padding:0}li{margin:2px 0}
.juste{color:#047857;font-weight:700}a{color:var(--accent)}
.sommaire{columns:2;font-size:14px}
@media print{main{max-width:none;padding:0}.diapo{border-color:#999}a{color:inherit;text-decoration:none}audio{display:none}h2{break-after:avoid}}
@media(max-width:640px){.sommaire{columns:1}}
"""


def e(t):
    return html.escape(str(t or ""))


def gestes(c):
    moments = [g["parametres"]["moment"] for g in c.get("pointage", []) if g.get("commande")]
    reperes = [g["repere"] for g in c.get("pointage", []) if g.get("repere")]
    out = []
    if moments:
        out.append(f"{len(moments)} moments joués sur les mots de la voix")
    if reperes:
        out.append(f"{len(reperes)} objets montrés à la baguette")
    if c.get("centre"):
        out.append(f"{len(c['centre'])} carte(s) écrite(s) au mot qui les dit")
    return " · ".join(out)


def reactions(rep, options, correct):
    l = ["<ul>"]
    for i, o in enumerate(options):
        r = rep.get(str(i), {})
        if i == correct:
            l.append(f"<li><span class='juste'>✔ {e(o)}</span><br>{e(r.get('juste', {}).get('ecrit'))}</li>")
        else:
            l.append(f"<li>✘ {e(o)}<br><span class='petit'>1er essai (indice, sans la réponse) :</span> "
                     f"{e(r.get('1', {}).get('ecrit'))}<br><span class='petit'>2e essai (la réponse) :</span> "
                     f"{e(r.get('2', {}).get('ecrit'))}</li>")
    l.append("</ul>")
    return "".join(l)


def bloc_diapo(n, s):
    c = s.get("concentration", {})
    l = [f"<section class='diapo' id='{e(s['id'])}'><div class='entete'><span class='num'>{n}</span>"
         f"<h3>{e(s['title'])}</h3>"]
    if s.get("demarche"):
        l.append(f"<span class='pastille'>Démarche : {e(s['demarche']['nom'])}</span>")
    if s.get("notion_importante"):
        l.append("<span class='etoile'>★ notion importante : annoncée, dite, redite, relue</span>")
    l.append("</div>")
    l.append(f"<p class='sous'>{e(s['screen_content'].get('lead'))}</p>")
    l.append(f"<h4>Ce que montre l'animation</h4><p>{e(s.get('ce_que_montre_l_animation'))}</p>")
    v = s.get("visual", {})
    if v.get("url"):
        l.append(f"<p class='petit'>Page : <a href='{e(v['url'])}'>{e(v['url'].split('/')[-1])}</a> — {e(gestes(c))}</p>")
    l.append(f"<h4>Texte dit — français</h4><p class='fr'>{e(s['speech_text']['fr'])}</p>")
    l.append(f"<h4>Texte dit — darija et français (la voix du cours)</h4><p class='ar' lang='ar'>{e(s['speech_text']['mixed'])}</p>")
    audio = ((s.get("audio") or {}).get("mixed") or {}).get("url")
    l.append(f"<audio controls preload='none' src='{e(audio)}'></audio>" if audio
             else "<p class='petit'>Piste audio : à générer (voix du cours).</p>")
    o = c.get("observation")
    if o:
        l.append(f"<h4>Question d'observation (la voix s'arrête, l'élève cherche)</h4><p><b>{e(o['enonce'])}</b></p>")
        l.append("<p class='petit'>Indices après chaque silence : " + " — ".join(e(i["texte"]) for i in o["indices"]) + "</p><ul>")
        for i, ch in enumerate(o["choix"]):
            cls = "juste" if i == o["bonne"] else ""
            l.append(f"<li><span class='{cls}'>{'✔' if i == o['bonne'] else '✘'} {e(ch)}</span><br>{e(o['retours'][i]['ecrit'])}</li>")
        l.append("</ul>")
    q = s.get("question")
    if q:
        l.append(f"<h4>Question du bloc</h4><p><b>{e(q['prompt'])}</b></p>")
        if q.get("association"):
            a = q["association"]
            l.append("<table><tr><th>À relier</th><th>Réponse attendue</th><th>Retour</th></tr>")
            droite = {d["id"]: d["texte"] for d in a["droite"]}
            for g in a["gauche"]:
                d = a["couples"][g["id"]]
                l.append(f"<tr><td>{e(g['id'])}. {e(g['texte'])}</td><td>{e(d)}. {e(droite[d])}</td>"
                         f"<td>{e(a['retours'][g['id'] + '-' + d]['texte'])}<br><span class='petit'>Si erreur : "
                         f"{e(a['retours'][g['id'] + '-*']['texte'])}</span></td></tr>")
            l.append("</table>")
        else:
            l.append(reactions(c.get("reponses", {}).get("q", {}), q["options"], q["correct"]))
        if q.get("demonstration"):
            l.append("<p class='petit'>Démonstration jouée sur la figure, ligne par ligne :</p><ul>"
                     + "".join(f"<li>{e(x['texte'])}</li>" for x in q["demonstration"]["lignes"]) + "</ul>")
    if c.get("legende"):
        l.append("<h4>Schéma à légender par l'élève</h4><ul>"
                 + "".join(f"<li>{e(k)} : {e(r['ecrit'])}</li>" for k, r in c["legende"]["reactions"].items()) + "</ul>")
    if c.get("cahier"):
        l.append(f"<h4>Dans le cahier</h4><p class='cahier'>{e(c['cahier'])}</p>")
        if c.get("cahier_figures"):
            l.append("<p class='petit'>Avec le dessin : " + " ; ".join(e(f["titre"]) for f in c["cahier_figures"]) + ".</p>")
    l.append("</section>")
    return "".join(l)


def main():
    d = json.loads(COURS.read_text(encoding="utf-8"))
    slides = [s for a in d["activities"] for s in a["slides"]]
    num = {s["id"]: i + 1 for i, s in enumerate(slides)}
    titre = {s["id"]: s["title"] for s in slides}
    nq = sum(1 for s in slides if s.get("question"))
    nobs = sum(1 for s in slides if s["concentration"].get("observation"))
    voix = sum(1 for s in slides if (s.get("audio") or {}).get("mixed"))
    h = [f"<!doctype html><html lang='fr'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'>"
         f"<title>Dossier du cours — {e(d['title'])}</title><style>{CSS}</style></head><body><main>"]
    h.append(f"<h1>{e(d['title'])}</h1><p class='sous'>Dossier du cours de référence — SVT, {e(d.get('niveau'))} — "
             f"<a href='{LIEN}'>ouvrir le cours</a></p>")
    h.append("<h2>1. Fiche pédagogique</h2><table>")
    fiche = [
        ("Niveau", "2ᵉ année du baccalauréat, sciences physiques, option française (BIOF)"),
        ("Place dans le programme", "Domaine 1 : consommation de la matière organique et flux d'énergie — sous-domaine 1.1 : "
         "réactions responsables de la libération de l'énergie emmagasinée dans la matière organique (25 % de la note au national pour le domaine)"),
        ("Contenu", "Parties 1 et 2 du chapitre réunies : mise en évidence de la respiration et de la fermentation, "
         "localisation, devenir du glucose, glycolyse, mitochondrie (isolement, ultrastructure, composition)"),
        ("Durée", f"5 séances, 11 blocs, {len(slides)} diapositives (environ {d.get('estimated_minutes', 100)} minutes de cours, hors temps d'écriture)"),
        ("Prérequis (enseignés dans le cours, jamais supposés)", "La cellule et ses organites ; le glucose, matière organique ; "
         "la levure ; l'ATP ; le transporteur d'hydrogène NAD⁺"),
        ("Objectifs", "<ul>" + "".join(f"<li>{e(c['id'])} — {e(c['label'])}</li>" for c in d["competences"]) + "</ul>"),
        ("Démarche", "Démarche d'investigation, visible sur chaque page (fil en haut à droite) : problème → hypothèse → "
         "expérience → résultats → analyse → conclusion. Devant chaque courbe : lire les axes, décrire avec les valeurs, puis déduire."),
        ("Supports", "Animations peintes pilotées par la voix (aucune image de manuel) : montage ExAO, courbes tracées en "
         "même temps que le phénomène, modèles moléculaires, centrifugeuse, zooms de microscopie, schéma à légender"),
        ("Langue", "Explication en darija simple ; termes du programme, nombres, unités et formules en français ; "
         "tout ce que l'élève écrit (cahier, questions, réponses) est en français"),
        ("Évaluation", f"{nq} questions de bloc et {nobs} questions d'observation (le résultat est trouvé par l'élève), chaque "
         "réponse possible ayant sa réaction préparée ; un schéma à légender ; rappels espacés par compétence (J+1, J+3, J+7, J+21)"),
        ("Trace écrite", "Le cahier de l'élève, étape obligatoire à la fin de chaque bloc : plan I, II, III, définitions "
         "encadrées, trois équations, tableau comparatif, trois schémas"),
    ]
    for k, v in fiche:
        h.append(f"<tr><th style='width:26%'>{e(k)}</th><td>{v if v.startswith('<ul>') else e(v)}</td></tr>")
    h.append("</table>")
    h.append("<h2>2. Du diaporama du professeur à nos diapositives</h2><table><tr><th>Diaporama du professeur</th>"
             "<th>Nos diapositives</th><th>Ce qui change</th></tr>")
    for partie, ids, note in CORRESPONDANCE:
        liens = "<br>".join(f"<a href='#{i}'>{num[i]}. {e(titre[i])}</a>" for i in ids)
        h.append(f"<tr><td>{e(partie)}</td><td>{liens}</td><td>{e(note)}</td></tr>")
    h.append("</table>")
    h.append("<h2>3. Le cahier de l'élève, bloc par bloc</h2>")
    for se in d["seances"]:
        h.append(f"<h3>{e(se['titre'])}</h3>")
        for b in se["blocs"]:
            lignes = "\n".join(x["texte"] for x in b["cahier"])
            h.append(f"<p><b>{e(b['titre'])}</b> <span class='petit'>(diapositives {num[b['slide_ids'][0]]} à "
                     f"{num[b['slide_ids'][-1]]})</span></p><p class='cahier'>{e(lignes)}</p>")
            if b.get("cahier_figures"):
                h.append("<p class='petit'>Dessin : " + " ; ".join(e(f["titre"]) for f in b["cahier_figures"]) + ".</p>")
            if b.get("retrouver"):
                h.append(f"<p class='petit'>À retrouver de mémoire : {e(b['retrouver']['prompt'])} → {e(b['retrouver']['attendu'])}</p>")
    h.append(f"<h2>4. Les {len(slides)} diapositives</h2><p class='petit'>Pistes audio posées : {voix} sur {len(slides)}.</p>"
             "<div class='sommaire'>" + "".join(f"<div><a href='#{s['id']}'>{num[s['id']]}. {e(s['title'])}</a></div>" for s in slides) + "</div>")
    for a in d["activities"]:
        h.append(f"<h2>{e(a['title'])}</h2>")
        for s in a["slides"]:
            h.append(bloc_diapo(num[s["id"]], s))
    h.append("<h2>5. Les rappels espacés, par compétence</h2><table><tr><th>Compétence</th><th>Questions de rappel</th></tr>")
    for c in d["competences"]:
        h.append(f"<tr><td>{e(c['id'])} — {e(c['label'])}</td><td><ul>"
                 + "".join(f"<li>{e(r['prompt'])}</li>" for r in c["rappels"]) + "</ul></td></tr>")
    h.append("</table></main></body></html>")
    SORTIE.parent.mkdir(parents=True, exist_ok=True)
    SORTIE.write_text("".join(h) + "\n", encoding="utf-8")
    print("écrit :", SORTIE.relative_to(RACINE), f"({SORTIE.stat().st_size // 1024} Ko, {len(slides)} diapositives, {voix} pistes audio)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
