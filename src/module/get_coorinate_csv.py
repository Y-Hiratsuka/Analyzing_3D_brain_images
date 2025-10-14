import pandas as pd

from libs.images_to_csv import get_cutting_array_func, images_to_dic_func
from libs.global_function import GetInfo
from libs.input import get_params

def get_init_dataframe():
    cutting_array = get_cutting_array_func()
    coordinate_dic = {}
    for z in range(60):
        for y in range(100):
            for x in range(120):
                coordinate_dic[f"x{x}.y{y}.z{z}"] = {
                    "x": x,
                    "y": y,
                    "z": z,
                    "cutting": cutting_array[z][y][x]
                }
    return coordinate_dic
    
def significant_diff_func():
    #! Do the final one again at the end
    
    # 初期の辞書の作成．有効エリアの情報を取得
    result_dic = get_init_dataframe()

    all_brain_li = get_params('all_brain_name_li')
    info = GetInfo(all_brain_li)
    # pathそれぞれに対する座標情報を取得
    
    for brain_name in all_brain_li:
        
        result_dic = images_to_dic_func(result_dic,brain_name)
        info.one_end()
        
    df = pd.DataFrame(result_dic).T
    df = df.reset_index()
    df = df.rename(columns={'index': 'coordinate'})
    df.to_csv(get_params("coordinate_csv_path"),index=False)
    pass

if __name__ == '__main__':
    '''
    それぞれの画像が有意差があるか検証する
    '''
    # import argparse
    # parser = argparse.ArgumentParser(description='''
    # 	#! Write a description for your future self
    #	#TODO EXAMPLE: python ....
    # 	''')
    # parser.add_argument('', help='')
    # parser.add_argument('-f', '--flag', action='store_true')
    # parser.add_argument('-a', '--alpha', type=float, default=0.01) 
    # args = parser.parse_args()
    
    significant_diff_func()