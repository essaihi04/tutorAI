"""Ce que le tuteur vient de dire — pour qu'il arrête de se recopier.

Un modèle relit son propre historique avant d'écrire, et c'est là que naît
la voix de robot : après trois réponses ouvertes par « مزيان بزاف زهير », la
quatrième ne se décide plus, elle se recopie. Une consigne de style ne gagne
pas contre ça — la consigne est UNE phrase, l'exemple est CINQ fois sous ses
yeux, et c'est l'exemple qui l'emporte.

D'où ce module : on relit l'historique et on rend au prompt un miroir qui
CITE les tournures déjà servies. Interdire une phrase qu'on lui montre mot
pour mot est la seule instruction qu'un modèle ne peut pas confondre avec son
propre style.

Deux choses sortent d'ici :

  • ``bloc_memoire`` — le miroir injecté dans le prompt système.
  • ``limiter_emojis`` — la seule règle de ce lot qui ne se négocie pas avec
    le modèle. Le prompt interdit déjà les pictogrammes dans le texte parlé ;
    l'échange du 18 août en contenait un par réponse, toujours à la même
    place. Ce qui doit tenir, on le tient ici, pas dans une consigne.

Tout est DÉRIVÉ de ``conversation_history``. Aucun état parallèle à tenir à
jour, donc rien qui puisse se désynchroniser de ce que le modèle voit.
"""
from __future__ import annotations

import re
from collections import Counter

#: Pictogrammes SEULS. Les flèches (« → ») et les signes mathématiques
#: restent : ce ne sont pas des décorations, ils portent du sens dans une
#: correction écrite au tableau.
_CLASSE_EMOJI = (
    "["
    "\U0001F000-\U0001FAFF"   # pictogrammes, émotions, objets, drapeaux
    "\U00002600-\U000026FF"   # symboles divers
    "\U00002700-\U000027BF"   # dingbats
    "\U00002B00-\U00002BFF"   # étoiles et flèches épaisses
    "\U0000FE00-\U0000FE0F"   # sélecteurs de variante
    "\U0000200D\U000020E3\U00002139\U00002764"
    "]"
)
#: Une rafale de pictogrammes collés est UNE décoration, pas deux : le « + »
#: les compte ensemble, et le sélecteur de variante ne consomme pas un budget
#: à lui tout seul.
_EMOJIS = re.compile(_CLASSE_EMOJI + "+")

#: Un mot, quel que soit l'alphabet. `[^\W_]` couvre le latin accentué ET
#: l'arabe, en laissant dehors la ponctuation arabe — « صحيح، » et
#: « صحيح » doivent compter pour le même mot.
_MOT = re.compile(r"[^\W_]+")
_FIN_DE_PHRASE = re.compile(r"(?<=[.!?؟…])\s+")
_ESPACES = re.compile(r" {2,}")

#: Mots trop fréquents pour signer une tournure. Une expression faite de ces
#: seuls mots revient dans toutes les phrases de darija : la citer au modèle
#: ne lui apprendrait rien et lui interdirait de parler.
_MOTS_VIDES = frozenset({
    # darija / arabe
    "و", "في", "من", "على", "الى", "إلى", "هو", "هي", "ما", "لا", "نعم",
    "هاد", "هادي", "هادو", "هاديك", "اللي", "ديال", "مع", "بحال", "بلا",
    "كان", "كاين", "كانت", "باش", "حتى", "كي", "كيف", "لي", "ليك", "ليا",
    "شي", "كل", "ولا", "أو", "غير", "راه", "راك", "هنا", "تما", "علاه",
    "نا", "انا", "أنا", "نتا", "انت", "أنت", "ديالك", "ديالي", "عند", "عندك",
    "يعني", "بزاف", "شوية", "دابا", "بعد", "قبل", "واحد", "جوج",
    # français
    "le", "la", "les", "de", "du", "des", "un", "une", "et", "ou", "que",
    "qui", "est", "pour", "dans", "sur", "avec", "ce", "cette", "tu", "je",
    "il", "elle", "on", "nous", "vous", "pas", "ne", "plus", "au", "aux",
    "en", "a", "à", "se", "son", "sa", "ses", "c", "l", "d", "y", "si",
})


# ── Pictogrammes ──────────────────────────────────────────────────


def retirer_emojis(texte: str) -> str:
    """Le texte sans ses pictogrammes, espaces doubles recousus."""
    return _ESPACES.sub(" ", _EMOJIS.sub("", texte or ""))


