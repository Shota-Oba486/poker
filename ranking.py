import itertools
import collections

def rank_of_five_card(five_card_list):
    rank_to_num = {'A': 14, 'K': 13, 'Q': 12, 'J': 11, 'T': 10, '9': 9, '8': 8, '7': 7, '6': 6, '5': 5, '4': 4, '3': 3,'2': 2}
    """
    9:royal straight flush
    8:four card
    7:full house
    6:flush
    5:straight
    4:three card
    3:two pair 
    2:one pair
    1:no pair
    """
    
    ### 5枚のカードを数値化
    number_ranks = [rank_to_num[card[0]] for card in five_card_list]
    num_cnt = collections.Counter(number_ranks)
    num_cnt = sorted(num_cnt.items(), key=lambda x: -x[0] - x[1]*100)
    num_list = sorted(list(num_cnt),reverse=True)

    high = sum([item[0] * 100 ** (4 - i) for i, item in enumerate(num_cnt)])

    ### 絵札をリスト化
    suits = [card[1] for card in five_card_list]
    suits_cnt = collections.Counter(suits)
    is_flush = len(suits_cnt) == 1

    if len(num_cnt) == 2:
        if num_cnt[0][1] == 4:
            rank_text,rank = "four card", 8
        else:
            rank_text,rank = "full house", 7
    elif len(num_cnt) == 3:
        if num_cnt[0][1] == 3:
            rank_text,rank = "three card", 4
        else:
            rank_text,rank = "two pair", 3
    elif len(num_cnt) == 4:
        rank_text,rank = "one pair", 2
    else:
        is_straight = (num_list[0][0] - num_list[4][0] == 4) or (num_list[0][0] == 14 and num_list[1][0] == 5)
        if is_flush:
            if is_straight:
                rank_text,rank = "straight flush", 9
            else:
                rank_text,rank = "flush", 6
        else:
            if is_straight:
                rank_text,rank = "straight", 5
            else:
                rank_text,rank = "nothing", 1
    
    high = rank * 10 ** 10 + high
    return rank_text,rank,high

def rank_of_multi_card(cards):
    best_rank_num = 0
    five_card_list = itertools.combinations(cards, 5)

    for five_card in five_card_list:
        ranks = rank_of_five_card(five_card)
        if ranks[2] > best_rank_num:
            best_rank_num = ranks[2]
            best_five_card = five_card
            best_rank_text = ranks[0]
            rank = best_rank_num // (10 ** 10)
    return best_five_card, best_rank_text, best_rank_num,rank