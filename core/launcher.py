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

    def launch_by_id(self, registry, app_id):
        app = registry.get(app_id)

        if app is None:
            raise ValueError(f"App not found: {app_id}")

        self.launch(app)