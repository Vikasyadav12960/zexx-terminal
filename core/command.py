class Command:
    """Represents a single ZEXX command."""

    def __init__(self, name, description, handler, exits=False):
        self.name = name
        self.description = description
        self.handler = handler
        self.exits = exits

    def execute(self, args):
        return self.handler(args)


class CommandEngine:
    """Stores and executes ZEXX commands."""

    def __init__(self):
        self.commands = {}

    def register(self, command):
        self.commands[command.name] = command

    def execute(self, name, args=None):
        if name not in self.commands:
            return None

        return self.commands[name].execute(args or [])

    def get_command(self, name):
        return self.commands.get(name)

    def list_commands(self):
        return self.commands.values()