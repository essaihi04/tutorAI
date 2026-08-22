"""Regenerate the Python view of the SVG schema library.

The schemas themselves live in the browser bundle
(`frontend/src/components/session/schemas/schemas_*.ts`) — that is where they
are drawn and rendered.  The tutor prompt, however, has to name them: the model
can only write `<schema>svt_mitose</schema>` if it knows the id exists.

Until now that list was retyped by hand inside two prompt blocks of
`llm_service.py`.  Every schema added on the front end was invisible to the
model until someone remembered to copy the id over — `svt_adn_structure` was
already missing from one of the two lists.

This script reads the registry and writes `app/services/schema_catalog.py`.
Run it after adding or renaming a schema:

    python tools/generate_schema_catalog.py
"""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCHEMAS_DIR = ROOT / "frontend" / "src" / "components" / "session" / "schemas"
TARGET = ROOT / "backend" / "app" / "services" / "schema_catalog.py"

SUBJECT_LABELS = {
    "svt": "SVT",
    "physics": "PHYSIQUE",
    "chemistry": "CHIMIE",
    "math": "MATHS",
}
SUBJECT_ORDER = ["svt", "physics", "chemistry", "math"]

# Un schéma déclare toujours ces trois champs d'affilée, dans cet ordre.
ENTRY = re.compile(
    r"id:\s*'(?P<id>[^']+)',\s*"
    r"title:\s*'(?P<title>(?:[^'\\]|\\.)*)',\s*"
    r"subject:\s*'(?P<subject>[^']+)'",
)


def collect() -> list[dict[str, str]]:
    found: list[dict[str, str]] = []
    seen: set[str] = set()
    for path in sorted(SCHEMAS_DIR.glob("schemas_*.ts")):
        source = path.read_text(encoding="utf-8")
        for match in ENTRY.finditer(source):
            schema_id = match.group("id")
            if schema_id in seen:
                continue
            seen.add(schema_id)
            found.append({
                "id": schema_id,
                "title": match.group("title").replace("\\'", "'"),
                "subject": match.group("subject"),
            })
    return found


def render(entries: list[dict[str, str]]) -> str:
    by_subject: dict[str, list[dict[str, str]]] = {}
    for entry in entries:
        by_subject.setdefault(entry["subject"], []).append(entry)

    lines: list[str] = []
    for subject in SUBJECT_ORDER + [s for s in by_subject if s not in SUBJECT_ORDER]:
        group = by_subject.get(subject)
        if not group:
            continue
        lines.append(f"  {SUBJECT_LABELS.get(subject, subject.upper())} :")
        for entry in group:
            lines.append(f"    {entry['id']} — {entry['title']}")
    catalogue = "\n".join(lines)

    items = "\n".join(
        "    {"
        f"\"id\": {entry['id']!r}, \"title\": {entry['title']!r}, \"subject\": {entry['subject']!r}"
        "},"
        for entry in entries
    )

    count = len(entries)

    return f'''"""Les schémas SVG disponibles, vus depuis le serveur — FICHIER GÉNÉRÉ.

Ne pas éditer à la main : lancer `python tools/generate_schema_catalog.py`
après avoir ajouté un schéma dans
`frontend/src/components/session/schemas/schemas_*.ts`.

Le catalogue sert au prompt : un identifiant absent d'ici n'existe pas pour le
modèle, et un schéma que personne ne nomme ne s'affiche jamais.
"""

from __future__ import annotations

SCHEMA_CATALOG: list[dict[str, str]] = [
{items}
]

SCHEMA_IDS: frozenset[str] = frozenset(entry["id"] for entry in SCHEMA_CATALOG)

SCHEMA_CATALOG_PROMPT = """[SCHÉMAS SVG DISPONIBLES — {count} identifiants]
Ces schémas sont déjà dessinés, animés et annotés. Les afficher coûte moins
cher et rend mieux qu'un dessin improvisé : si l'un d'eux couvre la notion,
c'est LUI qu'on affiche, dans TOUS les modes (cours, exercice, examen,
question libre).
Format : <schema>identifiant</schema> — ou l'action `show_schema`.
N'INVENTE JAMAIS un identifiant : s'il n'est pas dans cette liste, il n'existe
pas, et l'élève ne voit rien.

{catalogue}
"""
'''


def main() -> None:
    entries = collect()
    if not entries:
        raise SystemExit(f"Aucun schéma trouvé dans {SCHEMAS_DIR}")
    TARGET.write_text(render(entries), encoding="utf-8")
    print(f"{len(entries)} schémas -> {TARGET.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
