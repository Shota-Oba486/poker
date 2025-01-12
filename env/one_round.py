import random
from env.player import Player
from env.ranking import rank_of_multi_card
from train.state_encode import encode_state
from train.reward import decide_reward

class OneRound:
    def __init__(self,players,btn_player,sb_amount,print_flag = False):
        self.players = players
        self.btn_player = btn_player
        self.sb_amount = sb_amount
        self.battle_user_list = [player.stack >= 0 for player in  players]
        self.players_length = len (players)
        self.field_card = []
        self.field_card_truth = []
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
        self.r_count = 0
        self.pod = 0
        self.print_flag = print_flag
    
    def _current_phase(self):
        if self.current_phase == 1:
            # フィールドに3枚のカードが配られた状況
            ### フィールドに三枚表示する
            self.field_card.append(self.deck[0])
            self.field_card.append(self.deck[1])
            self.field_card.append(self.deck[2])
            self.action_count_phase = 0
            self.first_index = self.current_index
            if self.print_flag:
                print("Flop start!!(3cards in field)")
                print("field card :" ,{self.field_card[0]},{self.field_card[1]},{self.field_card[2]})
            return
        if self.current_phase == 2:
            # フィールドに4枚のカードが配られた状況
            self.field_card.append(self.deck[3])
            self.action_count_phase = 0
            self.first_index = self.current_index
            if self.print_flag:
                print("Turn start!!(4cards in field)")
                print("field card :" ,{self.field_card[0]},{self.field_card[1]},{self.field_card[2]},{self.field_card[3]})
            return
        if self.current_phase == 3:
            # フィールドに5枚のカードが配られた状況
            self.field_card.append(self.deck[4])
            self.action_count_phase = 0
            self.first_index = self.current_index
            if self.print_flag:
                print("River start!!(5cards,final betting time)")
                print("field card :" ,{self.field_card[0]},{self.field_card[1]},{self.field_card[2]},{self.field_card[3]},{self.field_card[4]})
            return
        if self.current_phase == 4:
            self.action_count_phase = 0
            # 最後の判別のタイミング
            best_player_score = 0
            self.first_index = self.current_index
            for player in self.players:
                if self.battle_user_list[player.num]:
                    card = player.card + self.field_card
                    player_five_card, player_rank_text, player_hand_score,rank = rank_of_multi_card(card)
                    player.card_rank = rank
                    player.card_rank_text = player_rank_text
                    if self.print_flag:
                        print(player.name,player_five_card[0],player_five_card[1],player_five_card[2],player_five_card[3],player_five_card[4])
                    if best_player_score < player_hand_score:
                        best_player_score = player_hand_score
                        best_player_num = player.num
                else:
                    if self.print_flag:
                        print(player.name,"fold")
            self.winner_index = best_player_num
            self.win_five_hand = rank_of_multi_card(self.players[self.winner_index].card + self.field_card)[0]
            self._get_field_money(self.winner_index)
            self.round_end_flag = True
            if self.print_flag:
                print("winner:",self.players[self.winner_index].name)
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
        self.players[winner_index].get(self.pod)
        for player in self.players:
            player.bet_amount = 0
        self.pod = 0

    def set(self):
        ###デッキのシャッフル
        random.shuffle(self.deck)
        self.sb_player = self._get_next_player_index(self.btn_player)
        bb_player = self._get_next_player_index(self.sb_player)

        ### sbプレイヤー、bbプレイヤーからmoneyを徴収する
        self.players[self.sb_player].bet(self.sb_amount)
        self.players[self.sb_player].first_bet_amount = self.sb_amount
        self.field_max_bet_amount = self.sb_amount * 2
        self.players[bb_player].bet(self.sb_amount * 2)
        self.players[bb_player].first_bet_amount = (self.sb_amount * 2)
        self.pod += self.sb_amount * 3
        ### 各プレイヤーに二枚ずつデッキからカードを配る
        if self.print_flag:
            print("preflop start!!!(each player have 2cards)")
        for player in self.players:
            player.recieve_card(self.deck.pop(0))
            player.recieve_card(self.deck.pop(0))
        self.current_index = self._get_next_player_index(bb_player)
        self.first_index = self.current_index

        self.field_card_truth = [d for d  in self.deck[:5]]
        best_player_score = 0
        for player in self.players:
            card = player.card + self.field_card_truth
            player_five_card, player_rank_text, player_hand_score,rank = rank_of_multi_card(card)

            if best_player_score < player_hand_score:
                best_player_score = player_hand_score
                best_player_num = player.num
        self.winner_index_truth = best_player_num

    def player_state(self,index):
        player = self.players[index]
        if index == 0:
            opponent_player = self.players[1]
        else:
            opponent_player = self.players[0]
        state = encode_state(player.start_stack,player.stack,opponent_player.stack,player.bet_amount,self.field_max_bet_amount,player.card,self.field_card,self.current_phase,self.last_field_act,player.last_player_act,self.r_count,self.first_index,self.current_index)
        return state
    
    def mask(self,player_index):
        player = self.players[player_index]
        ### フォールドできない時
        ### フィールドの掛け金が、自分のベットサイズと同じ時（chekとraiseのみ）
        if self.field_max_bet_amount == player.bet_amount:
            if self.field_max_bet_amount * 2 > (player.bet_amount + player.stack) :
                mask = [0,1,0,0,0,0]
            elif self.field_max_bet_amount * 3 > (player.bet_amount + player.stack) :
                mask = [0,1,0,1,0,0]
            elif self.field_max_bet_amount * 5 > (player.bet_amount + player.stack) :
                mask = [0,1,0,1,1,0]
            else:
                mask = [0,1,0,1,1,1]
        ### フィールドの掛け金が、自分のベットサイズより小さい時(fold,call,raise)
        else:
            if (player.stack + player.bet_amount) >= self.field_max_bet_amount * 5:
                mask = [1,0,1,1,1,1]
            elif (player.stack + player.bet_amount) >= self.field_max_bet_amount * 3:
                mask = [1,0,1,1,1,0]
            elif (player.stack + player.bet_amount) >= self.field_max_bet_amount * 2:
                mask = [1,0,1,1,0,0]
            elif (player.stack + player.bet_amount) >= self.field_max_bet_amount:
                mask = [1,0,1,0,0,0]
            else:
                mask = [1,0,0,0,0,0]
        return mask
    
    def step(self,action):
        current_phase = self.current_phase
        player = self.players[self.current_index]
        reward = decide_reward(self.pod,self.field_max_bet_amount,player.bet_amount,action,self.winner_index_truth == self.current_index,self.mask(self.current_index),self.current_phase,player.first_bet_amount)

        self.pod -= player.bet_amount
        action = player.take_action(self.field_max_bet_amount,action)
        self.pod += player.bet_amount
        self.first_index = None

        if action == "f":
            self.battle_user_list[self.current_index] = False
            self.last_field_act = "f"
        if action == "check":
            self.last_field_act = "check"
            self.action_count_phase += 1
        if action == "call":
            self.last_field_act = "call"
            self.action_count_phase += 1
        if action == "r_2":
            self.field_max_bet_amount = player.bet_amount
            self.act_done_list = [False] * self.players_length
            self.last_field_act = "r_2"
            self.action_count_phase += 2
            self.r_count += 1
        if action == "r_3":
            self.field_max_bet_amount = player.bet_amount
            self.act_done_list = [False] * self.players_length
            self.last_field_act = "r_3"
            self.action_count_phase += 2
            self.r_count += 1
        if action == "r_5":
            self.field_max_bet_amount = player.bet_amount
            self.act_done_list = [False] * self.players_length
            self.last_field_act = "r_5"
            self.action_count_phase += 2
            self.r_count += 1
        # if action == "a":
        #     self.act_done_list = [False] * self.players_length
        #     self.field_max_bet_amount = player.bet_amount

        # reward = decide_reward(self.field_max_bet_amount,player.bet_amount,self.current_phase,player.card,self.field_card,action,player.last_player_act,self.last_field_act,self.action_count_phase)
        if self.print_flag:
            print({player.name}," card",{player.card[0]},{player.card[1]}," action:",{action},"reward",{reward}, " bet_amount:",{player.bet_amount})
        self.act_done_list[self.current_index] = True

        # バトルユーザーが一人になった時の挙動
        if sum(self.battle_user_list) == 1:
            self._get_field_money(self.battle_user_list.index(True))
            self.winner_index = self.battle_user_list.index(True)
            self.round_end_flag= True
            if self.current_phase != 0:
                if self.print_flag:
                    print("このラウンドは終了しました🥺")
                    print("勝者は",{self.players[self.battle_user_list.index(True)].name},"です💪")
                    print("獲得賞金は",{(self.pod - self.players[self.battle_user_list.index(True)].bet_amount)},"です")
                    print([player.stack for player in self.players])
            next_state = None
            next_phase = self.current_phase
            return reward ,next_state, current_phase,next_phase

        else:
            #current_indexを次の人に渡して、その人が実行済みかどうかを判断する
            self.current_index = self._get_next_player_index(self.current_index)
            if self.act_done_list[self.current_index] == True:
                if  self.round_end_flag == False:
                    self._init_bet_round()
                    self.current_phase += 1
                    self._current_phase()
            
            next_state = self.player_state(self.current_index)
            next_phase = self.current_phase
            return reward, next_state, current_phase, next_phase

if __name__ == "__main__":
    players = []
    for i in range(2):
        players.append(Player(500,"player" + str(i),i))

    one_round = OneRound(players,0,100,True)
    one_round.set()
    one_round.step("call")
    one_round.step("check")
    one_round.step("check")
    one_round.step("check")
    one_round.step("check")
    one_round.step("check")
    one_round.step("check")
    one_round.step("check")