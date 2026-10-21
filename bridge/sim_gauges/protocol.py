"""Arduino line protocol helpers."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


def value_line(speed_kmh: float, rpm: float) -> bytes:
    return f"V {speed_kmh:.1f} {rpm:.0f}\n".encode("ascii")


def config_line(max_speed_kmh: float, max_rpm: float) -> bytes:
    return f"C {max_speed_kmh:.0f} {max_rpm:.0f}\n".encode("ascii")


def zero_line() -> bytes:
    return b"Z\n"


@dataclass(frozen=True)
class CabinInputs:
    engine: bool
    headlights: bool
    btn1: bool
    btn2: bool
    btn3: bool


def parse_input_line(line: str) -> Optional[CabinInputs]:
    """Parse Arduino 'I e h b1 b2 b3' reports."""
    line = line.strip()
    if not line or (line[0] != "I" and line[0] != "i"):
        return None
    parts = line[1:].split()
    if len(parts) != 5:
        return None
    try:
        vals = [int(p) for p in parts]
    except ValueError:
        return None
    if any(v not in (0, 1) for v in vals):
        return None
    return CabinInputs(
        engine=bool(vals[0]),
        headlights=bool(vals[1]),
        btn1=bool(vals[2]),
        btn2=bool(vals[3]),
        btn3=bool(vals[4]),
    )
