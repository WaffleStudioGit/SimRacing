"""Serial IO for the Arduino gauge / cabin firmware."""

from __future__ import annotations

import time
from typing import Callable, Optional

import serial

from .protocol import CabinInputs, config_line, parse_input_line, value_line, zero_line


class GaugeSerial:
    def __init__(self, port: str, baud: int = 115200, timeout: float = 0.05) -> None:
        self.port = port
        self.baud = baud
        self.timeout = timeout
        self._ser: Optional[serial.Serial] = None
        self._last_sent = (None, None)
        self._rx_buf = ""
        self.last_inputs: Optional[CabinInputs] = None

    def open(self) -> None:
        self._ser = serial.Serial(self.port, self.baud, timeout=self.timeout)
        time.sleep(2.0)
        self._ser.reset_input_buffer()
        self._rx_buf = ""

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

    def poll_inputs(
        self, on_input: Optional[Callable[[CabinInputs], None]] = None
    ) -> Optional[CabinInputs]:
        """Read any pending Arduino lines; return latest cabin state if any."""
        assert self._ser is not None
        latest: Optional[CabinInputs] = None
        chunk = self._ser.read(self._ser.in_waiting or 0)
        if chunk:
            self._rx_buf += chunk.decode("ascii", errors="ignore")
        while "\n" in self._rx_buf:
            line, self._rx_buf = self._rx_buf.split("\n", 1)
            line = line.strip()
            if not line or line.startswith("OK"):
                continue
            parsed = parse_input_line(line)
            if parsed is None:
                continue
            latest = parsed
            self.last_inputs = parsed
            if on_input is not None:
                on_input(parsed)
        return latest

    def __enter__(self) -> "GaugeSerial":
        self.open()
        return self

    def __exit__(self, *_) -> None:
        self.close()
