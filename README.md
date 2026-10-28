# Branchix

A lightweight, dependency-free CLI and Python library that prints a readable
tree of directories and files. Works on Linux, macOS and Windows.

## Install

```bash
pip install branchix
```

## Usage

```bash
branchix              # whole tree of the current directory
branchix -L 2         # limit depth to 2 levels
branchix path/to/dir  # another root
branchix -L 2 --save  # write to branchix-tree.txt
branchix --save=tree.md  # write to a custom file
```

Example:

```
.
├── src/
│   └── branchix/
│       ├── __init__.py
│       └── cli.py
├── tests/
└── README.md

3 directories, 3 files
```

### Options

| Option | Description |
| --- | --- |
| `PATH` | Root directory (default `.`) |
| `-L N`, `--level N` | Maximum depth (1 = root's children) |
| `-a`, `--all` | Include hidden entries (names starting with `.`) |
| `-d`, `--dirs-only` | Show directories only |
| `-I PATTERN`, `--ignore PATTERN` | Skip names matching a glob; repeatable (`-I node_modules -I "*.pyc"`) |
| `--save [FILE]` | Save to a file instead of printing (default `branchix-tree.txt`) |
| `--ascii` | Use ASCII characters instead of box-drawing characters |
| `-V`, `--version` | Show version |

Notes:

- Directories are listed first, then files, each sorted case-insensitively.
- Symlinks are shown as `name -> target` and are never followed.
- Unreadable directories are marked `[unreadable]`.
- Because `--save` takes an optional value, write `--save=FILE` (or put `PATH`
  first) when combining it with a path.
- Exit codes: `0` success, `1` runtime/IO error, `2` invalid usage or path.

## Python API

```python
from branchix import TreeOptions, build_tree

result = build_tree(".", TreeOptions(max_depth=2, ignore=("__pycache__",)))
print(result.render())
print(result.stats)  # TreeStats(directories=..., files=...)
```

## Development

```bash
git clone https://github.com/sonicore-dev/branchix
cd branchix
python -m pip install -e ".[dev]"
pytest
ruff check .
```

## Releasing

1. Update `__version__` in `src/branchix/__init__.py` (single source of truth)
   and add an entry to `CHANGELOG.md`.
2. Commit, tag (`git tag v0.1.0`) and push.
3. Create a GitHub Release; the `Publish to PyPI` workflow builds and uploads.

One-time setup: on PyPI, add a
[Trusted Publisher](https://docs.pypi.org/trusted-publishers/) for this repo
(workflow `publish.yml`, environment `pypi`), and create the `pypi` environment
in the GitHub repo settings.

## License

MIT
