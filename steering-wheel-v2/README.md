# DAZ Racing V2 steering wheel — Amazon parts list

Amazon (US) equivalents for the DAZ Racing V2 hoverboard direct-drive wheel.
The original AliExpress list is in [`parts-list-aliexpress.csv`](parts-list-aliexpress.csv);
the same data in spreadsheet form is in [`parts-list-amazon.csv`](parts-list-amazon.csv).

Prices are what Amazon showed in Oct 2026 and will drift. Listings come and go —
if a link is dead, use the search link in the last column.

> The designer only guarantees the build with the parts he linked. Anything marked
> **check fit** should be compared against the AliExpress listing (photos, dimensions)
> before you order.

## Estimated total (Oct 2026, before tax and shipping)

### Main components 1–14 (cheaper encoder, **two** button packs, **no** wireless board)

| # | Part | ~$ | Source |
|---|------|-----|--------|
| 1 | MKS XDrive Mini | 63 | Amazon listing |
| 2 | 6.5" hoverboard motor | 75 | Amazon listing |
| 3 | Encoder E6B2-CWZ6C 2000 P/R (generic) | 40 | Amazon listing |
| 4 | Steering wheel 13" / 330 mm | 95 | Estimate (RUNSCO ~$95 direct; Amazon ASIN often unavailable) |
| 5 | GT2 pulley 20T | 10 | Amazon listing (5-pack; you need one) |
| 6 | GT2 belt 212 mm | 15 | Amazon listing (5-pack; you need one) |
| 7 | GT2 idler 20T | 9 | Amazon listing (5-pack; you need one) |
| 8 | Wireless button board | — | **Not included** in subtotal below |
| 9 | XT60 connectors (5 pairs) | 8 | Estimate (~$8–12 for genuine Amass 5-pair) |
| 10 | Limit switches (10-pack) | 6 | Amazon listing |
| 11 | Push buttons, **2×** 6-pack | 18 | Amazon listing ($9 × 2 per BOM) |
| 12 | Magnets 30×10×4 mm (18-pack) | 12 | Estimate |
| 13 | 2×AA battery holder | 6 | Amazon listing (3-pack; you need one) |
| 14 | 24 V 10 A PSU | 22 | Amazon listing |
| | **Subtotal (main only)** | **379** | |

| Group | Cost |
|-------|------|
| Main components (table above) | 379 |
| Wireless button board (item 8, unconfirmed part) | ~20 |
| Quick release upgrade (items 15–18) | ~57 |
| Nuts, bolts, nails | ~20 |
| **Full build** | **~475** |

Without the quick release upgrade: **~$399** (379 + 20 wireless). Using genuine Omron encoder (+$90 on item 3): main subtotal **~$469**.

## Main components

