"""Patch pydicom.dataelem's DataElement_from_raw function."""
import contextlib
import dataclasses
import typing as t

import pydicom.config as pydicom_config
import pydicom.dataelem as pydicom_dataelem
from pydicom.datadict import dictionary_VR, get_entry
from pydicom.dataelem import DataElement, RawDataElement
from pydicom.dataset import Dataset
from pydicom.multival import MultiValue
from pydicom.valuerep import DSclass
from pydicom.values import convert_value

from .config import get_config

__all__ = ["raw_elem_tracker"]

# pylint: disable=protected-access
private_vr_for_tag = pydicom_dataelem._private_vr_for_tag
LUT_DESCRIPTOR_TAGS = pydicom_dataelem._LUT_DESCRIPTOR_TAGS
# pylint: enable=protected-access


def tag_specific_fixer(
    raw: RawDataElement,
    **_kwargs,
) -> t.Tuple[RawDataElement, dict]:
    """Fixes for known specific tags."""
    # make sure that SpecificCharacterSet has correct VR
    if raw.tag == 0x00080005 and raw.VR != "CS":
        raw = raw._replace(VR="CS")
    # avoid conversion errors on surplus SequenceDelimitationItem tags
    if raw.tag == 0xFFFEE0DD and raw.VR != "OB":
        raw = raw._replace(VR="OB")
    return raw, {}


def replace_None_with_known_VR(
    raw: RawDataElement, dataset: t.Optional[Dataset] = None, **kwargs
) -> t.Tuple[RawDataElement, dict]:
    """Replace VR=None with VR found in the public or private dictionaries."""
    if (raw.VR is not None) and not kwargs.get("force_infer"):
        return raw, {}
    VR = raw.VR
    try:
        VR = dictionary_VR(raw.tag)
    except KeyError:
        # just read the bytes, no way to know what they mean
        if raw.tag.is_private:
            # VRs for private tags see PS3.5, 6.2.2
            VR = private_vr_for_tag(dataset, raw.tag)
        # group length tag implied in versions < 3.0
        elif raw.tag.element == 0:
            VR = "UL"
        else:
            VR = "UN"
    if VR != raw.VR:
        raw = raw._replace(VR=VR)
    return raw, {}


def replace_UN_with_known_VR(
    raw: RawDataElement, dataset: t.Optional[Dataset] = None, **_kwargs
) -> t.Tuple[RawDataElement, dict]:
    """Replace VR='UN' with VR found in the public or private dictionaries."""
    if raw.VR != "UN":
        return raw, {}
    VR = raw.VR
    if raw.tag.is_private:
        VR = private_vr_for_tag(dataset, raw.tag)
    elif raw.value is None or len(raw.value) < 0xFFFF:
        try:
            VR = dictionary_VR(raw.tag)
        except KeyError:
            pass
    if VR != raw.VR:
        raw = raw._replace(VR=VR)
    return raw, {}


# TBD wouldn't an allow-list be simpler/shorter?
# http://dicom.nema.org/dicom/2013/output/chtml/part05/sect_6.2.html
backslash_compatible_VRs = (
    "AT,DS,FD,FL,IS,LT,OB,OB/OW,OB or OW,OF,OW,OW/OB,OW or OB,SL,SQ,SS,ST,UL,UN,US,UT"
).split(",")


def replace_backslash_in_VM1_str(
    raw: RawDataElement, **_kwargs
) -> t.Tuple[RawDataElement, dict]:
    r"""Replace invalid \ characters with _ in string VR values of VM=1."""
    try:
        VR, VM, *_ = get_entry(raw.tag)
    except KeyError:
        return raw, {}
    if VM == "1" and VR == raw.VR and VR not in backslash_compatible_VRs:
        value = raw.value
        if value and b"\\" in value:
            raw = raw._replace(value=value.replace(b"\\", b"_"))
    return raw, {}


# TBD truncate vs round?
def truncate_decimals_in_IS_VR(
    raw: RawDataElement, **_kwargs
) -> t.Tuple[RawDataElement, dict]:
    """Truncate unexpected decimals within Integer String VR values."""
    if raw.VR != "IS" or raw.value is None:
        return raw, {}
    if not any(c in raw.value for c in b".eE"):  # DS handles decimals/exp style
        return raw, {}
    value = convert_value("DS", raw)
    # TODO consider logging vs warnings, apply as needed
    if isinstance(value, (MultiValue, list, tuple)):
        value = "\\".join((str(int(v)) for v in value))
    else:
        assert isinstance(value, DSclass)
        value = str(int(value))
    return raw._replace(value=value.encode(encoding="ascii")), {}


