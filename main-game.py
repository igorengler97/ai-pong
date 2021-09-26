import time
import pygame
import sys
import random
from operator import itemgetter
from time import sleep

import matplotlib
matplotlib.use("Agg")

import matplotlib.backends.backend_agg as agg
import matplotlib.pylab as plt


# variaveis do algoritmo genetico
population = []
number_population = 400
size_dna = 300
choices = [
    "NOP",
    pygame.K_LEFT,
    pygame.K_RIGHT,
]
mutation_rate = 0.03
the_best_of_bests = [[], 0]

# setup geral
pygame.init()  # inicia todos os módulos pygame, necessário
clock = pygame.time.Clock()

# criando a imagem principal
screen_width = 720
screen_height = 720
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('pong')

# retangulos do jogo
ball = pygame.Rect(screen_width/2 - 15, screen_height/2 - 15, 30, 30)
player = []
time_alive = []

# pos 0 = player; pos 1 = vivo/morto; pos 2 = hora nascimento
t = time.time()
for x in range(number_population):
    player.append([pygame.Rect(screen_width/2 - 60, screen_height - 60, 120, 2), True])
    time_alive.append(t)
# variaveis de velocidade
ball_speed_x = 1
ball_speed_y = 2
player_speed = [0] * number_population

# cores
bg_color = pygame.Color('grey12')
player_colors = [
    (random.randint(30, 255), random.randint(30, 255), random.randint(30, 255) ) 
    for x in range(number_population)
    ]
light_grey = (200, 200, 200)
white = (255,255,255)

# variavel de pontuação
score = [0] * number_population

myfont = pygame.font.SysFont('Arial', 25)

def generate_dna():
    # função que gera o chormossomo de um individuo aleatóriamente
    global size_dna, choices

    dna = []
    for x in range(size_dna):
        dna.append(random.choice(choices))
    
    return dna

def generate_population():
    # função que gera a população
    global population, number_population

    for x in range(number_population):
        dna = generate_dna()
        population.append(dna)

def mutation(dna, method='bit_mutation'):
    global size_dna, population, choices, mutation_rate
    # função que muta um individuo da população
    # recebe o indice do individuo
    if method == 'bit_mutation':
        for x in range(size_dna):
            if random.uniform(0, 1) <= (1/size_dna):
                new_gene = dna[x]
                while new_gene == dna[x]:
                    new_gene = random.choice(choices)
                dna[x] = new_gene
    return dna

visited = {}

def crossover():
    global number_population, mutation_rate, visited
    visited = {}
    new_population = []
    for x in range(number_population):
        # pai, mãe, index pai, index mãe
        father, mother, fi, mi = roulette_selection()

        # 5 % dos melhor individuo vai direto pra proxima geração
        if x >= 0 and x <= int(number_population * 0.01):
            # escolhe o pai ou a mãe pra ir pra proxima geração
            if random.uniform(0, 1) >= 0.5:
                new_population.append(father)
                visited[fi] = True
            else:
                new_population.append(mother)
                visited[mi] = True
            continue

        position = random.randint(0, size_dna - 1)
        # chance de copularem
        chance_of_sex = random.uniform(0, 1)
        # chance da informação genetica do pai vir primeiro
        if (not visited.get(fi) or not visited.get(mi)) and chance_of_sex < 0.95:
            visited[fi] = True
            visited[mi] = True
            if random.randint(0, 100) > 50:
                child = father[0:position] + mother[position:]        
                if random.randint(0, 100) <= mutation_rate:
                    child = mutation(child)
                new_population.append(child)
            # chance da informação genetica da mãe vir primeiro
            else:
                child = mother[0:position] + father[position:]
                if random.randint(0, 100) < mutation_rate:
                    child = mutation(child)
                new_population.append(child)
        else:
            # se não copularem então só gera um individuo novo
            new_population.append(generate_dna())
    return new_population

