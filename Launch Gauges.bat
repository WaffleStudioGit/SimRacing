@echo off
cd /d "%~dp0bridge"
python -m sim_gauges.launcher
if errorlevel 1 pause
