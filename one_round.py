import random
from ranking import rank_of_multi_card
from state_encode import encode_state
from reward import decide_reward
from player import Player

class OneRound:
    def __init__(self,players,btn_player,sb_amount):
        self.players = players
        self.btn_player = btn_player
        self.sb_amount = sb_amount
        self.battle_user_list = [player.stack >= 0 for player in  players]
        self.players_length = len (players)
        self.field_card = []
        self.winner_index= None
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
        self.act_done_list = [False] * self.players_length
        self.round_end_flag = False
        self.current_phase= 0
        self.action_count_phase = 0
        self.last_field_act = None
    
    def _current_phase(self):
        if self.current_phase == 1:
            # フィールドに3枚のカードが配られた状況
            ### フィールドに三枚表示する
            self.field_card.append(self.deck.pop(0))
            self.field_card.append(self.deck.pop(0))
            self.field_card.append(self.deck.pop(0))
            self.action_count_phase = 0
            print("Flop start!!(3cards in field)")
            print("field card :" ,{self.field_card[0]},{self.field_card[1]},{self.field_card[2]})
            return
        if self.current_phase == 2:
            # フィールドに4枚のカードが配られた状況
            self.field_card.append(self.deck.pop(0))
            self.action_count_phase = 0
            print("Turn start!!(4cards in field)")
            print("field card :" ,{self.field_card[0]},{self.field_card[1]},{self.field_card[2]},{self.field_card[3]})
            return
        if self.current_phase == 3:
            # フィールドに5枚のカードが配られた状況
            self.field_card.append(self.deck.pop(0))
            self.action_count_phase = 0
            print("River start!!(5cards,final betting time)")
            print("field card :" ,{self.field_card[0]},{self.field_card[1]},{self.field_card[2]},{self.field_card[3]},{self.field_card[4]})
            return
        if self.current_phase == 4:
            self.action_count_phase = 0
            # 最後の判別のタイミング
            best_player_score = 0
            for player in self.players:
                if self.battle_user_list[player.num]:
                    card = player.card + self.field_card
                    player_five_card, player_rank_text, player_hand_score,rank = rank_of_multi_card(card)
                    print(player.name,player_five_card[0],player_five_card[1],player_five_card[2],player_five_card[3],player_five_card[4])
                    if best_player_score < player_hand_score:
                        best_player_score = player_hand_score
                        best_player_num = player.num
                else:
                    print(player.name,"fold")
            self._get_field_money(best_player_num)
            self.round_end_flag = True
            print("winner:",{self.players[best_player_num].name})
            print([player.stack for player in self.players])
    
    def _init_bet_round(self):
        self.act_done_list = [False] * self.players_length
        return

    def _get_next_player_index(self,current_index):
        ### 現在のindexから次のactiveプレイヤーのインデックスを把握する関数
        for i in range(1,self.players_length):
            next_index = (current_index + i) % self.players_length
            if self.battle_user_list[next_index]:
                return next_index
        return None

    def _get_field_money(self,winner_index):
        self.field_money = sum(player.bet_amount for player in self.players)
        self.players[winner_index].get(self.field_money)
    
    def _init_players(self):
        for player in self.players:
            player.reset()
    
    def set(self):
        ###デッキのシャッフル
        random.shuffle(self.deck)
        self.sb_player = self._get_next_player_index(self.btn_player)
        bb_player = self._get_next_player_index(self.sb_player)

        ### sbプレイヤー、bbプレイヤーからmoneyを徴収する
        self.players[self.sb_player].bet(self.sb_amount)
        self.field_max_bet_amount = self.sb_amount * 2
        self.players[bb_player].bet(self.sb_amount * 2)
        ### 各プレイヤーに二枚ずつデッキからカードを配る
        print("preflop start!!!(each player have 2cards)")
        for player in self.players:
            player.recieve_card(self.deck.pop(0))
            player.recieve_card(self.deck.pop(0))
        self.current_index = self._get_next_player_index(bb_player)
        self.first_index = self.current_index
    
    def player_state(self,index):
        state = encode_state(self.players[index].bet_amount,self.field_max_bet_amount,self.players[index].card,self.field_card,self.current_phase,self.last_field_act,self.players[index].last_player_act,self.action_count_phase)
        return state
    
    def mask(self,player_index):
        player = self.players[player_index]
        ### フィールドの掛け金が、自分のベットサイズと同じ時（chekとraiseのみ）
        if self.field_max_bet_amount == player.bet_amount:
            if self.field_max_bet_amount * 2 > (player.bet_amount + player.stack) :
                mask = [0,1,0]
            else:
                mask = [0,1,1]
        ### フィールドの掛け金が、自分のベットサイズより小さい時
        else:
            if (player.stack + player.bet_amount) > self.field_max_bet_amount * 2:
                mask = [1,1,1]
            elif (player.stack + player.bet_amount) > self.field_max_bet_amount:
                mask = [1,1,0]
            else:
                mask = [1,0,0]
        return mask
    
    def step(self,action):
        player = self.players[self.current_index]
        action = player.take_action(self.field_max_bet_amount,action)

        if action == "f":
            self.battle_user_list[self.current_index] = False
            self.last_field_act = "f"
        if action == "c":
            self.last_field_act = "c"
            self.action_count_phase += 1
        if action == "r":
            self.field_max_bet_amount = player.bet_amount
            self.act_done_list = [False] * self.players_length
            self.last_field_act = "r"
            self.action_count_phase += 2
        # if action =="a":
        #     self.act_done_list = [False] * self.splayers_length
        #     self.field_max_bet_amount = player.bet_amount

        reward = decide_reward(self.field_max_bet_amount,player.bet_amount,self.current_phase,player.card,self.field_card,action,player.last_player_act,self.last_field_act,self.action_count_phase)
        print({player.name}," card",{player.card[0]},{player.card[1]}," action:",{action},"reward",{reward}, " bet_amount:",{player.bet_amount})
        self.act_done_list[self.current_index] = True

        # バトルユーザーが一人になった時の挙動
        if sum(self.battle_user_list) == 1:
            self._get_field_money(self.battle_user_list.index(True))
            self.round_end_flag= True
            print("このラウンドは終了しました🥺")
            print("勝者は",{self.players[self.battle_user_list.index(True)].name},"です💪")
            print("獲得賞金は",{(self.field_money - self.players[self.battle_user_list.index(True)].bet_amount)},"です")
            print([player.stack for player in self.players])
            self._init_players()
            reward = 0
            next_state = None
            
            return reward ,next_state

        else:
            #current_indexを次の人に渡して、その人が実行済みかどうかを判断する
            self.current_index = self._get_next_player_index(self.current_index)
            if self.act_done_list[self.current_index] == True:
                if  self.round_end_flag == False:
                    self._init_bet_round()
                    self.current_phase += 1
                    self._current_phase()
            
            next_state = self.player_state(self.current_index)
            return reward, next_state

# players = []
# for i in range(2):
#     players.append(Player(500,"player" + str(i),i))

# one_round = OneRound(players,0,100)
# one_round.set()
# one_round.step("r")
# one_round.step("c")
# one_round.step("r")
# one_round.step("f")