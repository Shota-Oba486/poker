import tkinter as tk
from functools import partial
from PIL import Image, ImageTk
import random
from gui.function import load_image
from gui.function import create_transparent_black_image
from gui.function import card_to_path

class Home:
    def __init__(self, root, switch_game_func):
        self.root = root
        self.root.title("Poker Game")
        self.switch_game_func = switch_game_func
        self.frame_color = "#cd853f"
        self.board_color = "#008000"
        self.dealer_position = (500, 200)
        self.button_font = ('Arial', 20, 'bold')
        self.mode_describe_font = ('Arial', 20, 'normal')
        self.deck_card_size = (34, 54)
        self.deck_positions = [(554, 234),(555, 235),(556, 236),(557, 237),(558, 238),(559, 239),(560, 240)]
        self.player_card_positions = [(500,100),(855,160),(855,440),(500,500),(145,440),(145,160)]
        self.player_card_size = (51,81)
        self.destroy_flag = False
        self.dark_flag = False
        self.deck_image = load_image("gui/images/cards/bright/back.png", self.deck_card_size)
        self.welcome_screen()
        self.root.after(1000,lambda:self.setup_ui())
        self.root.after(1000,lambda:self.mode_button())

    def welcome_screen(self):
        self.canvas = tk.Canvas(self.root, width=1000, height=700, bg="black", highlightthickness=0)
        popup_font = ('Arial', 60, 'bold')
        self.canvas.create_text(500, 350,text="Poker AI",font= popup_font,fill="white",tags = "welcome_screen")
        self.canvas.pack(fill="both", expand=True)    

    def setup_ui(self):

        # ボード背景
        self.create_rounded_rectangle(self.canvas, 30, 30, 970, 570, radius=320, fill=self.frame_color)
        self.create_rounded_rectangle(self.canvas, 50, 50, 950, 550, radius=300, fill=self.board_color)

        # ディーラー
        dealer_image = load_image("gui/images/dealer.png", (126, 108))
        self.canvas.create_image(self.dealer_position[0], self.dealer_position[1], image=dealer_image, anchor="center")
        self.tk_dealer_image = dealer_image  # 参照を保持

        self.make_deck()

        # モードディスクリプション
        self.canvas.create_text(500, 620,text="おかえりなさいませ！！",font= self.mode_describe_font,fill="white",tags = "mode_description")
        self.root.after(2000,lambda:self.canvas.delete( "mode_description"))
        self.root.after(2000,lambda:self.canvas.create_text(500, 620,text="バトルスタイルを選択してゲームをはじめよう！！",font= self.mode_describe_font,fill="white",tags = "mode_description"))

        self.account_disp()
        self.setting_disp()
        self.animate()

    def create_rounded_rectangle(self, canvas, x1, y1, x2, y2, radius=25, **kwargs):
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
    
    def field_notice(self, notice=None):
        """フィールドの通知を表示"""
        self.canvas.delete("field_notice")
        
        # Canvas に直接テキストを描画
        self.canvas.create_text(
            500, 600,
            text=notice,
            fill=self.bg_fg,
            font=self.bg_font,
            tags="field_notice"
        )
    
    def mode_button(self):
        self.create_button(300, 400, 150, 60, "loose")
        self.create_button(500, 400, 150, 60, "normal")
        self.create_button(700, 400, 150, 60, "tight")

        self.canvas.create_text(500, 310,text="AI Battle Style",font=('Arial', 60, 'normal'),fill="white")

    def create_button(self, x, y, width, height, mode):
        # ボタンの矩形を作成
        button_rect = self.canvas.create_rectangle(x - 0.5*width, y - 0.5*height, x + 0.5*width, y + 0.5*height, fill="#006400", outline="black")
        # ボタンのテキストを作成
        text = self.canvas.create_text(x, y, text=mode, font=self.button_font,fill="white")

        # イベントのバインド
        self.canvas.tag_bind(button_rect, "<Enter>", lambda event, rect=button_rect: self.on_enter(event, rect, mode))
        self.canvas.tag_bind(button_rect, "<Leave>", lambda event, rect=button_rect: self.on_leave(event, rect))
        self.canvas.tag_bind(button_rect, "<Button-1>", lambda event : self.on_click(event, mode))
        self.canvas.tag_bind(text, "<Enter>", lambda event, rect=button_rect: self.on_enter(event, rect, mode))
        self.canvas.tag_bind(text, "<Leave>", lambda event, rect=button_rect: self.on_leave(event, rect))
        self.canvas.tag_bind(text, "<Button-1>", lambda event : self.on_click(event, mode))

    def on_enter(self,event,rect,mode): 
        self.canvas.delete("mode_description")
        self.canvas.itemconfig(rect, fill="#8fbc8f")

        message1 = "aiの対戦モードが " +mode+ " だよ"
        if mode == "loose":
            message2 = "弱い手でもガンガン攻めてくるので気をつけよう！！"
        if mode == "normal":
            message2 = "オーソドックスな攻め方をしてくるから、初心者におすすめのモードだ！！"
        if mode == "tight":
            message2 = "基本的に強い手でしか勝負に乗らないから、積極的に攻めよう！！"

        self.canvas.create_text(500, 600,text=message1,font= self.mode_describe_font,fill="white",tags = "mode_description")
        self.canvas.create_text(500, 630,text=message2,font=self.mode_describe_font,fill="white",tags = "mode_description")

    def on_leave(self,event,rect):
        self.canvas.delete("mode_description")
        self.canvas.itemconfig(rect, fill="#006400")
        self.canvas.create_text(500, 620,text="バトルスタイルを選択してゲームをはじめよう！！",font= self.mode_describe_font,fill="white",tags = "mode_description")

    def on_click(self, event, mode):
        # ボタンがクリックされた時にアクションを実行
        self.to_dark_screen(mode)
        self.root.after(3000,lambda: self.switch_game_func())
        print(mode)
    
    def account_disp(self):
        account_image_normal = load_image("gui/images/account_white.png", (75, 75))
        account_image_hover = load_image("gui/images/account_white.png", (80, 80))
        self.account_image_id = self.canvas.create_image(40,40, image=account_image_normal, anchor="center")
        self.account_image_normal = account_image_normal
        self.account_image_hover = account_image_hover
    
        # self.canvas.tag_bind(self.account_image_id, "<Button-1>", lambda event: self.exit_button_func())
        self.canvas.tag_bind(self.account_image_id, "<Enter>", lambda event: self.on_account_func())
        self.canvas.tag_bind(self.account_image_id, "<Leave>", lambda event: self.leave_account_func())

    def on_account_func(self):
        self.canvas.itemconfig(self.account_image_id, image=self.account_image_hover)

    def leave_account_func(self):
        self.canvas.itemconfig(self.account_image_id, image=self.account_image_normal)

    def setting_disp(self):
        setting_image_normal = load_image("gui/images/setting_white.png", (50, 50))
        setting_image_hover = load_image("gui/images/setting_white.png", (54, 54))

        self.setting_image_id = self.canvas.create_image(960,40, image=setting_image_normal, anchor="center")
        self.setting_image_normal = setting_image_normal
        self.setting_image_hover = setting_image_hover

        # self.canvas.tag_bind(self.setting_image_id, "<Button-1>", lambda event: self.exit_button_func())
        self.canvas.tag_bind(self.setting_image_id, "<Enter>", lambda event: self.on_setting_func())
        self.canvas.tag_bind(self.setting_image_id, "<Leave>", lambda event: self.leave_setting_func())

    def on_setting_func(self):
        self.canvas.itemconfig(self.setting_image_id, image=self.setting_image_hover)

    def leave_setting_func(self):
        self.canvas.itemconfig(self.setting_image_id, image=self.setting_image_normal)
    
    def to_dark_screen(self,mode=None):
        # フレームレート（何ミリ秒ごとに更新するか）
        self.dark_flag = True
        interval = 2  # 2ms
        trans_rate = 0

        def update():
            nonlocal trans_rate
            if trans_rate >= 256:
                return
            else:
                self.canvas.delete("transparent_black")
                transparent_black_img = create_transparent_black_image(1000, 800,trans_rate)
                self.photo = ImageTk.PhotoImage(transparent_black_img)
                self.transparent_image = self.canvas.create_image(0, 0, image=self.photo, anchor="nw",tag ="transparent_black")
                trans_rate += 8
                if trans_rate >= 200:
                    self.root.after(500,lambda: self.popup_mode(mode))
            
            self.root.after(interval,update)
        update()

    def popup_mode(self,mode):
        popup_font = ('Arial', 60, 'bold')
        self.canvas.create_text(500, 300,text= "VS  " + mode + " AI",font= popup_font,fill="white",tags = "popup_mode")
        self.canvas.create_text(500, 400,text="Game start!!!!!",font= popup_font,fill="white",tags = "popup_mode")

    def destroy(self):
        self.canvas.destroy()
        self.destroy_flag = True

    def animate(self):
        def background():
            if not self.dark_flag:
                for i in range(2):
                    for j in range(6):
                        self.canvas.delete("player_"+str(j)+"_card_"+str(i))

                # デッキ
                self.deck = [
                    "As", "Ad", "Ac", "Ah",
                    "Ks", "Kd", "Kc", "Kh",
                    "Qs", "Qd", "Qc", "Qh",
                    "Js", "Jd", "Jc", "Jh",
                    "Ts", "Td", "Tc", "Th",
                    "9s", "9d", "9c", "9h",
                    "8s", "8d", "8c", "8h",
                    "7s", "7d", "7c", "7h",
                    "6s", "6d", "6c", "6h",
                    "5s", "5d", "5c", "5h",
                    "4s", "4d", "4c", "4h",
                    "3s", "3d", "3c", "3h",
                    "2s", "2d", "2c", "2h"
                ]
                random.shuffle(self.deck)

                # フィールドカード
                self.current_idx = 0
                self.make_dotted_line()
                
                self.distribute_cards()
                if self.destroy_flag:
                    return
                self.root.after(8000,lambda:self.make_dotted_line())
                self.root.after(8000,lambda:self.make_deck())
                self.root.after(9000,lambda:background())
        
        background()

    def make_deck(self):
        if not self.dark_flag:
            for idx, position in enumerate(self.deck_positions):
                self.canvas.delete("deck_"+str(len(self.deck_positions)-idx))
                self.canvas.create_image(position[0], position[1], image=self.deck_image, anchor="center",tags="deck_"+str(len(self.deck_positions)-idx))

    def distribute_cards(self):
        # 0.1秒おきにカードを配布
        def distribute_next_card():
            # 配るカードがあればplayer_card()を呼び出し
            if self.current_idx < 12:
                card = self.deck[self.current_idx]
                i = self.current_idx % 6  # カード
                j = self.current_idx // 6  # プレイヤー
                self.player_card(card, i, j, disp_flag=i==3, from_dealer=True,delete_flag=True)
                if self.current_idx % 4 == 0:
                    idx = self.current_idx // 4 + 1
                    self.canvas.delete("deck_"+str(idx))
                self.current_idx += 1
                # 0.1秒後に次のカードを配布
                
                self.root.after(100, distribute_next_card)
        # 最初のカード配布を開始
        distribute_next_card()

    def player_card(self,card,player_idx,card_idx,disp_flag=False,from_dealer = True,delete_flag = False):
        if not delete_flag:
            self.canvas.delete("player_"+str(player_idx)+"_card_"+str(card_idx))
        target_coords = [self.player_card_positions[player_idx][0] + (card_idx-0.5) * 60,self.player_card_positions[player_idx][1]]

        if disp_flag:
            card_path = card_to_path(card)
            card_image = load_image(card_path, self.player_card_size)
            if from_dealer:
                card = self.canvas.create_image(self.dealer_position[0], self.dealer_position[1], image=card_image, anchor="center",tags="player_"+str(player_idx)+"_card_"+str(card_idx))
                self.move_obj(card, [self.dealer_position[0], self.dealer_position[1]], target_coords, duration=100)
            else:
                card = self.canvas.create_image(target_coords[0], target_coords[1], image=card_image, anchor="center",tags="player_"+str(player_idx)+"_card_"+str(card_idx))

        else:   
            card_path = "gui/images/cards/bright/back.png"
            card_image = load_image(card_path, self.player_card_size)
            if from_dealer:
                card = self.canvas.create_image(self.dealer_position[0], self.dealer_position[1], image=card_image, anchor="center",tags="player_"+str(player_idx)+"_card_"+str(card_idx))
                self.move_obj(card, [self.dealer_position[0], self.dealer_position[1]], target_coords, duration=50)
            else:
                card = self.canvas.create_image(target_coords[0], target_coords[1], image=card_image, anchor="center",tags="player_"+str(player_idx)+"_card_"+str(card_idx))     

        setattr(self, f"tk_player{player_idx}_image{card_idx}", card_image)  # 参照を保持
    
    def make_dotted_line(self):
        if not self.dark_flag:
            for i in range(0,2):
                for j in range(0,6):
                    self.canvas.delete("player_"+str(j)+"_card_"+str(i))
            for i in range(0,6):
                for j in range (0,2):
                    x0 = self.player_card_positions[i][0] - self.player_card_size[0]/2 + (j-0.5) * 60
                    y0 = self.player_card_positions[i][1] - self.player_card_size[1]/2
                    x1 = self.player_card_positions[i][0] + self.player_card_size[0]/2 + (j-0.5) * 60
                    y1 = self.player_card_positions[i][1] + self.player_card_size[1]/2
                    self.canvas.create_rectangle(x0+2, y0+2, x1-2, y1-2, dash=(4, 2), outline="white",tags="player_"+str(i)+"_card_"+str(j))

    def move_obj(self, obj, current_coords, target_coords, duration):
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
                self.canvas.move(obj, remaining_dx, remaining_dy)
                return
            if self.destroy_flag:
                return

            # オブジェクトを移動
            self.canvas.move(obj, step_x, step_y)
            current_coords[0] += step_x
            current_coords[1] += step_y
            steps -= 1

            # 次のフレームで再び呼び出し
            self.root.after(interval, update)

        # 初回の呼び出し
        update()


if __name__ == "__main__":
    root = tk.Tk()
    app = Home(root,None)
    root.mainloop()