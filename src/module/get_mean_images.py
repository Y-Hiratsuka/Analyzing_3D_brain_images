import argparse
import numpy as np
import glob

from libs.input import paths_to_3d_gray_array, get_params
from libs.global_function import mkdir_if_none
from libs.output import save_images_func


def get_mean(dir_li, save_dir_path):
    
    
    arrays = np.array([paths_to_3d_gray_array(glob.glob(f'{dir_path}/*.png')) for dir_path in dir_li])
    
    mean_array = np.mean(arrays, axis=0)
    mkdir_if_none(save_dir_path)
    
    save_images_func(mean_array,save_dir_path= save_dir_path)
        
if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='''
        複数の画像群の平均を取る
        ''')
    
    parser.add_argument("category_name", help="脳のカテゴリー名を指定")
    

    args = parser.parse_args()
    category_name = args.category_name
    

        
    dir_li = get_params(category_name)
    dir_li = [f'{temp}/rotate_images' for temp in dir_li]
    
    save_path = f"{get_params('mean_dir_path')}/{category_name}"
    mkdir_if_none(save_path)

    get_mean(dir_li= dir_li,
             save_dir_path= save_path)
