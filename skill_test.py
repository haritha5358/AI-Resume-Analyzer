import pdfplumber

SKILLS = [
    "python",
    "java",
    "c++",
    "javascript",
    "html",
    "css",
    "sql",
    "aws",
    "react",
    "node",
    "docker",
    "kubernetes"
]

pdf_path = "uploads/haritha.pdf"  # make sure file name matches

text = ""

with pdfplumber.open(pdf_path) as pdf:
    for page in pdf.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text.lower()

found_skills = []

for skill in SKILLS:
    if skill in text:
        found_skills.append(skill)

print("Detected Skills:")
print(found_skills)