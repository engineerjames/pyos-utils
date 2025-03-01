from pyos_utils._sound_utilities import normalize_sound


def test_normalize_sound_within_range() -> None:
    assert normalize_sound(0.5) == 0.5


def test_normalize_sound_below_range() -> None:
    assert normalize_sound(-0.5) == 0.0


def test_normalize_sound_above_range() -> None:
    assert normalize_sound(1.5) == 1.0


def test_normalize_sound_at_lower_bound() -> None:
    assert normalize_sound(0.0) == 0.0


def test_normalize_sound_at_upper_bound() -> None:
    assert normalize_sound(1.0) == 1.0
