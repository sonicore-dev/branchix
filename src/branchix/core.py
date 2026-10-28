"""Tree-building logic. Pure Python, standard library only."""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from fnmatch import fnmatchcase
from pathlib import Path

__all__ = ["ASCII", "UNICODE", "TreeOptions", "TreeResult", "TreeStats", "build_tree"]


@dataclass(frozen=True)
class TreeStyle:
    branch: str
    last: str
    pipe: str
    space: str


UNICODE = TreeStyle("├── ", "└── ", "│   ", "    ")
ASCII = TreeStyle("|-- ", "`-- ", "|   ", "    ")


@dataclass
class TreeOptions:
    """Settings controlling which entries are shown and how."""

    # None means no limit, 1 shows only the root's children.
    max_depth: int | None = None
    show_hidden: bool = False
    dirs_only: bool = False
    # Glob patterns matched against entry names.
    ignore: tuple = ()
    # Resolved paths to leave out.
    exclude_paths: frozenset = field(default_factory=frozenset)
    style: TreeStyle = UNICODE


@dataclass
class TreeStats:
    directories: int = 0
    files: int = 0


@dataclass
class TreeResult:
    lines: list
    stats: TreeStats

    def render(self) -> str:
        return "\n".join(self.lines)


def build_tree(root, options: TreeOptions | None = None) -> TreeResult:
    """Build the tree for ``root``. Raises ``NotADirectoryError`` if not a dir."""
    options = options or TreeOptions()
    root = Path(root)
    if not root.is_dir():
        raise NotADirectoryError(f"not a directory: {root}")
    lines = [str(root)]
    stats = TreeStats()
    _walk(root, "", 1, options, lines, stats)
    return TreeResult(lines, stats)


def _is_dir(entry: os.DirEntry) -> bool:
    try:
        return entry.is_dir(follow_symlinks=False)
    except OSError:
        return False


def _read_entries(directory: Path, options: TreeOptions):
    """Return filtered, sorted entries, or None if unreadable."""
    try:
        with os.scandir(directory) as it:
            entries = list(it)
    except OSError:
        return None

    def keep(entry: os.DirEntry) -> bool:
        name = entry.name
        if not options.show_hidden and name.startswith("."):
            return False
        if any(fnmatchcase(name, pat) for pat in options.ignore):
            return False
        if options.dirs_only and not _is_dir(entry):
            return False
        if options.exclude_paths and Path(entry.path).resolve() in options.exclude_paths:
            return False
        return True

    entries = [e for e in entries if keep(e)]
    entries.sort(key=lambda e: (not _is_dir(e), e.name.lower(), e.name))
    return entries


def _label(entry: os.DirEntry) -> str:
    if _is_dir(entry):
        return entry.name + "/"
    if entry.is_symlink():
        try:
            return f"{entry.name} -> {os.readlink(entry.path)}"
        except OSError:
            pass
    return entry.name


def _walk(directory, prefix, depth, options, lines, stats) -> None:
    if options.max_depth is not None and depth > options.max_depth:
        return
    entries = _read_entries(directory, options)
    if entries is None:
        lines[-1] += "  [unreadable]"
        return
    style = options.style
    for index, entry in enumerate(entries):
        is_last = index == len(entries) - 1
        lines.append(prefix + (style.last if is_last else style.branch) + _label(entry))
        if _is_dir(entry):
            stats.directories += 1
            extension = style.space if is_last else style.pipe
            _walk(Path(entry.path), prefix + extension, depth + 1, options, lines, stats)
        else:
            stats.files += 1