def limiter_emojis(texte: str, budget: int) -> tuple[str, int]:
    """Garde les ``budget`` premiers pictogrammes, supprime les suivants.

    Rendre le budget restant permet d'appeler la fonction morceau par morceau
    sur un flux : la réponse entière partage un seul quota, où que tombe la
    coupure entre deux tokens.
    """
    if not texte or budget < 0:
        return texte, budget

    morceaux: list[str] = []
    fin = 0
    for trouve in _EMOJIS.finditer(texte):
        morceaux.append(texte[fin:trouve.start()])
        if budget > 0:
            morceaux.append(trouve.group(0))
            budget -= 1
        fin = trouve.end()

    if not morceaux:                       # rien à retirer : texte intact
        return texte, budget
    morceaux.append(texte[fin:])
    return _ESPACES.sub(" ", "".join(morceaux)), budget


# ── Lecture de l'historique ───────────────────────────────────────


def _tours(historique, role: str, combien: int) -> list[str]:
    """Les ``combien`` derniers messages de ``role``, du plus ancien au dernier."""
    if not historique:
        return []
    textes = [
        str(message.get("content") or "").strip()
        for message in historique
        if message.get("role") == role
    ]
    return [texte for texte in textes if texte][-combien:]


def _mots(texte: str) -> list[str]:
    return _MOT.findall(retirer_emojis(texte).lower())


def _porteuse(expression: str) -> bool:
    """L'expression dit-elle quelque chose, ou n'est-elle que de la colle ?"""
    return any(
        mot not in _MOTS_VIDES and len(mot) >= 3
        for mot in expression.split()
    )


def _condenser(phrase: str, maxi: int = 90) -> str:
    phrase = _ESPACES.sub(" ", retirer_emojis(phrase)).strip()
    if len(phrase) <= maxi:
        return phrase
    return phrase[:maxi].rsplit(" ", 1)[0].strip() + "…"


def _signature(phrase: str) -> tuple[str, ...]:
    """Deux formulations d'une même question doivent se reconnaître."""
    return tuple(mot for mot in _mots(phrase) if mot not in _MOTS_VIDES)


def _phrases(texte: str) -> list[str]:
    return [bout.strip() for bout in _FIN_DE_PHRASE.split(texte.strip()) if bout.strip()]


def _est_question(phrase: str) -> bool:
    return "؟" in phrase or "?" in phrase


# ── Ce que le miroir montre ───────────────────────────────────────


def ouvertures_recentes(historique, tours: int = 3, mots: int = 6) -> list[str]:
    """Les premiers mots des dernières réponses — là où le tic s'installe."""
    ouvertures = []
    for message in _tours(historique, "assistant", tours):
        debut = retirer_emojis(message).split()[:mots]
        if debut:
            ouvertures.append(" ".join(debut))
    return ouvertures


def mots_d_ouverture_repetes(historique, tours: int = 3, seuil: int = 2) -> list[str]:
    """Les mots plantés en tête de réponse plus d'une fois de suite.

    C'est ici que le prénom de l'élève est attrapé, sans avoir à le
    translittérer : « زهير » ouvre trois réponses sur quatre, il ressort. Et
    si ce n'est pas le prénom mais « مزيان », c'est un tic tout autant — les
    deux méritent la même interdiction, donc la même détection.
    """
    compte: Counter = Counter()
    for message in _tours(historique, "assistant", tours):
        tete = {
            mot for mot in _mots(message)[:5]
            if mot not in _MOTS_VIDES and len(mot) >= 3
        }
        compte.update(tete)
    return [mot for mot, vus in compte.most_common() if vus >= seuil]


def formules_rabachees(
    historique, tours: int = 4, seuil: int = 2, maxi: int = 5
) -> list[str]:
    """Les suites de mots qui reviennent dans plusieurs réponses d'affilée."""
    messages = _tours(historique, "assistant", tours)
    if len(messages) < seuil:
        return []

    compte: Counter = Counter()
    for message in messages:
        mots = _mots(message)
        vues: set = set()
        for taille in (2, 3, 4):
            vues.update(
                " ".join(mots[debut:debut + taille])
                for debut in range(len(mots) - taille + 1)
            )
        compte.update(expression for expression in vues if _porteuse(expression))

    candidates = sorted(
        (expression for expression, vus in compte.items() if vus >= seuil),
        key=lambda expression: (-compte[expression], -len(expression)),
    )
    # Une tournure courte n'apprend rien de plus que la tournure longue qui la
    # contient : on ne cite que la plus longue.
    gardees: list[str] = []
    for expression in candidates:
        if any(expression in longue for longue in gardees):
            continue
        gardees.append(expression)
        if len(gardees) >= maxi:
            break
    return gardees


