"""CLI entry: python -m sim_gauges --game forza --port COM3"""

from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path
from typing import Any, Dict

from .serial_out import GaugeSerial
from .sources import SOURCES
from .sources.assetto import AssettoSource
from .sources.beamng import BeamNGSource
from .sources.demo import DemoSource
from .sources.forza import ForzaSource


def _load_toml(path: Path) -> Dict[str, Any]:
    try:
        import tomllib
    except ModuleNotFoundError:
        import tomli as tomllib  # type: ignore
    with path.open("rb") as f:
        return tomllib.load(f)


def build_source(game: str, cfg: Dict[str, Any], max_speed: float, max_rpm: float):
    if game == "forza":
        section = cfg.get("forza", {})
        return ForzaSource(
            listen_ip=section.get("listen_ip", "0.0.0.0"),
            listen_port=int(section.get("listen_port", 5300)),
        )
    if game == "beamng":
        section = cfg.get("beamng", {})
        return BeamNGSource(
            listen_ip=section.get("listen_ip", "0.0.0.0"),
            listen_port=int(section.get("listen_port", 4444)),
        )
    if game == "assetto":
        section = cfg.get("assetto", {})
        return AssettoSource(physics_map=section.get("physics_map", r"Local\acpmf_physics"))
    if game == "demo":
        return DemoSource(max_speed_kmh=max_speed, max_rpm=max_rpm)
    raise SystemExit(f"Unknown game: {game}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Sim racing telemetry → Arduino speed/RPM servos"
    )
    parser.add_argument(
        "--game",
        choices=sorted(SOURCES.keys()),
        default="demo",
        help="Telemetry source (default: demo sweep)",
    )
    parser.add_argument("--port", help="Serial port (overrides config)")
    parser.add_argument("--baud", type=int, help="Baud rate (default 115200)")
    parser.add_argument("--config", type=Path, help="Path to config.toml")
    parser.add_argument("--max-speed", type=float, help="Gauge full-scale km/h")
    parser.add_argument("--max-rpm", type=float, help="Gauge full-scale RPM")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print telemetry, do not open serial",
    )
    args = parser.parse_args(argv)

    cfg: Dict[str, Any] = {}
    if args.config:
        cfg = _load_toml(args.config)
    else:
        default_cfg = Path(__file__).resolve().parents[1] / "config.toml"
        if default_cfg.exists():
            cfg = _load_toml(default_cfg)

    serial_cfg = cfg.get("serial", {})
    gauge_cfg = cfg.get("gauges", {})

    port = args.port or serial_cfg.get("port")
    baud = args.baud or int(serial_cfg.get("baud", 115200))
    max_speed = float(args.max_speed or gauge_cfg.get("max_speed_kmh", 300))
    max_rpm = float(args.max_rpm or gauge_cfg.get("max_rpm", 9000))
    update_hz = float(gauge_cfg.get("update_hz", 30))
    min_interval = 1.0 / max(1.0, update_hz)

    if not args.dry_run and not port:
        print("Set --port or serial.port in config.toml", file=sys.stderr)
        return 2

    source = build_source(args.game, cfg, max_speed, max_rpm)
    print(f"source={source.name}  max_speed={max_speed:.0f} km/h  max_rpm={max_rpm:.0f}")

    gauge = None
    if not args.dry_run:
        gauge = GaugeSerial(port, baud)
        gauge.open()
        gauge.configure(max_speed, max_rpm)
        print(f"serial={port} @{baud}")

    last_push = 0.0
    try:
        for frame in source.frames():
            now = time.monotonic()
            if now - last_push < min_interval:
                continue
            last_push = now

            speed = min(frame.speed_kmh, max_speed)
            rpm = min(frame.rpm, max_rpm)
            # If the game reports redline, optionally retune tach scale once
            if frame.max_rpm and frame.max_rpm > 1000 and gauge is not None:
                if abs(frame.max_rpm - max_rpm) > 50:
                    max_rpm = frame.max_rpm
                    gauge.configure(max_speed, max_rpm)

            status = "ok" if frame.connected else "waiting"
            line = f"\r{status:7}  {speed:6.1f} km/h   {rpm:6.0f} rpm"
            print(line, end="", flush=True)

            if gauge is not None:
                gauge.send(speed, rpm)
            elif args.dry_run:
                pass
    except KeyboardInterrupt:
        print("\nstopped")
    finally:
        if gauge is not None:
            gauge.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
