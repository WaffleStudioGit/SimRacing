# SimRacing gauges

Game speed + RPM → PC bridge → Arduino → servos, shift-light bar, cabin controls.

```
Game ──telemetry──► bridge ──serial──► Arduino ──► speed servo
                                      │           rpm servo
                                      │           10× LED shift lights
                                      └──◄── key / lights / 3× Ender endstops
                                              (bridge → in-game keys)
```

Games: **Forza** (Data Out), **BeamNG** (OutGauge), **Assetto Corsa** (shared memory), plus **demo** sweep.

## Hardware (matches a typical Uno bench)

| Piece | Arduino pin | Notes |
|-------|-------------|--------|
| Speed servo | **D9** | Own 5V supply, common GND |
| RPM servo | **D10** | same |
| LED bar (10) GGGG YYY RRR | **D2–D8, D11, D12, D13** | Anode → pin, cathode → **220Ω** → GND |
| Engine key (toggle) | **A0** | Switch between pin and GND (pull-up on) |
| Headlights rocker | **A1** | same |
| Ender 3 endstops 1 / 2 / 3 | **A2 / A3 / A4** | See wiring below |

### Ender 3 endstops (buttons)

Stock Creality mechanical endstops are the three cabin buttons. Plug is usually **GND / SIG / VCC** (sometimes labeled G S V — verify your cable):

| Endstop wire | Arduino |
|--------------|---------|
| GND | GND |
| SIG | A2, A3, or A4 |
| VCC | **5V** (powers the little LED on the board) |

Lever pressed → SIG low → “button down” (25 ms debounce in firmware). If a switch reads inverted, set `ENDSTOP_INVERT` to `1` in the sketch.

Shift lights fill left→right with RPM (first LED ~55% redline, full bar at redline, flash above ~97%). Key **off** parks needles and kills the bar.

## Firmware

1. Flash `firmware/gauge_servos/gauge_servos.ino`
2. Serial @ **115200** → `OK gauge_servos`, then `I …` input lines

```
PC → board:  V <km/h> <rpm>   |  C <max_speed> <max_rpm>  |  Z
board → PC:  I <engine> <lights> <endstop1> <endstop2> <endstop3>
```

## Bridge

```bash
cd bridge
pip install -r requirements.txt
pip install pynput          # Windows gaming PC — cabin → keyboard
cp config.example.toml config.toml   # set COM port + keybinds
python -m sim_gauges --game demo --port COM3
python -m sim_gauges --game forza --port COM3
```

Bind the keys in `[controls]` to whatever your game uses for ignition, lights, horn, etc. Use `--no-keys` to only watch cabin state.

### Game telemetry

- **Forza**: Data Out ON → this PC IP, port `5300`
- **BeamNG**: OutGauge → port `4444`
- **Assetto Corsa**: bridge on same Windows PC as the game

## Steering wheel build

Amazon parts list for the DAZ Racing V2 hoverboard wheel: [`steering-wheel-v2/`](steering-wheel-v2/README.md).

## Notes

- Put a resistor on every LED. Ten bare LEDs will abuse the Uno.
- Servos need a separate 5V brick; USB alone is not enough.
- Tune needle travel with `SPEED_DEG_*` / `RPM_DEG_*` in the sketch after you mount the dials.
