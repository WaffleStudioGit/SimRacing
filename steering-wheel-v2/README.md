# DAZ Racing V2 steering wheel — Amazon parts list

Amazon (US) equivalents for the DAZ Racing V2 hoverboard direct-drive wheel.
The original AliExpress list is in [`parts-list-aliexpress.csv`](parts-list-aliexpress.csv);
the same data in spreadsheet form is in [`parts-list-amazon.csv`](parts-list-amazon.csv).

Prices are what Amazon showed in Oct 2026 and will drift. Listings come and go —
if a link is dead, use the search link in the last column.

> The designer only guarantees the build with the parts he linked. Anything marked
> **check fit** should be compared against the AliExpress listing (photos, dimensions)
> before you order.

## Estimated total (Oct 2026, before shipping)

Sales tax below is **6%** on the part prices. Amazon shipping is not included.

### Main components 1–14 (cheaper encoder, **two** button packs, **no** wireless board)

| # | Part | ~$ | Source |
|---|------|-----|--------|
| 1 | MKS XDrive Mini | 63 | Amazon listing |
| 2 | 6.5" hoverboard motor | 75 | Amazon listing |
| 3 | Encoder E6B2-CWZ6C 2000 P/R (generic) | 40 | Amazon listing |
| 4 | Steering wheel, flat ~320–350 mm | 23 | [YEHICY 13.8" flat vinyl](https://www.amazon.com/dp/B09GRQ8XR2). Bolt pattern does not matter if you drill the hub or a plate. |
| 5 | GT2 pulley 20T | 10 | Amazon listing (5-pack; you need one) |
| 6 | GT2 belt 212 mm | 15 | Amazon listing (5-pack; you need one) |
| 7 | GT2 idler 20T | 9 | Amazon listing (5-pack; you need one) |
| 8 | Wireless button board | — | **Not included** in subtotal below |
| 9 | XT60 connectors (5 pairs) | 8 | Estimate (~$8–12 for genuine Amass 5-pair) |
| 10 | Limit switches (10-pack) | 6 | Amazon listing |
| 11 | Push buttons, 12 mm momentary (10-pack) | 4 | [ucomshop 10-pack](https://www.amazon.com/dp/B072535X2W) (~$3.50). One pack covers the 8 wheel buttons. |
| 12 | Magnets 30×10×4 mm (18-pack) | 12 | Paddle magnets. Skip if you already have them. |
| 13 | 2×AA battery holder | 6 | Amazon listing (3-pack; you need one) |
| 14 | 24 V 10 A PSU | 22 | Amazon listing |
| | **Subtotal (main only)** | **293** | |
| | 6% sales tax | 18 | |
| | **Main only, with tax** | **311** | |

| Group | Before tax | With 6% tax |
|-------|------------|-------------|
| Main components | 293 | 311 |
| Wireless button board (item 8, unconfirmed) | 20 | 21 |
| Quick release upgrade (items 15–18) | 57 | 60 |
| Nuts, bolts, nails | 20 | 21 |
| **Full build** | **390** | **413** |

Without the quick release upgrade: **$313** before tax, **$332** with tax (293 + 20 wireless). The ~$95 suede rim adds about $72. Genuine Omron encoder adds $90 on item 3.

### If you already have a hoverboard and lever switches

Skip the motor ($75) and the roller limit switches ($6). Ender 3 endstops work electrically as the paddle switches. The printed paddle was drawn around a roller lever, so a plain lever can snag; it is fine if the paddle hits the lever cleanly.

### Cheaper magnetic encoder (FFBeast's own cheap build)

The belt, pulley, idler, and Omron-style encoder only exist so the PC can read wheel angle. [FFBeast's encoder page](https://ffbeast.github.io/docs/en/hardware_encoder.html) accepts any incremental A/B encoder, and their [cheap reference wheel](https://ffbeast.github.io/docs/en/wheel_assembly.html) uses an **MT6701** magnetic module at about **$2–5** (4096 counts/rev). Amazon example: [MT6701 module with magnet, ~$5](https://www.amazon.com/dp/B0D3F44HZL).

Use the **ABZ** pins (A and B). Z is unused. In the FFBeast config set encoder CPR to **4096**. Power the module from **3.3 V** so the outputs match the controller pins.

The kit magnet is diametric (poles on the round face). The 30×10×4 mm paddle magnets will not work here. Center that small magnet on the axle end and hold the PCB on the same axis, a couple of millimetres away. Off-center mounting makes the force feel uneven. The DAZ printed parts are shaped for the belt and the 40 mm encoder body, so this needs a small printed bracket of your own. Then you can also skip the GT2 pulley ($10), belt ($15), and idler ($9).

Skip the AS5600 (no A/B output the firmware can use) and the TLE5012B (a dead zone feels like backlash). The hoverboard's built-in Hall sensors are too coarse.

### What you still buy

Already on hand: hoverboard motor, steering wheel, paddle magnets, Ender 3 limit switches, ESP32 for the buttons, and XT60 connectors from an old Ender 3. Encoder is the MT6701, so the belt, pulley, idler, Omron encoder, wireless board, and AA holder are out.

| # | Part | Amazon ASIN | ~$ |
|---|------|-------------|----|
| 1 | MKS XDrive Mini | B0GWXY1YWW | 63 |
| 2 | MT6701 magnetic encoder (magnet included) | B0D3F44HZL | 5 |
| 3 | 12 mm momentary buttons, 10-pack | B072535X2W | 4 |
| 4 | 24 V 10 A power supply | B078RYWZMH | 22 |
| 5 | 1S 3.7 V 500 mAh LiPo (ESP32 in the rim) | B07QM19PL8 | 12 |
| 6 | 16×16 aluminum shaft clamp | B0BJ39VF5W | 24 |
| 7 | 16 mm aluminum tube, cut to 100 mm | B0CL6L4BR8 | 10 |
| | **Before tax** | | **140** |
| | 6% sales tax | | 8 |
| | **With tax** | | **148** |

Screws and nails are listed at the bottom and are not in that total.

### Why the batteries are there

The 24 V supply powers the motor controller, which stays on the desk. The buttons live in the rim, and the rim spins. The published design puts a small wireless board in the rim and runs it on **two AA cells** (3 V) through the battery holder, so no cable has to follow the rim around. The cells themselves are not in the price above, only the holder.

It can be wired. A sim wheel only turns about one and a half turns each way, so a loose loop of wire, or a coiled cable, has enough slack. Each button connects between a controller input and ground. In FFBeast, set that pin to **Generic button**. The pin is already pulled up, so a press to ground reads as on. [FFBeast wiring notes](https://ffbeast.github.io/docs/en/connection_odrive.html).

The MKS XDrive Mini does not bring every GPIO pin out to a connector, and FFBeast has eight button inputs total. This rim wants eight face buttons plus two paddle switches, so those ten switches may not all fit on the Mini's exposed pins. A wired USB button board in the rim, with one cable back to the PC, covers all of them. A slip ring is only needed if the wheel must spin without a stop.

Wired this way, drop the wireless board and the battery holder. The cart above goes from $131 to **$125** before tax, **$133** with 6% tax.

### ESP32 in the rim, no cable down the shaft

An ESP32 replaces the wireless button board. Flash it with the [ESP32-BLE-Gamepad](https://github.com/lemmingDev/ESP32-BLE-Gamepad) library and it shows up as a Bluetooth gamepad. FFBeast on the XDrive Mini stays as it is and still does the force feedback. The game sees two devices: the wheel axis from FFBeast, and the buttons from the ESP32.

Use a board that has Bluetooth: original ESP32, ESP32-C3, ESP32-S3, or ESP32-C6. An ESP32-S2 has no Bluetooth radio. A Super Mini fits the printed pocket better than a full-size dev board. Example: [AITRIP ESP32-C3 Super Mini, 2-pack, ~$10](https://www.amazon.com/dp/B0FBGDFPBQ).

Each face button and each paddle goes from its own GPIO pin to ground. The sketch uses the internal pull-up. Those leads stay inside the rim. Nothing runs out to the PC.

The original 2×AA pack is a poor supply for this. A connected ESP32 draws tens of milliamps and two AA cells sag until the board resets. Power a Super Mini from a small 1S LiPo (3.7 V) on its 5 V pin. Widen the printed battery bay if the cell does not sit in the AA holder.

If a game ignores the pad, use the library's XInput mode so Windows treats it as an Xbox controller. Generic HID is enough for the Windows game-controller test and for most sims.

Already have an ESP32: drop the $6 holder and the wireless board. The cart is **$125** before tax, **$133** with 6% tax, plus a LiPo if you do not have one. Buying a Super Mini adds about $5.

## Main components

| # | Part | Amazon pick | ~Price | Notes | Backup search |
|---|------|-------------|--------|-------|---------------|
| 1 | MKS XDrive Mini (FOC controller) | [CLNXMT MKS XDrive Mini, ODrive 3.6 + AS5047P](https://www.amazon.com/dp/B0GWXY1YWW) | $63 | Same board as the AliExpress one, marked up. Stay on its stock v0.5.1 firmware; don't run the odrivetool `upgrade` command on it. | [search](https://www.amazon.com/s?k=MKS+XDrive+Mini) |
| 2 | 6.5" hoverboard motor | [L-faster 6.5" self-balancing scooter motor, 36V 350W](https://www.amazon.com/dp/B0CCV76FCM) | $75 | Sold as a hoverboard replacement. A reviewer used it for a force-feedback wheel but had to reseat a crooked bearing. A used hoverboard from a local marketplace is often cheaper. | [search](https://www.amazon.com/s?k=6.5+inch+hoverboard+motor+replacement) |
| 3 | Encoder E6B2-CWZ6C 2000 P/R | [RSHVOBRRS E6B2-CWZ6C 2000P/R, 5–24 V NPN, 2 m cable](https://www.amazon.com/dp/B0FXFCBY9T) | $40 | Generic copy, same part number and 6 mm shaft. Genuine: [Omron E6B2-CWZ6C 2000P/R 2M](https://www.amazon.com/dp/B00J7HSSN8) ($130). | [search](https://www.amazon.com/s?k=E6B2-CWZ6C+2000P%2FR) |
| 4 | Steering wheel | [YEHICY 13.8" / 350 mm flat vinyl](https://www.amazon.com/dp/B09GRQ8XR2) | $23 | Bolt circle does not matter: drill the aluminum spokes or a flat plate to match the printed hub. Prefer a flat rim over a deep dish so the grip clears the printed shells. Same price band: [Auto Dynasty 320 mm](https://www.amazon.com/dp/B075FJL18P). Nicer suede if you want it later: [RUNSCO 330 mm](https://www.amazon.com/dp/B09Z22MFZL) (~$95). | [search](https://www.amazon.com/s?k=flat+vinyl+racing+steering+wheel+320mm+350mm) |
| 5 | GT2 pulley, 20T, 6 mm bore, 6 mm belt | [Bemonoc 2GT 20T 6 mm bore (5-pack)](https://www.amazon.com/dp/B014KN70QE) | $10 | Alt: [MECCANIXITY 2-pack](https://www.amazon.com/dp/B09VPR5RZN) | [search](https://www.amazon.com/s?k=GT2+20+teeth+pulley+6mm+bore+6mm+width) |
| 6 | GT2 belt, closed loop, 212 mm, 6 mm wide | [PJinloog 2GT 212 mm × 6 mm (5-pack)](https://www.amazon.com/dp/B096HCQMVY) | $15 | Pick the **212 mm** length option. Single belt: [FORYON 2GT212](https://www.amazon.com/dp/B0DLNH2GPP) | [search](https://www.amazon.com/s?k=GT2+closed+loop+belt+212mm+6mm) |
| 7 | GT2 idler, 20T, 5 mm bore, 6 mm belt | [WINSINN GT2 idler 20T 5 mm (5-pack)](https://www.amazon.com/dp/B07BPGYX3G) | $9 | Get the toothed version, not smooth. | [search](https://www.amazon.com/s?k=GT2+idler+20+teeth+5mm+bore+6mm) |
| 8 | Wireless button board | [AITRIP ESP32-C3 Super Mini, 2-pack](https://www.amazon.com/dp/B0FBGDFPBQ) | $10 | Use one board in the rim as a Bluetooth gamepad ([ESP32-BLE-Gamepad](https://github.com/lemmingDev/ESP32-BLE-Gamepad)). Do not buy an ESP32-S2; it has no Bluetooth. Power it from a 1S LiPo, not two AA cells. | [search](https://www.amazon.com/s?k=ESP32-C3+Super+Mini) |
| 9 | XT60 connectors | [Amass XT60 male/female, 5 pairs](https://www.amazon.com/dp/B00WND5A5C) | $8 | Estimate; 10-pair with heat shrink: [YoWoo/Amass](https://www.amazon.com/dp/B07233RVL6) | [search](https://www.amazon.com/s?k=Amass+XT60+connectors) |
| 10 | Limit switches (roller lever) | [HiLetgo KW12-3 roller lever micro switch (10-pack)](https://www.amazon.com/dp/B07X142VGC) | $6 | Paddle shifters. Wire to the normally-open (NO) pin. | [search](https://www.amazon.com/s?k=KW12-3+roller+lever+limit+switch) |
| 11 | Push buttons | [ucomshop 12 mm momentary, 10-pack](https://www.amazon.com/dp/B072535X2W) | $4 | One pack covers the 8 wheel buttons (12 mm hole). Pre-wired if you would rather not solder: [Meimom 10-pack](https://www.amazon.com/dp/B0D5MC7881) (~$9). | [search](https://www.amazon.com/s?k=12mm+momentary+push+button+10+pack) |
| 12 | Magnets 30×10×4 mm (or 30×10×3) | [ENHOCIYT 30×10×4 mm neodymium (18-pack)](https://www.amazon.com/dp/B0C9CKX9Y9) | $12 | Paddle return magnets. Not required if you already have magnets that fit the printed holders. The MT6701 kit includes its own small diametric magnet; these bar magnets do not replace that one. | [search](https://www.amazon.com/s?k=30x10x4mm+neodymium+block+magnet) |
| 13 | AA battery holder (2× AA) | [LampVPath 2×AA holder with leads (3-pack)](https://www.amazon.com/dp/B07TB4HDYH) | $6 | Powers the wireless button board in the spinning rim only. The motor uses the 24 V supply. With on/off switch: [LampVPath 2-pack](https://www.amazon.com/dp/B09T9XZH5M). | [search](https://www.amazon.com/s?k=2+AA+battery+holder+with+leads) |
| 14 | Power supply 24 V 10 A | [ALITOVE 24V 10A 240W](https://www.amazon.com/dp/B078RYWZMH) | $22 | Name brand: [Mean Well SP-240-24](https://www.amazon.com/dp/B00NBMW7F0) | [search](https://www.amazon.com/s?k=24V+10A+240W+power+supply) |

## Upgraded quick release (only if you're upgrading from the old design)

| # | Part | Amazon pick | ~Price | Notes | Backup search |
|---|------|-------------|--------|-------|---------------|
| 15 | Motor axle clamp, 16×16 | [16×16 aluminum shaft cross clamp](https://www.amazon.com/dp/B0BJ39VF5W) | — | Choose the **16×16** (same-diameter) option. Alt: [Flozari 16×16](https://www.amazon.com/dp/B0FKN26VJR) | [search](https://www.amazon.com/s?k=16x16+aluminum+shaft+cross+clamp) |
| 16 | 16 mm aluminum tube (cut to 100 mm) | [JoyTube 6061, 16 mm OD × 12 mm ID, 300 mm (2 pcs)](https://www.amazon.com/dp/B0CL6L4BR8) | $10 | Cut one piece to 100 mm. | [search](https://www.amazon.com/s?k=16mm+OD+aluminum+tube+6061) |
| 17 | Quick release base (Arca-Swiss clamp) | [Neewer 50 mm Arca-Swiss QR clamp](https://www.amazon.com/dp/B00KYEO70Q) | $14 | **Check fit.** Its mounting holes and footprint must match the printed mount. Alt: [CAVIX QR-50](https://www.amazon.com/dp/B096XQ8L2W) | [search](https://www.amazon.com/s?k=arca+swiss+quick+release+clamp+50mm) |
| 18 | Quick release plate, 100 mm long | [Harwerrel 100 mm Arca-Swiss plate](https://www.amazon.com/dp/B076Z8LL5Y) | $9 | Alt: [HITHUT 100 mm](https://www.amazon.com/dp/B0B3RJ1V3S) | [search](https://www.amazon.com/s?k=100mm+arca+swiss+quick+release+plate) |

## Nuts and bolts

A metric hex socket assortment covers most of these. Buy the self-tapping screws and nails separately.

| Qty | Item | Search |
|-----|------|--------|
| 9 | 3 mm nail | [search](https://www.amazon.com/s?k=3mm+nails) |
| 4 | M5 nut | [search](https://www.amazon.com/s?k=M5+hex+nuts) |
| 2 | M5 × 25 socket head screw | [search](https://www.amazon.com/s?k=M5x25+socket+head+cap+screw) |
| 8 | M3 × 12 self-tapping screw | [search](https://www.amazon.com/s?k=M3x12+self+tapping+screw) |
| 6 | M2.5 × 6 self-tapping screw | [search](https://www.amazon.com/s?k=M2.5x6+self+tapping+screw) |
| 3 | M6 nut | [search](https://www.amazon.com/s?k=M6+hex+nuts) |
| 2 | M6 × 30 countersunk screw | [search](https://www.amazon.com/s?k=M6x30+countersunk+screw) |
| 1 | M6 × 45 countersunk screw | [search](https://www.amazon.com/s?k=M6x45+countersunk+screw) |
| 3 | M3 × 10 socket head screw | [search](https://www.amazon.com/s?k=M3x10+socket+head+cap+screw) |
| 1 | M5 × 20 cap screw | [search](https://www.amazon.com/s?k=M5x20+socket+head+cap+screw) |
| 2 | M5 × 40 socket head screw | [search](https://www.amazon.com/s?k=M5x40+socket+head+cap+screw) |
| 2 | M5 washer | [search](https://www.amazon.com/s?k=M5+flat+washers) |
