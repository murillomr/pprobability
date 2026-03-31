# Calculadora de Probabilidades de Poker (Texas Hold'em)

Esta é uma ferramenta interativa de linha de comando projetada para ajudar jogadores a entenderem estatisticamente suas chances de melhorar a mão durante uma partida de Texas Hold'em.

## Como a Aplicação Funciona

O programa utiliza **Simulações de Monte Carlo** para calcular probabilidades. Em vez de resolver fórmulas matemáticas complexas de combinatória, ele simula 50.000 cenários aleatórios para as cartas que ainda serão reveladas, fornecendo uma estimativa precisa das chances reais do jogador.

## Funcionalidades

- **Avaliação de Mão Atual:** Identifica automaticamente a sua melhor combinação atual (ex: Carta Alta, Par, Trinca).
- **Análise Pós-Flop:** Calcula a probabilidade de cada mão possível ser formada ao chegar no Turn e no River após as 3 primeiras cartas comunitárias.
- **Análise Pós-Turn:** Recalcula as probabilidades para a última carta (River) após a revelação da 4ª carta da mesa.
- **Validação de Baralho:** Previne entradas de cartas duplicadas ou formatos inválidos.

## Como Usar

1. **Inicie o script:** Execute `python main.py`.
2. **Informe suas cartas:** Digite suas duas cartas iniciais (ex: `AE KC` para Ás de Espadas e Rei de Copas).
3. **Informe o Flop:** Digite as três cartas da mesa (ex: `2O 7P 9C`).
4. **Analise os Resultados:** O programa exibirá as porcentagens de chance para cada tipo de mão.
5. **Informe o Turn:** Digite a quarta carta da mesa para atualizar os cálculos para o River.

### Formato das Cartas
O formato utilizado é `[Valor][Naipe]`:
- **Valores:** 2 a 9, `T` (10), `J` (Valete), `Q` (Dama), `K` (Rei), `A` (Ás).
- **Naipes:** `E` (Espadas), `C` (Copas), `O` (Ouros), `P` (Paus).

*Exemplo: `AE` = Ás de Espadas, `7O` = 7 de Ouros.*

## Estrutura do Projeto

- `main.py`: Lógica de interface e fluxo da simulação.
- `poker_core/`: Módulo contendo a lógica de criação de baralho, parsing de cartas e avaliação de ranking de mãos.

## Requisitos

- Python 3.x
