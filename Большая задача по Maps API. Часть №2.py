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
    a = requests.get(f'https://static-maps.yandex.ru/1.x/?ll={cords[0]},{cords[1]}&l=sat&z={zoom}&z=4&size=600,600')
    target.write(a.content)
    target.close()

pygame.init()
pygame.display.set_caption('Map')
size = width, height = 600, 600
screen = pygame.display.set_mode(size)

flag = True
img = load_image("newfile.png")
screen.blit(img, (0, 0))
pygame.display.update()
fps = 1
clock = pygame.time.Clock()
while flag:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            flag = False
        if event.type == pygame.KEY_UP and event.key == 480:  # pg_up
            zoom += 1
            if zoom > 17:
                zoom = 17
        if event.type == pygame.KEY_UP and event.key == 481:  # pg_down
            zoom -= 1
            if zoom < 0:
                zoom = 0
    with open('newfile.png', 'wb') as target:
        a = requests.get(f'https://static-maps.yandex.ru/1.x/?ll={cords[0]},{cords[1]}&l=sat&z={zoom}&size=600,600')
        target.write(a.content)
        target.close()
    img = load_image("newfile.png")
    screen.blit(img, (0, 0))
    clock.tick(fps)
    pygame.display.flip()
pygame.quit()
