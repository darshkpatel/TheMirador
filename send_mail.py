import os


def send_mail(subject, body, to_email, message_file):
    cmd = f'echo "{body}" | mail -s  "{subject}" {to_email}'
    os.system(cmd)
    return
