"""L'expérience des professeurs, chapitre par chapitre.

Le périmètre dit au tuteur jusqu'où aller ; le skill professeur lui dit quand
expliquer, questionner, donner la réponse. Il lui manquait ce qu'un prof
apprend en dix ans de classe : où les élèves se trompent sur CE chapitre, le
geste qui débloque, le cas type qu'il faut reconnaître dans un énoncé, la
valeur repère qui trahit un calcul faux — et ce que certains profs disent de
faux et qu'il ne faut pas reprendre.

`data/curriculum/experience_profs.json` vient de cours réels de profs marocains,
lus en entier et paraphrasés, croisés avec les examens nationaux et vérifiés
contre `perimetre.json` : ce qui sort du programme n'y est pas.

Le module rend des blocs courts, chacun au moment où il sert (voir
`skill_professeur.consigne`) :

* **expliquer** : ce que les profs répètent, et ce qu'il ne faut pas dire ;
* **résoudre** : les cas types avec leur méthode, et les valeurs repères ;
* **après une erreur** : les pièges connus et le geste qui corrige.

Après la réponse, `detecter` relit le texte et note les approximations à ne pas
reprendre. Comme pour le périmètre : on journalise, on ne corrige pas encore.

Un chapitre absent du fichier ne reçoit rien. Mieux vaut un silence qu'une
expérience inventée.
"""
from __future__ import annotations

import json
import os
import re
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import Optional

from app.services.perimetre import Detection, _compiler, _normaliser
from app.services.prerequis import _matiere

CHEMIN = Path(__file__).resolve().parent.parent.parent / "data" / "curriculum" / "experience_profs.json"
JOURNAL = Path(os.environ.get("EXPERIENCE_JOURNAL_PATH") or
               Path(__file__).resolve().parent.parent.parent / "data" / "experience_journal.jsonl")


@dataclass(frozen=True)
class CasType:
    id: str
    nom: str
    indices: str
    methode: str


@dataclass(frozen=True)
class Piege:
    erreur: str
    geste: str


@dataclass(frozen=True)
class FicheExperience:
    chapitre: str
    nom: str
    insistances: tuple[str, ...]
    valeurs_reperes: tuple[str, ...]
    cas_types: tuple[CasType, ...]
    pieges: tuple[Piege, ...]
    analogies: tuple[str, ...]
    a_ne_pas_dire: tuple[tuple[str, object, str], ...]  # (terme, motif compilé, dire plutôt)
    exclus: tuple[str, ...]
    #: Questions que les élèves posent vraiment (commentaires sous les vidéos), avec la réponse juste.
    questions: tuple[tuple[str, str], ...] = ()


def _fiche_depuis(chapitre: str, f: dict) -> FicheExperience:
    for champ in ("nom", "insistances", "cas_types", "pieges"):
        if not f.get(champ):
            raise ValueError(f"experience_profs.json : champ « {champ} » vide pour {chapitre}")
    cas = []
    for c in f["cas_types"]:
        if not all(str(c.get(k, "")).strip() for k in ("id", "nom", "methode")):
            raise ValueError(f"experience_profs.json : cas type incomplet ({chapitre}) : {c}")
        cas.append(CasType(c["id"], c["nom"], c.get("indices", ""), c["methode"]))
    pieges = []
    for p in f["pieges"]:
        if not str(p.get("erreur", "")).strip() or not str(p.get("geste", "")).strip():
            raise ValueError(f"experience_profs.json : piège incomplet ({chapitre}) : {p}")
        pieges.append(Piege(p["erreur"], p["geste"]))
    a_eviter = []
    for t in f.get("a_ne_pas_dire", []):
        if not str(t.get("terme", "")).strip() or not str(t.get("motif", "")).strip():
            raise ValueError(f"experience_profs.json : formulation à éviter incomplète ({chapitre}) : {t}")
        a_eviter.append((t["terme"], _compiler(t["motif"]), t.get("dire_plutot", "")))
    return FicheExperience(
        chapitre=chapitre, nom=f["nom"], insistances=tuple(f["insistances"]),
        valeurs_reperes=tuple(f.get("valeurs_reperes", ())), cas_types=tuple(cas), pieges=tuple(pieges),
        analogies=tuple(f.get("analogies_validees", ())), a_ne_pas_dire=tuple(a_eviter),
        exclus=tuple(e.get("element", "") for e in f.get("exclus_hors_programme", ())),
        questions=tuple((q["question"], q["reponse"]) for q in f.get("questions_eleves", ())
                        if str(q.get("question", "")).strip() and str(q.get("reponse", "")).strip()),
    )


def charger(chemin: Path = CHEMIN) -> dict:
    """matière → {chapitre: FicheExperience}. Une entrée mal formée fait échouer le chargement."""
    brut = json.loads(chemin.read_text(encoding="utf-8"))
    return {
        matiere: {ch: _fiche_depuis(ch, f) for ch, f in bloc.get("chapitres", {}).items()}
        for matiere, bloc in brut["matieres"].items()
    }


@lru_cache(maxsize=1)
def _carte_par_defaut() -> dict:
    return charger()


