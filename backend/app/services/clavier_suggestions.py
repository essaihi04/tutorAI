"""Les suggestions du clavier scientifique (12 novembre 2026).

Quand une question à réponse libre (ou le « retrouver » d'un bloc) s'ouvre, le clavier montre en haut quelques
éléments propres à CET exercice : symboles, grandeurs, morceaux de relation, unités. Des justes (`aides`) et des faux
plausibles (`pieges`), mais JAMAIS la formule complète ni la réponse attendue.

D'où elles viennent, dans l'ordre :
  1. la question les porte (`clavier = {aides: [...], pieges: [...]}`, écrites avec le cours) → `source: "cours"` ;
  2. déjà générées pour cette question (cache mémoire borné) → `source: "cache"` ;
  3. demandées au LLM (`llm_service.chat`), puis filtrées ici → `source: "llm"`.

La réponse attendue est toujours lue dans le cours, côté serveur, jamais reçue du client : c'est elle qui sert au
filtre. Un filtre robuste retire tout élément égal à la réponse (après normalisation), qui la contient entière, qui
est une relation complète (un `=` avec deux côtés), ou trop long.
"""
from __future__ import annotations

import json
import re
import unicodedata
from collections import OrderedDict
from dataclasses import dataclass, field
from typing import Any, Optional

#: Ce qu'on demande au LLM (longueur d'un élément) et ce que le filtre laisse passer au plus.
LONGUEUR_DEMANDEE, LONGUEUR_MAX = 14, 18
AIDES_MAX, PIEGES_MAX = 6, 4
CACHE_MAX = 2000

_cache: "OrderedDict[tuple, dict]" = OrderedDict()


# ── Normalisation et filtre ──────────────────────────────────────────────────

_EXPOSANTS = str.maketrans({"⁰": "0", "¹": "1", "²": "2", "³": "3", "⁴": "4", "⁵": "5", "⁶": "6", "⁷": "7",
                            "⁸": "8", "⁹": "9", "⁺": "+", "⁻": "-", "ⁿ": "n"})


def normaliser(s: Any) -> str:
    """Une forme de comparaison : sans espaces, casse, ponctuation ni signes de produit ; « x² » = « x^2 »,
    « − » = « - », « m·s⁻¹ » = « m s^-1 »."""
    t = str(s or "").translate(_EXPOSANTS)
    t = unicodedata.normalize("NFKC", t).lower()
    t = t.replace("−", "-").replace("–", "-").replace("—", "-")
    t = re.sub(r"[\s·⋅∙×*^.,;:!?«»\"'`()\[\]{}]", "", t)
    return t


def _relation_complete(s: str) -> bool:
    """Un `=` (ou ≈, ≡) avec quelque chose des deux côtés : une relation entière, interdite au clavier."""
    for signe in ("=", "≈", "≡"):
        if signe in s:
            gauche, _, droite = s.partition(signe)
            if gauche.strip() and droite.strip():
                return True
    return False


def _formes_interdites(attendu: Optional[str]) -> list[str]:
    """La réponse attendue normalisée, et chaque côté d'une relation attendue (« x² − 9 = (x − 3)(x + 3) » interdit
    aussi « (x − 3)(x + 3) »)."""
    if not attendu:
        return []
    formes = [normaliser(attendu)]
    for cote in re.split(r"[=≈≡]", str(attendu)):
        n = normaliser(cote)
        if n and n not in formes:
            formes.append(n)
    return [f for f in formes if f]


def _elements_enumeres(attendu: Optional[str]) -> list[str]:
    """Une réponse qui ÉNUMÈRE (« Quatre formes indéterminées : 0/0, ∞/∞, +∞ − ∞, 0 × ∞ ») : chacun de ses éléments est
    interdit aussi — proposés ensemble, ils redonneraient la réponse entière (12 novembre 2026)."""
    if not attendu:
        return []
    corps = str(attendu).split(":", 1)[-1]
    morceaux = [m for m in re.split(r"[,;]|\bet\b|\bou\b", corps) if m.strip()]
    elements = [n for n in (normaliser(m) for m in morceaux) if len(n) >= 2] if len(morceaux) >= 2 else []
    # une factorisation (« (x − 3)(x + 3) ») : ses facteurs, proposés ensemble, la redonneraient aussi
    for cote in re.split(r"[=≈≡]", str(attendu)):
        facteurs = re.findall(r"\([^()]+\)", cote)
        if len(facteurs) >= 2:
            elements += [n for n in (normaliser(f) for f in facteurs) if len(n) >= 2]
    return elements


def interdit(element: str, attendu: Optional[str]) -> bool:
    e = str(element or "").strip()
    if not e or len(e) > LONGUEUR_MAX or _relation_complete(e):
        return True
    n = normaliser(e)
    if not n:
        return True
    for f in _formes_interdites(attendu):
        # égal à la réponse (ou à un côté) ; ou la contient entière (seulement si elle n'est pas un simple
        # caractère ou deux, sinon « 2 » interdirait « x² »)
        if n == f or (len(f) >= 3 and f in n):
            return True
    return n in _elements_enumeres(attendu)


