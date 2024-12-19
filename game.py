from player import Player
from one_round import OneRound

class Game:
    def __init__(self,player_num,stack,sb_amount,game_num):
        self.player_num = player_num
        self.players = []
        for i in range(player_num):
            self.players.append(Player(stack,"player" + str(i),i))
        self.btn_player = 0
        self.sb_amount = sb_amount
        self.game_num = game_num
        self.game_count = 1
        self.one_round = OneRound(self.players,self.btn_player,self.sb_amount)
        self.one_round.set()
        self.game_flag = False

    def _choose_next_btn(self):
        for i in range(1, self.player_num):
            potential_btn_player = (self.btn_player + i) % self.player_num
            if self.players[potential_btn_player].stack >= 0:
                self.btn_player = potential_btn_player
                return

    def step(self,action):
        reward, next_state = self.one_round.step(action)

        # ゲーム終了時に、次のゲームをセットする
        if next_state is None or self.one_round.current_phase == 4:
            self.declare_game_end()
            player_stack = [player.stack for player in self.players]
            if any(x <= 0 for x in player_stack):
                self.game_flag = True
            elif self.game_count == self.game_num:
                self.game_flag = True
            else:
                self.next_game()

        return reward,next_state
    
    def declare_game_end(self):
        self.result = [player.stack for player in self.players]
        self.rank_list = sorted(range(len(self.result)), key=lambda i: self.result[i], reverse=True)
        print("Game count",self.game_count,"が終了しました💔。")

    def next_game(self):
        self._choose_next_btn()
        self.game_count += 1
        # print(self.rank_list)
        self.one_round = OneRound(self.players,self.btn_player,self.sb_amount)
        for player in self.one_round.players:
            player.card = []
            player.bet_amount = 0
        self.one_round.set()
        return