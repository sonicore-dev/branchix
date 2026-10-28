import pytest


@pytest.fixture
def sample(tmp_path):
    (tmp_path / "src" / "pkg").mkdir(parents=True)
    (tmp_path / "docs").mkdir()
    (tmp_path / ".hidden").mkdir()
    (tmp_path / "README.md").write_text("hi")
    (tmp_path / "src" / "main.py").write_text("")
    (tmp_path / "src" / "pkg" / "deep.py").write_text("")
    (tmp_path / ".hidden" / "x.txt").write_text("")
    return tmp_path
