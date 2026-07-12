import sys
sys.stdout.reconfigure(encoding='utf-8')

with open(r"d:\societe\tmp\doc_text.txt", "r", encoding="utf-8") as f:
    lines = f.readlines()

# Print lines 1120 to 1260 (0-indexed: 1119 to 1259)
for idx in range(1119, min(1259, len(lines))):
    print(f"{idx+1}: {lines[idx].strip()}")
