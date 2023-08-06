# THIS FILE HAS BEEN GENERATED AUTOMATICALLY BY capnpy
# do not edit by hand
# generated on 2022-01-24 04:55
# cython: language_level=2

from capnpy cimport ptr as _ptr
from capnpy.struct_ cimport Struct as _Struct
from capnpy.struct_ cimport check_tag as _check_tag
from capnpy.struct_ import undefined as _undefined
from capnpy.enum import enum as _enum, fill_enum as _fill_enum
from capnpy.enum cimport BaseEnum as _BaseEnum
from capnpy.type import Types as _Types
from capnpy.segment.segment cimport Segment as _Segment
from capnpy.segment.segment cimport MultiSegment as _MultiSegment
from capnpy.segment.builder cimport SegmentBuilder as _SegmentBuilder
from capnpy.list cimport List as _List
from capnpy.list cimport PrimitiveItemType as _PrimitiveItemType
from capnpy.list cimport BoolItemType as _BoolItemType
from capnpy.list cimport TextItemType as _TextItemType
from capnpy.list cimport TextUnicodeItemType as _TextUnicodeItemType
from capnpy.list cimport StructItemType as _StructItemType
from capnpy.list cimport EnumItemType as _EnumItemType
from capnpy.list cimport VoidItemType as _VoidItemType
from capnpy.list cimport ListItemType as _ListItemType
from capnpy.anypointer import AnyPointer as _AnyPointer
from capnpy.util import text_bytes_repr as _text_bytes_repr
from capnpy.util import text_unicode_repr as _text_unicode_repr
from capnpy.util import data_repr as _data_repr
from capnpy.util import float32_repr as _float32_repr
from capnpy.util import float64_repr as _float64_repr
from capnpy.util import extend_module_maybe as _extend_module_maybe
from capnpy.util import check_version as _check_version
from capnpy.util import encode_maybe as _encode_maybe
from capnpy cimport _hash
from capnpy.list cimport void_list_item_type as _void_list_item_type
from capnpy.list cimport bool_list_item_type as _bool_list_item_type
from capnpy.list cimport int8_list_item_type as _int8_list_item_type
from capnpy.list cimport uint8_list_item_type as _uint8_list_item_type
from capnpy.list cimport int16_list_item_type as _int16_list_item_type
from capnpy.list cimport uint16_list_item_type as _uint16_list_item_type
from capnpy.list cimport int32_list_item_type as _int32_list_item_type
from capnpy.list cimport uint32_list_item_type as _uint32_list_item_type
from capnpy.list cimport int64_list_item_type as _int64_list_item_type
from capnpy.list cimport uint64_list_item_type as _uint64_list_item_type
from capnpy.list cimport float32_list_item_type as _float32_list_item_type
from capnpy.list cimport float64_list_item_type as _float64_list_item_type
from capnpy.list cimport data_list_item_type as _data_list_item_type
from capnpy.list cimport text_bytes_list_item_type as _text_bytes_list_item_type
from capnpy.list cimport text_unicode_list_item_type as _text_unicode_list_item_type
__capnpy_id__ = 0xedda8f1fc8b626fe
__capnpy_version__ = '0.9.0'
__capnproto_version__ = '0.7.0'
_check_version(__name__, __capnpy_version__)
from capnpy.schema import CodeGeneratorRequest as _CodeGeneratorRequest
from capnpy.annotate import Options as _Options
from capnpy.reflection import ReflectionData as _ReflectionData
class _medium_ReflectionData(_ReflectionData):
    request = _CodeGeneratorRequest.from_buffer(_Segment(b'\x00\x00\x00\x00\x00\x00\x04\x00\x11\x00\x00\x00\xb7\x00\x00\x00i\x01\x00\x00\x1f\x00\x00\x00\x04\x00\x00\x00\x01\x00\x00\x00%\x01\x00\x007\x00\x00\x00\x00\x00\x07\x00\x00\x00\x00\x00\x08\x00\x00\x00\x05\x00\x06\x00\xfe&\xb6\xc8\x1f\x8f\xda\xed%\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00A\x00\x00\x00Z\x01\x00\x00U\x00\x00\x00\x17\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x16.\x1b\x86\xbe5\xb0\x9f+\x00\x00\x00\x02\x00\x00\x00\xfe&\xb6\xc8\x1f\x8f\xda\xed\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00=\x00\x00\x00\x92\x01\x00\x00U\x00\x00\x00\x07\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00Q\x00\x00\x00\xaf\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00src/podping_hivewriter/schema/medium.capnp\x00\x00\x00\x00\x00\x00\x04\x00\x00\x00\x01\x00\x01\x00\x16.\x1b\x86\xbe5\xb0\x9f\x01\x00\x00\x00:\x00\x00\x00Medium\x00\x00src/podping_hivewriter/schema/medium.capnp:Medium\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x01\x00\x1c\x00\x00\x00\x01\x00\x02\x00\x00\x00\x00\x00\x00\x00\x00\x00M\x00\x00\x00B\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00E\x00\x00\x002\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x02\x00\x00\x00\x00\x00\x00\x00=\x00\x00\x002\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x03\x00\x00\x00\x00\x00\x00\x005\x00\x00\x00*\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x04\x00\x00\x00\x00\x00\x00\x00-\x00\x00\x00R\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x05\x00\x00\x00\x00\x00\x00\x00)\x00\x00\x00Z\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x06\x00\x00\x00\x00\x00\x00\x00%\x00\x00\x00*\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00podcast\x00music\x00\x00\x00video\x00\x00\x00film\x00\x00\x00\x00audiobook\x00\x00\x00\x00\x00\x00\x00newsletter\x00\x00\x00\x00\x00\x00blog\x00\x00\x00\x00\x08\x00\x00\x00\x01\x00\x02\x00\x16.\x1b\x86\xbe5\xb0\x9f\x00\x00\x00\x00\x00\x00\x00\x00\r\x00\x00\x00?\x00\x00\x00\xfe&\xb6\xc8\x1f\x8f\xda\xed\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x1c\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x04\x00\x00\x00\x01\x00\x02\x00\xfe&\xb6\xc8\x1f\x8f\xda\xed\x05\x00\x00\x00Z\x01\x00\x00\x19\x00\x00\x00\x07\x00\x00\x00src/podping_hivewriter/schema/medium.capnp\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x01\x00'), 8, 0, 4)
    default_options = _Options.from_buffer(_Segment(b'\x03\x00\x02\x00\x01\x00\x03\x00'), 0, 1, 0)
    pyx = True
_reflection_data = _medium_ReflectionData()

#### FORWARD DECLARATIONS ####

cdef class Medium(_BaseEnum):
    __capnpy_id__ = 11506756140341603862
    __members__ = ('podcast', 'music', 'video', 'film', 'audiobook', 'newsletter', 'blog',)
    @staticmethod
    cdef _new(long x, __prebuilt=(Medium(0), Medium(1), Medium(2), Medium(3), Medium(4), Medium(5), Medium(6),)):
        try:
            return __prebuilt[x]
        except IndexError:
            return Medium(x)
    @staticmethod
    def _new_hack(long x, __prebuilt=(Medium(0), Medium(1), Medium(2), Medium(3), Medium(4), Medium(5), Medium(6),)):
        try:
            return __prebuilt[x]
        except IndexError:
            return Medium(x)
_fill_enum(Medium)
_Medium_list_item_type = _EnumItemType(Medium)


#### DEFINITIONS ####


_extend_module_maybe(globals(), modname=__name__)