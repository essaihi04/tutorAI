#!/usr/bin/env python3
"""Debug the table parsing to understand the 2x2 QCM format."""

import json

def debug_table_parsing():
    print("=== Table Parsing Debug ===")
    
    # Load the raw exam JSON to see the table structure
    with open('data/exams/svt/2016_normale/exam.json', 'r', encoding='utf-8') as f:
        raw_exam = json.load(f)
    
    blocks = raw_exam.get('blocks', [])
    
    # Find the QCM table block
    for i, block in enumerate(blocks):
        if (block.get('type') == 'question' and 
            'proposition est correcte' in block.get('content', '').lower()):
            print(f"QCM Question Block {i}:")
            print(f"Content: {block['content']}")
            
            if i + 1 < len(blocks) and blocks[i + 1].get('type') == 'table':
                table_block = blocks[i + 1]
                print(f"\nTable Block {i + 1}:")
                content = table_block.get('content', '')
                print("Raw table content:")
                print(repr(content))
                
                print("\nTable lines:")
                lines = content.split('\n')
                for j, line in enumerate(lines):
                    print(f"Line {j}: {repr(line)}")
                
                print("\nParsing analysis:")
                for j, line in enumerate(lines):
                    if line.strip() and line.startswith('|') and not line.startswith('|---'):
                        cells = [cell.strip() for cell in line.split('|') if cell.strip()]
                        print(f"Line {j} cells: {cells}")

if __name__ == "__main__":
    debug_table_parsing()
