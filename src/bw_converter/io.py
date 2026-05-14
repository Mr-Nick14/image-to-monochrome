"""Input and output helpers for image files."""

from pathlib import Path

from PIL import Image, UnidentifiedImageError

from bw_converter.exceptions import (
    ImageReadError,
    ImageWriteError,
    InputDirectoryError,
    OutputDirectoryError,
    UnsupportedImageFormatError,
)

SUPPORTED_INPUT_FORMATS = {"JPEG", "PNG", "BMP", "TIFF", "WEBP"}
SUPPORTED_OUTPUT_FORMATS = {"jpeg", "jpg", "png", "bmp", "tiff", "webp"}
IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".tif", ".tiff", ".webp"}


def ensure_input_directory(path: Path) -> None:
    """Validate that an input directory exists and can be read."""
    if not path.exists():
        msg = f"Input directory does not exist: {path}"
        raise InputDirectoryError(msg)
    if not path.is_dir():
        msg = f"Input path is not a directory: {path}"
        raise InputDirectoryError(msg)


def ensure_output_directory(path: Path) -> None:
    """Create an output directory if needed and check that it is writable."""
    try:
        path.mkdir(parents=True, exist_ok=True)
    except OSError as exc:
        msg = f"Cannot create output directory: {path}"
        raise OutputDirectoryError(msg) from exc

    if not path.is_dir():
        msg = f"Output path is not a directory: {path}"
        raise OutputDirectoryError(msg)


def iter_image_candidates(input_dir: Path, recursive: bool = False) -> list[Path]:
    """Return files that look like image candidates by extension."""
    pattern = "**/*" if recursive else "*"
    return sorted(path for path in input_dir.glob(pattern) if path.is_file())


def open_image(path: Path) -> Image.Image:
    """Open an image file and validate its format."""
    try:
        image = Image.open(path)
        image.load()
    except (OSError, UnidentifiedImageError) as exc:
        msg = f"Cannot read image: {path}"
        raise ImageReadError(msg) from exc

    if image.format not in SUPPORTED_INPUT_FORMATS:
        msg = f"Unsupported image format for {path}: {image.format}"
        raise UnsupportedImageFormatError(msg)
    return image


def build_output_path(
    input_file: Path,
    input_dir: Path,
    output_dir: Path,
    output_format: str,
) -> Path:
    """Build an output path preserving subdirectories for recursive mode."""
    normalized_format = output_format.lower()
    if normalized_format not in SUPPORTED_OUTPUT_FORMATS:
        msg = f"Unsupported output format: {output_format}"
        raise UnsupportedImageFormatError(msg)
    suffix = ".jpg" if normalized_format == "jpeg" else f".{normalized_format}"
    relative = input_file.relative_to(input_dir).with_suffix(suffix)
    return output_dir / relative


def save_image(
    image: Image.Image, path: Path, output_format: str, overwrite: bool
) -> None:
    """Save an image to disk, creating parent directories if needed."""
    if path.exists() and not overwrite:
        msg = f"Output file already exists: {path}"
        raise ImageWriteError(msg)
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        image.save(path, format=output_format.upper())
    except OSError as exc:
        msg = f"Cannot write image: {path}"
        raise ImageWriteError(msg) from exc
