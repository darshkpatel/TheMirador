import subprocess, json, os
from log_manage import log
DEVNULL = open(os.devnull, 'wb')



def write_to_log(path):
    with open(path, "w") as f:
        cmd = ["sudo", "iptables", "--list"]
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE)
        for line in proc.stdout.readlines():
            f.write(str(line))


def check_iptables(config):
    IPTABLES_LOGS_PATH = config["logpath"] + "iptables.log"
    IPTABLES_TEMP_LOGS_PATH = config["logpath"]+"iptables.tmplog"

    write_to_log(IPTABLES_TEMP_LOGS_PATH)
    cmd = ["diff", IPTABLES_LOGS_PATH, IPTABLES_TEMP_LOGS_PATH]
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=DEVNULL)
    if proc.stdout.readlines():
        # send mail
        log("Iptables are Modified")
        write_to_log(IPTABLES_LOGS_PATH)
    else:
        #log("Iptables not modified")
        pass


