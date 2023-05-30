import os
import subprocess
from multiprocessing import Pool, cpu_count
import time

def create_dir(path):
    if not os.path.isdir(path):
        os.makedirs(path)

def susan(input_file, output_file, fwhm):
    """Calls the FSL SUSAN command.
    Usage: susan(input_file, output_file, fwhm)
    Parameters:
    - input_file: input image path
    - output_file: output smoothed image path
    - fwhm: spatial size of smoothing in mm

    Function is called with set parameters:
    -1 for brightness threshold to auto-set as 10% of the robust range
    3 for dimensionality of smoothing (3D)
    1 to use a local median filter in cases where single-point noise is detected
    0 for smoothing without secondary image
    """
    command = ["susan", input_file, "-1", str(fwhm),
               "3", "1", "0", output_file]
    subprocess.call(command)
    return

def main(src_path, dst_path, fwhm=4):
    print("Working on :", src_path)
    try:
        susan(src_path, dst_path, 4)
    except RuntimeError:
        print("\tFailed on: ", src_path)      
    return  

def unwarp_main(arg, **kwarg):
    return main(*arg, **kwarg)

st = time.time()
parent_dir = os.path.dirname(os.getcwd()) 
data_src_dir = os.path.join(parent_dir, "dataset", "raw")
data_dst_dir = os.path.join(parent_dir, "dataset", "processed", "denoised")
labels = ["schizophrenia", "bipolar_disorder", "healthy_control"]
create_dir(data_dst_dir)

data_src_paths, data_dst_paths = [], []
for label in labels:
    src_label_dir = os.path.join(data_src_dir, label)
    dst_label_dir = os.path.join(data_dst_dir, label)
    create_dir(dst_label_dir)
    for file in os.listdir(src_label_dir):
        if file.endswith("nii.gz"):
            data_src_paths.append(os.path.join(src_label_dir, file))
            data_dst_paths.append(os.path.join(dst_label_dir, file))

# Multi-processing
paras = zip(data_src_paths, data_dst_paths)
pool = Pool(processes=cpu_count())
pool.map(unwarp_main, paras)

et = time.time()
elapsed_time = et - st
print(f'Execution time:', elapsed_time, 'seconds')
