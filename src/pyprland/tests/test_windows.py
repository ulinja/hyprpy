"""Unit tests for the :class:`pyprland.models.Window` class.

WARNING
=======
These tests are obsolete. I will replace them in the future.
"""

from pathlib import Path

import pytest
from pydantic import ValidationError

from pyprland.models import Window


path_to_testdata = Path(__file__).absolute().parent / 'testdata' / 'windows.json'


@pytest.fixture
def data_valid() -> str:
    with open(path_to_testdata, 'r') as json_file:
        return json_file.read()


def test_valid_from_json(data_valid):
    result = Window.model_validate_json(data_valid)
    assert len(result) == 6
    assert isinstance(result[0], windows.Window)
    assert result[0].address == "0x325eca0"
    assert result[0].position_x == 145

    assert result[4].address == "0x3282b70"
    assert result[4].is_mapped == True
    assert result[4].is_hidden == False
    assert result[4].position_x == 11
    assert result[4].position_y == 41
    assert result[4].width == 1344
    assert result[4].height == 716
    assert result[4].workspace_id == 3
    assert result[4].workspace_name == "3"
    assert result[4].is_floating == False
    assert result[4].monitor_id == 0
    assert result[4].wm_class == "kitty"
    assert result[4].title == "hyprctl -j clients | ~"
    assert result[4].initial_wm_class == "kitty"
    assert result[4].initial_title == "fish"
    assert result[4].pid == 54486
    assert result[4].is_xwayland == False
    assert result[4].is_pinned == False
    assert result[4].is_fullscreen == False
    assert result[4].fullscreen_mode == 0
    assert result[4].is_fake_fullscreen == False


def test_invalid_json_syntax(data_valid):
    invalid_json = data_valid.replace('"', '')
    with pytest.raises(ParseError):
        windows.Window._from_json(invalid_json)

def test_invalid_json_structure_keys_missing(data_valid):
    keys_missing = data_valid.replace('"pid": 12032,', '')
    with pytest.raises(ParseError):
        windows.Window._from_json(keys_missing)

def test_invalid_json_structure_list_size(data_valid):
    too_many_window_dimensions = data_valid.replace('"size": [1344, 716]', '"size": [1344, 716, 69]')
    with pytest.raises(ParseError):
        windows.Window._from_json(too_many_window_dimensions)

def test_invalid_data_type(data_valid):
    wrong_data_type = data_valid.replace('"pid": 55144', '"pid": [55144]')
    with pytest.raises(ParseError):
        windows.Window._from_json(wrong_data_type)

def test_invalid_address_format(data_valid):
    wrong_address = data_valid.replace('0x32318e0', '0x1234U')
    with pytest.raises(ParseError):
        windows.Window._from_json(wrong_address)


def test_window_id_conversion(data_valid):
    window = windows.Window._from_json(data_valid)[1]
    assert window.id_as_int == int("0x32318e0", 16)
