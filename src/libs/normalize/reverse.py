import numpy as np

def get_reversal_images(arrays:np.ndarray)->np.ndarray:
    """
    渡された画像群の三次元配列の左右を反転させるコード

    Parameters
    ----------
    arrays : np.ndarray
        反転させる画像の三次元配列

    Returns
    -------
    np.ndarray
        反転させた画像の三次元配列
    """
    mirrored_arrays = np.array([np.fliplr(array) for array in arrays])
    return mirrored_arrays