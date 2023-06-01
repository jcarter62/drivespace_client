import argparse
import win32api, win32file, win32con
import requests

def get_drives() -> list:
    result = []
    drives = win32api.GetLogicalDriveStrings()
    drives = drives.split('\000')[:-1]
    for drive in drives:
        drivetype = get_drive_type(drive)
        driveinfo = get_drive_space(drive)
        result.append({
            "drive": drive,
            "type": drivetype,
            "info": driveinfo
        })
    return result


def get_drive_space(drive: str) -> dict:
    drivenums = win32api.GetDiskFreeSpaceEx(drive)
    free = bytes_to_gb(drivenums[0])
    total = bytes_to_gb(drivenums[1])
    used = total - free


    return {
        "name": get_drive_name(drive),
        "serial": get_drive_serial(drive),
        "filesystem": get_drive_filesystem(drive),
        "free": free,
        "total": total,
        "used": used,
        "freepct": round(free / total * 100, 2),
        "usedpct": round(used / total * 100, 2),
    }

def bytes_to_gb(bytes: int) -> float:
    gb = bytes / 1024 / 1024 / 1024
    return round(gb, 2)


def get_drive_type(drive: str) -> str:
    drivetype = win32file.GetDriveType(drive)
    if drivetype == win32con.DRIVE_FIXED:
        return "Fixed"
    elif drivetype == win32con.DRIVE_CDROM:
        return "CD-ROM"
    elif drivetype == win32con.DRIVE_REMOVABLE:
        return "Removable"
    elif drivetype == win32con.DRIVE_REMOTE:
        return "Remote"
    elif drivetype == win32con.DRIVE_RAMDISK:
        return "RAM Disk"
    else:
        return "Unknown"


def get_drive_name(drive: str) -> str:
    return win32api.GetVolumeInformation(drive)[0]

def get_drive_serial(drive: str) -> str:
    return win32api.GetVolumeInformation(drive)[1]

def get_drive_filesystem(drive: str) -> str:
    return win32api.GetVolumeInformation(drive)[4]


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # get api from app arguments
    argp = argparse.ArgumentParser()
    argp.add_argument("--api", type=str, required=True)
    args = argp.parse_args()
    api = args.api
    #

    # get system info
    drives = get_drives()
    systeminfo = {
        "name": win32api.GetComputerName(),
        "domain": win32api.GetDomainName(),
        "drives": drives,
    }
    #

    # send system info to api
    requests.post(api, json=systeminfo)

