"""Ce que le tuteur SAIT avoir sous la main quand l'élève pose sa question.

La bibliothèque visuelle est arrivée par couches — schémas, croquis au crayon,
scènes animées, modèle 3D, simulations de cours — et chaque couche avait son
propre chemin d'accès. En question libre, où la séance n'a ni leçon ni
objectif, la plupart de ces chemins ne s'ouvraient jamais : le tuteur
répondait en prose ou redessinait à main levée une figure qui existait déjà.

Ces tests vérifient les deux choses qui rendent ce câblage utile : le
rapprochement trouve les bonnes ressources, et l'INTENTION de l'élève —
dessiner, animer, tourner autour — choisit laquelle des cinq part à l'écran.
"""

from app.services.scientific_presets import SCIENTIFIC_PRESETS
from app.services.scientific_visual_skill import MODELES_3D
from app.services.visual_shortlist import (
    apparier_modeles_3d,
    apparier_presets,
    apparier_simulations,
    bloc_visuels_disponibles,
    carte_des_visuels,
    demande_de_la_profondeur,
    demande_un_croquis,
)


# ── Le rapprochement, surface par surface ─────────────────────────────

def test_une_scene_animee_se_rapproche_d_une_notion():
    """Les presets n'avaient AUCUN matcher : ils étaient recopiés dans le
    prompt, et le modèle devait se souvenir qu'un identifiant collait."""
    trouves = dict(apparier_presets("la chimiosmose et le gradient de protons"))

    assert "svt_ch1_chimiosmose" in trouves


def test_un_mot_de_chapitre_seul_ne_sort_aucune_scene():
    """« énergie » est dans la moitié du programme : sortir une scène sur ce
    seul mot imposerait une animation sans rapport avec la question."""
    assert apparier_presets("l'énergie") == []


def test_le_modele_3d_devient_atteignable_par_la_notion():
    """Il fallait auparavant que l'élève prononce lui-même « mitochondrie »
    ET « 3D » pour qu'un motif du routeur le débloque."""
    trouves = dict(apparier_modeles_3d("ultrastructure de la mitochondrie"))

    assert "mitochondrion" in trouves


def test_une_simulation_de_cours_est_nommee_avant_d_etre_demandee():
    """`OUVRIR_SIMULATION` était un pari : le tuteur promettait, le serveur
    cherchait après coup, et en question libre il ne trouvait rien."""
    ressources = [
        {
            "resource_type": "simulation",
            "title": "Facteurs cinétiques",
            "concepts": ["catalyseur", "température"],
        },
        {
            "resource_type": "image",
            "title": "Catalyseur en poudre",
            "concepts": ["catalyseur"],
        },
    ]

    trouves = apparier_simulations("effet du catalyseur sur la vitesse", ressources)

    assert [r["title"] for r in trouves] == ["Facteurs cinétiques"]


def test_une_ressource_qui_n_est_pas_une_simulation_ne_passe_pas():
    ressources = [{"resource_type": "video", "title": "Catalyseur", "concepts": ["catalyseur"]}]

    assert apparier_simulations("le catalyseur", ressources) == []


# ── L'intention de l'élève ────────────────────────────────────────────

def test_dessine_moi_ca_est_une_demande_de_croquis():
    assert demande_un_croquis("dessine-moi la mitochondrie")
    assert demande_un_croquis("schématise le cycle de Krebs au tableau")


def test_la_demande_de_croquis_se_reconnait_en_arabizi():
    """« rsem lia » est ce que la reconnaissance vocale produit telle quelle ;
    l'exiger en français aurait renvoyé la planche de référence."""
    assert demande_un_croquis("rsem lia chi croquis dyal la mitochondrie")


def test_expliquer_n_est_pas_dessiner():
    assert not demande_un_croquis("explique-moi la respiration cellulaire")


def test_la_profondeur_se_distingue_du_reste():
    assert demande_de_la_profondeur("montre-la en 3D, je veux tourner autour")
    assert not demande_de_la_profondeur("montre-moi la mitochondrie")


# ── La carte, et la règle qu'elle écrit ───────────────────────────────

def test_la_carte_separe_le_croquis_de_la_planche_de_reference():
    """Les deux versions de la même notion existent ; les confondre annule
    tout l'intérêt d'avoir fait les deux."""
    carte = carte_des_visuels(
        "svt la mitochondrie ses crêtes et sa matrice",
        "dessine-moi la mitochondrie",
    )

    assert carte["croquis"] is not None
    assert carte["croquis"][0].startswith("svt_croquis_")
    assert carte["reference"] is not None
    assert not carte["reference"][0].startswith("svt_croquis_")


