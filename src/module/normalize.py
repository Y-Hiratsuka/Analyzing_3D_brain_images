import argparse

from libs.global_function import mkdir_if_none
from libs.input import input_data_func,get_params
from libs.normalize import  get_reversal_images, correct_volume,move_gravity
from libs.output import save_images_func

def normalize(brain_name, csv_path):
    
    # データのインプット
    data = input_data_func(brain_name=brain_name,
                      input_path=csv_path)

    # 右脳なら，鏡面像で左脳とする
    image_arrays = data['image_arrays']
    if data['brain_RL'] == 'right':
        image_arrays = get_reversal_images(image_arrays)

    # 体積を変更
    equipped_array = correct_volume(image_arrays, data,new_volume=1e9)
    
    # 重心を中央に持ってくる
    padding_array = move_gravity(equipped_array)
    return padding_array



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='''
        体積を一定にし，重心を中央に持ってくる
        ''')
    parser.add_argument("brain_name", help="brain name(ex 1-1)")

    args = parser.parse_args()
    brain_name = args.brain_name
    
    
    IMAGES_PATH = get_params("adjusted_images_dir_path")
    save_dir_path = f'{IMAGES_PATH}/{brain_name}/normalize_images'
    
    # save_dirがない場合作る
    mkdir_if_none(f'{IMAGES_PATH}/{brain_name}')
    mkdir_if_none(save_dir_path)
    
    # 標準化
    normalize_arrays = normalize(brain_name=brain_name,csv_path=get_params("brains_csv_path"))

    # 画像の保存
    save_images_func(normalize_arrays,save_dir_path)