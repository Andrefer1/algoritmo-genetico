import random
import math

def getDist(p1, p2): # Distância entre 2 pontos
    #Verifica se p1 ou p2 não são do tipo list()

    #Retorna a distância entre as cidades (raiz da soma das potências dos eixos X e Y)
    return (math.sqrt( math.pow(int(p1[0]) - int(p2[0]), 2) + math.pow(int(p1[1]) - int(p2[1]), 2))) #Teorema de Pitágoras

def fitness(lista): # Função Objetivo
    #O Parâmetro 'lista' recebe o cromossomo, onde cada cidade é um número
    soma = 0

    print('Cromossomo -> ', lista)
    
    i = 0
    while i != len(lista)-2:
        # print('fitness - 1 --------', lista) #lista = [0, 1, 3, 2]

        soma += (int(getDist(cidades[lista[i]], cidades[lista[i+1]]))) 
        # print('fitness - 2 --------', cidades[lista[a]], cidades[lista[a+1]]) #cidades[lista[a]] -> cidades[lista[0]], onde a = 0 -> cidades[0]
                                                                    #cidades[lista[a+1]] -> cidades[lista[1]], onde a = 1 -> cidades[1] 
        i += 1
    return soma

def gera_pares(lista, quant): #! Essa função gera uma lista de populações, não entendi o porquê
    # print('1 - ', lista)
    # print('2 - ', quant)
    pares = []
    sorteados = []

    done = False

    for a in range(0, quant):
        dois_a_dois = []
        
        while True:
            par_1 = random.randint(0, len(lista) - 1)           

            if par_1 not in sorteados:
                while True:
                    par_2 = random.randint(0, len(lista) - 1)                    
                    if par_2 not in sorteados and par_1 != par_2:
                        dois_a_dois.append(lista[par_1])
                        dois_a_dois.append(lista[par_2])
                        sorteados.append(par_1)
                        sorteados.append(par_2)
                        done = True
                        break
            if done == True:
                done = False
                pares.append(dois_a_dois)
                break
    # print('PARES', pares)
    return pares
                
def roletar(roleta, quantidade):   

    # roleta => Lista de distâncias invertidas, que representam partes decimais (EX: 0.2, 0.35, 0.70, 0.95, 0.99, 1.00)
    # quantidade => quantidade de indivíduos.
    # print(roleta)
    
    if not isinstance(roleta, list):
        print('Insira uma lista como parâmetro.')
        return    

    populacao = []

    incremented_roleta = roleta[0] # Cada indice da roleta representa uma porcentagem (decimal), que juntas fecham 1 (100%).
    spin = []
    
    for a in range(0, len(roleta)):        
        spin.append(incremented_roleta)
        incremented_roleta += roleta[a]  
        # print('ROLETA', roleta[a])      
    # print('SPIN', spin)
    # print('SPIN', len(spin))

    for a in range(0, quantidade):
        generated = random.random() #Retorna 0.0 - 1.0   
        gera_populacao = 0                         
        
        for a in range(0, len(spin)):
            # print('SPIN', spin[a])
            # print('GENERATED', generated)
            if generated < spin[a]:
                break
            else:
                gera_populacao += 1                
                      
        populacao.append(gera_populacao)

    # print('populacao', populacao)
    #print('roletado: ', populacao, '\n')
    return populacao

def crossover(pares, populacao_inicial): # Function de Crossover

    cut_points = []
    
    for a in range(0, int(populacao_inicial/2)):
        cut_point = random.randint( int(len(cidades) / 2), len(cidades) - 1)  # corta do Ponto até o Fim        
        cut_points.append(int(cut_point))        

    cut_pares = [] # Do Ponto de corte ao fim
    left_pares = [] # Do Ponto de corte ao inicio
    original_pares = []
    
    cp = []
    lp = []
    op = []
    index = 0

    #print(populacao)
    #input()
    
    for a in range(0, len(pares)):
        for b in range(0, len(pares[a])):
            avoid_error = False
            
            for c in range(0, len(cidades)):      

                index = pares[a][b] # Pega o Indice do Par na População gerada.         

                cidade = populacao[b][c] # Pega a Cidade correspondente àquela população
                op.append(cidade)
                
                if c <= cut_points[a]:
                    cp.append(cidade)
                else:
                    lp.append(cidade)

                
                
            cut_pares.append(cp)
            left_pares.append(lp)
            original_pares.append(op)
            cp = []
            lp = []
            op = []            
            
    print('\nPontos de Corte: ', cut_points, '(INDEXS)')

    a = 0
    
    while a < len(cut_pares):
        for b in range(0, 1):
                for c in range(0, len(original_pares[a+1])):
                    if original_pares[a+1][c] not in cut_pares[a]:
                        cut_pares[a].append(original_pares[a+1][c])
                for c in range(0, len(original_pares[a])):
                    if original_pares[a][c] not in cut_pares[a+1]:
                        cut_pares[a+1].append(original_pares[a][c])                                
        a += 2
    return cut_pares          

