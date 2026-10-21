# SimRacing gauges

Game speed + RPM → PC bridge → Arduino → two servos (speedo + tach).

Supports **Forza Horizon / Motorsport** (Data Out UDP), **BeamNG.drive** (OutGauge), **Assetto Corsa** (shared memory, Windows), plus a **demo** sweep for bench testing.

```
Game telemetry ──► bridge (Python) ──serial──► Arduino ──► servo speed
                                                      └──► servo rpm
```

## Hardware

| Piece | Notes |
|-------|--------|
| Arduino Uno / Nano / similar | Any board with `Servo.h` |
| 2× hobby servos | SG90 is fine for light needles |
| Separate 5V supply for servos | Do **not** power both servos from the Arduino 5V pin |
| Common GND | Arduino GND tied to servo supply GND |

**Pins (change in firmware if you want):**

- Speed servo signal → **D9**
- RPM servo signal → **D10**

After mounting needles, edit `SPEED_DEG_*` / `RPM_DEG_*` in `firmware/gauge_servos/gauge_servos.ino` so 0 and full-scale match the dial artwork.

## Firmware

1. Open `firmware/gauge_servos/gauge_servos.ino` in Arduino IDE.
2. Flash the board.
3. Serial monitor @ **115200** should print `OK gauge_servos`.

Protocol (newline-terminated):

```
V <speed_kmh> <rpm>     # move needles
C <max_speed> <max_rpm> # set full-scale
Z                       # needles to zero
```

## Bridge (PC)

```bash
cd bridge
python -m venv .venv
# Windows: .venv\Scripts\activate
source .venv/bin/activate
pip install -r requirements.txt
cp config.example.toml config.toml   # edit port / UDP ports
```

**Bench test (no game):**

```bash
python -m sim_gauges --game demo --port COM3
# or dry-run without hardware:
python -m sim_gauges --game demo --dry-run
```

**Games:**

```bash
python -m sim_gauges --game forza --port COM3
python -m sim_gauges --game beamng --port COM3
python -m sim_gauges --game assetto --port COM3   # Windows, game running
```

### Per-game setup

**Forza Horizon 5 / Motorsport**  
Settings → HUD / DATA OUT → On. IP = this PC, port = `forza.listen_port` in config (default `5300`). Windows Firewall must allow UDP inbound.

**BeamNG.drive**  
Options → Other → OutGauge enabled, same IP/port as `beamng.listen_port` (default `4444`).

**Assetto Corsa**  
Run the bridge on the **same Windows PC** as the game. No extra plugins — reads `Local\acpmf_physics`.

## Layout

```
firmware/gauge_servos/   Arduino sketch
bridge/sim_gauges/       Python package
bridge/config.example.toml
bridge/tests/            Packet / protocol checks
```

## Notes

- Full-scale defaults are 300 km/h and 9000 rpm (`config.toml` / `--max-speed` / `--max-rpm`). Forza also retunes max RPM from the packet when redline is present.
- Assetto Corsa Competizione uses different shared memory; this repo targets Assetto Corsa.
- If needles twitch, lower `gauges.update_hz` or add mechanical damping on the linkage.
