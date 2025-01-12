class Player:
    def __init__(self,stack,name,num):
        self.stack = stack
        self.start_stack = stack
        self.name = name
        self.card = []
        self.num = num
        self.bet_amount = 0
        self.last_player_act = None
        self.first_bet_amount = 0
        self.card_rank = None
        self.card_rank_text = None
    
    def get(self,get_amount):
        self.stack += get_amount
    
    def recieve_card(self, card):
        self.card.append(card)
    
    def reset(self):
        self.bet_amount = 0
        self.card = []
        self.last_player_act = None
        self.card_rank = None
        self.card_rank_text = None
    
    def bet(self,bet_amount):
        self.bet_amount += bet_amount
        self.stack -= bet_amount

    def take_action(self,field_max_bet,action):
        if action == "f":
            self.last_player_act = "f"
            return "f"
        elif action == "check":
            call_amount = field_max_bet - self.bet_amount
            self.stack -= call_amount
            self.bet_amount += call_amount
            self.last_player_act = "check"
            return "check"
        elif action == "call":
            call_amount = field_max_bet - self.bet_amount
            self.stack -= call_amount
            self.bet_amount += call_amount
            self.last_player_act = "call"
            return "call"
        elif action == "r_2":
            total_bet_amount = 2 * field_max_bet
            raise_amount = total_bet_amount - self.bet_amount

            self.stack -= (raise_amount)
            self.bet_amount  = total_bet_amount
            self.last_player_act = "r_2"
            return "r_2"
        elif action == "r_3":
            total_bet_amount = 3 * field_max_bet
            raise_amount = total_bet_amount - self.bet_amount

            self.stack -= (raise_amount)
            self.bet_amount  = total_bet_amount
            self.last_player_act = "r_3"
            return "r_3"
        elif action == "r_5":
            total_bet_amount = 5 * field_max_bet
            raise_amount = total_bet_amount - self.bet_amount

            self.stack -= (raise_amount)
            self.bet_amount  = total_bet_amount
            self.last_player_act = "r_5"
            return "r_5"

        # elif action== "a":
        #     self.bet_amount += self.stack
        #     self.stack = 0
        #     return "a"