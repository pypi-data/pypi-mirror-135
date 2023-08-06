"""dicom module."""
from pydicom import dataelem, dataset, filereader, filewriter

from .config import get_config
from .dcmdict import load_dcmdict, load_private_dictionaries
from .dicom import DICOM, TagType
from .fixer import DataElement_from_raw, raw_elem_tracker
from .series import DICOMCollection, DICOMSeries, build_dicom_tree
from .utils import generate_uid

__all__ = [
    "DICOM",
    "DICOMCollection",
    "DICOMSeries",
    "TagType",
    "build_dicom_tree",
    "generate_uid",
    "get_config",
    "load_dcmdict",
    "raw_elem_tracker",
]

# extend pydicom private dict (with shipped extras and DCMDICTPATH if set)
load_private_dictionaries()

# Save a reference to the original DataElement_from_raw function just in case
orig_DataElement_from_raw = dataset.DataElement_from_raw

# Patch every DataElement_from_raw reference imported within pydicom
# NOTE grep -rnE "import.*DataElement_from_raw" <path/to/pydicom/git/dir>
for module in [dataelem, dataset, filereader, filewriter]:
    setattr(module, "DataElement_from_raw", DataElement_from_raw)
