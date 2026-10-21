from __future__ import annotations

from dataclasses import dataclass
from typing import Iterator, Optional, Protocol


@dataclass(frozen=True)
class Telemetry:
    speed_kmh: float
    rpm: float
    max_rpm: Optional[float] = None
    connected: bool = True


class TelemetrySource(Protocol):
    name: str

    def frames(self) -> Iterator[Telemetry]:
        """Yield telemetry forever (or until stopped). May sleep between frames."""
        ...
