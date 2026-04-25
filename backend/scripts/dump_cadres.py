"""Dump official taxonomies from the cadres de référence (2BAC PC)."""
import json
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent / "cours 2bac pc" / "cadres de references 2BAC PC"

def _walk(obj, depth=0):
    """Yield (depth, key_path, value) for every node with a 'nom' or 'titre'."""
    if isinstance(obj, dict):
        label = obj.get("nom") or obj.get("titre") or obj.get("id")
        if label:
            yield (depth, label, obj)
        for k, v in obj.items():
            yield from _walk(v, depth + 1)
    elif isinstance(obj, list):
        for x in obj:
            yield from _walk(x, depth)


def dump_domains(path: Path, label: str):
    print(f"\n{'═' * 80}\n{label}  ({path.name})\n{'═' * 80}")
    d = json.loads(path.read_text(encoding="utf-8"))
    for depth, title, node in _walk(d):
        t = str(title)[:140]
        # Only keep likely-domain nodes
        is_domain = (
            "Domaine" in t
            or "domaine" in t
            or "Chapitre" in t
            or (isinstance(node, dict) and "points_cles" in node)
            or (isinstance(node, dict) and "points_cl%C3%A9s" in node)
        )
        if not is_domain:
            continue
        print(f"\n{'  ' * depth}▸ [{node.get('id','?')}] {t}")
        for pk in (node.get("points_cles") or []):
            print(f"{'  ' * (depth+1)}• {str(pk)[:160]}")
        for key in ("contenu", "contenus", "sous_domaines", "chapitres"):
            if node.get(key):
                items = node[key]
                if isinstance(items, list):
                    for it in items[:10]:
                        if isinstance(it, dict):
                            print(f"{'  ' * (depth+1)}- {it.get('nom') or it.get('titre') or it.get('id','?')}")
                        else:
                            print(f"{'  ' * (depth+1)}- {str(it)[:140]}")

dump_domains(BASE / "cadre-de-reference-de-l-examen-national-svt-sciences-physiques (1).json", "SVT (2BAC PC)")
dump_domains(BASE / "cadre-de-reference-de-l-examen-national-physique-chimie-spc-2.json", "PHYSIQUE-CHIMIE (2BAC PC)")
dump_domains(BASE / "cadre-de-reference-de-l-examen-national-maths-sciences-experimentales.json", "MATHEMATIQUES (2BAC PC)")
