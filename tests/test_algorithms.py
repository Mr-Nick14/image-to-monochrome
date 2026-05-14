import pytest
from PIL import Image

from bw_converter.algorithms import convert_image


@pytest.fixture
def sample_image() -> Image.Image:
    return Image.new("RGB", (2, 1), color=(0, 0, 0))._new(
        Image.frombytes("RGB", (2, 1), bytes([30, 60, 90, 200, 100, 50])).im,
    )


def pixels(image: Image.Image) -> list[int]:
    return list(image.tobytes())


def test_average_algorithm(sample_image: Image.Image) -> None:
    result = convert_image(sample_image, "average")

    assert result.mode == "L"
    assert pixels(result) == [60, 116]


def test_luminosity_algorithm(sample_image: Image.Image) -> None:
    result = convert_image(sample_image, "luminosity")

    assert pixels(result) == [54, 124]


def test_threshold_algorithm(sample_image: Image.Image) -> None:
    result = convert_image(sample_image, "threshold", threshold_value=100)

    assert pixels(result) == [0, 255]


def test_threshold_rejects_invalid_value(sample_image: Image.Image) -> None:
    with pytest.raises(ValueError, match="Threshold"):
        convert_image(sample_image, "threshold", threshold_value=300)


def test_max_channel_algorithm(sample_image: Image.Image) -> None:
    result = convert_image(sample_image, "max_channel")

    assert pixels(result) == [90, 200]


def test_min_channel_algorithm(sample_image: Image.Image) -> None:
    result = convert_image(sample_image, "min_channel")

    assert pixels(result) == [30, 50]
