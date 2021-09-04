import pygame
import sys


def ball_animation():
    global ball_speed_x
    global ball_speed_y

    ball.x += ball_speed_x
    ball.y += ball_speed_y

    if ball.top <= 0 or ball.bottom >= screen_height:
        ball_speed_y *= -1
    if ball.left <= 0 or ball.right >= screen_width:
        ball_speed_x *= -1

    if ball.colliderect(player):
        ball_speed_y *= -1

# setup geral
pygame.init()  # inicia todos os módulos pygame, necessário
clock = pygame.time.Clock()

# criando a imagem principal
screen_width = 1280
screen_height = 960
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('pong')

# retangulos do jogo
# no meio da tela, com 30 pixels de altura e de largura
ball = pygame.Rect(screen_width/2 - 15, screen_height/2 - 15, 30, 30)
player = pygame.Rect(screen_width/2 - 60, screen_height - 60, 120, 10)

# variaveis de velocidade
ball_speed_x = 7
ball_speed_y = 7

bg_color = pygame.Color('grey12')
light_grey = (200, 200, 200)

while True:
    # lidando com input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    ball_animation()

    # aparencia dos objetos
    screen.fill(bg_color)
    pygame.draw.rect(screen, light_grey, player)
    pygame.draw.ellipse(screen, light_grey, ball)

    # atualizando a tela
    pygame.display.flip()
    clock.tick(60)  # limita o loop a rodar 60 vezes por segundo
