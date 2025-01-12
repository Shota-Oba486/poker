from env.player import Player
from env.one_round import OneRound

class Game:
    def __init__(self,player_num,stack,sb_amount,game_num,print_flag =False,train_flag = True):
        self.player_num = player_num
        self.players = []
        for i in range(player_num):
            self.players.append(Player(stack,"player" + str(i),i))
        self.btn_player = 0
        self.sb_amount = sb_amount
        self.game_num = game_num
        self.game_count = 1
        self.one_round = OneRound(self.players,self.btn_player,self.sb_amount,print_flag)
        self.one_round.set()
        self.game_flag = False
        self.print_flag = print_flag
        self.train_flag = train_flag

    def _choose_next_btn(self):
        for i in range(1, self.player_num):
            potential_btn_player = (self.btn_player + i) % self.player_num
            if self.players[potential_btn_player].stack >= 0:
                self.btn_player = potential_btn_player
                return

    def step(self,action):
        reward, next_state,current_phase,next_phase = self.one_round.step(action)

        if self.train_flag:
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
            return reward,next_state,current_phase,next_phase
        
        else:
            if next_state is None or self.one_round.current_phase == 4:
                player_stack = [player.stack for player in self.players]
                if any(x <= 0 for x in player_stack):
                    self.game_flag = True
                elif self.game_count == self.game_num:
                    self.game_flag = True
                
                if self.game_flag:
                    stack_list = [player.stack for player in self.players]
                    self.winner_index = stack_list.index(max(stack_list))

    def declare_game_end(self):
        self.result = [player.stack for player in self.players]
        self.rank_list = sorted(range(len(self.result)), key=lambda i: self.result[i], reverse=True)
        if self.print_flag:
            print("Game count",self.game_count,"が終了しました💔。")

    def next_game(self):
        self._choose_next_btn()
        self.game_count += 1
        self.one_round = OneRound(self.players,self.btn_player,self.sb_amount,self.print_flag)
        for player in self.one_round.players:
            player.reset()
        self.one_round.set()
        return

if __name__ == "__main__":
    game = Game(2,10000,100,3,True)
    game.step("f")
    game.step("f")
    game.step("f")
    # game.step("f")