def roulette_selection():
    # Acho que o metodo da roleta está funcionando
    # Precisa validar
    # p(i) = fi / soma dos fitness
    # p(i) = probabilidade do individuo ser selecionado
    # fi = fitness do individuo
    global score, population, number_population, visited, player
    
    totalfitness = 0
    # calcula o fitness total
    for i in range(number_population):
        totalfitness += pow(time_alive[i], score[i])

    if totalfitness == 0:
        totalfitness = 1
    
    probabilities = []
    father, mother = [], []
    # fi = index do pai, mi = index da mãe
    fi, mi = -1, -1
    # calcula a probabilidade de escolher um individuo
    for x in range(number_population):
        probabilities.append([pow(time_alive[x], score[x])/totalfitness, x])
    
    #ordena do melhor para o pior
    probabilities = sorted(probabilities, key=itemgetter(0), reverse=True)
    pick = random.uniform(0, 1)
    
    # sorteia e marca como visitado a mãe
    for x in range(number_population - 1):
        if pick >= 1 - probabilities[x][0] and (not visited.get(probabilities[x][1])):
            mi = probabilities[x][1]
            mother = population[mi]
            visited[mi] = True
            break
    
    if mother == []:
        aux = random.randint(0, number_population -1)
        mother = population[aux]
        visited[aux] = True

    pick = random.uniform(0, 1)

    # sorteia e marca como visitado o pai
    for x in range(number_population - 1):
        if pick >= 1 - probabilities[x][0] and (not visited.get(probabilities[x][1])):
            fi = probabilities[x][1]
            father = population[fi]
            visited[fi] = True
            break
    
    if father == []:
        aux = random.randint(0, number_population -1)
        father = population[aux]
        visited[aux] = True
    
    return [father, mother, fi, mi]
    
    # https://www.cin.ufpe.br/~rso/ag-tbl.pdf slide 20
    # https://github.com/FredericoBender/Algoritmo-Genetico-Problema-da-Mochila/blob/823e50d523e25f5175a581a533dfde0429d609f3/genetic2020.py#L11
    # tentei copiar o rolê mas quebra a aplicação

    # http://www2.peq.coppe.ufrj.br/Pessoal/Professores/Arge/COQ897/Naturais/aulas_piloto/aula4.pdf

def fitness(index):
    global time_alive
    ini = time_alive[index]
    end = time.time()
    time_alive[index] = (end - ini)


def ball_animation():
    # faz a animação da bola e vê se houve colisão
    # se tiver colisão mata e calcula o fitness das raquetes que não tiveram colisão
    global ball_speed_x, ball_speed_y, score

    ball.x += ball_speed_x
    ball.y += ball_speed_y

    if ball.top <= 0:
        ball_speed_y *= -1
    if ball.bottom >= screen_height or ball.bottom >= 667: #evitar bug da bola atravessando o paddle
        return True
    if ball.left <= 0 or ball.right >= screen_width:
        ball_speed_x *= -1

    is_colliding = False

    for x in range(len(player)):
        if ball.colliderect(player[x][0]) and player[x][1]:
            # se tiver colisão para pq tem que checar toda a população
            is_colliding = True
            break
    if is_colliding:
        # faz a bola ir pra cima
        ball_speed_y *= -1
        i = 0
        number_player = len(player) 
        while i < number_player:
            if ball.colliderect(player[i][0]) and player[i][1]:
                # se teve colisão então aumenta o score da raquete viva
                score[i] += 1
            else:
                # senão mata ela e calcula o fitness
                player[i][1] = False
                fitness(i)
            i += 1
    return False

def player_animation():
    # computa a movimentação na tela
    global player
    for x in range(len(player)):
        # se o jogador estiver vivo computa a animação
        if(player[x][1]):
            player[x][0].x += player_speed[x]
            # jogador não pode ir além do que está na tela
            if player[x][0].left <=0:
                player[x][0].left = 0
            if player[x][0].right >= screen_width:
                player[x][0].right = screen_width

