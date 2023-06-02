import argparse
import requests


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # get api from app arguments
    argp = argparse.ArgumentParser()
    argp.add_argument("--api", type=str, required=True)
    argp.add_argument("--input", type=str, required=True)
    args = argp.parse_args()
    api = args.api
    inputfile = args.input
    #

    systeminfo = {
        "name": "",
        "drives": [],
    }

    # get system info from input file
    with open(inputfile, "r") as f:
        # get system name from first line
        systeminfo["name"] = f.readline().strip()
        systeminfo['domain'] = f.readline().strip()
        # get drive information lines
        driveinfo = []
        for line in f.readlines():
            try:
                if line.startswith("    "):
                    drv = line.strip()
                    # driveinfo.append(line.strip())
                    totalGB = float(drv[42:53])
                    freeGB = float(drv[56:64])
                    used = totalGB - freeGB
                    usedpct = round(used / totalGB * 100, 2)
                    freepct = round(freeGB / totalGB * 100, 2)
                    driveinfo.append({
                        "drive": drv[0:1].strip(),
                        "type": drv[3:13].strip(),
                        "format": drv[14:20].strip(),
                        "name": drv[25:35].strip(),
                        "total": totalGB,
                        "free": freeGB,
                        "used": used,
                        "usedpct": usedpct,
                        "freepct": freepct,
                        "serial": "",
                    })
            except:
                pass

    systeminfo["drives"] = driveinfo

    # send system info to api
    requests.post(api, json=systeminfo)

