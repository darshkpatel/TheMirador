import json
from helpers import *




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
    #first_run(config)
    #check_hash(config)