def convert_exception_fixer(
    raw: RawDataElement,
    encoding: t.Optional[t.Union[str, t.List[str]]] = None,
    dataset: t.Optional[Dataset] = None,
    **_kwargs,
) -> t.Tuple[RawDataElement, dict]:
    """FW File convert_value handler.

    Will perform the following:
      - try loading elements with user-specified fallback VRs on failure
      - when all else fails, use VR=OB to just load the value as bytes
    """
    config = get_config()
    VR = t.cast(str, raw.VR)
    value = None
    try:
        value = convert_value(VR, raw, encoding)
    except NotImplementedError:
        # Try one more time to infer VR.  We only get here if the VR is
        # explicitely set to something that we can't convert, i.e a VR that
        # doesn't exist, so we need to force inference, since VR is not None
        # and is not UN.
        raw, _ = replace_None_with_known_VR(raw, dataset=dataset, force_infer=True)
        return convert_exception_fixer(raw, encoding, dataset)
    except ValueError:
        VRs = config.fix_VR_mismatch_with_VRs if config.fix_VR_mismatch else []
        if VR in VRs:
            VRs.remove(VR)
        for VR in VRs:
            try:
                value = convert_value(VR, raw, encoding)
            except ValueError:
                continue
            return convert_exception_fixer(raw._replace(VR=VR), encoding, dataset)
        return convert_exception_fixer(raw._replace(VR="OB"), encoding, dataset)
    except Exception:  # pylint: disable=broad-except
        return convert_exception_fixer(raw._replace(VR="OB"), encoding, dataset)
    return raw, {"value": value}


def LUT_descriptor_fixer(
    raw: RawDataElement, **kwargs
) -> t.Tuple[RawDataElement, dict]:
    """Fix LUT Descriptor tags."""
    # Value has already been converted, so value is a native python type,
    # not bytes
    value = kwargs.get("value", None)
    if raw.tag in LUT_DESCRIPTOR_TAGS and value:
        try:
            if value[0] < 0:
                value[0] += 65536  # type: ignore
        except TypeError:  # pragma: no cover
            pass
    return raw, {"value": value}


def DataElement_from_raw(  # pylint: disable=too-many-branches
    raw: RawDataElement,
    encoding: t.Optional[t.Union[str, t.List[str]]] = None,
    dataset: t.Optional[Dataset] = None,
) -> DataElement:
    """Override pydicom's DataElement_from_raw.

    This implementation separates the existing (as of pydicom 2.2.x)
    DataElement_from_raw into unit functions which are called in order.

    All these functions are accessible and configurable as user functions.
    FW File provides sensible defaults for these functions.
    """
    config = get_config()
    # Hardcode tracker first since user still needs to opt in
    tracker = pydicom_config.data_element_callback_kwargs.get("tracker")
    if tracker:
        raw = tracker.track(raw)
    fixer_kwargs: t.Dict[str, t.Any] = {}
    for fn in config.raw_elem_fixers:
        fn = t.cast(t.Callable, fn)
        raw, out_kwargs = fn(
            raw,
            encoding=encoding,
            dataset=dataset,
            **fixer_kwargs,
            **pydicom_config.data_element_callback_kwargs,
        )
        fixer_kwargs.update(out_kwargs)
    VR = t.cast(str, raw.VR)
    if fixer_kwargs.get("value", None):
        # Allow user to set converted value in fixers.
        value = fixer_kwargs.get("value")
    else:
        # Otherwise assume fixers have already ensured that convert_values
        # will not raise.
        value = convert_value(VR, raw, encoding)
    if tracker:
        tracker.update(raw)
    return DataElement(
        raw.tag,
        VR,
        value,
        raw.value_tell,
        raw.length == 0xFFFFFFFF,
        already_converted=True,
    )


@dataclasses.dataclass
class ReplaceEvent:
    """Dataclass to hold tracking event information."""

    field: str
    old: t.Optional[str]
    new: str

    def __repr__(self):
        """Return representation of tracking event."""
        return f"Replace {self.field}: {self.old} -> {self.new}"


