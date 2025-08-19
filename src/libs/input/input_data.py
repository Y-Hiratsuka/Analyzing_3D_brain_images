import pandas as pd
import glob


from .paths_to_array import paths_to_3d_gray_array
from .get_params import get_params

def input_data_func(brain_name:str,input_path:str) -> dict:
    """
    指定されたbrainの情報を返す関数

    Parameters
    ----------
    brain_name : str
        脳の名前を指定
    input_path : str
        脳の情報が書かれたcsvファイルのパスを指定

    Returns
    -------
    dict
        脳の情報を返す
    """
    IMAGES_PATH = get_params('original_data_path')
    # csvファイルから情報を取得
    df = pd.read_csv(input_path)
    info_dict = df[df['brain_name'] == brain_name].to_dict(orient='records')[0]
    
    # パスから三次元配列を作成
    path = f'{IMAGES_PATH}/{brain_name}/original_images'

    image_paths = glob.glob(f"{path}/*")
    arrays = paths_to_3d_gray_array(image_paths)
    
    dic = {
        'brain_name': brain_name,
        'image_arrays': arrays,
        'brain_RL': info_dict['brain_RL'],
        'x_pixel_size': info_dict['x_pixel_size'],
        'y_pixel_size': info_dict['y_pixel_size'],
        'z_step_size': info_dict['z_step_size'],
    }
    
    return dic
