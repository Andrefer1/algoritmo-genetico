import random
import math

cidades = []
menores_distancias = []

cdd = int(random.randrange(4, 5)) #Determina a quantidade de cidades
print(cdd, "Cidades")

for a in range(0, cdd): #Adiciona as coordenadas das cidades
    cidades.append( [ random.randint(0, 10), random.randint(0,10) ] )

print(cidades)

def getDist(p1, p2): # Distância entre 2 pontos
    #Verifica se p1 ou p2 não são do tipo list()
    if not isinstance(p1, list) or not isinstance(p2, list):
        print("Insira uma lista com dois pontos (X, Y).")
        return

    #Retorna a distância entre as cidades (raiz da soma das potências dos eixos X e Y)
    return (math.sqrt( math.pow(int(p1[0]) - int(p2[0]), 2) + math.pow(int(p1[1]) - int(p2[1]), 2))) #Teorema de Pitágoras

def fitness(lista): # Função Objetivo
    #O Parâmetro "lista" recebe o cromossomo, onde cada cidade é um número
    soma = 0
    
    #Verifica se o parâmetro "lista" não é do tipo list()
    if not isinstance(lista, list):
        print("Insira uma lista como parâmetro.")
        return
    
    for a in range(0, len(lista)-1):
        # print('fitness - 1 --------', lista) #lista = [0, 1, 3, 2]

        soma += (int(getDist(cidades[lista[a]], cidades[lista[a+1]]))) 
        # print('fitness - 2 --------', cidades[lista[a]], cidades[lista[a+1]]) #cidades[lista[a]] -> cidades[lista[0]], onde a = 0 -> cidades[0]
                                                                    #cidades[lista[a+1]] -> cidades[lista[1]], onde a = 1 -> cidades[1] 
        
        if a == len(lista)-2:
            break
    return soma

def generatePares(lista, quant): #! Essa função gera uma lista de populações, não entendi o porque
    print('1 - ', lista)
    print('2 - ', quant)
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
    print('PARES', pares)
    return pares
                
def roletar(roleta, quantidade):   

    # roleta => Lista de distâncias invertidas, que representam partes decimais (EX: 0.2, 0.35, 0.70, 0.95, 0.99, 1.00)
    # quantidade => quantidade de indivíduos.
    # print(roleta)
    
    if not isinstance(roleta, list):
        print("Insira uma lista como parâmetro.")
        return    

    population = []

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
        gpopulation = 0                         
        
        for a in range(0, len(spin)):
            # print('SPIN', spin[a])
            # print('GENERATED', generated)
            if generated < spin[a]:
                break
            else:
                gpopulation += 1                
                      
        population.append(gpopulation)
    print('POPULATION', population)
    #print("roletado: ", population, "\n")
    return population

def crossover(pares, input_number): # Function de Crossover

    cut_points = []
    
    for a in range(0, int(input_number/2)):
        cut_point = random.randint( int(len(cidades) / 2), len(cidades) - 1)  # corta do Ponto até o Fim        
        cut_points.append(int(cut_point))        

    cut_pares = [] # Do Ponto de corte ao fim
    left_pares = [] # Do Ponto de corte ao inicio
    original_pares = []
    
    cp = []
    lp = []
    op = []
    index = 0

    #print(population)
    #input()
    
    for a in range(0, len(pares)):
        for b in range(0, len(pares[a])):
            avoid_error = False
            
            for c in range(0, len(cidades)):      

                index = pares[a][b] # Pega o Indice do Par na População gerada.         

                cidade = population[b][c] # Pega a Cidade correspondente àquela população
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
            
    print("\nPontos de Corte: ", cut_points, "(INDEXS)")

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

def mutation(pares): # Function para Mutação
    mutation = 0.1
    rand = 0    
    
    for a in range(0, len(pares)-1): # cada um dos pares
        for b in range(0, len(pares[a])): # cada uma das cidades do pares
            rand = random.random()
            if rand <= mutation:
                print("Houve mutação no Par ", a)
                pos_1 = random.randint(0, len(cidades)-1)
                while True:
                    pos_2 = random.randint(0, len(cidades)-1)
                    if pos_1 != pos_2:
                        #print(len(pares[a]))
                        #print(pos_1, ", ", pos_2)
                        aux = pares[a][pos_1]
                        pares[a][pos_1] = pares[a][pos_2]
                        pares[a][pos_2] = aux                        
                        break                              

    return pares

