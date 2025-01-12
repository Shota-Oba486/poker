import tkinter as tk
from PIL import Image, ImageTk

def load_image(card_path, size):
    """画像をロードしてリサイズ"""
    card = Image.open(card_path)
    card = card.resize(size)
    return ImageTk.PhotoImage(card)

def create_transparent_black_image(width, height,trans_rate = 128):
    # 半透明な黒の画像を作成
    img = Image.new("RGBA", (width, height), (0, 0, 0, trans_rate))  # (R, G, B, A)で透明度128
    return img

def create_rounded_rectangle(canvas, x1, y1, x2, y2, radius=25, **kwargs):
    """角丸の長方形を描画する"""
    points = [
        x1 + radius, y1,
        x2 - radius, y1,
        x2, y1,
        x2, y1 + radius,
        x2, y2 - radius,
        x2, y2,
        x2 - radius, y2,
        x1 + radius, y2,
        x1, y2,
        x1, y2 - radius,
        x1, y1 + radius,
        x1, y1
    ]
    return canvas.create_polygon(points, smooth=True, **kwargs)

def card_to_path(card,bright=True):
    rank_to_num = {'A': 1, 'K': 13, 'Q': 12, 'J': 11, 'T': 10, '9': 9, '8': 8, '7': 7, '6': 6, '5': 5, '4': 4, '3': 3,'2': 2}
    num,suit = card[0],card[1]
    num = str(rank_to_num[num])
    card_str = suit + num
    if bright:
        card_path = "gui/images/cards/bright/" + card_str + ".png"
    else:
        card_path = "gui/images/cards/dark/" + card_str + ".png"
    return card_path

def move_obj(canvas, root, obj, current_coords, target_coords, duration):
    """
    オブジェクトを目的地まで指定された時間で移動させる。

    Args:
        obj: 移動させるオブジェクト
        current_coords: 現在の座標 [x, y]
        target_coords: 目的地点 [x, y]
        duration: 移動にかける時間（m秒）
    """
    # フレームレート（何ミリ秒ごとに更新するか）
    interval = 3  # 3ms
    steps = duration // interval  # 合計ステップ数

    # 移動距離を計算
    dx = target_coords[0] - current_coords[0]
    dy = target_coords[1] - current_coords[1]

    # 1ステップごとの移動量
    step_x = dx / steps
    step_y = dy / steps

    def update():
        nonlocal steps
        if steps <= 0:  # 終了条件
            remaining_dx = target_coords[0] - current_coords[0]
            remaining_dy = target_coords[1] - current_coords[1]
            canvas.move(obj, remaining_dx, remaining_dy)
            return

        # オブジェクトを移動
        canvas.move(obj, step_x, step_y)
        current_coords[0] += step_x
        current_coords[1] += step_y
        steps -= 1

        # 次のフレームで再び呼び出し
        root.after(interval, update)

    # 初回の呼び出し
    update()
