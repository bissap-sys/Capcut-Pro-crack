import os
import sys
import psutil
import shutil
from pathlib import Path
import ctypes
import time
import itertools
import threading
from colorama import init, Fore, Style

init(autoreset=False)

DLL_FILENAME = "VECreator.dll"
done = False  

def print_banner():
    purple = Fore.MAGENTA + Style.BRIGHT
    reset = Style.RESET_ALL
    print(purple + "=" * 50)
    print("        🔧 CapCut Pro Patcher by B2oba 🔧         ")
    print("=" * 50 + "\n" + reset)


def animate_crack():
    for c in itertools.cycle(['.', '..', '...', '....']):
        if done:
            break
        sys.stdout.write(f'\rCrack in progress{c}   ')
        sys.stdout.flush()
        time.sleep(0.5)
    sys.stdout.write('\r✅ Crack complete. Relaunch CapCut.\n')


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


def replace_binary(data, from_str, to_str):
    from_bytes = b"\0" + from_str.encode() + b"\0"
    to_bytes = b"\0" + to_str.encode() + b"\0"
    data_list = list(data)
    pos = 0
    while True:
        try:
            pos = data_list.index(from_bytes[0], pos)
        except ValueError:
            break
        if data_list[pos:pos + len(from_bytes)] == list(from_bytes):
            data_list[pos:pos + len(from_bytes)] = list(to_bytes)
            pos += len(to_bytes)
        else:
            pos += 1
    return bytes(data_list)


def patch_dll(dll_path, mode):
    if not dll_path.exists():
        sys.exit(1)
    original = dll_path.read_bytes()
    on_path = dll_path.with_name(dll_path.name + "_On.dll")
    off_path = dll_path.with_name(dll_path.name + "_Off.dll")
    if not (on_path.exists() and off_path.exists()):
        on_path.write_bytes(replace_binary(original, "vip_entrance", "pro_fortnite"))
        off_path.write_bytes(replace_binary(original, "pro_fortnite", "vip_entrance"))
    selected = on_path if mode == "on" else off_path
    shutil.copy2(selected, dll_path)
    return True


def close_capcut():
    for proc in psutil.process_iter(['name']):
        if proc.info['name'] and proc.info['name'].lower() == "capcut.exe":
            try:
                proc.terminate()
                proc.wait(timeout=5)
            except:
                pass


def remove_watermark(exe_dir):
    watermark_path = exe_dir / "Resources" / "watermark"
    if watermark_path.exists():
        try:
            shutil.rmtree(watermark_path)
        except:
            pass


def find_dll(start_path: Path, target_filename: str):
    for root, dirs, files in os.walk(start_path):
        if target_filename in files:
            return Path(root) / target_filename
    return None


def main():
    print_banner()

    choice = input("Do you want to crack CapCut? (y/n): ").strip().lower()
    if choice != 'y':
        print("Operation cancelled.")
        return

    if not is_admin():
        print("Error: Please run this script as administrator.")
        sys.exit(1)

    dll_path = find_dll(Path("C:/Users"), DLL_FILENAME)
    if not dll_path:
        print("Error: VECreator.dll not found.")
        sys.exit(1)

    exe_dir = dll_path.parent
    close_capcut()
    remove_watermark(exe_dir)

    global done
    t = threading.Thread(target=animate_crack)
    t.start()

    patch_dll(dll_path, "on")

    time.sleep(3)
    done = True
    t.join()


if __name__ == "__main__":
    main()
