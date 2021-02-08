import requests
import pygame
import os
import sys


# just for test

def load_image(name, colorkey=None):
    fullname = os.path.join(name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


with open('newfile.png', 'wb') as target:
    cords = input('Введите координаты через пробел: ').split()
    zoom = int(input('Введите масштаб (0 - 17): '))
    a = requests.get(f'https://static-maps.yandex.ru/1.x/?ll={cords[0]},{cords[1]}&l=sat&z={zoom}&size=600,400')
    target.write(a.content)
    target.close()

pygame.init()
pygame.display.set_caption('Map')
size = width, height = 600, 400
screen = pygame.display.set_mode(size)
flag1 = True
font = pygame.font.Font(None, 40)
while flag1:
    text = font.render("Пожалуйста, нажмите кнопку Pg up", True, (100, 255, 100))
    text_x = width // 2 - text.get_width() // 2
    text_y = height // 2 - text.get_height() // 2
    text_w = text.get_width()
    text_h = text.get_height()
    screen.blit(text, (text_x, text_y))
    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            flag1 = False
            pygame.quit()
        if event.type == pygame.KEYUP:
            pg_up = event.key
            flag1 = False
flag2 = True
screen.fill((0, 0, 0))
pygame.display.flip()

while flag2:
    text = font.render("Пожалуйста, нажмите кнопку Pg down", True, (100, 255, 100))
    screen.blit(text, (text_x, text_y))
    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            flag2 = False
            pygame.quit()
        if event.type == pygame.KEYUP:
            pg_down = event.key
            flag2 = False
    pygame.display.flip()
flag = True
img = load_image("newfile.png")
screen.blit(img, (0, 0))
pygame.display.update()
fps = 60
clock = pygame.time.Clock()
while flag:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            flag = False
        if event.type == pygame.KEYUP and event.key == pg_up:  # pg_up
            zoom += 1
            if zoom > 17:
                zoom = 17
            with open('newfile.png', 'wb') as target:
                a = requests.get(
                    f'https://static-maps.yandex.ru/1.x/?ll={cords[0]},{cords[1]}&l=sat&z={zoom}&size=600,400')
                target.write(a.content)
                target.close()
            img = load_image("newfile.png")
            screen.blit(img, (0, 0))
        if event.type == pygame.KEYUP and event.key == pg_down:  # pg_down
            zoom -= 1
            if zoom < 0:
                zoom = 0
            with open('newfile.png', 'wb') as target:
                a = requests.get(
                    f'https://static-maps.yandex.ru/1.x/?ll={cords[0]},{cords[1]}&l=sat&z={zoom}&size=600,400')
                target.write(a.content)
                target.close()
            img = load_image("newfile.png")
            screen.blit(img, (0, 0))
    clock.tick(fps)
    pygame.display.flip()
pygame.quit()
