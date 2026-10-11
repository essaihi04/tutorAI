"""Génère une fois, vérifie puis publie l'audio persistant des cours.

Exemples, depuis ``backend``::

    python -m scripts.generate_course_audio generate --deck svt_ch1_energy --language fr
    python -m scripts.generate_course_audio verify --deck svt_ch1_energy --language fr --reviewer UUID_ADMIN

``generate`` ne publie jamais. Il réutilise tout fichier dont l'empreinte de
speech est inchangée. ``verify`` est l'acte humain qui rend les fichiers
visibles par le lecteur et publie le deck lorsque toutes ses diapositives ont
un audio validé dans la langue demandée.

Mode hors base (``--offline``) : quand l'API de la base n'est pas joignable
(instance privée sur le VPS), ``generate --offline`` travaille depuis le manifeste
seul et consigne chaque fichier dans un registre
``frontend/public/media/audio/courses/<deck>/<langue>/ledger.json`` (mêmes
champs qu'une ligne ``course_slide_audio``). ``import-ledger`` rejoue ensuite ce
registre dans la base, là où elle est accessible (ex. sur le VPS) ; ``verify``
fonctionne alors comme d'habitude.
"""
from __future__ import annotations

import argparse
import asyncio
import base64
import hashlib
import json
import mimetypes
import sys
from datetime import datetime, timezone
from pathlib import Path


BACKEND_ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = BACKEND_ROOT.parent
if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))

from app.services.tts_service import tts_service  # noqa: E402
from app.supabase_client import get_supabase_admin  # noqa: E402


COURSE_DIR = BACKEND_ROOT / "data" / "courses"
AUDIO_ROOT = PROJECT_ROOT / "frontend" / "public" / "media" / "audio" / "courses"


def load_manifest(deck_stable_id: str) -> tuple[Path, dict]:
    for path in COURSE_DIR.glob("*_course_v1.json"):
        manifest = json.loads(path.read_text(encoding="utf-8"))
        if deck_stable_id in {manifest.get("id"), manifest.get("stable_id")}:
            return path, manifest
    raise RuntimeError(f"Manifest inconnu : {deck_stable_id}")


def load_db_deck(admin, manifest: dict) -> dict:
    """Deck en base pour ce manifeste : même stable_id et même version, sinon (repli) la version
    la plus récente de même stable_id. Le repli est sûr car l'audio est rattaché par empreinte du
    texte : import-ledger refuse toute ligne dont le texte ne correspond pas à la diapositive en base."""
    rows = admin.table("course_decks").select("*").execute().data or []
    same = [row for row in rows if (row.get("metadata") or {}).get("stable_id") == manifest.get("stable_id")]
    wanted = int(manifest.get("version") or 1)
    for row in same:
        if int(row.get("version") or 0) == wanted:
            return row
    if same:
        row = max(same, key=lambda r: int(r.get("version") or 0))
        print(f"ATTENTION version manifeste v{wanted} ≠ base v{row['version']} : deck de base utilisé "
              f"(textes vérifiés diapositive par diapositive).")
        return row
    raise RuntimeError("Deck non synchronisé. Lancez d'abord scripts.sync_course_decks.")


def db_slides(admin, deck_id: str) -> dict[str, dict]:
    activities = admin.table("course_activities").select("id").eq("deck_id", deck_id).execute().data or []
    activity_ids = [row["id"] for row in activities]
    if not activity_ids:
        return {}
    slides = admin.table("course_slides").select("id,stable_id,speech_text").in_(
        "activity_id", activity_ids
    ).execute().data or []
    return {row["stable_id"]: row for row in slides}


def manifest_slides(manifest: dict):
    for activity in manifest.get("activities") or []:
        for slide in activity.get("slides") or []:
            yield slide


