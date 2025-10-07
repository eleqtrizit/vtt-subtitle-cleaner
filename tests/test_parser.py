"""Tests for VTT parser module."""

from subtitle_cleanup.parser import clean_vtt_text, is_timestamp_line, remove_html_tags, remove_timestamp_tags


def test_remove_html_tags():
    """Test HTML tag removal."""
    text = "<c>word</c> and <b>bold</b>"
    assert remove_html_tags(text) == "word and bold"


def test_remove_timestamp_tags():
    """Test timestamp tag removal."""
    text = "word<00:39:45.119><c> test</c>"
    result = remove_timestamp_tags(text)
    assert "<00:39:45.119>" not in result
    assert "word" in result


def test_is_timestamp_line():
    """Test timestamp line detection."""
    assert is_timestamp_line("00:39:44.960 --> 00:39:46.310 align:start position:0%") is True
    assert is_timestamp_line("This is subtitle text") is False


def test_clean_vtt_text():
    """Test full VTT text cleaning."""
    vtt_content = """00:39:44.960 --> 00:39:46.310 align:start position:0%
&gt;&gt; That's right. Get the full show. Help
support<00:39:45.119><c> the</c><00:39:45.280><c> future</c><00:39:45.440><c> of</c><00:39:45.599><c> independent</c>
<00:39:46.079><c> media</c>

00:39:46.310 --> 00:39:46.320 align:start position:0%
support the future of independent media


00:39:46.320 --> 00:39:49.480 align:start position:0%
support the future of independent media
at<00:39:46.480><c> breakingpoints.com.</c>"""

    result = clean_vtt_text(vtt_content)

    # Should not contain timestamp lines
    assert "-->" not in result

    # Should not contain HTML tags
    assert "<c>" not in result
    assert "</c>" not in result

    # Should not contain timestamp tags
    assert "<00:39" not in result

    # Should contain the actual words
    assert "That's right" in result
    assert "Get the full show" in result
    assert "support" in result
    assert "breakingpoints.com" in result