def boruto_next_generations(gen):
    # prepara a proxima geração
    global ball_speed_x, ball_speed_y, number_population, player, population, score, player_speed, the_best_of_bests, time_alive
    ball.center = (screen_width/2, screen_height/2)
    if ball_speed_x < 0:
        ball_speed_y *= -1

    maxFitIndex =  max(range(len(score)), key=score.__getitem__)

    # salva o melhor dos individuos de todo a evolução de todas as gerações do universo das raquetes
    if max(score) > the_best_of_bests[1]:
        the_best_of_bests = [population[maxFitIndex], max(score)*time_alive[maxFitIndex]]

    # cruza
    population = crossover()
    # reseta as variaveis
    player = []
    score = [0] * number_population
    player_speed = [0] * number_population
    time_alive = []
    # calcula a data de nascimento
    t = time.time()
    for x in range(number_population):
        # atribui ao player uma raquete e uma data de nascimento
        player.append([pygame.Rect(screen_width/2 - 60, screen_height - 60, 120, 2), True])
        time_alive.append(t)
    
    for x in range(number_population):
        player[x][0].center = (screen_width/2, screen_height - 55)
    
    # atualiza o display
    pygame.display.flip()

def saveScore(best_fitness, sum_fitness):
    textfile = open("bestFitness.txt", "w")
    for element in best_fitness:
        textfile.write(str(element) + "\n")
    textfile.close()
    textfile2 = open("sumFitness.txt", "w")
    for element in sum_fitness:
        textfile2.write(str(element) + "\n")
    textfile2.close() 

def saving(gen):
    global the_best_of_bests, score, fitness_data
    maxFit = max(score)
    
    textfile = open("chromossome_"+ str(gen) + "_" + str(maxFit) +".txt", "w")
    history_fitness = open("fitness.txt", "w")
    for element in the_best_of_bests:
        textfile.write(str(element) + "\n")
        history_fitness.write(str(fitness_data) + "\n")
    history_fitness.close()
    textfile.close()
    print("Jesus salvou o melhor dos melhores")

best_fitness = []
sum_fitness = []
# 1ª vez executando, prepara o ambiente
generate_population()
gen = 1
best_score = 0
alive = 0
fitness_data = [0]
# variavel usada no while 1
event = ["NOP"] * number_population

fitness_data.append(sum(score))


while True:
                
    for gene in range(size_dna):
        for x in range(len(player)):
            event[x] = population[x][gene]

        for x in range(len(event)):
            # NOP - não faz nada
            if event[x] == choices[0]:
                player_speed[x] = 0
            if event[x] == choices[1]:
                player_speed[x] = -16
            if event[x] == choices[2]:
                player_speed[x] = 16

        game_over = ball_animation()
        if game_over:
            best_fitness.append(max(score))
            sum_fitness.append(sum(score))
            break
        player_animation()

        for a in pygame.event.get():
            if a.type == pygame.KEYDOWN:
                if a.key == pygame.K_ESCAPE:
                    saveScore(best_fitness, sum_fitness)
                    print("saindo")
                    sys.exit()
                if a.key == pygame.K_s:
                    print('Eu sou jesus e eu tenho o poder de salvar')
                    saving(gen)

        # aparencia dos objetos
        screen.fill(bg_color)

        textsurface = myfont.render('Generation: '+ str(gen), True, white)
        screen.blit(textsurface,(50,50))

        textsurface2 = myfont.render('Score: '+ str(max(score)), True, white)
        screen.blit(textsurface2,(400,50))

        textsurface3 = myfont.render('Total Fitness: '+ str(sum(score)), True, white)
        screen.blit(textsurface3,(520,50))

        textsurface4 = myfont.render('Best score: '+ str(best_score), True, white)
        screen.blit(textsurface4,(400,100))
        
        alive = 0
        for ply in player:
            if ply[1]:
                alive += 1

        textsurface5 = myfont.render('Alive: '+ str(alive), True, white)
        screen.blit(textsurface5,(220,50))

        for x in range(len(player)):
            if player[x][1]:
                pygame.draw.rect(screen, player_colors[x], player[x][0])
        pygame.draw.ellipse(screen, light_grey, ball)
        
        # atualizando a tela
        pygame.display.flip()
        clock.tick(360)  # limita o loop a rodar 60 vezes por segundo

    if game_over:
        if best_score < max(score):
            best_score = max(score)

        fitness_data.append(sum(score))
        boruto_next_generations(gen)
        gen +=1
    naoapagaressamerda = pygame.event.get()