def test_le_bloc_envoie_au_croquis_quand_l_eleve_dit_dessine():
    bloc = bloc_visuels_disponibles(
        "svt la mitochondrie ses crêtes et sa matrice",
        "dessine-moi la mitochondrie",
    )

    assert "CROQUIS AU CRAYON" in bloc
    assert "Il demande un DESSIN" in bloc


def test_le_bloc_envoie_a_la_scene_animee_quand_l_eleve_veut_du_mouvement():
    """Une image fixe ne répond pas à « fais-la bouger » — c'est la boucle
    observée en séance, où le tuteur repromettait une animation à chaque tour."""
    bloc = bloc_visuels_disponibles(
        "chimie cinétique effet du catalyseur",
        "anime-moi l'effet du catalyseur",
    )

    assert "SCÈNE ANIMÉE" in bloc
    assert "chem_ch1_facteurs_cinetiques" in bloc
    assert "Il demande à voir BOUGER" in bloc


def test_le_bloc_envoie_au_modele_3d_quand_l_eleve_veut_tourner_autour():
    bloc = bloc_visuels_disponibles(
        "svt la mitochondrie ses crêtes et sa matrice",
        "montre-la en 3D, je veux tourner autour",
    )

    assert "MODÈLE 3D" in bloc
    assert "Il demande à TOURNER AUTOUR" in bloc


def test_le_visuel_part_meme_quand_l_eleve_n_a_rien_demande():
    """L'élève ignore que ces figures existent : il ne les réclamera jamais.
    Attendre sa demande, c'est garder la bibliothèque fermée."""
    bloc = bloc_visuels_disponibles(
        "svt la mitochondrie ses crêtes et sa matrice",
        "je comprends pas trop ce chapitre",
    )

    assert "AFFICHE-EN UNE MAINTENANT" in bloc
    assert "TU N'ATTENDS PAS QU'ON TE LE DEMANDE" in bloc
    assert "AUCUNE demande particulière" in bloc


def test_le_tour_socratique_reste_sans_tableau():
    """Afficher pendant qu'on interroge, c'est montrer la réponse. C'est la
    seule exception, et l'affichage par défaut ne doit pas l'écraser."""
    bloc = bloc_visuels_disponibles(
        "svt la mitochondrie ses crêtes et sa matrice",
        "explique-moi la mitochondrie",
    )

    assert "SEULE EXCEPTION" in bloc
    assert "POSES une question" in bloc


def test_une_figure_deja_a_l_ecran_n_est_pas_renvoyee():
    """Le seul défaut que l'affichage automatique produit tout seul : le
    contexte bouge peu, la même ressource ressort, et le tableau clignote."""
    contexte = "svt la mitochondrie ses crêtes et sa matrice"
    schema_id = carte_des_visuels(contexte)["reference"][0]

    bloc = bloc_visuels_disponibles(contexte, "continue", deja_affiches=[schema_id])

    assert "DÉJÀ À L'ÉCRAN" in bloc
    assert "Ne les RENVOIE pas" in bloc
    assert schema_id in bloc  # elle reste nommée : on peut la commenter


def test_sans_historique_aucune_regle_de_repetition_n_encombre_le_bloc():
    bloc = bloc_visuels_disponibles(
        "svt la mitochondrie ses crêtes et sa matrice", "explique-moi ça"
    )

    assert "DÉJÀ À L'ÉCRAN" not in bloc


def test_le_bloc_reste_vide_quand_rien_ne_couvre_la_notion():
    """Répéter « aucune ressource » à chaque tour occuperait le contexte sans
    rien apprendre au modèle, qui sait déjà générer une figure."""
    assert bloc_visuels_disponibles("bonjour ça va aujourd'hui", "bonjour") == ""


def test_la_question_libre_recoit_l_insistance_et_pas_les_autres_modes():
    contexte, demande = "svt la mitochondrie et ses crêtes", "explique-moi la mitochondrie"

    assert "MODE QUESTION LIBRE" in bloc_visuels_disponibles(contexte, demande, insister=True)
    assert "MODE QUESTION LIBRE" not in bloc_visuels_disponibles(contexte, demande)


