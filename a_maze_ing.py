"""Script principal para la ejecución de A-Maze-ing."""

import sys
# Aquí importarás tus futuros módulos de la carpeta app/ (Estudiante B)
# from app.parser import parse_config
# from app.printer import export_maze, interactive_loop

# Importamos el trabajo que ya hicimos del Estudiante A
from mazegen import MazeGenerator


def main() -> None:
    """Punto de entrada principal del programa."""
    # 1. Validar que nos pasan el config.txt
    if len(sys.argv) != 2:
        print("Error: Uso incorrecto.")
        print("Ejecuta: python3 a_maze_ing.py <archivo_configuracion>")
        sys.exit(1)

    config_file: str = sys.argv[1]

    # 2. Bloque TRY-EXCEPT gigante para evitar crasheos (Obligatorio)
    try:
        print(f"Leyendo configuración de: {config_file}...")

        # TODO: parse_config leerá el archivo y devolverá un diccionario
        # config = parse_config(config_file)

        # Valores simulados temporalmente para que compile:
        width, height = 20, 15
        entry_pos, exit_pos = (0, 0), (19, 14)
        perfect = True
        output_file = "maze.txt"

        print("Generando laberinto...")
        # 3. Instanciamos el módulo reutilizable (Estudiante A)
        generator = MazeGenerator(
            width=width,
            height=height,
            entry_pos=entry_pos,
            exit_pos=exit_pos,
            perfect=perfect
        )
        maze = generator.generate()

        print(f"Exportando laberinto a {output_file}...")
        # 4. Guardamos el archivo hexadecimal (Estudiante B)
        # export_maze(maze, output_file, entry_pos, exit_pos)

        print("Iniciando visualización interactiva...")
        # 5. Mostramos el menú y el renderizado (Estudiante B)
        # interactive_loop(maze)

    except FileNotFoundError:
        print(f"Error: No se encontró el archivo '{config_file}'.")
        sys.exit(1)
    except ValueError as e:
        print(f"Error de configuración: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error inesperado: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
