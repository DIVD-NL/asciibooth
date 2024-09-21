#!/usr/bin/env python

import time
import glob
import shutil
import os
import subprocess
import cups

def printit(file: str) -> None :
    # Convert image to ascii art
    filename = os.path.basename(file)
    result = subprocess.run(f"jp2a process/{filename} --border --size=120x64 --invert",shell=True, capture_output=True, text=True)
    with open(f"done/{filename[0:-4]}.txt", "w") as out:
        print(header, file=out)
        print(file=out)
        print(result.stdout, file=out)
        print(f"\n{filename[0:-4]}.txt", file=out)
        print("\f", file=out, end="")
    job_id = conn.printFile("Oki_ML3391", f"done/{filename[0:-4]}.txt", f"{filename[0:-4]}.txt", {"raw": "true"})

def mailit(file: str) -> None :
    # Convert image to ascii art
    filename = os.path.basename(file)
    print("WOuld email if i could")



header = "".join(open("printable/header.txt", "r").readlines())
# Connect to CUPS
conn = cups.Connection()
# Get a list of printers
#printers = conn.getPrinters()
#printer_name = list(printers.keys())[1]  # Select the first printer (or specify by name)
#
#print(f"Using printer: {printer_name}")
#quit()


while True:
    files = glob.glob("process/*.jpg")
    for file in files:
        print(f"Printing '{file}'...", end="")
        printit(file)
        shutil.move(file, "done/")
        print("done")
    files = glob.glob("process/*.email")
    for file in files:
        filename = os.path.basename(file)
        if os.path.exists(f"done/{filename[0:-6]}.txt") :
            print(f"Emailing '{file}'...", end="")
            mailit(file)
            print("done")
            shutil.move(file, "done/")
    time.sleep(1)
