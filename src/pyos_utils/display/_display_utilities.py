def get_bit_depth_from_colors(colors: int) -> int:
    """
    Get the bit depth from the number of colors.

    :param colors: The number of colors.

    :returns: The bit depth.
    """
    if colors <= 0:
        raise ValueError("Number of colors must be positive and greater than zero.")  # noqa: EM101, TRY003

    return (colors - 1).bit_length()
