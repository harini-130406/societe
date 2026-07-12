import sys
sys.stdout.reconfigure(encoding='utf-8')

with open(r"d:\societe\tmp\doc_text.txt", "r", encoding="utf-8") as f:
    lines = f.readlines()

for idx in range(799, min(929, len(lines))):
    print(f"{idx+1}: {lines[idx].strip()}")
