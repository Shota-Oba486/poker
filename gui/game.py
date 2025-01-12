import tkinter as tk
from PIL import Image, ImageTk
from gui.agent import AI
from env.game import Game
from env.ranking import sort_5card
from gui.function import load_image
from gui.function import create_transparent_black_image
from gui.function import create_rounded_rectangle
from gui.function import load_image
from gui.function import card_to_path

class PokerGameUI:
    def __init__(self, root,switch_home_func,switch_game_func,ai_mode=True):
        self.destory_flag = False
        self.ai_mode = ai_mode
        self.root = root
        self.root.title("Poker Game")
        self.root.geometry("1000x700")
        self.switch_home_func = switch_home_func
        self.switch_game_func = switch_game_func
        self.phase_names = ["Preflop", "Flop", "Turn", "River", "Show Down"]
        self.action_to_notice = {"f":"fold","check":"check","call":"call","r_2":"2_raise","r_3":"3_raise","r_5":"5_raise"}
        self.bg_color = "black"
        self.bg_fg = "white"
        self.board_color = "#008000"
        self.frame_color = "#cd853f"
        self.player_fg = "white"
        self.celebrate_win_player_fg = "red"
        self.celebrate_lose_player_fg = "blue"
        self.player_font = ('Arial', 20, 'normal')
        self.bg_font = ('Arial', 20, 'normal')
        self.board_font = ('Arial', 40, 'bold')
        self.rank_font = ('Arial', 60, 'bold')
        self.pod_font = ('Arial', 40, 'bold')
        self.pod_amount_font = ('Arial', 60, 'bold')
        self.button_font = ('Arial', 20, 'bold')
        self.field_card_size = (85, 135)
        self.player_card_size = (68, 108)
        self.deck_card_size = (34, 54)
        self.last_card_size = (102, 162)
        self.field_card_x_positions = [300, 400, 500, 600, 700]
        self.field_card_y_position =250
        self.last_field_card_x_positions = [260, 380, 500, 620, 740]
        self.last_field_card_y_position =250
        self.player0_positions = [220, 300]
        self.player1_positions = [700, 780]
        self.pod_text_position = (500, 430)
        self.pod_amount_position = (500, 490)
        self.dealer_position = (500, 100)
        self.deck_positions = [(554, 134),(555, 135),(556, 136),(557, 137),(558, 138),(559, 139),(560, 140)]
        self.notice_act_positions = [[300, 420],(700,420)]
        self.player_money_positions = [[[200, 500], [200, 530]], [[700, 500], [700, 530]]]
        self.player_bet_positions = [[200, 500], [720, 500]]
        self.player_stack_positions = [[200, 530], [720, 530]]
        self.players_pos_y = 400
        self.act_list = ["f","check","call","r_2","r_3","r_5"]

        """リセットするーず"""
        self.ai_last_act = None
        self.phase_last_act = None
        self.last_act_player_idx = None
        self.gui_phase = 0
        self.recurrent_field_card_length = 0
        self.player_current_bet_dict = {"player0":0,"player1":0}

        self.game = Game(2,10000,100,10,train_flag=False)
        self.game.players[0].name = "AI😤"
        self.game.players[1].name = "Youuuuuu!!!"
        self.ai = AI()
        self.setup_ui()
        if self.ai_mode:
            if self.game.one_round.current_index == 0:
                self.root.after(300, lambda: self.act_ai())
    
    def reset(self):
        self.ai_last_act = None
        self.phase_last_act = None
        self.last_act_player_idx = None
        self.gui_phase = 0
        self.recurrent_field_card_length = 0
        self.player_bet = {}
        self.player_current_bet_dict = {"player0":0,"player1":0}
        self.canvas.destroy()
        self.setup_ui()
        if self.ai_mode:
            if self.game.one_round.current_index == 0:
                self.root.after(300, lambda: self.act_ai())
    
    def step(self,action):
        self.phase_last_act = action
        self.last_act_player_idx = self.game.one_round.current_index
        player_index = self.game.one_round.current_index
        self.game.step(action)
        if self.gui_phase != self.game.one_round.current_phase:
            self.gui_phase = self.game.one_round.current_phase
            if self.last_act_player_idx == 0:
                self.root.after(300,lambda:self.notice_change_phase())
            elif self.last_act_player_idx == 1:
                self.root.after(500,lambda:self.notice_change_phase())
            if self.game.one_round.current_phase == 4:
                self.player_card(0,disp_flag=True,from_dealer=False)
                self.root.after(1800,lambda:self.showdown_end())

        if not self.game.one_round.round_end_flag:
            self.update_ui()
        else:
            self.round_end()
        self.notice_action(action,player_index)
        if self.ai_mode:
            if self.game.one_round.current_index == 0 and self.phase_last_act == None and self.game.one_round.round_end_flag != True:
                self.root.after(1800, lambda: self.act_ai())
            elif self.game.one_round.current_index == 0 and self.game.one_round.round_end_flag != True:
                self.root.after(400, lambda: self.act_ai())

    def notice_action(self, action,player_index):
        notice_action = self.action_to_notice[action]
        if action != "f":
            notice_action = self.canvas.create_text(self.notice_act_positions[player_index][0], self.notice_act_positions[player_index][1], text=notice_action + "!!!!!!", font=("Helvetica", 80), fill="red", angle= 60 * (player_index-0.5))
            self.root.after(100, lambda: self.move_obj(notice_action,list(self.notice_act_positions[player_index]),[500,280],150))
            self.root.after(300, lambda: self.canvas.delete(notice_action))
        else:
            transparent_black_img = create_transparent_black_image(1000, 800)
            self.photo = ImageTk.PhotoImage(transparent_black_img)
            self.transparent_image = self.canvas.create_image(0, 0, image=self.photo, anchor="nw",tag ="transparent_black")
            notice_action = self.canvas.create_text(self.notice_act_positions[player_index][0], self.notice_act_positions[player_index][1], text=notice_action + "!!!!!!", font=("Helvetica", 80), fill="red", angle= 60 * (player_index-0.5))
            self.root.after(100, lambda: self.move_obj(notice_action,list(self.notice_act_positions[player_index]),[500,280],60))
            self.canvas.tag_raise("Pod")
            self.canvas.tag_raise("pod_amount_notice")

    def notice_change_phase(self):
        # 背景を黒くする
        transparent_black_img = create_transparent_black_image(1000, 800)
        self.photo = ImageTk.PhotoImage(transparent_black_img)
        self.transparent_image = self.canvas.create_image(0, 0, image=self.photo, anchor="nw",tag ="transparent_black")
        notice = self.phase_names[int(self.game.one_round.current_phase)]
        self.root.after(100, lambda: self.canvas.create_text(500, 270, text=notice +"!!!!!!", font=("Helvetica", 80), fill="red", angle=15,tags = "notice_change_phase"))
        
        if self.game.one_round.current_phase != 4:
            self.root.after(1100, lambda: self.canvas.delete("notice_change_phase"))
            self.root.after(1100, lambda: self.canvas.delete("transparent_black"))
        else:
            self.root.after(2100, lambda: self.canvas.delete("notice_change_phase"))

    def setup_ui(self):
        """UIを構築"""
        # Canvasを作成
        self.canvas = tk.Canvas(self.root, width=1000, height=700, bg=self.bg_color, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        # ボード背景
        create_rounded_rectangle(self.canvas, 30, 30, 970, 570, radius=320, fill=self.frame_color)
        create_rounded_rectangle(self.canvas, 50, 50, 950, 550, radius=300, fill=self.board_color)

        # ディーラー
        dealer_image = load_image("gui/images/dealer.png", (126, 108))
        self.canvas.create_image(self.dealer_position[0], self.dealer_position[1], image=dealer_image, anchor="center")
        self.tk_dealer_image = dealer_image  # 参照を保持

        self.notice_round_num()

        # ゲーム終了ボタン
        exit_button_normal = load_image("gui/images/exit_gray.png", (80, 80))  # 通常状態の画像
        exit_button_hover = load_image("gui/images/exit_white.png", (80, 80))  # ホバー時の画像

        self.exit_button_id = self.canvas.create_image(960, 40, image=exit_button_normal, anchor="center")
        self.exit_button_normal = exit_button_normal  # 通常状態の参照を保持
        self.exit_button_hover = exit_button_hover 

        self.canvas.tag_bind(self.exit_button_id, "<Button-1>", lambda event: self.exit_button_func())
        self.canvas.tag_bind(self.exit_button_id, "<Enter>", lambda event: self.on_exit_button_func())
        self.canvas.tag_bind(self.exit_button_id, "<Leave>", lambda event: self.leave_exit_button_func())

        # デッキ
        deck_image = load_image("gui/images/cards/bright/back.png", self.deck_card_size)
        for idx, position in enumerate(self.deck_positions):
            self.canvas.create_image(position[0], position[1], image=deck_image, anchor="center",tags="deck_"+str(len(self.deck_positions)-idx))
        self.deck_image = deck_image  # 参照を保持

        # ポッドとボタン
        self.set_pod()
        self.setup_buttons()

        # フィールドカード
        for i in range(0,5):
            x0 = self.field_card_x_positions[0] - self.field_card_size[0]/2 + i*100
            y0 = self.field_card_y_position - self.field_card_size[1]/2
            x1 = self.field_card_x_positions[0] + self.field_card_size[0]/2 + i*100
            y1 = self.field_card_y_position + self.field_card_size[1]/2
            self.canvas.create_rectangle(x0, y0, x1, y1, dash=(4, 2), outline="white",tags="field_card_"+str(i))

        #プレイヤーカード
        self.player_card(0,disp_flag=False,from_dealer=True)
        self.player_card(1,disp_flag=True,from_dealer=True)

        #stackとbet_amountを表示
        self.player_money(0,self.game.one_round.players[0].bet_amount,self.game.one_round.players[0].stack)
        self.player_money(1,self.game.one_round.players[1].bet_amount,self.game.one_round.players[1].stack)

        # podを表示
        self.pod_amount_notice()

        #フィールドnoticeを表示
        self.field_notice()
        self.notice_phase(0)

    def set_pod(self):
        self.pod_text = self.canvas.create_text(self.pod_text_position[0],self.pod_text_position[1], text="Pod", fill=self.player_fg, font=self.pod_font,tags = "Pod")

    def setup_buttons(self):
        self.canvas.delete("button")
        c_amount = self.game.one_round.field_max_bet_amount - self.game.one_round.players[self.game.one_round.current_index].bet_amount
        r_2_amount = self.game.one_round.field_max_bet_amount * 2- self.game.one_round.players[self.game.one_round.current_index].bet_amount
        r_3_amount = self.game.one_round.field_max_bet_amount * 3- self.game.one_round.players[self.game.one_round.current_index].bet_amount
        r_5_amount = self.game.one_round.field_max_bet_amount * 5- self.game.one_round.players[self.game.one_round.current_index].bet_amount

        f_button = tk.Button(self.root, text="Fold", width=10, height=2, relief="flat", bd=0, font=self.button_font, bg="white", activebackground="lightgray",command=lambda: self.step("f"))
        check_button = tk.Button(self.root, text="Check" + "($"+str(c_amount)+")", width=10, height=2, relief="flat", bd=0, font=self.button_font, command=lambda: self.step("check"))
        call_button = tk.Button(self.root, text="Call" + "($"+str(c_amount)+")", width=10, height=2, relief="flat", bd=0, font=self.button_font, command=lambda: self.step("call"))
        r_2_button = tk.Button(self.root, text="Raise($"+str(r_2_amount)+")", width=10, height=2, relief="flat", bd=0, font=self.button_font, command=lambda: self.step("r_2"))
        r_3_button = tk.Button(self.root, text="Raise($"+str(r_3_amount)+")", width=10, height=2, relief="flat", bd=0, font=self.button_font, command=lambda: self.step("r_3"))
        r_5_button = tk.Button(self.root, text="Raise($"+str(r_5_amount)+")", width=10, height=2, relief="flat", bd=0, font=self.button_font, command=lambda: self.step("r_5"))

        """ボタンの有効/無効を更新"""
        self.buttons = [f_button,check_button,call_button,r_2_button,r_3_button,r_5_button]    
        mask = self.game.one_round.mask(self.game.one_round.current_index)
        for button, state in zip(self.buttons, mask):
            if state == 1:
                button.config(state="normal")
            else:
                button.config(state="disabled")

        self.canvas.create_window(200, 660, window=f_button,tags="button")
        if c_amount == 0:
            self.canvas.create_window(350, 660, window=check_button,tags="button")
        else:
            self.canvas.create_window(350, 660, window=call_button,tags="button")
        self.canvas.create_window(500, 660, window=r_2_button,tags="button")
        self.canvas.create_window(650, 660, window=r_3_button,tags="button")
        self.canvas.create_window(800, 660, window=r_5_button,tags="button")

    def display_card(self,card_idx):
        """カードを表示"""
        card = self.game.one_round.field_card[card_idx]
        self.canvas.delete("field_card_" + str(card_idx))
        card_path = card_to_path(card)
        card_image = load_image(card_path, self.field_card_size)
        target_coords = [self.field_card_x_positions[card_idx], self.field_card_y_position]

        card_obj = self.canvas.create_image(
            self.dealer_position[0], self.dealer_position[1], image=card_image, anchor="center",tags=f"field_card_{card_idx}"
        )
        self.move_obj(card_obj,list(self.dealer_position), target_coords, duration=100)
        setattr(self, f"tk_card_image{card}", card_image)
        self.canvas.delete("deck_"+str(card_idx))

    def add_field_card(self,field_cards):
        if self.recurrent_field_card_length == 0:
            self.root.after(0, lambda:self.display_card(0))
            self.root.after(100, lambda:self.display_card(1))
            self.root.after(200, lambda:self.display_card(2))
        if self.recurrent_field_card_length == 3:
            self.display_card(3)
        if self.recurrent_field_card_length == 4:
            self.display_card(4)

        self.recurrent_field_card_length = len(field_cards)
    
    def player_card(self,player_idx,disp_flag=True,from_dealer = False):
        self.canvas.delete("player"+str(player_idx)+"_card_0")
        self.canvas.delete("player"+str(player_idx)+"_card_1")
        cards = self.game.one_round.players[player_idx].card
        if player_idx == 0:
            positions_x = self.player0_positions
        else:
            positions_x = self.player1_positions
        
        if disp_flag and len(cards) != 0:
            for i, card in enumerate(cards):
                card_path = card_to_path(card)
                card_image = load_image(card_path, self.player_card_size)
                if from_dealer:
                    card = self.canvas.create_image(self.dealer_position[0], self.dealer_position[1], image=card_image, anchor="center",tags="player"+str(player_idx)+"_card"+str(i))
                    self.move_obj(card, [self.dealer_position[0], self.dealer_position[1]], [positions_x[i], self.players_pos_y], duration=100)
                else:
                    self.canvas.create_image(positions_x[i], self.players_pos_y, image=card_image, anchor="center",tags="player"+str(player_idx)+"_card"+str(i))
                setattr(self, f"tk_player{player_idx}_image{i}", card_image)  # 参照を保持
        else:
            for i in range(len(cards)):
                card_path = "gui/images/cards/bright/back.png"  
                card_image = load_image(card_path, self.player_card_size)
                if from_dealer:
                    card = self.canvas.create_image(self.dealer_position[0], self.dealer_position[1], image=card_image, anchor="center",tags="player"+str(player_idx)+"_card"+str(0))
                    self.move_obj(card, [self.dealer_position[0], self.dealer_position[1]], [positions_x[i], self.players_pos_y], duration=100)
                    setattr(self, "tk_player"+str(player_idx)+"_image"+str(i), card_image)
                else:
                    self.canvas.create_image(positions_x[0], self.players_pos_y, image=card_image, anchor="center",tags="player"+str(player_idx)+"_card"+str(i))
                    setattr(self, "tk_player"+str(player_idx)+"_image"+str(i), card_image)

    def notice_phase(self, phase):
        """フェーズの通知を表示"""
        self.canvas.delete("notice_phase")
        
        # フェーズ名を定義
        phase_names = ["Preflop", "Flop", "Turn", "River", "Show Down"]
        notice = phase_names[int(phase)]
        
        # Canvas に直接テキストを描画
        self.canvas.create_text(
            230, 120, 
            text=notice, 
            fill=self.bg_fg, 
            font=self.board_font, 
            tags="notice_phase"
        )

    def notice_round_num(self):
        """フェーズの通知を表示"""
        self.canvas.delete("notice_round_num")
        notice = self.game.game_count
        
        # Canvas に直接テキストを描画
        self.canvas.create_text(
            800, 120, 
            text="Round: " + str(notice), 
            fill=self.bg_fg, 
            font=self.board_font, 
            tags="notice_round_num"
        )

    def pod_amount_notice(self):
        """ポットの合計金額を通知"""
        self.canvas.delete("pod_amount_notice")
        # Canvas に直接テキストを描画
        pod = 0
        for player in self.game.one_round.players:
            pod += player.bet_amount
        self.pod_amount_not = self.canvas.create_text(
            self.pod_amount_position,
            text='$' + str(pod),
            fill=self.player_fg,
            font=self.pod_amount_font,
            tags="pod_amount_notice"
        )

    def player_money(self, idx, bet, stack):
        """プレイヤーのベット額とスタックを表示"""
        #以前と掛け金が変わっていたら
        if self.player_current_bet_dict["player"+str(idx)] != bet:
            self.player_current_bet_dict["player"+str(idx)] = bet
            bet_positions = self.player_bet_positions
            stack_positions = self.player_stack_positions
            # スタックを表示
            self.canvas.delete(f"player{idx}_stack")
            self.canvas.create_text(
                stack_positions[idx][0], stack_positions[idx][1],
                text=f'stack: ${stack}',
                fill=self.player_fg,
                font=self.player_font,
                tags=f"player{idx}_stack"
            )
            # 掛け金を表示
            self.canvas.delete(f"player{idx}_bet")
            self.canvas.create_text(
                bet_positions[idx][0], bet_positions[idx][1],
                text=f'bet: ${bet}',
                fill=self.player_fg,
                font=self.player_font,
                tags=f"player{idx}_bet"
            )
            bet_amount_text = self.canvas.create_text(
                bet_positions[idx][0], bet_positions[idx][1],
                text=f'bet: ${bet}',
                fill=self.player_fg,
                font=self.player_font,
                tags=f"player{idx}_bet_move"
            )
            self.move_obj(bet_amount_text,list(self.player_bet_positions[idx]),self.pod_amount_position,duration=100)
            self.root.after(100, lambda: self.canvas.delete(f"player{idx}_bet_move"))

    
    def field_notice(self, notice=None):
        """フィールドの通知を表示"""
        self.canvas.delete("field_notice")
        
        if notice is not None:
            text = notice
        else:
            if self.ai_mode:
                if self.ai_last_act == None:
                    text = self.phase_names[self.gui_phase] + "になりました‼️アクションを選定してください❤️"
                else:
                    text = "aiは "+self.action_to_notice[self.ai_last_act]+" をしてきました。次のアクションを選定してください❤️"
            if not self.ai_mode:
                player_name = self.game.one_round.players[self.game.one_round.current_index].name
                text = f"{player_name}の番です。actionを選んでください❤️"
        
        # Canvas に直接テキストを描画
        self.canvas.create_text(
            500, 600,
            text=text,
            fill=self.bg_fg,
            font=self.bg_font,
            tags="field_notice"
        )

    def update_ui(self):
        self.pod_amount_notice()
        for player in self.game.one_round.players:
            self.player_money(player.num,player.bet_amount,player.stack)
        if self.recurrent_field_card_length != len(self.game.one_round.field_card):
            self.add_field_card(self.game.one_round.field_card)
        self.notice_phase(str(self.game.one_round.current_phase))
        self.field_notice()
        self.setup_buttons()
    
    def act_ai(self):
        state = self.game.one_round.player_state(self.game.one_round.current_index)
        mask = self.game.one_round.mask(self.game.one_round.current_index)
        phase_index = self.game.one_round.current_phase
        action_index = self.ai.get_action(state,mask,phase_index)
        action = self.act_list[action_index]
        self.ai_last_act = action
        self.step(action)

    def showdown_end(self):
        player0_rank_text = self.game.one_round.players[0].card_rank_text
        player1_rank_text = self.game.one_round.players[1].card_rank_text

        if self.game.one_round.winner_index == 0:
            player0_fg = self.celebrate_win_player_fg
            player1_fg = self.celebrate_lose_player_fg
        else:
            player0_fg = self.celebrate_lose_player_fg
            player1_fg = self.celebrate_win_player_fg
        # Player 0 のランクを描画
        notice_rank_player0= self.canvas.create_text(
            250, 400,
            text=player0_rank_text,
            fill=player0_fg,
            font=self.rank_font,
            tags="player0_rank"
        )
        
        # Player 1 のランクを描画
        notice_rank_player1 = self.canvas.create_text(
            750, 400,
            text=player1_rank_text,
            fill=player1_fg,
            font=self.rank_font,
            tags="player1_rank"
        )

        if self.game.one_round.winner_index == 0:
            self.root.after(100, lambda: self.move_obj(notice_rank_player1, [750, 400], [750,470], duration=100))
            self.root.after(100, lambda: self.move_obj(notice_rank_player0, [250, 400], [500,370], duration=100))
        else:
            self.root.after(100, lambda: self.move_obj(notice_rank_player0, [250, 400], [250,470], duration=100))
            self.root.after(100, lambda: self.move_obj(notice_rank_player1, [750, 400], [500,370], duration=100))

        # 背景を黒くする
        transparent_black_img = create_transparent_black_image(1000, 800)
        self.photo = ImageTk.PhotoImage(transparent_black_img)
        self.transparent_image = self.canvas.create_image(0, 0, image=self.photo, anchor="nw",tag ="transparent_black")
        
        #カードを移動させる
        win_five_card = self.game.one_round.win_five_hand
        sorted_five_card = sort_5card(win_five_card)

        for idx,card in enumerate(self.game.one_round.field_card):
            self.canvas.delete("field_card_" + str(idx))
            card_path = card_to_path(card,bright=False)
            card_image = load_image(card_path, self.field_card_size)
            self.canvas.create_image(self.field_card_x_positions[idx], self.field_card_y_position, image=card_image, anchor="center")
            setattr(self, f"tk_win_five_card_image{idx}", card_image)
        
        for idx,card in enumerate(self.game.one_round.players[0].card):
            self.canvas.delete("0_card_"+str(idx))
            card_path = card_to_path(card,bright=False)
            card_image = load_image(card_path, self.player_card_size)
            self.canvas.create_image(self.player1_positions[idx], self.players_pos_y, image=card_image, anchor="center",tags="player0_card_"+str(idx))
            setattr(self, f"tk_player0_image{idx}", card_image)

        for idx,card in enumerate(self.game.one_round.players[1].card):
            self.canvas.delete("player1_card_"+str(idx))
            card_path = card_to_path(card,bright=False)
            card_image = load_image(card_path, self.player_card_size)
            self.canvas.create_image(self.player1_positions[idx], self.players_pos_y, image=card_image, anchor="center",tags="player1_card_"+str(idx))
            setattr(self, f"tk_player1_image{idx}", card_image)
        
        for idx,card in enumerate(sorted_five_card):
            card_path = card_to_path(card,bright=True)
            card_image = load_image(card_path, self.last_card_size)

            if card in self.game.one_round.field_card:
                index = self.game.one_round.field_card.index(card)
                self.canvas.delete("field_card_" + str(index))
                card_obj = self.canvas.create_image(self.field_card_x_positions[index], self.field_card_y_position, image=card_image, anchor="center")
                self.move_obj(card_obj,[self.field_card_x_positions[index],self.field_card_y_position], [self.last_field_card_x_positions[idx],self.last_field_card_y_position], duration = 50)
                setattr(self, f"tk_win_five_card_image{idx}", card_image)
            elif card in self.game.one_round.players[0].card:
                index = self.game.one_round.players[0].card.index(card)
                self.canvas.delete("player0_card_" + str(index))
                card_obj = self.canvas.create_image(self.player0_positions[index], self.players_pos_y, image=card_image, anchor="center")
                self.move_obj(card_obj,[self.player0_positions[index],self.players_pos_y], [self.last_field_card_x_positions[idx],self.last_field_card_y_position], duration = 50)
                setattr(self, f"tk_win_five_card_image{idx}", card_image)
            elif card in self.game.one_round.players[1].card:
                index = self.game.one_round.players[1].card.index(card)
                self.canvas.delete("player1_card_" + str(index))
                card_obj = self.canvas.create_image(self.player1_positions[index], self.players_pos_y, image=card_image, anchor="center")
                self.move_obj(card_obj,[self.player1_positions[index],self.players_pos_y], [self.last_field_card_x_positions[idx],self.last_field_card_y_position], duration = 50)
                setattr(self, f"tk_win_five_card_image{idx}", card_image)  

        self.canvas.tag_raise("player0_rank")
        self.canvas.tag_raise("player1_rank")
        self.canvas.tag_raise("Pod")
        self.canvas.tag_raise("pod_amount_notice")

    def round_end(self):
        self.canvas.delete("field_notice")
        self.canvas.delete("button")
        if not self.game.game_flag:
            next_button = tk.Button(self.root, text="次のラウンドへ", width=10, height=2, relief="flat", bd=0, font=self.button_font, command=lambda: self.next_round())
            self.canvas.create_window(500, 630, window=next_button,tags="button")
        else:
            end_button = tk.Button(self.root, text="終了画面へ", width=10, height=2, relief="flat", bd=0, font=self.button_font, command=lambda: self.end_game())
            self.canvas.create_window(500, 630, window=end_button,tags="button")

    def next_round(self):
        if self.game.one_round.winner_index == 0:
            target_coords = [200, 530]
        else:
            target_coords = [700, 530]
        self.move_obj(self.pod_amount_not,list(self.pod_amount_position), target_coords, duration=100)
        self.root.after(100, lambda: self.canvas.delete("pod_amount_notice"))

        self.root.after(100, lambda: self.player_money(0,self.game.one_round.players[0].bet_amount,self.game.one_round.players[0].stack))
        self.root.after(100, lambda: self.player_money(1,self.game.one_round.players[1].bet_amount,self.game.one_round.players[1].stack))

        self.root.after(300, lambda: self.game.next_game())
        self.root.after(300, lambda: self.reset())
    
    def end_game(self):
        if self.game.one_round.winner_index == 0:
            target_coords = [200, 530]
        else:
            target_coords = [700, 530]
        self.move_obj(self.pod_amount_not,list(self.pod_amount_position), target_coords, duration=100)
        self.root.after(100, lambda: self.canvas.delete("pod_amount_notice"))

        self.root.after(100, lambda: self.player_money(0,self.game.one_round.players[0].bet_amount,self.game.one_round.players[0].stack))
        self.root.after(100, lambda: self.player_money(1,self.game.one_round.players[1].bet_amount,self.game.one_round.players[1].stack))
        self.root.after(100, lambda: self.game_end_screen())
    
    def game_end_screen(self):
        self.canvas.delete("button")
        transparent_black_img = create_transparent_black_image(1000, 800,192)
        self.photo = ImageTk.PhotoImage(transparent_black_img)
        self.transparent_image = self.canvas.create_image(0, 0, image=self.photo, anchor="nw",tag ="transparent_black")
        self.root.after(100, lambda: self.canvas.create_text(500, 200, text="Winner is ....", font=("Helvetica", 80), fill="white"))
        winner_name = self.game.players[self.game.winner_index].name
        self.root.after(800, lambda: self.canvas.create_text(500, 320, text=winner_name, font=("Helvetica", 100), fill="white"))
        home_button = tk.Button(self.root, text="Home", width=10, height=2, relief="flat", bd=0, font=self.button_font, command=lambda: self.switch_home_func())
        next_game_button = tk.Button(self.root, text="Next Game..", width=10, height=2, relief="flat", bd=0, font=self.button_font, command=lambda: self.switch_game_func())
        self.root.after(1300, lambda: self.canvas.create_window(425, 630, window=home_button,tags="button"))
        self.root.after(1300, lambda: self.canvas.create_window(575, 630, window=next_game_button,tags="button"))

    def destroy(self):
        self.canvas.destroy()
        self.destory_flag = True

    def exit_button_func(self):
        # 背景を黒くする
        self.canvas.delete("button")
        self.to_dark_screen()
        self.root.after(1000,lambda:self.switch_home_func())

    def on_exit_button_func(self):
        self.canvas.itemconfig(self.exit_button_id, image=self.exit_button_hover)

    def leave_exit_button_func(self):
        self.canvas.itemconfig(self.exit_button_id, image=self.exit_button_normal)

    def to_dark_screen(self):
        # フレームレート（何ミリ秒ごとに更新するか）
        interval = 2  # 3ms
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
                trans_rate += 16
            
            self.root.after(interval,update)
        update()

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
            if self.destory_flag:
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
    app = PokerGameUI(root,None,None)
    root.mainloop()