import docx
import sys

def read_docx(file_path, output_path):
    doc = docx.Document(file_path)
    fullText = []
    for para in doc.paragraphs:
        fullText.append(para.text)
    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                # To avoid duplicate printing for merged cells, we can keep it simple
                fullText.append(cell.text)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(fullText))
    print(f"Extracted {len(fullText)} lines to {output_path}")

if __name__ == "__main__":
    read_docx(r"d:\societe\GRC-Hackathon-main\GRC_Hackathon_Problem_Statements.docx", r"d:\societe\tmp\doc_text.txt")
