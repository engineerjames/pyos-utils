def test_normalize_sound_within_range() -> None:
    from pyos_utils.sound._sound_utilities import normalize_sound

    assert normalize_sound(0.5) == 0.5


def test_normalize_sound_below_range() -> None:
    from pyos_utils.sound._sound_utilities import normalize_sound

    assert normalize_sound(-0.5) == 0.0


def test_normalize_sound_above_range() -> None:
    from pyos_utils.sound._sound_utilities import normalize_sound

    assert normalize_sound(1.5) == 1.0


def test_normalize_sound_at_lower_bound() -> None:
    from pyos_utils.sound._sound_utilities import normalize_sound

    assert normalize_sound(0.0) == 0.0


def test_normalize_sound_at_upper_bound() -> None:
    from pyos_utils.sound._sound_utilities import normalize_sound

    assert normalize_sound(1.0) == 1.0
