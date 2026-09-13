"""Keep user- and database-supplied file paths inside their designated root."""
from pathlib import Path
from fastapi import HTTPException


def safe_child_path(root: Path, *parts: str) -> Path:
    for part in parts:
        if not part or '\\' in part or ':' in part or part.startswith('/'):
            raise HTTPException(400, 'Chemin invalide')
        if any(segment in ('.', '..') for segment in part.split('/')):
            raise HTTPException(400, 'Chemin invalide')
    base = root.resolve()
    target = base.joinpath(*parts).resolve()
    if target == base or base not in target.parents:
        raise HTTPException(400, 'Chemin invalide')
    return target
