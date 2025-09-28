import glob
import cv2
import numpy as np
import argparse
from scipy.ndimage import zoom

from libs.global_function import mkdir_if_none
from libs.input import get_params

def overlap_func(dir_path, save_dir_path,standard_path,zoom_rate,a = 0.5):
    # 配列の取得
    paths = glob.glob(f'{dir_path}/*.png')
    array = np.array([cv2.imread(path) for path in paths])
    
    # 基準配列の画像
    standard_paths = glob.glob(f'{standard_path}/*.png')
    standard_array = np.array([cv2.imread(path) for path in standard_paths])
    
    zoom_rate = standard_array.shape[0] / array.shape[0]
    array = zoom(array,[1, zoom_rate, zoom_rate, 1], order=0) # 倍率の変化

    mkdir_if_none(save_dir_path)
    for i in range(len(array)):
        new_image = cv2.addWeighted(array[i], a, standard_array[int(i * zoom_rate)], 1-a, 0)
        zero_n = 4 - len(str(i))
        file_name = "0" * zero_n + f"{i}.png"
        cv2.imwrite(f'{save_dir_path}/{file_name}', new_image)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='''
    	基準画像を背景に加える
    	''')
    parser.add_argument("image_dir_path", help="image_dir_path")
    parser.add_argument("save_path", help="save_path")
    
    args = parser.parse_args()
    image_dir_path = args.image_dir_path
    save_path = args.save_path
    
    standard_dir_path = get_params('standard_brain_path')
    overlap_func(dir_path=image_dir_path,
                  save_dir_path=save_path,
                  standard_path=standard_dir_path,
                  zoom_rate=1)