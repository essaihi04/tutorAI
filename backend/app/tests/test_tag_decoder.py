"""Le vocabulaire d'affichage, et son décodage.

Le test le plus important est `test_identique_a_l_ancienne_liste` : il rejoue
mot pour mot les 14 substitutions qui étaient recopiées dans le handler et
vérifie que le décodeur produit EXACTEMENT le même texte. Sans lui, centraliser
serait un pari.
"""
import json
import re

import pytest

from app.services.tag_decoder import (
    BALISES,
    extraire,
    roles_ui,
    retirer_balises,
    texte_parle,
)


def _ancienne_implementation(texte: str) -> str:
    """Copie conforme de ce que faisait `_sanitize_history_content`."""
    for b in ("ui", "board", "draw", "schema", "live", "exam_exercise", "suggestions"):
        texte = re.sub(rf"<{b}>[\s\S]*?</{b}>", "", texte, flags=re.DOTALL)
        texte = re.sub(rf"<{b}>[\s\S]*", "", texte, flags=re.DOTALL)
    return texte


CORPUS = [
    "",
    "Une explication sans aucune balise.",
    'Voici : <board>{"title":"T","lines":[]}</board> et la suite.',
    'Avant <ui>{"type":"qcm"}</ui> milieu <ui>{"type":"show_live"}</ui> apres.',
    'Coupe en plein vol <ui>{"title":"a mo',                 # balise jamais fermee
    '<suggestions>["a","b"]</suggestions>',
    'Deux familles <draw>{"a":1}</draw> puis <schema>svt_mitose</schema>.',
    'Texte <exam_exercise>genetique</exam_exercise> fin.',
    '<live>{"steps":[]}</live>',
    'Imbrication trompeuse <board>{"lines":["<ui> pas une balise"]}</board>',
    "Un < seul, et un <inconnu>bloc</inconnu> qui n'est pas du vocabulaire.",
    'Multiligne <board>{"title":"T",\n"lines":[\n1,2\n]}</board> suite.',
]


@pytest.mark.parametrize("texte", CORPUS)
def test_identique_a_l_ancienne_liste(texte):
    """Centraliser ne doit RIEN changer au texte produit."""
    assert retirer_balises(texte) == _ancienne_implementation(texte)


def test_le_vocabulaire_est_complet():
    """Les sept balises du protocole, ni plus ni moins."""
    assert set(BALISES) == {
        "ui", "board", "draw", "schema", "live", "exam_exercise", "suggestions",
    }


# ── Extraction ────────────────────────────────────────────────────

def test_extraction_dans_l_ordre_du_texte():
    texte = ('debut <board>{"a":1}</board> milieu '
             '<suggestions>["x"]</suggestions> fin')
    blocs = extraire(texte)
    assert [b.balise for b in blocs] == ["board", "suggestions"]
    assert blocs[0].donnees == {"a": 1}
    assert blocs[1].donnees == ["x"]


def test_json_illisible_ne_leve_pas():
    """Une réponse abîmée dégrade l'affichage, elle n'arrête pas le cours."""
    (bloc,) = extraire('<board>ceci n\'est pas du json</board>')
    assert bloc.lisible is False and bloc.donnees is None
    assert bloc.brut == "ceci n'est pas du json"


def test_balise_ouverte_non_extraite_mais_retiree():
    """Un demi-JSON ne doit jamais partir dans le chat de l'élève."""
    texte = 'Explication <ui>{"titre":"cou'
    assert extraire(texte) == []
    assert texte_parle(texte) == "Explication"


# ── Le piège : à quoi sert vraiment un <ui> ───────────────────────

def test_ui_show_live_est_un_tableau():
    """C'est l'erreur que ce module existe pour empêcher."""
    assert roles_ui({"type": "show_live", "lines": []}) == {"tableau"}


def test_ui_show_board_est_un_tableau():
    assert roles_ui({"type": "show_board"}) == {"tableau"}


def test_ui_qcm_est_un_exercice():
    assert roles_ui({"lines": [{"type": "qcm", "q": "?"}]}) == {"exercice"}


@pytest.mark.parametrize("primitive", ["write", "draw", "arrow", "zoom", "rect"])
def test_les_primitives_de_trace_signent_un_tableau(primitive):
    """Le modèle omet parfois le sous-type mais dessine quand même."""
    assert roles_ui({"lines": [{"type": primitive}]}) == {"tableau"}


def test_un_qcm_affiche_au_tableau_porte_LES_DEUX_roles():
    """La forme reellement emise : show_board (ou) + qcm (quoi).

    Trancher pour un seul role ferait compter cet exercice comme un tableau,
    et personne ne verrait que le prof a bien pose une question.
    """
    donnees = {"type": "show_board", "lines": [{"type": "qcm"}]}
    assert roles_ui(donnees) == {"tableau", "exercice"}


def test_sous_type_profondement_imbrique():
    donnees = {"whiteboard": {"content": {"lines": [{"type": "show_live"}]}}}
    assert roles_ui(donnees) == {"tableau"}


@pytest.mark.parametrize("valeur", [None, {}, [], "texte", 42, {"type": 3}])
def test_roles_ui_ne_leve_jamais(valeur):
    assert roles_ui(valeur) <= {"tableau", "exercice"}


# ── La prose ──────────────────────────────────────────────────────

def test_texte_parle_ne_garde_que_la_prose():
    texte = ('Salam Zouhair ! <ui>{"type":"show_live"}</ui> '
             'On commence. <suggestions>["oui"]</suggestions>')
    assert texte_parle(texte) == "Salam Zouhair !  On commence."


def test_texte_parle_sur_une_reponse_vide():
    assert texte_parle("") == ""
    assert texte_parle('<board>{"a":1}</board>') == ""


def test_cas_reel_deux_ui_un_tableau_un_qcm():
    """La forme exacte mesurée sur le prompt de production."""
    tableau = json.dumps({"type": "show_live", "lines": [{"type": "write"}]})
    qcm = json.dumps({"type": "show_board", "lines": [{"type": "qcm"}]})
    texte = f'Explication. <ui>{tableau}</ui> Question : <ui>{qcm}</ui>'

    roles = [roles_ui(b.donnees) for b in extraire(texte) if b.balise == "ui"]
    assert roles == [{"tableau"}, {"tableau", "exercice"}]
    assert texte_parle(texte) == "Explication.  Question :"
