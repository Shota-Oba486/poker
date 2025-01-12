import numpy as np
from env.ranking import rank_of_multi_card
from train.hand_strength.flop_turn import flop_turn_str

"""
Args:
    start_stack
    stack
    bet_amount
    max_bet_amount
    hand_card
    field_card
    phase
    last_field_act
    last_player_act
    r_count
    first_index
    current_index

Returns:23桁
    [c_require_rate,r_require_rate]:2
    [rank,str_in_rank,outs_rate]:3
    last_player_act_encoded:5
    last_field_act_encoded:5
    r_count:
    canend_flag
    [stack_size,bet_size,call_size,raise_size]:4
"""

def encode_state_12(start_stack,stack,bet_amount,max_bet_amount,hand_card,field_card,phase,last_field_act,last_player_act,r_count,first_index,agent_num):
    canend_flag = True
    if first_index != None:
        if first_index == agent_num:
            canend_flag = False

    cards = hand_card + field_card
    ### プレイヤーが二人の時を想定（プレイヤーが増えたときは変更する必要あり）
    if max_bet_amount != bet_amount:
        c_require_rate = (max_bet_amount - bet_amount) / (max_bet_amount * 2)
    else:
        c_require_rate = 0

    r_require_rate = (max_bet_amount * 2 - bet_amount) / (max_bet_amount * 2 * 2)
    rank,str_in_rank,outs_rate = 0,0,0

    if phase == 1:
        rank,high,outs = flop_turn_str(cards)
        str_in_rank = (high % (10 ** 10)) /10**9
        outs_rate = 2 * outs / 47
    if phase == 2:
        rank,high,outs = flop_turn_str(cards)
        str_in_rank = (high % (10 ** 10)) /10**9
        outs_rate = outs / 46

    act_to_num = {"f":0,"check":1,"call":2,"r_2":3,"r_3":4,"r_5":5}
    last_field_act_encoded = np.zeros(6)
    last_player_act_encoded = np.zeros(6)
    if last_field_act != None:
        last_field_act_num = act_to_num[last_field_act]
        last_field_act_encoded[last_field_act_num] = 1
    if last_player_act != None:
        last_player_act_num = act_to_num[last_player_act]
        last_player_act_encoded[last_player_act_num] = 1

    stack_size = stack/start_stack
    bet_size = bet_amount/start_stack
    call_size = (max_bet_amount-bet_amount)/start_stack
    raise_size = max_bet_amount/start_stack
    
    # 全ての情報を結合
    state_vector = np.concatenate([
        [c_require_rate,r_require_rate],
        [rank,str_in_rank,outs_rate],
        last_player_act_encoded,
        last_field_act_encoded,
        [r_count/4],
        [int(canend_flag)],
        [stack_size,bet_size,call_size,raise_size],
    ])

    return state_vector

if __name__ == "__main__":
    start_stack = 10000
    stack = 9000
    bet_amount = 200
    max_bet_amount = 200

    player_hand = ["9s","7c"]
    field_card = ["Ks","Ts","Qs","8s"]

    phase = 2
    last_field_act = "r_2"
    last_player_act = "r_2"
    r_count = 1
    first_index = 1
    current_index = 1

    a = encode_state_12(start_stack,stack,bet_amount,max_bet_amount,player_hand,field_card,phase,last_field_act,last_player_act,r_count,first_index,current_index)
    print(a)
    print(a.shape)