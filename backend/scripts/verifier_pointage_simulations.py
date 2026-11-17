"""Contrôle voix ↔ simulation d'un cours « au tableau » (17 novembre 2026).

Règle du professeur : ce que dit le tuteur, la simulation le montre au même instant ; la baguette (`highlight`)
se pose sur l'objet nommé dans la phrase, jamais sur un autre ; un processus décrit sans animation est un défaut.

Pour chaque diapositive à simulation, le script liste chaque entrée de `concentration.pointage` :
l'instant estimé dans la voix (même calcul que le lecteur : place du mot dans le texte parlé, rapportée à la durée
de la piste ; une commande part 0,9 s plus tôt), le morceau de phrase, les objets qu'il nomme (lexique ci-dessous)
et la commande ou le repère visé. Il signale :
  - REPERE   la baguette vise un repère que le morceau de phrase ne nomme pas (ou un repère inconnu du lexique) ;
  - PROCESSUS une phrase décrit un processus animé (lexique `PROCESSUS`) sans `play_until` vers un des moments
             attendus dans cette phrase ;
  - MOMENT   un `play_until` vise un moment absent du code de la simulation ;
  - IFRAME   deux diapositives de suite ont la même URL de simulation (l'iframe n'est pas rechargée : la scène de la
             diapositive précédente reste, souvent finie, et les `play_until` sont refusés) ;
  - DEPART   une diapositive pilotée par des `play_until` démarre la scène avec `start` (elle court seule, sans la voix) ;
  - GESTE    un geste qui part plus de 0,6 s après son mot (le tuteur fait un geste par seconde : trop serrés, ils prennent du retard).

Usage : python backend/scripts/verifier_pointage_simulations.py [chemin du cours] [--diapo ID] [--ecarts]
Sortie non nulle s'il reste des écarts (utilisé par backend/app/tests/test_pointage_simulations.py).
"""
from __future__ import annotations

import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from urllib.parse import parse_qs, urlparse

RACINE = Path(__file__).resolve().parents[2]
PUBLIC = RACINE / "frontend" / "public"
COURS_DEFAUT = RACINE / "backend" / "data" / "courses" / "svt_ch1_reactions_responsables_liberation_energie.json"
AVANCE_COMMANDE = 0.9   # CourseFocusStage.tsx : une commande part un peu avant le mot
GESTE_S = 1.0            # CourseFocusStage.tsx : un geste à la fois, une seconde chacun

# ── Lexique : pour chaque simulation, les mots qui nomment chaque repère (voix « mixed » : darija + français) ──
# Un repère sans entrée est accepté s'il est nommé par son identifiant (« sphere » → « sphère »…) ; mieux vaut le décrire.
ECRIT = r"كنكتبو|نكتبو|كتكتب|نكونو|نعاود نقرا|سميتو|سميتها|نسميو|écrit|définition|la réaction|l'équation|le bilan"
LEXIQUE: dict[str, dict[str, str]] = {
    "chaine.html": {
        "mitochondrie_zoom": r"mitochondrie|الصغيرة|المربع",
        "membrane": r"membrane|la bande",
        "matrice": r"matrice",
        "espace": r"espace|الفوق",
        "t1": r"(?<![A-Za-z])[TC] un\b|premier transporteur",
        "t2": r"(?<![A-Za-z])[TC] deux\b",
        "t3": r"(?<![A-Za-z])[TC] trois\b",
        "t4": r"(?<![A-Za-z])[TC] quatre\b|سد",
        "transporteurs": r"transporteurs?\b",
        "taxi": r"N A D H|NADH|N A D plus|NAD\+|taxi|R H deux|transporteurs? réduits?|le transporteur est oxydé|F A D H|ورجع خاوي",
        "electrons": r"électrons?|وتجمعو من اللور",
        "protons": r"protons?|H plus",
        "protons_matrice": r"protons?|H plus|التحت قلال",
        "o2": r"dioxygène|O deux|demi O",
        "poignee_o2": r"نحيدو le dioxygène|بلا dioxygène|sans dioxygène",
        "eau": r"l'eau|H2O|molécule d'eau",
        "atp": r"ATP|ADP|phosphate",
        "sphere": r"sphères?|C cinq",
        "equation": ECRIT + r"|بالflèches|accepteur|gradient|phosphorylation",
        "ecrit_taxi_eq": ECRIT + r"|H plus est oxydé",
        "ecrit_relais": ECRIT + r"|réactions d'oxydoréduction",
        "ecrit_eau_eq": ECRIT + r"|un demi O deux",
        "ecrit_bilan_fadh": r"ATP|كيعطي trois",
        "ecrit_accepteur": r"accepteur",
        "ecrit_gradient": r"gradient",
        "ecrit_atp_eq": r"phosphorylation|" + ECRIT,
        "ecrit_chaine_causale": ECRIT + r"|بالflèches",
        "schema": r"schéma",
        "structures": r"الأرقام|structures|من un حتى",
        "reactions": r"الحروف|réactions",
        "etiquettes": r"étiquettes",
        "legende": r"légende",
    },
}
# Processus décrits par la voix → moments qui les montrent (au moins un `play_until` vers l'un d'eux dans la phrase).
PROCESSUS: dict[str, list[tuple[str, list[str]]]] = {
    "chaine.html": [
        (r"جا N A D H|NADH,H\+ arrive", ["taxi_arrive"]),
        (r"طيح deux protons", ["taxi_decharge", "entree_fadh2"]),
        (r"ورجع خاوي، N A D plus", ["nad_repart"]),
        (r"كيدوزو من T un|ل T deux", ["e_t2", "e_t3", "electrons_passent"]),
        (r"وفاللخر ل T quatre", ["electrons_passent"]),
        (r"كاين le dioxygène", ["o2_arrive"]),
        (r"خدا deux électrons", ["o2_recoit"]),
        (r"وتكون l'eau", ["eau_formee"]),
        (r"un demi O deux, deux protons et deux électrons donnent", ["equation_eau"]),
        (r"accepteur final", ["o2_accepteur"]),
        (r"les électrons بقاو", ["sans_o2_arret", "bloque"]),
        (r"des protons كيطلعو", ["protons_pompes"]),
        (r"تجمعو بزاف ديال les protons", ["espace_charge"]),
        (r"سميتو le gradient", ["gradient_ecrit"]),
        (r"les protons كيهبطو", ["retour_par_la_sphere"]),
        (r"ولاو ATP", ["atp_forme"]),
        (r"N A D H, H plus est oxydé", ["equation_nadh"]),
        (r"سد T quatre", ["cyanure_pose", "bloque"]),
        (r"ما بقاش كياخد les électrons", ["o2_non"]),
        (r"ما بقاش le pompage", ["pas_d_atp"]),
        (r"شوف الأرقام", ["structures"]),
        (r"وشوف الحروف", ["reactions"]),
        (r"دابا les réponses", ["solution"]),
        (r"F A D H deux كيعطي", ["entree_fadh2"]),
        (r"كيعطي deux ATP", ["bilan_fadh2"]),
    ],
}
FIN_PHRASE = re.compile(r"[.!?؟]")


