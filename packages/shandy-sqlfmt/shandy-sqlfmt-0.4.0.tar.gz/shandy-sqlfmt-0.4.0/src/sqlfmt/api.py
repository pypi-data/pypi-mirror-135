import sys
from pathlib import Path
from typing import Iterable, Iterator, List, Set

from sqlfmt.cache import Cache, check_cache, load_cache, write_cache
from sqlfmt.exception import SqlfmtError
from sqlfmt.formatter import QueryFormatter
from sqlfmt.mode import Mode
from sqlfmt.report import STDIN_PATH, Report, SqlFormatResult


def format_string(source: str, mode: Mode) -> str:
    analyzer = mode.dialect.initialize_analyzer(line_length=mode.line_length)
    raw_query = analyzer.parse_query(source_string=source)
    formatter = QueryFormatter(mode)
    formatted_query = formatter.format(raw_query)
    return str(formatted_query)


def run(files: List[str], mode: Mode) -> Report:
    """
    Runs sqlfmt on all files in list of given paths (files), using the specified mode.

    Modifies sql files in place, by default. Check or diff mode do not modify files,
    they only create a report.

    Returns a Report that can be queried or printed.
    """

    matched_paths: Set[Path] = set()
    matched_paths.update(_generate_matched_paths([Path(s) for s in files], mode))

    cache = load_cache()
    results = list(_generate_results(matched_paths, cache, mode))
    report = Report(results, mode)

    if not (mode.check or mode.diff):
        _update_source_files(results)
    write_cache(cache, results, mode)

    return report


def _generate_matched_paths(paths: Iterable[Path], mode: Mode) -> Iterator[Path]:
    for p in paths:
        if p == STDIN_PATH:
            yield p
        elif p.is_file() and "".join(p.suffixes) in (mode.SQL_EXTENSIONS):
            yield p
        elif p.is_dir():
            yield from (_generate_matched_paths(p.iterdir(), mode))


def _generate_results(
    paths: Iterable[Path], cache: Cache, mode: Mode
) -> Iterator[SqlFormatResult]:
    """
    Runs sqlfmt on all files in an iterable of given paths, using the specified mode.
    Yields SqlFormatResults.
    """
    for p in paths:
        cached = check_cache(cache=cache, p=p)
        if cached:
            yield SqlFormatResult(
                source_path=p, source_string="", formatted_string="", from_cache=True
            )
        else:
            source = _read_path_or_stdin(p)
            try:
                formatted = format_string(source, mode)
                yield SqlFormatResult(
                    source_path=p, source_string=source, formatted_string=formatted
                )
            except SqlfmtError as e:
                yield SqlFormatResult(
                    source_path=p,
                    source_string=source,
                    formatted_string="",
                    exception=e,
                )


def _update_source_files(results: Iterable[SqlFormatResult]) -> None:
    """
    Overwrites file contents at result.source_path with result.formatted_string.

    No-ops for unchanged files, results without a source path, and empty files
    """
    for res in results:
        if res.has_changed and res.source_path != STDIN_PATH and res.formatted_string:
            with open(res.source_path, "w") as f:
                f.write(res.formatted_string)


def _read_path_or_stdin(path: Path) -> str:
    """
    If passed a Path, calls open() and read() and returns contents as a string.

    If passed a TextIO buffer, calls read() directly
    """
    if path == STDIN_PATH:
        source = sys.stdin.read()
    else:
        with open(path, "r") as f:
            source = f.read()
    return source
