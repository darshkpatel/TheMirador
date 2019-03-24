import argparse
import os
import shutil
import hashlib
import time
import subprocess
import json
watch_folders = []
from log_manage import *

def is_valid_file(parser, arg):
    if not os.path.exists(arg):
        parser.error("The file %s does not exist!" % arg)
    else:
        return open(arg, 'r')


def first_run_folders(config):
    work_dir = config["work_dir"]
    if os.path.isdir(work_dir):
        shutil.rmtree(work_dir)
        os.mkdir(work_dir)
        os.chdir(work_dir)
        #print("DELETED")
    else:
        os.mkdir(work_dir)
        os.chdir(work_dir)

    work_dir = config["logpath"]
    if os.path.isdir(work_dir):
        shutil.rmtree(work_dir)
        #print("DELETED")
        os.mkdir(work_dir)
        os.chdir(work_dir)
    else:
        os.mkdir(work_dir)
        os.chdir(work_dir)
    with open(config['logpath']+'.lastreported', 'w') as f:
        f.write('')
    
    with open(config['logpath']+'mirador.log', 'w') as f:
        f.write('')

def first_run(config):
    first_run_folders(config)
    work_dir = config["work_dir"]
    from iptables import write_to_log

    write_to_log(work_dir+"iptables.log")
    hash_watch_folders(config)


def hash_folder(config, folder):
    work_dir = config["work_dir"]
    os.chdir(work_dir)
    cmd = "find {} -type f | xargs md5sum ".format(folder)
    hashes = subprocess.check_output(cmd , shell=True)
    final_json = []
    for line in str(hashes).split("\\n")[:-1]:
        hash_path = line.split(' ')
        final_json.append({"hash": hash_path[0], "location": hash_path[2], "accessed": os.stat(
            hash_path[2]).st_atime})
    #print(final_json)
    return final_json



def hash_watch_folders(config):
    work_dir = config["work_dir"]
    for folder in config["watch_folders"]:
        hex_folder = hashlib.md5(str(folder).encode('utf-8')).hexdigest()
        hashes = hash_folder(config, folder)
        path = work_dir+'/'+hex_folder
        with open(path, 'w', encoding="utf-8") as f:
            f.write(json.dumps(hashes))
            log("Wrote baseline for {} at {}".format(folder, path))


def check_hash(config):
    work_dir = config["work_dir"]
    for folder in config["watch_folders"]:
        hex_folder = hashlib.md5(str(folder).encode('utf-8')).hexdigest()
        current_hash = hash_folder(config, folder)
        path = work_dir+'/'+hex_folder
        with open(path, 'rb') as f:
            loaded_hash = json.loads(f.read())
        current_hash = [(x['hash'], x['location']) for x in current_hash]
        loaded_hash = [(x['hash'], x['location']) for x in loaded_hash]
        modified_files = [x for x in loaded_hash +
                          current_hash if x not in loaded_hash or x not in current_hash]
        #logging.info('Watching Files Modified: ')with open(path, 'w', encoding="utf-8") as f:
        update_access_time(config)
        return list(set(dict.fromkeys(modified_files)))

def update_access_time(config):
    work_dir = config["work_dir"]
    for folder in config["watch_folders"]:
        hex_folder = hashlib.md5(str(folder).encode('utf-8')).hexdigest()
        path = work_dir+'/'+hex_folder
        with open(path, 'rb') as f:
            loaded_hash = json.loads(f.read())
        new_hash = []
        for file in loaded_hash:
            file['accessed'] = os.stat(file['location']).st_atime
            new_hash.append(file)
        with open(path, 'w', encoding="utf-8") as f:
            f.write(json.dumps(new_hash))

def check_accessed(config):
    work_dir = config["work_dir"]
    for folder in config["watch_folders"]:
        hex_folder = hashlib.md5(str(folder).encode('utf-8')).hexdigest()
        path = work_dir+'/'+hex_folder
        with open(path, 'rb') as f:
            loaded_hash = json.loads(f.read())
        loaded_hash = [(x['accessed'], x['location']) for x in loaded_hash]
        current_hash = []
        for x in loaded_hash:
            try:
                current_hash.append((os.stat(x[1]).st_atime, x[1]))
            except FileNotFoundError:
                return
        modified_files = [x for x in loaded_hash +
                          current_hash if x not in loaded_hash or x not in current_hash]
       # logging.info('Watching Files Accessed: ')
        return list(set(dict.fromkeys(modified_files)))
