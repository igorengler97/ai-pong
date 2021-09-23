from time import time
import pygame
import sys
import random
from enum import Enum

# variaveis do algoritmo genetico
population = []
number_population = 10
size_dna = 20
choices = [
    "NOP",
    pygame.K_LEFT,
    pygame.K_RIGHT,
]
mutation_rate = 0.005

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

for x in range(number_population):
    player.append(pygame.Rect(screen_width/2 - 60, screen_height - 60, 120, 3))

# variaveis de velocidade
ball_speed_x = 6
ball_speed_y = 6
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
        for x in len(size_dna):
            if random.uniform(0, 1) <= mutation_rate:
                new_gene = dna[x]
                while new_gene == dna[x]:
                    new_gene = random.choice(choices)
                dna[x] = new_gene
    return dna

def mate(father, mother):
    global number_population, mutation_rate
    visited = {}
    new_population = []
    for x in range(number_population):
        position = random.randint(0, len(father))
        if not visited.get(position):
            visited[position] = True
            if random.randint(0, 100) > 50:
                child = father[0:position] + mother[position:]        
                if random.randint(0, 100) <= mutation_rate:
                    print("MUTATED")
                    child = mutation(child)
                new_population.append(child)
            else:
                child = mother[0:position] + father[position:]
                if random.randint(0, 100) < mutation_rate:
                    print("MUTATED")
                    child = mutation(child)
                new_population.append(child)
        else:
            new_population.append(generate_dna())

def roulette_selection():
    # Acho que o metodo da roleta está funcionando
    # Precisa validar
    # p(i) = fi / soma dos fitness
    # p(i) = probabilidade do individuo ser selecionado
    # fi = fitness do individuo
    global score, population, number_population
    max = sum(score)
    pick = random.uniform(0, max)
    current = 0
    for x in range(number_population):
        current += score[x]
        if current > pick:
            return population[x]
    

def ball_animation():
    global ball_speed_x, ball_speed_y, score

    ball.x += ball_speed_x
    ball.y += ball_speed_y

    if ball.top <= 0:
        ball_speed_y *= -1
    if ball.bottom >= screen_height or ball.bottom >= 680: #evitar bug da bola atravessando o paddle
        #game_restart()
        score = 0
        print(score)
    if ball.left <= 0 or ball.right >= screen_width:
        ball_speed_x *= -1

    for x in range(number_population):
        if ball.colliderect(player[x]):
            ball_speed_y *= -1
            score += 1
            print(score)

def player_animation():
    for x in range(number_population):
        player[x].x += player_speed[x]
        # jogador não pode ir além do que está na tela
        if player[x].left <=0:
            player[x].left = 0
        if player[x].right >= screen_width:
            player[x].right = screen_width

def game_restart(): 
    global ball_speed_y, ball_speed_x
    ball.center = (screen_width/2, screen_height/2)
    #print("speed ", ball_speed_x)
    if ball_speed_x < 0:
        ball_speed_x *= -1
    #ball_speed_y *= 1
    player.center = (screen_width/2, screen_height - 55)
    

#click = 0

event = ["NOP"] * number_population

generate_population()

while True:
    for gene in range(size_dna):
        for x in range(number_population):
            event[x] = population[x][gene]

        for x in range(len(event)):
            # NOP - não faz nada
            if event[x] == choices[0]:
                player_speed[x] = 0
            if event[x] == choices[1]:
                player_speed[x] = -16
            if event[x] == choices[2]:
                player_speed[x] = 16

        ball_animation()
        player_animation()
        # aparencia dos objetos
        screen.fill(bg_color)
        for x in range(number_population):
            pygame.draw.rect(screen, player_colors[x], player[x])
        pygame.draw.ellipse(screen, light_grey, ball)
        
        # atualizando a tela
        pygame.display.flip()
        clock.tick(60)  # limita o loop a rodar 60 vezes por segundo