def questions_deja_posees(historique, tours: int = 6, maxi: int = 6) -> list[str]:
    """Les questions déjà sorties — reposer l'une d'elles fait tourner en rond.

    La dernière est écartée : elle est encore ouverte, l'élève n'y a pas
    répondu, et `question_ouverte` la présente pour ce qu'elle est. La lister
    ici aussi reviendrait à demander au modèle de l'oublier et de s'y tenir
    dans la même consigne.
    """
    vues: set = set()
    posees: list[str] = []
    for message in _tours(historique, "assistant", tours):
        for phrase in _phrases(message):
            if not _est_question(phrase):
                continue
            signature = _signature(phrase)
            if not signature or signature in vues:
                continue
            vues.add(signature)
            posees.append(_condenser(phrase))
    encore_ouverte = question_ouverte(historique)
    if posees and encore_ouverte and posees[-1] == encore_ouverte:
        posees.pop()
    return posees[-maxi:]


def question_ouverte(historique) -> str:
    """La dernière question posée : c'est à elle que « 7 » ou « ok » répond."""
    derniers = _tours(historique, "assistant", 1)
    if not derniers:
        return ""
    questions = [phrase for phrase in _phrases(derniers[-1]) if _est_question(phrase)]
    return _condenser(questions[-1]) if questions else ""


# ── L'accord entre ce qui se dit et ce qui s'écrit ────────────────
#
# Le tuteur a deux canaux : sa voix, et le tableau. Le prompt leur interdit
# de se DOUBLER — et le modèle lit cette règle au pied de la lettre : il
# écrit au tableau ce qu'il ne dit pas, donc l'élève reçoit des lignes que
# personne ne lui a expliquées. L'autre bord du même défaut : il pose une
# question à l'oral pendant que le tableau en affiche la réponse.
#
# Les deux se repèrent sur la réponse complète, avant qu'elle ne parte.

_BALISES_AFFICHAGE = ("ui", "board", "draw", "schema", "live", "exam_exercise")
_BLOC_AFFICHAGE = re.compile(
    r"<(" + "|".join(_BALISES_AFFICHAGE) + r")>.*?(?:</\1>|$)",
    re.DOTALL | re.IGNORECASE,
)
_OUVERTURE_AFFICHAGE = re.compile(
    r"<(?:" + "|".join(_BALISES_AFFICHAGE) + r")>", re.IGNORECASE
)
#: Une réponse plus longue que ça porte un cours, pas une simple question.
_LONGUEUR_PURE_QUESTION = 400

#: Comment un professeur renvoie à ce qu'il vient d'écrire. Le pendant, pour
#: le tableau, de `_AMORCES_IMAGE` côté session_handler : sans annonce, le
#: tableau s'allume en silence et l'élève recopie sans savoir pourquoi.
_AMORCES_TABLEAU = (
    # français
    "tableau", "je t'écris", "j'écris", "je note", "regarde ce que",
    "voici ce que", "comme tu le vois", "comme tu vois", "ci-dessous",
    # darija / arabe
    "اللوح", "كتبت ليك", "كتبتها", "غادي نكتب", "كنكتب", "نكتب ليك",
    "شوف معايا", "شوف هاد", "شوف اللي", "ها هي", "ها هو",
)


def texte_parle(reponse: str) -> str:
    """La réponse privée de ses blocs d'affichage : ce que l'élève ENTEND."""
    return _BLOC_AFFICHAGE.sub(" ", reponse or "").strip()


def _finit_sur_une_question(texte: str) -> bool:
    """La dernière chose dite est-elle une question posée à l'élève ?"""
    nettoye = retirer_emojis(texte).rstrip()
    # Le modèle referme parfois sur un mot-clé de commande, jamais prononcé.
    nettoye = re.sub(r"[A-Z_]{6,}\s*$", "", nettoye).rstrip()
    return nettoye.endswith(("؟", "?"))


def tour_purement_socratique(reponse: str) -> bool:
    """Ce tour est-il une question à l'élève, et rien d'autre ?

    Un tel tour n'a RIEN à écrire au tableau : la réponse, c'est l'élève qui
    doit la chercher. Forcer un tableau ici revient à la lui montrer.
    """
    if not reponse or _OUVERTURE_AFFICHAGE.search(reponse):
        return False
    parle = texte_parle(reponse)
    return bool(parle) and len(parle) <= _LONGUEUR_PURE_QUESTION and _finit_sur_une_question(parle)


