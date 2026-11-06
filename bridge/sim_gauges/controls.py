"""Map cabin switches/buttons to in-game keyboard binds."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Optional

from .protocol import CabinInputs


@dataclass
class KeyBinds:
    # Key names for pynput.keyboard.Key or single characters
    engine_on: Optional[str] = "i"  # ignition / starter bind in game
    engine_off: Optional[str] = None  # if None, tap engine_on again on off
    headlights: Optional[str] = "l"
    btn1: Optional[str] = "h"  # horn
    btn2: Optional[str] = "c"  # camera / look
    btn3: Optional[str] = "v"
    enabled: bool = True


def _key(section: Dict[str, Any], name: str, default: Optional[str]) -> Optional[str]:
    if name not in section:
        return default
    val = section[name]
    if val is None:
        return None
    s = str(val).strip()
    return s or None


def _btn_key(section: Dict[str, Any], index: int, default: str) -> Optional[str]:
    # Prefer endstopN (Ender 3 switches); fall back to btnN
    for name in (f"endstop{index}", f"btn{index}"):
        if name in section:
            return _key(section, name, default)
    return default


def binds_from_config(cfg: Dict[str, Any]) -> KeyBinds:
    section = cfg.get("controls", {})
    return KeyBinds(
        engine_on=_key(section, "engine_on", "i"),
        engine_off=_key(section, "engine_off", "i"),
        headlights=_key(section, "headlights", "l"),
        btn1=_btn_key(section, 1, "h"),
        btn2=_btn_key(section, 2, "c"),
        btn3=_btn_key(section, 3, "v"),
        enabled=bool(section.get("keyboard", True)),
    )


class CabinController:
    """Edge-detect cabin inputs and optionally emit key presses."""

    def __init__(self, binds: KeyBinds, dry_run: bool = False) -> None:
        self.binds = binds
        self.dry_run = dry_run
        self._prev: Optional[CabinInputs] = None
        self._kb = None
        if binds.enabled and not dry_run:
            try:
                from pynput.keyboard import Controller

                self._kb = Controller()
            except ImportError:
                print("pynput not installed — cabin keys logged only")
                self.dry_run = True

    def _tap(self, key_name: Optional[str], label: str) -> None:
        if not key_name:
            return
        if self.dry_run or self._kb is None:
            print(f"\n[ctrl] {label} → key '{key_name}'")
            return
        from pynput.keyboard import Key

        special = {
            "space": Key.space,
            "enter": Key.enter,
            "shift": Key.shift,
            "ctrl": Key.ctrl,
            "alt": Key.alt,
            "tab": Key.tab,
            "esc": Key.esc,
        }
        key = special.get(key_name.lower(), key_name)
        self._kb.press(key)
        self._kb.release(key)

    def handle(self, state: CabinInputs) -> None:
        prev = self._prev
        self._prev = state
        if prev is None:
            return

        if state.engine != prev.engine:
            if state.engine:
                self._tap(self.binds.engine_on, "engine ON")
            else:
                self._tap(self.binds.engine_off or self.binds.engine_on, "engine OFF")

        if state.headlights != prev.headlights:
            self._tap(self.binds.headlights, "headlights")

        if state.btn1 and not prev.btn1:
            self._tap(self.binds.btn1, "endstop1")
        if state.btn2 and not prev.btn2:
            self._tap(self.binds.btn2, "endstop2")
        if state.btn3 and not prev.btn3:
            self._tap(self.binds.btn3, "endstop3")
