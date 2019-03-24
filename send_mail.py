import os,json
f = open("watch.conf", "r")
hostname = json.load(f)["system_name"]
f.close()

def send_mail(subject, body, to_email):
    subject = subject+" - "+hostname
    cmd = f'echo "{body}" | mail -s  "{subject}" {to_email}'
    os.system(cmd)
    return
