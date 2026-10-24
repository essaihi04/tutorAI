"""Le périmètre du programme : jusqu'où le tuteur a le droit d'aller.

Les garde-fous existants disent au modèle de refuser un SUJET hors programme
(matrices, équations de Maxwell). Ils ne disent rien du NIVEAU à l'intérieur
d'un chapitre au programme : rien n'empêche d'expliquer le dipôle RC avec une
transformée de Laplace, ou le RLC avec une impédance complexe. Pour un élève
du bac, c'est pire qu'un refus — il croit qu'il devait le savoir.

Deux outils, tous deux déterministes, nourris par `data/curriculum/perimetre.json` :

* **avant** que le modèle parle, un bloc court injecté dans le prompt : les
  notions du chapitre, les méthodes autorisées, les termes à ne pas employer
  et ce qu'on dit à la place ;
* **après**, un détecteur qui relit la réponse et note chaque terme hors
  programme employé. En observation d'abord : on journalise, on compte, on
  ne corrige pas encore. Les listes se stabilisent sur des réponses réelles
  avant qu'on leur donne le droit de bloquer quoi que ce soit.

Un chapitre absent du fichier n'a pas de périmètre : rien n'est injecté ni
détecté. Mieux vaut un silence qu'une liste inventée.
"""
from __future__ import annotations

import json
import os
import re
import unicodedata
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import Optional

from app.services.prerequis import _matiere

CHEMIN = Path(__file__).resolve().parent.parent.parent / "data" / "curriculum" / "perimetre.json"
#: Déplaçable par PERIMETRE_JOURNAL_PATH, comme le journal du mode libre : les
#: tests écrivent dans un dossier jetable, jamais dans data/.
JOURNAL = Path(os.environ.get("PERIMETRE_JOURNAL_PATH") or
               Path(__file__).resolve().parent.parent.parent / "data" / "perimetre_journal.jsonl")


@dataclass(frozen=True)
class TermeHorsProgramme:
    terme: str
    motif: re.Pattern
    dire_plutot: str
    #: "" pour un terme valable sur toute la matière, sinon l'identifiant du chapitre.
    chapitre: str = ""


@dataclass(frozen=True)
class Fiche:
    chapitre: str
    nom: str
    source: str
    notions: tuple[str, ...]
    termes_programme: tuple[str, ...]
    termes_hors_programme: tuple[TermeHorsProgramme, ...]
    methodes_autorisees: tuple[str, ...]
    demonstrations_attendues: tuple[str, ...]
    demonstrations_admises: tuple[str, ...]
    niveau: str


@dataclass(frozen=True)
class Detection:
    terme: str
    extrait: str
    dire_plutot: str
    chapitre: str


def _normaliser(texte: str) -> str:
    """Minuscules sans accents : « Impédance » et « impedance » sont le même mot."""
    texte = unicodedata.normalize("NFD", texte or "")
    return "".join(c for c in texte if unicodedata.category(c) != "Mn").lower()


def _compiler(motif: str) -> re.Pattern:
    # Les motifs sont écrits avec accents facultatifs ([ée]) ; on les applique
    # au texte normalisé, donc on les normalise aussi.
    return re.compile(_normaliser(motif), re.IGNORECASE)


def _termes(brut: list[dict], chapitre: str = "") -> tuple[TermeHorsProgramme, ...]:
    out = []
    for t in brut:
        if not str(t.get("terme", "")).strip() or not str(t.get("motif", "")).strip():
            raise ValueError(f"perimetre.json : terme hors programme incomplet ({chapitre or 'matière'}) : {t}")
        out.append(TermeHorsProgramme(t["terme"], _compiler(t["motif"]), t.get("dire_plutot", "hors programme"), chapitre))
    return tuple(out)


@lru_cache(maxsize=1)
def charger(chemin: Path = CHEMIN) -> dict:
    """matière → {"generiques": termes, "fiches": {chapitre: Fiche}}. Une entrée
    mal formée fait échouer le chargement."""
    brut = json.loads(chemin.read_text(encoding="utf-8"))
    carte: dict[str, dict] = {}
    for matiere, bloc in brut["matieres"].items():
        fiches: dict[str, Fiche] = {}
        for chapitre, f in bloc.get("chapitres", {}).items():
            for champ in ("nom", "source", "notions", "methodes_autorisees"):
                if not f.get(champ):
                    raise ValueError(f"perimetre.json : champ « {champ} » vide pour {matiere}/{chapitre}")
            demos = f.get("demonstrations", {})
            fiches[chapitre] = Fiche(
                chapitre=chapitre, nom=f["nom"], source=f["source"], notions=tuple(f["notions"]),
                termes_programme=tuple(f.get("termes_programme", ())),
                termes_hors_programme=_termes(f.get("termes_hors_programme", []), chapitre),
                methodes_autorisees=tuple(f["methodes_autorisees"]),
                demonstrations_attendues=tuple(demos.get("attendues", ())),
                demonstrations_admises=tuple(demos.get("admises", ())),
                niveau=str(f.get("niveau", "")),
            )
        carte[matiere] = {"generiques": _termes(bloc.get("termes_hors_programme", [])), "fiches": fiches}
    return carte


