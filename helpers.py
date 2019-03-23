import argparse
import os,shutil,hashlib
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
    with open(config['logpath']+'.lastreported','w') as f:
        f.write('')

    hash_watch_folders(config)



def hash_folder(config, folder):
    hashes = subprocess.check_output("find {} -type f | xargs md5sum ".format(folder), shell=True)
    final_json = []
    for line in str(hashes).split("\\n")[:-1]:
            hash_path = line.split(' ')
            final_json.append({'hash':hash_path[0], 'location':hash_path[2], 'modified':str(time.ctime(os.path.getmtime(hash_path[2])))})
    return final_json

def hash_watch_folders(config):
    work_dir = config["work_dir"]
    for folder in config["watch_folders"]:
        hex_folder = hashlib.md5(str(folder).encode('utf-8')).hexdigest()
        hashes = str(hash_folder(config, folder))
        path = work_dir+'/'+hex_folder
        with open(path,'w',encoding="utf8") as f:
            json.dump(hashes,f,ensure_ascii=False, indent=4)
            print("Wrote baseline for {} at {}".format(folder,path))

    
def match_hash(config):
    pass