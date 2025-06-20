import os
import re
from pathlib import Path

SOURCE_DIR = Path(".")
DOCS_DIR = Path("docs")
EXCLUDE_FILES = {"README.md", "mkdocs.yml"}

LICENSE_LINK = "https://github.com/TamerOnLine/indexMD/blob/main/LICENSE"

def clean_content(content: str) -> str:
    content = re.sub(r".*?\[Live Documentation\]\([^)]+\)\s*\n?", "", content)
    content = re.sub(r"\[.*?Back to Top.*?\]\([^)]+\)\s*\n?", "", content, flags=re.IGNORECASE)
    content = re.sub(r"## Table of Contents[\s\S]+?(?=\n## )", "", content)
    return content

def fix_links(content: str) -> str:
    content = content.replace("screenshots/", "screenshots/")
    content = content.replace("(../LICENSE)", f"({LICENSE_LINK})")
    content = content.replace("(LICENSE)", f"({LICENSE_LINK})")
    return content

def write_to_docs(filename: str, content: str):
    output_path = DOCS_DIR / filename
    os.makedirs(output_path.parent, exist_ok=True)

    lines = content.splitlines()
    while lines and not lines[0].strip():
        lines.pop(0)
    while lines and not lines[-1].strip():
        lines.pop()
    content = '\n'.join(lines)

    with open(output_path, "w", encoding="utf-8") as file:
        file.write(content)

def process_markdown_files():
    md_files = [f for f in SOURCE_DIR.glob("*.md") if f.name not in EXCLUDE_FILES]

    for md_file in md_files:
        print(f"Processing {md_file.name}...")
        with open(md_file, "r", encoding="utf-8") as f:
            content = f.read()

        cleaned = clean_content(content)
        fixed = fix_links(cleaned)

        write_to_docs(md_file.name, fixed)

    print("All markdown files have been processed into the docs/ folder.")

if __name__ == "__main__":
    process_markdown_files()
