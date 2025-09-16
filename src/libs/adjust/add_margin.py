import numpy as np
from scipy.ndimage import zoom

def add_margin(array1:np.ndarray,array2: np.ndarray,zoom_rate = 0.25) -> tuple:
    """
    与えられた二つの配列に対して十分な余白をつける

    Parameters
    ----------
    array1 : np.ndarray
        一つ目の配列
    array2 : np.ndarray
        二つ目の配列

    Returns
    -------
    tuple
        余白をつけた二つの配列をタップルで返す
    """
    
    # 形状を取得
    shape1, shape2 = array1.shape,array2.shape
    
    # それぞれの軸方向の大きい方の2倍を変更後の形状とする
    max_size = max(max(shape1,shape2))
    # after_shape = (max(shape1[0],shape2[0]) * 2,
    #              max(shape1[1],shape2[1]) * 2,
    #              max(shape1[2], shape2[2]) * 2)
    # print(shape1,shape2)
    after_shape = (max_size * 2,
                   max_size * 2,
                   max_size * 2)
    # 余白の大きさを計算
    pad_width1 = [(int((after - before) / 2), (after - before) - int((after - before) / 2))
                for before, after in zip(shape1,after_shape)]
    pad_width2 = [(int((after - before) / 2), (after - before) - int((after - before) / 2))
                for before, after in zip(shape2,after_shape)]

    # 余白をつける
    padding_array1 = np.pad(array1, pad_width=pad_width1,
                           mode='constant', constant_values=0)
    padding_array2 = np.pad(array2, pad_width=pad_width2,
                           mode='constant', constant_values=0)
    

    # # ８分の1に変換
    zoom_factors = (zoom_rate, zoom_rate, zoom_rate)
    padding_array1 = zoom(padding_array1, zoom_factors, order=0)
    padding_array2 = zoom(padding_array2, zoom_factors, order=0)
    return padding_array1,padding_array2