import subprocess
import datetime
import time
import sys
import json
import os
from send_mail import send_mail
from log_manage import log
f = open("watch.conf", "r")
fj = json.load(f)
LOGS_PATH = fj["logpath"]
EMAIL_TO = fj["email_to"]
f.close()
LOG_FILE_PATH = LOGS_PATH + "auth_access.log"
LAST_REPORTED_PATH = LOGS_PATH+".lastreported"
DEVNULL = open(os.devnull, 'wb')


def update_auth_logs():
    cmd = ["tail", "/var/log/auth.log"]
    email = False
    try:
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=DEVNULL)
    except Exception as e:
        return
    with open(LOG_FILE_PATH, "w") as logfile:
        for line in proc.stdout.readlines():
            line_timestamp = str(line[0:15])
            line_timestamp = time.mktime(datetime.datetime.strptime(
                line_timestamp + str(datetime.datetime.now().year), "b'%b %d %H:%M:%S'%Y").timetuple())
            if b'USER=root' in line and b'mirador' not in line:
                logfile.write(str(line))
                email = True
            if b'sshd' in line:
                logfile.write(str(line))
                email = True
        logfile.close()
    if email:
        with open(LOG_FILE_PATH, "r") as logfile:
            log("Something found in Auth Logs ")
            send_mail("Alert in authlogs ",
                      logfile.read(), EMAIL_TO)
    f = open(LAST_REPORTED_PATH, "w")
    try:
        f.write(str(line_timestamp))
    except UnboundLocalError:
        #log("No auth logs found")
        pass
    f.close()


def check_auth_log():
    with open(LAST_REPORTED_PATH, "r") as f:
        try:
            timestamp = float(f.read())
            if timestamp > time.time():
                # send_mail()  # send a mail to the sysadmin
                with open(LOG_FILE_PATH, "r") as logfile:
                    log("Tampered auth file")
                    send_mail("Tampered .lastreported file",
                              logfile.read(), EMAIL_TO)
            else:
                update_auth_logs()
        except ValueError:  # case when the file is an empty file.
            update_auth_logs()
