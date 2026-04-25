#!/usr/bin/env python3
"""Detailed debug of QCM structure and document mixing."""

from app.services.exam_service import exam_service
import json

def debug_detailed():
    print("=== Detailed QCM and Document Debug ===")
    
    # Load both exams to check for document mixing
    exam_2016 = exam_service.get_exam('svt_2016_normale')
    exam_2019 = exam_service.get_exam('svt_2019_normale')
    
    if not exam_2016 or not exam_2019:
        print("ERROR: Could not load exams")
        return
    
    print(f"2016 Exam: {len(exam_2016['questions'])} questions")
    print(f"2019 Exam: {len(exam_2019['questions'])} questions")
    
    # Check for document path overlaps
    docs_2016 = set()
    docs_2019 = set()
    
    for q in exam_2016['questions']:
        for doc in q.get('documents', []):
            docs_2016.add(doc.get('src', ''))
        if q.get('sub_questions'):
            print(f"2016 Question {q['index']} has sub_questions: {len(q['sub_questions'])}")
            for sq in q['sub_questions']:
                print(f"  Sub-question {sq.get('number', '?')}: {sq.get('content', '')[:50]}...")
                print(f"  Choices: {len(sq.get('choices', []))}")
    
    for q in exam_2019['questions']:
        for doc in q.get('documents', []):
            docs_2019.add(doc.get('src', ''))
    
    print(f"\n2016 documents: {len(docs_2016)}")
    print(f"2019 documents: {len(docs_2019)}")
    
    overlap = docs_2016.intersection(docs_2019)
    if overlap:
        print(f"DOCUMENT MIXING DETECTED: {len(overlap)} overlapping paths")
        for path in sorted(overlap):
            print(f"  {path}")
    else:
        print("No document mixing detected")
    
    # Check QCM structure in detail
    print("\n=== QCM Structure Analysis ===")
    for q in exam_2016['questions']:
        if q.get('type') == 'qcm':
            print(f"QCM Question {q['index']}:")
            print(f"  Content: {q['content'][:80]}...")
            print(f"  Has sub_questions: {'sub_questions' in q}")
            print(f"  Has choices: {'choices' in q}")
            if 'sub_questions' in q:
                print(f"  Number of sub_questions: {len(q['sub_questions'])}")
                for i, sq in enumerate(q['sub_questions']):
                    print(f"    Sub {i+1}: {sq.get('content', '')[:40]}... ({len(sq.get('choices', []))} choices)")

if __name__ == "__main__":
    debug_detailed()
