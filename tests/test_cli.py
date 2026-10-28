import pytest

from branchix import __version__
from branchix.cli import DEFAULT_OUTPUT, main


def test_prints_tree(sample, capsys):
    assert main([str(sample), "-L", "1"]) == 0
    out = capsys.readouterr().out
    assert "src/" in out and "deep.py" not in out
    assert "2 directories, 1 file" in out


def test_save_default_name(sample, monkeypatch, capsys):
    monkeypatch.chdir(sample)
    assert main([".", "--save"]) == 0
    saved = (sample / DEFAULT_OUTPUT).read_text(encoding="utf-8")
    assert "README.md" in saved
    # The output file should not list itself.
    assert DEFAULT_OUTPUT not in saved
    assert "Saved tree to" in capsys.readouterr().out


def test_save_custom_name(sample, tmp_path_factory):
    target = tmp_path_factory.mktemp("out") / "tree.txt"
    assert main([str(sample), f"--save={target}"]) == 0
    assert "src/" in target.read_text(encoding="utf-8")


def test_save_unwritable(sample, capsys):
    assert main([str(sample), f"--save={sample / 'nope' / 'x.txt'}"]) == 1
    assert "cannot write" in capsys.readouterr().err


def test_missing_path(tmp_path, capsys):
    assert main([str(tmp_path / "missing")]) == 2
    assert "no such path" in capsys.readouterr().err


def test_file_path(sample, capsys):
    assert main([str(sample / "README.md")]) == 2
    assert "not a directory" in capsys.readouterr().err


@pytest.mark.parametrize("value", ["0", "-1", "abc"])
def test_invalid_level(sample, value, capsys):
    with pytest.raises(SystemExit) as exc:
        main([str(sample), "-L", value])
    assert exc.value.code == 2


def test_version(capsys):
    with pytest.raises(SystemExit) as exc:
        main(["--version"])
    assert exc.value.code == 0
    assert __version__ in capsys.readouterr().out
