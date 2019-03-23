import os


def send_mail(subject, body, to_email):
    cmd = f'echo "{body}" | mail -s  "{subject}" {to_email}'
    os.system(cmd)
    return
