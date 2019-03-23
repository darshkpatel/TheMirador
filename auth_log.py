import subprocess
import datetime
import time
import sys
import json,os

f = open("watch.conf", "r")
LOGS_PATH = json.load(f)["logpath"]
f.close()
LOG_FILE_PATH = LOGS_PATH + "auth_access.log"
LAST_REPORTED_PATH = LOGS_PATH+".lastreported"
DEVNULL = open(os.devnull, 'wb')

def update_auth_logs():
    cmd = ["cat", "/var/log/auth.log"]
    try:
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=DEVNULL)
    except Exception as e:
        return
    with open(LOG_FILE_PATH, "w") as logfile:
        for line in proc.stdout.readlines():
            line_timestamp = line[0:15]
            line_timestamp = time.mktime(datetime.datetime.strptime(
                line_timestamp + str(datetime.datetime.now().year), "%b %d %H:%M:%S%Y").timetuple())
            if "USER=root" in line:
                logfile.write(line)
        logfile.close()
    f = open(LAST_REPORTED_PATH, "w")
    f.write(str(line_timestamp))
    f.close()

def check_auth_log():
    try:
        with open(LAST_REPORTED_PATH, "r") as f:
            try:
                timestamp = float(f.read())
                if timestamp > time.time():
                    # send_mail()  # send a mail to the sysadmin
                    print("Something found in Auth Logs ")
                    pass
                else:
                    update_auth_logs()
            except ValueError:  # case when the file is an empty file.
                update_auth_logs()
    except Exception as e:
        return