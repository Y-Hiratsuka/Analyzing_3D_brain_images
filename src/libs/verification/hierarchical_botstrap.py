import numpy as np

def hierarchical_bootstrap_test(
    ko: np.ndarray,
    wt: np.ndarray,
    B: int = 5000,
    ci: float = 0.95,
) -> dict:
    """
    階層型ブートストラップ検定（平均固定・シード固定なし）

    【概要】
    個体（subject）内に複数のボクセル（voxel）データがあるような
    階層構造データに対して、KO群とWT群の差を非パラメトリックに検定する。

    【入力】
    ko, wt : np.ndarray
        各群のデータ。形状は (個体数, ボクセル数)。
        各行が1個体、各列がボクセルの染色強度など。
    B : int
        ブートストラップの繰り返し回数（通常2000〜10000）。
    ci : float
        信頼区間の信頼度（例：0.95）。

    【出力】
    dict 型の辞書を返す：
        observed_effect : 観測効果量（KO群−WT群）
        ci_low, ci_high : 信頼区間（パーセンタイル法）
        p_value : 両側p値（帰無分布に基づく）
        boot_effects : 観測分布の効果量
    """

    # 乱数生成器（固定シードなし）
    rng = np.random.default_rng()

    # numpy配列に変換
    ko = np.asarray(ko, dtype=float)
    wt = np.asarray(wt, dtype=float)
    n_subj_ko, n_vox_ko = ko.shape
    n_subj_wt, n_vox_wt = wt.shape

    # 実際の観測効果量（KO群−WT群）
    ko_subj = np.mean(ko, axis=1)  # 個体内平均
    wt_subj = np.mean(wt, axis=1)
    obs_effect = np.mean(ko_subj) - np.mean(wt_subj)

    # ---------- 階層型ブートストラップ（観測分布） ----------
    effects = np.empty(B)
    for b in range(B):
        idx_ko = rng.integers(0, n_subj_ko, size=n_subj_ko)
        idx_wt = rng.integers(0, n_subj_wt, size=n_subj_wt)
        ko_b = [np.mean(rng.choice(ko[i], size=n_vox_ko, replace=True)) for i in idx_ko]
        wt_b = [np.mean(rng.choice(wt[j], size=n_vox_wt, replace=True)) for j in idx_wt]
        effects[b] = np.mean(ko_b) - np.mean(wt_b)

    # 信頼区間
    alpha = 1 - ci
    lo, hi = np.quantile(effects, [alpha/2, 1 - alpha/2])

    # ---------- p値（帰無仮説: 群差=0 に基づくシフト・ブートストラップ） ----------
    g_ko = np.mean(ko_subj)
    g_wt = np.mean(wt_subj)
    grand = (g_ko + g_wt) / 2
    shift_ko = grand - g_ko
    shift_wt = grand - g_wt
    ko_null = ko + shift_ko
    wt_null = wt + shift_wt

    effects_null = np.empty(B)
    for b in range(B):
        idx_ko = rng.integers(0, n_subj_ko, size=n_subj_ko)
        idx_wt = rng.integers(0, n_subj_wt, size=n_subj_wt)
        ko_b = [np.mean(rng.choice(ko_null[i], size=n_vox_ko, replace=True)) for i in idx_ko]
        wt_b = [np.mean(rng.choice(wt_null[j], size=n_vox_wt, replace=True)) for j in idx_wt]
        effects_null[b] = np.mean(ko_b) - np.mean(wt_b)

    # 両側p値
    p_two = (np.sum(np.abs(effects_null) >= np.abs(obs_effect)) + 1) / (B + 1)

    # 出力
    return {
        "observed_effect": float(obs_effect),
        "ci_low": float(lo),
        "ci_high": float(hi),
        "p_value": float(p_two),
        "boot_effects": effects,
        "settings": {
            "B": B,
            "ci": ci,
            "method": "mean固定・シフトブートストラップp値",
        },
    }
