from __future__ import annotations

import os
import sys
import subprocess
from pathlib import Path


if __name__ == "__main__":
    project_root = Path(__file__).resolve().parents[1]

    env = os.environ.copy()
    env["PYTHONPATH"] = str(project_root)

    subprocess.run(
        [
            sys.executable,
            "-m",
            "streamlit",
            "run",
            str(project_root / "app" / "ui" / "streamlit_app.py"),
        ],
        env=env,
        check=True,
    )