import subprocess
import datetime

import json

f = open("watch.conf", "r")
LOG_FILE_PATH = json.load(f)["logpath"]+".lastreported"
f.close()

with open(LOG_FILE_PATH, "r") as f:
    print(f.read())

# with open("/")

def get_auth_logs():
    cmd = ["tail", "/var/log/auth.log"]
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    last_reported = 0
    for line in proc.stdout.readlines():
        if "USER=root" in line:
            pass

