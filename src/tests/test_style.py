from pycodestyle import StyleGuide


def test_style():
    style = StyleGuide(max_line_length=120)
    result = style.check_files(['../../src'])
    assert result.total_errors == 0
