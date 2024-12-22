import pickle
from ranking import rank_of_five_card
from ranking import rank_of_six_card
from ranking import rank_of_seven_card

with open('2_hand.pkl', 'rb') as f:
    dict = pickle.load(f)

def judge_2hand(player_hand):

    if player_hand[0][1] == player_hand[1][1]:
        cond0 = "same"
    else:
        cond0 = "diff"
    
    rank_to_num = {'A': 14, 'K': 13, 'Q': 12, 'J': 11, 'T': 10, '9': 9, '8': 8, '7': 7, '6': 6, '5': 5, '4': 4, '3': 3,'2': 2}
    if rank_to_num[player_hand[0][0]] <= rank_to_num[player_hand[1][0]]:
        cond1,cond2 = player_hand[0][0], player_hand[1][0]
    else:
        cond1,cond2 = player_hand[1][0], player_hand[0][0]
    return dict[(cond0,cond1,cond2)]

def hand_state(player_hand,field_card):
    cards = player_hand + field_card

    if len(field_card) == 0:
        hand_strength = judge_2hand(player_hand)
    elif len(field_card) == 3:
        rank,high = rank_of_five_card(cards)[1],rank_of_five_card(cards)[2]
        hand_strength = 0.8 if rank >= 4 else 0.7 if rank >= 3 else 0.6 if rank >= 2 else (high/(10 **11))
    elif len(field_card) == 4:
        high = rank_of_six_card(cards)[2]
        rank = (high // (10 ** 10))
        hand_strength = 0.8 if rank >= 4 else 0.7 if rank >= 3 else 0.6 if rank >= 2 else (high/(10 **11))
    elif len(field_card) == 5:
        high = rank_of_seven_card(cards)[2]
        rank = (high // (10 ** 10))
        hand_strength = 0.8 if rank >= 4 else 0.7 if rank >= 3 else 0.6 if rank >= 2 else (high/(10 **11))

    return hand_strength

# import random
# for _ in range(10000):
#     deck = [
#         "As", "Ad", "Ac", "Ah",
#         "Ks", "Kd", "Kc", "Kh",
#         "Qs", "Qd", "Qc", "Qh",
#         "Js", "Jd", "Jc", "Jh",
#         "Ts", "Td", "Tc", "Th",
#         "9s", "9d", "9c", "9h",
#         "8s", "8d", "8c", "8h",
#         "7s", "7d", "7c", "7h",
#         "6s", "6d", "6c", "6h",
#         "5s", "5d", "5c", "5h",
#         "4s", "4d", "4c", "4h",
#         "3s", "3d", "3c", "3h",
#         "2s", "2d", "2c", "2h"
#     ]

#     random.shuffle(deck)
#     player_hand = []
#     player_hand.append(deck[0])
#     player_hand.append(deck[1])
#     field_card = []
#     field_card.append(deck[2])
#     field_card.append(deck[3])
#     field_card.append(deck[4])
#     field_card.append(deck[5])
#     field_card.append(deck[6])

#     reward = decide_reward(player_hand,field_card,2,"r")
#     print(field_card,player_hand)
#     print(reward)