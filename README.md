# Prompt Template Generator (TXT Cleaner & Structurer)

![Python](https://img.shields.io/badge/Python-3.8+-blue)
![Sin dependencias](https://img.shields.io/badge/dependencias-ninguna-green)
![Determinista](https://img.shields.io/badge/IA-no%20usa-lightgrey)

Herramienta en Python para convertir textos "sucios" (extraídos de PDFs o PowerPoints) en apuntes estructurados y listos para estudio o uso en sistemas de recuperación de información (RAG).

No utiliza IA. Todo el procesamiento es determinista (reglas + parsing).

---

## ¿Qué hace?

Convierte un archivo `.txt` desordenado en un archivo estructurado con formato:

- Secciones organizadas (`##`)
- Bloques de contenido agrupados
- Limpieza de ruido (saltos, páginas, texto innecesario)
- Estructura homogénea para estudio o reutilización

---

## Estructura del proyecto

```
project/
├── main.py
├── utils.py
└── template.txt
```

---

## Uso

### Opción 1: ejecución por argumento (recomendado)

```bash
python main.py archivo.txt
```

Ejemplo:

```bash
python main.py /home/user/temario/ejemplo.txt
```

Salida:

```
ejemplo_prompt.txt
```

---

### Opción 2: modo interactivo

```bash
python main.py
```

El programa pedirá:

```
Archivo input:
```

Debes introducir SOLO la ruta del archivo:

```
/home/user/temario/ejemplo.txt
```

---

## Resultado

El programa genera un nuevo archivo:

```
nombre_original_prompt.txt
```

Ejemplo:

```
ejemplo.txt → ejemplo_prompt.txt
```

---

## Cómo funciona

Pipeline interno:

```
TXT input
   ↓
Limpieza de ruido
   ↓
Detección de bloques (títulos / contenido)
   ↓
Agrupación estructurada
   ↓
Formateo en plantilla
   ↓
TXT final estructurado
```

---

## Qué detecta automáticamente

- Títulos (UD1, mayúsculas, encabezados)
- Listas y contenido asociado
- Bloques de información relacionados
- Texto irrelevante (páginas, ruido básico OCR)

---

## Requisitos

- Python 3.8+

No requiere librerías externas.

---

## Limitaciones

- No interpreta semántica (no usa IA)
- La calidad depende del texto de entrada
- Diseñado para textos tipo PDF/PPT convertidos a TXT

---

## Uso recomendado

Ideal para:

- Apuntes de universidad
- Temarios de oposiciones
- Material técnico (programación, sistemas, etc.)
- Preparación de bases para sistemas RAG o IA posterior

---

## Ejemplo de mejora del input

❌ Texto sucio:

```
Page 1
PROGRAMACION MULTIHILO
hilo es una secuencia...
```

✔ Salida:

```
## UD1 PROGRAMACION MULTIHILO
hilo es una secuencia...
```

---

## Idea del proyecto

Este proyecto transforma documentos desestructurados en conocimiento organizado, listo para estudio o procesamiento automático.

---

## Futuras mejoras (opcional)

- Detección avanzada de definiciones y ejemplos
- Exportación a PDF
- Modo examen (generación de preguntas)
- Integración con sistemas RAG