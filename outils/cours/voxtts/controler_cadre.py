"""Second contrôle d'un script de cours : reste-t-il dans le cadre de référence de l'examen national (2ᵉ Bac PC) ?

  python controler_cadre.py <cours.json> <chapitre>      (ex. ondes_mecaniques)

Vérifie, d'après backend/data/curriculum/cadre_reference_2bac_pc.json :
  1. chaque compétence du cours (`deck.competences[].cadre_ids`) vise au moins une capacité du cadre, et chaque
     capacité du cadre est visée par au moins une compétence (sinon le cours a un trou) ;
  2. chaque formule écrite dans le cours (texte contenant « = », hors parole et réactions) est une formule du cadre
     ou une application numérique de l'une d'elles ; une écriture inconnue est signalée pour relecture ;
  3. aucun mot hors cadre n'apparaît dans l'écrit (titres, contenu, questions, exercices, formules au centre,
     cahier) ni dans la voix (`speech_text.*`), sauf ceux tolérés quand ils sont annoncés comme « plus tard » ;
  4. la lecture des formules dans la voix suit l'écriture du cadre (`dit`).
Code de sortie 1 s'il y a une faute (manque ou hors cadre) ; les simples « à relire » ne bloquent pas.
Skill : cours-concentration, étape 8 (second contrôle), et professeur, règle 8 (périmètre).
"""
import json
import re
import sys
from pathlib import Path

CADRE = Path(r"backend/data/curriculum/cadre_reference_2bac_pc.json")
CHAMPS_ECRITS = ("title", "lead", "bullets", "essential_text", "student_trace", "caption", "table", "question", "exercises", "concentration", "label")


def textes_ecrits(o, cle=None):
    """Tous les textes écrits (pas la parole, pas les réactions préparées, pas les identifiants)."""
    if isinstance(o, dict):
        for k, v in o.items():
            if k in ("speech_text", "reponses", "audio", "visual", "id", "stable_id", "url", "mot", "repere", "commande", "parametres", "moment", "cible", "competence_ids", "cadre_ids", "slide_ids", "note", "_note"):
                continue
            yield from textes_ecrits(v, k)
    elif isinstance(o, list):
        for v in o:
            yield from textes_ecrits(v, cle)
    elif isinstance(o, str) and cle not in ("type", "kind", "status", "language", "phase"):
        yield o


def normaliser(f):
    return re.sub(r"\s+", "", f).replace("×", "·").replace("*", "·").replace("Δt", "Δt").lower()


def main(cours_p, chapitre):
    cadre = json.loads(CADRE.read_text(encoding="utf-8"))["chapitres"][chapitre]
    m = json.loads(Path(cours_p).read_text(encoding="utf-8"))
    fautes, relire = [], []

    # 1. compétences ↔ capacités
    caps = {c["id"] for c in cadre["capacites"]}
    visees = set()
    for c in m.get("competences") or []:
        ids = set(c.get("cadre_ids") or [])
        if not ids:
            fautes.append(f"compétence {c['id']} « {c['label'][:50]} » : aucune capacité du cadre (cadre_ids)")
        if ids - caps:
            fautes.append(f"compétence {c['id']} : capacité inconnue {sorted(ids - caps)}")
        visees |= ids & caps
    for cap in caps - visees:
        fautes.append(f"capacité du cadre non travaillée : {cap}")

    # 2. formules écrites : on retire du texte chaque formule du cadre (et ses variantes) ; ce qui reste avec un
    #    « = » et autre chose qu'un nombre à droite est une écriture inconnue, à relire.
    connues = [f["ecriture"] for f in cadre["formules"]] + [v for f in cadre["formules"] for v in f.get("variantes_admises", [])]
    connues_n = [normaliser(c) for c in connues]
    for t in textes_ecrits(m):
        if "=" not in t:
            continue
        reste = normaliser(t)
        for c in sorted(connues_n, key=len, reverse=True):
            reste = reste.replace(c, " ")
        for form in re.findall(r"[a-zτθδλ0-9_()·/-]{1,24}=[^=,;]{1,30}", reste):
            droite = form.split("=", 1)[1]
            if re.match(r"^[\s(]*[\d]", droite) or droite.startswith("f(") or "enfonctionde" in droite:
                continue       # application numérique, ou « Δt = f(d) »
            relire.append(f"formule inconnue du cadre : « {form.strip()} » dans « {t[:70]} »")

    # 3. hors cadre
    hors = cadre["hors_cadre"]["mots"]
    tolere = set(cadre["hors_cadre"].get("tolere_si_annonce", []))
    annonce = re.compile(r"plus tard|viendra|prochain|غادي تجي|من بعد|chapitre suivant|périodiques", re.I)
    for t in list(textes_ecrits(m)) + [p for a in m["activities"] for s in a["slides"] for p in (s.get("speech_text") or {}).values()]:
        for mot in hors:
            if mot.lower() in t.lower():
                if mot in tolere and annonce.search(t):
                    continue
                fautes.append(f"hors cadre « {mot} » dans : « {t[:90]} »")

    # 4. lecture des formules dans la voix : « <racine> égale … » doit être l'une des lectures du cadre.
    par_racine = {}
    for f in cadre["formules"]:
        racine = f["dit"].split(" égale")[0]
        par_racine.setdefault(racine, []).append(f["dit"])
    for a in m["activities"]:
        for s in a["slides"]:
            dit = (s.get("speech_text") or {}).get("mixed", "")
            for racine, lectures in par_racine.items():
                for occ in re.finditer(rf"(?<![\w]){re.escape(racine)} égale ([^.،,؟?]*)", dit):
                    suite = occ.group(1).strip()
                    if re.match(r"^(un|une|deux|trois|quatre|cinq|six|sept|huit|neuf|dix|onze|douze|quinze|vingt|trente|quarante|cinquante|soixante|zéro|cent|mille)", suite):
                        continue       # application numérique dite en lettres
                    autour = dit[max(0, occ.start() - 8):occ.end()]
                    if not any(l in autour for l in lectures):
                        relire.append(f"{s['id']} : la voix lit « {occ.group(0)[:60]} », pas une lecture du cadre")

    for x in sorted(set(relire)):
        print("À RELIRE :", x)
    for x in fautes:
        print("FAUTE    :", x)
    print("cadre : OK" if not fautes else f"cadre : {len(fautes)} faute(s)", f"; {len(set(relire))} point(s) à relire")
    sys.exit(1 if fautes else 0)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main(sys.argv[1], sys.argv[2])
