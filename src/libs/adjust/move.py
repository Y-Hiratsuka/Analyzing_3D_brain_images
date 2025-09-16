import numpy as np
from scipy import interpolate

def shift_array(array, shift):
    """
    与えられた3D NumPy配列を指定された実数のシフト量で移動させる関数

    Parameters:
    - array (numpy.ndarray): 3D NumPy配列
    - shift (tuple or list): シフト量を示す3つの要素を持つタプルまたはリスト（z, y, x）

    Returns:
    - numpy.ndarray: シフト後の新しい3D NumPy配列
    """

    # 配列の形状を取得
    array_shape = array.shape

    # 元の配列のグリッドを作成
    z, y, x = np.mgrid[0:array_shape[0], 0:array_shape[1], 0:array_shape[2]]

    # シフト後のグリッドを計算
    new_z = z + shift[0]
    new_y = y + shift[1]
    new_x = x + shift[2]

    # 3D補間オブジェクトを作成
    interpolator = interpolate.RegularGridInterpolator(
        (z[:, 0, 0], y[0, :, 0], x[0, 0, :]), array, bounds_error=False, fill_value=0)

    # 新しいグリッドの点での配列の値を補間
    shifted_array = interpolator((new_z, new_y, new_x))

    return shifted_array