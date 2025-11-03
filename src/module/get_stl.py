import argparse
import numpy as np
from stl import mesh
from skimage.measure import marching_cubes

from libs.input import dir_to_array

def get_stl_file(dir_path: str, save_path: str) -> None:
    """
    パスで指定されたディレクトリ内の二次元画像群をstlファイルに保存する

    Parameters
    ----------
    dir_path : str
        変換するディレクトリ
    save_path : str
        保存パスを指定
    """
    
    # データの入力
    arr = dir_to_array(dir_path)
    # メッシュの構成
    verts, faces, _, _ = marching_cubes(arr, level=0)
    mesh_data = mesh.Mesh(np.zeros(faces.shape[0], dtype=mesh.Mesh.dtype))
    for i, f in enumerate(faces):
        for j in range(3):
            mesh_data.vectors[i][j] = verts[f[j], :]
            
    # 保存
    mesh_data.save(save_path)
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='''
        ディレクトリに保存された二次元画像群をstlファイルとして出力する
        ''')
    parser.add_argument("dir_path", help="dir_path")
    parser.add_argument("save_path", help="save_path")

    args = parser.parse_args()
    dir_path = args.dir_path
    save_path = args.save_path
    
    get_stl_file(dir_path=dir_path,
                 save_path=save_path)