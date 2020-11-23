import pygame
import random
from pygame.locals import *
import sys
import os
import time


pygame.init()
pygame.time.set_timer(USEREVENT, 2000)
screen = pygame.display.set_mode((500, 700))
done = False
clock = pygame.time.Clock()

def image_name(name, width, height):
    name = pygame.image.load("images/" + name)
    name = pygame.transform.scale(name, (width, height))

    return name

image_car = image_name("car01.png",40, 80)
image_obstacle = image_name("car04.png", 40, 80)
image_start = image_name("start.png", 96, 40)
image_lawn = image_name("lawn.jpg", 96, 700)
image_coin = image_name("oil1.png", 30, 30)
image_pit = image_name("pit_1.png", 50, 50)
image_crash = image_name('crash.png', 30, 30)

road_speed = 0
place = [112, 176, 240, 304, 368]


class Car:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Block:
    def __init__(self, x, y, obstacle_speed_change):
        self.x = x
        self.y = y
        self.obstacle_speed_change = obstacle_speed_change


class Coin:
    def __init__(self, x, y):
        self.x = x
        self.y = y


def crash():
    python = sys.executable
    os.execl(python, python, * sys.argv)

def random_appear( n):
    line_appear = random.randint(0, n)
    return place[line_appear]


def collision(x, y,x_width, y_height,  x_1, y_1, x_1_width, y_1_height ):
    first_rectangular = pygame.Rect((x, y,x_width, y_height))
    second_rectangular = pygame.Rect((x_1, y_1, x_1_width, y_1_height))

    return first_rectangular.colliderect(second_rectangular)

blocks = []
coins = []

coin_speed_change = 6
num_of_obstacles = None
num_of_coin = None
num_of_pit = None
car_life = 10

direction = ""
money = 0

road_speed_change = 4
left_right_speed_change = 5

car = Car(place[2], 500)


while not done:


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
   
    if pygame.key.get_pressed()[pygame.K_LEFT]:
        if 0 < car.x < 98:
            car.x += left_right_speed_change
        car.x -= left_right_speed_change
    if pygame.key.get_pressed()[pygame.K_RIGHT]:
        if 380 < car.x < 700:
            car.x -= left_right_speed_change
        car.x += left_right_speed_change
    

    screen.fill((65, 65, 65))

    for i in range(163, 419, 64):
        for j in range(0, 720, 20):
            if ((j+road_speed+10) % 700-(j+road_speed) % 700) < 0:
                pygame.draw.line(screen, (255, 255, 255), (i, 0), (i, (j+road_speed+10) % 700), 3)
            else: 
                pygame.draw.line(screen, (255, 255, 255), (i, (j+road_speed) % 700), (i, (j+road_speed+10) % 700), 3)
    pygame.draw.line(screen, (255, 255, 255), (98, 0), (98, 700), 3)
    pygame.draw.line(screen, (255, 255, 255), (418, 0), (418, 700), 3)
    screen.blit(image_lawn, (0, 0))
    screen.blit(image_lawn, (420, 0))
    
    screen.blit(image_car, (car.x, car.y))
    screen.blit(image_start, (212, road_speed))
    
    k = pygame.time.get_ticks() % 2000

    if 1300 < k < 1340:
        if money >= 100 and money <= 200:
            num_of_obstacles = random_appear(2)
            left_right_speed_change = 8
            num_of_pit = random_appear(2)

        else:
            num_of_obstacles = random_appear(4)
            num_of_pit = None
        num_of_coin = random_appear(4)
        
        random_num =  random.randint(0, 3)
        block = Block(num_of_obstacles, -80, random_num)
        blocks.append((block, "obstacle")) 

        if num_of_pit != None:
            pit = Block(num_of_pit, -40, 0)
            if collision(block.x, block.y, 40,80,  pit.x, pit.y, 40, 40 ):
                blocks.append((pit, "pit"))
                blocks.remove((block, "obstacle"))
            else: continue
        coin = Coin(num_of_coin, -30)
        coins.append(coin)


    for block_i in blocks:
        if block_i[1] == "pit":
            screen.blit(image_pit, (block_i[0].x, block_i[0].y))
            screen.blit(image_car, (car.x, car.y))
            if collision(car.x, car.y, 40,80,  block_i[0].x, block_i[0].y, 40, 40 ):
                car_life -= 1
                print("----LIFE + ",car_life, end="\n\n")
            block_i[0].y += 4
                

        elif block_i[1] == "obstacle":
            screen.blit(image_obstacle, (block_i[0].x, block_i[0].y))
            if collision(car.x, car.y, 40,80,  block_i[0].x, block_i[0].y, 40, 80 ):
                print("CRASH")
                screen.blit(image_crash, (car.x, car.y))
                time.sleep(2)
                done = True
        block_i[0].y += block_i[0].obstacle_speed_change

        if block_i[0].y > 700:
            blocks.remove(block_i)
            num_of_obstacles = []

        
        
    
    for coin in coins:
        screen.blit(image_coin, (coin.x, coin.y))
        coin.y += coin_speed_change
        if coin.y > 700:
            coins.remove(coin)
            num_of_coin = []

        if collision(car.x, car.y, 40,80,  coin.x, coin.y, 30, 30 ):             
            print("\n++money!!!!!\n")
            money += 10 
            if money % 100 == 0:
                coin_speed_change += 2

            coins.remove(coin)

    

    road_speed += road_speed_change
    

        


    pygame.display.flip()
    clock.tick(40)
print(money)