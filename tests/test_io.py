from pathlib import Path
from unittest.mock import patch

import pytest
from PIL import Image

from bw_converter.exceptions import (
    ImageReadError,
    ImageWriteError,
    InputDirectoryError,
    OutputDirectoryError,
    UnsupportedImageFormatError,
)
from bw_converter.io import (
    build_output_path,
    ensure_input_directory,
    ensure_output_directory,
    iter_image_candidates,
    open_image,
    save_image,
)


@pytest.fixture
def image_file(tmp_path: Path) -> Path:
    path = tmp_path / "input.png"
    Image.new("RGB", (1, 1), color=(255, 0, 0)).save(path)
    return path


def test_ensure_input_directory_rejects_missing_path(tmp_path: Path) -> None:
    with pytest.raises(InputDirectoryError):
        ensure_input_directory(tmp_path / "missing")


def test_ensure_input_directory_rejects_file(tmp_path: Path) -> None:
    input_file = tmp_path / "input.txt"
    input_file.write_text("not a directory", encoding="utf-8")

    with pytest.raises(InputDirectoryError):
        ensure_input_directory(input_file)


def test_ensure_output_directory_creates_path(tmp_path: Path) -> None:
    output_dir = tmp_path / "nested" / "out"

    ensure_output_directory(output_dir)

    assert output_dir.is_dir()


def test_ensure_output_directory_wraps_os_error(tmp_path: Path) -> None:
    with (
        patch.object(Path, "mkdir", side_effect=PermissionError("denied")),
        pytest.raises(OutputDirectoryError),
    ):
        ensure_output_directory(tmp_path / "out")


def test_ensure_output_directory_rejects_non_directory(tmp_path: Path) -> None:
    with (
        patch.object(Path, "mkdir"),
        patch.object(Path, "is_dir", return_value=False),
        pytest.raises(OutputDirectoryError),
    ):
        ensure_output_directory(tmp_path / "out")


def test_iter_image_candidates_can_be_recursive(tmp_path: Path) -> None:
    nested = tmp_path / "nested"
    nested.mkdir()
    (tmp_path / "a.txt").write_text("not image", encoding="utf-8")
    (nested / "b.png").write_text("fake image", encoding="utf-8")

    assert len(iter_image_candidates(tmp_path, recursive=False)) == 1
    assert len(iter_image_candidates(tmp_path, recursive=True)) == 2


def test_open_image_loads_supported_image(image_file: Path) -> None:
    image = open_image(image_file)

    assert image.size == (1, 1)


def test_open_image_rejects_non_image(tmp_path: Path) -> None:
    path = tmp_path / "file.txt"
    path.write_text("hello", encoding="utf-8")

    with pytest.raises(ImageReadError):
        open_image(path)


def test_open_image_rejects_unsupported_format(tmp_path: Path) -> None:
    path = tmp_path / "palette.gif"
    Image.new("P", (1, 1)).save(path)

    with pytest.raises(UnsupportedImageFormatError):
        open_image(path)


def test_build_output_path_preserves_relative_folder(tmp_path: Path) -> None:
    source = tmp_path / "src"
    nested = source / "nested"
    nested.mkdir(parents=True)
    input_file = nested / "photo.jpg"

    result = build_output_path(input_file, source, tmp_path / "out", "png")

    assert result == tmp_path / "out" / "nested" / "photo.png"


def test_build_output_path_rejects_format(tmp_path: Path) -> None:
    with pytest.raises(UnsupportedImageFormatError):
        build_output_path(tmp_path / "a.png", tmp_path, tmp_path / "out", "gif")


def test_save_image_rejects_existing_file_without_overwrite(tmp_path: Path) -> None:
    image = Image.new("L", (1, 1))
    output = tmp_path / "out.png"
    output.write_bytes(b"existing")

    with pytest.raises(ImageWriteError):
        save_image(image, output, "png", overwrite=False)


def test_save_image_wraps_write_error(tmp_path: Path) -> None:
    image = Image.new("L", (1, 1))
    output = tmp_path / "out.png"

    with (
        patch.object(Image.Image, "save", side_effect=PermissionError("denied")),
        pytest.raises(ImageWriteError),
    ):
        save_image(image, output, "png", overwrite=True)
