import struct
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from sim_gauges.controls import CabinController, KeyBinds, binds_from_config
from sim_gauges.protocol import (
    CabinInputs,
    config_line,
    parse_input_line,
    value_line,
    zero_line,
)
from sim_gauges.sources.beamng import _OUTGAUGE_FMT, _OUTGAUGE_SIZE
from sim_gauges.sources.forza import _OFF_CURRENT_RPM, _OFF_ENGINE_MAX_RPM, _OFF_SPEED


def test_value_line():
    assert value_line(123.45, 4500.2) == b"V 123.5 4500\n"


def test_config_and_zero():
    assert config_line(280, 8000) == b"C 280 8000\n"
    assert zero_line() == b"Z\n"


def test_parse_input_line():
    assert parse_input_line("I 1 0 1 0 0") == CabinInputs(True, False, True, False, False)
    assert parse_input_line("OK gauge_servos") is None
    assert parse_input_line("I 1 0") is None


def test_cabin_edges_dry_run():
    ctrl = CabinController(KeyBinds(enabled=True), dry_run=True)
    ctrl.handle(CabinInputs(False, False, False, False, False))  # prime
    ctrl.handle(CabinInputs(True, False, False, False, False))  # engine on
    ctrl.handle(CabinInputs(True, True, False, False, False))  # lights
    ctrl.handle(CabinInputs(True, True, True, False, False))  # endstop1 press


def test_endstop_config_alias():
    binds = binds_from_config({"controls": {"endstop1": "x", "endstop2": "y", "endstop3": "z"}})
    assert binds.btn1 == "x"
    assert binds.btn2 == "y"
    assert binds.btn3 == "z"
    binds2 = binds_from_config({"controls": {"btn1": "a"}})
    assert binds2.btn1 == "a"


def test_forza_offsets_unpack():
    buf = bytearray(331)
    struct.pack_into("<i", buf, 0, 1)
    struct.pack_into("<f", buf, _OFF_ENGINE_MAX_RPM, 7500.0)
    struct.pack_into("<f", buf, _OFF_CURRENT_RPM, 3200.0)
    struct.pack_into("<f", buf, _OFF_SPEED, 27.7778)
    assert abs(struct.unpack_from("<f", buf, _OFF_SPEED)[0] * 3.6 - 100.0) < 0.1
    assert struct.unpack_from("<f", buf, _OFF_CURRENT_RPM)[0] == 3200.0


def test_beamng_packet_size():
    assert _OUTGAUGE_SIZE == 96
    packet = bytearray(_OUTGAUGE_SIZE)
    struct.pack_into("<ff", packet, 12, 20.0, 4000.0)
    unpacked = struct.unpack_from(_OUTGAUGE_FMT, packet, 0)
    assert abs(unpacked[5] - 20.0) < 1e-3
    assert abs(unpacked[6] - 4000.0) < 1e-3
