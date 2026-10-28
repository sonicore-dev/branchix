import os

import pytest

from branchix import ASCII, TreeOptions, build_tree


def names(result):
    return [line.lstrip("│ ").split(" ", 1)[-1] for line in result.lines[1:]]


def test_full_tree_order_and_stats(sample):
    result = build_tree(sample)
    assert names(result) == [
        "docs/", "src/", "pkg/", "deep.py", "main.py", "README.md",
    ]
    assert result.lines[1].startswith("├── ")
    assert result.lines[-1].startswith("└── ")
    assert (result.stats.directories, result.stats.files) == (3, 3)


def test_max_depth(sample):
    result = build_tree(sample, TreeOptions(max_depth=1))
    assert names(result) == ["docs/", "src/", "README.md"]


def test_hidden_toggle(sample):
    assert ".hidden/" not in names(build_tree(sample))
    assert ".hidden/" in names(build_tree(sample, TreeOptions(show_hidden=True)))


def test_dirs_only(sample):
    result = build_tree(sample, TreeOptions(dirs_only=True))
    assert all(n.endswith("/") for n in names(result))
    assert result.stats.files == 0


def test_ignore_patterns(sample):
    result = build_tree(sample, TreeOptions(ignore=("*.py", "docs")))
    assert names(result) == ["src/", "pkg/", "README.md"]


def test_ascii_style(sample):
    result = build_tree(sample, TreeOptions(style=ASCII))
    assert result.lines[1].startswith("|-- ")


def test_empty_directory(tmp_path):
    result = build_tree(tmp_path)
    assert result.lines == [str(tmp_path)]
    assert result.stats.directories == 0


def test_not_a_directory(tmp_path):
    f = tmp_path / "a.txt"
    f.write_text("")
    with pytest.raises(NotADirectoryError):
        build_tree(f)


@pytest.mark.skipif(not hasattr(os, "symlink") or os.name == "nt", reason="symlinks")
def test_symlink_not_followed(tmp_path):
    (tmp_path / "real").mkdir()
    (tmp_path / "real" / "f.txt").write_text("")
    os.symlink(tmp_path / "real", tmp_path / "link")
    result = build_tree(tmp_path)
    assert any("link -> " in line for line in result.lines)
    assert sum("f.txt" in line for line in result.lines) == 1
