from webcolors import name_to_rgb
import os
import datetime

def mkdir_if_none(path: str) -> None:
    """パスのディレクトリがない場合は作る
    ある場合はスルー

    Parameters
    ----------
    path : str
        判定するディレクトリのパス
    """
    if not os.path.exists(path):
        os.mkdir(path)

class GetInfo:
    """
    現在どの段階にいるかを出力するためのクラス
    """

    def __init__(self, input_li,show_flag = True):
        self.show_flag = show_flag
        self.input_li = input_li
        self.len_li = [len(temp) for temp in self.input_li]
        max_len = max(self.len_li)
        self.input_li = [temp + ' ' * (max_len - len(temp))
                         for temp in self.input_li]
        self.state_dic = {}
        for i, temp in enumerate(self.input_li):
            if not i:
                self.state_dic[temp] = self.get_color_and_time(
                    f'In progress', 'blue', time_flag=False)
            else:
                self.state_dic[temp] = self.get_color_and_time(
                    'Not implemented', 'green', time_flag=False)
        self.complete_n = 0
        self.move_n = len(self.input_li) + 2
        self.show_info()

    def move_cursor(self, n):
        if self.show_flag:
            print(f'\033[{n + 1}A')

    def show_info(self):
        if self.show_flag:
            print('=' * 70)
            for key, value in self.state_dic.items():
                print(f'{key} : {value}')
            print('=' * 70)

    def one_end(self):
        self.state_dic[self.input_li[self.complete_n]] = self.get_color_and_time(
            f'Completed', 'yellow')
        if self.complete_n + 1 <= len(self.input_li) - 1:
            self.state_dic[self.input_li[self.complete_n + 1]
                           ] = self.get_color_and_time(f'In progress', 'blue', time_flag=False)
        self.move_cursor(self.move_n)
        self.show_info()
        self.complete_n += 1

    def get_color_and_time(self, x, color, time_flag=True, a=20):
        color_dic = {'green': '32',
                     'blue': '34',
                     'yellow': '33'}
        START = f'\033[{color_dic[color]}m'
        END = '\033[0m'
        if time_flag:
            x = x + f' [{self.making_now_date()}]'
        else:
            x = x + ' ' * a
        return START + x + END

    def making_now_date(self):
        dt_now = datetime.datetime.now()
        return dt_now.strftime('%m/%d %H:%M:%S')