import pycodestyle
import os


def test_style():
    os.system('pycodestyle ./src --show-source')
    style = pycodestyle.StyleGuide()
    result = style.check_files(['./src'])
    assert result.total_errors == 0
