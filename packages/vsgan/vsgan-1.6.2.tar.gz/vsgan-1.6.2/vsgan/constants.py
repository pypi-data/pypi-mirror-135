from __future__ import annotations

from typing import OrderedDict

import numpy as np
import vapoursynth as vs
from torch import Tensor

VS_API = vs.__api_version__.api_major
IS_VS_API_4 = VS_API == 4

MAX_DTYPE_VALUES = {
    np.dtype("int8"): 127,
    np.dtype("uint8"): 255,
    np.dtype("int16"): 32767,
    np.dtype("uint16"): 65535,
    np.dtype("int32"): 2147483647,
    np.dtype("uint32"): 4294967295,
    np.dtype("int64"): 9223372036854775807,
    np.dtype("uint64"): 18446744073709551615,
    np.dtype("float32"): 1.0,
    np.dtype("float64"): 1.0,
}
STATE_T = OrderedDict[str, Tensor]
