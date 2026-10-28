"""Command-line interface for Branchix."""

from __future__ import annotations

import argparse
import os
import sys
from collections.abc import Sequence
from pathlib import Path

from . import __version__
from .core import ASCII, UNICODE, TreeOptions, TreeStats, build_tree

DEFAULT_OUTPUT = "branchix-tree.txt"


def _positive_int(value: str) -> int:
    try:
        number = int(value)
    except ValueError:
        raise argparse.ArgumentTypeError(f"invalid integer: {value!r}") from None
    if number < 1:
        raise argparse.ArgumentTypeError("depth must be 1 or greater")
    return number


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="branchix",
        description="Print a readable tree of directories and files.",
        epilog="Tip: use --save=FILE (with '=') when a PATH argument follows.",
    )
    parser.add_argument("path", nargs="?", default=".", help="root directory (default: .)")
    parser.add_argument(
        "-L", "--level", type=_positive_int, metavar="N", help="maximum depth to display"
    )
    parser.add_argument("-a", "--all", action="store_true", help="include hidden entries")
    parser.add_argument("-d", "--dirs-only", action="store_true", help="list directories only")
    parser.add_argument(
        "-I", "--ignore", action="append", default=[], metavar="PATTERN",
        help="skip names matching a glob pattern (repeatable)",
    )
    parser.add_argument(
        "--save", nargs="?", const=DEFAULT_OUTPUT, default=None, metavar="FILE",
        help=f"save to a file instead of printing (default: {DEFAULT_OUTPUT})",
    )
    parser.add_argument("--ascii", action="store_true", help="use ASCII characters only")
    parser.add_argument("-V", "--version", action="version", version=f"%(prog)s {__version__}")
    return parser


def _can_encode(stream, text: str) -> bool:
    encoding = getattr(stream, "encoding", None) or "utf-8"
    try:
        text.encode(encoding)
    except (UnicodeEncodeError, LookupError):
        return False
    return True


def _summary(stats: TreeStats, dirs_only: bool) -> str:
    d = f"{stats.directories} director{'y' if stats.directories == 1 else 'ies'}"
    if dirs_only:
        return d
    return f"{d}, {stats.files} file{'' if stats.files == 1 else 's'}"


def _error(message: str) -> None:
    print(f"branchix: error: {message}", file=sys.stderr)


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    root = Path(args.path)

    if not root.exists():
        _error(f"no such path: {root}")
        return 2
    if not root.is_dir():
        _error(f"not a directory: {root}")
        return 2

    use_ascii = args.ascii
    if args.save is None and not use_ascii:
        use_ascii = not _can_encode(sys.stdout, UNICODE.branch + UNICODE.last + UNICODE.pipe)

    exclude = frozenset()
    if args.save is not None:
        exclude = frozenset({Path(args.save).resolve()})

    options = TreeOptions(
        max_depth=args.level,
        show_hidden=args.all,
        dirs_only=args.dirs_only,
        ignore=tuple(args.ignore),
        exclude_paths=exclude,
        style=ASCII if use_ascii else UNICODE,
    )

    try:
        result = build_tree(root, options)
    except OSError as exc:
        _error(str(exc))
        return 1

    text = result.render() + "\n\n" + _summary(result.stats, args.dirs_only) + "\n"

    if args.save is not None:
        target = Path(args.save)
        try:
            target.write_text(text, encoding="utf-8", newline="\n")
        except OSError as exc:
            _error(f"cannot write {target}: {exc.strerror or exc}")
            return 1
        print(f"Saved tree to {target}")
        return 0

    try:
        sys.stdout.write(text)
        sys.stdout.flush()
    except BrokenPipeError:
        # The reader closed the pipe, so just exit quietly.
        os.dup2(os.open(os.devnull, os.O_WRONLY), sys.stdout.fileno())
    return 0


if __name__ == "__main__":
    sys.exit(main())
