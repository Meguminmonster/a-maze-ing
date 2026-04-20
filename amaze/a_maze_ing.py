import sys
from mazegen import MazeGenerator


def main() -> None:
    if len(sys.argv) != 2:
        print("Error: Uso incorrecto.")
        print("Ejecuta: python3 a_maze_ing.py <archivo_configuracion>")
        sys.exit(1)

    config_file: str = sys.argv[1]

    try:
        print(f"Leyendo configuración de: {config_file}...")
        width, height = 20, 15
        entry_pos, exit_pos = (0, 0), (19, 14)
        perfect = True
        output_file = "maze.txt"

        print("Generando laberinto...")
        generator = MazeGenerator(
            width=width,
            height=height,
            entry_pos=entry_pos,
            exit_pos=exit_pos,
            perfect=perfect
        )
        maze = generator.generate()

        print(f"Exportando laberinto a {output_file}...")
        print("Iniciando visualización interactiva...")

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
