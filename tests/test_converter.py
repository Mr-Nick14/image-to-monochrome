from pathlib import Path
from unittest.mock import patch

from PIL import Image

from bw_converter.converter import ConversionOptions, convert_directory
from bw_converter.exceptions import ImageReadError


def test_convert_directory_processes_images_and_skips_bad_files(tmp_path: Path) -> None:
    input_dir = tmp_path / "input"
    output_dir = tmp_path / "output"
    input_dir.mkdir()
    Image.new("RGB", (2, 2), color=(10, 20, 30)).save(input_dir / "ok.png")
    (input_dir / "bad.txt").write_text("not an image", encoding="utf-8")

    result = convert_directory(input_dir, output_dir, ConversionOptions())

    assert result.processed_count == 1
    assert result.skipped_count == 1
    assert (output_dir / "ok.png").exists()


def test_convert_directory_supports_recursive_mode(tmp_path: Path) -> None:
    input_dir = tmp_path / "input"
    nested = input_dir / "nested"
    output_dir = tmp_path / "output"
    nested.mkdir(parents=True)
    Image.new("RGB", (1, 1), color=(255, 255, 255)).save(nested / "ok.jpg")

    options = ConversionOptions(recursive=True, output_format="png")
    result = convert_directory(input_dir, output_dir, options)

    assert result.processed == [output_dir / "nested" / "ok.png"]
    assert (output_dir / "nested" / "ok.png").exists()


def test_convert_directory_records_read_errors(tmp_path: Path) -> None:
    input_dir = tmp_path / "input"
    output_dir = tmp_path / "output"
    input_dir.mkdir()
    image_path = input_dir / "ok.png"
    Image.new("RGB", (1, 1)).save(image_path)

    with patch(
        "bw_converter.converter.open_image",
        side_effect=ImageReadError("cannot read"),
    ):
        result = convert_directory(input_dir, output_dir, ConversionOptions())

    assert result.processed_count == 0
    assert result.skipped == {image_path: "cannot read"}
