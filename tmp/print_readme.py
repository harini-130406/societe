import sys
sys.stdout.reconfigure(encoding='utf-8')

with open(r"d:\societe\GRC-Hackathon-main\Problem Statements\README.md", "r", encoding="utf-8") as f:
    lines = f.readlines()

for idx in range(250, min(370, len(lines))):
    print(f"{idx+1}: {lines[idx].strip()}")