class TrackedRawDataElement(RawDataElement):
    """RawDataElement subclass adding change tracking to _replace events."""

    id_: int
    original: RawDataElement
    events: t.List[ReplaceEvent]

    def __new__(cls, *args, id_=None, **kwargs) -> "TrackedRawDataElement":
        """Return a new TrackedRawDataElement instance."""
        tracked = super().__new__(cls, *args, **kwargs)
        tracked.id_ = id_
        tracked.original = RawDataElement(*args, **kwargs)
        tracked.events = []
        return tracked

    # pylint: disable=arguments-differ
    def _replace(self, **kwargs) -> "TrackedRawDataElement":
        """Extend namedtuple _replace with change event tracking."""
        for key, val in kwargs.items():
            old = getattr(self, key)
            event = ReplaceEvent(field=key, old=old, new=val)
            self.events.append(event)
        raw = super()._replace(**kwargs)  # calls new
        # NOTE updating the extra namedtuple attrs
        raw.original = self.original
        raw.events = self.events
        raw.id_ = self.id_
        return raw

    def export(self) -> dict:
        """Return the original dataelem, the events and the final version as a dict."""
        return {
            "original": self.original,
            "events": self.events,
            "final": self,
        }


def filter_none_vr_replacement(event: ReplaceEvent) -> bool:
    """Return True except for VR=None replacement events."""
    return not (event.field == "VR" and event.old is None)


class Tracker:
    """Tracker for RawDataElement change events within a dataset."""

    def __init__(self):
        """Initializes the tracker instance."""
        self.data_element_dict: t.Dict[int, TrackedRawDataElement] = {}

    @property
    def data_elements(self) -> t.List[TrackedRawDataElement]:
        """Expose data_elements as a list for backwards compat."""
        return list(self.data_element_dict.values())

    # NOTE: We need to us hash, and not ID to store the unique id.  hash looks
    # at the values of the object, whereas id looks at the location in memory.
    # id is guarenteed to be unique while objects overlap in lifetime, but due
    # to this implementation, RawDataElements won't be overlapping in life
    # time, and due to RawDataElement being a namedtuple with a very definite
    # size, they are often stored at the same location in memory.  So you can
    # end up with id returning the same value for two different
    # RawDataElements.

    def track(self, raw: RawDataElement) -> TrackedRawDataElement:
        """Return a TrackedRawDataElement from a RawDataElement."""
        # Store a unique id for each Tracked element, and use it to update the
        # _data_element_dict on Tracker
        # This needs to be `hash`, not `id`, see note above
        dict_key = hash(raw)
        # Can't actually think of a use case here.  We'd have to be calling
        # `track` on the same RawDataElement again, which would have already
        # been decoded.
        if dict_key in self.data_element_dict:
            return self.data_element_dict[dict_key]  # pragma: no cover
        tracked_elem = TrackedRawDataElement(*raw, id_=dict_key)
        self.data_element_dict[dict_key] = tracked_elem
        return tracked_elem

    def update(self, tr_raw: TrackedRawDataElement) -> None:
        """Update a TrackedRawDataElement."""
        self.data_element_dict[tr_raw.id_] = tr_raw

    def trim(self, event_filter: t.Callable = None) -> None:
        """Filter tracked events and remove data elements without any changes."""
        if not event_filter:
            event_filter = filter_none_vr_replacement
        for key in list(self.data_element_dict):
            de = self.data_element_dict[key]
            de.events = [evt for evt in de.events if event_filter(evt)]
            if not de.events:
                self.data_element_dict.pop(key)

    def __repr__(self):
        """Return representation of the tracker instance."""
        strings = []
        for raw in self.data_elements:
            trace = raw.export()
            events = "None"
            if trace["events"]:
                events = "\n" + "\n".join([f"\t{e}" for e in trace["events"]])
            strings.append(
                f"- original: {trace['original']}\n"
                f"  events: {events}\n"
                f"  final: {trace['final']}\n"
            )
        return "\n".join(strings)


@contextlib.contextmanager
def raw_elem_tracker(tracker: Tracker = None) -> t.Iterator[None]:
    """Context manager for tracking changes made to RawDataElements."""
    orig_tracker = pydicom_config.data_element_callback_kwargs.get("tracker")
    pydicom_config.data_element_callback_kwargs["tracker"] = tracker
    try:
        yield
    finally:
        pydicom_config.data_element_callback_kwargs["tracker"] = orig_tracker
