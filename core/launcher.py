import subprocess
import sys


class AppLauncher:
    def launch(self, app):
        entry = app["entry"]

        if not entry.exists():
            raise FileNotFoundError(f"App entry not found: {entry}")

        subprocess.run(
            [sys.executable, str(entry)],
            check=False
        )