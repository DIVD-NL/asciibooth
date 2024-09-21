#!/usr/bin/env python

import time
import glob
import shutil
import os
import sys
import subprocess
import cups
import json
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders


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
    # Send email, if we can
    filename = os.path.basename(file)
    # Create the MIMEMultipart message object
    to = "".join(open(file,"r").readlines()).strip()
    msg = MIMEMultipart()
    msg['From'] = config["email"]["from"]
    msg['To'] = to
    msg['Subject'] = config["email"]["subject"]

    # Attach the body text to the email
    msg.attach(MIMEText(config["email"]["message"], 'plain'))

    # Attach picture
    with open(f"done/{filename[0:-6]}.jpg", "rb") as fh:
        # Create a MIMEBase instance and attach the text file
        part = MIMEBase('img', 'jpg')
        part.set_payload(fh.read())

        # Encode the payload to base64
        encoders.encode_base64(part)

        # Add header for the attachment
        part.add_header(
            'Content-Disposition',
            f'attachment; filename={filename[0:-6]}.jpg',
        )

        # Attach the file to the message
        msg.attach(part)

    # Attach text
    with open(f"done/{filename[0:-6]}.txt", "r") as fh:
        # Create a MIMEBase instance and attach the text file
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(fh.read())

        # Encode the payload to base64
        encoders.encode_base64(part)

        # Add header for the attachment
        part.add_header(
            'Content-Disposition',
            f'attachment; filename={filename[0:-6]}.txt',
        )

        # Attach the file to the message
        msg.attach(part)

    try:
        with smtplib.SMTP(config["email"]["server"], config["email"]["port"]) as server:
            server.starttls()  # Upgrade the connection to TLS
            server.login(config["email"]["user"], config["email"]["pass"])  # Log in to the email account
            text = msg.as_string()  # Convert the message to string format
            server.sendmail(config["email"]["from"], to, text) #Send the email
        shutil.move(file, "done/")
        print("done")
    except:
        shutil.move(file, "failed/")
        print("failed")



header = "".join(open("printable/header.txt", "r").readlines())
# Connect to CUPS
conn = cups.Connection()
# Get a list of printers
#printers = conn.getPrinters()
#printer_name = list(printers.keys())[1]  # Select the first printer (or specify by name)
#
#print(f"Using printer: {printer_name}")
#quit()

config = json.load(open("config.json", "r"))

while True:
    files = glob.glob("process/*.jpg")
    for file in files:
        print(f"Printing '{file}'...", end="")
        printit(file)
        shutil.move(file, "done/")
        print("done")
    files = glob.glob("process/*.email")
    if "email" in config :
        for file in files:
            filename = os.path.basename(file)
            if os.path.exists(f"done/{filename[0:-6]}.txt") :
                print(f"Emailing '{file}'...", end="")
                sys.stdout.flush()
                mailit(file)
    time.sleep(1)
