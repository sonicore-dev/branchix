# Changelog

All notable changes to this project are documented here.
The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/)
and this project adheres to [Semantic Versioning](https://semver.org/).

## [0.1.0] - 2026-10-28

### Added
- `branchix` CLI and Python API for printing directory trees.
- `-L/--level` depth limit, `-a/--all`, `-d/--dirs-only`, `-I/--ignore`.
- `--save [FILE]` to write the tree to a file (default `branchix-tree.txt`).
- Automatic ASCII fallback for terminals that cannot render Unicode; `--ascii` flag.
- Test suite and GitHub Actions workflows for CI and PyPI publishing.

[0.1.0]: https://github.com/sonicore-dev/branchix/releases/tag/v0.1.0
