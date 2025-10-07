"""VTT subtitle parser and cleaner."""

import re
from pathlib import Path


def remove_html_tags(text: str) -> str:
    """
    Remove all HTML tags from text.

    :param text: The input text containing HTML tags
    :type text: str
    :return: Text with HTML tags removed
    :rtype: str
    """
    return re.sub(r'<.*?>', '', text)


def remove_timestamp_tags(text: str) -> str:
    """
    Remove inline timestamp tags from VTT subtitle text.

    :param text: The input text containing timestamp tags
    :type text: str
    :return: Text with timestamp tags removed
    :rtype: str
    """
    # Remove patterns like <00:39:45.119>
    return re.sub(r'<\d{2}:\d{2}:\d{2}\.\d{3}>', '', text)


def is_timestamp_line(line: str) -> bool:
    """
    Check if a line is a VTT timestamp line.

    :param line: The line to check
    :type line: str
    :return: True if line is a timestamp, False otherwise
    :rtype: bool
    """
    return ' --> ' in line


def clean_vtt_text(text: str) -> str:
    """
    Clean VTT subtitle text by removing timestamps and tags.

    :param text: Raw VTT subtitle text
    :type text: str
    :return: Cleaned text with only spoken words
    :rtype: str
    """
    lines = text.split('\n')
    cleaned_lines = []

    for line in lines:
        line = line.strip()

        # Skip empty lines and timestamp lines
        if not line or is_timestamp_line(line):
            continue

        # Skip lines that start with align: or position:
        if line.startswith('align:') or line.startswith('position:'):
            continue

        # Skip WEBVTT header lines
        if line.startswith('WEBVTT') or line.startswith('Kind:') or line.startswith('Language:'):
            continue

        # Remove HTML entities
        line = line.replace('&gt;&gt;', '\n')
        line = line.replace('&gt;', '>')
        line = line.replace('&lt;', '<')
        line = line.replace('&amp;', '&')
        line = line.replace('&nbsp;', ' ')

        # Remove timestamp tags and HTML tags
        line = remove_timestamp_tags(line)
        line = remove_html_tags(line)

        # Add cleaned line if it has content
        line = line.strip()
        if line:
            cleaned_lines.append(line)

    # Deduplicate consecutive identical lines
    deduplicated = []
    previous = None
    for line in cleaned_lines:
        if line != previous:
            deduplicated.append(line)
            previous = line

    # Join with spaces, then split by newlines to get individual speaker lines
    full_text = ' '.join(deduplicated)
    lines_list = full_text.split('\n')

    # Remove any remaining duplicate consecutive lines after splitting
    final_lines = []
    previous = None
    for line in lines_list:
        line = line.strip()
        if line and line != previous:
            final_lines.append(line)
            previous = line

    return '\n'.join(final_lines)


def parse_vtt_file(file_path: Path) -> str:
    """
    Parse a VTT file and return cleaned text.

    :param file_path: Path to the VTT file
    :type file_path: Path
    :return: Cleaned subtitle text
    :rtype: str
    """
    content = file_path.read_text(encoding='utf-8')
    return clean_vtt_text(content)
