"""Arduino line protocol helpers."""

from __future__ import annotations


def value_line(speed_kmh: float, rpm: float) -> bytes:
    return f"V {speed_kmh:.1f} {rpm:.0f}\n".encode("ascii")


def config_line(max_speed_kmh: float, max_rpm: float) -> bytes:
    return f"C {max_speed_kmh:.0f} {max_rpm:.0f}\n".encode("ascii")


def zero_line() -> bytes:
    return b"Z\n"
