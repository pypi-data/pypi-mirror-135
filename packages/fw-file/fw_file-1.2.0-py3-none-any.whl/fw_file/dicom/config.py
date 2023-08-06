"""DICOM config module."""
import functools
import importlib
import re
import typing as t

from pydantic import BaseSettings, validator

from .. import __version__

__all__ = [
    "get_config",
    "IMPLEMENTATION_CLASS_UID",
    "IMPLEMENTATION_VERSION_NAME",
    "UID_ROOT",
    "UID_PREFIX",
]


# Flywheel DICOM UID Management Plan:
# https://docs.google.com/document/d/1HcMcWBrDsYIFOkMgGL8W7Hzt7I2tl4UbeC40R5HH99A
# UID root for ANSI registered numeric organization name 114570 (Flywheel)
UID_ROOT = "2.16.840.1.114570"
# UID prefix and version of product fw-file
UID_PREFIX = f"{UID_ROOT}.4"
VERSION = re.split(r"[^\d]+", __version__)

# fw-file (0002,0012) ImplementationClassUID
IMPLEMENTATION_CLASS_UID: str = f"{UID_PREFIX}.1.{'.'.join(VERSION)}"
# fw-file (0002,0013) ImplementationVersionName
IMPLEMENTATION_VERSION_NAME: str = f"FWFILE_{'_'.join(VERSION)}"


@functools.lru_cache()
def import_func(func_path: str) -> t.Callable:
    """Return function imported from a fully qualified name."""
    try:
        module_name, func_name = func_path.rsplit(".", maxsplit=1)
        module = importlib.import_module(module_name)
        func = getattr(module, func_name)
    except (ValueError, ImportError, AttributeError) as exc:
        msg = f"Cannot import fixer {func_path!r} ({exc})"
        raise ValueError(msg) from exc
    assert callable(func), f"{func_path} is not callable"
    return func


class DICOMConfig(BaseSettings):
    """DICOM config."""

    class Config:
        """Enable envvars with prefix `FW_DCM_`."""

        # Needed to call raw_elem_callbacks validator on update
        validate_assignment = True
        underscore_attrs_are_private = True
        env_prefix = "FW_DCM_"

    # data element loader / fixer config
    fix_VR_mismatch: bool = False
    fix_VR_mismatch_with_VRs: t.List[str] = ["PN", "DS", "IS"]
    track: bool = False

    # List of raw data element fixer functions
    raw_elem_fixers: t.List[t.Union[str, t.Callable]] = [
        "fw_file.dicom.fixer.tag_specific_fixer",
        "fw_file.dicom.fixer.replace_None_with_known_VR",
        "fw_file.dicom.fixer.replace_UN_with_known_VR",
        "fw_file.dicom.fixer.replace_backslash_in_VM1_str",
        "fw_file.dicom.fixer.truncate_decimals_in_IS_VR",
        "fw_file.dicom.fixer.convert_exception_fixer",
        "fw_file.dicom.fixer.LUT_descriptor_fixer",
    ]

    @validator("raw_elem_fixers")
    @classmethod
    def checker(cls, v):
        """Resolve string or functions and import if necessary."""
        callbacks = []
        for val in v:
            fn = val
            if isinstance(val, str):
                fn = import_func(val)
            callbacks.append(fn)
        return callbacks

    # pylint: enable=no-self-argument,no-self-use

    def add_fixers(
        self,
        fixers: t.Union[t.List[t.Union[t.Callable, str]], t.Callable, str],
        index: t.Optional[int] = None,
    ) -> None:
        """Helper function to add one or more raw element fixers.

        Args:
            fixers (List, Callable, str): List or single function to add, can
                either be specified as the actual function or a string
                representing its import path.
            index (int): Optional index at which to add the fixer(s)
        """
        if not isinstance(fixers, list):
            fixers = [fixers]
        add = [import_func(fn) if isinstance(fn, str) else fn for fn in fixers]
        if index:
            self.raw_elem_fixers[index:index] = add
            return
        self.raw_elem_fixers.extend(add)
        return

    def remove_fixers(self, fixers: t.Union[t.List[str], str]) -> None:
        """Helper function to remove one or more raw_elem_fixers.

        Args:
            fixers (List, str): List or single string representing the name of
                the function to remove.  You don't need to specify the full
                import path, just the name of the function.
        """
        if not isinstance(fixers, list):
            fixers = [fixers]
        for to_remove in fixers:
            self.raw_elem_fixers = [
                fn
                for fn in self.raw_elem_fixers
                if fn.__name__ != to_remove  # type: ignore
            ]

    def list_fixers(self) -> t.List[str]:
        """Helper to list name and order of all enabled fixers."""
        return [fn.__name__ for fn in self.raw_elem_fixers]  # type: ignore

    # allow private tag access without specifying private creator like dcm["0019xx10"]
    # when enabled dataset/private dict will be used to figure out the private creator
    implicit_creator: bool = False

    # num of instances (with local paths) to keep loaded in memory in collections
    instance_cache_size = 10000


@functools.lru_cache(maxsize=None)
def get_config() -> DICOMConfig:
    """Return DICOMConfig object loaded from envvars (cached / singleton)."""
    return DICOMConfig()
