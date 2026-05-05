# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    test_parser.py                                     :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: jpedra-v <marvin@42.fr>                    +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2026/05/05 15:58:37 by jpedra-v          #+#    #+#              #
#    Updated: 2026/05/05 16:09:27 by jpedra-v         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import pytest
from app.errors import ConfigError
from app.parser import MazeConfig, parse_config


# ---------------------------------------------------------
# TESTS EXISTENTES
# ---------------------------------------------------------

def test_config():
    config = parse_config("config.txt")
    assert config.width == 20
    assert config.height == 15
    assert config.entry == (0, 0)
    assert config.exit == (19, 14)
    assert config.perfect is True
    assert config.output_file == "maze.txt"


def test_config_file_not_found():
    with pytest.raises(ConfigError):
        parse_config("archivo_que_no_existe.txt")


def test_invalid_width(tmp_path):
    config_file = tmp_path / "bad_config.txt"
    config_file.write_text(
        "WIDTH=abc\nHEIGHT=15\nENTRY=0,0\nEXIT=19,14\nOUTPUT_FILE=maze.txt\nPERFECT=True\n"
    )
    with pytest.raises(ConfigError):
        parse_config(str(config_file))


# ---------------------------------------------------------
# TESTS NUEVOS (FIRMAS PENDIENTES)
# ---------------------------------------------------------

def test_missing_key(tmp_path):
    content = """WIDTH=20
HEIGHT=15
ENTRY=0,0
# Falta EXIT
OUTPUT_FILE=maze.txt
PERFECT=True
"""
    file = tmp_path / "config.txt"
    file.write_text(content)

    with pytest.raises(ConfigError) as exc:
        parse_config(str(file))

    assert "Missing keys" in str(exc.value)


def test_invalid_entry_format(tmp_path):
    content = """WIDTH=20
HEIGHT=15
ENTRY=0;0
EXIT=19,14
OUTPUT_FILE=maze.txt
PERFECT=True
"""
    file = tmp_path / "config.txt"
    file.write_text(content)

    with pytest.raises(ConfigError) as exc:
        parse_config(str(file))

    assert "ENTRY and EXIT must be in 'x,y'" in str(exc.value)


def test_entry_outside_bounds(tmp_path):
    content = """WIDTH=10
HEIGHT=10
ENTRY=20,5
EXIT=9,9
OUTPUT_FILE=maze.txt
PERFECT=True
"""
    file = tmp_path / "config.txt"
    file.write_text(content)

    with pytest.raises(ConfigError) as exc:
        parse_config(str(file))

    assert "ENTRY (20, 5) outside the maze" in str(exc.value)


def test_entry_equals_exit(tmp_path):
    content = """WIDTH=20
HEIGHT=15
ENTRY=5,5
EXIT=5,5
OUTPUT_FILE=maze.txt
PERFECT=True
"""
    file = tmp_path / "config.txt"
    file.write_text(content)

    with pytest.raises(ConfigError) as exc:
        parse_config(str(file))

    assert "ENTRY and EXIT coordinates must be different" in str(exc.value)


def test_invalid_perfect(tmp_path):
    content = """WIDTH=20
HEIGHT=15
ENTRY=0,0
EXIT=19,14
OUTPUT_FILE=maze.txt
PERFECT=maybe
"""
    file = tmp_path / "config.txt"
    file.write_text(content)

    with pytest.raises(ConfigError) as exc:
        parse_config(str(file))

    assert "PERFECT must be 'True' or 'False'" in str(exc.value)


def test_invalid_seed(tmp_path):
    content = """WIDTH=20
HEIGHT=15
ENTRY=0,0
EXIT=19,14
OUTPUT_FILE=maze.txt
PERFECT=True
SEED=abc
"""
    file = tmp_path / "config.txt"
    file.write_text(content)

    with pytest.raises(ConfigError) as exc:
        parse_config(str(file))

    assert "SEED must be an integer" in str(exc.value)


def test_maze_too_small(tmp_path):
    content = """WIDTH=1
HEIGHT=1
ENTRY=0,0
EXIT=0,0
OUTPUT_FILE=maze.txt
PERFECT=True
"""
    file = tmp_path / "config.txt"
    file.write_text(content)

    with pytest.raises(ConfigError) as exc:
        parse_config(str(file))

    assert "WIDTH and HEIGHT must be at least 2" in str(exc.value)