@dataclass
class Ligne:
    diapo: str
    t: float
    mot: str
    morceau: str
    nommes: list[str]
    action: str
    ecart: str = ""


@dataclass
class Rapport:
    lignes: list[Ligne] = field(default_factory=list)
    ecarts: list[str] = field(default_factory=list)


def fichier_sim(url: str) -> str:
    return Path(urlparse(url).path).name


def source_sim(url: str) -> str:
    chemin = PUBLIC / urlparse(url).path.lstrip("/")
    try:
        return chemin.read_text(encoding="utf-8")
    except OSError:
        return ""


def nommes_dans(texte: str, lexique: dict[str, str]) -> list[str]:
    out = []
    for rep, motif in lexique.items():
        m = re.search(motif, texte, re.I)
        if m:
            out.append((m.start(), rep))
    return [r for _, r in sorted(out)]


def bornes_phrase(parole: str, i: int) -> tuple[int, int]:
    debut = 0
    for m in FIN_PHRASE.finditer(parole, 0, i):
        debut = m.end()
    m = FIN_PHRASE.search(parole, i)
    return debut, (m.end() if m else len(parole))


def verifier(cours: dict, seule: str | None = None) -> Rapport:
    r = Rapport()
    precedente = None
    for act in cours.get("activities", []):  # noqa: C901 (un seul parcours, lisible de haut en bas)
        for s in act.get("slides", []):
            vis = s.get("visual") or {}
            url = vis.get("url") or ""
            conc = s.get("concentration") or {}
            simu = vis.get("kind") == "simulation" and "-tableau/" in url
            if seule and s["id"] != seule:
                precedente = url if simu else None
                continue
            if not simu:
                precedente = None
                continue
            nom = fichier_sim(url)
            lexique = LEXIQUE.get(nom, {})
            parole = ((s.get("speech_text") or {}).get("mixed") or "").strip()
            duree = ((s.get("audio") or {}).get("mixed") or {}).get("duration_ms", 0) / 1000
            pointage = conc.get("pointage") or []
            code = source_sim(url)
            if precedente == url:
                r.ecarts.append(f"{s['id']} IFRAME même URL que la diapositive précédente ({url}) : la scène n'est pas rechargée")
            precedente = url
            if conc.get("demarrer") == "start" and any(p.get("commande") == "play_until" for p in pointage):
                r.ecarts.append(f"{s['id']} DEPART demarrer=start : la scène court seule ; ouvrir figée (?depart=…) et demarrer=reset")
            instants = []
            for p in pointage:
                mot = p.get("mot", "")
                i = parole.find(mot)
                t = max(0.0, (i / max(1, len(parole))) * duree - 0.3 - (AVANCE_COMMANDE if p.get("commande") else 0)) if i >= 0 else -1
                instants.append(t)
                deb, fin = bornes_phrase(parole, max(0, i + len(mot) - 1))
                # le morceau qui accompagne le geste : du mot jusqu'au mot du geste suivant ou à la fin de la phrase
                suivants = [parole.find(q.get("mot", ""), i + 1) for q in pointage if q is not p]
                suivants = [j for j in suivants if j > i]
                fin_morceau = min([fin] + [j for j in suivants if j < fin]) if i >= 0 else 0
                morceau = parole[i:max(fin_morceau, i + len(mot))] if i >= 0 else ""
                nommes = nommes_dans(morceau, lexique)
                if p.get("commande"):
                    action = f"{p['commande']} {json.dumps(p.get('parametres') or {}, ensure_ascii=False)}"
                else:
                    action = f"highlight {p.get('repere') or p.get('cible')}"
                ligne = Ligne(s["id"], t, mot, morceau.strip(), nommes, action)
                if i < 0:
                    ligne.ecart = "mot introuvable dans la voix"
                elif p.get("repere"):
                    rep = p["repere"]
                    if lexique and rep not in lexique:
                        ligne.ecart = f"repère « {rep} » absent du lexique"
                    elif lexique and rep not in nommes:
                        ligne.ecart = f"REPERE la baguette va sur « {rep} », la phrase nomme {nommes or 'rien du lexique'}"
                    if code and not re.search(r"['\"`]" + re.escape(rep) + r"['\"`]|'t' \+ \(k \+ 1\)|'ecrit_' \+", code):
                        ligne.ecart = (ligne.ecart + " ; " if ligne.ecart else "") + f"repère « {rep} » introuvable dans {nom}"
                elif p.get("commande") == "play_until":
                    m = (p.get("parametres") or {}).get("moment")
                    if m and code and not re.search(r"\b" + re.escape(m) + r"\b", code):
                        ligne.ecart = f"MOMENT « {m} » introuvable dans {nom}"
                if ligne.ecart:
                    r.ecarts.append(f"{s['id']} {ligne.ecart} — « {ligne.morceau[:70]} »")
                r.lignes.append(ligne)
            # gestes en file : le tuteur fait un geste par seconde ; un geste qui arrive plus de 0,6 s après son mot est en retard
            prochain = -1e9
            for t, p in sorted(((t, p) for t, p in zip(instants, pointage) if t >= 0), key=lambda x: x[0]):
                eff = max(t, prochain)
                prochain = eff + GESTE_S
                mot_t = t + (AVANCE_COMMANDE if p.get("commande") else 0)
                if eff - mot_t > 0.6:
                    r.ecarts.append(f"{s['id']} GESTE « {p.get('mot')} » part à {eff:.1f} s, {eff - mot_t:.1f} s après son mot (gestes trop serrés)")
            # processus dits sans animation
            for motif, moments in PROCESSUS.get(nom, []):
                for m in re.finditer(motif, parole):
                    deb, fin = bornes_phrase(parole, m.start())
                    deb = bornes_phrase(parole, max(0, deb - 2))[0]   # la commande peut partir avec la phrase d'avant
                    ok = False
                    for p in pointage:
                        j = parole.find(p.get("mot", ""))
                        if p.get("commande") == "play_until" and (p.get("parametres") or {}).get("moment") in moments and deb - 1 <= j < fin:
                            ok = True
                    if not ok:
                        r.ecarts.append(f"{s['id']} PROCESSUS « {m.group()} » sans play_until vers {moments} dans la phrase « {parole[deb:fin].strip()[:70]} »")
    return r


def main(argv: list[str]) -> int:
    chemin = COURS_DEFAUT
    seule = None
    juste_ecarts = "--ecarts" in argv
    args = [a for a in argv if a != "--ecarts"]
    if "--diapo" in args:
        k = args.index("--diapo")
        seule = args[k + 1]
        del args[k:k + 2]
    if args:
        chemin = Path(args[0])
    cours = json.loads(chemin.read_text(encoding="utf-8"))
    r = verifier(cours, seule)
    if not juste_ecarts:
        diapo = None
        for l in r.lignes:
            if l.diapo != diapo:
                diapo = l.diapo
                print(f"\n== {diapo}")
            drapeau = "  ✗ " + l.ecart if l.ecart else ""
            print(f"  {l.t:5.1f}s  {l.action:<48} | nomme {','.join(l.nommes) or '—':<28} | « {l.morceau[:60]} »{drapeau}")
    print(f"\n{len(r.ecarts)} écart(s)")
    for e in r.ecarts:
        print("  -", e)
    return 1 if r.ecarts else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
