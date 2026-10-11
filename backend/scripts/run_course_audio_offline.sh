#!/usr/bin/env bash
# Génère l'audio des cours (mode hors base) avec le serveur VoxCPM « voix du tuteur » exposé par un tunnel.
#
#   bash scripts/run_course_audio_offline.sh https://xxxx.trycloudflare.com JETON phys_ch1_waves fr mixed
#
# - Le serveur VoxCPM (dépôt voxtts, server/academy_api.py) parle le contrat « Academy » attendu par
#   app/services/tts_service.py : on le branche via ACADEMY_TTS_URL / ACADEMY_TTS_TOKEN sans toucher à .env.
# - Les replis payants (Google Cloud TTS) sont désactivés pour cette exécution : un échec reste un échec,
#   jamais une voix différente glissée dans le cours.
# - Résultat : fichiers dans frontend/public/media/audio/courses/<deck>/<langue>/ + ledger.json,
#   à importer en base avec `python -m scripts.generate_course_audio import-ledger --deck … --language …`.
set -euo pipefail
URL="${1:?URL du serveur TTS}"; TOKEN="${2:?jeton}"; DECK="${3:?stable_id du deck}"; shift 3
LANGS=("$@"); [ ${#LANGS[@]} -eq 0 ] && LANGS=(fr mixed)
cd "$(dirname "$0")/.."
PY=../.venv/Scripts/python.exe; [ -x "$PY" ] || PY=python
for L in "${LANGS[@]}"; do
  echo "=== $DECK / $L"
  ACADEMY_TTS_URL="$URL" ACADEMY_TTS_TOKEN="$TOKEN" ACADEMY_TTS_VOICE=tuteur ACADEMY_TTS_STREAM=0 \
  GOOGLE_CLOUD_TTS_API_KEY= GEMINI_TTS_API_KEY= GRADIO_TTS_URL= TTS_DISABLED=0 TTS_CACHE_ENABLED=0 \
  "$PY" -X utf8 -m scripts.generate_course_audio generate --offline --deck "$DECK" --language "$L"
done
