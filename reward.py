"""
Args:
    field_max_bet
    player_bet_amount
    phase:0,1,2,3,4（preflop,flop,river,turn）
    player_card:
    field_card
    action:"f","c","r"
    sb_player_flag:True or False

Returns:
    reward
"""
from hand_strength.preflop import pf_str_sb
from hand_strength.preflop import pf_str_bb
from hand_strength.preflop import pf_str_yokosawa
from hand_strength.flop_turn import flop_turn_str

def decide_reward(field_max_bet,player_bet_amount,phase,player_card,field_card,action,sb_player_flag,):

    if phase == 0:
        ### pf_str を定める
        if sb_player_flag:
            pf_str = pf_str_sb(player_card)
        else:
            pf_str = pf_str_bb(player_card)
            
        if action == "r":
            # -0.75,-0.25,0.25,0.75
            reward = (pf_str - 2.5)/2
        if action == "c":
            # -0.25,0.25,0.25,0.25
            if pf_str == 2 or pf_str == 3:
                reward = 0.25
            else:
                reward = - 0.25
        if action == "f":
            # 0.5,0.0,-0.5,-1.0
            reward = ( - (pf_str)+2) / 2

    if phase == 1 or phase == 2:

        rank,high,outs = flop_turn_str(player_card + field_card)

        if phase == 1:
            outs_rate = 2 * outs/47
        if phase == 2:
            outs_rate = outs /46

        if rank == 1:
            # プレイヤーが二人の時を仮定
            # 変更する必要あり
            c_rate = (field_max_bet - player_bet_amount) / player_bet_amount * 2
            r_rate = (field_max_bet*2 - player_bet_amount) / player_bet_amount * 2 * 2

            if outs_rate >= r_rate:
                if action == "r":
                    reward = 0.5
                if action == "c":
                    reward = -0.25
                if action == "f":
                    reward = -0.5
            elif outs_rate >= c_rate:
                if action == "r":
                    reward = -0.25
                if action == "c":
                    reward = 0.5
                if action == "f":
                    reward = -0.4
            else:
                if outs_rate >= 0.1:
                    if action == "r":
                        reward = -0.5
                    if action == "c":
                        reward = -0.1
                    if action == "f":
                        reward = 0.1
                else:
                    if action == "r":
                        reward = -0.5
                    if action == "c":
                        reward = -0.4
                    if action == "f":
                        reward = 0.4
        if rank == 2:
            str_in_rank = 0.5 * (high % (10 ** 10)) /10**9
            if action == "r":
                reward = str_in_rank - 0.2
            if action == "c":
                reward = str_in_rank - 0.4
            if action == "f":
                reward = -(str_in_rank - 0.2)
        if rank >= 3:
            if action == "r":
                reward = 1
            if action == "c":
                reward = -0.5
            if action == "f":
                reward = -1.0

    if phase == 3:

        rank,high,outs = flop_turn_str(player_card + field_card)
        if rank == 1:
            if action == "r":
                reward = -0.5
            if action == "c":
                reward = -0.05
            if action == "f":
                reward = 0.05
        if rank == 2:
            str_in_rank = 0.5 * (high % (10 ** 10)) /10**9
            if action == "r":
                reward = str_in_rank - 0.2
            if action == "c":
                reward = str_in_rank - 0.4
            if action == "f":
                reward = -(str_in_rank - 0.2)
        if rank >= 3:
            if action == "r":
                reward = 1
            if action == "c":
                reward = -0.5
            if action == "f":
                reward = -1.0
    
    return reward