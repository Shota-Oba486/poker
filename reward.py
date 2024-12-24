"""
Args:
    field_max_bet
    player_bet_amount
    phase:0,1,2,3,4（preflop,flop,river,turn）
    player_card:
    field_card
    action:"f","c","r"
    # sb_player_flag:True or False
    last_player_act
    last_field_act
    r_count

Returns:
    reward
"""

from hand_strength.preflop import pf_str_yokosawa
from hand_strength.flop_turn import flop_turn_str

def decide_reward(field_max_bet,player_bet_amount,phase,player_card,field_card,action,last_player_act,last_field_act,action_count_phase):
    action_to_index = {"f":0,"c":1,"r":2}
    action_index = action_to_index[action]

    if phase == 0:

        ### pf_strは1~7のint型
        pf_str = pf_str_yokosawa(player_card)
        opti_index = pf_str - 2 - action_count_phase

        if opti_index < 0:
            reward_list = [0.5,0,-0.5]
        elif opti_index == 0:
            reward_list = [0,0.5,0]
        elif opti_index > 0:
            reward_list = [-0.5,0,0.5]

    if phase == 1 or phase == 2:

        rank,high,outs = flop_turn_str(player_card + field_card)

        if phase == 1:
            outs_rate = 2*outs/ 47
        elif phase == 2:
            outs_rate = outs / 46

        if rank == 1:
            # プレイヤーが二人の時を仮定
            # 変更する必要あり
            c_rate = (field_max_bet - player_bet_amount) / player_bet_amount * 2
            r_rate = (field_max_bet * 2 - player_bet_amount) / player_bet_amount * 2 * 2

            if outs_rate >= r_rate:
                # raiseしても割に合う
                reward_list = [-0.3,0,0.3]
            elif outs_rate >= c_rate:
                # callも割に合う
                reward_list = [-0.15,0.3,-0.15]
            else:
                # raiseもcallも割に合わない
                reward_list = [0.25,-0.1,-0.15]

        elif rank == 2:
            str_in_rank = (high % (10 ** 10)) /10**9
            # str_in_rank のrangeは 0~0.7 くらい
            reward_list = [-(str_in_rank -0.2),str_in_rank - 0.4,str_in_rank - 0.2]

        elif rank >= 3:
            str_in_rank = 0.5 * (high % (10 ** 10)) /10**9
            reward_list = [-0.3,0,0.3]
        
        if last_field_act == "r":
            if action == "r":
                reward_list[2] -= 0.2
                ### raiseのreward　-0.2
        elif last_player_act == "c":
            if action == "c":
                reward_list[2] -= 0.2
                ### raiseのreward　-0.2

    if phase == 3:

        rank,high,outs = flop_turn_str(player_card + field_card)
        if rank == 1:
            reward_list = [0,0,-0.3]
        if rank == 2:
            str_in_rank = (high % (10 ** 10)) /10**9
            reward_list = [-0.15,0.3,0.15]
        if rank >= 3:
            reward_list = [-0.5,0,0.5]

        if last_field_act == "r":
            if action == "r":
                reward_list[2] -= 0.2
        if last_player_act == "c":
            if action == "c":
                reward_list[2] -=0.2
                ### raiseのreward　-0.2

    print(reward_list)
    reward = reward_list[action_index]
    return reward

#### テスト

# field_max_bet = 200
# player_bet_amount = 100
# phase = 1
# player_card = []
# field_card = []
# action = "c"
# last_player_act = "r"
# last_field_act = "r"
# action_count_phase = 3


# reward = decide_reward(field_max_bet,player_bet_amount,phase,player_card,field_card,action,last_player_act,last_field_act,action_count_phase)
# print(reward)