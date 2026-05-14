"""Command-line interface for bw-converter."""

from pathlib import Path

import click

from bw_converter.algorithms import ALGORITHMS, AlgorithmName
from bw_converter.converter import ConversionOptions, convert_directory
from bw_converter.exceptions import BWConverterError


@click.command()
@click.argument("input_dir", type=click.Path(path_type=Path))
@click.argument("output_dir", type=click.Path(path_type=Path))
@click.option(
    "--algorithm",
    type=click.Choice(ALGORITHMS),
    default="luminosity",
    show_default=True,
    help="Black-and-white conversion algorithm.",
)
@click.option(
    "--threshold",
    type=click.IntRange(0, 255),
    default=128,
    show_default=True,
    help="Threshold value for the threshold algorithm.",
)
@click.option("--recursive", is_flag=True, help="Process nested folders recursively.")
@click.option("--overwrite", is_flag=True, help="Overwrite existing output files.")
@click.option(
    "--format",
    "output_format",
    type=click.Choice(["png", "jpg", "jpeg", "bmp", "tiff", "webp"]),
    default="png",
    show_default=True,
    help="Output image format.",
)
@click.option("--verbose", is_flag=True, help="Print skipped files and output paths.")
def main(
    input_dir: Path,
    output_dir: Path,
    algorithm: AlgorithmName,
    threshold: int,
    recursive: bool,
    overwrite: bool,
    output_format: str,
    verbose: bool,
) -> None:
    """Convert images from INPUT_DIR and save results to OUTPUT_DIR."""
    options = ConversionOptions(
        algorithm=algorithm,
        threshold=threshold,
        recursive=recursive,
        overwrite=overwrite,
        output_format=output_format,
    )

    try:
        result = convert_directory(input_dir, output_dir, options)
    except BWConverterError as exc:
        raise click.ClickException(str(exc)) from exc

    click.echo(f"Processed: {result.processed_count}; skipped: {result.skipped_count}")
    if verbose:
        for path in result.processed:
            click.echo(f"saved: {path}")
        for path, reason in result.skipped.items():
            click.echo(f"skipped: {path} ({reason})")


if __name__ == "__main__":
    main()
