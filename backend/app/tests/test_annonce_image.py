"""Le tuteur annonce une image : est-ce que le systeme l'entend ?

Le bug d'origine : la detection cherchait CINQ phrases francaises litterales
(« regarde cette image »...) alors que la regle #0 du prompt impose au tuteur
de parler darija en alphabet arabe. Les deux consignes se contredisaient. Le
modele obeissait a la plus visible, disait a l'eleve de regarder une image,
et rien ne s'affichait.
"""
from app.websockets.session_handler import _annonce_une_image


def _detecte(phrase):
    return _annonce_une_image(phrase.lower())


# -- Le cas qui echouait ------------------------------------------

def test_une_annonce_en_darija_est_entendue():
    """Le coeur du bug : c'est ainsi que le tuteur parle vraiment."""
    assert _detecte("واخا، شوف هاد الصورة باش تفهم مزيان la glycolyse")


def test_les_variantes_courantes_du_darija():
    for phrase in (
        "شوفي هاد الصورة",
        "شوفو هاد الصورة",
        "تأمل هاد الرسم مزيان",
        "ها هي الصورة اللي كتبين العملية",
        "هاد الشكل كيبين ليك المراحل",
    ):
        assert _detecte(phrase), phrase


# -- Ce qui marchait deja ne doit pas casser ----------------------

def test_les_annonces_francaises_marchent_toujours():
    for phrase in (
        "Regarde cette image pour mieux comprendre",
        "Observe ce schema attentivement",
        "Voici une illustration de la glycolyse",
    ):
        assert _detecte(phrase), phrase


def test_la_casse_ne_compte_pas():
    assert _detecte("REGARDE CETTE IMAGE")


# -- Pas de faux positifs -----------------------------------------

def test_parler_d_une_image_n_est_pas_l_annoncer():
    """Afficher une ressource que le tuteur n'a pas annoncee surprend
    l'eleve autant que l'inverse."""
    for phrase in (
        "الصورة اللي شفتي البارح كانت واضحة",
        "une image vaut mille mots",
        "on va parler de la glycolyse",
        "",
    ):
        assert not _detecte(phrase), phrase
