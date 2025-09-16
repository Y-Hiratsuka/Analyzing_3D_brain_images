import numpy as np


def change_shape(array: np.ndarray, after_shape: tuple) -> np.ndarray:
    """
    配列を中心維持したまま，指定された形状に変更する

    Parameters
    ----------
    array : np.ndarray
        形状を変更する配列
    after_shape : tuple
        新しい形状

    Returns
    -------
    np.ndarray
        形状を変更した配列
    """
    old_shape = array.shape
    # 余白の大きさを計算
    pad_width2 = [(int((after - before) / 2), (after - before) - int((after - before) / 2))
                  for before, after in zip(old_shape, after_shape)]
    
    # 余白をつける数値を設定
    padding_width = [(temp[0],temp[1])if temp[0] > 0 else (0,0) for temp in pad_width2 ]
    
    # 切り取る数値を設定
    cut_width = [(- temp[0], -temp[1]) if temp[0] <= 0 else (0, 0) for temp in pad_width2]

    
    # 余白をつける

    padding_array2 = np.pad(array, pad_width=padding_width,
                            mode='constant', constant_values=0)

    
    #  切り取る
    padding_array2 = padding_array2[cut_width[0][0]:padding_array2.shape[0] - cut_width[0][1],
                                    cut_width[1][0]:padding_array2.shape[1] - cut_width[1][1],
                                    cut_width[2][0]:padding_array2.shape[2] - cut_width[2][1]]
    


    return padding_array2
