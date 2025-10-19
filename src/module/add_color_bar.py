import cv2
import glob

from libs.certification import make_color_bar_func
from libs.input import get_params
from libs.global_function import mkdir_if_none, get_path_name

def stack_images_with_fixed_width(image1_path, text,image2_path = get_params("color_bar_path")):
    """
    画像1の横幅に合わせて画像2をリサイズし、縦に重ねる関数。
    
    Parameters:
    - image1_path: str, 最初の画像のパス
    - image2_path: str, 二番目の画像のパス
    
    Returns:
    - stacked: numpy.ndarray, 縦に結合された画像
    """
    # 画像を読み込む
    img1 = cv2.imread(image1_path, cv2.IMREAD_UNCHANGED)
    img1 = cv2.resize(img1, (img1.shape[1] * 5, img1.shape[0] * 5), interpolation=cv2.INTER_LINEAR)
    img2 = cv2.imread(image2_path, cv2.IMREAD_UNCHANGED)

    # アルファチャネルが存在する場合は取り除く（必要に応じて）
    if img1.shape[2] == 4:
        img1 = cv2.cvtColor(img1, cv2.COLOR_BGRA2BGR)
    if img2.shape[2] == 4:
        img2 = cv2.cvtColor(img2, cv2.COLOR_BGRA2BGR)

    # 画像2を画像1の横幅に合わせてリサイズ
    width = img1.shape[1]
    ratio = width / img2.shape[1]
    new_height = int(img2.shape[0] * ratio)
    img2_resized = cv2.resize(img2, (width, new_height), interpolation=cv2.INTER_LINEAR)

    # 画像を縦に結合
    stacked = cv2.vconcat([img1, img2_resized])
    # テキストを追加
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 1.5  # フォントサイズ
    font_color = (255, 255, 255)  # 白色
    font_thickness = 2  # フォントの太さ
    text_x = 50  # 左端から10ピクセル
    text_y = 60  # 上端から30ピクセル（フォントサイズによる高さを考慮）

    cv2.putText(stacked, text, (text_x, text_y), font, font_scale, font_color, font_thickness)

    return stacked

if __name__ == '__main__':
    '''
    写真にカラーバーを配置する
    '''
    import argparse
    parser = argparse.ArgumentParser(description='''
    	画像郡にカラーバーを下につける．その際に画像は拡大されることに注意
    	''')
    parser.add_argument('dir_path', help='')
    parser.add_argument('save_dir', help='')
    args = parser.parse_args()
    
    dir_path = args.dir_path
    save_dir = args.save_dir
    
    # カラーバーの作成
    make_color_bar_func()
    
    
    path_li = glob.glob(f'{dir_path}/*.png')
    mkdir_if_none(save_dir)
    
    for path in path_li:
        save_path = f'{save_dir}/{get_path_name(path,-1)}'
        img = stack_images_with_fixed_width(path,f"Z:{int(get_path_name(path, -1, extension=False))}")
        cv2.imwrite(save_path,img)