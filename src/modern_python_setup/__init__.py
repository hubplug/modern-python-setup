"""The modern Python setup project."""

try:
    # if python version >= 3.8
    from importlib.metadata import version, PackageNotFoundError  # type: ignore
except ImportError:  # pragma: no cover
    # if python version < 3.8
    from importlib_metadata import version, PackageNotFoundError  # type: ignore


try:
    # if package installed
    __version__ = version(__name__)
except PackageNotFoundError:  # pragma: no cover
    # if package not installed
    __version__ = "unknown"
