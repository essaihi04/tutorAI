"""(VPS) Extraits à écouter : une même phrase dite avec plusieurs écritures d'un mot (skill prononciation).

Usage, sur le VPS, kernel d'essai réveillé (accès dans /tmp/essai_acces.json, voir reveil_essai_compte2.py) :
  cd /opt/moalim/backend && .venv/bin/python ecoute_prononciation.py "PHRASE avec {} à la place du mot" ecriture1 ecriture2 ...
Écrit /tmp/ecoute_<n>_<ecriture>.wav (deux essais par écriture) et affiche ce que MoulSot entend.
Attention : MoulSot ne connaît pas non plus les mots rares ; c'est l'oreille de l'utilisateur qui choisit.
Exemple (16/11/2026) : "quatre virgule six milli{} par mètre، و sigma كتساوي huit {} par mètre." siemens simens "si mènsse"
"""
import json, re, sys
import httpx

A = json.load(open("/tmp/essai_acces.json"))
H = {"Authorization": "Bearer " + A["jeton"]}
phrase, ecritures = sys.argv[1], sys.argv[2:]
for e in ecritures:
    t = phrase.replace("{}", e)
    for n in (1, 2):
        r = httpx.post(A["url"] + "/tts", json={"texte": t, "langue": "ma", "pas_flow": 10}, headers=H, timeout=300)
        f = "/tmp/ecoute_%d_%s.wav" % (n, re.sub(r"\W+", "_", e))
        open(f, "wb").write(r.content)
        s = httpx.post(A["url"] + "/stt", params={"langue": "ma"}, content=r.content, headers=H, timeout=120)
        print(f, "=>", s.json().get("texte") if s.status_code == 200 else s.status_code, flush=True)
