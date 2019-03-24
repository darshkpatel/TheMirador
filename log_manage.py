import logging,json,time,sys,os,shutil
f = open("watch.conf", "r")
config = json.load(f)
logpath = config["logpath"]
dumpmem = config["dump_memory"]
f.close()

work_dir = config["logpath"]
if os.path.isdir(work_dir):
    shutil.rmtree(work_dir)
    os.mkdir(work_dir)
else:
    os.mkdir(work_dir)


with open(config['logpath']+'.lastreported', 'w') as f:
    f.write('')

with open(config['logpath']+'mirador.log', 'w') as f:
    f.write('')

for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)
logging.basicConfig(filename=logpath+'mirador.log', filemode='w',format='%(asctime)s - %(message)s', level=logging.INFO)

def log(message):
    f = open(logpath+'mirador.log','a')
    f.write("{} - {}\n".format(str(time.strftime("%x_%X")), message))
    f.close()
    print(message)

    if(dumpmem=='true'):
        import os
        logging.info("Dumping Memory")
        log("Dumping Memory")
        os.system("sudo dd if=/dev/fmem of={}memory_dump_{}.raw bs=1MB".format(logpath,str(time.strftime("%x_%X"))))
        logging.info("Memory Dumped")
        log("Memory Dumped")
    