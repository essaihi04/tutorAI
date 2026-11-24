#!/bin/bash
# suivre_partie.sh N PARTIE : attend le lot academy-tts-<partie> du compte N, le récupère dans att_ et garde la sortie brute
N=$1; P=$2; cd /srv/corpus_v4/voix_lot
for i in $(seq 1 600); do
  s=$(KERNEL_LOT=academy-tts-$P bash lancer_lot.sh $N statut 2>&1 | tail -1)
  case "$s" in *COMPLETE*|*ERROR*|*CANCEL*) break;; esac; sleep 60
done
echo "$P statut : $s $(date)"
KERNEL_LOT=academy-tts-$P bash lancer_lot.sh $N recuperer 2>&1 | tail -3
d=$(ls -dt /tmp/kaggle_lot_sortie_* | head -1); rm -rf /tmp/sortie_$P; cp -r "$d" /tmp/sortie_$P
python3 - "$P" <<"PY"
import json, sys
P = sys.argv[1]; r = json.load(open(f"/tmp/sortie_{P}/rapport.json", encoding="utf-8"))
f = {c: [x for n in v["notes"] for x in n["reste"]] for c, v in r.items()}
f = {c: v for c, v in f.items() if v}
json.dump(f, open(f"/srv/corpus_v4/voix_lot/fautes_kaggle_{P}.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
from collections import Counter
st = Counter(n.get("strategie", "normal") for v in r.values() for n in v["notes"])
print(P, "FIN_PARTIE", len(r), "pistes,", len(f), "encore signalées ; stratégies gardées :", dict(st))
PY
