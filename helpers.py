import argparse
import os,shutil,hashlib
import subprocess

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
    hash_watch_folders(config)


def hash_folder(config, folder):
    output = subprocess.check_output("find {} -type f | xargs md5sum ".format(folder), shell=True)
    return output
def hash_watch_folders(config):
    work_dir = config["work_dir"]
    for folder in config["watch_folders"]:
        print(folder)
        hex_folder = hashlib.md5(str(folder).encode('utf-8')).hexdigest()
        watch_folders.append({
            'hex_folder': hex_folder,
            'path': folder 
        })
        hashes = hash_folder(config, folder)
        path = work_dir+'/'+hex_folder
        with open(path,'wb') as f:
            f.write(hashes)
            print("Wrote at {}".format(path))

    
