class Player:
    def __init__(self,stack,name,num):
        self.stack = stack
        self.name = name
        self.card = []
        self.num = num
        self.bet_amount = 0
        self.last_player_act = None
    
    def get(self,get_amount):
        self.stack += get_amount
    
    def recieve_card(self, card):
        self.card.append(card)
    
    def reset(self):
        self.bet_amount = 0
        self.card = []
        self.last_player_act = None
    
    def bet(self,bet_amount):
        self.bet_amount += bet_amount
        self.stack -= bet_amount

    def take_action(self,field_max_bet,action):
        if action == "f":
            self.last_player_act = "f"
            return "f"
        elif action == "c":
            call_amount = field_max_bet - self.bet_amount
            self.stack -= call_amount
            self.bet_amount += call_amount
            self.last_player_act = "c"
            return "c"
        elif action == "r":
            total_bet_amount = 2 * field_max_bet
            raise_amount = total_bet_amount - self.bet_amount

            self.stack -= (raise_amount)
            self.bet_amount  = total_bet_amount
            self.last_player_act = "r"
            return "r"

        # elif action== "a":
        #     self.bet_amount += self.stack
        #     self.stack = 0
        #     return "a"