from typing import Dict, List, Set, Tuple

def load_automata(filename: str) -> tuple:

    try:
        with open(filename, 'r', encoding='utf-8') as arquivo:
            # Ler o alfabeto
            alphabet = arquivo.readline().strip().split()
            # Validar se o símbolo '&' está presente no alfabeto
            if '&' not in alphabet:
                raise ValueError("O símbolo '&' para a palavra vazia deve estar presente no alfabeto.")

            # Ler os estados
            states = arquivo.readline().strip().split()

            # Ler o estado inicial
            initial_state = arquivo.readline().strip()
            # Validar se o estado inicial é válido
            if initial_state not in states:
                raise ValueError("O estado inicial não está presente na lista de estados.")

            # Ler os estados finais
            final_states = arquivo.readline().strip().split()
            # Validar se os estados finais são válidos
            for final_state in final_states:
                if final_state not in states:
                    raise ValueError(f"O estado final '{final_state}' não está presente na lista de estados.")

            # Inicializar a função de transição como um dicionário
            transitions = {}

            # Ler as transições
            for linha in arquivo:
                partes = linha.strip().split()
                if len(partes) != 3:
                    raise ValueError("Formato de transição inválido. Cada linha deve ter três partes: estado_origem simbolo_transicao estado_destino")
                origin_state, transition_symbol, destination_state = partes
                # Validar se o estado de origem e o estado de destino são válidos
                if origin_state not in states or destination_state not in states:
                    raise ValueError(f"Estado de origem '{origin_state}' ou estado de destino '{destination_state}' inválido.")
                # Validar se o símbolo de transição é válido
                if transition_symbol not in alphabet and transition_symbol != '&':
                    raise ValueError(f"Símbolo de transição '{transition_symbol}' inválido.")

                key = (origin_state, transition_symbol)
                if key not in transitions:
                    transitions[key] = []
                transitions[key].append(destination_state)

        return states, alphabet, transitions, initial_state, final_states

    except FileNotFoundError:
        raise FileNotFoundError(f"O arquivo '{filename}' não foi encontrado.")
    except ValueError as e:
        raise ValueError(f"Erro na leitura do arquivo: {e}")

def process(automata, word: list[str]) -> Dict[str, str]:

    states, alphabet, transitions, initial_state, final_states = automata

    results = {}
    for word_to_check in word:
        # Verificar se a palavra contém símbolos inválidos
        for symbol in word_to_check:
            if symbol not in alphabet:
                results[word_to_check] = "INVALIDA"
                break
        else:
            # Se a palavra for válida, simular o autômato
            current_state = initial_state
            # Caso a palavra seja vazia, verifica o estado inicial
            if word_to_check == '&':
                if current_state in final_states:
                    results[word_to_check] = "ACEITA"
                else:
                    results[word_to_check] = "REJEITA"
            else:
                for symbol in word_to_check:
                    if (current_state, symbol) in transitions:
                        current_state = transitions[(current_state, symbol)][0]  # Assumindo que delta é uma função determinista
                    else:
                        results[word_to_check] = "REJEITA"
                        break
                else:
                    # Se o autômato chegou a um estado final, a palavra é aceita
                    if current_state in final_states:
                        results[word_to_check] = "ACEITA"
                    else:
                        results[word_to_check] = "REJEITA"

    return results

def convert_to_dfa(automata) -> tuple:

    states, alphabet, transitions, initial_state, final_states = automata

    # Inicializar o conjunto de estados do DFA
    dfa_states = set()
    dfa_states.add((initial_state,))

    # Inicializar a função de transição do DFA
    dfa_transitions = {}

    # Criar uma fila para armazenar os estados a serem processados
    queue = [(initial_state,)]

    # Processar cada estado na fila
    while queue:
        current_state, *rest = queue.pop(0)
        # Adicionar o estado atual ao conjunto de estados do DFA
        dfa_states.add(current_state)
        # Para cada símbolo no alfabeto
        for symbol in alphabet:
            # Calcular o estado de destino para o símbolo atual
            next_state = set()
            for state in current_state:
                if (state, symbol) in transitions:
                    next_state.update(transitions[(state, symbol)])
            # Adicionar a transição ao DFA
            if next_state:
                # Adicionar o estado de destino à fila se ele não estiver na fila
                if next_state not in dfa_states:
                    queue.append(tuple(next_state))
                dfa_transitions[(tuple(current_state), symbol)] = tuple(next_state)
            else:
                # Adicionar uma transição para um estado vazio se não houver transição para o símbolo atual
                dfa_transitions[(tuple(current_state), symbol)] = tuple()

    # Converter o conjunto de estados finais do DFA
    dfa_final_states = set()
    for state in dfa_states:
        if any(s in final_states for s in state):
            dfa_final_states.add(state)

    # Retornar o DFA
    return tuple(dfa_states), alphabet, dfa_transitions, (initial_state,), tuple(dfa_final_states)

# Exemplo de uso
if __name__ == "__main__":
    try:
        automata = load_automata("automato.txt")
        dfa_automata = convert_to_dfa(automata)
        words_to_check = ["&", "aba", "ab", "abb", "aa", "c"]
        results = process(dfa_automata, words_to_check)
        for word, result in results.items():
            print(f"Palavra: {word}, Resultado: {result}")
    except Exception as e:
        print(f"Erro: {e}")
