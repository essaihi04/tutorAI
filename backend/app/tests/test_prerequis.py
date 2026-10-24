"""La carte des prérequis : chargée, cohérente, retrouvée depuis un titre de séance."""
import json

import pytest

from app.services import prerequis
from app.services.prerequis import (
    NIVEAUX, Prerequis, bloc_candidats, charger, lire_declaration, pour_chapitre, trouver_chapitre,
)


def test_la_carte_officielle_se_charge_et_chaque_entree_a_une_source():
    carte = charger()
    assert len(carte.competences) >= 30
    for p in carte.competences.values():
        assert p.niveau in NIVEAUX
        assert len(p.source) > 15, p.id
        assert p.verification.rstrip().endswith("?"), p.id
    for matiere in ("Physique-Chimie", "Mathématiques", "SVT"):
        assert carte.chapitres[matiere], matiere
        for chapitre, ids in carte.chapitres[matiere].items():
            assert 2 <= len(ids) <= 7, (matiere, chapitre)


def test_les_chapitres_de_la_carte_sont_ceux_du_programme_2bac():
    import pathlib
    racine = pathlib.Path(prerequis.CHEMIN).parent
    carte = charger()
    for fichier, matiere in (("physique.json", "Physique-Chimie"), ("mathematiques.json", "Mathématiques"), ("svt.json", "SVT")):
        programme = json.loads((racine / fichier).read_text(encoding="utf-8"))
        ids = {ch["id"] for dom in programme["domains"] for ch in dom["chapters"]}
        inconnus = set(carte.chapitres[matiere]) - ids
        assert not inconnus, (matiere, inconnus)


def test_un_titre_de_seance_retrouve_son_chapitre_ou_rien():
    assert trouver_chapitre("Physique", "Le dipôle RC : charge d'un condensateur") == "dipole_RC"
    assert trouver_chapitre("PC", "Dosage acido-basique par pH-métrie") == "dosage"
    assert trouver_chapitre("Mathématiques", "Suites numériques : convergence") in ("convergence", "suites_definition", None)
    assert trouver_chapitre("SVT", "Les lois de Mendel") == "lois_mendel"
    assert trouver_chapitre("Physique", "Bonjour") is None
    assert trouver_chapitre("Philosophie", "La liberté") is None


def test_les_prerequis_d_un_chapitre_viennent_des_annees_anterieures():
    rc = pour_chapitre("Physique-Chimie", "dipole_RC")
    assert rc and all(p.niveau in NIVEAUX for p in rc)
    assert any("ériv" in p.titre for p in rc), "le RC exige de savoir dériver"
    assert pour_chapitre("Physique-Chimie", None) == [] and pour_chapitre("Général", "dipole_RC") == []


def test_la_declaration_du_modele_est_filtree_par_la_liste_du_chapitre():
    a = Prerequis("a", "A", "TC", "SVT", "source officielle x", "r", "e", "v ?")
    assert lire_declaration("<eval>faux</eval> <prerequis>a</prerequis> …", [a]) is a
    assert lire_declaration("<prerequis>b</prerequis>", [a]) is None
    assert lire_declaration("rien", [a]) is None


def test_le_bloc_candidats_donne_de_quoi_ouvrir_sans_inventer():
    a = Prerequis("a", "A", "1BAC", "SVT", "source", "phrase clé", "exemple", "question ?")
    bloc = bloc_candidats([a])
    assert "a — A (1re bac)" in bloc and "phrase clé" in bloc and "question ?" in bloc
    assert bloc_candidats([]) == ""


def test_une_carte_incoherente_est_refusee(tmp_path):
    mauvais = tmp_path / "p.json"
    mauvais.write_text(json.dumps({
        "competences": {"a": {"titre": "A", "niveau": "TC", "matiere": "SVT", "source": "s", "rappel": "r", "exemple": "e", "verification": "v ?"}},
        "chapitres": {"SVT": {"x": {"nom": "X", "prerequis": ["a", "fantome"]}}},
    }), encoding="utf-8")
    with pytest.raises(ValueError):
        charger(mauvais)
