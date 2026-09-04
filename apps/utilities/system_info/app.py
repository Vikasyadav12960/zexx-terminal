import platform
import os


def main():
    print()
    print("╔══════════════════════════════╗")
    print("║        ZEXX SYSTEM INFO      ║")
    print("╠══════════════════════════════╣")
    print(f"║ OS:       {platform.system():<17}║")
    print(f"║ Version:  {platform.version()[:15]:<17}║")
    print(f"║ Machine:  {platform.machine():<17}║")
    print(f"║ CPU:      {os.cpu_count():<17}║")
    print("╚══════════════════════════════╝")
    print()


if __name__ == "__main__":
    main()