def fiche(subject: str, chapitre: Optional[str], carte: Optional[dict] = None) -> Optional[Fiche]:
    carte = carte or charger()
    matiere = _matiere(subject)
    if matiere is None or not chapitre:
        return None
    return carte.get(matiere, {}).get("fiches", {}).get(chapitre)


def bloc_prompt(subject: str, chapitre: Optional[str], carte: Optional[dict] = None) -> str:
    """Ce que le modèle lit avant de parler : court, impératif, sourcé."""
    f = fiche(subject, chapitre, carte)
    if f is None:
        return ""
    carte = carte or charger()
    generiques = carte[_matiere(subject)]["generiques"]
    hors = [t for t in list(f.termes_hors_programme) + list(generiques)]
    lignes = [
        f"\n\n[PÉRIMÈTRE DU PROGRAMME — {f.nom}] ({f.source})",
        "Reste dans ce périmètre : un terme ou une méthode qui n'y figure pas n'aide pas l'élève, il l'inquiète.",
        "Notions du chapitre : " + " ; ".join(f.notions) + ".",
        "Méthodes attendues au bac : " + " ; ".join(f.methodes_autorisees) + ".",
    ]
    if f.demonstrations_admises:
        lignes.append("Admis sans démonstration : " + " ; ".join(f.demonstrations_admises) + ".")
    if hors:
        lignes.append("N'emploie pas : " + " ; ".join(f"{t.terme} → {t.dire_plutot}" for t in hors[:12]) + ".")
    if f.niveau:
        lignes.append("Niveau attendu : " + f.niveau)
    return "\n".join(lignes) + "\n"


def detecter(texte: str, subject: str, chapitre: Optional[str], carte: Optional[dict] = None) -> list[Detection]:
    """Les termes hors programme employés dans un texte du tuteur.

    Les termes génériques de la matière s'appliquent toujours ; ceux du
    chapitre seulement si le chapitre a une fiche. Chaque terme n'est signalé
    qu'une fois, avec un court extrait pour qu'un humain puisse juger.
    """
    carte = carte or charger()
    matiere = _matiere(subject)
    if matiere is None or not texte:
        return []
    termes = list(carte.get(matiere, {}).get("generiques", ()))
    f = fiche(subject, chapitre, carte)
    if f is not None:
        termes = list(f.termes_hors_programme) + termes
    normalise = _normaliser(texte)
    detections: list[Detection] = []
    for t in termes:
        m = t.motif.search(normalise)
        if not m:
            continue
        debut, fin = max(0, m.start() - 40), min(len(texte), m.end() + 40)
        # L'extrait vient du texte normalisé (même longueur que l'original sans
        # les accents combinants) : lisible, suffisant pour juger.
        detections.append(Detection(t.terme, normalise[debut:fin].strip(), t.dire_plutot, t.chapitre or chapitre or ""))
    return detections


def journaliser(detections: list[Detection], *, subject: str, chapitre: Optional[str], student_id: str = "",
                tour: int = 0, chemin: Path = JOURNAL) -> None:
    """Une ligne JSON par tour où quelque chose dépasse. C'est le journal de la
    phase d'observation : il dit quels termes reviennent, sur quels chapitres."""
    if not detections:
        return
    from datetime import datetime, timezone

    ligne = {
        "quand": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "eleve": (student_id or "")[:8], "matiere": subject, "chapitre": chapitre or "", "tour": tour,
        "termes": [{"terme": d.terme, "extrait": d.extrait, "dire_plutot": d.dire_plutot} for d in detections],
    }
    chemin.parent.mkdir(parents=True, exist_ok=True)
    with chemin.open("a", encoding="utf-8") as f:
        f.write(json.dumps(ligne, ensure_ascii=False) + "\n")