def tableau_non_annonce(reponse: str) -> bool:
    """Un tableau s'affiche sans que l'oral n'en dise un mot.

    Le tableau est muet. Une ligne écrite que le professeur ne commente pas
    est une ligne que l'élève recopie sans la comprendre — et c'est bien ce
    qu'on lui reproche : « des données au tableau qu'il n'explique pas ».
    """
    if not reponse or "show_board" not in reponse:
        return False
    parle = retirer_emojis(texte_parle(reponse)).lower()
    if not parle:
        return True
    return not any(amorce in parle for amorce in _AMORCES_TABLEAU)


def defaut_d_accord(reponse: str) -> str:
    """Le rappel à servir au tour SUIVANT, ou "" si les canaux s'accordent.

    On ne peut plus rien pour le tour qui vient de partir — la voix est déjà
    dite. Mais le défaut nommé au tour d'après se corrige, exactement comme
    les répétitions se corrigent par le miroir.
    """
    if tableau_non_annonce(reponse):
        return (
            "Au tour précédent, tu as affiché un tableau sans en dire un mot à "
            "l'oral. Le tableau est MUET : l'élève a recopié des lignes que "
            "personne ne lui a expliquées. Cette fois, annonce ce que tu écris "
            "(« شوف اللوح », « كتبت ليك… ») et commente-le en une phrase au "
            "moins, avec tes mots."
        )
    return ""


def bloc_memoire(historique) -> str:
    """Le miroir à coller au prompt système. Vide tant qu'il n'a rien à dire."""
    ouvertures = ouvertures_recentes(historique)
    tics = mots_d_ouverture_repetes(historique)
    formules = formules_rabachees(historique)
    posees = questions_deja_posees(historique)
    ouverte = question_ouverte(historique)

    lignes: list[str] = []
    if ouvertures:
        # Le renvoi mot pour mot du tour précédent est le pire des cas : il
        # est arrivé sur un message tronqué par la reconnaissance vocale
        # (« كتوقع في »), que le modèle n'a pas su lire — alors il a rejoué
        # sa réponse. L'élève l'avait déjà lue.
        lignes.append(
            "• Ta réponse précédente a déjà été lue par l'élève. Ne la renvoie "
            "JAMAIS à l'identique, même partiellement.\n"
            "  → si son message est incompréhensible ou coupé en plein milieu "
            "(la reconnaissance vocale tronque souvent), dis-le-lui et demande-"
            "lui de répéter. Recevoir deux fois le même paragraphe lui apprend "
            "que personne ne l'écoute."
        )
    if ouvertures:
        citees = " | ".join(f"« {o} »" for o in ouvertures)
        lignes.append(
            f"• Tes dernières ouvertures : {citees}\n"
            "  → commence CETTE réponse autrement. Pas de variante déguisée."
        )
    if tics:
        lignes.append(
            "• Mots que tu replaces en tête à chaque fois : "
            + ", ".join(f"« {mot} »" for mot in tics[:4])
            + "\n  → aucun d'eux dans tes cinq premiers mots. Le prénom de "
            "l'élève compris : on ne s'adresse pas à quelqu'un par son prénom "
            "trois phrases de suite."
        )
    if formules:
        lignes.append(
            "• Formules que tu rabâches : "
            + ", ".join(f"« {f} »" for f in formules)
            + "\n  → si c'est un encouragement ou une transition, change-la : "
            "un compliment qui revient à chaque tour ne récompense plus rien. "
            "Si c'est un terme scientifique, garde le terme mais ne rebâtis "
            "pas la même phrase autour."
        )
    if posees:
        lignes.append(
            "• Questions déjà posées :\n"
            + "\n".join(f"    – {q}" for q in posees)
            + "\n  → l'élève y a déjà répondu. Ne les repose pas : avance."
        )
    if ouverte:
        lignes.append(
            f"• Question restée ouverte : « {ouverte} »\n"
            "  → une réponse courte de l'élève porte SUR CELLE-CI et sur "
            "aucune autre. Si elle n'y colle pas, demande à quoi il répond ; "
            "n'invente ni énoncé ni valeur chiffrée pour lui donner raison."
        )

    if not lignes:
        return ""
    return (
        "\n\n[MIROIR DE TES DERNIERS TOURS — LIS-LE AVANT D'ÉCRIRE]\n"
        "Calculé sur TES propres réponses. Un élève décroche à la seconde où "
        "il reconnaît la formule : ce qui est cité ici est INTERDIT dans la "
        "réponse que tu écris maintenant.\n"
        + "\n".join(lignes)
        + "\n"
    )
