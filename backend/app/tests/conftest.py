"""Ce que la suite de tests n'a pas le droit de salir.

Deux journaux servent d'observation de la PRODUCTION : `visual_gaps.jsonl`
liste les primitives que le validateur a jetées d'une figure, `schema_gaps.jsonl`
les notions que la bibliothèque ne couvre pas. On les relit pour décider quoi
dessiner ensuite — c'est leur seule raison d'être.

Or la suite de tests appelle le validateur avec des figures VOLONTAIREMENT
invalides : une aire sans bornes, un texte sans légende. Chaque exécution y
ajoutait donc ses deux refus, et six jours d'exécutions ont suffi pour que les
fixtures deviennent majoritaires — 150 lignes sur 154, toutes fausses.
`classement()`, dont le travail est de dire quelle primitive manque vraiment
aux élèves, ne classait plus que du décor de test.

Les tests écrivent maintenant dans un fichier jetable. Le journal de
production ne contient plus que ce que des élèves ont réellement provoqué.
"""
from __future__ import annotations

import os
import tempfile
from pathlib import Path

# Posé AVANT l'import des modules applicatifs : ils lisent ces variables au
# moment où ils sont chargés, c'est-à-dire pendant la collecte des tests.
_jetable = Path(tempfile.mkdtemp(prefix="gaps-tests-"))
os.environ.setdefault("VISUAL_GAPS_PATH", str(_jetable / "visual_gaps.jsonl"))
os.environ.setdefault("SCHEMA_GAPS_PATH", str(_jetable / "schema_gaps.jsonl"))
os.environ.setdefault("LIBRE_JOURNAL_PATH", str(_jetable / "libre_journal.jsonl"))
