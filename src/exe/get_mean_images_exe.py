import subprocess
import pandas as pd

from libs.input import get_params
from libs.global_function import GetInfo


category_li = get_params("category_name_li")
# info = GetInfo(category_li)

for category_name  in category_li:
    subprocess.run(['python', 'src/module/get_mean_images.py',category_name])
    # info.one_end()