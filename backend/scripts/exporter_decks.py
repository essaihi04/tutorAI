"""Exporte les cours publiés, tels que le lecteur les reçoit (entrée de scripts/phrases_cours.cjs).

    cd /opt/moalim/backend && .venv/bin/python -m scripts.exporter_decks /tmp/decks.json
"""
import asyncio
import json
import sys

from app.supabase_client import get_supabase_admin
from app.services.course_player_service import course_player_service as s


async def main():
    decks = get_supabase_admin().table("course_decks").select("lesson_id").eq("status", "published").execute().data
    sortie, vus = [], set()
    for d in decks:
        if d["lesson_id"] in vus:
            continue
        vus.add(d["lesson_id"])
        deck = await s.get_deck(d["lesson_id"])
        if deck:
            sortie.append(deck)
    json.dump(sortie, open(sys.argv[1] if len(sys.argv) > 1 else "decks.json", "w", encoding="utf-8"), ensure_ascii=False, default=str)
    print(len(sortie), "cours exportés")


asyncio.run(main())