| # | Part | Amazon pick | ~Price | Notes | Backup search |
|---|------|-------------|--------|-------|---------------|
| 1 | MKS XDrive Mini (FOC controller) | [CLNXMT MKS XDrive Mini, ODrive 3.6 + AS5047P](https://www.amazon.com/dp/B0GWXY1YWW) | $63 | Same board as the AliExpress one, marked up. Stay on its stock v0.5.1 firmware; don't run the odrivetool `upgrade` command on it. | [search](https://www.amazon.com/s?k=MKS+XDrive+Mini) |
| 2 | 6.5" hoverboard motor | [L-faster 6.5" self-balancing scooter motor, 36V 350W](https://www.amazon.com/dp/B0CCV76FCM) | $75 | Sold as a hoverboard replacement. A reviewer used it for a force-feedback wheel but had to reseat a crooked bearing. A used hoverboard from a local marketplace is often cheaper. | [search](https://www.amazon.com/s?k=6.5+inch+hoverboard+motor+replacement) |
| 3 | Encoder E6B2-CWZ6C 2000 P/R | [RSHVOBRRS E6B2-CWZ6C 2000P/R, 5–24 V NPN, 2 m cable](https://www.amazon.com/dp/B0FXFCBY9T) | $40 | Generic copy, same part number and 6 mm shaft. Genuine: [Omron E6B2-CWZ6C 2000P/R 2M](https://www.amazon.com/dp/B00J7HSSN8) ($130). | [search](https://www.amazon.com/s?k=E6B2-CWZ6C+2000P%2FR) |
| 4 | Steering wheel (13" / 330 mm) | [RUNSCO 13" 330 mm suede, 6-bolt 70 mm PCD](https://www.amazon.com/dp/B09Z22MFZL) or [Hiracing 330 mm flat-bottom, 6-bolt 70 mm](https://www.amazon.com/dp/B0D73GH2K4) | $95 | **Check fit.** Estimate when Amazon is out of stock; RUNSCO sells direct ~$95. Match 330 mm and 6×70 mm PCD. | [search](https://www.amazon.com/s?k=13+inch+330mm+6+bolt+steering+wheel+suede) |
| 5 | GT2 pulley, 20T, 6 mm bore, 6 mm belt | [Bemonoc 2GT 20T 6 mm bore (5-pack)](https://www.amazon.com/dp/B014KN70QE) | $10 | Alt: [MECCANIXITY 2-pack](https://www.amazon.com/dp/B09VPR5RZN) | [search](https://www.amazon.com/s?k=GT2+20+teeth+pulley+6mm+bore+6mm+width) |
| 6 | GT2 belt, closed loop, 212 mm, 6 mm wide | [PJinloog 2GT 212 mm × 6 mm (5-pack)](https://www.amazon.com/dp/B096HCQMVY) | $15 | Pick the **212 mm** length option. Single belt: [FORYON 2GT212](https://www.amazon.com/dp/B0DLNH2GPP) | [search](https://www.amazon.com/s?k=GT2+closed+loop+belt+212mm+6mm) |
| 7 | GT2 idler, 20T, 5 mm bore, 6 mm belt | [WINSINN GT2 idler 20T 5 mm (5-pack)](https://www.amazon.com/dp/B07BPGYX3G) | $9 | Get the toothed version, not smooth. | [search](https://www.amazon.com/s?k=GT2+idler+20+teeth+5mm+bore+6mm) |
| 8 | Wireless button board | No confirmed match — best guess: a 2.4 GHz wireless "zero delay" arcade encoder | — | **Check fit.** The AliExpress listing couldn't be read. It runs off the 2×AA holder (item 13), which points to a 2.4 GHz zero-delay wireless encoder with a USB receiver. Compare photos and pin layout with the AliExpress board. | [search](https://www.amazon.com/s?k=2.4G+wireless+zero+delay+arcade+encoder) |
| 9 | XT60 connectors | [Amass XT60 male/female, 5 pairs](https://www.amazon.com/dp/B00WND5A5C) | $8 | Estimate; 10-pair with heat shrink: [YoWoo/Amass](https://www.amazon.com/dp/B07233RVL6) | [search](https://www.amazon.com/s?k=Amass+XT60+connectors) |
| 10 | Limit switches (roller lever) | [HiLetgo KW12-3 roller lever micro switch (10-pack)](https://www.amazon.com/dp/B07X142VGC) | $6 | Paddle shifters. Wire to the normally-open (NO) pin. | [search](https://www.amazon.com/s?k=KW12-3+roller+lever+limit+switch) |
| 11 | Push buttons (buy two sets) | [Twidec 12 mm momentary, pre-wired (6-pack)](https://www.amazon.com/dp/B08JHW8BPV) | $18 | 8 buttons on the wheel → **2×** six-packs ($9 each). Alt: [ESUPPORT 10-pack](https://www.amazon.com/dp/B018TV1E4C). **Check fit**: 12 mm hole. | [search](https://www.amazon.com/s?k=12mm+momentary+push+button+switch) |
| 12 | Magnets 30×10×4 mm (or 30×10×3) | [ENHOCIYT 30×10×4 mm neodymium (18-pack)](https://www.amazon.com/dp/B0C9CKX9Y9) | $12 | Estimate for 18-pack. Paddle magnets. | [search](https://www.amazon.com/s?k=30x10x4mm+neodymium+block+magnet) |
| 13 | AA battery holder (2× AA) | [LampVPath 2×AA holder with leads (3-pack)](https://www.amazon.com/dp/B07TB4HDYH) | $6 | With on/off switch: [LampVPath 2-pack](https://www.amazon.com/dp/B09T9XZH5M) | [search](https://www.amazon.com/s?k=2+AA+battery+holder+with+leads) |
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
