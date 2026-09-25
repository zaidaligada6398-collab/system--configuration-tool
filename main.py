import ctypes
import os
import platform
import shutil


def format_size(bytes_size, suffix="B"):
    factor = 1024
    for unit in ["", "K", "M", "G", "T"]:
        if bytes_size < factor:
            return f"{bytes_size:.2f} {unit}{suffix}"
        bytes_size /= factor
    return f"{bytes_size:.2f} P{suffix}"


def get_total_ram():
    """Extracts total system RAM across Windows, Linux, and macOS using built-in libraries."""
    if hasattr(os, "sysconf"):
        try:
            pages = os.sysconf("SC_PHYS_PAGES")
            page_size = os.sysconf("SC_PAGE_SIZE")
            return pages * page_size
        except (ValueError, OSError):
            pass

    if platform.system() == "Windows":

        class MEMORYSTATUSEX(ctypes.Structure):
            _fields_ = [
                ("dwLength", ctypes.c_ulong),
                ("dwMemoryLoad", ctypes.c_ulong),
                ("ullTotalPhys", ctypes.c_ulonglong),
                ("ullAvailPhys", ctypes.c_ulonglong),
                ("ullTotalPageFile", ctypes.c_ulonglong),
                ("ullAvailPageFile", ctypes.c_ulonglong),
                ("ullTotalVirtual", ctypes.c_ulonglong),
                ("ullAvailVirtual", ctypes.c_ulonglong),
                ("sullAvailExtendedVirtual", ctypes.c_ulonglong),
            ]

        stat = MEMORYSTATUSEX()
        stat.dwLength = ctypes.sizeof(MEMORYSTATUSEX)
        if ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(stat)):
            return stat.ullTotalPhys

    return None


def get_system_specs():
    print("=" * 50)
    print("            SYSTEM INFORMATION")
    print("=" * 50)

    # 1. Operating System
    print("\n[Operating System]")
    print(f"OS: {platform.system()}")
    print(f"Release: {platform.release()}")
    print(f"Version: {platform.version()}")
    print(f"Architecture: {platform.machine()}")

    # 2. CPU
    print("\n[CPU]")
    print(f"Processor: {platform.processor()}")
    print(f"CPU Threads/Cores: {os.cpu_count()}")

    # 3. RAM
    print("\n[Memory / RAM]")
    total_ram = get_total_ram()
    if total_ram:
        print(f"Total RAM: {format_size(total_ram)}")
    else:
        print("RAM information not available")

    # 4. Disk Space
    print("\n[Disk Space]")
    try:
        root_dir = "C:\\" if platform.system() == "Windows" else "/"
        disk = shutil.disk_usage(root_dir)

        print(f"Root Drive: {root_dir}")
        print(f"Total Space: {format_size(disk.total)}")
        print(f"Used Space:  {format_size(disk.used)}")
        print(f"Free Space:  {format_size(disk.free)}")
    except Exception as e:
        print(f"Disk information not available: {e}")

    print("\n" + "=" * 50)


if __name__ == "__main__":
    get_system_specs()
