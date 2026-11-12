#!/bin/sh
# Refait tout le cours phys_ch13_acides_bases (rien n'est voisé) : build, ajouts, photo, blocs, contrôles, items. Depuis la racine du dépôt.
set -e
export PYTHONIOENCODING=utf-8
D=outils/cours/notes/cours/acides_bases_build; B=outils/cours/notes/cours/methode_blocs; C=backend/data/courses/phys_ch13_acides_bases.json
python3 $D/build.py
python3 $D/ajouts.py
rm -f $B/base/phys_ch13_acides_bases.json
python3 $B/blocs.py base $C
python3 $B/blocs.py appliquer $C $B/ajouts/phys_ch13_acides_bases.json | tail -1
python3 $B/blocs.py verifier $C acides_bases | tail -3
python3 outils/cours/voxtts/controler_cadre.py $C acides_bases | tail -1
python3 outils/cours/voxtts/preparer_reponses.py items $C $D/items_cours.json | tail -1
python3 $B/blocs.py items $C $D/items_blocs.json $D/demos_blocs.json | tail -2
