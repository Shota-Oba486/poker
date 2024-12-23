"""
Args:引数は一つ

    [hand_card + field_card]

Returns:hand_strength
    4:raise
    3:raise or call
    2:call
    1:fold
"""

pf_sb_dict_same = {
    frozenset(["A","K"]): 4,
    frozenset(["A","Q"]): 4,
    frozenset(["A","J"]): 4,
    frozenset(["A","T"]): 4,
    frozenset(["A","9"]): 4,
    frozenset(["A","8"]): 4,
    frozenset(["A","7"]): 4,
    frozenset(["A","6"]): 2,
    frozenset(["A","5"]): 4,
    frozenset(["A","4"]): 4,
    frozenset(["A","3"]): 4,
    frozenset(["A","2"]): 2,

    frozenset(["K","Q"]): 4,
    frozenset(["K","J"]): 4,
    frozenset(["K","T"]): 4,
    frozenset(["K","9"]): 4,
    frozenset(["K","8"]): 4,
    frozenset(["K","7"]): 2,
    frozenset(["K","6"]): 2,
    frozenset(["K","5"]): 3,
    frozenset(["K","4"]): 3,
    frozenset(["K","3"]): 3,
    frozenset(["K","2"]): 2,

    frozenset(["Q","J"]): 4,
    frozenset(["Q","T"]): 4,
    frozenset(["Q","9"]): 4,
    frozenset(["Q","8"]): 4,
    frozenset(["Q","7"]): 4,
    frozenset(["Q","6"]): 2,
    frozenset(["Q","5"]): 2,
    frozenset(["Q","4"]): 4,
    frozenset(["Q","3"]): 2,
    frozenset(["Q","2"]): 4,

    frozenset(["J","T"]): 4,
    frozenset(["J","9"]): 4,
    frozenset(["J","8"]): 2,
    frozenset(["J","7"]): 4,
    frozenset(["J","6"]): 2,
    frozenset(["J","5"]): 2,
    frozenset(["J","4"]): 2,
    frozenset(["J","3"]): 2,
    frozenset(["J","2"]): 2,

    frozenset(["T","9"]): 4,
    frozenset(["T","8"]): 2,
    frozenset(["T","7"]): 4,
    frozenset(["T","6"]): 4,
    frozenset(["T","5"]): 2,
    frozenset(["T","4"]): 2,
    frozenset(["T","3"]): 1,
    frozenset(["T","2"]): 1,

    frozenset(["9","8"]): 4,
    frozenset(["9","7"]): 4,
    frozenset(["9","6"]): 4,
    frozenset(["9","5"]): 2,
    frozenset(["9","4"]): 1,
    frozenset(["9","3"]): 1,
    frozenset(["9","2"]): 1,

    frozenset(["8","7"]): 3,
    frozenset(["8","6"]): 4,
    frozenset(["8","5"]): 2,
    frozenset(["8","4"]): 1,
    frozenset(["8","3"]): 1,
    frozenset(["8","2"]): 1,

    frozenset(["7","6"]): 4,
    frozenset(["7","5"]): 3,
    frozenset(["7","4"]): 2,
    frozenset(["7","3"]): 1,
    frozenset(["7","2"]): 1,

    frozenset(["6","5"]): 4,
    frozenset(["6","4"]): 2,
    frozenset(["6","3"]): 2,
    frozenset(["6","2"]): 1,

    frozenset(["5","4"]): 4,
    frozenset(["5","3"]): 4,
    frozenset(["5","2"]): 1,

    frozenset(["4","3"]): 2,
    frozenset(["4","2"]): 1,

    frozenset(["3","2"]): 1,
}

