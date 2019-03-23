from helpers import *
from iptables import check_iptables
from auth_log import check_auth_log
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
    print("Watching Folders: ")
    for folder in config["watch_folders"]:
        print("\t"+folder)
    if not os.path.isdir(config["work_dir"]):
        print("Baseline Not Generated, Generating")
        first_run(config)
    if args.map:
        hash_watch_folders(config)
    if args.cli:
        accessed_files = check_accessed(config)
        if len(accessed_files)>0:
            print("File Accessed inside folder")
            print(accessed_files)
        else:
            print("Files not Accessed since last check")
        hash_files = check_hash(config)
        if(len(hash_files)>0):
            print("Integrity Check Failed")
            print(hash_files)
            hash_watch_folders(config)
        else:
            print("File Integrity Intact")
        
        check_iptables()
        check_auth_log()
