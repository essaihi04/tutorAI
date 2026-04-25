#!/usr/bin/env python
"""Indexation complète des cadres de référence pour toutes les matières."""
import os
import sys
from pathlib import Path

# Force RAG enabled
os.environ["RAG_DISABLED"] = "0"

# Add backend to path
backend_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(backend_root))

from app.services.rag_service import RAGService

print("=" * 80)
print("INDEXATION DES CADRES DE RÉFÉRENCE")
print("=" * 80)

rag = RAGService()

# Indexer les cadres pour chaque matière
for subject in ["SVT", "Physique-Chimie", "Mathematiques"]:
    print(f"\n[{subject}] Indexation...")
    try:
        rag.index_subject(subject)
        print(f"  ✓ {subject} indexé avec succès")
    except Exception as e:
        print(f"  ✗ Erreur indexation {subject} : {e}")

# Vérifier les caches après indexation
print("\n" + "=" * 80)
print("VÉRIFICATION DES CACHES APRÈS INDEXATION")
print("=" * 80)
for subject in ["SVT", "Physique-Chimie", "Mathematiques"]:
    cache_path = rag._get_cache_path(subject)
    exists = cache_path.exists()
    size = cache_path.stat().st_size if exists else 0
    print(f"  {subject:20s} → {cache_path.name} {'✓' if exists else '✗'} ({size} bytes)")

print("\n" + "=" * 80)
print("INDEXATION TERMINÉE")
print("=" * 80)
