import sys
import random
import pygame
from pygame.examples.music_drop_fade import volume

from words_list import *

pygame.init()


def find_word(secret_word_state, secret_word,  letter_choice):
    nouveau_mot_cache = ""
    for indice, lettre in enumerate(secret_word):
        if lettre == letter_choice:
            nouveau_mot_cache += letter_choice
        else:
            nouveau_mot_cache += secret_word_state[indice]
    return nouveau_mot_cache



life = 8
hearth = pygame.image.load("coeurs.png")
hearth = pygame.transform.scale(hearth, (32, 32))
click = pygame.mixer.Sound("click.mp3")
win = pygame.mixer.Sound("win.mp3")
fail = pygame.mixer.Sound("fail.mp3")


pygame.mixer.music.load("BackGround_effect.mp3")
pygame.mixer.music.play(loops=-1)
pygame.mixer.music.set_volume(0.02)


secret_word = random.choice(mots)
mot_cache = "_" * len(secret_word)
state_word = mot_cache
win_play = 0
loose_play = 0

screen = pygame.display.set_mode((800, 600))
restart_rect = pygame.Rect((screen.get_width() // 2 - 75, 225), (155, 64))
Letter = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
font=pygame.font.SysFont('Helvetica.tff', 64)
font_2=pygame.font.SysFont('Helvetica.tff', 32)
letter_rect = []

end_background = pygame.Surface((800,600), pygame.SRCALPHA)
end_background.fill((0,0,0,200))

n = 0
for y in range(3):
    if y == 2:
        for x in range(8):
            letter_rect.append([pygame.Rect(90 + (64 + 15)*x, 320 + (64 + 15)*y, 64, 64), n, 1, 1])
            n += 1
    else:
        for x in range(9):
            letter_rect.append([pygame.Rect(55 + (64 + 15)*x, 320 + (64 + 15)*y, 64, 64), n, 1, 1])
            n += 1




while True:
    mouse_x, mouse_y = 0, 0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_x, mouse_y = pygame.mouse.get_pos()
            elif event.button == 3:
                print("droite")
    screen.fill((50, 55, 58))

    for j, letter in enumerate(letter_rect):
        if letter[2] == 1:
            if letter[0].collidepoint(mouse_x, mouse_y) and letter[3] != 0:
                click.play()
                print(Letter[letter[1]])
                state_word = find_word(state_word, secret_word, Letter[letter[1]])
                if Letter[letter[1]] not in secret_word:
                    letter_rect[j][2] = 0
                    life -= 1
                else:
                    letter_rect[j][3] = 0
            else:
                if letter[3] == 0:
                    pygame.draw.rect(screen, (0, 255, 0), letter[0], border_radius=15)
                else:
                    pygame.draw.rect(screen, (213, 215, 211), letter[0], border_radius=15)
            screen.blit(font.render(Letter[letter[1]].upper(),1,(49,54,63)), (letter[0].centerx - 16, letter[0].centery - 16))

    for i, l in enumerate(state_word):
        screen.blit(font.render(l.upper(), 1, (209,216,215)), (screen.get_width()//2 - ((64*len(secret_word))//2) + (64*i), 150))

    for i in range(life):
        screen.blit(hearth, (10 + (32+10)*i, 10))

    if secret_word == state_word:
        if win_play == 0:
            win_play = 1
            win_play = 1
            win.play(loops=0)

        screen.blit(end_background, (0, 0))
        screen.blit(font.render(f'Tu as gagné !', 1, (255, 255, 255)), (screen.get_width() // 2 - 145, 30))
        pygame.draw.rect(screen, (255, 255, 255), restart_rect, border_radius=15)
        screen.blit(font_2.render("Recommencer", 1, (0, 0, 0)), (screen.get_width() // 2 - 75, 248))
        if restart_rect.collidepoint(mouse_x, mouse_y):
            life = 8
            loose_play = 0
            secret_word = random.choice(mots)
            mot_cache = "_" * len(secret_word)
            state_word = mot_cache
            for letter in letter_rect:
                letter[2] = 1
                letter[3] = 1


    if life <= 0:
        if loose_play == 0:
            fail.set_volume(0.2)
            fail.play(loops=0)
            loose_play = 1

        screen.blit(end_background, (0, 0))
        screen.blit(font.render(f'Tu as perdu !', 1,  (255, 255, 255)), (screen.get_width()//2 - 145, 30))
        pygame.draw.rect(screen, (255, 255, 255), restart_rect, border_radius=15)
        screen.blit(font_2.render("Recommencer", 1, (0, 0, 0)), (screen.get_width() // 2 - 75, 248))
        if restart_rect.collidepoint(mouse_x, mouse_y):
            click.play()
            pygame.mixer.music.load("BackGround_effect.mp3")
            pygame.mixer.music.play(loops=-1)
            pygame.mixer.music.set_volume(0.05)
            life = 8
            loose_play = 0
            secret_word = random.choice(mots)
            mot_cache = "_" * len(secret_word)
            state_word = mot_cache
            for letter in letter_rect:
                letter[2] = 1
                letter[3] = 1

    pygame.display.flip()




