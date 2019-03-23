import subprocess
from auth_log import LOGS_PATH

IPTABLES_LOGS_PATH = LOGS_PATH + "iptables.log"
IPTABLES_TEMP_LOGS_PATH = LOGS_PATH+"iptables.tmplog"


def write_to_log(path):
    with open(path, "w") as f:
        cmd = ["sudo", "iptables", "--list"]
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE)
        for line in proc.stdout.readlines():
            f.write(str(line))


def check_diff():
    write_to_log(IPTABLES_TEMP_LOGS_PATH)
    cmd = ["diff", IPTABLES_LOGS_PATH, IPTABLES_TEMP_LOGS_PATH]
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    if proc.stdout.readlines():
        # send mail
        print("Modified")
    else:
        print("Not modified")


check_diff()
