import sys
import termios
import tty
import os
from bleak import BleakScanner
import asyncio
import time
import pandas as pd


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
    macdb = "./res/macdb/mac.csv"


macdf = pd.read_csv(fp.macdb, usecols=["Mac Address", "Organization Name"])  # type: ignore
macdf["Mac Address"] = macdf["Mac Address"].str.upper()
macdf.set_index("Mac Address", inplace=True)


def get_manufacturer(mac):
    oui = mac.replace(":", "")[:6]
    try:
        return macdf.loc[oui, "Organization Name"]
    except KeyError:
        return "Unknown"


def clear_screen():
    os.system("clear" if os.name != "nt" else "cls")


def init():
    clear_screen()
    draw_banner()
    found_files = 0
    if os.path.isfile(fp.banner_file):
        print(f"✅ Banner file found ({fp.banner_file})")
        found_files += 1
    else:
        print(f"{colors.RED}❌ Banner file not found ({fp.banner_file}){colors.RESET}")
    if os.path.isfile(fp.macdb):
        print(f"✅ Mac database file found ({fp.macdb})")
        found_files += 1
    else:
        print(f"{colors.RED}❌ Mac database file not found ({fp.macdb}){colors.RESET}")
    if found_files == 2:
        print(f"\nAll files {colors.GREEN}succsessfully{colors.RESET} found!")
        print(f"{colors.YELLOW}Press any key to continue…{colors.RESET}")
        getch()
        clear_screen()


def draw_banner():
    clear_screen()
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
    draw_banner()
    print(f"""
{colors.YELLOW}Please enter one of the options below:{colors.RESET}

    {colors.GREEN}[1] Continious scan {colors.RESET}

    {colors.RED}[Q] Quit{colors.RESET}
    """)
    user_choice = getch()
    if user_choice == "1":
        try:
            asyncio.run(continuous_scan())
        except KeyboardInterrupt:
            pass
    elif user_choice == "q":
        print(f"{colors.YELLOW}Quitting…{colors.RESET}")
        sys.exit()


async def continuous_scan():
    print(f"{colors.YELLOW}Starting continuous scan…{colors.RESET}")
    start_time = time.time()

    def estimate_distance(rssi):
        if rssi is None:
            return None
        elif rssi >= -60:
            return "< 1m"
        elif rssi >= -70:
            return "1-3m"
        elif rssi >= -80:
            return "3-10m"
        elif rssi >= -90:
            return "10-30m"
        elif rssi < -90:
            return "30m+"

    def detection_callback(device, advertisement_data):
        manufacturer = get_manufacturer(device.address)
        distance = estimate_distance(advertisement_data.rssi)
        # if device.name == "AirPods Pro":
        #     print(
        #         f"{device.name}, {device.address}, rssi {advertisement_data.rssi}dBm, tx_power: {advertisement_data.tx_power}, distance: {distance}"
        #     )
        # else:
        #     pass
        print(
            f"{(colors.GREEN + device.name + colors.RESET) if device.name else 'Unknown'}, "
            f"{device.address}, "
            f"rssi {advertisement_data.rssi}dBm, "
            f"manufacturer: {(colors.GREEN + manufacturer + colors.RESET) if manufacturer != 'Unknown' else manufacturer}, "
            f"distance: {distance}"
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
        time_taken = round((time.time() - start_time), 2)
        print(f"\n\nscanned for {time_taken}s")
        print(f"{colors.YELLOW}Press any key to continue…{colors.RESET}")
        getch()


def main():
    init()
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
# Path loss formula: RSSI = TxPower - 10 * n * log10(distance)
# n = 2 for free space (can be 2-4 depending on environment)
# unicode char:
# ✅
# ❌
