import os
from multiprocessing import Pool, cpu_count
from nipype.interfaces.ants.segmentation import N4BiasFieldCorrection

def bias_field_correction(src_path, dst_path):
    print("N4ITK on: ", src_path)
    try:
        n4 = N4BiasFieldCorrection()
        n4.inputs.input_image = src_path
        n4.inputs.output_image = dst_path
        n4.inputs.dimension = 3
        n4.inputs.n_iterations = [50, 50, 30, 20]
        n4.inputs.shrink_factor = 3
        # n4.inputs.convergence_threshold = 1e-4
        # n4.inputs.bspline_fitting_distance = 300
        res = n4.run()
    except RuntimeError:
        print("\tFailed on: ", src_path)
    return

def unwarp_bias_field_correction(arg, **kwarg):
    return bias_field_correction(*arg, **kwarg)

# parent_dir = os.getcwd()
data_src_dir = "/mnt/d/preprocessed_dataset/schizophrenia/denoised/"
data_dst_dir = "schizophrenia/bias_corrected"
files = sorted(os.listdir(data_src_dir)[25:])

data_src_paths, data_dst_paths = [], []
for file in files:
    src_label = os.path.join(data_src_dir, file)
    dst_label = os.path.join(data_dst_dir, file)
    data_src_paths.append(src_label)
    data_dst_paths.append(dst_label)

# Multi-processing
paras = zip(data_src_paths, data_dst_paths)
pool = Pool(processes=cpu_count())
pool.map(unwarp_bias_field_correction, paras)