"""Main app: click a game to start the telemetry bridge (and optionally the game)."""

from __future__ import annotations

import os
import queue
import subprocess
import sys
import threading
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

BRIDGE_DIR = Path(__file__).resolve().parents[1]
GAMES: List[Tuple[str, str, str]] = [
    ("forza", "Forza", "Data Out UDP → gauges"),
    ("beamng", "BeamNG", "OutGauge UDP → gauges"),
    ("assetto", "Assetto Corsa", "Shared memory → gauges"),
    ("demo", "Demo", "Sweep needles / LEDs (no game)"),
]


def _load_toml(path: Path) -> Dict[str, Any]:
    try:
        import tomllib
    except ModuleNotFoundError:
        import tomli as tomllib  # type: ignore
    with path.open("rb") as f:
        return tomllib.load(f)


def config_path() -> Path:
    preferred = BRIDGE_DIR / "config.toml"
    if preferred.exists():
        return preferred
    return BRIDGE_DIR / "config.example.toml"


def list_ports() -> List[str]:
    try:
        from serial.tools import list_ports

        return [p.device for p in list_ports.comports()]
    except Exception:
        return []


def bridge_cmd(game: str, port: str, cfg: Optional[Path] = None) -> List[str]:
    path = cfg if cfg is not None else config_path()
    cmd = [sys.executable, "-m", "sim_gauges", "--game", game]
    if port:
        cmd.extend(["--port", port])
    if path.exists():
        cmd.extend(["--config", str(path)])
    return cmd


def game_exe_from_config(cfg: Dict[str, Any], game: str) -> Optional[Path]:
    section = cfg.get("launcher", {})
    raw = section.get(f"{game}_exe") or section.get(game)
    if not raw:
        return None
    path = Path(str(raw)).expanduser()
    return path if path.is_file() else None