def test_le_bloc_ne_nomme_que_des_identifiants_qui_existent():
    """Un identifiant inventé n'affiche RIEN : l'élève regarde un écran vide
    pendant que le tuteur lui dit « regarde »."""
    bloc = bloc_visuels_disponibles(
        "svt respiration mitochondrie chaîne respiratoire ATP",
        "montre-moi tout ça",
    )

    def identifiant_de(ligne: str) -> str:
        return ligne.split(":", 1)[1].split("—")[0].strip()

    vus = 0
    for ligne in bloc.splitlines():
        if "SCÈNE ANIMÉE" in ligne:
            assert identifiant_de(ligne) in SCIENTIFIC_PRESETS
            vus += 1
        if "MODÈLE 3D" in ligne:
            assert identifiant_de(ligne) in MODELES_3D
            vus += 1
    assert vus, "la notion la mieux couverte du programme ne sort aucune ressource"


# ── Ce que l'audit du 27 août 2026 a trouvé fermé ─────────────────────

def test_une_demande_de_mouvement_descend_le_seuil_des_scenes():
    """« montre-moi l'onde qui bouge » ne sortait RIEN.

    « onde » est un mot de chapitre : il vaut un point, sous le seuil de deux.
    La scène de propagation restait donc fermée, et le tuteur repartait vers un
    dessin FIXE — c'est-à-dire vers une réponse qui ne répond pas. Face à une
    demande de mouvement, une scène faiblement rapprochée bat une image
    immobile.
    """
    carte = carte_des_visuels("montre-moi l'onde qui bouge", "montre-moi l'onde qui bouge")

    assert carte["veut_mouvement"]
    assert "phys_ch1_propagation_onde" in dict(carte["presets"])


def test_une_courbe_a_tracer_n_est_pas_un_croquis_a_la_craie():
    """Le verbe est le même, la demande ne l'est pas : un croquis au crayon
    est une planche pré-dessinée, il ne peut pas placer les points de la
    fonction que l'élève vient d'écrire."""
    assert not demande_un_croquis("trace la courbe de f(x) = x^2 - 1")
    assert not demande_un_croquis("dessine le graphe de la fonction")
    assert demande_un_croquis("dessine-moi le cycle de Krebs")


def test_un_mot_generique_ne_repeche_pas_une_figure_d_une_autre_matiere():
    """Le repêchage sert à sortir la planche du chapitre quand rien de mieux
    n'existe. « énergie » traverse la moitié du programme : il ne doit pas
    faire sortir les oscillations RLC sur une question de chimie."""
    carte = carte_des_visuels(
        "explique-moi l'énergie d'activation",
        "explique-moi l'énergie d'activation",
    )

    assert (carte["reference"] or ("", 0))[0] != "phys_rlc"
    assert "chem_ch1_energie_activation" in dict(carte["presets"])


def test_l_apostrophe_typographique_ne_ferme_plus_une_scene():
    """Le catalogue écrit « énergie d’activation », l'élève tape « d'activation ».
    `re.escape` compare des caractères : les deux ne se rencontraient jamais."""
    assert "chem_ch1_energie_activation" in dict(
        apparier_presets("comment le catalyseur abaisse l'énergie d'activation")
    )


def test_une_scene_animee_seule_recoit_quand_meme_sa_consigne():
    """Le trou de la chaîne : quand aucun schéma ne couvre la notion mais
    qu'une scène le fait, le bloc annonçait « l'une d'elles part dans cette
    réponse » puis ne disait pas LAQUELLE — et le bloc de génération qui suit
    réclamait un dessin. C'est le dessin improvisé qui partait."""
    bloc = bloc_visuels_disponibles(
        "explique-moi l'énergie d'activation avec un catalyseur",
        "explique-moi l'énergie d'activation avec un catalyseur",
    )

    assert "SCÈNE ANIMÉE" in bloc
    assert "SCHÉMA DE RÉFÉRENCE" not in bloc
    assert "c'est ELLE qui part, pas une figure improvisée" in bloc


def test_la_fonction_ecrite_par_l_eleve_passe_avant_toute_ressource():
    """Aucune planche du chapitre ne contient SA courbe."""
    bloc = bloc_visuels_disponibles(
        "trace la courbe de f(x) = (x^2-4)/(x-2) et explique la limite en 2",
        "trace la courbe de f(x) = (x^2-4)/(x-2) et explique la limite en 2",
    )

    assert "Il a ÉCRIT une fonction à tracer" in bloc
    assert "AUCUNE demande particulière" not in bloc
