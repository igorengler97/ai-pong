import pygame
import sys
import random
from enum import Enum

cromossomos = 100
geracoes = 100

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
player = pygame.Rect(screen_width/2 - 60, screen_height - 60, 120, 3)

# variaveis de velocidade
ball_speed_x = 6
ball_speed_y = 6
player_speed = 0

# cores
bg_color = pygame.Color('grey12')
light_grey = (200, 200, 200)
white = (255,255,255)

# variavel de pontuação
score = 0


class Direction(Enum):
    LEFT = 0
    RIGH = 2
    STOP = 3

def generate_dna():
    pass

def generate_population():
    pass

def mate():
    pass

def ball_animation():
    global ball_speed_x, ball_speed_y, score

    ball.x += ball_speed_x
    ball.y += ball_speed_y

    if ball.top <= 0:
        ball_speed_y *= -1
    if ball.bottom >= screen_height or ball.bottom >= 680: #evitar bug da bola atravessando o paddle
        game_restart()
        score = 0
        print(score)
    if ball.left <= 0 or ball.right >= screen_width:
        ball_speed_x *= -1

    if ball.colliderect(player):
        ball_speed_y *= -1
        score += 1
        print(score)

def player_animation():
    player.x += player_speed
    # jogador não pode ir além do que está na tela
    if player.left <=0:
        player.left = 0
    if player.right >= screen_width:
        player.right = screen_width

def game_restart(): 
    global ball_speed_y, ball_speed_x
    ball.center = (screen_width/2, screen_height/2)
    #print("speed ", ball_speed_x)
    if ball_speed_x < 0:
        ball_speed_x *= -1
    #ball_speed_y *= 1
    player.center = (screen_width/2, screen_height - 55)
    

#click = 0


while True:
    # lidando com input
    for event in pygame.event.get():
        #pygame.time.wait(100)
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                #click += 1
                player_speed -= 16
                #pygame.time.wait(500)
            if event.key == pygame.K_RIGHT:
                #click += 1
                player_speed += 16
                #pygame.time.wait(500)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                #click += 1
                #print(click)
                player_speed += 16
            if event.key == pygame.K_RIGHT:
                #click += 1
                #print(click)
                player_speed -= 16
        #print(click)
        

    ball_animation()

    player_animation()
    
    # aparencia dos objetos
    screen.fill(bg_color)
    pygame.draw.rect(screen, light_grey, player)
    pygame.draw.ellipse(screen, light_grey, ball)
    
    # atualizando a tela
    pygame.display.flip()
    clock.tick(60)  # limita o loop a rodar 60 vezes por segundo
