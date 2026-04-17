# Prompt Template Generator

![Python](https://img.shields.io/badge/Python-3.8+-blue)
![Dependency](https://img.shields.io/badge/dependency-pypdf-green)
![Deterministic](https://img.shields.io/badge/AI-not%20used-lightgrey)

A lightweight Python tool that converts unstructured TXT or PDF content into clean, structured text suitable for study, indexing, or downstream processing.

This project is fully deterministic. It does not rely on AI or external services.

---

## Features

* Cleans noisy text (OCR artifacts, page numbers, formatting issues)
* Detects structural elements (titles, sections)
* Groups content into logical blocks
* Outputs consistent, structured text format
* Supports both `.txt` and `.pdf` inputs

---

## Project Structure

```
project/
├── main.py
├── utils.py
```

---

## Installation

```bash
pip install pypdf
```

Recommended: use a virtual environment.

---

## Usage

### CLI mode

```bash
python main.py file.txt
python main.py file.pdf
```

### Interactive mode

```bash
python main.py
```

You will be prompted to configure:

* Output language (EN default / ES optional)
* Output file name
* Output directory
* Input type

---

## Output

The tool generates:

```
<original_name>_prompt.txt
```

Example:

```
notes.pdf → notes_prompt.txt
```

---

## Processing Pipeline

### TXT

```
TXT → Cleaning → Block Detection → Structuring → Output
```

### PDF

```
PDF → Text Extraction → Cleaning → Block Detection → Structuring → Output
```

---

## Detection Heuristics

* Uppercase lines → treated as titles
* Lines starting with `UD` → treated as units
* Short lines ending with `:` → treated as headings
* Numeric-only lines and page markers → removed

---

## Limitations

* No semantic understanding (rule-based only)
* PDF extraction quality depends on source
* Not suitable for scanned PDFs (no OCR)

---

## Use Cases

* Academic notes structuring
* Study material normalization
* Preprocessing for search or RAG pipelines
* Cleaning exported slides or documents

---

## Example

**Input:**

```
Page 1
MULTITHREADED PROGRAMMING
thread is a sequence...
```

**Output:**

```
## MULTITHREADED PROGRAMMING
thread is a sequence...
```

---

## Future Work

* Improved structure detection
* List and bullet recognition
* Optional translation layer (API-based)
* JSON / structured export
* RAG-ready output formats

---

## License

MIT
