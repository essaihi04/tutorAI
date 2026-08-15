"""Découpe de l'ouverture prononcée pendant que le LLM écrit encore.

Se tromper ici s'entend immédiatement : une coupe trop tôt fait dire au prof
une phrase tronquée, une coupe trop tard lui fait avaler tout le paragraphe et
supprime le gain de latence qu'on cherchait.
"""
from app.websockets.session_handler import SessionHandler as S


coupe = S._fin_de_premiere_phrase


def test_trop_court_on_attend_la_suite():
    """Sous 30 caractères, la phrase ne porte rien : on laisse le LLM écrire."""
    assert coupe("Salam Zouhair !") == 0


def test_premiere_phrase_seulement():
    """Deux phrases écrites : seule la première part en synthèse."""
    texte = ("Salam Zouhair, on commence par la genetique. "
             "Ensuite on verra les croisements.")
    assert texte[:coupe(texte)] == "Salam Zouhair, on commence par la genetique."


def test_pas_de_coupe_au_milieu_d_un_nombre():
    """« 12.5 » n'est pas une fin de phrase : il faut un blanc derrière."""
    texte = "On calcule la moyenne des notes obtenues : 12.5 puis 14.5 au total."
    assert texte[:coupe(texte)] == "On calcule la moyenne des notes obtenues :"


def test_deux_points_comptent_comme_une_frontiere():
    """Le prof annonce souvent par « … voici : » — l'intonation s'y prête."""
    texte = "La genetique au 2BAC PC, c'est deux grandes parties : la classique et la moleculaire."
    assert texte[:coupe(texte)] == "La genetique au 2BAC PC, c'est deux grandes parties :"


def test_phrase_sans_ponctuation_n_est_pas_coupee():
    """Plutôt aucune ouverture qu'une ouverture coupée en plein milieu."""
    assert coupe("a" * 400) == 0


def test_ouverture_bornee():
    """Au-delà de la fenêtre, on renonce plutôt que de tout prononcer."""
    texte = "mot " * 100 + "fin."
    assert coupe(texte) == 0


def test_darija_en_caracteres_arabes():
    """La langue d'enseignement doit se découper comme le français."""
    texte = "واخا Zouhair, hadchi mouhim bezzaf f BAC. Nbdaw daba b chi mital."
    assert texte[:coupe(texte)] == "واخا Zouhair, hadchi mouhim bezzaf f BAC."
