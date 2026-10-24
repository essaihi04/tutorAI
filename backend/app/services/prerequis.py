"""Les compétences des années antérieures dont dépend chaque chapitre.

Un élève de 2e bac qui bute sur le dipôle RC ne bute pas toujours sur le
dipôle RC : souvent il ne sait plus dériver, ou résoudre une équation du
premier degré. Continuer le cours sans le voir, c'est bâtir sur du sable ;
tout arrêter pour refaire la 1re bac, c'est perdre l'élève. Un prof ouvre une
PARENTHÈSE : il nomme le prérequis, le réexplique en trois phrases avec un
exemple du niveau d'origine, vérifie d'une question, et revient exactement où
il en était.

Ce module tient la carte — chapitre de 2e bac → prérequis (tronc commun,
1re bac, collège), tirée des programmes officiels et relue dans
`data/curriculum/prerequis.json` — et rien d'autre. Il ne décide pas d'ouvrir
une parenthèse : c'est le modèle qui, voyant l'erreur, déclare
``<prerequis>id</prerequis>`` parmi les identifiants qu'on lui a donnés pour
ce chapitre, et le skill prof qui tient le déroulé. Un identifiant hors de la
liste du chapitre est ignoré, comme un mode inconnu : on ne part pas en
parenthèse sur une invention.

Le module ne lit ni base ni réseau. Il charge un fichier une fois.
"""
from __future__ import annotations

import json
import re
import unicodedata
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import Optional

CHEMIN = Path(__file__).resolve().parent.parent.parent / "data" / "curriculum" / "prerequis.json"
BALISE_PREREQUIS = re.compile(r"<prerequis>\s*([a-z0-9_]+)\s*</prerequis>", re.IGNORECASE)
NIVEAUX = ("college", "TC", "1BAC")
NIVEAU_LISIBLE = {"college": "collège", "TC": "tronc commun", "1BAC": "1re bac"}


@dataclass(frozen=True)
class Prerequis:
    id: str
    titre: str
    niveau: str
    matiere: str
    #: Le document officiel et le chapitre d'origine. C'est ce qui permet à un
    #: enseignant de contester une entrée : sans source, une carte de prérequis
    #: n'est qu'une opinion.
    source: str
    #: La phrase à relire, telle qu'elle doit rester dans la tête de l'élève.
    rappel: str
    #: Un exemple du niveau d'origine, à faire résoudre avant la vérification.
    exemple: str
    #: UNE question courte qui tranche : acquis ou pas.
    verification: str

    @property
    def niveau_lisible(self) -> str:
        return NIVEAU_LISIBLE.get(self.niveau, self.niveau)


@dataclass(frozen=True)
class Carte:
    competences: dict[str, Prerequis]
    #: matière → chapitre → identifiants de prérequis, dans l'ordre où un prof
    #: les suspecterait.
    chapitres: dict[str, dict[str, tuple[str, ...]]]
    #: matière → chapitre → nom lisible (pour retrouver le chapitre depuis un
    #: titre libre de séance).
    noms: dict[str, dict[str, str]]


def _normaliser(texte: str) -> str:
    texte = unicodedata.normalize("NFD", (texte or "").lower())
    texte = "".join(c for c in texte if unicodedata.category(c) != "Mn")
    return re.sub(r"[^a-z0-9]+", " ", texte).strip()


def _matiere(subject: str) -> Optional[str]:
    s = _normaliser(subject)
    if s in ("pc", "physique chimie") or "phys" in s or "chim" in s:
        return "Physique-Chimie"
    if "math" in s:
        return "Mathématiques"
    if "svt" in s or "vie et de la terre" in s:
        return "SVT"
    return None


