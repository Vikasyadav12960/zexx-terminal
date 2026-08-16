from core.command import CommandEngine
from core.commands import VERSION, register_builtin_commands


def main():
    engine = CommandEngine()

    register_builtin_commands(engine)

    print("╔══════════════════════════════════╗")
    print("║          ZEXX TERMINAL           ║")
    print(f"║       Retro Terminal v{VERSION}      ║")
    print("╚══════════════════════════════════╝")

    while True:
        try:
            user_input = input("ZEXX > ").strip()

            if not user_input:
                continue

            parts = user_input.split()
            command_name = parts[0]
            args = parts[1:]

            command = engine.get_command(command_name)

            if command is None:
                print(f"Unknown command: {command_name}")
                continue

            result = command.execute(args)

            if result:
                print(result)

            if command.exits:
                break

        except KeyboardInterrupt:
            print("\nGoodbye.")
            break

        except EOFError:
            print("\nGoodbye.")
            break


if __name__ == "__main__":
    main()