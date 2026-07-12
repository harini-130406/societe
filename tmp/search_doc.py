with open(r"d:\societe\tmp\doc_text.txt", "r", encoding="utf-8") as f:
    lines = f.readlines()

search_terms = ["problem statement 3", "problem 3", "ps 3", "approach", "policy conflict"]
for idx, line in enumerate(lines):
    line_lower = line.lower()
    if any(term in line_lower for term in search_terms):
        print(f"Line {idx+1}: {line.strip()}")
