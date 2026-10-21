"""Assetto Corsa physics shared memory (Windows).

Game must be running. Map name defaults to Local\\acpmf_physics.
"""

from __future__ import annotations

import struct
import sys
import time
from typing import Iterator, Optional

from .base import Telemetry

# SPageFilePhysics (partial):
# int packetId; float gas; float brake; float fuel; int gear; int rpms;
# float steerAngle; float speedKmh;
_OFF_RPMS = 20
_OFF_SPEED_KMH = 28
_PHYSICS_MIN = 32


class AssettoSource:
    name = "assetto"

    def __init__(self, physics_map: str = r"Local\acpmf_physics") -> None:
        self.physics_map = physics_map

    def _open_map(self):
        if sys.platform != "win32":
            raise RuntimeError(
                "Assetto Corsa shared memory only works on Windows "
                "(run the bridge on the same PC as the game)."
            )
        import mmap

        # size must be >= physics struct; AC allocates a large page
        return mmap.mmap(-1, 4096, tagname=self.physics_map, access=mmap.ACCESS_READ)

    def frames(self) -> Iterator[Telemetry]:
        mm: Optional[object] = None
        last_packet = -1
        while True:
            try:
                if mm is None:
                    mm = self._open_map()
                data = mm[:_PHYSICS_MIN]
                packet_id = struct.unpack_from("<i", data, 0)[0]
                if packet_id == last_packet:
                    time.sleep(0.01)
                    continue
                last_packet = packet_id
                rpm = float(struct.unpack_from("<i", data, _OFF_RPMS)[0])
                speed = float(struct.unpack_from("<f", data, _OFF_SPEED_KMH)[0])
                yield Telemetry(speed_kmh=max(0.0, speed), rpm=max(0.0, rpm))
            except (FileNotFoundError, OSError, ValueError, PermissionError):
                if mm is not None:
                    try:
                        mm.close()  # type: ignore[attr-defined]
                    except Exception:
                        pass
                    mm = None
                yield Telemetry(0.0, 0.0, connected=False)
                time.sleep(0.5)