pf_sb_dict_dif = {
    frozenset(["A","A"]): 4,
    frozenset(["A","K"]): 4,
    frozenset(["A","Q"]): 4,
    frozenset(["A","J"]): 3,
    frozenset(["A","T"]): 2,
    frozenset(["A","9"]): 3,
    frozenset(["A","8"]): 2,
    frozenset(["A","7"]): 4,
    frozenset(["A","6"]): 2,
    frozenset(["A","5"]): 3,
    frozenset(["A","4"]): 4,
    frozenset(["A","3"]): 2,
    frozenset(["A","2"]): 2,

    frozenset(["K","K"]): 4,
    frozenset(["K","Q"]): 4,
    frozenset(["K","J"]): 4,
    frozenset(["K","T"]): 4,
    frozenset(["K","9"]): 4,
    frozenset(["K","8"]): 4,
    frozenset(["K","7"]): 2,
    frozenset(["K","6"]): 2,
    frozenset(["K","5"]): 4,
    frozenset(["K","4"]): 4,
    frozenset(["K","3"]): 1,
    frozenset(["K","2"]): 1,

    frozenset(["Q","Q"]): 3,
    frozenset(["Q","J"]): 4,
    frozenset(["Q","T"]): 4,
    frozenset(["Q","9"]): 4,
    frozenset(["Q","8"]): 4,
    frozenset(["Q","7"]): 3,
    frozenset(["Q","6"]): 4,
    frozenset(["Q","5"]): 1,
    frozenset(["Q","4"]): 1,
    frozenset(["Q","3"]): 1,
    frozenset(["Q","2"]): 1,

    frozenset(["J","J"]): 4,
    frozenset(["J","T"]): 4,
    frozenset(["J","9"]): 4,
    frozenset(["J","8"]): 4,
    frozenset(["J","7"]): 2,
    frozenset(["J","6"]): 1,
    frozenset(["J","5"]): 1,
    frozenset(["J","4"]): 1,
    frozenset(["J","3"]): 1,
    frozenset(["J","2"]): 1,

    frozenset(["T","T"]): 1,
    frozenset(["T","9"]): 1,
    frozenset(["T","8"]): 3,
    frozenset(["T","7"]): 2,
    frozenset(["T","6"]): 1,
    frozenset(["T","5"]): 1,
    frozenset(["T","4"]): 1,
    frozenset(["T","3"]): 1,
    frozenset(["T","2"]): 1,

    frozenset(["9","9"]): 4,
    frozenset(["9","8"]): 4,
    frozenset(["9","7"]): 3,
    frozenset(["9","6"]): 1,
    frozenset(["9","5"]): 1,
    frozenset(["9","4"]): 1,
    frozenset(["9","3"]): 1,
    frozenset(["9","2"]): 1,

    frozenset(["8","8"]): 4,
    frozenset(["8","7"]): 4,
    frozenset(["8","6"]): 1,
    frozenset(["8","5"]): 1,
    frozenset(["8","4"]): 1,
    frozenset(["8","3"]): 1,
    frozenset(["8","2"]): 1,

    frozenset(["7","7"]): 4,
    frozenset(["7","6"]): 4,
    frozenset(["7","5"]): 1,
    frozenset(["7","4"]): 1,
    frozenset(["7","3"]): 1,
    frozenset(["7","2"]): 1,

    frozenset(["6","6"]): 4,
    frozenset(["6","5"]): 4,
    frozenset(["6","4"]): 1,
    frozenset(["6","3"]): 1,
    frozenset(["6","2"]): 1,

    frozenset(["5","5"]): 4,
    frozenset(["5","4"]): 1,
    frozenset(["5","3"]): 1,
    frozenset(["5","2"]): 1,

    frozenset(["4","4"]): 3,
    frozenset(["4","3"]): 1,
    frozenset(["4","2"]): 1,

    frozenset(["3","3"]): 4,
    frozenset(["3","2"]): 1,

    frozenset(["2","2"]): 4,
}

