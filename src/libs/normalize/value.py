import numpy as np
from scipy.ndimage import zoom

def correct_volume(arr:np.ndarray,info:dict,new_volume = 1e10) -> np.ndarray:
    """
    与えられた三次元配列が表す立体の体積を指定された大きさになるように縮小する

    Parameters
    ----------
    arr : np.ndarray
        修正する三次元配列
    info : dict
        xyz軸それぞれの単位あたりの長さを与える
    new_volume : _type_, optional
        補整したあたりの体積, by default 1e10

    Returns
    -------
    np.ndarray
        修正した三次元配列
    """
    
    AFTER_PIXEL_SIZE = 10
    # 配列の形状を取得
    z_before_pixel_n, y_before_pixel_n, x_before_pixel_n = arr.shape
    # 0ではない要素の個数を取得
    elements_n = np.count_nonzero(arr)
    
    # xyzの単位長さを取得
    x_one_pixel_size, y_one_pixel_size, z_one_step_size =\
        info['x_pixel_size'], info['y_pixel_size'], info['z_step_size']
    
    # それぞれの単一長さをかけて立体の体積を出す
    volume = elements_n * x_one_pixel_size * y_one_pixel_size * z_one_step_size
    
    # 縮小率を算定
    scale_factor = (new_volume / volume) ** (1/3)
    
    # xの縮小率を算定
    x_before_length = x_one_pixel_size * x_before_pixel_n 
    x_after_pixel_n = x_before_length * scale_factor / AFTER_PIXEL_SIZE
    x_rate = x_after_pixel_n / x_before_pixel_n
    
    # yの縮小率を算定
    y_before_length = y_one_pixel_size * y_before_pixel_n
    y_after_pixel_n = y_before_length * scale_factor / AFTER_PIXEL_SIZE
    y_rate = y_after_pixel_n / y_before_pixel_n
    
    # xの縮小率を算定
    z_before_length = z_one_step_size * z_before_pixel_n
    z_after_pixel_n = z_before_length * scale_factor / AFTER_PIXEL_SIZE
    z_rate = z_after_pixel_n / z_before_pixel_n
    
    zoom_factors = (z_rate,y_rate,x_rate)

    # 拡大
    expanded_array = zoom(arr, zoom_factors, order=0)
    
    # 不要な部分を削除する
    bounding_array = get_bounding_box(expanded_array)

    return bounding_array


def get_bounding_box(arr:np.ndarray) -> np.ndarray:
    """
    与えられた立体図形を表す配列の周囲で0しかない部分を削除する

    Parameters
    ----------
    arr : np.ndarray
        修正する三次元配列

    Returns
    -------
    np.ndarray
        修正した三次元配列
    """
    
    # 非ゼロ要素のインデックスを取得
    non_zero_indices = np.nonzero(arr)

    # 各軸に対する最小および最大のインデックスを取得
    min_z, min_y, min_x = np.min(non_zero_indices, axis=1)
    max_z, max_y, max_x = np.max(non_zero_indices, axis=1)
    
    # 立体を切り取る
    bounding_arr = arr[min_z:max_z +1 , min_y:max_y + 1, min_x:max_x + 1]
    
    return bounding_arr
    