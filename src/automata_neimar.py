# Função para ler as informações do autômato a partir de um arquivo
def ler_automato(filename):
    # Abre o arquivo especificado em modo de leitura
    with open(filename, 'r') as arquivo:
        # Lê e armazena o estado inicial
        estado_inicial = arquivo.readline().strip()
        # Lê e armazena o alfabeto como uma lista de símbolos
        alfabeto = arquivo.readline().strip().split()
        # Lê e armazena a lista de estados possíveis
        estados = arquivo.readline().strip().split()
        # Lê e armazena a lista de estados finais
        estados_finais = arquivo.readline().strip().split()
        
        # Inicializa um dicionário vazio para armazenar as transições
        transicoes = {}
        # Lê cada linha restante no arquivo
        for linha in arquivo:
            # Divide a linha em partes usando espaços em branco como separador
            partes = linha.strip().split()
            # Extrai informações sobre a transição
            estado_origem = partes[0]
            estado_destino = partes[1]
            simbolo_transicao = partes[2]
            # Cria uma chave única para a transição usando o estado de origem e o símbolo
            chave = (estado_origem, simbolo_transicao)
            # Adiciona o estado de destino à lista de destinos para essa transição
            if chave not in transicoes:
                transicoes[chave] = []
            transicoes[chave].append(estado_destino)
            # Exibe mensagem de depuração sobre a transição lida
            print(f"Lendo transição: {chave} -> {estado_destino}")
    
    # Retorna as informações lidas do autômato
    return estado_inicial, alfabeto, estados, estados_finais, transicoes

# Função para simular o autômato com uma palavra de entrada
def simular_automato(estado_inicial, alfabeto, estados_finais, transicoes, palavra_input):
    estados_atuais = {estado_inicial}
    
    # Imprime informações sobre o início da simulação
    print("\nIniciando simulação do autômato:\n")
    print(f"Estado Inicial: {estado_inicial}")
    print(f"Palavra de Entrada: {palavra_input}\n")
    
    # Itera sobre cada símbolo na palavra de entrada
    for simbolo in palavra_input:
        # Imprime informações sobre o processamento do símbolo
        print("Processando símbolo:")
        print(f"Estado atual: {estados_atuais}")
        print(f"Símbolo no estado: {get_simbolo_estado(estados_atuais, transicoes)}")
        print(f"Símbolo inserido: {simbolo}\n")
        
        # Inicializa um conjunto para armazenar os novos estados após a transição
        novos_estados = set()
        # Para cada estado atual, verifica se há uma transição com o símbolo ou a palavra vazia
        for estado_atual in estados_atuais:
            chave_simbolo = (estado_atual, simbolo)
            chave_vazio = (estado_atual, '&')
            # Se houver uma transição para o símbolo ou palavra vazia, adiciona estados de destino
            if chave_simbolo in transicoes:
                novos_estados.update(transicoes[chave_simbolo])
            if chave_vazio in transicoes:
                novos_estados.update(transicoes[chave_vazio])
        
        # Verifica se houve transição possível para o símbolo atual
        if not novos_estados:
            return f"Rejeita - Transição não definida para o estado atual '{estado_atual}' e símbolo '{simbolo}'"
        
        # Atualiza os estados atuais com os novos estados obtidos após a transição
        estados_atuais = novos_estados
        # Exibe os estados atuais após processar o símbolo atual
        print(f"Estados atuais após processar símbolo '{simbolo}': {estados_atuais}\n")
    
    # Verifica se pelo menos um dos estados atuais é um estado final
    if any(estado in estados_finais for estado in estados_atuais):
        return "Aceita"  # A palavra foi aceita pelo autômato
    else:
        return "Rejeita - Estado final não alcançado"  # A palavra foi rejeitada pelo autômato

# Função auxiliar para obter o símbolo correspondente ao estado atual
def get_simbolo_estado(estados_atuais, transicoes):
    for estado in estados_atuais:
        for chave in transicoes.keys():
            if chave[0] == estado:
                return chave[1]
    return None  # Caso o símbolo não seja encontrado, retorna None

# Função principal
def main():
    filename = "automato.txt"
    estado_inicial, alfabeto, _, estados_finais, transicoes = ler_automato(filename)
    
    # Solicita ao usuário que insira a palavra de entrada
    palavra_input = input("Digite uma palavra para testar: ")
    resultado = simular_automato(estado_inicial, alfabeto, estados_finais, transicoes, palavra_input)
    print(resultado)

if __name__ == "__main__":
    main()