async def generate(deck_stable_id: str, language: str) -> None:
    _, manifest = load_manifest(deck_stable_id)
    admin = get_supabase_admin()
    deck = load_db_deck(admin, manifest)
    slides_by_stable = db_slides(admin, deck["id"])
    generated = reused = failed = 0

    for manifest_slide in manifest_slides(manifest):
        stable_id = manifest_slide.get("stable_id") or manifest_slide["id"]
        db_slide = slides_by_stable.get(stable_id)
        if not db_slide:
            print(f"MANQUANT {stable_id}: resynchronisez le deck")
            failed += 1
            continue
        speech_map = manifest_slide.get("speech_text") or {}
        speech = speech_map.get(language)
        if not speech:
            print(f"SANS SPEECH {stable_id}")
            failed += 1
            continue
        speech_hash = hashlib.sha256(speech.strip().encode("utf-8")).hexdigest()
        existing = admin.table("course_slide_audio").select("*").eq(
            "slide_id", db_slide["id"]
        ).eq("language", language).order("version", desc=True).execute().data or []
        latest = existing[0] if existing else None
        if latest and latest.get("speech_hash") == speech_hash:
            local_path = PROJECT_ROOT / "frontend" / "public" / latest["file_path"].lstrip("/")
            if local_path.exists() and latest.get("status") in {"generated", "verified", "published"}:
                reused += 1
                print(f"RÉUTILISÉ {stable_id} v{latest['version']} ({latest['status']})")
                continue

        result = await tts_service.synthesize(speech, language)
        if not result.audio_b64:
            failed += 1
            print(f"ÉCHEC TTS {stable_id}")
            continue
        audio_bytes = base64.b64decode(result.audio_b64)
        extension = ".wav" if result.mime == "audio/wav" else ".mp3"
        version = int(latest.get("version") or 0) + 1 if latest else 1
        relative_path = Path("media") / "audio" / "courses" / manifest["stable_id"] / language / f"{stable_id}_v{version}{extension}"
        output_path = PROJECT_ROOT / "frontend" / "public" / relative_path
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_bytes(audio_bytes)
        checksum = hashlib.sha256(audio_bytes).hexdigest()

        if existing:
            admin.table("course_slide_audio").update({"status": "stale"}).eq(
                "slide_id", db_slide["id"]
            ).eq("language", language).neq("status", "rejected").execute()
        admin.table("course_slide_audio").insert({
            "slide_id": db_slide["id"],
            "language": language,
            "version": version,
            "speech_hash": speech_hash,
            "file_path": "/" + relative_path.as_posix(),
            "mime_type": result.mime or mimetypes.guess_type(output_path.name)[0] or "audio/mpeg",
            "provider": result.provider,
            "checksum": checksum,
            "status": "generated",
        }).execute()
        generated += 1
        print(f"GÉNÉRÉ {stable_id} v{version} → /{relative_path.as_posix()}")

    print(f"Résultat : {generated} générés, {reused} réutilisés, {failed} échecs. Aucun audio n'a été publié.")


def ledger_path(manifest: dict, language: str) -> Path:
    return AUDIO_ROOT / manifest["stable_id"] / language / "ledger.json"


def load_ledger(manifest: dict, language: str) -> dict:
    path = ledger_path(manifest, language)
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return {"deck_stable_id": manifest["stable_id"], "language": language, "slides": {}}


def save_ledger(manifest: dict, language: str, ledger: dict) -> Path:
    path = ledger_path(manifest, language)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(ledger, ensure_ascii=False, indent=2), encoding="utf-8")
    return path


