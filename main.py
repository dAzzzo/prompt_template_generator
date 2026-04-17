import os
import sys
from utils import (
    read_file,
    save_file,
    clean_text,
    group_blocks,
    format_blocks,
    generate_output_name,
    read_pdf_text,
    sanitize_path
)


def ask_output_name():
    name = input("Output file name (empty = auto): ").strip()
    if not name:
        return None
    if not name.endswith(".txt"):
        name += ".txt"
    return name


def ask_output_dir():
    out_dir = input("Output directory (empty = same as input): ").strip()
    return out_dir if out_dir else None


def ask_input_type(input_file):
    if input_file.lower().endswith(".pdf"):
        return "pdf"

    print("\nInput type:")
    print("1. TXT (default)")
    print("2. PDF")
    opt = input("Option [1/2, default=1]: ").strip()
    return "pdf" if opt == "2" else "txt"


def process_content(raw_text, default_title):
    print("Cleaning...")
    lines = clean_text(raw_text)

    print("Grouping blocks...")
    blocks = group_blocks(lines, default_title=default_title)

    print("Formatting...")
    return format_blocks(blocks)


def main():
    if len(sys.argv) >= 2:
        input_file = sanitize_path(sys.argv[1])
        custom_name = None
        output_dir = None
        input_type = "pdf" if input_file.lower().endswith(".pdf") else "txt"
    else:
        print("=== Prompt Template Generator ===")
        input_file = sanitize_path(input("Input file path: "))
        custom_name = ask_output_name()
        output_dir = ask_output_dir()
        input_type = ask_input_type(input_file)

    if not os.path.exists(input_file):
        print(f"Error: file not found -> {input_file}")
        sys.exit(1)

    base_title = os.path.splitext(os.path.basename(input_file))[0]

    output_file = generate_output_name(
        input_file,
        output_dir=output_dir,
        custom_name=custom_name
    )

    print("Reading file...")
    if input_type == "pdf":
        raw = read_pdf_text(input_file)
    else:
        raw = read_file(input_file)

    final = process_content(raw, base_title)

    os.makedirs(os.path.dirname(output_file) or ".", exist_ok=True)

    print(f"Saving to {output_file}")
    save_file(output_file, final)

    print("Done")


if __name__ == "__main__":
    main()