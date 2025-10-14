

from libs.input import dir_to_array, get_params

def images_to_dic_func(info_dic, brain_name):
    '''
    座標ごとにまとめた脳の情報辞書にデータを追加
    '''
    brain_path = f'{get_params("corrected_images_dir_path")}/{brain_name}/rotate_images'
    
    array = dir_to_array(brain_path)

    for z in range(60):
        for y in range(100):
            for x in range(120):
                info_dic[f"x{x}.y{y}.z{z}"][brain_name] = array[z][y][x]
    
    return info_dic

