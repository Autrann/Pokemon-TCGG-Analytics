## ETL Pipeline

Los datos se extraen desde la API TCGDex con su el SDK para python mediante un proceso ETL dividido en etapas.

### Extract

#### `extract_sets.py`

Obtiene todos los sets disponibles y los almacena en formato JSON en:

```text
data/raw/sets.json
```

#### `extract_cards.py`

Lee el archivo `sets.json`, descarga todas las cartas pertenecientes a cada set y genera un archivo JSON por expansión dentro de:

```text
data/raw/cards/
```

Ejemplo:

```text
data/raw/cards/
├── base1.json
├── base2.json
├── swsh3.json
└── ...
```

Al finalizar la extracción se muestra un resumen con:

- Número de sets procesados.
- Número total de cartas descargadas.
- Tiempo total de ejecución.

### Estructura del proyecto

```text
project/
│
├── data/
│   └── raw/
│       ├── sets.json
│       └── cards/
│           ├── base1.json
│           ├── base2.json
│           └── ...
│
├── src/
│   └── etl/
│       └── extract/
│           ├── extract_sets.py
│           └── extract_cards.py
│
```

## Dataset

Este repositorio incluye el dataset extraído desde la API de TCGDex utilizando el pipeline ETL desarrollado para el proyecto.

Los datos se encuentran en:

```text
data/raw/
├── sets.json
└── cards/
```

Si se desea regenerar el dataset desde la fuente original se pueden ejecutar ambos archivos previamente mencionados corriendo:

```bash
python src/etl/extract/extract_sets.py
python src/etl/extract/extract_cards.py
```

Los datos incluidos corresponden al momento de la extracción y pueden actualizarse ejecutando nuevamente el proceso ETL.