def filtrer(aides: Any, pieges: Any, attendu: Optional[str]) -> dict:
    """Nettoie, filtre et dédoublonne ; un piège ne peut pas être aussi une aide."""
    vus: set[str] = set()

    def passe(liste: Any, maximum: int) -> list[str]:
        out: list[str] = []
        for x in liste if isinstance(liste, list) else []:
            if not isinstance(x, (str, int, float)) or isinstance(x, bool):
                continue
            e = re.sub(r"\s+", " ", str(x)).strip()
            n = normaliser(e)
            if n in vus or interdit(e, attendu):
                continue
            vus.add(n)
            out.append(e)
            if len(out) >= maximum:
                break
        return out

    a = passe(aides, AIDES_MAX)
    return {"aides": a, "pieges": passe(pieges, PIEGES_MAX)}


# ── Retrouver la question dans le cours ──────────────────────────────────────

def trouver_question(deck: dict, slide_id: str, cle: str) -> Optional[dict]:
    """La question (dict du cours) visée par (slide_id, cle) :
      - diapositive : `question` (cle « q »), `exercises[i]` (cle « e<i> »), affirmation « e<i>s<j> » d'un vrai/faux ;
      - bloc (slide_id = id du bloc) : `retrouver` (cle « retrouver »), `exercice` (cle « exercice_bloc ») ;
      - compétence (slide_id = id de la compétence) : un de ses `rappels` (cle = id du rappel)."""
    if not isinstance(deck, dict) or not slide_id:
        return None
    cle = cle or "q"
    for a in deck.get("activities") or []:
        for s in (a or {}).get("slides") or []:
            if not isinstance(s, dict) or s.get("id") != slide_id:
                continue
            if cle == "q":
                q = s.get("question")
                return q if isinstance(q, dict) else None
            m = re.fullmatch(r"e(\d+)(?:s(\d+))?", cle)
            if not m:
                return None
            exs = s.get("exercises") or []
            i = int(m.group(1))
            if i >= len(exs) or not isinstance(exs[i], dict):
                return None
            if m.group(2) is None:
                return exs[i]
            sts = exs[i].get("statements") or []
            j = int(m.group(2))
            if j >= len(sts) or not isinstance(sts[j], dict):
                return None
            st = sts[j]
            return {**st, "prompt": st.get("text") or st.get("prompt") or "", "type": "vrai_faux"}
    for se in deck.get("seances") or []:
        for b in (se or {}).get("blocs") or []:
            if isinstance(b, dict) and b.get("id") == slide_id:
                q = b.get("retrouver") if cle == "retrouver" else b.get("exercice") if cle == "exercice_bloc" else None
                return q if isinstance(q, dict) else None
    for c in deck.get("competences") or []:
        if isinstance(c, dict) and c.get("id") == slide_id:
            return next((r for r in c.get("rappels") or [] if isinstance(r, dict) and r.get("id") == cle), None)
    return None


def attendu_de(q: Optional[dict]) -> Optional[str]:
    """La réponse attendue : `attendu` (ou ses synonymes), sinon la bonne option d'un QCM."""
    if not isinstance(q, dict):
        return None
    for k in ("attendu", "reponse_attendue", "expected", "answer", "reponse"):
        v = q.get(k)
        if isinstance(v, (str, int, float)) and not isinstance(v, bool) and str(v).strip():
            return str(v).strip()
    options = q.get("options") or q.get("choices")
    c = q.get("correct")
    if isinstance(options, list) and isinstance(c, int) and not isinstance(c, bool) and 0 <= c < len(options):
        return str(options[c]).strip() or None
    return None


def enonce_de(q: Optional[dict]) -> str:
    if not isinstance(q, dict):
        return ""
    return str(q.get("prompt") or q.get("text") or q.get("enonce") or "").strip()


def suggestions_preparees(question: Optional[dict]) -> Optional[dict]:
    """Les suggestions écrites avec le cours (`question.clavier`), nettoyées et filtrées comme les autres."""
    if not isinstance(question, dict):
        return None
    c = question.get("clavier")
    if not isinstance(c, dict) or not (c.get("aides") or c.get("pieges")):
        return None
    return filtrer(c.get("aides"), c.get("pieges"), attendu_de(question))


# ── Le LLM ───────────────────────────────────────────────────────────────────

NOMS_MATIERES = {"physique": "physique-chimie", "chimie": "physique-chimie", "math": "mathématiques",
                 "svt": "SVT (sciences de la vie et de la Terre)"}

EXEMPLES = {
    "physique-chimie": "« λ », « v », « T », « 1/f », « Hz », « m·s⁻¹ », « d/Δt », « τ »",
    "mathématiques": "« 1/x », « x → +∞ », « 0⁺ », « √x », « ln », « f(a) », « +∞ − ∞ », « |x| »",
    "SVT (sciences de la vie et de la Terre)": "« ATP », « NADH,H⁺ », « mitochondrie », « O₂ », « ADN », « 2n », « méiose »",
}

SYSTEME = "Tu es un professeur de 2e Bac (Maroc, BIOF) qui prépare le clavier d'un exercice. Tu réponds uniquement en JSON valide."


