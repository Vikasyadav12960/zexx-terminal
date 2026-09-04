from pathlib import Path
import json


class AppDiscovery:
    def __init__(self, apps_dir="apps"):
        self.apps_dir = Path(apps_dir)

    def discover(self):
        apps = []

        if not self.apps_dir.exists():
            return apps

        for manifest in self.apps_dir.rglob("manifest.json"):
            try:
                data = json.loads(manifest.read_text(encoding="utf-8"))

                required = {"name", "id", "category", "entry"}
                if not required.issubset(data):
                    continue

                apps.append({
                    "name": data["name"],
                    "id": data["id"],
                    "category": data["category"],
                    "entry": manifest.parent / data["entry"],
                    "path": manifest.parent,
                })

            except (json.JSONDecodeError, OSError):
                continue

        return apps

    def find(self, app_id):
        for app in self.discover():
            if app["id"] == app_id:
                return app

        return None