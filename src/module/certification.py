import argparse
import pandas as pd
import numpy as np
from scipy import stats

from libs.global_function import mkdir_if_none
from libs.input import get_params

def welch(array1, array2):
    return stats.ttest_ind(array1, array2, equal_var=False)

def certification_func(brain1_li, brain2_li):
    csv_path = get_params('coordinate_csv_path')
    coordinate_df = pd.read_csv(csv_path)
    
    # 1-1_GAP43に存在しない箇所を対象から除外
    coordinate_df = coordinate_df[coordinate_df['1-1_GAP43'] != 0]
    
    coordinate_df = coordinate_df.set_index("coordinate", drop=True)
    
    # liごとの検定に使用する情報を取得
    brain1_dic = coordinate_df[brain1_li].T.to_dict(orient="list")
    brain2_dic = coordinate_df[brain2_li].T.to_dict(orient="list")
    
    # 座標ごとに検定を行う
    result_dic = {}
    coor_li = brain1_dic.keys()
    
    for coor in coor_li:
        array1 = np.array(brain1_dic[coor])
        array2 = np.array(brain2_dic[coor])
        
        result = welch(array1, array2)
        result_dic[coor] = {'t': result[0],
                            'p': result[1]}
    
    # 結果をデータフレームに変形
    df_result = pd.DataFrame(result_dic).T
    df_result = df_result[df_result['p'] < 0.05] # 有意差があるもののみ保存
    df_result = df_result.reset_index()
    df_result = df_result.rename(columns={'index': 'coordinate'})
    
    return df_result

if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(description='''
    	brains1とbrains2について検定
    	''')
    parser.add_argument('brains1_name', help='')
    parser.add_argument('brains2_name', help='')
    
    args = parser.parse_args()
    
    brain1_name = args.brains1_name
    brain2_name = args.brains2_name
    
    brain1_path_li = get_params(brain1_name)
    brain2_path_li = get_params(brain2_name)
    
    brain1_li = [path.split("/")[-1] for path in brain1_path_li]
    brain2_li = [path.split("/")[-1] for path in brain2_path_li]
    
    result_df = certification_func(brain1_li, brain2_li)
    
    # 保存
    dir_path = get_params('certification_csv_dir_path')
    mkdir_if_none(dir_path)
    save_path = f'{dir_path}/certification_{brain1_name}_vs_{brain2_name}.csv'
    result_df.to_csv(save_path, index=False)
    