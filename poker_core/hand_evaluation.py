from collections import Counter
import itertools
from .cards import RANK_MAP

# --- Lógica de Avaliação da Mão ---

def get_hand_details(hand):
    """
    Analisa uma mão de 5 cartas e retorna seu ranking e os valores das cartas.
    """
    if len(hand) != 5:
        return (0, [])

    ranks = sorted([RANK_MAP[r] for r, s in hand], reverse=True)
    suits = {s for r, s in hand}

    is_flush = len(suits) == 1
    # Verifica straight, incluindo o caso A-2-3-4-5
    is_straight = (max(ranks) - min(ranks) == 4 and len(set(ranks)) == 5) or \
                  (ranks == [14, 5, 4, 3, 2])
    
    # Se for um straight A-2-3-4-5, o Ás conta como 1 para o ranking
    if ranks == [14, 5, 4, 3, 2]:
        ranks = [5, 4, 3, 2, 1]

    # Contagem de cartas do mesmo valor (ex: um par, uma trinca)
    rank_counts = Counter(ranks).values()
    
    if is_straight and is_flush:
        return (8, ranks)  # Straight Flush
    if 4 in rank_counts:
        return (7, ranks)  # Four of a Kind
    if sorted(rank_counts) == [2, 3]:
        return (6, ranks)  # Full House
    if is_flush:
        return (5, ranks)  # Flush
    if is_straight:
        return (4, ranks)  # Straight
    if 3 in rank_counts:
        return (3, ranks)  # Three of a Kind
    if list(rank_counts).count(2) == 2:
        return (2, ranks)  # Two Pair
    if 2 in rank_counts:
        return (1, ranks)  # One Pair
    return (0, ranks)      # High Card


def get_best_hand(seven_cards):
    """
    Encontra a melhor mão de 5 cartas a partir de 7 cartas.
    """
    combinations = list(itertools.combinations(seven_cards, 5))
    if not combinations:
        return (0, [])
    return max(
        (get_hand_details(hand) for hand in combinations),
        key=lambda x: (x[0], tuple(x[1]))
    )
