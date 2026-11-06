@echo off
cd /d "%~dp0"
python -m sim_gauges.launcher
if errorlevel 1 pause