def prompt_suggestions(enonce: str, attendu: Optional[str], matiere: str) -> str:
    nom = NOMS_MATIERES.get(matiere, matiere or "physique-chimie")
    lignes = [
        f"Matière : {nom}.",
        f"Exercice posé à l'élève : {enonce.strip()[:600]}",
        f"Réponse attendue (À NE JAMAIS DONNER, ni entière ni sous forme de relation complète) : {attendu}" if attendu else None,
        "",
        "L'élève va écrire sa réponse avec un clavier scientifique. Propose les touches à mettre en haut du clavier pour CET exercice :",
        "- « aides » : 4 à 6 éléments justes et utiles pour écrire la réponse (un symbole, une grandeur, une unité, un morceau de relation) ;",
        "- « pieges » : 2 à 4 éléments faux mais plausibles (l'erreur classique d'un élève : mauvaise unité, mauvais symbole, morceau inversé).",
        f"Chaque élément est COURT ({LONGUEUR_DEMANDEE} caractères au plus), par exemple {EXEMPLES.get(nom, EXEMPLES['physique-chimie'])}.",
        "Interdit : la réponse attendue, une relation complète (pas de « = » avec deux côtés), une phrase, du LaTeX, le signe $.",
        "Écris les symboles en Unicode (λ, τ, Δ, ², ⁻¹, →, √, ∞), comme dans le cours.",
        'Rends uniquement : {"aides": ["..."], "pieges": ["..."]}',
    ]
    return "\n".join(l for l in lignes if l is not None)


def _json(texte: str) -> Optional[dict]:
    t = re.sub(r"^```(?:json)?|```$", "", (texte or "").strip(), flags=re.M).strip()
    debut, fin = t.find("{"), t.rfind("}")
    if debut < 0 or fin <= debut:
        return None
    try:
        d = json.loads(t[debut:fin + 1])
    except ValueError:
        return None
    return d if isinstance(d, dict) else None


def analyser(texte: str, attendu: Optional[str], enonce: str = "") -> dict:
    """La réponse du LLM, filtrée. `enonce` : un élément qui recopie tout l'énoncé est aussi retiré."""
    d = _json(texte) or {}
    r = filtrer(d.get("aides"), d.get("pieges"), attendu)
    if enonce:
        n_enonce = normaliser(enonce)
        for k in ("aides", "pieges"):
            r[k] = [x for x in r[k] if normaliser(x) != n_enonce]
    return r


# ── Le parcours d'une demande ────────────────────────────────────────────────

@dataclass
class Demande:
    enonce: str
    attendu: Optional[str]
    matiere: str
    cle_cache: tuple
    question: Optional[dict] = None
    preparees: Optional[dict] = field(default=None)


def preparer(deck: Optional[dict], deck_id: str, slide_id: str, cle: str, enonce: str, matiere: str) -> Optional[Demande]:
    """Ce qu'il faut pour répondre ; None si ni la question ni un énoncé ne sont connus."""
    q = trouver_question(deck or {}, slide_id, cle) if deck else None
    if q is not None:
        return Demande(enonce=enonce_de(q) or (enonce or "").strip(), attendu=attendu_de(q), matiere=matiere,
                       cle_cache=(deck_id, slide_id, cle), question=q, preparees=suggestions_preparees(q))
    if not (enonce or "").strip():
        return None
    # question inconnue : on génère sur l'énoncé du client, sans attendu (seules les relations complètes sont filtrées)
    return Demande(enonce=enonce.strip(), attendu=None, matiere=matiere,
                   cle_cache=(deck_id, slide_id, cle, normaliser(enonce)[:300]))


def deja_pretes(d: Demande) -> Optional[dict]:
    """Les suggestions sans appel au LLM : celles du cours, puis le cache."""
    if d.preparees is not None:
        return {**d.preparees, "source": "cours"}
    r = _cache.get(d.cle_cache)
    if r is not None:
        _cache.move_to_end(d.cle_cache)
        return {**r, "source": "cache"}
    return None


def _garder(cle: tuple, r: dict) -> None:
    _cache[cle] = r
    _cache.move_to_end(cle)
    while len(_cache) > CACHE_MAX:
        _cache.popitem(last=False)


async def generer(d: Demande, student_id: Optional[str] = None) -> dict:
    """Demande au LLM, filtre, garde en cache. Jamais d'exception : en cas d'échec, des listes vides."""
    from app.services.llm_service import llm_service

    prompt = prompt_suggestions(d.enonce, d.attendu, d.matiere)
    for _ in range(2):
        try:
            texte = await llm_service.chat(messages=[{"role": "user", "content": prompt}], system_prompt=SYSTEME,
                                           temperature=0.4, max_tokens=300, student_id=student_id,
                                           session_type="course_player")
        except Exception:  # noqa: BLE001
            break
        r = analyser(texte, d.attendu, d.enonce)
        if r["aides"] or r["pieges"]:
            _garder(d.cle_cache, r)
            return {**r, "source": "llm"}
    return {"aides": [], "pieges": [], "source": "aucune"}
