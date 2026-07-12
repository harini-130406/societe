with open(r"d:\societe\tmp\doc_text.txt", "r", encoding="utf-8") as f:
    lines = f.readlines()

for idx, line in enumerate(lines):
    if line.strip().startswith("Problem Statement") or line.strip().startswith("Problem "):
        print(f"Line {idx+1}: {line.strip()}")
