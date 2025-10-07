"""Main CLI entry point for subtitle cleanup."""

import sys
from pathlib import Path

from subtitle_cleanup.parser import parse_vtt_file


def main():
    """
    Parse VTT subtitle file and print cleaned text.

    :return: Exit code (0 for success, 1 for error)
    :rtype: int
    """
    if len(sys.argv) < 2:
        print("Usage: python -m subtitle_cleanup <vtt_file>", file=sys.stderr)
        return 1

    vtt_path = Path(sys.argv[1])

    if not vtt_path.exists():
        print(f"Error: File not found: {vtt_path}", file=sys.stderr)
        return 1

    try:
        cleaned_text = parse_vtt_file(vtt_path)
        print(cleaned_text)
        return 0
    except Exception as e:
        print(f"Error processing file: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
