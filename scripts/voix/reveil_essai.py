"""Réveille le kernel d essai (compte choisi par l env : compte 2 = KAGGLE_USERNAME=$KAGGLE2_USERNAME KAGGLE_API_TOKEN=$KAGGLE2_API_TOKEN, sinon ferdaous04) et écrit /tmp/essai_acces.json {url, jeton} (16 novembre 2026).
À lancer sur le VPS depuis /opt/moalim/backend, env /etc/moalim/backend.env chargé, KAGGLE_TTS_SOCLE="" PROPRIETAIRE=ferdaous04."""
import json, os, sys
sys.path.insert(0, "/opt/moalim/backend")
import app.services.kaggle_tts as K
PROPRIETAIRE = os.environ.get("PROPRIETAIRE", "ferdaous04")
_c = K.construire_kernel
def construire_kernel(dossier, *a, **k):
    d = _c(dossier, *a, **k)
    p = dossier / "kernel-metadata.json"
    meta = json.loads(p.read_text(encoding="utf-8"))
    u = K.settings.kaggle_username
    meta["kernel_sources"] = [s.replace(f"{u}/", f"{PROPRIETAIRE}/", 1) for s in meta["kernel_sources"]]
    p.write_text(json.dumps(meta, indent=1), encoding="utf-8")
    return d
K.construire_kernel = construire_kernel
from scripts.kaggle_tts import _reveiller_essai
url, jeton, _ = _reveiller_essai()
json.dump({"url": url, "jeton": jeton}, open("/tmp/essai_acces.json", "w"))
os.chmod("/tmp/essai_acces.json", 0o600)
print("PRET", flush=True)