async def generate_offline(deck_stable_id: str, language: str) -> None:
    """Comme ``generate`` mais sans base : versions et statuts tenus dans ledger.json."""
    _, manifest = load_manifest(deck_stable_id)
    ledger = load_ledger(manifest, language)
    generated = reused = failed = 0

    for manifest_slide in manifest_slides(manifest):
        stable_id = manifest_slide.get("stable_id") or manifest_slide["id"]
        speech = (manifest_slide.get("speech_text") or {}).get(language)
        if not speech:
            print(f"SANS SPEECH {stable_id}")
            failed += 1
            continue
        speech_hash = hashlib.sha256(speech.strip().encode("utf-8")).hexdigest()
        history = ledger["slides"].get(stable_id) or []
        latest = history[-1] if history else None
        if latest and latest.get("speech_hash") == speech_hash:
            local_path = PROJECT_ROOT / "frontend" / "public" / latest["file_path"].lstrip("/")
            if local_path.exists() and latest.get("status") in {"generated", "verified", "published"}:
                reused += 1
                print(f"RÉUTILISÉ {stable_id} v{latest['version']} ({latest['status']})")
                continue

        result = await tts_service.synthesize(speech, language)
        if not result.audio_b64:
            failed += 1
            print(f"ÉCHEC TTS {stable_id} (provider={result.provider})")
            continue
        audio_bytes = base64.b64decode(result.audio_b64)
        extension = ".wav" if result.mime == "audio/wav" else ".mp3"
        version = int(latest.get("version") or 0) + 1 if latest else 1
        while True:  # un fichier déjà présent mais absent du registre (ancienne génération) n'est jamais écrasé
            relative_path = Path("media") / "audio" / "courses" / manifest["stable_id"] / language / f"{stable_id}_v{version}{extension}"
            output_path = PROJECT_ROOT / "frontend" / "public" / relative_path
            if not output_path.exists():
                break
            version += 1
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_bytes(audio_bytes)
        for row in history:
            if row.get("status") != "rejected":
                row["status"] = "stale"
        history.append({
            "language": language,
            "version": version,
            "speech_hash": speech_hash,
            "file_path": "/" + relative_path.as_posix(),
            "mime_type": result.mime or mimetypes.guess_type(output_path.name)[0] or "audio/mpeg",
            "provider": result.provider,
            "checksum": hashlib.sha256(audio_bytes).hexdigest(),
            "size_bytes": len(audio_bytes),
            "status": "generated",
            "generated_at": datetime.now(timezone.utc).isoformat(),
        })
        ledger["slides"][stable_id] = history
        save_ledger(manifest, language, ledger)  # sauvegardé à chaque fichier : rien n'est perdu si le TTS tombe
        generated += 1
        print(f"GÉNÉRÉ {stable_id} v{version} → /{relative_path.as_posix()} ({result.provider}, {len(audio_bytes) // 1024} ko)")

    print(f"Résultat (hors base) : {generated} générés, {reused} réutilisés, {failed} échecs. "
          f"Registre : {ledger_path(manifest, language)}. Aucun audio n'a été publié.")


def import_ledger(deck_stable_id: str, language: str) -> None:
    """Rejoue ledger.json dans course_slide_audio (idempotent : même version + même empreinte = ignoré)."""
    _, manifest = load_manifest(deck_stable_id)
    ledger = load_ledger(manifest, language)
    admin = get_supabase_admin()
    deck = load_db_deck(admin, manifest)
    slides_by_stable = db_slides(admin, deck["id"])
    inserted = skipped = missing = 0
    for stable_id, history in ledger["slides"].items():
        db_slide = slides_by_stable.get(stable_id)
        if not db_slide:
            print(f"MANQUANT {stable_id}: resynchronisez le deck")
            missing += 1
            continue
        existing = admin.table("course_slide_audio").select("version,speech_hash,status").eq(
            "slide_id", db_slide["id"]
        ).eq("language", language).execute().data or []
        known = {(int(row["version"]), row.get("speech_hash")) for row in existing}
        db_speech = ((db_slide.get("speech_text") or {}).get(language) or "").strip()
        db_hash = hashlib.sha256(db_speech.encode("utf-8")).hexdigest()
        for row in history:
            if row["speech_hash"] != db_hash and row.get("status") != "stale":
                print(f"TEXTE DIFFÉRENT {stable_id} v{row['version']} : la diapositive en base a un autre texte, ligne ignorée")
                missing += 1
                continue
            local_path = PROJECT_ROOT / "frontend" / "public" / row["file_path"].lstrip("/")
            if not local_path.exists():
                print(f"FICHIER ABSENT {row['file_path']}")
                continue
            if (int(row["version"]), row["speech_hash"]) in known:
                skipped += 1
                continue
            if row.get("status") == "generated" and existing:
                admin.table("course_slide_audio").update({"status": "stale"}).eq(
                    "slide_id", db_slide["id"]
                ).eq("language", language).neq("status", "rejected").execute()
            admin.table("course_slide_audio").insert({
                "slide_id": db_slide["id"],
                "language": language,
                "version": row["version"],
                "speech_hash": row["speech_hash"],
                "file_path": row["file_path"],
                "mime_type": row["mime_type"],
                "provider": row["provider"],
                "checksum": row["checksum"],
                "status": row.get("status", "generated"),
            }).execute()
            inserted += 1
    print(f"Registre importé : {inserted} lignes insérées, {skipped} déjà en base, {missing} diapositives manquantes.")


