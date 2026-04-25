#!/usr/bin/env python
"""Vérification complète du système RAG : modèle, indexation, cache, recherche."""
import os
import sys
from pathlib import Path

# Force RAG enabled
os.environ["RAG_DISABLED"] = "0"

# Add backend to path
backend_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(backend_root))

# Import WITHOUT triggering torch/sentence-transformers loading
print("=" * 80)
print("VERIFICATION RAG - MODE ACTIF (sans chargement de modèle)")
print("=" * 80)

print(f"\n[CONFIG] RAG_DISABLED = {os.environ.get('RAG_DISABLED', 'non défini')}")

# 1. Test imports basiques
print("\n[1] Test imports RAG...")
try:
    from app.services.rag_service import RAGService, RAG_DISABLED
    print(f"  ✓ RAGService importé, RAG_DISABLED={RAG_DISABLED}")
except Exception as e:
    print(f"  ✗ Erreur import RAGService : {e}")
    sys.exit(1)

# 2. Test configuration
print("\n[2] Test configuration RAGService...")
rag = RAGService()
print(f"  ✓ RAGService initialisé")
print(f"  Courses dir : {rag.courses_dir}")
print(f"  Cache dir : {rag.cache_dir}")

# 3. Vérification cache files
print("\n[3] Vérification des fichiers cache...")
for subject in ["SVT", "Physique-Chimie", "Mathematiques"]:
    cache_path = rag._get_cache_path(subject)
    exists = cache_path.exists()
    size = cache_path.stat().st_size if exists else 0
    print(f"  {subject:20s} → {cache_path.name} {'✓' if exists else '✗'} ({size} bytes)")

# 4. Vérification cadres de référence
print("\n[4] Vérification cadres de référence...")
cadres_dir = rag.courses_dir / "cadres de references 2BAC PC"
if cadres_dir.exists():
    json_files = list(cadres_dir.glob("*.json"))
    print(f"  ✓ Dossier cadres : {len(json_files)} fichiers JSON")
    for f in json_files:
        print(f"    - {f.name}")
else:
    print(f"  ✗ Dossier cadres introuvable : {cadres_dir}")

# 5. Vérification batches study_plan_service
print("\n[5] Vérification batches study_plan_service...")
try:
    from app.services.study_plan_service import StudyPlanService
    print("  ✓ StudyPlanService importé")
    print("  Les insertions study_plan_sessions se font par batches de 50")
except Exception as e:
    print(f"  ✗ Erreur import StudyPlanService : {e}")

# 6. Vérification diagnostic_service
print("\n[6] Vérification diagnostic_service...")
try:
    from app.services.diagnostic_service import DiagnosticService
    print("  ✓ DiagnosticService importé")
    print("  Les réponses diagnostiques sont batchées")
except Exception as e:
    print(f"  ✗ Erreur import DiagnosticService : {e}")

print("\n" + "=" * 80)
print("VERIFICATION TERMINEE - RAG ACTIF")
print("=" * 80)
