import argparse
import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt

from libs.global_function import mkdir_if_none
from libs.input import get_params
from libs.verification import hierarchical_bootstrap_test

def welch(array1, array2):
    return stats.ttest_ind(array1, array2, equal_var=False)

def area_verification_func(brain1_li, brain2_li):
    csv_path = get_params('coordinate_csv_path')
    coordinate_df = pd.read_csv(csv_path)
    
    # 1-1_GAP43に存在しない箇所を対象から除外
    coordinate_df = coordinate_df[coordinate_df['1-1_GAP43'] != 0]
    
    coordinate_df = coordinate_df.set_index("coordinate", drop=True)
    
    # 指定されたエリアのみに限定
    coordinate_df = coordinate_df[coordinate_df['cutting'] == 1]
    
    
    # それぞれの群のリストを取得
    brain1_array = np.array(coordinate_df[brain1_li].T.values.tolist())
    brain2_array = np.array(coordinate_df[brain2_li].T.values.tolist())
    
    result = hierarchical_bootstrap_test(ko=brain1_array,
                                             wt=brain2_array,)
    
    return result

def area_verification_box_fig_func(
    brain1_li, brain2_li,save_path,
    brain1_label="Group1", brain2_label="Group2",
    B=5000, ci=0.95
):

    # ---- データ読み込みと前処理 ----
    csv_path = get_params('coordinate_csv_path')
    coordinate_df = pd.read_csv(csv_path)

    # 1-1_GAP43 に存在しない箇所を除外
    coordinate_df = coordinate_df[coordinate_df['1-1_GAP43'] != 0]

    # 指定エリアのみ
    coordinate_df = coordinate_df[coordinate_df['cutting'] == 1]

    # 行=ボクセル名に
    coordinate_df = coordinate_df.set_index("coordinate", drop=True)

    # ---- 検定用の配列化（行=ボクセル, 列=脳名 → 転置して (個体, ボクセル) へ）----
    # ここはあなたの元コードを踏襲
    brain1_array = np.array(coordinate_df[brain1_li].T.values.tolist())  # shape: (n1, n_vox)
    brain2_array = np.array(coordinate_df[brain2_li].T.values.tolist())  # shape: (n2, n_vox)

    # ---- 階層型ブートストラップ検定（平均固定・p値はシフトブート）----
    result = hierarchical_bootstrap_test(
        ko=brain1_array,
        wt=brain2_array,
        B=B,
        ci=ci,
    )

    # 行=ボクセルで列=脳名なので、axis=0 で各列の平均
    means1 = coordinate_df[brain1_li].mean(axis=0, skipna=True)  # pd.Series(index=brain1_li)
    means2 = coordinate_df[brain2_li].mean(axis=0, skipna=True)  # pd.Series(index=brain2_li)

    # 図示用データ（長い形式）
    per_brain_means_df = pd.DataFrame({
        "brain": list(means1.index) + list(means2.index),
        "mean_intensity": np.concatenate([means1.values, means2.values]),
        "group": [brain1_label]*len(means1) + [brain2_label]*len(means2),
    })

    # ---- 箱ひげ図＋個体点 ----
    fig, ax = plt.subplots(figsize=(6, 4))

    # 箱ひげ
    ax.boxplot(
        [means1.values, means2.values],
        tick_labels=[brain1_label, brain2_label],
        showfliers=False
    )



    ax.set_ylabel("Mean voxel intensity")
    ax.set_title("Comparison of brain-averaged voxel intensity")
    ax.grid(alpha=0.3)

    # 参考に検定結果をサブタイトル等で添える（任意）
    ax.set_xlabel(f"hierarchical bootstrap test: KO−WT={result['observed_effect']:.3f}, "
                  f"95%CI=[{result['ci_low']:.3f}, {result['ci_high']:.3f}], "
                  f"p={result['p_value']:.3g}")

    fig.savefig(save_path)
    return result, fig, ax, per_brain_means_df
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
    
    area_verification_box_fig_func(brain1_li, brain2_li,
                                   save_path=f'result/area_verification_{brain1_name}_vs_{brain2_name}.png',
                 brain1_label=brain1_name,brain2_label=brain2_name)
    exit()
    result = area_verification_func(brain1_li, brain2_li)
    
    print("=== 階層型ブートストラップ検定 結果 ===")
    print(f"観測効果量 (KO−WT) : {result['observed_effect']:.3f}")
    print(f"95%信頼区間 : [{result['ci_low']:.3f}, {result['ci_high']:.3f}]")
    print(f"両側p値 : {result['p_value']:.4f}")