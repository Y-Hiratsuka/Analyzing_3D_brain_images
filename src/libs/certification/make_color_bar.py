import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

from libs.input import get_params

def make_color_bar_func():
    #! Do the final one again at the end
    # ダミーデータの生成
    data = np.random.rand(10, 10)

    # グラフを描画する
    # カラーマップの作成
    cmap = mpl.cm.Spectral_r
    # 新しいカラーマップの定義
    colors = cmap(np.linspace(0, 1, 256))
    total = 256  # カラーマップの色数
    start = int((-1.301 - 3) / 6  * total)  # -0.3 に相当するインデックス
    end = int((1.301 + 3) / 6 * total)  # 0.3 に相当するインデックス
    colors[start:end] = (0, 0, 0, 1)  # 白色に設定

    # 新しいカラーマップの作成
    cmap = mpl.colors.LinearSegmentedColormap.from_list("ModifiedSpectral", colors)
        # Normalizeオブジェクトの作成（ここでは0から1までとする）
    norm = mpl.colors.Normalize(vmin=-3, vmax=3)

    # カラーバーの作成
    fig, ax = plt.subplots(figsize = (8,2))
    fig.patch.set_facecolor('black')  # 図の背景色を黒に設定
    ax.patch.set_facecolor('black')  # 軸の背景色も黒に設定
    cbar = fig.colorbar(mpl.cm.ScalarMappable(norm=norm, cmap=cmap),
                 cax=ax, orientation='horizontal',label = 'p score')
    # カラーバーの目盛り位置とラベルの設定
    cbar.set_ticks([-3,-2, -1.301,0, 1.301,2, 3])
    cbar.set_ticklabels(['10^-3',"10^-2","0.05",  'significant difference zorn',"0.05",'10^-2' ,'10^-3'])
    # cbar.ax.tick_params(labelsize=36)  # フォントサイズを12に設定
    ax.set_aspect(0.05) 
    plt.title('←lower   KO(compared to WILD)   higher→',color='white')
    
    # カラーバーとラベルの文字色を白に変更
    cbar.set_label('P score', color='white')
    cbar.outline.set_edgecolor('white')
    cbar.ax.tick_params( colors='white')  # メモリの文字色を白に設定
    
    save_path = get_params('color_bar_path')
    plt.savefig(save_path)
    