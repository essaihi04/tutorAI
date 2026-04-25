#!/usr/bin/env python3
"""Debug script to analyze the 2016 exam structure and issues."""

from app.services.exam_service import exam_service
import json

def debug_2016_exam():
    print("=== Debugging SVT 2016 Exam ===")
    
    # Load the exam
    exam = exam_service.get_exam('svt_2016_normale')
    if not exam:
        print("ERROR: Could not load svt_2016_normale")
        return
    
    print(f"Total questions: {len(exam['questions'])}")
    print(f"Exam title: {exam.get('title', 'N/A')}")
    print(f"Subject: {exam.get('subject', 'N/A')}")
    print(f"Year: {exam.get('year', 'N/A')}")
    
    print("\n=== Question Analysis ===")
    for i, q in enumerate(exam['questions'][:10]):  # First 10 questions
        print(f"\nQ{i+1}:")
        print(f"  Type: {q.get('type', 'unknown')}")
        print(f"  Content: {q['content'][:100]}...")
        print(f"  Has documents: {len(q.get('documents', []))}")
        print(f"  Has schema: {'schema' in q}")
        if q.get('documents'):
            for doc in q['documents']:
                print(f"    Doc: {doc.get('type', 'unknown')} - {doc.get('src', 'no src')}")
    
    print("\n=== Document Path Analysis ===")
    all_docs = []
    for q in exam['questions']:
        all_docs.extend(q.get('documents', []))
        if q.get('schema'):
            all_docs.append(q['schema'])
    
    print(f"Total document references: {len(all_docs)}")
    src_paths = [doc.get('src', 'no src') for doc in all_docs]
    unique_paths = set(src_paths)
    print(f"Unique src paths: {len(unique_paths)}")
    for path in sorted(unique_paths):
        print(f"  {path}")

if __name__ == "__main__":
    debug_2016_exam()
