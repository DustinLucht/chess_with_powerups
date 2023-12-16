@echo off

REM Virtuelle Umgebung erstellen
python -m venv venv

set original_dir=%CD%
set venv_root_dir="venv"

cd %venv_root_dir%

REM Virtuelle Umgebung aktivieren
call Scripts\activate.bat

pip install -r "%original_dir%\requirements.txt"

call Scripts\deactivate.bat
REM Beende die virtuelle Umgebung

cd %original_dir%

REM Starte das Spiel
call venv\Scripts\python.exe main.py
