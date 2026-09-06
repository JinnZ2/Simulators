# SPDX-License-Identifier: CC0-1.0
"""
Trace parsing and the hardware probe.

Two halves of the rig split by what can be checked here.

PARSE (checkable now, on constructed strings): turn the two instruments'
logs into `Sample` lists. Card telemetry from
`nvidia-smi --query-gpu=power.draw --format=csv,noheader -lms 100` is one
power value per line with NO timestamp -- the timestamps come from the loop
interval (`-lms 100` == 0.1 s == 10 Hz), so the interval is a parameter of
the parse, not read from the log. Wall-meter exports vary; the generic form
is a two-column `t,watts` CSV (seconds, watts), which most smart-plug
exports can be massaged into.

CAPTURE (NOT runnable here): actually taking a measurement needs a GPU, a
wall meter, and `nvidia-smi` on PATH. `probe_hardware()` reports what is
present -- and in this environment nothing is (no accelerator, no meter, no
`nvidia-smi`). No capture code that shells out to a meter is written,
because it could not be exercised and an untested capture path is worse than
an honest gap. The parse half is ready; the number is the gap (RIG_STATUS.md).

Stdlib only. Parses under Python 3.9. ASCII only. CC0.
"""

from __future__ import annotations

import shutil
from dataclasses import dataclass
from typing import List, Optional

from phase_energy import Sample


class TraceParseError(Exception):
    pass


def parse_nvidia_smi(text: str, interval_s: float = 0.1) -> List[Sample]:
    """Parse the output of
        nvidia-smi --query-gpu=power.draw --format=csv,noheader -lms 100
    which is one line per sample, each like `42.13 W` (or `42.13`), with no
    timestamp. Timestamps are synthesized from `interval_s` -- the `-lms`
    loop period (100 ms -> 0.1 s -> 10 Hz). If you logged at a different
    `-lms`, pass the matching interval; passing the wrong one is a
    sample-rate error the rig's UNDERSAMPLED flag will not catch, because it
    changes the x-axis the flag is computed on. `interval_s` is therefore
    part of the record, not a default to forget.
    """
    if interval_s <= 0:
        raise TraceParseError("interval_s must be positive; got %r"
                              % interval_s)
    out: List[Sample] = []
    i = 0
    for raw in text.splitlines():
        line = raw.strip()
        if not line:
            continue
        # strip a trailing unit token if present ("42.13 W" or "42.13")
        tok = line.split()[0].rstrip(",")
        try:
            watts = float(tok)
        except ValueError:
            raise TraceParseError("could not read a power value from %r"
                                  % raw)
        out.append(Sample(i * interval_s, watts))
        i += 1
    return out


def parse_wall_csv(text: str, t_col: int = 0, w_col: int = 1,
                   skip_header: bool = True) -> List[Sample]:
    """Parse a generic wall-meter export: a CSV with a time-in-seconds
    column and a watts column. Columns are named so a differently ordered
    export is a parameter, not a silent misread. The time column is REAL
    (the meter stamps it), unlike the card log."""
    out: List[Sample] = []
    lines = text.splitlines()
    started = False
    for raw in lines:
        line = raw.strip()
        if not line:
            continue
        parts = [p.strip() for p in line.split(",")]
        if skip_header and not started:
            started = True
            # a header row has a non-numeric time cell; skip exactly one
            try:
                float(parts[t_col])
            except (ValueError, IndexError):
                continue
        started = True
        if max(t_col, w_col) >= len(parts):
            raise TraceParseError("row has too few columns: %r" % raw)
        try:
            t = float(parts[t_col])
            w = float(parts[w_col])
        except ValueError:
            raise TraceParseError("non-numeric t/watts in row: %r" % raw)
        out.append(Sample(t, w))
    return out


# --------------------------------------------------------------------------
# The hardware probe. Reports what is present; takes no measurement.
# --------------------------------------------------------------------------

@dataclass
class HardwareProbe:
    nvidia_smi_path: Optional[str]
    has_gpu_telemetry: bool
    wall_meter: str            # always "manual" -- no meter is auto-detected
    capture_runnable: bool
    note: str


def probe_hardware() -> HardwareProbe:
    """Report the instruments available to the rig. Does NOT run nvidia-smi
    (running it here would prove nothing and there is no card behind it); it
    only checks PATH. A wall meter is never auto-detected -- it is an
    external AC device with its own logger -- so it is always 'manual', and
    `capture_runnable` is card-side availability only."""
    smi = shutil.which("nvidia-smi")
    has_card = smi is not None
    return HardwareProbe(
        nvidia_smi_path=smi,
        has_gpu_telemetry=has_card,
        wall_meter="manual",
        capture_runnable=has_card,
        note=("card telemetry needs nvidia-smi (or a vendor equivalent) on "
              "PATH and a real accelerator behind it; the wall channel needs "
              "an external AC meter with a logged export. Neither is "
              "auto-detected as present here."),
    )


if __name__ == "__main__":
    import sys
    p = probe_hardware()
    sys.stderr.write(
        "trace_parse.py is a parser + probe, not a check. Its checks live in "
        "agent-lifecycle-energy/selftest_ale.py.\n"
        "hardware probe: nvidia-smi=%r has_gpu_telemetry=%s wall_meter=%s "
        "capture_runnable=%s\n"
        % (p.nvidia_smi_path, p.has_gpu_telemetry, p.wall_meter,
           p.capture_runnable))
    sys.exit(2)