def verify(deck_stable_id: str, language: str, reviewer: str) -> None:
    _, manifest = load_manifest(deck_stable_id)
    admin = get_supabase_admin()
    deck = load_db_deck(admin, manifest)
    slides = db_slides(admin, deck["id"])
    rows_to_publish: list[dict] = []

    for manifest_slide in manifest_slides(manifest):
        stable_id = manifest_slide.get("stable_id") or manifest_slide["id"]
        db_slide = slides.get(stable_id)
        speech = (manifest_slide.get("speech_text") or {}).get(language) or ""
        if not speech:
            raise RuntimeError(f"Speech {language} absent pour {stable_id}")
        expected_hash = hashlib.sha256(speech.strip().encode("utf-8")).hexdigest()
        rows = admin.table("course_slide_audio").select("*").eq(
            "slide_id", db_slide["id"]
        ).eq("language", language).eq("speech_hash", expected_hash).order("version", desc=True).limit(1).execute().data or []
        if not rows:
            raise RuntimeError(f"Audio actuel absent pour {stable_id}")
        row = rows[0]
        local_path = PROJECT_ROOT / "frontend" / "public" / row["file_path"].lstrip("/")
        if not local_path.exists() or hashlib.sha256(local_path.read_bytes()).hexdigest() != row.get("checksum"):
            raise RuntimeError(f"Fichier absent ou checksum invalide pour {stable_id}")
        rows_to_publish.append(row)

    verified_at = datetime.now(timezone.utc).isoformat()
    for row in rows_to_publish:
        admin.table("course_slide_audio").update({
            "status": "published",
            "verified_by": reviewer,
            "verified_at": verified_at,
        }).eq("id", row["id"]).execute()
    admin.table("course_decks").update({
        "status": "published",
        "published_at": verified_at,
        "updated_at": verified_at,
    }).eq("id", deck["id"]).execute()
    print(f"Deck publié : {len(rows_to_publish)} audios {language} vérifiés par {reviewer}.")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)
    for command in ("generate", "verify", "import-ledger"):
        sub = subparsers.add_parser(command)
        sub.add_argument("--deck", required=True, help="stable_id du manifest")
        sub.add_argument("--language", default="fr", choices=("fr", "ar", "mixed"))
        if command == "generate":
            sub.add_argument("--offline", action="store_true",
                             help="sans base : registre ledger.json à importer ensuite avec import-ledger")
        if command == "verify":
            sub.add_argument("--reviewer", required=True, help="UUID auth de l'administrateur ayant écouté les fichiers")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.command == "generate":
        asyncio.run(generate_offline(args.deck, args.language) if args.offline else generate(args.deck, args.language))
    elif args.command == "import-ledger":
        import_ledger(args.deck, args.language)
    else:
        verify(args.deck, args.language, args.reviewer)


if __name__ == "__main__":
    main()
