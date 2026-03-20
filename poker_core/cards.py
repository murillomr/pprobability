import itertools

# --- Representação de Cartas e Baralho ---

# Usamos um mapa para converter a entrada do usuário (letras) para os naipes
# C = Copas (♥), O = Ouro (♦), P = Paus (♣), E = Espada (♠)
SUIT_MAP = {'C': '♥', 'O': '♦', 'P': '♣', 'E': '♠'}
SUITS = list(SUIT_MAP.values())

# Ases (A) são tratados como o maior valor (14) para facilitar a comparação.
RANKS = '23456789TJQKA'
RANK_MAP = {rank: i for i, rank in enumerate(RANKS, 2)}


def create_deck():
    """Cria um baralho padrão de 52 cartas."""
    return list(itertools.product(RANKS, SUITS))


def parse_card(card_str):
    """
    Converte uma string como 'AE' para um formato interno ('A', '♠').
    Retorna None se a entrada for inválida.
    """
    card_str = card_str.upper()
    if len(card_str) != 2:
        return None
    rank, suit_char = card_str[0], card_str[1]
    if rank not in RANKS or suit_char not in SUIT_MAP:
        return None
    return (rank, SUIT_MAP[suit_char])
