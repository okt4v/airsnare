import sys
import termios
import tty
import os
from bleak import BleakScanner
import asyncio


class colors:
    # Formatting codes
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    UNDERLINE = "\033[4m"
    INVERSE = "\033[7m"
    HIDDEN = "\033[8m"
    STRIKETHROUGH = "\033[9m"

    # Foreground colors
    BLACK = "\033[30m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"

    # Bright foreground colors
    BRIGHT_BLACK = "\033[90m"
    BRIGHT_RED = "\033[91m"
    BRIGHT_GREEN = "\033[92m"
    BRIGHT_YELLOW = "\033[93m"
    BRIGHT_BLUE = "\033[94m"
    BRIGHT_MAGENTA = "\033[95m"
    BRIGHT_CYAN = "\033[96m"
    BRIGHT_WHITE = "\033[97m"

    # Background colors
    BG_BLACK = "\033[40m"
    BG_RED = "\033[41m"
    BG_GREEN = "\033[42m"
    BG_YELLOW = "\033[43m"
    BG_BLUE = "\033[44m"
    BG_MAGENTA = "\033[45m"
    BG_CYAN = "\033[46m"
    BG_WHITE = "\033[47m"

    # Bright background colors
    BRIGHT_BG_BLACK = "\033[100m"
    BRIGHT_BG_RED = "\033[101m"
    BRIGHT_BG_GREEN = "\033[102m"
    BRIGHT_BG_YELLOW = "\033[103m"
    BRIGHT_BG_BLUE = "\033[104m"
    BRIGHT_BG_MAGENTA = "\033[105m"
    BRIGHT_BG_CYAN = "\033[106m"
    BRIGHT_BG_WHITE = "\033[107m"


class fp:
    banner_file = "./res/program/banner.txt"


def clear_screen():
    os.system("clear" if os.name != "nt" else "cls")


def draw_banner():
    try:
        with open(fp.banner_file, "r") as file:
            banner = file.read()
            banner = (
                banner.replace("{colors.YELLOW}", colors.YELLOW)
                .replace("{colors.RESET}", colors.RESET)
                .replace("{colors.MAGENTA}", colors.MAGENTA)
                .replace("{colors.BOLD}", colors.BOLD)
            )
            print(banner)
    except FileNotFoundError:
        print(f"The file that stores the banner ({fp.banner_file}) was not found.")


def getch():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        ch = sys.stdin.read(1).lower()
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch


def main_screen():
    clear_screen()
    draw_banner()
    print("""
[1] Continious scan

[Q] Exit
    """)  # improve this later
    tmpgetch = getch()
    if tmpgetch == "1":
        try:
            asyncio.run(continuous_scan())
        except KeyboardInterrupt:
            pass
    elif tmpgetch == "q":
        sys.exit()


async def continuous_scan():
    def detection_callback(device, advertisement_data):
        print(
            f"{device.name} {device.address} {advertisement_data.rssi}dBm  {advertisement_data.tx_power}"
        )

    scanner = BleakScanner(detection_callback=detection_callback)

    try:
        await scanner.start()
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        print("Stopping")
    finally:
        await scanner.stop()


def main():
    draw_banner()
    try:
        while True:
            main_screen()
    except KeyboardInterrupt:
        print("\nExiting...")
        sys.exit()


if __name__ == "__main__":
    main()


# NOTES
# {advertisement_data.local_name} --> this is unused but may be usefull in the future so that if a device doesnt have a device.name then one can check if it has this
#
#
