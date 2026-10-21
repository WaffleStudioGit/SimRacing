"""BeamNG.drive OutGauge (UDP).

In BeamNG: Options → Other → enable OutGauge, set IP + port.
Packet matches Live for Speed OutGauge (ID version = 96 bytes).
"""

from __future__ import annotations

import socket
import struct
from typing import Iterator

from .base import Telemetry

# time u32, car[4], flags u16, gear i8, plid u8,
# speed f32, rpm f32, turbo f32, engTemp f32, fuel f32,
# oilPressure f32, oilTemp f32, dashLights u32, showLights u32,
# throttle f32, brake f32, clutch f32, display1[16], display2[16], id i32
_OUTGAUGE_FMT = "<I4sHbb7f2I3f16s16si"
_OUTGAUGE_SIZE = struct.calcsize(_OUTGAUGE_FMT)  # 96
_OFF_SPEED = 12


class BeamNGSource:
    name = "beamng"

    def __init__(self, listen_ip: str = "0.0.0.0", listen_port: int = 4444) -> None:
        self.listen_ip = listen_ip
        self.listen_port = listen_port

    def frames(self) -> Iterator[Telemetry]:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((self.listen_ip, self.listen_port))
        sock.settimeout(1.0)
        try:
            while True:
                try:
                    data, _ = sock.recvfrom(256)
                except socket.timeout:
                    yield Telemetry(0.0, 0.0, connected=False)
                    continue
                if len(data) < 36:
                    continue
                # Prefer full ID packet; tolerate shorter without trailing id
                if len(data) >= _OUTGAUGE_SIZE:
                    unpacked = struct.unpack_from(_OUTGAUGE_FMT, data, 0)
                    # I, 4s, H, b, b, then speed, rpm → indices 5, 6
                    speed_ms = unpacked[5]
                    rpm = unpacked[6]
                else:
                    speed_ms, rpm = struct.unpack_from("<ff", data, _OFF_SPEED)
                yield Telemetry(
                    speed_kmh=max(0.0, speed_ms * 3.6),
                    rpm=max(0.0, rpm),
                )
        finally:
            sock.close()
