import re

def read_file(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def save_file(path, content):
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

def generate_output_name(input_file):
    return input_file.replace(".txt", "_prompt.txt")


def clean_text(text):
    lines = text.split("\n")
    cleaned = []

    for line in lines:
        line = line.strip()

        # elimina basura típica OCR / PPT
        if len(line) < 2:
            continue
        if "Page" in line:
            continue
         # regex de n sueltos
        if re.match(r"^\d+$", line): 
            continue

        cleaned.append(line)

    return cleaned


# Detecta títulos
def is_title(line):
    return (
        line.isupper()
        or line.startswith("UD")
        or line.endswith(":")
    )


# Agrupa en bloques
def group_blocks(lines):
    blocks = []
    current = {"title": "SIN_TITULO", "content": []}

    for line in lines:

        if is_title(line):
            if current["content"]:
                blocks.append(current)
            current = {"title": line, "content": []}
        else:
            current["content"].append(line)

    if current["content"]:
        blocks.append(current)

    return blocks


# Convierte bloques a estructura final
def format_blocks(blocks):
    output = []

    for b in blocks:
        title = b["title"]
        content = "\n".join(b["content"])

        formatted = f"""
## {title}

{content}
""".strip()

        output.append(formatted)

    return "\n\n".join(output)