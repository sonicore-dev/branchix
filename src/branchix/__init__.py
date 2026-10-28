"""Branchix: print a readable tree of directories and files."""

from .core import ASCII, UNICODE, TreeOptions, TreeResult, TreeStats, build_tree

__version__ = "0.1.0"

__all__ = [
    "ASCII",
    "UNICODE",
    "TreeOptions",
    "TreeResult",
    "TreeStats",
    "build_tree",
    "__version__",
]
