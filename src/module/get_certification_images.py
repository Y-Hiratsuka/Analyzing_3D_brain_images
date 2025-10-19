import pandas as pd
import numpy as np
import subprocess
import math
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np

from libs.output import save_images_func
from libs.global_function import mkdir_if_none
from libs.overlap import overlap_func
# import matplotlib.pyplot as plt

def coordinate_reshape(coordinate_text):
    li = coordinate_text.split('.')
    x = int(li[0].replace("x",''))
    y = int(li[1].replace("y",''))
    z = int(li[2].replace("z",''))
    
    return {
        'x': x,
        'y': y,
        'z': z
    }

def get_gradation_number(n, limit = 0.05):
    return (limit - n ) / limit

def get_new_gradation_number(n, limit= 10):
    if n > 0.05:
        return 0
    
    score =  - math.log10(n)
    if score > limit:
        return 1
    else:
        return score / limit

def get_color(value):

        
    norm = mcolors.Normalize(vmin=-1, vmax=1)
    cmap = plt.cm.Spectral_r
    rgba_color = cmap(norm(value))
    # Convert RGBA to RGB
    rgb_color = tuple(int(rgba_color[i] * 255) for i in range(3))
    
    bgr_color = np.array([rgb_color[2],rgb_color[1],rgb_color[0]])
    return bgr_color


def certification_images_func(csv_path,save_dir, factor = 1):
    # 検定結果の読み込み
    df = pd.read_csv(csv_path).set_index('coordinate')
    cert_dic = df.to_dict(orient='index')
    
    # 初期配列の設定
    cert_array = np.zeros((60//factor,100//factor,120// factor,3))

    for coordinate in cert_dic:
        # 平均の差分値と，P値の取得
        t = cert_dic[coordinate]['t']
        p = cert_dic[coordinate]['p']
        
        # P値の結果からグラデーションの値を出力
        p_gradation_n = get_new_gradation_number(p,limit= 3)
        
        # 座標データの変形
        position = coordinate_reshape(coordinate)
        
        # 値の設定
        #!  cv2はBGR形式である．t正で赤になるようになっている
        if t > 0:
            cert_array[position['z']][position['y']][position['x']] \
                    = get_color(p_gradation_n)
        elif t < 0:
            cert_array[position['z']][position['y']][position['x']] \
                    = get_color( - p_gradation_n)
        else:
            cert_array[position['z']][position['y']][position['x']] \
                    = np.array([0,0,0])
    
    # 基準画像を重ね合わせ
    cert_array = overlap_func(cert_array)
    
    mkdir_if_none(save_dir)    
    save_images_func(cert_array,save_dir)

if __name__ == '__main__':
    '''
    検定の結果を視覚的に表示するためのもの
    '''
    import argparse
    parser = argparse.ArgumentParser(description='''
        検定結果を視覚化する
    	#TODO EXAMPLE: python ....
    ''')
    parser.add_argument('csv_path', help='検定結果のcsvファイルを作成')
    
    args = parser.parse_args()
    
    csv_path = args.csv_path
    
    save_dir = csv_path.split('.')[0]
    
    # 検定結果のcsvから検定の可視化画像を出力
    certification_images_func(csv_path=csv_path,
                              save_dir=save_dir,
                              factor=1)
    
    # mkdir_if_none(f"{save_dir}_overlap")
    # subprocess.run(
    #         ['python', 'brain-image-processing/get_block.py',
    #           save_dir,standard_brain_path,
    #           f"{save_dir}_overlap"])
    subprocess.run([
        'python',
        "src/module/add_color_bar.py",save_dir,save_dir
    ])