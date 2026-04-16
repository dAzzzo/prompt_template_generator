import sys
from utils import (
    read_file,
    save_file,
    clean_text,
    group_blocks,
    format_blocks,
    generate_output_name
)

def main():

    if len(sys.argv) < 2:
        input_file = input("Archivo input: ")
    else:
        input_file = sys.argv[2]

    output_file = generate_output_name(input_file)
    print("Leyendo archivo...")
    raw = read_file(input_file)

    print("Limpiando...")
    lines = clean_text(raw)

    print("Agrupando bloques...")
    blocks = group_blocks(lines)

    print("Formateando...")
    final = format_blocks(blocks)

    print(f"Guardando en {output_file}")
    save_file(output_file, final)

    print("OK")

if __name__ == "__main__":
    main()