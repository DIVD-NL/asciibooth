#!/usr/bin/env python

import time
import glob
import shutil
import os
import sys
import subprocess
import cups
import json

def printit(file: str) -> None :
    # Convert image to ascii art
    filename = os.path.basename(file)
    size = config.get("size", "120x64")
    if config.get("invert", True) :
        invert="--invert"
    else:
        invert=""
    before = config.get("before_print","")
    after = config.get("after_print","")
    result = subprocess.run(f"jp2a process/{filename} --border --size={size} {invert}",shell=True, capture_output=True, text=True)
    data = f"{header}\n{result}\n\f"
    with open(f"done/{filename[0:-4]}.txt", "w") as out:
        print(header, file=out)
        print(file=out)
        print(result.stdout, file=out)
        print(f"\n{filename[0:-4]}.txt", file=out)
    with open(f"done/{filename[0:-4]}.raw", "w") as out:
        print(before, end="", file=out)
        print(header, file=out)
        print(file=out)
        print(result.stdout, file=out)
        print(f"\n{filename[0:-4]}.txt", file=out)
        print("\f", file=out, end="")
        print(after, end="", file=out)
    job_id = conn.printFile(config["printer"], f"done/{filename[0:-4]}.raw", f"{filename[0:-4]}.jpg", {"raw": "true"})

config = json.load(open("config.json", "r"))
header = "".join(open("printable/header.txt", "r").readlines())
# Connect to CUPS
conn = cups.Connection()
print(f"Using printer: {config['printer']}")

while True:
    files = glob.glob("process/*.jpg")
    for file in files:
        print(f"Printing '{file}'...", end="")
        printit(file)
        shutil.move(file, "done/")
        print("done")
    time.sleep(1)
