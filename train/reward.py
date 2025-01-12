"""
Args:
    pod
    field_max_bet
    player_bet_amount
    action:"f","check","call","r_2","r_3","r_5"
    winner_flag
    mask
    phase

Returns:
    reward
"""

import numpy as np

def normalize_array(arr):

    # 負の数の部分を正規化（最小値を-1に）
    negative_mask = arr < 0
    if np.any(negative_mask):  # 負の数が存在する場合のみ処理
        negative_values = arr[negative_mask]
        min_neg = np.min(negative_values)
        arr[negative_mask] = arr[negative_mask] / abs(min_neg)  # -1にスケール

    # 正の数の部分を正規化（最大値を1に）
    positive_mask = arr > 0
    if np.any(positive_mask):  # 正の数が存在する場合のみ処理
        positive_values = arr[positive_mask]
        max_pos = np.max(positive_values)
        arr[positive_mask] = arr[positive_mask] / max_pos
    
    return arr

def decide_reward(
        pod,
        field_max_bet,
        player_bet_amount,
        action,
        winner_flag,
        mask,
        phase,
        first_bet_amount):
    action_to_index = {"f":0,"check":1,"call":2,"r_2":3,"r_3":4,"r_5":5}
    action_index = action_to_index[action]

    if winner_flag:
        f_reward = - pod / 1000
        check_reward = 0
        call_reward = 0
        r_2_reward = ((field_max_bet * 1))/ 1000
        r_3_reward = ((field_max_bet * 2))/ 1000
        r_5_reward = ((field_max_bet * 4))/ 1000

    else:
        f_reward = (field_max_bet - player_bet_amount) /1000
        check_reward = 0
        call_reward = -((field_max_bet - player_bet_amount)/1000)
        r_2_reward = - ((2 * field_max_bet - player_bet_amount)/1000)
        r_3_reward = - ((3 * field_max_bet - player_bet_amount)/1000)
        r_5_reward = - ((5 * field_max_bet - player_bet_amount)/1000)

    lst = np.array([f_reward, check_reward, call_reward, r_2_reward, r_3_reward, r_5_reward])
    mask = np.array(mask)
    reward_list = lst * mask
    # reward_list = normalize_array(reward_list)
    reward = reward_list[action_index]
    return reward

if __name__ == "__main__":
    pod = 300
    field_max_bet = 2000
    player_bet_amount = 1000
    phase = 1
    player_card = []
    field_card = []
    field_card_truth = []
    action = "r_2"
    last_player_act = "r_2"
    last_field_act = "r_2"
    action_count_phase = 3
    winner_flag = True
    mask = [1,1,1,1,1,1]
    phase = 1
    first_bet_amount = 100

    print(decide_reward(
        pod,
        field_max_bet,
        player_bet_amount,
        action,
        winner_flag,
        mask,
        phase,
        first_bet_amount
        ))