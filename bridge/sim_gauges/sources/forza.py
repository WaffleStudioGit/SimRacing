"""Forza Motorsport / Forza Horizon Data Out (UDP).

Enable in-game: HUD / SETTINGS → DATA OUT → ON, IP = your PC, port matching config.
Packet layouts (sled + dash / horizon):
  CurrentEngineRpm @ 16, EngineMaxRpm @ 8, Speed (m/s) @ 256
"""

from __future__ import annotations

import socket
import struct
from typing import Iterator

from .base import Telemetry

# Common Forza Data Out sizes
_PACKET_SIZES = {232, 311, 321, 331, 334}

_OFF_ENGINE_MAX_RPM = 8
_OFF_CURRENT_RPM = 16
_OFF_SPEED = 256  # m/s, dash / horizon formats only


class ForzaSource:
    name = "forza"

    def __init__(self, listen_ip: str = "0.0.0.0", listen_port: int = 5300) -> None:
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
                    data, _ = sock.recvfrom(512)
                except socket.timeout:
                    yield Telemetry(0.0, 0.0, connected=False)
                    continue
                if len(data) < _OFF_SPEED + 4:
                    continue
                if len(data) not in _PACKET_SIZES and len(data) < 260:
                    continue
                rpm = struct.unpack_from("<f", data, _OFF_CURRENT_RPM)[0]
                max_rpm = struct.unpack_from("<f", data, _OFF_ENGINE_MAX_RPM)[0]
                speed_ms = struct.unpack_from("<f", data, _OFF_SPEED)[0]
                # IsRaceOn is int32 at offset 0; if 0, car is not active
                is_race_on = struct.unpack_from("<i", data, 0)[0]
                if is_race_on == 0:
                    yield Telemetry(0.0, 0.0, max_rpm=max_rpm if max_rpm > 0 else None)
                    continue
                yield Telemetry(
                    speed_kmh=max(0.0, speed_ms * 3.6),
                    rpm=max(0.0, rpm),
                    max_rpm=max_rpm if max_rpm > 1 else None,
                )
        finally:
            sock.close()
