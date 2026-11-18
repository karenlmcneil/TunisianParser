from aeb_parser import analyze_word, analyze_text


def test_analyze_word_preserves_surface_and_segments():
    result = analyze_word("والكتاب")

    assert result["normalized"] == "والكتاب"
    assert result["surface"] == "والكتاب"
    assert result["segments"] == [
        {"text": "و", "pos": "C"},
        {"text": "ال", "pos": "DET"},
        {"text": "كتاب", "pos": "N"},
    ]
    assert result["stem"] == "كتاب"

def test_analyze_text_preserves_word_boundaries():
    text = "والكتاب مشيت للدار"

    result = analyze_text(text)

    assert [word["surface"] for word in result] == [
        "والكتاب", "مشيت", "للدار"
    ]

    assert [word["stem"] for word in result] == [
        "كتاب", "مشي", "دار"
    ]

    assert result[0]["segments"] == [
        {"text": "و", "pos": "C"},
        {"text": "ال", "pos": "DET"},
        {"text": "كتاب", "pos": "N"},
    ]

def test_analyze_text_preserves_original_offsets():
    text = "إلّي مشيت، والكتاب."

    result = analyze_text(text)

    for token in result:
        assert text[token["start"]:token["end"]] == token["surface"]

    assert result[0]["surface"] == "إلّي"
    assert result[0]["normalized"] == "الي"
    assert result[0]["start"] == 0
    assert result[0]["end"] == 4

def test_analyze_text_handles_punctuation():
    result = analyze_text("مشيت!")

    assert result[-1] == {
        "surface": "!",
        "normalized": "!",
        "start": 4,
        "end": 5,
        "segments": [{"text": "!", "pos": "PUNCT"}],
        "stem": None,
    }

def test_analyze_text_handles_foreign_words():
    result = analyze_text("الdiscours")

    assert [word["surface"] for word in result] == [
        "ال", "discours"
    ]

    assert result[1]["segments"] == [
        {"text": "discours", "pos": "FW"}
    ]

def test_analyze_word_normalizes_input():
    result = analyze_word("إلّي")

    assert result["surface"] == "إلّي"
    assert result["normalized"] == "الي"
    assert result["segments"] == [
        {"text": "الي", "pos": "REL"}
    ]
    assert result["stem"] == "الي"

def test_analyze_word_handles_predefined_vocabulary():
    result = analyze_word("باش")

    assert result["segments"] == [
        {"text": "باش", "pos": "PART"}
    ]

def test_analyze_word_handles_foreign_words():
    result = analyze_word("discours")

    assert result["segments"] == [
        {"text": "discours", "pos": "FW"}
    ]
    assert result["stem"] is None

def test_analyze_word_handles_punctuation():
    result = analyze_word("!")

    assert result["segments"] == [
        {"text": "!", "pos": "PUNCT"}
    ]
    assert result["stem"] is None

def test_analyze_text_preserves_repeated_words_and_paragraphs():
    text = "كتاب كتاب\n\nإلّي"

    result = analyze_text(text)

    assert [item["surface"] for item in result] == [
        "كتاب", "كتاب", "إلّي"
    ]

    for item in result:
        assert text[item["start"]:item["end"]] == item["surface"]

    assert result[0]["start"] == 0
    assert result[1]["start"] == 5
    assert result[2]["start"] == 11
    assert result[2]["normalized"] == "الي"

def test_analysis_preserves_mixed_script_unicode_offsets():
    text = "إلّي الdiscours متاعو!\nوالكتاب"

    result = analyze_text(text)

    assert [item["surface"] for item in result] == [
        "إلّي",
        "ال",
        "discours",
        "متاعو",
        "!",
        "والكتاب",
    ]

    for item in result:
        assert text[item["start"]:item["end"]] == item["surface"]

    assert result[0]["normalized"] == "الي"
    assert result[2]["segments"] == [
        {"text": "discours", "pos": "FW"}
    ]
    assert result[-1]["stem"] == "كتاب"

def test_parser_loads_reference_corpus_from_another_directory(
    tmp_path, monkeypatch
):
    import importlib
    from aeb_parsing import goodness_of_fit

    monkeypatch.chdir(tmp_path)

    importlib.reload(goodness_of_fit)

    assert goodness_of_fit.fd.N() > 0
