"""High-level directory conversion workflow."""

from dataclasses import dataclass, field
from pathlib import Path

from bw_converter.algorithms import AlgorithmName, convert_image
from bw_converter.exceptions import BWConverterError
from bw_converter.io import (
    build_output_path,
    ensure_input_directory,
    ensure_output_directory,
    iter_image_candidates,
    open_image,
    save_image,
)


@dataclass(frozen=True)
class ConversionOptions:
    """User-selected conversion settings."""

    algorithm: AlgorithmName = "luminosity"
    threshold: int = 128
    recursive: bool = False
    overwrite: bool = False
    output_format: str = "png"


@dataclass
class ConversionResult:
    """Summary of a directory conversion run."""

    processed: list[Path] = field(default_factory=list)
    skipped: dict[Path, str] = field(default_factory=dict)

    @property
    def processed_count(self) -> int:
        """Return the number of successfully processed files."""
        return len(self.processed)

    @property
    def skipped_count(self) -> int:
        """Return the number of skipped files."""
        return len(self.skipped)


def convert_directory(
    input_dir: Path,
    output_dir: Path,
    options: ConversionOptions,
) -> ConversionResult:
    """Convert all images from an input directory into an output directory."""
    ensure_input_directory(input_dir)
    ensure_output_directory(output_dir)

    result = ConversionResult()
    for input_file in iter_image_candidates(input_dir, recursive=options.recursive):
        try:
            output_path = build_output_path(
                input_file=input_file,
                input_dir=input_dir,
                output_dir=output_dir,
                output_format=options.output_format,
            )
            image = open_image(input_file)
            converted = convert_image(
                image,
                algorithm=options.algorithm,
                threshold_value=options.threshold,
            )
            save_image(
                converted,
                path=output_path,
                output_format=options.output_format,
                overwrite=options.overwrite,
            )
        except BWConverterError as exc:
            result.skipped[input_file] = str(exc)
            continue
        result.processed.append(output_path)
    return result
