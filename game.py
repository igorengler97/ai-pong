import pygame
import sys
import random

def ball_animation():
    global ball_speed_x, ball_speed_y, score

    ball.x += ball_speed_x
    ball.y += ball_speed_y

    if ball.top <= 0:
        ball_speed_y *= -1
    if ball.bottom >= screen_height:
        ball_restart()
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

def ball_restart(): 
    global ball_speed_y, ball_speed_x
    ball.center = (screen_width/2, screen_height/2)
    ball_speed_x *= random.choice((1, -1))
    #ball_speed_y *= random.choice((1, -1))

# setup geral
pygame.init()  # inicia todos os módulos pygame, necessário
clock = pygame.time.Clock()

# criando a imagem principal
screen_width = 1280
screen_height = 720
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('pong')

# retangulos do jogo
ball = pygame.Rect(screen_width/2 - 15, screen_height/2 - 15, 30, 30)
player = pygame.Rect(screen_width/2 - 60, screen_height - 60, 120, 10)

# variaveis de velocidade
ball_speed_x = 8 * random.choice((1, -1))
ball_speed_y = 8
player_speed = 0

# cores
bg_color = pygame.Color('grey12')
light_grey = (200, 200, 200)
white = (255,255,255)

# variavel de pontuação
score = 0

while True:
    # lidando com input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_speed -= 12
            if event.key == pygame.K_RIGHT:
                player_speed += 12
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                player_speed += 12
            if event.key == pygame.K_RIGHT:
                player_speed -= 12
            

    ball_animation()

    player_animation()
    
    # aparencia dos objetos
    screen.fill(bg_color)
    pygame.draw.rect(screen, light_grey, player)
    pygame.draw.ellipse(screen, light_grey, ball)
    
    # atualizando a tela
    pygame.display.flip()
    clock.tick(60)  # limita o loop a rodar 60 vezes por segundo
