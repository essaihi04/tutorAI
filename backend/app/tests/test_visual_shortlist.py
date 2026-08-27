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
