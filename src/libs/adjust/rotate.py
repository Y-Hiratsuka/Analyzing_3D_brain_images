import numpy as np
from scipy.ndimage import rotate


def rotate_3d(data: np.ndarray,angle_list: list) -> np.ndarray:
    """
    立体を回転させる

    Parameters
    ----------
    data : np.ndarray
        回転させる立体を指定
    angle_list : list
        xyz軸それぞれの角度を指定
        ex [0,0,0]

    Returns
    -------
    np.ndarray
        回転した立体を返す
    """
    
    # 受け取り
    angle_x, angle_y, angle_z = angle_list
    # x軸周りの回転
    data_rot_x = rotate(data, angle_x, axes=(0,1), reshape=False)

    # y軸周りの回転
    data_rot_xy = rotate(data_rot_x, angle_y, axes=(0,2), reshape=False)

    # z軸周りの回転
    data_rot_xyz = rotate(data_rot_xy, angle_z, axes=(1,2), reshape=False)

    return data_rot_xyz