@lru_cache(maxsize=1)
def charger(chemin: Path = CHEMIN) -> Carte:
    """Lit la carte une fois. Une entrée mal formée fait échouer le chargement :
    mieux vaut une parenthèse jamais ouverte qu'une parenthèse sur du vide."""
    brut = json.loads(chemin.read_text(encoding="utf-8"))
    competences: dict[str, Prerequis] = {}
    for cle, c in brut["competences"].items():
        if c.get("niveau") not in NIVEAUX:
            raise ValueError(f"prerequis.json : niveau inconnu pour {cle} : {c.get('niveau')!r}")
        for champ in ("titre", "matiere", "source", "rappel", "exemple", "verification"):
            if not str(c.get(champ, "")).strip():
                raise ValueError(f"prerequis.json : champ « {champ} » vide pour {cle}")
        competences[cle] = Prerequis(id=cle, **{k: c[k] for k in ("titre", "niveau", "matiere", "source", "rappel", "exemple", "verification")})
    chapitres: dict[str, dict[str, tuple[str, ...]]] = {}
    noms: dict[str, dict[str, str]] = {}
    for matiere, chaps in brut["chapitres"].items():
        chapitres[matiere], noms[matiere] = {}, {}
        for chapitre, entree in chaps.items():
            ids = tuple(entree["prerequis"])
            inconnus = [i for i in ids if i not in competences]
            if inconnus:
                raise ValueError(f"prerequis.json : {matiere}/{chapitre} cite des prérequis inconnus : {inconnus}")
            chapitres[matiere][chapitre] = ids
            noms[matiere][chapitre] = entree["nom"]
    return Carte(competences, chapitres, noms)


_VIDES = {"le", "la", "les", "de", "du", "des", "et", "d", "l", "un", "une", "dans", "en", "au", "aux", "a", "sur", "par", "pour", "chapitre", "cours", "lecon"}


def trouver_chapitre(subject: str, texte: str, carte: Optional[Carte] = None) -> Optional[str]:
    """Le chapitre de 2e bac dont parle un titre libre de séance, ou None.

    Les séances portent un titre rédigé (« Le dipôle RC : charge d'un
    condensateur »), pas un identifiant. On cherche le chapitre dont le nom
    partage le plus de mots pleins avec ce titre ; en dessous de deux mots
    communs, ou à égalité, on ne devine pas.
    """
    carte = carte or charger()
    matiere = _matiere(subject)
    if matiere is None or matiere not in carte.noms or not texte:
        return None
    mots = {m for m in _normaliser(texte).split() if m not in _VIDES and len(m) > 1}
    scores: list[tuple[int, str]] = []
    for chapitre, nom in carte.noms[matiere].items():
        communs = mots & {m for m in _normaliser(nom + " " + chapitre.replace("_", " ")).split() if m not in _VIDES}
        if communs:
            scores.append((len(communs), chapitre))
    if not scores:
        return None
    scores.sort(reverse=True)
    meilleur, chapitre = scores[0]
    if meilleur < 2 or (len(scores) > 1 and scores[1][0] == meilleur):
        return None
    return chapitre


def pour_chapitre(subject: str, chapitre: Optional[str], carte: Optional[Carte] = None) -> list[Prerequis]:
    carte = carte or charger()
    matiere = _matiere(subject)
    if matiere is None or not chapitre:
        return []
    return [carte.competences[i] for i in carte.chapitres.get(matiere, {}).get(chapitre, ())]


def lire_declaration(reponse_brute: str, candidats: list[Prerequis]) -> Optional[Prerequis]:
    """Le prérequis déclaré par le modèle, s'il fait partie de ceux du chapitre."""
    match = BALISE_PREREQUIS.search(reponse_brute or "")
    if not match:
        return None
    voulu = match.group(1).lower()
    return next((p for p in candidats if p.id == voulu), None)


def bloc_candidats(candidats: list[Prerequis]) -> str:
    """Ce que le modèle lit avant de juger une réponse fausse : les prérequis
    plausibles de ce chapitre, avec de quoi ouvrir la parenthèse sans inventer."""
    if not candidats:
        return ""
    lignes = [
        "Prérequis des années antérieures dont dépend ce chapitre. Si l'erreur de l'élève vient de l'un "
        "d'eux (et non de la notion du jour), ouvre une PARENTHÈSE dans ce message : écris la balise "
        "<prerequis>identifiant</prerequis> (retirée avant l'affichage), annonce « On ouvre une parenthèse : "
        "[titre] », explique ce prérequis en 3 à 5 phrases avec l'exemple donné, relis la phrase-clé "
        "(« Je relis : … »), puis pose UNIQUEMENT la question de vérification ci-dessous. Ne traite pas la "
        "question du cours dans ce message ; elle attendra. Un seul prérequis à la fois, seulement parmi "
        "cette liste, et seulement si c'est vraiment la cause de l'erreur.",
    ]
    for p in candidats:
        lignes.append(
            f"- {p.id} — {p.titre} ({p.niveau_lisible}). Phrase-clé : « {p.rappel} » Exemple : {p.exemple} "
            f"Vérification : « {p.verification} »"
        )
    return "\n".join(lignes)
