"""
Pointe le backend vers l'API Academy TTS qui vient de démarrer dans Colab.

Le tunnel trycloudflare change d'URL ET de jeton à CHAQUE lancement du
notebook : plutôt que d'éditer backend/.env à la main (et d'oublier une ligne
sur deux), on colle ici les deux valeurs affichées par la cellule 5.

    python scripts/set_academy_tts.py \
        https://combines-checking-guests-boom.trycloudflare.com \
        c4UzKjMkUzPQNcnVpdFYGZJXPEjcly2k

Sans argument, le script relit backend/.env et teste seulement l'API.
Le backend lit .env au démarrage (Settings est en lru_cache) : il faut le
redémarrer après avoir lancé ce script.
"""
from __future__ import annotations

import json
import sys
import urllib.error
import urllib.request
from pathlib import Path

ENV_PATH = Path(__file__).resolve().parents[1] / "backend" / ".env"

# Les seules clés que ce script possède ; le reste du .env n'est pas touché.
_CLES = ("ACADEMY_TTS_URL", "ACADEMY_TTS_TOKEN", "TTS_DISABLED")


def ecrire_env(url: str, jeton: str) -> None:
    valeurs = {
        "ACADEMY_TTS_URL": url.rstrip("/"),
        "ACADEMY_TTS_TOKEN": jeton,
        # Sans ça, tts_disabled=1 couperait la voix quel que soit le tunnel.
        "TTS_DISABLED": "0",
    }
    lignes = ENV_PATH.read_text(encoding="utf-8").splitlines() if ENV_PATH.exists() else []
    vues = set()
    for i, ligne in enumerate(lignes):
        cle = ligne.split("=", 1)[0].strip()
        if cle in valeurs:
            lignes[i] = f"{cle}={valeurs[cle]}"
            vues.add(cle)
    manquantes = [c for c in _CLES if c not in vues]
    if manquantes:
        if lignes and lignes[-1].strip():
            lignes.append("")
        lignes.append("# Academy Darija-FR TTS (notebook Colab)")
        lignes += [f"{c}={valeurs[c]}" for c in manquantes]

    ENV_PATH.parent.mkdir(parents=True, exist_ok=True)
    ENV_PATH.write_text("\n".join(lignes) + "\n", encoding="utf-8")
    print(f"ecrit dans {ENV_PATH}")
    for c in _CLES:
        affiche = valeurs[c] if c != "ACADEMY_TTS_TOKEN" else valeurs[c][:6] + "…"
        print(f"  {c}={affiche}")


def lire_env() -> tuple[str, str]:
    if not ENV_PATH.exists():
        return "", ""
    url = jeton = ""
    for ligne in ENV_PATH.read_text(encoding="utf-8").splitlines():
        cle, _, val = ligne.partition("=")
        if cle.strip() == "ACADEMY_TTS_URL":
            url = val.strip()
        elif cle.strip() == "ACADEMY_TTS_TOKEN":
            jeton = val.strip()
    return url, jeton


def tester(url: str, jeton: str) -> bool:
    """/health ne demande pas de jeton, /voices si — les deux comptent :
    un tunnel vivant avec un mauvais jeton donne un 401 sur chaque phrase."""
    base = url.rstrip("/")
    try:
        with urllib.request.urlopen(f"{base}/health", timeout=20) as r:
            sante = json.loads(r.read().decode())
        print("health :", sante)
    except Exception as e:
        print(f"/health injoignable ({type(e).__name__}: {e})")
        print("  -> la cellule 5 du notebook tourne-t-elle toujours ?")
        return False

    req = urllib.request.Request(
        f"{base}/voices", headers={"Authorization": f"Bearer {jeton}"}
    )
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            print("voix   :", json.loads(r.read().decode()))
    except urllib.error.HTTPError as e:
        if e.code in (401, 403):
            print(f"jeton REFUSE (HTTP {e.code}) — recopie le JETON de la cellule 5")
            return False
        print(f"/voices HTTP {e.code}")
        return False
    except Exception as e:
        print(f"/voices injoignable ({type(e).__name__}: {e})")
        return False
    return True


def main() -> int:
    args = sys.argv[1:]
    if args:
        if len(args) != 2:
            print(__doc__)
            return 2
        url, jeton = args
        ecrire_env(url, jeton)
    else:
        url, jeton = lire_env()
        if not url:
            print(f"aucun ACADEMY_TTS_URL dans {ENV_PATH}")
            print(__doc__)
            return 2
        print(f"valeurs actuelles de {ENV_PATH} : {url}")

    print()
    ok = tester(url, jeton)
    print()
    print("API joignable — redemarre le backend pour qu'il relise .env"
          if ok else "API NON joignable — voir ci-dessus")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
