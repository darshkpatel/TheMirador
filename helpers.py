import argparse
import os
import shutil
import hashlib
import time
import subprocess
import json
watch_folders = []


def is_valid_file(parser, arg):
    if not os.path.exists(arg):
        parser.error("The file %s does not exist!" % arg)
    else:
        return open(arg, 'r')


def first_run(config):
    work_dir = config["work_dir"]
    if os.path.isdir(work_dir):
        shutil.rmtree(work_dir)
        os.mkdir(work_dir)
        os.chdir(work_dir)
    else:
        os.mkdir(work_dir)
        os.chdir(work_dir)

    work_dir = config["logpath"]
    if os.path.isdir(work_dir):
        shutil.rmtree(work_dir)
        os.mkdir(work_dir)
        os.chdir(work_dir)
    else:
        os.mkdir(work_dir)
        os.chdir(work_dir)

    with open(config['logpath']+'.lastreported', 'w') as f:
        f.write('')

    hash_watch_folders(config)


def hash_folder(config, folder):
    hashes = subprocess.check_output(
        "find {} -type f | xargs md5sum ".format(folder), shell=True)
    final_json = []
    for line in str(hashes).split("\\n")[:-1]:
        hash_path = line.split(' ')
        final_json.append({"hash": hash_path[0], "location": hash_path[2], "modified": str(
            time.ctime(os.path.getmtime(hash_path[2])))})
    return final_json


def hash_watch_folders(config):
    work_dir = config["work_dir"]
    for folder in config["watch_folders"]:
        hex_folder = hashlib.md5(str(folder).encode('utf-8')).hexdigest()
        hashes = hash_folder(config, folder)
        path = work_dir+'/'+hex_folder
        with open(path, 'w', encoding="utf-8") as f:
            f.write(json.dumps(hashes))
            print("Wrote baseline for {} at {}".format(folder, path))


def check_hash(config):
    work_dir = config["work_dir"]
    for folder in config["watch_folders"]:
        hex_folder = hashlib.md5(str(folder).encode('utf-8')).hexdigest()
        current_hash = hash_folder(config, folder)
        path = work_dir+'/'+hex_folder
        with open(path, 'rb') as f:
            loaded_hash = json.loads(f.read())
        current_hash = [(x['hash'],x['location']) for x in current_hash ]
        loaded_hash = [(x['hash'],x['location']) for x in loaded_hash ]
        modified_files = [x for x in loaded_hash + current_hash if x not in loaded_hash or x not in current_hash]
        print('Files Modified: ')
        print(list(set(dict.fromkeys(modified_files))))
            