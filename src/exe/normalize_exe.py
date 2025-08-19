import subprocess
import pandas as pd

from libs.input import get_params
from libs.global_function import GetInfo


CSV_PATH = get_params('brains_csv_path')
df = pd.read_csv(CSV_PATH)
brain_name_li = df['brain_name'].to_list()

info = GetInfo(brain_name_li)

for brain_name  in brain_name_li:
    subprocess.run(['python', 'src/module/normalize.py',brain_name])
    info.one_end()