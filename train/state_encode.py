import numpy as np
from train.hand_strength.flop_turn import flop_turn_str
import pickle
with open('train/hand_strength/preflop_dict/s.pkl', 'rb') as f:
    s_dict = pickle.load(f)
with open('train/hand_strength/preflop_dict/o.pkl', 'rb') as f:
    o_dict = pickle.load(f)

"""
Args:
    start_stack
    stack
    opponent_stack
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

Returns:17桁
    [c_require_rate,r_require_rate]:2
    [rank,str_in_rank,outs_rate]:3
    last_player_act_encoded:5
    last_field_act_encoded:5
    r_count:
    canend_flag
    [stack_size,bet_size,call_size,raise_size]:4
"""

def encode_state(start_stack,stack,opponent_stack,bet_amount,max_bet_amount,hand_card,field_card,phase,last_field_act,last_player_act,r_count,first_index,agent_num):
    canend_flag = True
    if first_index != None:
        if first_index == agent_num:
            canend_flag = False

    if phase == 0:
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
    
    if phase == 1 or phase == 2 or phase == 3 or phase == 4:

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
    if last_field_act != None:
        last_field_act_num = act_to_num[last_field_act]
        last_field_act_encoded[last_field_act_num] = 1

    stack_size = stack/start_stack
    opponent_stack_size = opponent_stack/start_stack
    bet_size = bet_amount/start_stack
    call_size = (max_bet_amount-bet_amount)/start_stack
    raise_size = max_bet_amount/start_stack
    
    common_state_vector = np.concatenate([
        last_field_act_encoded,
        [int(canend_flag)],
        [stack_size,opponent_stack_size,bet_size,call_size,raise_size]
    ])

    if phase == 0:
        state_vector = np.concatenate([
            common_state_vector,
            np.array([hand_strength,suit_flag]),
            np.array([0,0,0])
        ])
    if phase == 1 or phase == 2:
        state_vector = np.concatenate([
            np.array(common_state_vector),
            np.array([c_require_rate,r_require_rate]),
            np.array([rank,str_in_rank,outs_rate])
        ])
    if phase == 3 or phase == 4:
        state_vector = np.concatenate([
            common_state_vector,
            np.array([rank,str_in_rank]),
            np.array([0,0,0])
        ])

    return state_vector

if __name__ == "__main__":
    start_stack = 10000
    stack = 9000
    opponent_stack = 8000
    bet_amount = 200
    max_bet_amount = 200

    player_hand = ["9s","7c"]
    field_card = ["Ks","Ts","Qs","8s"]

    phase = 3
    last_field_act = "r_2"
    last_player_act = "r_2"
    r_count = 1
    first_index = 1
    current_index = 1

    a = encode_state(start_stack,stack,opponent_stack,bet_amount,max_bet_amount,player_hand,field_card,phase,last_field_act,last_player_act,r_count,first_index,current_index)
    print(a)
    print(a.shape)