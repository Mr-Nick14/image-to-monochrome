from pathlib import Path

from click.testing import CliRunner
from PIL import Image

from bw_converter.cli import main


def test_cli_converts_image(tmp_path: Path) -> None:
    input_dir = tmp_path / "input"
    output_dir = tmp_path / "output"
    input_dir.mkdir()
    Image.new("RGB", (1, 1), color=(100, 100, 100)).save(input_dir / "a.png")

    result = CliRunner().invoke(
        main,
        [
            str(input_dir),
            str(output_dir),
            "--algorithm",
            "threshold",
            "--threshold",
            "120",
            "--overwrite",
            "--verbose",
        ],
    )

    assert result.exit_code == 0
    assert "Processed: 1; skipped: 0" in result.output
    assert (output_dir / "a.png").exists()


def test_cli_reports_missing_input_directory(tmp_path: Path) -> None:
    result = CliRunner().invoke(
        main, [str(tmp_path / "missing"), str(tmp_path / "out")]
    )

    assert result.exit_code != 0
    assert "Input directory does not exist" in result.output


def test_cli_validates_algorithm(tmp_path: Path) -> None:
    result = CliRunner().invoke(
        main,
        [str(tmp_path), str(tmp_path / "out"), "--algorithm", "wrong"],
    )

    assert result.exit_code != 0
    assert "Invalid value" in result.output