def generateCities(): # Funcão para gerar indivíduos
    selected_cities = []
    selected_cities.append(0) # Cidade de partida
    contador = 1
    
    while contador < len(cidades):
        chosen_city = random.randint(1, len(cidades)-1) # Escolhe uma cidade da lista "cidades" #!Alterar para letras, invés de números
    
        if not chosen_city in selected_cities: # Se a cidade sorteada não estiver na lista de selecionadas, adicione-a.
            selected_cities.append(chosen_city) # Adicionando à lista de cidades selecionadas a cidade sorteada.
            contador += 1

    # print('tamanho cidade', len(cidades))
    # print('contador', contador)
    # print('SELECTED_CITIES', selected_cities)
    return selected_cities
# ------------------------------------------------------------------- #

# x) Os N individuos são gerados e adicionados à lista POPULATION.
# x) O procedimento COMPLETO é repetido X vezes, conforme o número informado pelo usuário.
# -----------------------------------------------------------------------------------------

# 1) Calcula-se o Fitness (soma de todas as distâncias das cidades que compõe um indivíduo), EX: Distância de A -> B / B -> C / C -> D.....
# 2) Calcula-se o percentual de cada indivíduo para a mutação.
# 3) Gira-se a roleta para sortear os INDIVIDUOS
# 4) Faz-se o CROSSOVER a partir dos individuos anteriormente selecionados para gerar os pares através de pontos de corte.
# 5) Faz-se a MUTATION 

gpopulation = []
population = []

distances = []
roleta = []
inverted_distances = []

input_number = 5 #int(input("\nDigite o número inicial da populaçao: ")) #! ???????

vezes = 2 #int(input("Digite o número de vezes a executar o procedimento: ")) #! ???????

for a in range(0, input_number): # Gera os N indivíduos iniciais
    gpopulation = generateCities()
    population.append(gpopulation) # Adiciona a lista de cidades sorteadas à lista de populações!

# print('POPULATION', population)

for a in range(0, vezes):
    if a == 0: # O Fitness é realizado em cada indivíduo.
        for a in range(0, len(population)): #TODO Pode apagar!!!!!
            print(population[a])

        for b in range(0, len(population)):
            fitness_result = fitness(population[b]) # Soma das distâncias de todos os indivíduos.
            distances.append(fitness_result) # Adiciona a distância entre todas as Cidades desta população à Lista de Distâncias            
            # print('DISTANCES', distances)
            inverted_distances.append(1 / fitness_result) # Distâncias invertidas (porcentagem).
            # print('INVERTED_DISTANCES', inverted_distances)

    else:
        for b in range(0, len(population)):
            fitness_result = fitness(population[b])
            distances.append(fitness_result)
            inverted_distances.append(1 / fitness_result)
    
    print("DISTANCIAS POS-CROSSOVER  --> ", distances, "\n")
    menor_distancia = float(min(distances))
    print(" -------> Menor Distancia: ", menor_distancia, "m." )
    menores_distancias.append(menor_distancia)

    for a in range(0, len(inverted_distances)):
        roleta.append( (inverted_distances[a] / sum(inverted_distances)) ) # Distância invertida DIVIDIDO PELA Soma das distâncias invertidas.

    rolled_population = roletar(roleta, input_number)
    pares = generatePares(rolled_population, int(input_number/2))
    #print("Pares: ",pares, "\n")    
    
    print("--------------------------------------------------------------------------------")
    pares = mutation(crossover(pares, input_number))
    for a in range(0, len(pares)):
        print(pares[a])
    gpopulation = []
    
    population = []

    for a in range(0, len(pares)):    
        population.append(pares[a])
        

    fitness_result = []
    #distances = []
    roleta = []
print(cidades)
print("\nFIM DO PROCEDIMENTO....")
print("PROCEDIMENTO EXECUTADO ", vezes, " VEZES COM POP INICIAL DE ", input_number)
print("\nMENOR DISTANCIA ENCONTRADA: ", min(menores_distancias), " m.")

file = open('distancias.txt', 'w')
file.close()

file = open('distancias.txt', 'w')

for a in range(0, len(menores_distancias)):
    file.write(str(int(menores_distancias[a]))+"\n")

file.close()