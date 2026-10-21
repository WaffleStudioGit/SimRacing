"""Sweep needles so you can wire/tune without a game running."""

from __future__ import annotations

import math
import time
from typing import Iterator

from .base import Telemetry


class DemoSource:
    name = "demo"

    def __init__(self, max_speed_kmh: float = 300.0, max_rpm: float = 9000.0) -> None:
        self.max_speed_kmh = max_speed_kmh
        self.max_rpm = max_rpm

    def frames(self) -> Iterator[Telemetry]:
        t0 = time.monotonic()
        while True:
            t = time.monotonic() - t0
            # Slow sine sweeps, phase-offset so needles aren't locked together
            speed = (math.sin(t * 0.4) * 0.5 + 0.5) * self.max_speed_kmh
            rpm = (math.sin(t * 0.7 + 1.2) * 0.5 + 0.5) * self.max_rpm
            yield Telemetry(speed_kmh=speed, rpm=rpm, max_rpm=self.max_rpm)
            time.sleep(1 / 30)
