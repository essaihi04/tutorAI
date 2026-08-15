"""Recollage des appels d'outils arrivant en fragments.

Mesuré sur deepseek-chat : 181 fragments pour UN seul appel. Se tromper ici
ne se voit pas dans un log — ça produit un tableau vide, ou pire, le contenu
d'un exercice mélangé à celui d'un autre.
"""
import json

import pytest

from app.services.ai_commands import (
    BALISE_POUR_OUTIL,
    NOMS_OUTILS,
    OUTILS,
    AssembleurAppels,
)


def _deltas_pour(nom, arguments, index=0, taille=3, identifiant="call_1"):
    """Découpe un appel comme le fait un vrai flux SSE : nom d'abord,
    puis les arguments par petites tranches."""
    brut = json.dumps(arguments)
    deltas = [{"index": index, "id": identifiant,
               "function": {"name": nom, "arguments": ""}}]
    for i in range(0, len(brut), taille):
        deltas.append({"index": index,
                       "function": {"arguments": brut[i:i + taille]}})
    return deltas


# ── Le contrat ────────────────────────────────────────────────────

def test_chaque_outil_a_une_balise_equivalente():
    """Un outil sans équivalent n'aurait personne pour l'exécuter."""
    assert NOMS_OUTILS == set(BALISE_POUR_OUTIL)


def test_les_schemas_sont_bien_formes():
    for outil in OUTILS:
        f = outil["function"]
        assert outil["type"] == "function"
        assert f["name"] and f["description"]
        params = f["parameters"]
        assert params["type"] == "object"
        for requis in params.get("required", []):
            assert requis in params["properties"], f"{f['name']}: {requis}"


# ── Le recollage ──────────────────────────────────────────────────

def test_appel_recolle_depuis_des_fragments():
    a = AssembleurAppels()
    for d in _deltas_pour("ecrire_au_tableau",
                          {"titre": "Dérivée", "lignes": ["f(x)=x²", "f'(x)=2x"]}):
        a.ajouter([d])

    (appel,) = a.termines()
    assert appel.nom == "ecrire_au_tableau"
    assert appel.arguments["titre"] == "Dérivée"
    assert appel.arguments["lignes"] == ["f(x)=x²", "f'(x)=2x"]
    assert appel.connu and appel.balise == "board"


def test_fragments_d_un_caractere():
    """Le cas réel : deepseek découpe jusqu'à l'accolade près."""
    a = AssembleurAppels()
    for d in _deltas_pour("proposer_suites",
                          {"suggestions": ["Oui", "Non"]}, taille=1):
        a.ajouter([d])

    (appel,) = a.termines()
    assert appel.arguments["suggestions"] == ["Oui", "Non"]


def test_deux_appels_entrelaces_ne_se_melangent_pas():
    """LE piège : sans indexation, les arguments des deux se concatènent."""
    a = AssembleurAppels()
    un = _deltas_pour("ecrire_au_tableau", {"titre": "A", "lignes": ["1"]},
                      index=0, identifiant="call_a")
    deux = _deltas_pour("poser_exercice", {"lignes": [{"q": "B"}]},
                        index=1, identifiant="call_b")
    # Entrelacement strict, comme dans un vrai flux.
    for g, d in zip(un, deux):
        a.ajouter([g, d])
    for reste in un[len(deux):] + deux[len(un):]:
        a.ajouter([reste])

    premier, second = a.termines()
    assert premier.nom == "ecrire_au_tableau"
    assert premier.arguments == {"titre": "A", "lignes": ["1"]}
    assert second.nom == "poser_exercice"
    assert second.arguments == {"lignes": [{"q": "B"}]}


def test_ordre_par_index_pas_par_arrivee():
    a = AssembleurAppels()
    for d in _deltas_pour("poser_exercice", {"lignes": []}, index=1):
        a.ajouter([d])
    for d in _deltas_pour("ecrire_au_tableau", {"titre": "T", "lignes": []}, index=0):
        a.ajouter([d])

    assert [x.nom for x in a.termines()] == ["ecrire_au_tableau", "poser_exercice"]


def test_json_tronque_est_ecarte():
    """Mieux vaut un tableau absent qu'une commande à moitié lue."""
    a = AssembleurAppels()
    a.ajouter([{"index": 0, "function": {"name": "ecrire_au_tableau",
                                         "arguments": '{"titre": "coup'}}])
    assert a.termines() == []


def test_arguments_vides_valent_objet_vide():
    a = AssembleurAppels()
    a.ajouter([{"index": 0, "function": {"name": "afficher_schema", "arguments": ""}}])

    (appel,) = a.termines()
    assert appel.arguments == {}


def test_appel_sans_nom_ignore():
    a = AssembleurAppels()
    a.ajouter([{"index": 0, "function": {"arguments": '{"titre": "x"}'}}])
    assert a.termines() == []


def test_outil_inconnu_signale_mais_pas_perdu():
    """On le décode quand même : c'est l'appelant qui décide d'y renoncer."""
    a = AssembleurAppels()
    for d in _deltas_pour("faire_le_cafe", {"sucre": 2}):
        a.ajouter([d])

    (appel,) = a.termines()
    assert appel.connu is False and appel.balise == ""


@pytest.mark.parametrize("bruit", [None, [], [None], ["texte"], [{}]])
def test_le_bruit_ne_fait_rien_lever(bruit):
    """Un flux abîmé ne doit jamais interrompre la réponse du prof."""
    a = AssembleurAppels()
    a.ajouter(bruit)
    assert a.termines() == []


def test_index_absent_retombe_sur_la_position():
    """Tous les fournisseurs ne remplissent pas `index`."""
    a = AssembleurAppels()
    a.ajouter([{"function": {"name": "afficher_schema",
                             "arguments": '{"schema_id": "mitose"}'}}])

    (appel,) = a.termines()
    assert appel.arguments["schema_id"] == "mitose"


def test_reinitialiser_vide_l_etat():
    a = AssembleurAppels()
    for d in _deltas_pour("afficher_schema", {"schema_id": "x"}):
        a.ajouter([d])
    a.reinitialiser()
    assert a.termines() == []
