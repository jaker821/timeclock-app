import os
import shutil
import sys
from pathlib import Path

APP_NAME = "MyTimeClock"

def get_appdata_base() -> str:
    """
    Returns the base AppData path for this app:
    C:/Users/<User>/AppData/Roaming/MyTimeClock
    """
    appdata = Path(os.getenv("APPDATA"))
    base = appdata / APP_NAME
    base.mkdir(parents=True, exist_ok=True)
    return str(base)

def get_appdata_path(subfolder: str = "") -> str:
    """
    Returns a path inside AppData (creates folder if missing)
    Example: get_appdata_path("backups")
    """
    base = Path(get_appdata_base())
    target = base / subfolder if subfolder else base
    if subfolder and not target.exists():
        target.mkdir(parents=True, exist_ok=True)
    return str(target)

def get_resource_path(filename: str) -> str:
    """
    Returns the full path to a resource in AppData/resources.
    Copies from bundled resources if first run.
    """
    resources_dir = Path(get_appdata_path("resources"))
    target_file = resources_dir / filename

    if not target_file.exists():
        # PyInstaller bundled folder
        if hasattr(sys, "_MEIPASS"):
            bundle_dir = Path(sys._MEIPASS) / "resources"
        else:
            bundle_dir = Path(__file__).parent / "resources"

        source_file = bundle_dir / filename
        if source_file.exists():
            shutil.copy2(source_file, target_file)
        else:
            print(f"Warning: resource {filename} not found in bundle.")

    return str(target_file)

def get_db_path() -> str:
    """
    Returns the full path to the main database in AppData.
    """
    base = Path(get_appdata_base())
    db_file = base / "timeclock.db"
    return str(db_file)
