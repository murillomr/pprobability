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
            
            # Pede a carta da mesa
            flop_str = input("➡️ Digite a primeira carta da mesa (ex: QP): ")

            parsed_hand = [parse_card(c) for c in hand_str]
            parsed_flop = [parse_card(flop_str)]

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

    num_simulations = 50000  # Aumentar para mais precisão
    good_hand_count = 0  # "Bom jogo" = Um Par ou melhor

    # Avalia a mão atual de 3 cartas
    # Com 3 cartas, não podemos formar uma mão completa de 5, então apenas checamos pares ou trincas.
    initial_3_cards = my_cards + table_cards
    initial_ranks = [RANK_MAP[r] for r, s in initial_3_cards]
    initial_rank_counts = Counter(initial_ranks)

    current_hand_rank = 0  # Carta Alta
    if 3 in initial_rank_counts.values():
        current_hand_rank = 3  # Trinca
    elif 2 in initial_rank_counts.values():
        current_hand_rank = 1  # Um Par


    for _ in range(num_simulations):
        # Embaralha o resto do baralho e completa a mesa
        simulation_deck = deck[:]
        random.shuffle(simulation_deck)
        
        # O flop tem 3 cartas, uma já está na mesa. Faltam 2 para o flop + 1 turn + 1 river
        remaining_table_cards = simulation_deck[:4]
        
        # Avalia a mão final de 7 cartas
        final_7_cards = my_cards + table_cards + remaining_table_cards
        
        # AQUI ESTÁ A CORREÇÃO PRINCIPAL:
        # A simulação deve considerar as 4 cartas restantes para completar as 5 da mesa.
        # No seu código original, estava pegando 4 cartas, mas o baralho já tinha sido modificado.
        # A melhor abordagem é sempre trabalhar com uma cópia para cada simulação.
        
        best_rank, _ = get_best_hand(final_7_cards)

        # Consideramos "bom jogo" se for um par ou melhor (ranking > 0)
        if best_rank > 0:
            good_hand_count += 1

    probability = good_hand_count / num_simulations

    print("\n--- Resultados ---")
    hand_names = ["Carta Alta", "Um Par", "Dois Pares", "Trinca", "Straight", "Flush", "Full House", "Quadra", "Straight Flush"]
    
    current_hand_name = "Carta Alta"
    if current_hand_rank > 0:
        current_hand_name = hand_names[current_hand_rank]

    print(f"Sua mão inicial com a carta da mesa: {current_hand_name}")
    print(f"Probabilidade de terminar com no mínimo 'Um Par': {probability:.2%}")
    print("\nNota: Este cálculo é para a sua mão. A probabilidade contra oponentes é mais complexa e não foi implementada.")


if __name__ == "__main__":
    main()
