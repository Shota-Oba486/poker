from collections import Counter
from env.ranking import rank_of_multi_card
"""
Args:
    cards:hand_card + field_card
    cardは5枚か6枚

Retunrs:
    rank:rank
    high:high
    outs:outsの数
"""

def is_flush_chance(cards):
    suits = [card[1] for card in cards]
    suit_counts = Counter(suits)
    if max(suit_counts.values()) == 4:
        return True
    return False

def is_straight(num_list):
    ranks = set(num_list)

    # エースを1として扱うための調整
    if 14 in ranks:
        ranks.add(1)
    unique_ranks = sorted(ranks,reverse=True)
    
    if len(unique_ranks) >= 5:
        for i in range(0,len(unique_ranks)-4):
            if (unique_ranks[i] - unique_ranks[i + 4]) == 4:
                return True
    return False

def outs_num_straight(cards):
    rank_dict = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, 'T': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14}
    # カードのランク部分を数値に変換してセットに格納
    ranks = set(rank_dict[card[0]] for card in cards)
    outs_list = []

    # エースを1として扱うための調整
    if 14 in ranks:
        ranks.add(1)
    unique_ranks = sorted(ranks,reverse=True) 
    ### numの種類が3種類以下だったら、flushdrawの可能性がないので、return 0
    if len(unique_ranks) <= 3:
        return 0
    ### straightだったら、0
    if is_straight(unique_ranks):
        return 0
    ### それ以外の場合（numの種類が4種類以上の場合)
    min_num = max(1,unique_ranks[-1]-1)
    max_num = min(14,unique_ranks[0]+1)

    for i in range (min_num,max_num+1):
        if not i in ranks:
            append_i_cards = list(unique_ranks)
            append_i_cards.append(i)

            if is_straight(append_i_cards):
                outs_list.append(i)
    return len(set(outs_list))

def flop_turn_str(cards):
    high,rank = rank_of_multi_card(cards)[2],rank_of_multi_card(cards)[3]
    
    outs = 0
    if rank == 1:
        ### フラッシュの可能性について
        if is_flush_chance(cards):
            outs += 9
        ### straightの可能性について
        if outs != 0:
            outs += outs_num_straight(cards) * 4 - 2
        else:
            outs += outs_num_straight(cards) * 4

    return rank,high,outs

import random

if __name__ == "__main__":
    deck = [
        "As", "Ad", "Ac", "Ah",
        "Ks", "Kd", "Kc", "Kh",
        "Qs", "Qd", "Qc", "Qh",
        "Js", "Jd", "Jc", "Jh",
        "Ts", "Td", "Tc", "Th",
        "9s", "9d", "9c", "9h",
        "8s", "8d", "8c", "8h",
        "7s", "7d", "7c", "7h",
        "6s", "6d", "6c", "6h",
        "5s", "5d", "5c", "5h",
        "4s", "4d", "4c", "4h",
        "3s", "3d", "3c", "3h",
        "2s", "2d", "2c", "2h"
    ]
    random.shuffle(deck)

    player_hand = []
    field_card = []
    player_hand.append(deck[0])
    player_hand.append(deck[1])
    field_card.append(deck[2])
    field_card.append(deck[3])
    field_card.append(deck[4])

    # player_hand = ["9s","7c"]
    # field_card = ["Ks","Ts","Qs","8s"]

    player_hand = ["9s","7c"]
    field_card = ["Ks","Ts","Qs","8s"]


    print(flop_turn_str(player_hand + field_card))