"""Black-and-white conversion algorithms."""

from typing import Literal

import numpy as np
from PIL import Image

AlgorithmName = Literal[
    "average", "luminosity", "threshold", "max_channel", "min_channel"
]
MAX_CHANNEL_VALUE = 255

ALGORITHMS: tuple[AlgorithmName, ...] = (
    "average",
    "luminosity",
    "threshold",
    "max_channel",
    "min_channel",
)


def _to_rgb_array(image: Image.Image) -> np.ndarray:
    """Convert an image to a three-channel RGB NumPy array."""
    return np.asarray(image.convert("RGB"), dtype=np.uint8)


def average(image: Image.Image) -> Image.Image:
    """Convert by averaging red, green, and blue channels."""
    data = _to_rgb_array(image).astype(np.uint16)
    gray = data.mean(axis=2).astype(np.uint8)
    return Image.fromarray(gray, mode="L")


def luminosity(image: Image.Image) -> Image.Image:
    """Convert using the luminosity formula 0.299R + 0.587G + 0.114B."""
    data = _to_rgb_array(image).astype(np.float32)
    gray = np.dot(data[..., :3], np.array([0.299, 0.587, 0.114], dtype=np.float32))
    return Image.fromarray(np.clip(gray, 0, 255).astype(np.uint8), mode="L")


def threshold(image: Image.Image, threshold_value: int = 128) -> Image.Image:
    """Convert to binary black-and-white using a threshold value."""
    if not 0 <= threshold_value <= MAX_CHANNEL_VALUE:
        msg = "Threshold must be between 0 and 255."
        raise ValueError(msg)
    gray = np.asarray(luminosity(image), dtype=np.uint8)
    binary = np.where(gray >= threshold_value, MAX_CHANNEL_VALUE, 0).astype(np.uint8)
    return Image.fromarray(binary, mode="L")


def max_channel(image: Image.Image) -> Image.Image:
    """Convert by taking the maximum RGB channel value for each pixel."""
    gray = _to_rgb_array(image).max(axis=2).astype(np.uint8)
    return Image.fromarray(gray, mode="L")


def min_channel(image: Image.Image) -> Image.Image:
    """Convert by taking the minimum RGB channel value for each pixel."""
    gray = _to_rgb_array(image).min(axis=2).astype(np.uint8)
    return Image.fromarray(gray, mode="L")


def convert_image(
    image: Image.Image,
    algorithm: AlgorithmName,
    threshold_value: int = 128,
) -> Image.Image:
    """Apply a selected conversion algorithm to an image."""
    match algorithm:
        case "average":
            return average(image)
        case "luminosity":
            return luminosity(image)
        case "threshold":
            return threshold(image, threshold_value)
        case "max_channel":
            return max_channel(image)
        case "min_channel":
            return min_channel(image)
