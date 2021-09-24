from time import time
import pygame
import sys
import random
from enum import Enum
from operator import itemgetter
from time import sleep



# variaveis do algoritmo genetico
population = []
number_population = 100
size_dna = 800
choices = [
    "NOP",
    pygame.K_LEFT,
    pygame.K_RIGHT,
]
mutation_rate = 0.1

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

# pos 0 = player; pos 1 = vivo/morto
for x in range(number_population):
    player.append([pygame.Rect(screen_width/2 - 60, screen_height - 60, 120, 2), True])

# variaveis de velocidade
ball_speed_x = 2
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
    global size_dna, choices

    dna = []
    for x in range(size_dna):
        dna.append(random.choice(choices))
    
    return dna

def generate_population():
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
            if random.uniform(0, 1) <= 0.1:
                new_gene = dna[x]
                while new_gene == dna[x]:
                    new_gene = random.choice(choices)
                dna[x] = new_gene
    return dna

def crossover():
    global number_population, mutation_rate
    visited = {}
    new_population = []
    for x in range(number_population):
        father, mother = roulette_selection()   
        position = random.randint(0, number_population)
        chance_of_sex = random.uniform(0, 1)
        if not visited.get(position) and chance_of_sex < 0.5:
            visited[position] = True
            if random.randint(0, 100) > 50:
                child = father[0:position] + mother[position:]        
                if random.randint(0, 100) <= mutation_rate:
                    child = mutation(child)
                new_population.append(child)
            else:
                child = mother[0:position] + father[position:]
                if random.randint(0, 100) < mutation_rate:
                    child = mutation(child)
                new_population.append(child)
        else:
            new_population.append(generate_dna())
    return new_population

def roulette_selection():
    # Acho que o metodo da roleta está funcionando
    # Precisa validar
    # p(i) = fi / soma dos fitness
    # p(i) = probabilidade do individuo ser selecionado
    # fi = fitness do individuo
    global score, population, number_population
    
    maxfit = sum(score, 0)
    if maxfit == 0:
        maxfit = 1
    
    probabilities = []
    father, mother = [], []
    ignored_index = -1
    for x in range(number_population):
        probabilities.append([score[x]/maxfit, x])
    
    probabilities = sorted(probabilities, key=itemgetter(0), reverse=True)
    pick = random.uniform(0, 1)
    
    for x in range(number_population - 1):
        if pick >= 1 - probabilities[x][0]:
            mother = population[probabilities[x][1]]
            break
    
    if mother == []:
        #aux = random.randint(0, number_population -1)
        mother = population[probabilities[0][1]]

    probabilities.remove(probabilities[x])
    pick = random.uniform(0, 1)

    for x in range(number_population - 1):
        if pick >= 1 - probabilities[x][0]:
            father = population[probabilities[x][1]]
            break
    
    if father == []:
        #aux = random.randint(0, number_population -1)
        father = population[probabilities[0][1]]
    
    return [father, mother]
    
    # https://www.cin.ufpe.br/~rso/ag-tbl.pdf slide 20
    # https://github.com/FredericoBender/Algoritmo-Genetico-Problema-da-Mochila/blob/823e50d523e25f5175a581a533dfde0429d609f3/genetic2020.py#L11
    # tentei copiar o rolê mas quebra a aplicação

    # http://www2.peq.coppe.ufrj.br/Pessoal/Professores/Arge/COQ897/Naturais/aulas_piloto/aula4.pdf

    population[int(random.uniform(0, 1))]

def ball_animation():
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
            is_colliding = True
            break
    if is_colliding:
        ball_speed_y *= -1
        i = 0
        number_player = len(player) 
        while i < number_player:
            if ball.colliderect(player[i][0]) and player[i][1]:
                score[i] += 1
            else:
                player[i][1] = False
            i += 1
    return False

def player_animation():
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
    global ball_speed_x, ball_speed_y, number_population, player, population, score, player_speed
    ball.center = (screen_width/2, screen_height/2)
    if ball_speed_x < 0:
        ball_speed_y *= -1
    print('Best fitness of gen', gen, ' is: ', max(score))
    print('Sum of all fitness of gen ', gen, ' is: ', sum(score))

    population = crossover()
    player = []
    score = [0] * number_population
    player_speed = [0] * number_population
    for x in range(number_population):
        player.append([pygame.Rect(screen_width/2 - 60, screen_height - 60, 120, 2), True])
    
    for x in range(number_population):
        player[x][0].center = (screen_width/2, screen_height - 55)
    pygame.display.flip()

event = ["NOP"] * number_population

generate_population()

gen = 1

while True:
    for a in pygame.event.get():
        if a.type == pygame.KEYDOWN:
            if a.key == pygame.K_ESCAPE:
                print("saindo")
                sys.exit()
                
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
            break
        player_animation()
        # aparencia dos objetos
        screen.fill(bg_color)

        textsurface = myfont.render('Generation: '+ str(gen), True, white)
        screen.blit(textsurface,(50,50))

        textsurface2 = myfont.render('Score: '+ str(max(score)), True, white)
        screen.blit(textsurface2,(400,50))

        textsurface3 = myfont.render('Fitness sum: '+ str(sum(score)), True, white)
        screen.blit(textsurface3,(520,50))

        #textsurface4 = myfont.render('Alive: '+ str(len(player)), True, white)
        #screen.blit(textsurface4,(220,50))

        for x in range(len(player)):
            if player[x][1]:
                pygame.draw.rect(screen, player_colors[x], player[x][0])
        pygame.draw.ellipse(screen, light_grey, ball)
        
        # atualizando a tela
        pygame.display.flip()
        clock.tick(360)  # limita o loop a rodar 60 vezes por segundo

    if game_over:
        boruto_next_generations(gen)
        gen +=1
    naoapagaressamerda = pygame.event.get()