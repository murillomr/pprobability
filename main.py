import random
from collections import Counter
from poker_core.cards import create_deck, parse_card, RANK_MAP
from poker_core.hand_evaluation import get_best_hand

# --- Lógica Principal e Simulação ---

def get_user_input(deck):
    """
    Pega a entrada do usuário para suas cartas e a carta da mesa,
    validando e removendo-as do baralho.
    """
    my_cards, table_cards = [], []
    while True:
        try:
            # Pede as cartas do usuário
            hand_str = input("➡️ Digite suas duas cartas (ex: AE KC): ").split()
            if len(hand_str) != 2:
                print("ERRO: Você deve inserir exatamente duas cartas.")
                continue
            
            # Pede as cartas da mesa (flop)
            flop_str = input("➡️ Digite as três cartas da mesa (ex: AE KC QP): ").split()
            if len(flop_str) != 3:
                print("ERRO: Você deve inserir exatamente três cartas para a mesa.")
                continue

            parsed_hand = [parse_card(c) for c in hand_str]
            parsed_flop = [parse_card(c) for c in flop_str]

            if None in parsed_hand or None in parsed_flop:
                print("ERRO: Formato de carta inválido. Use o formato RankNaipe (ex: 'AE', 'TP', '2O').")
                continue

            my_cards = parsed_hand
            table_cards = parsed_flop
            
            # Verifica se as cartas são únicas
            all_input_cards = my_cards + table_cards
            if len(set(all_input_cards)) != len(all_input_cards):
                print("ERRO: Você inseriu cartas duplicadas.")
                continue
            
            # Remove as cartas do baralho
            for card in all_input_cards:
                deck.remove(card)
            
            return my_cards, table_cards

        except ValueError:
            print("ERRO: Carta não encontrada no baralho (pode já ter sido inserida). Tente novamente.")
            # Reinicia o baralho para a próxima tentativa
            deck = create_deck()
        except Exception as e:
            print(f"Ocorreu um erro inesperado: {e}")
            return [], []


def main():
    """
    Função principal que executa a calculadora de probabilidades.
    """
    print("--- Calculadora de Probabilidades de Poker (Texas Hold'em) ---")
    
    deck = create_deck()
    my_cards, table_cards = get_user_input(deck)

    if not my_cards:
        return

    print("\nCalculando probabilidades...")

    num_simulations = 50000
    hand_rank_counts = Counter()

    # Avalia a mão atual de 5 cartas (2 suas + 3 da mesa)
    initial_5_cards = my_cards + table_cards
    current_hand_rank, _ = get_best_hand(initial_5_cards)

    for _ in range(num_simulations):
        simulation_deck = deck[:]
        random.shuffle(simulation_deck)
        
        # Pega as próximas 2 cartas (Turn e River)
        remaining_table_cards = simulation_deck[:2]
        
        # Avalia a mão final de 7 cartas
        final_7_cards = my_cards + table_cards + remaining_table_cards
        best_rank, _ = get_best_hand(final_7_cards)
        hand_rank_counts[best_rank] += 1

    print("\n--- Resultados ---")
    hand_names = ["Carta Alta", "Um Par", "Dois Pares", "Trinca", "Straight", "Flush", "Full House", "Quadra", "Straight Flush"]
    
    print(f"Sua mão atual (com o flop): {hand_names[current_hand_rank]}")
    print("\nProbabilidades de formar cada mão no final:")

    # Imprime as probabilidades em ordem, da melhor para a pior
    for rank in range(len(hand_names) - 1, 0, -1): # Começa de Straight Flush (8) até Um Par (1)
        count = hand_rank_counts[rank]
        if count > 0:
            probability = count / num_simulations
            print(f"- {hand_names[rank]:<15}: {probability:.2%}")

    print("\nNota: Este cálculo é para a sua mão. A probabilidade contra oponentes é mais complexa e não foi implementada.")


if __name__ == "__main__":
    main()
