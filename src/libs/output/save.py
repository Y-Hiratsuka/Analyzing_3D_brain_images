import numpy as np
import cv2

from libs.global_function import mkdir_if_none

def save_images_func(array: np.ndarray, save_dir_path: str) -> None:
    '''
    np.ndarrayを複数のimageにして保存
    '''
    #! Do the final one again at the end
    mkdir_if_none(save_dir_path)
    for i in range(len(array)):
        zero_n = 4 - len(str(i))
        file_name = "0" * zero_n + f"{i}.png"
        cv2.imwrite(f'{save_dir_path}/{file_name}', array[i])