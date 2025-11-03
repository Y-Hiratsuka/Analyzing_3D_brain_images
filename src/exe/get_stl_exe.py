import subprocess
import pandas as pd

from libs.input import get_params
from libs.global_function import GetInfo


CSV_PATH = get_params('brains_csv_path')
df = pd.read_csv(CSV_PATH)
brain_name_li = df['brain_name'].to_list()

dir_name = get_params('corrected_images_dir_path')

info = GetInfo(brain_name_li)

for brain_name  in brain_name_li:
    brain_image_dir_path = f'{dir_name}/{brain_name}/normalize_images'
    save_path = f'{dir_name}/{brain_name}/{brain_name}.stl'
    subprocess.run(['python', 'src/module/get_stl.py',brain_image_dir_path,save_path])
    info.one_end()