def fiche(subject: str, chapitre: Optional[str], carte: Optional[dict] = None) -> Optional[FicheExperience]:
    matiere = _matiere(subject)
    if matiere is None or not chapitre:
        return None
    carte = carte if carte is not None else _carte_par_defaut()
    return carte.get(matiere, {}).get(chapitre)


# ------------------------------------------------------------------ blocs du prompt
# Courts et impératifs : un bloc long se fait paraphraser au lieu d'être suivi.

def bloc_explication(f: Optional[FicheExperience]) -> str:
    if f is None:
        return ""
    lignes = [f"Expérience des profs ({f.nom}) — ce qu'ils répètent : " + " ; ".join(f.insistances) + "."]
    if f.analogies:
        lignes.append("Images qui marchent en classe : " + " ; ".join(f.analogies[:4]) + ".")
    if f.a_ne_pas_dire:
        lignes.append("Ne dis pas : " + " ; ".join(f"« {t} » → {d}" for t, _, d in f.a_ne_pas_dire) + ".")
    if f.exclus:
        lignes.append("Hors de ce cours : " + ", ".join(f.exclus) + ".")
    return " ".join(lignes)


def _indices_trouves(c: CasType, texte: str) -> bool:
    t = _normaliser(texte or "")
    return any(len(i) >= 4 and i in t for i in (_normaliser(x).strip() for x in re.split(r"[,;]", c.indices)))


def bloc_resolution(f: Optional[FicheExperience], texte: str = "") -> str:
    """Les cas types, les valeurs repères — et la méthode complète des seuls cas que le texte évoque.

    Tous les cas sont nommés avec leurs indices (pour reconnaître le cas) ; la méthode détaillée
    n'est donnée que pour ceux dont un indice figure dans le texte de l'élève ou de l'énoncé,
    sinon pour tous tant que le bloc reste court.
    """
    if f is None:
        return ""
    vises = [c for c in f.cas_types if texte and _indices_trouves(c, texte)][:3]
    complet = " | ".join(f"{c.nom} ({c.indices}) : {c.methode}" for c in f.cas_types)
    if not vises and len(complet) < 2600:
        cas = complet
    else:
        cas = " | ".join(f"{c.nom} ({c.indices})" + (f" : {c.methode}" if c in vises else "") for c in f.cas_types)
    lignes = [f"Cas types du chapitre — reconnais-en un aux indices de l'énoncé, nomme-le, fais schématiser, "
              f"puis suis sa méthode : {cas}."]
    if f.valeurs_reperes:
        lignes.append("Valeurs repères pour contrôler un résultat : " + " ; ".join(f.valeurs_reperes) + ".")
    return " ".join(lignes)


_MOT = re.compile(r"[a-z0-9θτλ]{3,}|[؀-ۿ]{3,}")
_VIDES = {"les", "des", "une", "est", "que", "qui", "pour", "dans", "avec", "pas", "sur", "par", "son", "ses", "mais",
          "quoi", "comment", "pourquoi", "quand", "elle", "faut", "peut", "on", "dire", "ce", "cette", "sont"}


def _mots(texte: str) -> set[str]:
    return {m for m in _MOT.findall(_normaliser(texte)) if m not in _VIDES}


def bloc_questions(f: Optional[FicheExperience], demande: str, n: int = 2) -> str:
    """Les questions d'élèves les plus proches de la demande, avec leur réponse juste.

    Seules les plus proches sont servies : toute la liste allongerait chaque prompt
    pour rien. Rien n'est servi si aucune question ne partage au moins deux mots.
    """
    if f is None or not f.questions or not (demande or "").strip():
        return ""
    mots = _mots(demande)
    proches = sorted(((len(mots & _mots(q)), q, r) for q, r in f.questions), key=lambda x: -x[0])
    proches = [(q, r) for score, q, r in proches[:n] if score >= 2]
    if not proches:
        return ""
    return ("Des élèves ont déjà posé une question proche — appuie-toi sur la réponse juste, avec tes mots : "
            + " ; ".join(f"« {q} » → {r}" for q, r in proches) + ".")


def bloc_pieges(f: Optional[FicheExperience]) -> str:
    if f is None:
        return ""
    return ("Erreurs que les profs voient souvent sur ce chapitre — si sa réponse en relève une, nomme-la et "
            "utilise le geste indiqué comme indice : "
            + " ; ".join(f"{p.erreur} → {p.geste}" for p in f.pieges) + ".")


# ------------------------------------------------------------------ après la réponse

def detecter(texte: str, subject: str, chapitre: Optional[str], carte: Optional[dict] = None) -> list[Detection]:
    """Les approximations de profs que le tuteur vient de reprendre, une fois chacune."""
    f = fiche(subject, chapitre, carte)
    if f is None or not texte:
        return []
    normalise = _normaliser(texte)
    detections = []
    for terme, motif, dire in f.a_ne_pas_dire:
        m = motif.search(normalise)
        if m:
            debut, fin = max(0, m.start() - 40), min(len(normalise), m.end() + 40)
            detections.append(Detection(terme, normalise[debut:fin].strip(), dire, f.chapitre))
    return detections