def _build_app():
    import tkinter as tk
    from tkinter import messagebox, ttk

    class LauncherApp(tk.Tk):
        def __init__(self) -> None:
            super().__init__()
            self.title("SimRacing Gauges")
            self.minsize(520, 480)
            self.configure(bg="#1a1d21")

            self._cfg = self._read_config()
            self._proc: Optional[subprocess.Popen] = None
            self._game_proc: Optional[subprocess.Popen] = None
            self._active_game: Optional[str] = None
            self._log_q: queue.Queue[str] = queue.Queue()

            self._build_style()
            self._build_ui()
            self._refresh_ports()
            self.after(100, self._drain_log)
            self.protocol("WM_DELETE_WINDOW", self._on_close)

        def _read_config(self) -> Dict[str, Any]:
            path = config_path()
            if not path.exists():
                return {}
            try:
                return _load_toml(path)
            except Exception as exc:
                messagebox.showwarning("Config", f"Could not read {path.name}: {exc}")
                return {}

        def _build_style(self) -> None:
            style = ttk.Style(self)
            try:
                style.theme_use("clam")
            except tk.TclError:
                pass
            style.configure(".", background="#1a1d21", foreground="#e8eaed")
            style.configure("TFrame", background="#1a1d21")
            style.configure(
                "TLabel", background="#1a1d21", foreground="#e8eaed", font=("Segoe UI", 10)
            )
            style.configure(
                "Title.TLabel", font=("Segoe UI Semibold", 18), foreground="#f0f2f5"
            )
            style.configure("Sub.TLabel", foreground="#9aa0a6", font=("Segoe UI", 9))
            style.configure("Status.TLabel", font=("Consolas", 10), foreground="#8ab4f8")
            style.configure("TButton", font=("Segoe UI", 10), padding=8)
            style.configure("Game.TButton", font=("Segoe UI Semibold", 12), padding=(16, 14))
            style.configure("TCheckbutton", background="#1a1d21", foreground="#e8eaed")
            style.configure("TCombobox", padding=4)

        def _build_ui(self) -> None:
            root = ttk.Frame(self, padding=16)
            root.pack(fill=tk.BOTH, expand=True)

            ttk.Label(root, text="SimRacing Gauges", style="Title.TLabel").pack(anchor=tk.W)
            ttk.Label(
                root,
                text="Pick a game — starts the Arduino bridge. Optional: launch the game exe too.",
                style="Sub.TLabel",
            ).pack(anchor=tk.W, pady=(4, 14))

            bar = ttk.Frame(root)
            bar.pack(fill=tk.X, pady=(0, 12))
            ttk.Label(bar, text="Serial port").pack(side=tk.LEFT)
            self.port_var = tk.StringVar(
                value=str(self._cfg.get("serial", {}).get("port", ""))
            )
            self.port_box = ttk.Combobox(bar, textvariable=self.port_var, width=18)
            self.port_box.pack(side=tk.LEFT, padx=(8, 6))
            ttk.Button(bar, text="Refresh", command=self._refresh_ports).pack(side=tk.LEFT)

            self.launch_game_var = tk.BooleanVar(value=True)
            ttk.Checkbutton(
                bar,
                text="Also launch game exe",
                variable=self.launch_game_var,
            ).pack(side=tk.RIGHT)

            grid = ttk.Frame(root)
            grid.pack(fill=tk.X, pady=(0, 12))
            for i, (key, title, blurb) in enumerate(GAMES):
                cell = ttk.Frame(grid)
                cell.grid(row=i // 2, column=i % 2, sticky="nsew", padx=4, pady=4)
                ttk.Button(
                    cell,
                    text=title,
                    style="Game.TButton",
                    command=lambda k=key: self._start_game(k),
                ).pack(fill=tk.X)
                ttk.Label(cell, text=blurb, style="Sub.TLabel").pack(
                    anchor=tk.W, pady=(4, 0)
                )
            grid.columnconfigure(0, weight=1)
            grid.columnconfigure(1, weight=1)

            row = ttk.Frame(root)
            row.pack(fill=tk.X, pady=(0, 8))
            self.status_var = tk.StringVar(value="Idle")
            ttk.Label(row, textvariable=self.status_var, style="Status.TLabel").pack(
                side=tk.LEFT
            )
            self.stop_btn = ttk.Button(
                row, text="Stop", command=self._stop, state=tk.DISABLED
            )
            self.stop_btn.pack(side=tk.RIGHT)

            log_frame = ttk.Frame(root)
            log_frame.pack(fill=tk.BOTH, expand=True)
            self.log = tk.Text(
                log_frame,
                height=14,
                bg="#0f1114",
                fg="#c5c8ce",
                insertbackground="#e8eaed",
                relief=tk.FLAT,
                font=("Consolas", 9),
                wrap=tk.WORD,
            )
            scroll = ttk.Scrollbar(log_frame, command=self.log.yview)
            self.log.configure(yscrollcommand=scroll.set)
            self.log.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            scroll.pack(side=tk.RIGHT, fill=tk.Y)

        def _refresh_ports(self) -> None:
            ports = list_ports()
            current = self.port_var.get().strip()
            values = list(ports)
            if current and current not in values:
                values.insert(0, current)
            if not values:
                values = ["COM3"]
            self.port_box["values"] = values
            if not self.port_var.get():
                self.port_var.set(values[0])

        def _append_log(self, text: str) -> None:
            self.log.insert(tk.END, text)
            self.log.see(tk.END)

        def _drain_log(self) -> None:
            try:
                while True:
                    self._append_log(self._log_q.get_nowait())
            except queue.Empty:
                pass
            self.after(100, self._drain_log)

        def _start_game(self, game: str) -> None:
            if self._proc and self._proc.poll() is None:
                if not messagebox.askyesno(
                    "Already running",
                    f"Stop {self._active_game} and start {game}?",
                ):
                    return
                self._stop()

            port = self.port_var.get().strip()
            if not port:
                if not messagebox.askyesno(
                    "No serial port",
                    "No COM port set. Start bridge anyway?",
                ):
                    return

            if self.launch_game_var.get() and game != "demo":
                exe = game_exe_from_config(self._cfg, game)
                if exe is not None:
                    try:
                        self._game_proc = subprocess.Popen(
                            [str(exe)],
                            cwd=str(exe.parent),
                            close_fds=True,
                        )
                        self._log_q.put(f"Launched game: {exe}\n")
                    except OSError as exc:
                        messagebox.showerror("Game launch failed", str(exc))
                else:
                    self._log_q.put(
                        f"(No launcher.{game}_exe in config — bridge only)\n"
                    )

            cmd = bridge_cmd(game, port)
            self._log_q.put(f"$ {' '.join(cmd)}\n")
            try:
                creationflags = 0
                if sys.platform == "win32":
                    creationflags = subprocess.CREATE_NEW_PROCESS_GROUP  # type: ignore[attr-defined]
                self._proc = subprocess.Popen(
                    cmd,
                    cwd=str(BRIDGE_DIR),
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True,
                    bufsize=1,
                    creationflags=creationflags,
                    env={**os.environ, "PYTHONUNBUFFERED": "1"},
                )
            except OSError as exc:
                messagebox.showerror("Bridge failed", str(exc))
                return

            self._active_game = game
            self.status_var.set(f"Running: {game}")
            self.stop_btn.configure(state=tk.NORMAL)
            threading.Thread(target=self._read_stdout, daemon=True).start()
            self.after(400, self._watch_proc)

        def _read_stdout(self) -> None:
            proc = self._proc
            if proc is None or proc.stdout is None:
                return
            for line in proc.stdout:
                self._log_q.put(line if line.endswith("\n") else line + "\n")

        def _watch_proc(self) -> None:
            if self._proc is None:
                return
            code = self._proc.poll()
            if code is None:
                self.after(400, self._watch_proc)
                return
            self._log_q.put(f"\n[bridge exited {code}]\n")
            self.status_var.set("Idle")
            self.stop_btn.configure(state=tk.DISABLED)
            self._proc = None
            self._active_game = None

        def _stop(self) -> None:
            proc = self._proc
            if proc and proc.poll() is None:
                self._log_q.put("Stopping bridge…\n")
                try:
                    proc.terminate()
                    try:
                        proc.wait(timeout=3)
                    except subprocess.TimeoutExpired:
                        proc.kill()
                except OSError:
                    pass
            self._proc = None
            self._active_game = None
            self.status_var.set("Idle")
            self.stop_btn.configure(state=tk.DISABLED)

        def _on_close(self) -> None:
            self._stop()
            self.destroy()

    return LauncherApp


def main() -> int:
    if sys.platform.startswith("linux") and not os.environ.get("DISPLAY"):
        print(
            "No display — run on your gaming PC:\n"
            "  python -m sim_gauges.launcher\n"
            "or double-click bridge\\Launch Gauges.bat",
            file=sys.stderr,
        )
        return 1
    try:
        LauncherApp = _build_app()
    except ModuleNotFoundError as exc:
        print(f"GUI unavailable ({exc}). Install a Python build with tkinter.", file=sys.stderr)
        return 1
    app = LauncherApp()
    app.mainloop()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
