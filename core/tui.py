from textual.app import App, ComposeResult
from textual.containers import Vertical, Horizontal
from textual.widgets import Header, Footer, Static, ListView, ListItem, Label
from textual.binding import Binding

from core.app_discovery import AppDiscovery
from core.launcher import AppLauncher


class ZexxTerminal(App):
    TITLE = "ZEXX TERMINAL"
    SUB_TITLE = "v0.2"

    CSS = """
    Screen {
        background: #050505;
        color: #00ff66;
    }

    Header {
        background: #001a0a;
        color: #00ff66;
    }

    Footer {
        background: #001a0a;
        color: #00ff66;
    }

    #main {
        height: 1fr;
        padding: 1;
    }

    #title {
        height: 3;
        content-align: center middle;
        border: double #00ff66;
        color: #00ff66;
        text-style: bold;
    }

    #apps {
        width: 1fr;
        height: 1fr;
        margin-top: 1;
        border: round #00ff66;
        padding: 1;
    }

    #terminal {
        height: 5;
        margin-top: 1;
        border: round #00ff66;
        padding: 1;
    }

    ListView {
        background: #050505;
    }

    ListItem {
        height: 3;
        border-bottom: solid #003311;
        padding: 0 1;
    }

    ListItem:hover {
        background: #003311;
    }

    ListItem.-selected {
        background: #004d1a;
        color: #ffffff;
        text-style: bold;
    }

    .app-name {
        color: #00ff66;
        text-style: bold;
    }

    .app-category {
        color: #888888;
    }
    """

    BINDINGS = [
        Binding("q", "quit", "Quit"),
        Binding("enter", "launch_selected", "Launch"),
        Binding("r", "refresh", "Refresh"),
    ]

    def __init__(self):
        super().__init__()

        self.discovery = AppDiscovery()
        self.launcher = AppLauncher()

        self.apps = []

    def compose(self) -> ComposeResult:
        yield Header()

        with Vertical(id="main"):

            yield Static(
                "╔══════════════════════════════════════════════════════╗\n"
                "║                    Z E X X                           ║\n"
                "║                 TERMINAL v0.2                        ║\n"
                "╚══════════════════════════════════════════════════════╝",
                id="title",
            )

            yield Static(
                "  APPLICATIONS",
                id="apps-header",
            )

            yield ListView(id="apps")

            yield Static(
                "zexx > READY\n"
                "ENTER  Launch    R  Refresh    Q  Quit",
                id="terminal",
            )

        yield Footer()

    def on_mount(self) -> None:
        self.refresh_apps()

    def refresh_apps(self) -> None:
        self.apps = self.discovery.discover()

        app_list = self.query_one("#apps", ListView)

        app_list.clear()

        for app in self.apps:
            item = ListItem(
                Label(
                    f"[{app['category'].upper()}]  "
                    f"{app['name']}  "
                    f"({app['id']})",
                    classes="app-name",
                )
            )

            app_list.append(item)

        if self.apps:
            app_list.index = 0

    def action_refresh(self) -> None:
        self.refresh_apps()

        terminal = self.query_one("#terminal", Static)

        terminal.update(
            "zexx > APPLICATIONS REFRESHED\n"
            "ENTER  Launch    R  Refresh    Q  Quit"
        )

    def action_launch_selected(self) -> None:
        if not self.apps:
            return

        app_list = self.query_one("#apps", ListView)

        if app_list.index is None:
            return

        index = app_list.index

        if index >= len(self.apps):
            return

        app = self.apps[index]

        terminal = self.query_one("#terminal", Static)

        terminal.update(
            f"zexx > Launching {app['name']}...\n"
            "The application will open separately."
        )

        self.launcher.launch(app)


if __name__ == "__main__":
    ZexxTerminal().run()