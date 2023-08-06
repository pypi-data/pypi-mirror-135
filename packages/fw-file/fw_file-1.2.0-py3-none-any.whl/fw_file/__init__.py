"""fw_file package metadata."""
try:
    from importlib.metadata import version
except ImportError:  # pragma: no cover
    from importlib_metadata import version  # type: ignore

__version__ = version(__name__)
