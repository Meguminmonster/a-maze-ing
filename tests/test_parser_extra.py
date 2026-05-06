import pytest
from app.errors import ConfigError
from app.parser import parse_config


def test_binary_config_file(tmp_path):
    file = tmp_path / "bin.dat"
    file.write_bytes(b"\x00\xFF\x00INVALID")

    with pytest.raises(ConfigError) as exc:
        parse_config(str(file))

    assert "binary" in str(exc.value).lower()


def test_duplicate_key(tmp_path):
    file = tmp_path / "dup.txt"
    file.write_text(
        "WIDTH=20\n"
        "WIDTH=30\n"
        "HEIGHT=15\n"
        "ENTRY=0,0\n"
        "EXIT=19,14\n"
        "OUTPUT_FILE=maze.txt\n"
        "PERFECT=True\n"
    )

    with pytest.raises(ConfigError) as exc:
        parse_config(str(file))

    assert "Duplicate key" in str(exc.value)


def test_unknown_key(tmp_path):
    file = tmp_path / "unknown.txt"
    file.write_text(
        "WIDTH=20\n"
        "HEIGHT=15\n"
        "ENTRY=0,0\n"
        "EXIT=19,14\n"
        "OUTPUT_FILE=maze.txt\n"
        "PERFECT=True\n"
        "FOO=BAR\n"
    )

    with pytest.raises(ConfigError) as exc:
        parse_config(str(file))

    assert "Unknown keys" in str(exc.value)


def test_entry_with_single_number(tmp_path):
    file = tmp_path / "bad_entry.txt"
    file.write_text(
        "WIDTH=20\n"
        "HEIGHT=15\n"
        "ENTRY=5\n"
        "EXIT=19,14\n"
        "OUTPUT_FILE=maze.txt\n"
        "PERFECT=True\n"
    )

    with pytest.raises(ConfigError) as exc:
        parse_config(str(file))

    assert "x,y" in str(exc.value)


def test_invalid_perfect_value(tmp_path):
    file = tmp_path / "bad_perfect.txt"
    file.write_text(
        "WIDTH=20\n"
        "HEIGHT=15\n"
        "ENTRY=0,0\n"
        "EXIT=19,14\n"
        "OUTPUT_FILE=maze.txt\n"
        "PERFECT=maybe\n"
    )

    with pytest.raises(ConfigError) as exc:
        parse_config(str(file))

    assert "PERFECT" in str(exc.value)
