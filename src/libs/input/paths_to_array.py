import numpy as np
import cv2


def path_to_gray_image(path: str) -> np.ndarray:
    """パスをグレイスケールに変換

    Parameters
    ----------
    path : str
        変換するパスを指定

    Returns
    -------
    np.ndarray
        グレイスケールに変換された画像の三次元配列を返す
    """
    image = cv2.imread(path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return gray

def paths_to_3d_gray_array(paths:list) ->np.ndarray:
    """パスのリストを三次元配列に変換するコードです

    Parameters
    ----------
    paths : list
        変換するパスのリストを指定

    Returns
    -------
    np.ndarray
        変換した三次元配列を返す
    """
    # パスを画像に変換
    rgba_arrays = [path_to_gray_image(path) for path in paths]
    # Noneのものを排除
    rgba_arrays = [[array] for array in rgba_arrays if array is not  None]
    # それぞれの結合
    arr = np.concatenate(rgba_arrays)
    return arr