import os
import subprocess
from multiprocessing import Pool, cpu_count

def BET(src_path, dst_path, frac="0.4"):
    command = ["bet", src_path, dst_path, "-m", "-n", "-R", "-f", str(frac)]  
    subprocess.call(command)
    return

def strip_skull(src_path, dst_path, frac="0.4"): 
    print("Working on :", src_path)
    try:
        BET(src_path, dst_path, frac)  
    except RuntimeError:
        print("\tFailed on: ", src_path)
    return

def unwarp_strip_skull(arg, **kwarg):
    return strip_skull(*arg, **kwarg)

data_src_dir = "/mnt/d/preprocessed_dataset/schizophrenia/bias_corrected/"
data_dst_dir = "schizophrenia/brain_extracted"
files = os.listdir(data_src_dir)[25:]

data_src_paths, data_dst_paths,= [], [],
for file in files:
    src_label_dir = os.path.join(data_src_dir, file)
    dst_label_dir = os.path.join(data_dst_dir, file)
    data_src_paths.append(src_label_dir)
    data_dst_paths.append(dst_label_dir)

# Multi-processing
paras = zip(data_src_paths, data_dst_paths)
pool = Pool(processes=cpu_count())
pool.map(unwarp_strip_skull, paras)



