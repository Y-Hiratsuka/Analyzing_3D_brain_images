import numpy as np
import math

def move_gravity(array:np.ndarray) -> np.ndarray:
    """
    重心を中央に移動する
    ただし，補整前と補整後のサイズは一致しないことに注意
    
    Parameters
    ----------
    array : np.ndarray
        補整前の三次元配列

    Returns
    -------
    np.ndarray
        補整後の三次元配列
    """
    def get_shift(s:float) -> tuple:
        """
        移動したい距離から，追加する余白の量を算出 
        重心を右にX移動することは,左に2Xの余白を追加することで擬似的に実現することができる
        
        Parameters
        ----------
        s : float
            移動する距離

        Returns
        -------
        tuple
            （正の方向に追加する量，負の方向に追加する量）
        """
        abs_s = abs(s)
        if s > 0:
            return (math.ceil(abs_s * 2), 0)
        else:
            return (0, math.ceil(abs_s * 2))
    
    # np.nonzeroを用いて、0でない要素のインデックスを取得します。
    indices = np.nonzero(array)
    
    # np.meanを用いて、各軸についてのインデックスの平均を計算し、これを重心とします。
    center_of_mass = np.mean(indices, axis=1)
    
    # 真ん中の座標を求めます。
    center = np.array(array.shape) / 2
    
    # 重心が真ん中に来るように移動させるための差分を計算します。
    shift_size = center - center_of_mass
    
    # 加える余白を作成
    #? 重心を右にX移動することは，左に2Xの余白を追加することで擬似的に実現することができる
    pad_width = [get_shift(temp) for temp in shift_size]
    
    # 余白を追加し，擬似的に重心を移動する
    padding_array = np.pad(array, pad_width=pad_width,
                   mode='constant', constant_values=0)
    
    return padding_array