def mutacao(pares): # Function para Mutação
    mutacao = 0.1
    rand = 0    
    
    for a in range(0, len(pares)-1): # cada um dos pares
        for b in range(0, len(pares[a])): # cada uma das cidades do pares
            rand = random.random()
            if rand <= mutacao:
                print('Houve mutação no Par ', a)
                pos_1 = random.randint(0, len(cidades)-1)
                while True:
                    pos_2 = random.randint(0, len(cidades)-1)
                    if pos_1 != pos_2:
                        #print(len(pares[a]))
                        #print(pos_1, ', ', pos_2)
                        aux = pares[a][pos_1]
                        pares[a][pos_1] = pares[a][pos_2]
                        pares[a][pos_2] = aux                        
                        break                              

    return pares

def gera_cidades(): # Funcão para gerar indivíduos
    selected_cities = []
    selected_cities.append(0) # Cidade de partida
    contador = 1
    
    while contador < len(cidades):
        chosen_city = random.randint(1, len(cidades)-1) # Escolhe uma cidade da lista 'cidades' #!Alterar para letras, invés de números
    
        if not chosen_city in selected_cities: # Se a cidade sorteada não estiver na lista de selecionadas, adicione-a.
            selected_cities.append(chosen_city) # Adicionando à lista de cidades selecionadas a cidade sorteada.
            contador += 1

    # print('tamanho cidade', len(cidades))
    # print('contador', contador)
    # print('SELECTED_CITIES', selected_cities)
    return selected_cities
# ------------------------------------------------------------------- #

# x) Os N individuos são gerados e adicionados à lista populacao.
# x) O procedimento COMPLETO é repetido X vezes, conforme o número informado pelo usuário.
# -----------------------------------------------------------------------------------------

# 1) Calcula-se o Fitness (soma de todas as distâncias das cidades que compõe um indivíduo), EX: Distância de A -> B / B -> C / C -> D.....
# 2) Calcula-se o percentual de cada indivíduo para a mutação.
# 3) Gira-se a roleta para sortear os INDIVIDUOS
# 4) Faz-se o CROSSOVER a partir dos individuos anteriormente selecionados para gerar os pares através de pontos de corte.
# 5) Faz-se a mutacao 

cidades = []
menores_distancias = []
gera_populacao = []
populacao = []
distancias = []
roleta = []
distancias_invertidas = []

populacao_inicial = 5 #int(input('\nDigite o número inicial da populaçao: '))
vezes = 2 #int(input('Digite o número de vezes a executar o procedimento: '))
cdd = 4 #int(input('Digite o número de cidades: ')) #int(random.randrange(4, 5)) #Determina a quantidade de cidades

for i in range(0, cdd): #Adiciona as coordenadas das cidades
    cidades.append( [ random.randint(0, 100), random.randint(0, 100) ] )

print('\nLocalização das cidades -> ', cidades, '\n')

for i in range(0, populacao_inicial): # Gera os N indivíduos iniciais
    gera_populacao = gera_cidades()
    populacao.append(gera_populacao) # Adiciona a lista de cidades sorteadas à lista de populações.

for i in range(0, vezes):
    if i == 0: # O Fitness é realizado em cada indivíduo.
        for j in range(0, len(populacao)):
            fitness_result = fitness(populacao[j]) # Soma das distâncias de todos os indivíduos.
            distancias.append(fitness_result) # Adiciona a distância entre todas as Cidades desta população à Lista de Distâncias            
            # print('distancias', distancias)
            distancias_invertidas.append(1 / fitness_result) # Distâncias invertidas (porcentagem).
            # print('distancias_invertidas', distancias_invertidas)

    else:
        for j in range(0, len(populacao)):
            fitness_result = fitness(populacao[j])
            distancias.append(fitness_result)
            distancias_invertidas.append(1 / fitness_result)
    
    print('\nDISTANCIAS POS-CROSSOVER  --> ', distancias, '\n')
    menor_distancia = float(min(distancias))
    print('Menor Distancia: ', menor_distancia, 'metros')
    menores_distancias.append(menor_distancia)

    for i in range(0, len(distancias_invertidas)):
        roleta.append( (distancias_invertidas[i] / sum(distancias_invertidas)) ) # Distância invertida DIVIDIDO PELA Soma das distâncias invertidas.

    rolled_populacao = roletar(roleta, populacao_inicial)
    pares = gera_pares(rolled_populacao, int(populacao_inicial/2))
    
    print('--------------------------------------------------------------------------------')
    pares = mutacao(crossover(pares, populacao_inicial))
    for i in range(0, len(pares)):
        print(pares[i])
    gera_populacao = []
    
    populacao = []

    for i in range(0, len(pares)):    
        populacao.append(pares[i])
        
    fitness_result = []
    roleta = []

print(cidades)

print('\n--------------------------------------FIM----------------------------------------')
print('\nPROCEDIMENTO EXECUTADO ', vezes, ' VEZES COM POP INICIAL DE ', populacao_inicial)

print('\nDISTÂNCIAS ENCONTRADAS: ', menores_distancias)
print('MENOR DISTÂNCIA ENCONTRADA: ', min(menores_distancias), ' metros\n')
