import pycodestyle


def test_style():
    style = pycodestyle.StyleGuide(max_line_length=100)
    result = style.check_files(['./src'])
    assert result.total_errors == 1
