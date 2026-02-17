from app.subtitles import Segment, to_srt, to_vtt


def test_to_srt_format():
    content = to_srt([
        Segment(start=0, end=1.234, text="Hola"),
        Segment(start=62.5, end=65.0, text="Mundo"),
    ])

    assert "00:00:00,000 --> 00:00:01,234" in content
    assert "00:01:02,500 --> 00:01:05,000" in content
    assert "Hola" in content
    assert "Mundo" in content


def test_to_vtt_format():
    content = to_vtt([Segment(start=0.1, end=2.2, text="Texto")])
    assert content.startswith("WEBVTT")
    assert "00:00:00.100 --> 00:00:02.200" in content
