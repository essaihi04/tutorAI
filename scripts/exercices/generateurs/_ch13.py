# Outils du ch. 13 (acides-bases) : courbe pH(V) calculée par _chimie.courbe_ph, tableau des indicateurs du cours.
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _chimie import *

# zones de virage données dans le cours (ab_i2_virage)
INDICATEURS = [("Hélianthine", "3,1 – 4,4"), ("Rouge de méthyle", "4,2 – 6,2"), ("BBT", "6,0 – 7,6"), ("Rouge de crésol", "7,2 – 8,8")]


def fig_indicateurs():
    return tableau_texte("Zones de virage de quelques indicateurs colorés", ["Indicateur", "Zone de virage"],
                         [[n, z] for n, z in INDICATEURS], cadre=(8, 0.6))


def fig_ph(titre, Va, Ca, Ct, Vmax, pKa, acide, gradV, nomV="V_B", legende=None):
    """Courbe pH = f(V) d'un dosage, calculée (bilan des charges) ; quadrillage fin en pH pour lire pH_E."""
    pts = courbe_ph(Va, Ca, Ct, Vmax, pKa, acide)
    return courbe_fig(titre, ((0, Vmax, nomV, "mL", gradV), (0, 14, "pH", None, list(range(0, 15)))),
                      [{"f": "ligne", "pts": pts, "lisse": True, "couleur": "cyan", "epais": True}],
                      legende=legende, ratio=0.75)