pf_bb_dict_same = {
    frozenset(["A","K"]): 4,
    frozenset(["A","Q"]): 4,
    frozenset(["A","J"]): 3,
    frozenset(["A","T"]): 2,
    frozenset(["A","9"]): 2,
    frozenset(["A","8"]): 2,
    frozenset(["A","7"]): 2,
    frozenset(["A","6"]): 2,
    frozenset(["A","5"]): 2,
    frozenset(["A","4"]): 2,
    frozenset(["A","3"]): 2,
    frozenset(["A","2"]): 2,

    frozenset(["K","Q"]): 2,
    frozenset(["K","J"]): 2,
    frozenset(["K","T"]): 2,
    frozenset(["K","9"]): 2,
    frozenset(["K","8"]): 1,
    frozenset(["K","7"]): 1,
    frozenset(["K","6"]): 1,
    frozenset(["K","5"]): 1,
    frozenset(["K","4"]): 1,
    frozenset(["K","3"]): 1,
    frozenset(["K","2"]): 1,

    frozenset(["Q","J"]): 2,
    frozenset(["Q","T"]): 2,
    frozenset(["Q","9"]): 2,
    frozenset(["Q","8"]): 1,
    frozenset(["Q","7"]): 1,
    frozenset(["Q","6"]): 1,
    frozenset(["Q","5"]): 1,
    frozenset(["Q","4"]): 1,
    frozenset(["Q","3"]): 1,
    frozenset(["Q","2"]): 1,

    frozenset(["J","T"]): 2,
    frozenset(["J","9"]): 2,
    frozenset(["J","8"]): 1,
    frozenset(["J","7"]): 1,
    frozenset(["J","6"]): 1,
    frozenset(["J","5"]): 1,
    frozenset(["J","4"]): 1,
    frozenset(["J","3"]): 1,
    frozenset(["J","2"]): 1,

    frozenset(["T","9"]): 2,
    frozenset(["T","8"]): 1,
    frozenset(["T","7"]): 1,
    frozenset(["T","6"]): 1,
    frozenset(["T","5"]): 1,
    frozenset(["T","4"]): 1,
    frozenset(["T","3"]): 1,
    frozenset(["T","2"]): 1,

    frozenset(["9","8"]): 2,
    frozenset(["9","7"]): 1,
    frozenset(["9","6"]): 1,
    frozenset(["9","5"]): 1,
    frozenset(["9","4"]): 1,
    frozenset(["9","3"]): 1,
    frozenset(["9","2"]): 1,

    frozenset(["8","7"]): 2,
    frozenset(["8","6"]): 1,
    frozenset(["8","5"]): 1,
    frozenset(["8","4"]): 1,
    frozenset(["8","3"]): 1,
    frozenset(["8","2"]): 1,

    frozenset(["7","6"]): 2,
    frozenset(["7","5"]): 1,
    frozenset(["7","4"]): 1,
    frozenset(["7","3"]): 1,
    frozenset(["7","2"]): 1,

    frozenset(["6","5"]): 2,
    frozenset(["6","4"]): 1,
    frozenset(["6","3"]): 1,
    frozenset(["6","2"]): 1,

    frozenset(["5","4"]): 2,
    frozenset(["5","3"]): 1,
    frozenset(["5","2"]): 1,

    frozenset(["4","3"]): 1,
    frozenset(["4","2"]): 1,

    frozenset(["3","2"]): 1
}

