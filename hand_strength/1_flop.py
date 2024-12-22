import sys
import os 
from collections import Counter
sys.path.append(os.path.abspath('..'))

# モジュールをインポート
from ranking import rank_of_five_card


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
    print(unique_ranks)

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
    print(unique_ranks)
    ### numの種類が3種類以下だったら、flushdrawの可能性がないので、return 0
    if len(unique_ranks) <= 3:
        return 
    ### straightだったら、0
    if is_straight(unique_ranks):
        return 0
    ### それ以外の場合（numの種類が4種類以上の場合)
    min_num = max(1,unique_ranks[-1]-1)
    max_num = min(14,unique_ranks[0]+1)

    for i in range (min_num,max_num+1):
        if not i in ranks:
            print(i)
            append_i_cards = list(unique_ranks)
            append_i_cards.append(i)

            if is_straight(append_i_cards):
                outs_list.append(i)
    return len(set(outs_list))