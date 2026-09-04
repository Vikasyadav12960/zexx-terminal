from core.app_discovery import AppDiscovery
from core.launcher import AppLauncher
from core.tui import ZexxTerminal

class ZexxTerminal:
    def __init__(self):
        self.discovery = AppDiscovery()
        self.launcher = AppLauncher()

    # --------------------------------------------------
    # Display all discovered applications
    # --------------------------------------------------
    def show_apps(self):
        apps = self.discovery.discover()

        if not apps:
            print("\nNo ZEXX apps found.\n")
            return

        print("\n=== ZEXX APPS ===")

        for app in apps:
            print(
                f"{app['id']:<20}"
                f"{app['name']:<20}"
                f"[{app['category']}]"
            )

        print()

    # --------------------------------------------------
    # Find an application by ID or name
    # --------------------------------------------------
    def find_app(self, target):
        target = target.strip().strip('"').strip("'")

        # Exact ID
        app = self.discovery.find(target)

        if app:
            return app

        # Exact name
        for candidate in self.discovery.discover():
            if candidate["name"].lower() == target.lower():
                return candidate

        # ID with spaces converted to underscores
        normalized = target.lower().replace(" ", "_")

        for candidate in self.discovery.discover():
            if candidate["id"].lower() == normalized:
                return candidate

        return None

    # --------------------------------------------------
    # Launch an application
    # --------------------------------------------------
    def launch_app(self, target):
        if not target:
            print("Usage: launch <app>")
            return

        app = self.find_app(target)

        if not app:
            print(f"App not found: {target}")
            print("Use 'apps' to see available applications.")
            return

        print(f"\nLaunching {app['name']}...\n")

        try:
            self.launcher.launch(app)
        except FileNotFoundError as error:
            print(f"Launch error: {error}")
        except Exception as error:
            print(f"Unexpected launch error: {error}")

    # --------------------------------------------------
    # Help
    # --------------------------------------------------
    def show_help(self):
        print("""
ZEXX COMMANDS
────────────────────────────────────

apps
    List all discovered applications.

launch <app>
    Launch an application.

help
    Show this help message.

clear
    Clear the terminal screen.

exit
    Exit ZEXX.

quit
    Exit ZEXX.

EXAMPLES
────────────────────────────────────

launch system_info
launch system info
launch "System Info"
""")

    # --------------------------------------------------
    # Clear terminal
    # --------------------------------------------------
    def clear_screen(self):
        import os

        os.system("cls" if os.name == "nt" else "clear")

    # --------------------------------------------------
    # Process commands
    # --------------------------------------------------
    def process_command(self, command):
        command = command.strip()

        if not command:
            return True

        # Split only once so app names can contain spaces
        parts = command.split(maxsplit=1)

        cmd = parts[0].lower()

        argument = ""

        if len(parts) > 1:
            argument = parts[1].strip()

        # ----------------------------------------------
        # APPS
        # ----------------------------------------------
        if cmd == "apps":
            self.show_apps()

        # ----------------------------------------------
        # LAUNCH
        # ----------------------------------------------
        elif cmd in ("launch", "run", "open"):
            self.launch_app(argument)

        # ----------------------------------------------
        # HELP
        # ----------------------------------------------
        elif cmd == "help":
            self.show_help()

        # ----------------------------------------------
        # CLEAR
        # ----------------------------------------------
        elif cmd == "clear":
            self.clear_screen()

        # ----------------------------------------------
        # EXIT
        # ----------------------------------------------
        elif cmd in ("exit", "quit"):
            print("\nShutting down ZEXX...")
            return False

        # ----------------------------------------------
        # UNKNOWN COMMAND
        # ----------------------------------------------
        else:
            print(
                f"Unknown command: {cmd}\n"
                "Type 'help' to see available commands."
            )

        return True

    # --------------------------------------------------
    # Start ZEXX
    # --------------------------------------------------
    def run(self):
        print("""
╔════════════════════════════════╗
║          Z E X X               ║
║        TERMINAL v0.2           ║
╚════════════════════════════════╝
""")

        print("Type 'help' for available commands.\n")

        while True:
            try:
                command = input("zexx > ")

                if not self.process_command(command):
                    break

            except KeyboardInterrupt:
                print("\n\nShutting down ZEXX...")
                break

            except EOFError:
                print("\n\nShutting down ZEXX...")
                break


# ------------------------------------------------------
# Entry point
# ------------------------------------------------------
if __name__ == "__main__":
    terminal = ZexxTerminal()
    terminal.run()

if __name__ == "__main__":
    ZexxTerminal().run()