import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from sim_gauges.launcher import BRIDGE_DIR, GAMES, bridge_cmd, game_exe_from_config


def test_games_cover_sources():
    keys = {g[0] for g in GAMES}
    assert keys == {"forza", "beamng", "assetto", "demo"}


def test_bridge_dir_exists():
    assert (BRIDGE_DIR / "sim_gauges").is_dir()


def test_bridge_cmd_includes_game_and_port():
    cmd = bridge_cmd("forza", "COM5", cfg=Path("/tmp/nope.toml"))
    assert cmd[-4:] == ["--game", "forza", "--port", "COM5"] or (
        "--game" in cmd and "forza" in cmd and "--port" in cmd and "COM5" in cmd
    )


def test_game_exe_missing():
    assert game_exe_from_config({}, "forza") is None
    assert game_exe_from_config({"launcher": {"forza_exe": ""}}, "forza") is None
