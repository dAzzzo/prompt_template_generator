import re
import os
from pypdf import PdfReader


# ----------- PATH & FILE HELPERS ----------- #

def sanitize_path(path: str) -> str:
    return path.strip().strip('"').strip("'")


def validate_path(path: str) -> str:
    """Sanitize and verify the file exists. Raises FileNotFoundError otherwise."""
    path = sanitize_path(path)
    if not os.path.exists(path):
        raise FileNotFoundError(f"File not found: {path}")
    return path


def read_file(path: str) -> str:
    path = validate_path(path)
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def save_file(path: str, content: str) -> None:
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


def generate_output_name(input_file: str, output_dir=None, custom_name=None) -> str:
    input_file = sanitize_path(input_file)

    if custom_name:
        base_name = custom_name.strip()
        if not base_name.endswith(".txt"):
            base_name += ".txt"
    else:
        base_name = os.path.splitext(os.path.basename(input_file))[0] + "_prompt.txt"

    if output_dir:
        return os.path.join(output_dir, base_name)

    return os.path.join(os.path.dirname(input_file) or ".", base_name)


# ----------- PDF ----------- #

def read_pdf_text(path: str) -> str:
    path = validate_path(path)
    reader = PdfReader(path)
    pages = []

    for i, page in enumerate(reader.pages):
        text = page.extract_text()
        if text:
            pages.append(text)
        else:
            print(f"Warning: page {i} has no extractable text")

    return "\n".join(pages)


# ----------- CLEANING ----------- #

# Typical PDF header/footer dates: short line, isolated, date format or "Page 3", "Page 3 of 12", "3 of 12"
# Covers: 12/03/2024  |  12-03-2024  |  2024/03/12 sp | 12/03/2024 en |  March 12, 2024  |  12 de marzo de 2024
_PAGE_PATTERN = re.compile(r"^(Page\s+\d+(\s+of\s+\d+)?|\d+\s+of\s+\d+)$", re.IGNORECASE)

# Footer page lone number
_LONE_NUMBER_PATTERN = re.compile(r"^\d{1,3}$")

_FOOTER_DATE_PATTERN = re.compile(
    r"^("
    r"\d{1,2}[\/\-\.]\d{1,2}[\/\-\.]\d{2,4}"           # 12/03/2024 | 12-03-24
    r"|\d{4}[\/\-\.]\d{1,2}[\/\-\.]\d{1,2}"             # 2024/03/12 sp
    r"|\d{1,2}[\/\-\.]\d{1,2}[\/\-\.]\d{4}"             # 12/03/2024 en
    r"|[A-Za-záéíóúÁÉÍÓÚ]+\s+\d{1,2},?\s+\d{4}"         # March 12, 2024
    r"|\d{1,2}\s+de\s+[a-záéíóúA-ZÁÉÍÓÚ]+\s+de\s+\d{4}" # 12 de marzo de 2024
    r")$"
)


def clean_text(text: str) -> list[str]:
    cleaned = []

    for line in text.split("\n"):
        line = line.strip()

        # Skip truly empty or single-char noise
        if len(line) < 2:
            continue
        
        # Skip only unambiguous page indicators, not any line containing "Page"
        if _PAGE_PATTERN.match(line):
            continue

        # Lone number in short line → isolated page number ("12", "123")
        if _LONE_NUMBER_PATTERN.match(line) and len(line) <= 3:
            cleaned.append("")
            continue

        # Isolated date in short line → typical of PDF header/footer
        if _FOOTER_DATE_PATTERN.match(line) and len(line) < 30:
            cleaned.append("")  # replace with a blank space
            continue

        cleaned.append(line)

    return cleaned

# ----------- STRUCTURE ----------- #

# Matches section codes like "UD1", "UD12", etc.
_SECTION_CODE = re.compile(r"^UD\d+", re.IGNORECASE)


def is_title(line: str) -> bool:
    if len(line) < 4:
        return False

    # All-caps line (but not a sentence that just starts with a capital)
    if line.isupper():
        return True

    # Explicit section code
    if _SECTION_CODE.match(line):
        return True

    # Short line ending in colon — likely a label/heading
    if line.endswith(":") and len(line) < 80:
        return True

    return False


def group_blocks(lines: list[str], default_title: str = "NO_TITLE") -> list[dict]:
    """
    Group lines into titled blocks.
    If the document starts with content before any title, that content
    is collected under default_title instead of being silently dropped.
    """
    blocks = []
    current = {"title": default_title, "content": []}

    for line in lines:
        if is_title(line):
            # Only flush if there's actual content — avoids empty ghost blocks
            if current["content"]:
                blocks.append(current)
            current = {"title": line, "content": []}
        else:
            current["content"].append(line)

    # Flush the last block
    if current["content"]:
        blocks.append(current)

    return blocks


def format_blocks(blocks: list[dict]) -> str:
    output = []

    for block in blocks:
        title = block["title"]
        content = "\n".join(block["content"])
        formatted = f"## {title}\n\n{content}".strip()
        output.append(formatted)

    return "\n\n".join(output)