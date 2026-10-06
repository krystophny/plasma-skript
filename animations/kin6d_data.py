"""Reader for kin6d animation exports (animations/data/kin6d/<slug>/).

kin6d (a Fortran plasma kinetic code by the course authors) is the scientific
source of the data-driven scenes; the scenes only visualize its exports.  Each
export directory holds raw little-endian arrays in Fortran (column-major)
order and ``provenance.json`` (schema kin6d-animation-export-v1) with the
kin6d commit, command, namelist, physical parameters, units and the decode
rule of quantized arrays.  This module applies exactly that rule.
"""

import json
import os

import numpy as np

_HERE = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(_HERE, "data", "kin6d")

_DTYPES = {"float32": "<f4", "uint8": "u1", "uint16": "<u2"}


class Export:
    """Arrays and declared parameters of one kin6d animation export."""

    def __init__(self, slug):
        self.path = os.path.join(DATA_DIR, slug)
        with open(os.path.join(self.path, "provenance.json"), encoding="utf-8") as f:
            self.provenance = json.load(f)
        if self.provenance.get("schema") != "kin6d-animation-export-v1":
            raise ValueError(f"{slug}: unknown export schema")
        self.parameters = {k: v["value"] for k, v in self.provenance["parameters"].items()}
        self._cache = {}

    def __getitem__(self, name):
        if name not in self._cache:
            self._cache[name] = self._read(name)
        return self._cache[name]

    def _read(self, name):
        entry = self.provenance["arrays"][name]
        raw = np.fromfile(os.path.join(self.path, entry["file"]), dtype=_DTYPES[entry["dtype"]])
        shape = tuple(entry["shape"])
        if raw.size != int(np.prod(shape)):
            raise ValueError(f"{name}: {raw.size} values for shape {shape}")
        values = raw.reshape(shape, order="F")
        decode = entry.get("decode")
        if decode is None:
            return values.astype(np.float64)
        # code 0: below lo; code >= 1: lo + (code - 1) (hi - lo)/(cmax - 1).
        cmax = np.iinfo(values.dtype).max
        lo, hi = decode["lo"], decode["hi"]
        decoded = lo + (values.astype(np.float64) - 1.0) * (hi - lo) / (cmax - 1)
        decoded[values == 0] = -np.inf
        return decoded
