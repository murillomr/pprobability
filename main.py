import random
from collections import Counter
from poker_core.cards import create_deck, parse_card
from poker_core.hand_evaluation import get_best_hand

# --- Constantes ---
HAND_NAMES = ["Carta Alta", "Um Par", "Dois Pares", "Trinca", "Straight", "Flush", "Full House", "Quadra", "Straight Flush"]
NUM_SIMULATIONS = 50000

# --- Lógica de Simulação e Apresentação ---

def run_simulation(my_cards, table_cards, deck, num_cards_to_draw):
    """
    Executa uma simulação de Monte Carlo para calcular as probabilidades de mãos.
    """
    hand_rank_counts = Counter()
    for _ in range(NUM_SIMULATIONS):
        simulation_deck = deck[:]
        random.shuffle(simulation_deck)
        
        # Pega as próximas cartas da simulação (1 para o Turn, 1 para o River)
        drawn_cards = simulation_deck[:num_cards_to_draw]
        
        # Avalia a mão final
        final_cards = my_cards + table_cards + drawn_cards
        best_rank, _ = get_best_hand(final_cards)
        hand_rank_counts[best_rank] += 1
        
    return hand_rank_counts

def print_probabilities(hand_rank_counts, num_simulations):
    """
    Imprime as probabilidades de cada mão a partir dos resultados da simulação.
    """
    # Imprime as probabilidades em ordem, da melhor para a pior
    for rank in range(len(HAND_NAMES) - 1, 0, -1): # de Straight Flush (8) a Um Par (1)
        count = hand_rank_counts[rank]
        if count > 0:
            probability = count / num_simulations
            print(f"- {HAND_NAMES[rank]:<15}: {probability:.2%}")

# --- Lógica de Entrada do Usuário ---

def get_initial_cards(deck):
    """
    Pega as duas cartas do jogador e as três do flop, validando-as.
    """
    while True:
        try:
            hand_str = input("➡️ Digite suas duas cartas (ex: AE KC): ").split()
            if len(hand_str) != 2:
                print("ERRO: Você deve inserir exatamente duas cartas.")
                continue
            
            flop_str = input("➡️ Digite as três cartas da mesa (ex: AE KC QP): ").split()
            if len(flop_str) != 3:
                print("ERRO: Você deve inserir exatamente três cartas para a mesa.")
                continue

            my_cards = [parse_card(c) for c in hand_str]
            table_cards = [parse_card(c) for c in flop_str]

            if None in my_cards or None in table_cards:
                print("ERRO: Formato de carta inválido. Use RankNaipe (ex: 'AE', 'TP', '2O').")
                continue

            all_input_cards = my_cards + table_cards
            if len(set(all_input_cards)) != len(all_input_cards):
                print("ERRO: Você inseriu cartas duplicadas.")
                continue
            
            for card in all_input_cards:
                deck.remove(card)
            
            return my_cards, table_cards

        except ValueError:
            print("ERRO: Carta não encontrada no baralho. Tente novamente.")
            deck = create_deck() # Reinicia o baralho
        except Exception as e:
            print(f"Ocorreu um erro inesperado: {e}")
            return [], []

def get_turn_card(deck):
    """
    Pega a carta do turn, validando-a.
    """
    while True:
        try:
            turn_str = input("➡️ Digite a carta do Turn (ex: 7C): ")
            if len(turn_str.split()) != 1:
                print("ERRO: Você deve inserir exatamente uma carta.")
                continue

            turn_card = parse_card(turn_str)
            if turn_card is None:
                print("ERRO: Formato de carta inválido.")
                continue
            
            deck.remove(turn_card)
            return turn_card

        except ValueError:
            print("ERRO: Carta duplicada ou já está em jogo. Tente novamente.")
        except Exception as e:
            print(f"Ocorreu um erro inesperado: {e}")
            return None

# --- Fluxo Principal ---

def main():
    """
    Função principal que executa a calculadora de probabilidades.
    """
    print("--- Calculadora de Probabilidades de Poker (Texas Hold'em) ---")
    
    deck = create_deck()
    my_cards, table_cards = get_initial_cards(deck)

    if not my_cards:
        return

    # --- ANÁLISE PÓS-FLOP ---
    print("\n--- Análise Pós-Flop ---")
    initial_5_cards = my_cards + table_cards
    current_hand_rank, _ = get_best_hand(initial_5_cards)
    print(f"Mão atual (com o flop): {HAND_NAMES[current_hand_rank]}")

    print("\nCalculando probabilidades para o Turn...")
    # Simula com 6 cartas (2 mão + 3 flop + 1 turn)
    turn_hand_counts = run_simulation(my_cards, table_cards, deck, 1)
    print("Probabilidades de formar cada mão no Turn:")
    print_probabilities(turn_hand_counts, NUM_SIMULATIONS)
    
    # --- ANÁLISE PÓS-TURN ---
    print("\n--- Análise Pós-Turn ---")
    turn_card = get_turn_card(deck)
    if not turn_card:
        return

    table_cards.append(turn_card)
    current_6_cards = my_cards + table_cards
    current_hand_rank, _ = get_best_hand(current_6_cards)
    print(f"Mão atual (com o turn): {HAND_NAMES[current_hand_rank]}")
    
    print("\nCalculando probabilidades para o River...")
    # Simula com 7 cartas (2 mão + 4 mesa + 1 river)
    river_hand_counts = run_simulation(my_cards, table_cards, deck, 1)
    print("Probabilidades de formar cada mão no River:")
    print_probabilities(river_hand_counts, NUM_SIMULATIONS)

    print("\nNota: Este cálculo é para a mão atual.")


if __name__ == "__main__":
    main()
