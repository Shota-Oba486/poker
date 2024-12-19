import numpy as np

def encode_state(player_chips, bet_amount, hand_cards, table_cards, phase):
    """
    ポーカーの状態をエンコードする
    
    Args:
        player_chips (int): プレイヤーの持ち金
        bet_amount (int): ベット金額
        hand_cards (list): 持ちカード [(rank, suit), ...]
        table_cards (list): テーブルカード [(rank, suit), ...]
        phase (int): 0,1,2,3,4 現在のフェーズ ("preflop", "flop", "turn", "river")
    
    Returns:
        np.array: エンコードされた状態ベクトル
    """
    # 持ち金とベット金額（連続値の正規化/最大100,000チップと仮定)
    normalized_chips = player_chips / 100000
    normalized_bet = bet_amount / 100000

    # 持ちカードとフィールドカードのエンコード (ランクとスートをワンホットでエンコード)
    def encode_cards(cards):
        encoded = np.zeros(52)
        if len(cards) == 0:
            return encoded
        else:
            rank_to_num = {'A': 14, 'K': 13, 'Q': 12, 'J': 11, 'T': 10, '9': 9, '8': 8, '7': 7, '6': 6, '5': 5, '4': 4, '3': 3,'2': 2}
            suit_to_num = {"s":0,"d":1,"c":2,"h":3}

            ranks = np.array([rank_to_num[card[0]] for card in cards])
            suits = np.array([suit_to_num[card[1]] for card in cards])
            indices = (ranks - 2) * 4 + suits
            encoded[indices]

            return encoded

    encoded_hand = encode_cards(hand_cards)
    encoded_table = encode_cards(table_cards)

    # フェーズ情報のワンホットエンコード
    phase_encoded = np.zeros(5)
    phase_encoded[phase] = 1

    # 全ての情報を結合
    state_vector = np.concatenate([
        [normalized_chips, normalized_bet],  # 数値情報
        encoded_hand,  # 手札情報
        encoded_table,  # テーブルカード情報
        phase_encoded  # フェーズ情報
    ])
    
    return state_vector

# # 状態の例
# player_chips = 99900
# bet_amount = 100
# hand_cards = ["2d", "Qs"]
# table_cards = []
# phase = 0

# state = encode_state(player_chips, bet_amount, hand_cards, table_cards, phase)
# print(state)

# print(state.shape)