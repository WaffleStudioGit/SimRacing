"""Serial writer for the Arduino gauge firmware."""

from __future__ import annotations

import time
from typing import Optional

import serial

from .protocol import config_line, value_line, zero_line


class GaugeSerial:
    def __init__(self, port: str, baud: int = 115200, timeout: float = 0.2) -> None:
        self.port = port
        self.baud = baud
        self.timeout = timeout
        self._ser: Optional[serial.Serial] = None
        self._last_sent = (None, None)

    def open(self) -> None:
        self._ser = serial.Serial(self.port, self.baud, timeout=self.timeout)
        # USB-serial boards reset on open; give firmware a moment
        time.sleep(2.0)
        self._ser.reset_input_buffer()

    def close(self) -> None:
        if self._ser and self._ser.is_open:
            try:
                self._ser.write(zero_line())
                self._ser.flush()
            except serial.SerialException:
                pass
            self._ser.close()
        self._ser = None

    def configure(self, max_speed_kmh: float, max_rpm: float) -> None:
        assert self._ser is not None
        self._ser.write(config_line(max_speed_kmh, max_rpm))
        self._ser.flush()

    def send(self, speed_kmh: float, rpm: float, force: bool = False) -> None:
        assert self._ser is not None
        key = (round(speed_kmh, 1), round(rpm, 0))
        if not force and key == self._last_sent:
            return
        self._ser.write(value_line(speed_kmh, rpm))
        self._last_sent = key

    def __enter__(self) -> "GaugeSerial":
        self.open()
        return self

    def __exit__(self, *_) -> None:
        self.close()
