from PIL import Image
from scipy.ndimage import median_filter
import os
import numpy as np

def create_dir(path):
    if not os.path.isdir(path):
        os.makedirs(path)
        
def thresholding(img, thr):       
    shape = img.shape
    height, width = shape
    new_img = np.zeros(shape)

    for i in range(height):
        for j in range(width):
            if img[i,j]>= thr:
                new_img[i,j] = 0
            else:
                new_img[i,j] = img[i,j]   
    return new_img

def save_img(img_array, save_path):
    img = Image.fromarray(img_array.astype(np.uint8))
    img.save(save_path)

parent_dir = "/drive0-storage/Gracia"
src_path = os.path.join(parent_dir, "sliced_data")
dst_path = os.path.join(parent_dir, "dataset")
create_dir(dst_path)
labels = ["schizophrenia","bipolar_disorder","healthy_controls"]

for label in labels:
    src_folder = os.path.join(src_path, label)
    dst_folder= os.path.join(dst_path, label)
    create_dir(dst_folder)
    for filename in sorted(os.listdir(src_folder)):
        if filename.endswith(".png"):
            file_path = os.path.join(src_folder, filename)
            img = np.array(Image.open(file_path))
            new_img = thresholding(img, 250)
            filtered = median_filter(new_img, size=3)
            save_path = os.path.join(dst_folder, filename)
            save_img(filtered,save_path)
        