pf_bb_dict_dif = {
    frozenset(["A","A"]): 4,
    frozenset(["A","K"]): 2,
    frozenset(["A","Q"]): 2,
    frozenset(["A","J"]): 2,
    frozenset(["A","T"]): 2,
    frozenset(["A","9"]): 1,
    frozenset(["A","8"]): 1,
    frozenset(["A","7"]): 1,
    frozenset(["A","6"]): 1,
    frozenset(["A","5"]): 1,
    frozenset(["A","4"]): 1,
    frozenset(["A","3"]): 1,
    frozenset(["A","2"]): 1,

    frozenset(["K","K"]): 4,
    frozenset(["K","Q"]): 2,
    frozenset(["K","J"]): 1,
    frozenset(["K","T"]): 1,
    frozenset(["K","9"]): 1,
    frozenset(["K","8"]): 1,
    frozenset(["K","7"]): 1,
    frozenset(["K","6"]): 1,
    frozenset(["K","5"]): 1,
    frozenset(["K","4"]): 1,
    frozenset(["K","3"]): 1,
    frozenset(["K","2"]): 1,

    frozenset(["Q","Q"]): 4,
    frozenset(["Q","J"]): 1,
    frozenset(["Q","T"]): 1,
    frozenset(["Q","9"]): 1,
    frozenset(["Q","8"]): 1,
    frozenset(["Q","7"]): 1,
    frozenset(["Q","6"]): 1,
    frozenset(["Q","5"]): 1,
    frozenset(["Q","4"]): 1,
    frozenset(["Q","3"]): 1,
    frozenset(["Q","2"]): 1,

    frozenset(["J","J"]): 4,
    frozenset(["J","T"]): 1,
    frozenset(["J","9"]): 1,
    frozenset(["J","8"]): 1,
    frozenset(["J","7"]): 1,
    frozenset(["J","6"]): 1,
    frozenset(["J","5"]): 1,
    frozenset(["J","4"]): 1,
    frozenset(["J","3"]): 1,
    frozenset(["J","2"]): 1,

    frozenset(["T","T"]): 2,
    frozenset(["T","9"]): 1,
    frozenset(["T","8"]): 1,
    frozenset(["T","7"]): 1,
    frozenset(["T","6"]): 1,
    frozenset(["T","5"]): 1,
    frozenset(["T","4"]): 1,
    frozenset(["T","3"]): 1,
    frozenset(["T","2"]): 1,

    frozenset(["9","9"]): 2,
    frozenset(["9","8"]): 1,
    frozenset(["9","7"]): 1,
    frozenset(["9","6"]): 1,
    frozenset(["9","5"]): 1,
    frozenset(["9","4"]): 1,
    frozenset(["9","3"]): 1,
    frozenset(["9","2"]): 1,

    frozenset(["8","8"]): 2,
    frozenset(["8","7"]): 1,
    frozenset(["8","6"]): 1,
    frozenset(["8","5"]): 1,
    frozenset(["8","4"]): 1,
    frozenset(["8","3"]): 1,
    frozenset(["8","2"]): 1,

    frozenset(["7","7"]): 2,
    frozenset(["7","6"]): 1,
    frozenset(["7","5"]): 1,
    frozenset(["7","4"]): 1,
    frozenset(["7","3"]): 1,
    frozenset(["7","2"]): 1,

    frozenset(["6","6"]): 2,
    frozenset(["6","5"]): 1,
    frozenset(["6","4"]): 1,
    frozenset(["6","3"]): 1,
    frozenset(["6","2"]): 1,

    frozenset(["5","5"]): 2,
    frozenset(["5","4"]): 1,
    frozenset(["5","3"]): 1,
    frozenset(["5","2"]): 1,

    frozenset(["4","4"]): 2,
    frozenset(["4","3"]): 1,
    frozenset(["4","2"]): 1,

    frozenset(["3","3"]): 2,
    frozenset(["3","2"]): 1,

    frozenset(["2","2"]): 2,
}

