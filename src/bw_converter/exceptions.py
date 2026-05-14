"""Project-specific exceptions for image conversion errors."""


class BWConverterError(Exception):
    """Base exception for all expected converter errors."""


class InputDirectoryError(BWConverterError):
    """Raised when an input directory cannot be used."""


class OutputDirectoryError(BWConverterError):
    """Raised when an output directory cannot be created or written to."""


class ImageReadError(BWConverterError):
    """Raised when a file cannot be opened as an image."""


class UnsupportedImageFormatError(BWConverterError):
    """Raised when an image format is not supported by the converter."""


class ImageWriteError(BWConverterError):
    """Raised when an output image cannot be saved."""
