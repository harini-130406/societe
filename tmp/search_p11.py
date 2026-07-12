import sys
sys.stdout.reconfigure(encoding='utf-8')

with open(r"d:\societe\tmp\doc_text.txt", "r", encoding="utf-8") as f:
    lines = f.readlines()

for idx, line in enumerate(lines):
    if "conflict" in line.lower() and ("problem" in line.lower() or "track" in line.lower()):
        print(f"Line {idx+1}: {line.strip()}")
