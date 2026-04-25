#!/usr/bin/env python3
"""Debug QCM extraction from the 2016 exam."""

from app.services.exam_service import exam_service
import json

def debug_qcm_extraction():
    print("=== Debugging QCM Extraction ===")
    
    # Load the exam
    exam = exam_service.get_exam('svt_2016_normale')
    if not exam:
        print("ERROR: Could not load svt_2016_normale")
        return
    
    # Find QCM questions
    qcm_questions = [q for q in exam['questions'] if q.get('type') == 'qcm']
    print(f"Found {len(qcm_questions)} QCM questions")
    
    for i, q in enumerate(qcm_questions):
        print(f"\n=== QCM Question {i+1} ===")
        print(f"Content: {q['content'][:100]}...")
        print(f"Has choices: {'choices' in q}")
        if 'choices' in q:
            print(f"Number of choices: {len(q['choices'])}")
            for j, choice in enumerate(q['choices']):
                print(f"  Choice {j+1}: {choice}")
        else:
            print("No choices found!")
    
    # Also check the raw blocks to see what we're working with
    print("\n=== Raw Blocks Analysis ===")
    raw_exam = exam_service._load_exam_json('svt_2016_normale')
    if raw_exam and 'blocks' in raw_exam:
        blocks = raw_exam['blocks']
        for i, block in enumerate(blocks):
            if block.get('type') == 'question' and 'proposition est correcte' in block.get('content', '').lower():
                print(f"\nQCM Question Block {i}:")
                print(f"Content: {block['content'][:100]}...")
                
                # Check next block
                if i + 1 < len(blocks):
                    next_block = blocks[i + 1]
                    print(f"Next block type: {next_block.get('type')}")
                    if next_block.get('type') == 'table':
                        print(f"Table content preview: {next_block.get('content', '')[:200]}...")

if __name__ == "__main__":
    debug_qcm_extraction()
