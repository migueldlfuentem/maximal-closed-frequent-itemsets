# Maximal and Closed Frequent Itemsets Mining

Implementación de algoritmos para descubrir **maximal** y **closed** frequent itemsets a partir de datos transaccionales, usando Python puro sin librerías externas.

## Requisitos

- Python 3.9+
- Sin dependencias externas para la funcionalidad principal

## Instalación

```bash
# Crear entorno virtual
python -m venv .venv
source .venv/bin/activate  # En Windows: .venv\Scripts\activate

# Instalar dependencias (solo para desarrollo)
pip install -r requirements.txt
```

## Ejecución Rápida

```bash
# Ejecutar con configuración por defecto (5% soporte mínimo)
python main.py

# Ejecutar con parámetros personalizados
python main.py --data data/groceries.csv --min-support 0.02 --limit 500

# Ver ayuda
python main.py --help
```

## Opciones de Línea de Comandos

| Opción | Corto | Por Defecto | Descripción |
|--------|-------|-------------|-------------|
| `--data` | `-d` | `data/groceries.csv` | Ruta al dataset CSV |
| `--min-support` | `-s` | `0.05` | Soporte mínimo (0.0 a 1.0) |
| `--limit` | `-l` | None | Máximo de transacciones a cargar |
| `--top` | `-t` | `20` | Número de resultados a mostrar |
| `--header` | - | `auto` | Si el CSV tiene cabecera: `true`, `false`, o `auto` |

## Formatos de Dataset Soportados

### Formato Lista de Items (groceries.csv)
Cada fila contiene items separados por comas:
```
whole milk,butter,bread
yogurt,whole milk
bread,butter,eggs,milk
```

### Formato Matriz Binaria (market.csv)
Primera fila: nombres de items. Filas siguientes: valores 0/1 separados por punto y coma:
```
Bread;Milk;Butter;Eggs
1;1;1;0
0;1;0;1
1;0;1;1
```

## Estructura del Proyecto

```
maximal-closed-frequent-itemsets/
├── data/
│   ├── groceries.csv     # Dataset de supermercado (formato lista)
│   ├── market.csv        # Dataset de mercado (formato matriz binaria)
│   └── validation.csv    # Dataset de validación
├── src/
│   ├── __init__.py
│   ├── data_loader.py    # Carga y parsing de CSV
│   ├── apriori.py        # Algoritmo Apriori
│   ├── closed_itemsets.py   # Detección de closed itemsets
│   └── maximal_itemsets.py  # Detección de maximal itemsets
├── main.py               # Punto de entrada CLI
├── README.md             # Este archivo
├── METODOLOGIA.md        # Explicación detallada del algoritmo (español)
└── requirements.txt      # Dependencias
```

## Ejemplo de Salida

```
============================================================
MAXIMAL AND CLOSED FREQUENT ITEMSETS MINING
============================================================

Loading transactions from: data/validation.csv
  - Transactions loaded: 20
  - Unique items: 5
  - Min support: 0.15 (3 transactions)

Finding frequent itemsets (Apriori algorithm)...
  - Frequent itemsets found: 13

Finding closed itemsets...
  - Closed itemsets found: 8

Finding maximal itemsets...
  - Maximal itemsets found: 2

SUMMARY
  - Frequent itemsets: 13
  - Closed itemsets:   8 (61.5% of frequent)
  - Maximal itemsets:  2 (15.4% of frequent)

  Property verification: |maximal| ≤ |closed| ≤ |frequent|
  2 ≤ 8 ≤ 13: ✓
```

## Autor

Miguel de la Fuente Muñoz