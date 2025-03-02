def normalize_sound(sound: float) -> float:
    """Normalize the sound level to a valid (0.0 <= s <= 1.0) range."""
    return max(0.0, min(1.0, sound))
