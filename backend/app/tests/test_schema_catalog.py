"""Le rapprochement entre une séance et un schéma déjà dessiné.

Ce chemin décide si l'élève voit un schéma validé ou un croquis improvisé.
Ses erreurs sont silencieuses : personne ne remarque qu'un mot-clé n'a pas
répondu, on voit seulement un dessin à main levée à la place du bon schéma.
"""

from app.services.schema_catalog import SCHEMA_CATALOG, SCHEMA_IDS, match_schema, schema_title


def test_un_mot_cle_ne_repond_pas_au_milieu_d_un_autre_mot():
    """`exp` est dans « expansion », `ln` dans dix mots : cherchés en
    sous-chaîne, ils proposaient les fonctions exponentielles à un cours de
    géologie."""
    schema_id, _ = match_schema("la dorsale océanique et l'expansion des fonds océaniques")

    assert schema_id == "svt_dorsale_accretion"


def test_le_vrai_cours_d_exponentielle_repond_toujours():
    schema_id, score = match_schema("cours sur la fonction exponentielle et le logarithme népérien")

    assert schema_id == "math_exp_ln"
    assert score >= 2


def test_le_pluriel_et_les_accents_absents_repondent():
    """Un cours parle des « myofibrilles », un élève tape « accretion » sans
    accent : le mot-clé est au singulier et accentué, il doit répondre quand
    même."""
    avec, _ = match_schema("les myofibrilles et le réticulum sarcoplasmique de la fibre musculaire")
    sans_accent, _ = match_schema("la dorsale et l'accretion oceanique")

    assert avec == "svt_fibre_musculaire"
    assert sans_accent == "svt_dorsale_accretion"


def test_un_contexte_vide_ou_hors_sujet_ne_propose_rien():
    assert match_schema("") == (None, 0)
    assert match_schema("   ") == (None, 0)
    assert match_schema("bonjour ça va merci") == (None, 0)


def test_tout_identifiant_propose_existe_vraiment():
    """Proposer un identifiant absent de la bibliothèque afficherait du vide."""
    for entry in SCHEMA_CATALOG:
        contexte = " ".join(entry["keywords"][:3])
        schema_id, _ = match_schema(contexte)
        assert schema_id is None or schema_id in SCHEMA_IDS


def test_chaque_schema_porte_des_mots_cles_et_un_titre():
    for entry in SCHEMA_CATALOG:
        assert entry["keywords"], f"{entry['id']} n'a aucun mot-clé : introuvable"
        assert schema_title(entry["id"]) == entry["title"]


def test_le_mot_cle_le_plus_precis_l_emporte():
    """« fibre musculaire » designe une figure, « muscle » designe un chapitre.

    Sans ponderation ni depart au plus long, les deux schemas du muscle
    arrivaient a egalite et c'est l'ordre du fichier qui tranchait : un cours
    sur la fibre musculaire se voyait proposer le sarcomere.
    """
    fibre, _ = match_schema("structure du muscle strié, faisceaux et fibre musculaire")
    sarcomere, _ = match_schema("contraction musculaire, actine et myosine, strie Z")

    assert fibre == "svt_fibre_musculaire"
    assert sarcomere == "svt_muscle_sarcomere"
