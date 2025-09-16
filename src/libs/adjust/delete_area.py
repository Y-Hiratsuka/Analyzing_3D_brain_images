import numpy as np
import glob

from libs.input import paths_to_3d_gray_array,get_params

def delete_unnecessary_areas(array: np.ndarray,) -> np.ndarray:
    STANDARD_BRAIN_PATH = f'{get_params("adjusted_images_dir_path")}/1-1_GAP43/rotate_images',
    # 基準脳のインポート
    standard_path_li = glob.glob(f'{STANDARD_BRAIN_PATH}/*')
    standard_array = paths_to_3d_gray_array(standard_path_li)
    
    
    # 基準脳のゼロエリアを取得
    zero_arias_of_standard_brain = standard_array[...] == 0
    array[zero_arias_of_standard_brain] = 0
    
    return array
