"""
Args:
    start_stack
    stack
    bet_amount
    max_bet_amount
    hand_card
    last_field_act
    last_player_act
    r_count
    first_index
    agent_num

Returns:18桁
    hand_strength:
    suit_flag:
    r_count:
    last_player_act_encoded:
    last_field_act_encoded:
    canend_flag
    [stack_size,bet_size,call_size,raise_size]:4
"""
import numpy as np
import pickle
with open('train/hand_strength/preflop_dict/s.pkl', 'rb') as f:
    s_dict = pickle.load(f)
with open('train/hand_strength/preflop_dict/o.pkl', 'rb') as f:
    o_dict = pickle.load(f)

def encode_state_0(start_stack,stack,bet_amount,max_bet_amount,hand_card,last_field_act,last_player_act,r_count,first_index,agent_num):

    canend_flag = True
    if first_index != None:
        if first_index == agent_num:
            canend_flag = False

    rank_to_num = {'A': 14, 'K': 13, 'Q': 12, 'J': 11, 'T': 10, '9': 9, '8': 8, '7': 7, '6': 6, '5': 5, '4': 4, '3': 3,'2': 2}

    num0 = rank_to_num[hand_card[0][0]]
    num1 = rank_to_num[hand_card[1][0]]

    if num0 <= num1:
        small_num = hand_card[0][0]
        big_num = hand_card[1][0]
    else:
        small_num = hand_card[1][0]
        big_num = hand_card[0][0]

    if hand_card[0][1] == hand_card[1][1]:
        hand_strength = s_dict[("same",small_num,big_num)]
        suit_flag = 1
    else:
        hand_strength = o_dict[("diff",small_num,big_num)]
        suit_flag = 0

    act_to_num = {"f":0,"check":1,"call":2,"r_2":3,"r_3":4,"r_5":5}
    last_field_act_encoded = np.zeros(6)
    last_player_act_encoded = np.zeros(6)
    if last_field_act != None:
        last_field_act_num = act_to_num[last_field_act]
        last_field_act_encoded[last_field_act_num] = 1
    if last_player_act != None:
        last_player_act_num = act_to_num[last_player_act]
        last_player_act_encoded[last_player_act_num] = 1
    # 全ての情報を結合
    stack_size = stack/start_stack
    bet_size = bet_amount/start_stack
    call_size = (max_bet_amount-bet_amount)/start_stack
    raise_size = max_bet_amount/start_stack

    state_vector = np.concatenate([
        [hand_strength],
        [suit_flag],
        [r_count/4],
        last_player_act_encoded,
        last_field_act_encoded,
        [int(canend_flag)],
        [stack_size,bet_size,call_size,raise_size],
        [0,0,0]
    ])

    return state_vector

if __name__ == "__main__":
    start_stack = 10000
    stack = 9000
    bet_amount = 200
    max_bet_amount = 200

    player_hand = ["9s","7c"]
    last_field_act = "r_2"
    last_player_act = "r_2"
    r_count = 1
    first_flag = True
    first_index = 1
    current_index = 1
    a = encode_state_0(start_stack,stack,bet_amount,max_bet_amount,player_hand,last_field_act,last_player_act,r_count,first_index,current_index)
    print(a)
    print(a.shape)