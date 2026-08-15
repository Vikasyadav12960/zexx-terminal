from core.command import Command, CommandEngine


def main():
    engine = CommandEngine()

    def help_command(args):
        return "ZEXX commands: help, exit"

    def exit_command(args):
        return "Goodbye."

    engine.register(
        Command(
            "help",
            "Show available commands",
            help_command,
        )
    )

    engine.register(
        Command(
            "exit",
            "Exit ZEXX",
            exit_command,
        )
    )

    print("╔══════════════════════════════════╗")
    print("║          ZEXX TERMINAL           ║")
    print("║       Retro Terminal v0.1.0      ║")
    print("╚══════════════════════════════════╝")

    while True:
        try:
            user_input = input("ZEXX > ").strip()

            if not user_input:
                continue

            parts = user_input.split()
            command_name = parts[0]
            args = parts[1:]

            if command_name == "exit":
                print(engine.execute(command_name, args))
                break

            print(engine.execute(command_name, args))

        except KeyboardInterrupt:
            print("\nGoodbye.")
            break
        except EOFError:
            print("\nGoodbye.")
            break


if __name__ == "__main__":
    main()