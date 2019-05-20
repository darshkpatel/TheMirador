#!/usr/bin/python3 -u

from helpers import *
from iptables import check_iptables
from auth_log import check_auth_log
from send_mail import send_mail

if __name__ == "__main__":
    from argparse import ArgumentParser
    import sys
    parser = ArgumentParser(description="TheMirador a python IDS")
    parser.add_argument("-c", "--config",
                        dest="filename", required=True, type=lambda x: is_valid_file(parser, x),
                        help="Path to config file", metavar="FILE")
    parser.add_argument('-cli', action='store_true', dest='cli')
    parser.add_argument('-map', action='store_true', dest='map')

    args = parser.parse_args()

    print("Loading Config")
    config = json.load(args.filename)
    hostname = config["system_name"]
    log("Started Monitoring")    
    log("Watching Folders: "+str(', '.join(config["watch_folders"])))
    if not os.path.isdir(config["work_dir"]):
        log("Baseline Not Generated, Generating")
        first_run(config)
    if args.map:
        hash_watch_folders(config)
    if args.cli:
        while True:
            accessed_files = check_accessed(config)
            if len(accessed_files)>0:
                log("File Accessed inside folder")
                send_mail("File Access Alert",str(accessed_files),config['email_to'])
                log(accessed_files)
            else:
                pass
            hash_files = check_hash(config)
            if(len(hash_files)>0):
                log("Integrity Check Failed")
                send_mail("File Integrity Check Failed",str(hash_files),config['email_to'])
                log(hash_files)
                hash_watch_folders(config)
            else:
                pass
            
            check_iptables(config)
            check_auth_log()
            time.sleep(5)
