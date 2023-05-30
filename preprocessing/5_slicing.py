import os
import numpy as np
from PIL import Image
import re
import nibabel as nib

def create_dir(path):
    if not os.path.isdir(path):
        os.makedirs(path)
        
src_path = "/mnt/d/Files/Akademik/Semester_8/Tugas_Akhir/proc_dataset"
dst_path = os.path.join(src_path, "sliced")
labels = ["schizophrenia","bipolar_disorder","healthy_controls"]

for label in labels:
    src_folder = os.path.join(src_path, label)
    dst_folder= os.path.join(dst_path, label)
    create_dir(dst_folder)
    for filename in sorted(os.listdir(src_folder)):
        if filename.endswith("nii.gz"):
            file = os.path.join(src_folder,filename)
            img = nib.load(file).get_fdata()
            pattern = "\d{5}"
            match = re.search(pattern, filename)
            subject_id = match.group()
            for idx in range(50,146):
                sliced = img[:,:,idx]
                # normalize and convert image to uint8
                normalized = sliced/sliced.max()
                normalized *= 255
                normalized = normalized.astype(np.uint8)
                # save as png
                save_path = os.path.join(dst_folder, "{}_{}.png".format(subject_id,idx))
                norm_img = Image.fromarray(normalized)
                norm_img.save(save_path)
        else:
            continue