from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
BACKUP_SUFFIX = ".backup.ipynb"


def parse_string_end(text: str, start: int) -> int:
    index = start + 1
    while index < len(text):
        char = text[index]
        if char == "\\":
            index += 2
            continue
        if char == "\"":
            return index + 1
        index += 1
    raise ValueError("Unterminated JSON string")


def skip_whitespace(text: str, index: int) -> int:
    while index < len(text) and text[index] in " \t\r\n":
        index += 1
    return index


def skip_json_value(text: str, start: int) -> int:
    index = skip_whitespace(text, start)
    if text[index] == "\"":
        return parse_string_end(text, index)

    if text[index] in "[{":
        opener = text[index]
        closer = "}" if opener == "{" else "]"
        depth = 1
        index += 1
        while index < len(text):
            char = text[index]
            if char == "\"":
                index = parse_string_end(text, index)
                continue
            if char == opener:
                depth += 1
            elif char == closer:
                depth -= 1
                if depth == 0:
                    return index + 1
            index += 1
        raise ValueError("Unterminated JSON container")

    while index < len(text) and text[index] not in ",}]\r\n\t ":
        index += 1
    return index


def find_object_property(text: str, object_start: int, key: str):
    index = skip_whitespace(text, object_start)
    if text[index] != "{":
        raise ValueError("Expected JSON object")

    index += 1
    while True:
        index = skip_whitespace(text, index)
        if index >= len(text) or text[index] == "}":
            return None

        key_start = index
        key_end = parse_string_end(text, key_start)
        key_name = json.loads(text[key_start:key_end])

        index = skip_whitespace(text, key_end)
        if text[index] != ":":
            raise ValueError("Expected colon after JSON object key")

        value_start = skip_whitespace(text, index + 1)
        value_end = skip_json_value(text, value_start)

        if key_name == key:
            prop_start = key_start
            prop_end = value_end
            after_value = skip_whitespace(text, value_end)
            if after_value < len(text) and text[after_value] == ",":
                prop_end = after_value + 1
            else:
                before_key = key_start - 1
                while before_key >= 0 and text[before_key] in " \t\r\n":
                    before_key -= 1
                if before_key >= 0 and text[before_key] == ",":
                    prop_start = before_key
            return prop_start, prop_end, value_start, value_end

        index = skip_whitespace(text, value_end)
        if index < len(text) and text[index] == ",":
            index += 1


def remove_top_level_widgets_metadata(text: str) -> str | None:
    metadata = find_object_property(text, 0, "metadata")
    if metadata is None:
        return None

    _, _, metadata_start, _ = metadata
    widgets = find_object_property(text, metadata_start, "widgets")
    if widgets is None:
        return None

    prop_start, prop_end, _, _ = widgets
    cleaned = text[:prop_start] + text[prop_end:]
    json.loads(cleaned)
    return cleaned


def clean_notebook(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    cleaned = remove_top_level_widgets_metadata(text)
    if cleaned is None:
        return False

    path.write_text(cleaned, encoding="utf-8")
    return True


def iter_notebooks(root: Path):
    for path in sorted(root.rglob("*.ipynb")):
        if ".ipynb_checkpoints" in path.parts:
            continue
        yield path


def main() -> None:
    scanned = 0
    fixed = 0
    removed_backups = 0
    failed = 0

    for path in iter_notebooks(ROOT):
        relative_path = path.relative_to(ROOT)

        if path.name.endswith(BACKUP_SUFFIX):
            path.unlink()
            removed_backups += 1
            print(f"Removed backup: {relative_path}")
            continue

        scanned += 1
        try:
            if clean_notebook(path):
                fixed += 1
                print(f"Fixed: {relative_path}")
        except Exception as error:
            failed += 1
            print(f"Failed: {relative_path} ({error})")

    print(
        f"Done. Scanned {scanned} notebook(s), fixed {fixed}, "
        f"removed {removed_backups} backup file(s), failed {failed}."
    )


if __name__ == "__main__":
    main()
