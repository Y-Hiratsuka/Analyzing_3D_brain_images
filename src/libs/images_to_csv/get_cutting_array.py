import pandas as pd
import numpy as np
import cv2

from libs.input import get_params

def cutting_out_area_func(csv_path: str,
                        start_line: int,end_line: int,
                        brain_shape = (24,20,60)) -> np.ndarray:
    """
    切り出すエリアが保存されているcsvパスを読み込み，arrayで返す    

    Parameters
    ----------
    csv_path : str
        エリアが保存されいるcsvパス（1が切り取る場所）
    start_line : int
        エリアの開始行数
    end_line : int
        エリアの終了行数
    brain_shape : tuple, optional
        脳の形状, by default (24,20,60)

    Returns
    -------
    np.ndarray
        _description_
    """
    df = pd.read_csv(csv_path,header=None)

    # 4-45 42
    array4_45 = np.array(df)
    array4_45 = array4_45.reshape((-1,brain_shape[1], brain_shape[0]))

    array4_45 = np.where(array4_45 == 1,1,0)

    array1_3 = np.full((start_line - 1,brain_shape[1], brain_shape[0]),0) 
    array46_60 = np.full((brain_shape[2] - end_line,brain_shape[1], brain_shape[0]),0) 

    array1_60 = np.concatenate([array1_3,array4_45,array46_60])

    return array1_60

def get_cutting_array_func():
    '''
    解析対象のボクセルのみ取得
    '''
    cutting_csv_path = get_params("cutting_csv_path")
    
    # 必要部位を１，不要部位を０に割り振ったarrayを作成
    cutting_array = cutting_out_area_func(csv_path=cutting_csv_path,
                                        start_line=4, end_line=45)
    # 形状を揃える
    # (60,20,24) -> (60,20,24,1)
    cutting_array = np.reshape(cutting_array,(60,20,24,1)) 
    # print(cutting_array[34])
    # (60,20,24,1) -> (60,20,24,3)
    cutting_array = np.tile(cutting_array, (1, 1,1, 1)).astype(np.uint8)
    # (60,20,24,3) -> (60,100,120,3)
    cutting_array = np.array([
        cv2.resize(cutting_array[i],(120,100))
        for i in range(cutting_array.shape[0])
    ])
    return cutting_array


