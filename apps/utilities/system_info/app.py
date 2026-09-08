import os
import platform


def main():
    print()
    print("+-----------------------------------+")
    print("|         ZEXX SYSTEM INFO          |")
    print("+-----------------------------------+")
    print(f"| OS:       {platform.system():<21}|")
    print(f"| Version:  {platform.version()[:21]:<21}|")
    print(f"| Machine:  {platform.machine():<21}|")
    print(f"| CPU:      {os.cpu_count():<21}|")
    print("+-----------------------------------+")
    print()


if __name__ == "__main__":
    main()