pf_yokosawa_same = {
    frozenset(["A","K"]): 7,
    frozenset(["A","Q"]): 6,
    frozenset(["A","J"]): 6,
    frozenset(["A","T"]): 6,
    frozenset(["A","9"]): 5,
    frozenset(["A","8"]): 5,
    frozenset(["A","7"]): 5,
    frozenset(["A","6"]): 5,
    frozenset(["A","5"]): 5,
    frozenset(["A","4"]): 5,
    frozenset(["A","3"]): 5,
    frozenset(["A","2"]): 5,

    frozenset(["K","Q"]): 6,
    frozenset(["K","J"]): 5,
    frozenset(["K","T"]): 4,
    frozenset(["K","9"]): 4,
    frozenset(["K","8"]): 2,
    frozenset(["K","7"]): 2,
    frozenset(["K","6"]): 2,
    frozenset(["K","5"]): 2,
    frozenset(["K","4"]): 2,
    frozenset(["K","3"]): 2,
    frozenset(["K","2"]): 2,

    frozenset(["Q","J"]): 5,
    frozenset(["Q","T"]): 4,
    frozenset(["Q","9"]): 3,
    frozenset(["Q","8"]): 2,
    frozenset(["Q","7"]): 2,
    frozenset(["Q","6"]): 2,
    frozenset(["Q","5"]): 1,
    frozenset(["Q","4"]): 1,
    frozenset(["Q","3"]): 1,
    frozenset(["Q","2"]): 1,

    frozenset(["J","T"]): 5,
    frozenset(["J","9"]): 3,
    frozenset(["J","8"]): 2,
    frozenset(["J","7"]): 2,
    frozenset(["J","6"]): 1,
    frozenset(["J","5"]): 1,
    frozenset(["J","4"]): 1,
    frozenset(["J","3"]): 1,
    frozenset(["J","2"]): 1,

    frozenset(["T","9"]): 4,
    frozenset(["T","8"]): 3,
    frozenset(["T","7"]): 1,
    frozenset(["T","6"]): 1,
    frozenset(["T","5"]): 1,
    frozenset(["T","4"]): 1,
    frozenset(["T","3"]): 1,
    frozenset(["T","2"]): 1,

    frozenset(["9","8"]): 3,
    frozenset(["9","7"]): 2,
    frozenset(["9","6"]): 1,
    frozenset(["9","5"]): 1,
    frozenset(["9","4"]): 1,
    frozenset(["9","3"]): 1,
    frozenset(["9","2"]): 1,

    frozenset(["8","7"]): 2,
    frozenset(["8","6"]): 1,
    frozenset(["8","5"]): 1,
    frozenset(["8","4"]): 1,
    frozenset(["8","3"]): 1,
    frozenset(["8","2"]): 1,

    frozenset(["7","6"]): 2,
    frozenset(["7","5"]): 1,
    frozenset(["7","4"]): 1,
    frozenset(["7","3"]): 1,
    frozenset(["7","2"]): 1,

    frozenset(["6","5"]): 2,
    frozenset(["6","4"]): 1,
    frozenset(["6","3"]): 1,
    frozenset(["6","2"]): 1,

    frozenset(["5","4"]): 1,
    frozenset(["5","3"]): 1,
    frozenset(["5","2"]): 1,

    frozenset(["4","3"]): 1,
    frozenset(["4","2"]): 1,

    frozenset(["3","2"]): 1
}

