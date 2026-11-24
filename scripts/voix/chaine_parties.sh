#!/bin/bash
# chaine.sh N P1 P2 P3 ... : sur le compte N, attend la fin de P1 (déjà lancée), puis lance et suit P2, puis P3...
N=$1; shift; cd /srv/corpus_v4/voix_lot
prec=$1; shift
for P in "$@"; do
  until grep -q FIN_PARTIE /tmp/suivre_$prec.log 2>/dev/null; do sleep 60; done
  LISTE=/srv/corpus_v4/voix_lot/liste_$P.json KERNEL_LOT=academy-tts-$P bash lancer_lot.sh $N 2>&1 | tail -1 > /tmp/suivre_$P.log
  bash suivre_partie.sh $N $P >> /tmp/suivre_$P.log 2>&1
  prec=$P
done
