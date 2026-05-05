*This project has been created as part of the 42 curriculum by \carrovir\, \jpedra-v/*

## Descripción

A‑Maze‑ing es un generador de laberintos escrito en Python 3.10+. 

- Lee un archivo de configuración.
- Genera un laberinto perfecto o imperfecto.
- Inserta un patrón “42” visible dentro del laberinto.
- Muestra el laberinto en ASCII con colores.
- Exporta el laberinto en formato hexadecimal.
- Calcula el camino más corto entre entrada y salida.
- Permite interacción mediante un menú (regenerar, mostrar camino, cambiar colores…).

## Instrucciones

- Python 3.10 o superior 

Instalación:
```bash
make install
```

Ejecución:
```bash
make run
```

Linting:
```bash
flake8
mypy

---

## Configuración

El archivo debe contener pares `KEY=VALUE`, uno por línea.

Ejemplo:

```
WIDTH=20
HEIGHT=15
ENTRY=0,0
EXIT=19,14
OUTPUT_FILE=maze.txt
PERFECT=True
SEED=42
```

### Claves obligatorias

| Clave | Descripción |
|-------|-------------|
| WIDTH | Anchura del laberinto |
| HEIGHT | Altura del laberinto |
| ENTRY | Coordenadas de entrada (x,y) |
| EXIT | Coordenadas de salida (x,y) |
| OUTPUT_FILE | Archivo de salida |
| PERFECT | True/False |

### Claves opcionales
- `SEED`: Semilla para reproducibilidad.

---

## Algoritmo

El algoritmo principal utilizado es Recursive Backtracking (DFS).

- Genera laberintos perfectos de forma natural.
- Es simple, eficiente y fácil de modificar.
- Permite añadir ciclos para laberintos imperfectos.
- Se integra muy bien con celdas representadas mediante bitmasks.

### Laberinto perfecto
- DFS visita todas las celdas sin crear ciclos.
- Garantiza un único camino entre entrada y salida.

### Laberinto imperfecto
- Tras el DFS, se rompen paredes aleatorias para introducir ciclos.
- Esto crea múltiples caminos posibles.

## Representación del laberinto

Cada celda contiene un entero de 4 bits:

| Bit | Dirección |
|-----|-----------|
| 0 | Norte |
| 1 | Este |
| 2 | Sur |
| 3 | Oeste |

Un bit en `1` significa pared cerrada.

Ejemplo: 
`0b1010` → paredes cerradas en Este y Oeste.

## Visualización

El proyecto incluye un render ASCII con colores:

- `E` → Entrada (verde)
- `X` → Salida (rojo)
- `·` → Camino más corto (cyan)
- Paredes coloreadas rotando entre varios colores
- Patrón “42” visible mediante celdas completamente cerradas

El menú permite:

1. Regenerar el laberinto
2. Mostrar/ocultar el camino
3. Cambiar colores
4. Salir

## Módulo reutilizable

El proyecto incluye un paquete instalable:

```
mazegen/
    __init__.py
    maze.py
    cell.py
    generator.py
```

### Construir el paquete

# 1. Crear un entorno virtual
python3 -m venv .venv
source .venv/bin/activate

# 2. Instalar la herramienta de construcción
pip install build

# 3. Construir el paquete
python3 -m build

# 4. Instalar el paquete generado
pip install dist/mazegen-1.0.0-py3-none-any.whl

# 5. Verificar que el paquete esta instalado correctamente
python3 -c "from mazegen import MazeGenerator; print('OK')"

### Uso básico

```python
from mazegen import MazeGenerator

gen = MazeGenerator(
    width=20,
    height=15,
    entry_pos=(0,0),
    exit_pos=(19,14),
    perfect=True,
    seed=42
)

maze = gen.generate()
```

### Acceso a la estructura

```python
cell = maze.get_cell(3, 5)
print(cell.walls)
```

### Roles
- jpedra-v: Generación del laberinto, módulo mazegen, parser.
- carrovir: Visualización ASCII, menú interactivo, exportación.
- conjunto: Validación, documentación, testing.

### Herramientas utilizadas
- Python 3.10 
- flake8, mypy 
- venv 
- Git 
- IA para acelerar tareas repetitivas

## Recursos

- Jamis Buck – Maze Generation Algorithms
- Documentación oficial de Python
- CLRS – BFS para shortest path

### Uso de IA
La IA se utilizó para:

- Generar ejemplos de README
- Revisar código para detectar inconsistencias
- Proponer mejoras de estructura
- Ayudar a redactar documentación

Todo el código fue revisado, entendido y validado manualmente.
