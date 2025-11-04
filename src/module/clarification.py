import numpy as np
import argparse
import glob

from libs.input import paths_to_3d_gray_array
from libs.global_function import mkdir_if_none
from libs.output import save_images_func

def z_normalize_3d(img: np.ndarray, desired_mean=150,
                   desired_std=30) -> np.ndarray:
    
    """
    配列をz_normalizeする
    配列の0の部分は0のままになるようにし，それ以外の部分の
    平均と標準偏差が指定の値になるように標準化する

    Parameters
    ----------
    img : np.ndarray
        標準化前の配列
    desired_mean : int, optional
        平均値を指定, by default 150
    desired_std : int, optional
        標準偏差を指定, by default 30

    Returns
    -------
    np.ndarray
        標準化した配列
    """
    # imgからコピーを作成
    new_img = img.astype(np.float64)

    # 画像の中で0より大きな値（物体部分）を抽出
    solid_parts = new_img[new_img > 0]
    
    # 0ではない部分の平均と偏差を計算
    current_mean = np.mean(solid_parts)
    current_std = np.std(solid_parts)
    
    # 配列すべて変更
    normalized_array = desired_std / current_std * \
        (new_img - current_mean) + desired_mean
        
    # 本来0の部分の値を取得する
    normalized_zero = desired_std / current_std * \
        (0 - current_mean) + desired_mean
    
    # もともと0の部分は0にする
    normalized_array[normalized_array == normalized_zero] = 0
    
    # もし値が0以下や255以上になった場合、それぞれ0や255にクリッピングします。
    clipped_array = np.clip(normalized_array, 0, 255)
    
    return clipped_array

def clarification_func(input_path,output_path):
    input_path_li = glob.glob(f'{input_path}/*.png')
    input_array = paths_to_3d_gray_array(input_path_li)
    
    output_array = z_normalize_3d(input_array)
    mkdir_if_none(output_path)
    save_images_func(output_array, output_path)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='''
    	画像を明確化する
    	''')
    parser.add_argument('before_path', help='')
    parser.add_argument('after_path', help='')
    # parser.add_argument('-f', '--flag', action='store_true')
    # parser.add_argument('-a', '--alpha', type=float, default=0.01) 
    args = parser.parse_args()
    before_path = args.before_path
    after_path = args.after_path
    
    clarification_func(before_path,after_path)