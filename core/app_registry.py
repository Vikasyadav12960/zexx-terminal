class AppRegistry:
    def __init__(self, apps=None):
        self._apps = {}

        if apps:
            self.register_all(apps)

    def register(self, app):
        app_id = app["id"]

        if app_id in self._apps:
            raise ValueError(f"Duplicate app id: {app_id}")

        self._apps[app_id] = app

    def register_all(self, apps):
        for app in apps:
            self.register(app)

    def get(self, app_id):
        return self._apps.get(app_id)

    def all(self):
        return list(self._apps.values())

    def by_category(self, category):
        return [
            app
            for app in self._apps.values()
            if app["category"] == category
        ]

    def exists(self, app_id):
        return app_id in self._apps

    def __len__(self):
        return len(self._apps)