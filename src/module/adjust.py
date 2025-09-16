import glob
import numpy as np
import argparse
import pandas as pd
from scipy.ndimage import zoom

from libs.input import paths_to_3d_gray_array,get_params
from libs.adjust import add_margin,rotate_3d,shift_array,change_shape,delete_unnecessary_areas
from libs.output import save_images_func

def original_rotate(rotate_brain_path,save_dir_path,
                    dic,white_flag = False):

    AFTER_SHAPE = (60,100,120)
    
    # 読み込み
    rotate_paths = glob.glob(f'{rotate_brain_path}/*')
    rotate_array = paths_to_3d_gray_array(rotate_paths)

    # 余白をつける
    rotate_array, _ = add_margin(
        array1=rotate_array, array2=rotate_array, zoom_rate=0.5)
    
    # 倍率を変更
    rotate_array = zoom(rotate_array, [dic['z_zoom'], dic['x_zoom'], dic['y_zoom']], order=0)

    #　回転させる
    rotated_array = rotate_3d(rotate_array, [dic['x_deg'], dic['y_deg'], dic['z_deg']])

    #　中心位置の移動
    rotated_array = shift_array(
        rotated_array, [dic['z_move'] , dic['y_move'], dic['x_move']])
    
    # 形状の統一
    rotated_array = change_shape(rotated_array,AFTER_SHAPE)

    if white_flag:
        rotated_array = np.where(rotated_array == 0, 0, 255)
    
    #! 色の標準化 ->　標準化は行わないことにする 
    # rotated_array = z_normalize_3d(rotated_array,desired_mean=DESIRED_MEAN,desired_std=DESIRED_STD)
    
    
    # 基準脳（1-1）にはない部分は全て0に設定する
    if not "1-1_GAP43" in rotate_brain_path :
        rotated_array = delete_unnecessary_areas(rotated_array)

    # 画像群の保存
    save_images_func(rotated_array, save_dir_path)
    
if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='''
        図形を回転させる
        ''')
    parser.add_argument("brain_name", help="brain name(ex 1-1)")
    args = parser.parse_args()
    brain_name = args.brain_name

    INPUT_CSV_PATH = get_params('brains_csv_path')
    IMAGE_PATH = get_params('corrected_images_dir_path')


    rotate_brain_path = f'{IMAGE_PATH}/{brain_name}/normalize_images'
    save_dir_path = f'{IMAGE_PATH}/{brain_name}/rotate_images'

    df = pd.read_csv(INPUT_CSV_PATH)
    info_dict = df[df['brain_name'] == brain_name].to_dict(orient='records')[0]
    li_str = info_dict['rotate_info']

    
    li = li_str.split('\t')
    li = [float(temp) for temp in li]

    dic = {
        "x_deg":li[0], "y_deg": li[1], "z_deg": li[2],
        "x_zoom":li[3], "y_zoom": li[4], "z_zoom": li[5],
        "x_move": li[6], "y_move": li[7], "z_move": li[8],
    }
    
    original_rotate(rotate_brain_path=rotate_brain_path,
                    save_dir_path=save_dir_path,
                    dic = dic,
                    white_flag=False)