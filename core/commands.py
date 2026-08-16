import os

from core.command import Command, CommandEngine


VERSION = "0.1.0"


def help_command(engine: CommandEngine, args: list[str]) -> str:
    lines = ["Available commands:", ""]

    for command in engine.list_commands():
        lines.append(
            f"  {command.name:<10} {command.description}"
        )

    return "\n".join(lines)


def version_command(args: list[str]) -> str:
    return f"ZEXX Terminal v{VERSION}"


def clear_command(args: list[str]) -> str:
    os.system("cls" if os.name == "nt" else "clear")
    return ""


def exit_command(args: list[str]) -> str:
    return "Goodbye."


def register_builtin_commands(engine: CommandEngine) -> None:
    engine.register(
        Command(
            "help",
            "Show available commands",
            lambda args: help_command(engine, args),
        )
    )

    engine.register(
        Command(
            "version",
            "Show ZEXX version",
            version_command,
        )
    )

    engine.register(
        Command(
            "clear",
            "Clear the terminal",
            clear_command,
        )
    )

    engine.register(
        Command(
            "exit",
            "Exit ZEXX",
            exit_command,
            exits=True,
        )
    )