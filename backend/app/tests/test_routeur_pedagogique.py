"""Une étape, une surface, une action.

Le tuteur pouvait poser une scène, puis une image, puis rouvrir une
simulation dans la même réponse : quatre écrans pour une idée. Ces tests
verrouillent l'ordre de la planche et les deux conditions qui font tout son
intérêt — la 3D seulement si la profondeur compte, la simulation seulement si
manipuler change la compréhension.
"""
from app.services.routeur_pedagogique import (
    ORDRE_PAR_DEFAUT,
    budget_respecte,
    consigne_d_etape,
    forme_attendue,
    manipulation_utile,
    router,
)


TOUT_DISPONIBLE = dict(
    scene_disponible=True,
    image_disponible=True,
    modele_3d_disponible=True,
    simulation_disponible=True,
)


def test_la_scene_est_le_premier_choix():
    etape = router(demande="Explique la propagation d'une onde", **TOUT_DISPONIBLE)

    assert etape.rang == 1
    assert etape.surface == "scene"


def test_sans_scene_on_descend_a_l_image():
    etape = router(
        demande="Explique la structure de la cellule",
        image_disponible=True,
        simulation_disponible=True,
    )

    assert etape.surface == "image"


def test_la_3d_ne_sert_que_si_la_profondeur_compte():
    """Une rotation coûte cher : elle doit apporter ce que le plat ne peut pas."""
    plat = router(demande="Montre la mitochondrie", image_disponible=True, modele_3d_disponible=True)
    profond = router(
        demande="Montre la mitochondrie en 3D pour tourner autour",
        image_disponible=True,
        modele_3d_disponible=True,
    )

    assert plat.surface == "image"
    assert profond.surface == "modele_3d"


def test_l_image_et_la_3d_ne_sortent_jamais_ensemble():
    """La planche l'écrit : A OU B, jamais les deux à la fois."""
    etape = router(
        demande="Fais-moi voir le volume de la molécule, en profondeur",
        image_disponible=True,
        modele_3d_disponible=True,
    )

    assert etape.surface == "modele_3d"
    assert etape.repli != "image"


def test_la_simulation_attend_que_manipuler_serve():
    """Sans paramètre à changer ni mesure à lire, une scène suffit."""
    a_regarder = router(
        demande="C'est quoi la definition d'un allele",
        simulation_disponible=True,
    )
    a_manipuler = router(
        demande="Fais varier la concentration et mesure la vitesse",
        simulation_disponible=True,
    )

    assert a_regarder.surface == "cahier"
    assert a_manipuler.surface == "simulation"


def test_l_eleve_qui_reclame_une_simulation_l_obtient():
    """Le serveur valide le choix du MODÈLE, pas celui de l'élève."""
    etape = router(
        demande="Ouvre la simulation",
        simulation_disponible=True,
        manipulation_exigee=True,
    )

    assert etape.surface == "simulation"


def test_le_cahier_reste_ouvert_quand_rien_n_existe():
    etape = router(demande="Explique-moi les suites numériques")

    assert etape.surface == "cahier"
    assert etape.repli is None


def test_une_surface_deja_vue_ne_se_reprend_pas():
    """Sinon le tuteur repose la même image à chaque tour, faute de mieux."""
    etape = router(
        demande="Explique la propagation d'une onde",
        deja_montre=["scene"],
        **TOUT_DISPONIBLE,
    )

    assert etape.surface != "scene"


def test_toutes_les_surfaces_vues_ramenent_au_cahier():
    etape = router(demande="Explique encore", deja_montre=list(ORDRE_PAR_DEFAUT), **TOUT_DISPONIBLE)

    assert etape.surface == "cahier"
    assert etape.raison == "toutes_les_surfaces_deja_vues"


def test_chaque_etape_porte_une_action_et_un_critere():
    """Un support sans action demandée n'est qu'une illustration."""
    etape = router(demande="Explique la propagation d'une onde", **TOUT_DISPONIBLE)

    assert etape.action_attendue.strip()
    assert etape.critere.strip()
    consigne = consigne_d_etape(etape)
    assert "UNE seule idée nouvelle" in consigne
    assert "AUCUN nouvel écran avant la réponse" in consigne


def test_le_budget_refuse_deux_ressources_principales():
    assert budget_respecte(["scene", "cahier"])
    assert not budget_respecte(["scene", "image"])
    assert not budget_respecte(["scene", "image", "modele_3d", "simulation"])


def test_la_forme_suit_la_famille_de_notions():
    """Le bandeau du bas : chaque famille a la forme qui la sert."""
    assert forme_attendue("les vecteurs et les forces en optique") == "figure_coordonnee"
    assert forme_attendue("le cycle de Krebs, un processus en etapes") == "schema_causal"
    assert forme_attendue("la chute et la vitesse du mobile") == "simulation_mesuree"
    assert forme_attendue("definition d'un allele") == "tableau_ordinaire"


def test_la_mecanique_en_mouvement_appelle_la_mesure():
    assert manipulation_utile("Explique-moi la chute libre d'une bille")
    assert not manipulation_utile("Donne la definition d'un gene")


# ── L'introduction passe avant toute surface ───────────────────────

def test_rien_ne_s_ouvre_avant_que_le_plan_soit_annonce():
    """L'élève doit savoir où on l'emmène avant de regarder un écran."""
    etape = router(
        demande="Fais-moi un cours complet sur les ondes",
        plan_annonce=False,
        **TOUT_DISPONIBLE,
    )

    assert etape.rang == 0
    assert etape.surface == "introduction"
    assert etape.repli == "scene"


def test_le_plan_annonce_rend_la_main_a_l_explication():
    etape = router(
        demande="Fais-moi un cours complet sur les ondes",
        plan_annonce=True,
        **TOUT_DISPONIBLE,
    )

    assert etape.surface == "scene"


def test_la_consigne_d_introduction_demande_le_plan():
    etape = router(demande="Explique les ondes", plan_annonce=False, **TOUT_DISPONIBLE)
    consigne = consigne_d_etape(etape)

    assert "plan" in consigne.lower()
    assert "AUCUN support" in consigne