pf_yokosawa_dif = {
    frozenset(["A","A"]): 7,
    frozenset(["A","K"]): 7,
    frozenset(["A","Q"]): 6,
    frozenset(["A","J"]): 5,
    frozenset(["A","T"]): 4,
    frozenset(["A","9"]): 3,
    frozenset(["A","8"]): 2,
    frozenset(["A","7"]): 2,
    frozenset(["A","6"]): 1,
    frozenset(["A","5"]): 1,
    frozenset(["A","4"]): 1,
    frozenset(["A","3"]): 1,
    frozenset(["A","2"]): 1,

    frozenset(["K","K"]): 7,
    frozenset(["K","Q"]): 5,
    frozenset(["K","J"]): 4,
    frozenset(["K","T"]): 3,
    frozenset(["K","9"]): 2,
    frozenset(["K","8"]): 1,
    frozenset(["K","7"]): 1,
    frozenset(["K","6"]): 1,
    frozenset(["K","5"]): 1,
    frozenset(["K","4"]): 1,
    frozenset(["K","3"]): 1,
    frozenset(["K","2"]): 1,

    frozenset(["Q","Q"]): 7,
    frozenset(["Q","J"]): 3,
    frozenset(["Q","T"]): 2,
    frozenset(["Q","9"]): 2,
    frozenset(["Q","8"]): 1,
    frozenset(["Q","7"]): 1,
    frozenset(["Q","6"]): 1,
    frozenset(["Q","5"]): 1,
    frozenset(["Q","4"]): 1,
    frozenset(["Q","3"]): 1,
    frozenset(["Q","2"]): 1,

    frozenset(["J","J"]): 6,
    frozenset(["J","T"]): 3,
    frozenset(["J","9"]): 2,
    frozenset(["J","8"]): 1,
    frozenset(["J","7"]): 1,
    frozenset(["J","6"]): 1,
    frozenset(["J","5"]): 1,
    frozenset(["J","4"]): 1,
    frozenset(["J","3"]): 1,
    frozenset(["J","2"]): 1,

    frozenset(["T","T"]): 6,
    frozenset(["T","9"]): 2,
    frozenset(["T","8"]): 1,
    frozenset(["T","7"]): 1,
    frozenset(["T","6"]): 1,
    frozenset(["T","5"]): 1,
    frozenset(["T","4"]): 1,
    frozenset(["T","3"]): 1,
    frozenset(["T","2"]): 1,

    frozenset(["9","9"]): 6,
    frozenset(["9","8"]): 1,
    frozenset(["9","7"]): 1,
    frozenset(["9","6"]): 1,
    frozenset(["9","5"]): 1,
    frozenset(["9","4"]): 1,
    frozenset(["9","3"]): 1,
    frozenset(["9","2"]): 1,

    frozenset(["8","8"]): 5,
    frozenset(["8","7"]): 1,
    frozenset(["8","6"]): 1,
    frozenset(["8","5"]): 1,
    frozenset(["8","4"]): 1,
    frozenset(["8","3"]): 1,
    frozenset(["8","2"]): 1,

    frozenset(["7","7"]): 5,
    frozenset(["7","6"]): 1,
    frozenset(["7","5"]): 1,
    frozenset(["7","4"]): 1,
    frozenset(["7","3"]): 1,
    frozenset(["7","2"]): 1,

    frozenset(["6","6"]): 4,
    frozenset(["6","5"]): 1,
    frozenset(["6","4"]): 1,
    frozenset(["6","3"]): 1,
    frozenset(["6","2"]): 1,

    frozenset(["5","5"]): 4,
    frozenset(["5","4"]): 1,
    frozenset(["5","3"]): 1,
    frozenset(["5","2"]): 1,

    frozenset(["4","4"]): 3,
    frozenset(["4","3"]): 1,
    frozenset(["4","2"]): 1,

    frozenset(["3","3"]): 3,
    frozenset(["3","2"]): 1,

    frozenset(["2","2"]): 3,
}

def pf_str_sb(hand_card):
    if hand_card[0][1] == hand_card[1][0]:
        return pf_sb_dict_same[frozenset([hand_card[0][0],hand_card[1][0]])]
    else:
        return pf_sb_dict_dif[frozenset([hand_card[0][0],hand_card[1][0]])]

def pf_str_bb(hand_card): 
    if hand_card[0][1] == hand_card[1][1]:
        return pf_yokosawa_same[frozenset([hand_card[0][0],hand_card[1][0]])]
    else:
         return pf_bb_dict_dif[frozenset([hand_card[0][0],hand_card[1][0]])]

def pf_str_yokosawa(hand_card):
    if hand_card[0][1] == hand_card[1][0]:
        return pf_sb_dict_same[frozenset([hand_card[0][0],hand_card[1][0]])]
    else:
        return pf_yokosawa_dif[frozenset([hand_card[0][0],hand_card[1][0]])]

# import random
# deck = [
#     "As", "Ad", "Ac", "Ah",
#     "Ks", "Kd", "Kc", "Kh",
#     "Qs", "Qd", "Qc", "Qh",
#     "Js", "Jd", "Jc", "Jh",
#     "Ts", "Td", "Tc", "Th",
#     "9s", "9d", "9c", "9h",
#     "8s", "8d", "8c", "8h",
#     "7s", "7d", "7c", "7h",
#     "6s", "6d", "6c", "6h",
#     "5s", "5d", "5c", "5h",
#     "4s", "4d", "4c", "4h",
#     "3s", "3d", "3c", "3h",
#     "2s", "2d", "2c", "2h"
# ]
# random.shuffle(deck)

# player_hand = []
# player_hand.append(deck[0])
# player_hand.append(deck[1])
# print(player_hand)
# pf_str_bb(player_hand)