import numpy as np
from hand_strength.preflop import pf_str_yokosawa
from hand_strength.flop_turn import flop_turn_str
from ranking import rank_of_multi_card

"""
Args:
    bet_amount
    max_bet_amount
    hand_card
    field_card
    phase
    last_field_act
    last_player_act
    r_count


Returns:18桁
    [c_require_rate,r_require_rate]:2
    [rank,str_in_rank,outs_rate]:3
    [pf_str]:1
    phase_encoded:4
    last_player_act_encoded:3
    last_field_act_encoded:3
    r_count:
"""

def encode_state(bet_amount,max_bet_amount,hand_card,field_card,phase,last_field_act,last_player_act,r_count):

    cards = hand_card + field_card
    ### プレイヤーが二人の時を想定（プレイヤーが増えたときは変更する必要あり）
    if max_bet_amount != bet_amount:
        c_require_rate = (max_bet_amount - bet_amount) / (max_bet_amount * 2)
    else:
        c_require_rate = 0

    r_require_rate = (max_bet_amount * 2 - bet_amount) / (max_bet_amount * 2 * 2)

    rank,str_in_rank,outs_rate = 0,0,0

    pf_str = pf_str_yokosawa(hand_card)
    if phase == 1:
        rank,high,outs = flop_turn_str(cards)
        str_in_rank = (high % (10 ** 10)) /10**9
        outs_rate = 2 * outs / 47
    if phase == 2:
        rank,high,outs = flop_turn_str(cards)
        str_in_rank = (high % (10 ** 10)) /10**9
        outs_rate = outs / 46
    if phase == 3:
        high,rank = rank_of_multi_card(cards)[2],rank_of_multi_card(cards)[3],
        str_in_rank = (high % (10 ** 10)) /10**9

    phase_encoded = np.zeros(5)
    phase_encoded[phase] = 1

    act_to_num = {"f":0,"c":1,"r":2}
    last_field_act_encoded = np.zeros(3)
    last_player_act_encoded = np.zeros(3)
    if last_field_act != None:
        last_field_act_num = act_to_num[last_field_act]
        last_field_act_encoded[last_field_act_num] = 1
    if last_player_act != None:
        last_player_act_num = act_to_num[last_player_act]
        last_player_act_encoded[last_player_act_num] = 1

    # 全ての情報を結合
    state_vector = np.concatenate([
        [c_require_rate,r_require_rate],
        [rank,str_in_rank,outs_rate],
        [pf_str],
        phase_encoded,  # フェーズ情報
        last_player_act_encoded,
        last_field_act_encoded,
        [r_count/4]
    ])

    return state_vector

# ####状態の例c

# bet_amount = 200
# max_bet_amount = 200

# player_hand = ["9s","7c"]
# field_card = ["Ks","Ts","Qs","8s"]

# phase = 2

# last_field_act = "r"
# last_player_act = "r"
# r_count = 1
# a = encode_state(bet_amount,max_bet_amount,player_hand,field_card,phase,last_field_act,last_player_act,r_count)
# print(a)
# print(a.shape)