import os
import subprocess
from multiprocessing import Pool, cpu_count

def create_dir(path):
    if not os.path.isdir(path):
        os.makedirs(path)

def FLIRT(src_path, dst_path, ref_path, omat_path):
    command = ["flirt", "-in", src_path, "-ref", ref_path, "-out", dst_path,
               "-omat", omat_path,  "-bins", "256", "-cost", "corratio",
               "-dof", "12", "-interp", "spline"]
    subprocess.call(command)
    return

def unwarp_main(arg, **kwarg):
    return main(*arg, **kwarg)

def main(src_path, dst_path, ref_path, omat_path):
    print("Registration on: ", src_path)
    try:
        FLIRT(src_path, dst_path, ref_path, omat_path)
    except RuntimeError:
        print("\tFalied on: ", src_path)
    return

ref_path ="/home/gracia/fsl/data/standard/MNI152_T1_1mm_brain.nii.gz"
data_src_dir = "/mnt/d/preprocessed_dataset/schizophrenia/brain_extracted/anat/"
data_dst_dir = "schizophrenia/registered/image"
omat_dst_dir = "schizophrenia/registered/affine"
create_dir(data_dst_dir)
create_dir(omat_dst_dir)
files = sorted(os.listdir(data_src_dir))[25:]

data_src_paths, data_dst_paths, omat_paths = [], [], []
for file in files:
    src_label_dir = os.path.join(data_src_dir, file)
    dst_label_dir = os.path.join(data_dst_dir, file)
    omat_label_dir = os.path.join(omat_dst_dir, file)
    data_src_paths.append(src_label_dir)
    data_dst_paths.append(dst_label_dir)
    omat_paths.append(omat_label_dir.replace("nii.gz","omat"))

# Multi-processing
paras = zip(data_src_paths, data_dst_paths,
            [ref_path] * len(data_src_paths), omat_paths)
pool = Pool(processes=cpu_count())
pool.map(unwarp_main, paras)    
