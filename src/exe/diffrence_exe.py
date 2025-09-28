import subprocess
import pandas as pd

from libs.input import get_params
from libs.global_function import GetInfo,mkdir_if_none

category_combination_li = get_params("category_combination")
mean_dir = get_params('mean_dir_path')
diff_dir_path = get_params('diff_dir_path')
mkdir_if_none(diff_dir_path)
info = GetInfo([f'{comb[0]}_vs_{comb[1]}' 
                for comb in category_combination_li])

for comb  in category_combination_li:
    
    path1 = f'{mean_dir}/{comb[0]}'
    path2 = f'{mean_dir}/{comb[1]}'
    save_path = f'{diff_dir_path}/{comb[0]}_vs_{comb[1]}'
    
    subprocess.run(['python', 'src/module/difference.py',
                    path1,path2,save_path])
    
    info.one_end()