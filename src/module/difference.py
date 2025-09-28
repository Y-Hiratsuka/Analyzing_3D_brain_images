import numpy as np
import argparse

from libs.input import dir_to_array
from libs.output import save_images_func

def difference_func(path1,path2, n = 30):
    array1 = dir_to_array(path1).astype(np.float32)
    array2 = dir_to_array(path2).astype(np.float32)

    diff_array = array1 - array2

    output_array = np.zeros((*diff_array.shape,3))
    
    mask_positive = diff_array > 0
    output_array[mask_positive, 2] = diff_array[mask_positive] * n
    
    mask_negative = diff_array < 0
    output_array[mask_negative, 0] = - diff_array[mask_negative] * n
    
    output_array = np.clip(output_array, 0, 255)
    
    return output_array

if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(description='''
    	差分画像の作成
    	''')
    parser.add_argument('path1', help='')
    parser.add_argument('path2', help='')
    parser.add_argument('save_path')
    args = parser.parse_args()
    
    path1 = args.path1
    path2 = args.path2
    save_path = args.save_path
    
    output_array = difference_func(path1, path2)
    
    save_images_func(output_array, save_path)