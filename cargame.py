import pygame
import random
from pygame.locals import *
import sys
import os
import time


pygame.init()
pygame.time.set_timer(USEREVENT, 2000)
screen = pygame.display.set_mode((500, 700))

clock = pygame.time.Clock()


def image_name(name, width, height):
    name = pygame.image.load("images/" + name)
    name = pygame.transform.scale(name, (width, height))

    return name


pygame.mixer.init()
pygame.mixer.music.load("sounds/car_start_garage.wav")
pygame.mixer.music.load("sounds/Racer.mpeg")


image_car = image_name("car_03.png", 40, 85)
image_start = image_name("start.png", 96, 40)
image_lawn = image_name("lawn_1.jpg", 96, 700)
image_coin = image_name("one_coin.png", 30, 30)
image_pit = image_name("pit.png", 50, 50)
image_crash = image_name('crash.png', 40, 40)
image_2x = image_name('2x.png', 30, 30)
image_life = image_name("life.png",20, 20)
image_start_1 = image_name("ssstart.jpeg", 76, 32)
image_levels = image_name("setting.jpeg", 76, 32)
image_instruction = image_name("instruction.jpeg", 76, 32)
image_exit = image_name("exit.jpeg", 76, 32)
image_yes = image_name("yes.jpeg", 76, 32)
image_no = image_name("no.jpeg", 76, 32)
image_avengers = image_name("avengers.jpeg", 500, 500)
image_coin_counter = image_name('coin_counter.png', 60, 60)
image_score = image_name('scores.png', 30, 400)
image_coin_counter_background = image_name('coin_counter_background.jpg', 100, 30)

road_speed = 0
place = [112, 176, 240, 304, 368]
place_1 = [120, 200, 280, 360]

start_ticks = pygame.time.get_ticks()


class Car:
    def __init__(self, x, y, money,life, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.money = money
        self.life = life

    def collision(self, x_1, y_1, x_1_width, y_1_height):
        first_rectangular = pygame.Rect((self.x, self.y, self.width, self.height))
        second_rectangular = pygame.Rect((x_1, y_1, x_1_width, y_1_height))

        return first_rectangular.colliderect(second_rectangular)


class Block:
    obstacle_cars = [image_name("car03.png", 40, 80), image_name("car04.png", 40, 80),
                     image_name("car02.png", 40, 80), image_name("car01_level1.png", 40, 80), 
                     image_name("car01_level2.png", 40, 80), image_name("kamaz.png", 40, 90), 
                     image_name("truck_1.png", 40, 90), image_name("car06.png", 40, 90),
                     image_name("car05.png", 35, 80), image_name("car06.png", 40, 80), ]

    def __init__(self, x, y, name, random_obstacle):
        self.x = x
        self.y = y
        self.name = name
        self.random_obstacle = random_obstacle
        self.img = self.obstacle_cars[self.random_obstacle]
        self.obstacle_speed_change = None

    def different_speeds_of_obstacles(self, road_speed_change, control):
        if self.x == 112:
            self.obstacle_speed_change = road_speed_change + control - 3 + 1
        if self.x == 176:
            self.obstacle_speed_change = road_speed_change + control - 4 + 1
        if self.x == 240:
            self.obstacle_speed_change = road_speed_change + control - 2 + 1
        if self.x == 304:
            self.obstacle_speed_change = road_speed_change + control - 2 + 1
        if self.x == 368:
            self.obstacle_speed_change = road_speed_change + control - 3 + 1
        

class PitCoin:
    tree_images = [image_name('trees_1.png', 80, 50), image_name('tree_4.png', 80, 50), image_name('tree_5.png',
                                                                                                   80, 50)]

    def __init__(self, x, y, name, is_collision):
        self.x = x
        self.y = y
        self.name = name
        self.is_collision = is_collision

    def random_tree(self, n):
        return self.tree_images[n]


def crash():
    python = sys.executable
    os.execl(python, python, * sys.argv)


def random_appear( n):
    line_appear = random.randint(0, n)
    return place[line_appear]


def lines():
    screen.fill((65, 65, 65))
    for i in range(163, 419, 64):
        for j in range(0, 720, 20):
            pygame.draw.line(screen, (255, 255, 255), (i, j), (i, j+10), 3)
    pygame.draw.line(screen, (255, 255, 255), (98, 0), (98, 700), 3)
    pygame.draw.line(screen, (255, 255, 255), (418, 0), (418, 700), 3)
    screen.blit(image_car, (car_1.x, car_1.y))


shift = 0
car_1 = Car(place_1[shift], 350, 0, 100, 40, 85)


def coin_counter():
    screen.blit(image_coin_counter, (20, 20))


def coin_display(coin_number):
    screen.blit(image_coin_counter, (15, 5))
    font = pygame.font.Font('images/Sunday Morning.ttf', 20)
    coin_text = font.render(str(coin_number), True, (255, 0, 0))
    screen.blit(image_coin_counter_background, (0, 80))
    screen.blit(coin_text, (5, 75))


def main_menu():
    global shift, event, done_1

    done_1 = False

    while not done_1:
        car_1.x = place_1[shift]
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done_1 = True

        lines()
        screen.blit(image_lawn, (0, 0))
        screen.blit(image_lawn, (420, 0))
        screen.blit(image_start_1, (100, 300))
        screen.blit(image_levels, (180, 300))
        screen.blit(image_instruction, (260, 300))
        screen.blit(image_exit, (340, 300))

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                shift = (shift-1) % 4
            if event.key == pygame.K_RIGHT:
                shift = (shift+1) % 4
            if event.key == pygame.K_RETURN:
                if car_1.x == 120:
                    start_game()
                    done_1 = True
                if car_1.x == 200:
                    setting()
                    done_1 = True
                if car_1.x == 280:
                    instructions()
                    done_1 = True
                if car_1.x == 360:
                    done_1 = True
        pygame.display.flip()
        clock.tick(7)


def setting():
    global event, sett

    sett = False
    place_of_sound = [160, 320]
    shift = 0

    while not sett:
        car_1.x = place_of_sound[shift]

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sett = True

        lines()
        screen.blit(image_lawn, (0, 0))
        screen.blit(image_lawn, (420, 0))
        screen.blit(image_yes, (140, 300))
        screen.blit(image_no, (300, 300))

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                shift = (shift-1) % 2
            if event.key == pygame.K_RIGHT:
                shift = (shift+1) % 2
            if event.key == pygame.K_RETURN:
                if car_1.x == 160:
                    pygame.mixer.music.play(2)
                if car_1.x == 320:
                    pygame.mixer.music.stop()
            if event.key == pygame.K_ESCAPE:
                sett = True
                main_menu()

        pygame.display.flip()
        clock.tick(5)


def instructions():
    global event, instr

    instr = False

    while not instr:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                instr = True
                main_menu()
        screen.fill((10, 63, 15))
        for i in range(163, 419, 64):
            for j in range(0, 720, 20):
                screen.blit(image_avengers, (0, 100))

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                instr = True
                main_menu()
        pygame.display.flip()
        clock.tick(40)


def start_game():
    global event, done
    blocks = []
    coins = []
    trees = []
    pits = []
    lives = []
    list_seconds = []
    money = 0
    road_speed = 6
    road_speed_change = 6
    left_right_speed_change = 5
    done = False

    car = Car(place[2], 500, 0, 100, 40, 85)

    while not done:
        control = 0
        surf = pygame.Surface((car.life, 10))
        surf.fill((0, 255, 0))
        
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
                    pygame.draw.line(screen, (255, 255, 255), (i, (j+road_speed) % 700), (i, (j+road_speed+10) % 700),
                                     3)
        pygame.draw.line(screen, (255, 255, 255), (98, 0), (98, 700), 3)
        pygame.draw.line(screen, (255, 255, 255), (418, 0), (418, 700), 3)

        screen.blit(image_car, (car.x, car.y))
        screen.blit(image_start, (212, road_speed))

        seconds = int((pygame.time.get_ticks() - start_ticks) / 1000)

        list_seconds.append(seconds)

        if list_seconds.count(seconds) == 1:
            if seconds % 15 == 0:
                num_of_life = random_appear(4)
                life = PitCoin(num_of_life, -40, 'life', False)
                lives.append(life)
            if seconds % 2 == 0:
                distance_of_trees = 0
                n = 4
                n_1 = 350
                for i in range(n):

                    tree = PitCoin(0, distance_of_trees - n_1, 'tree', False)
                    random_n = random.randint(0, 2)
                    image_tree = tree.random_tree(random_n)

                    trees.append((tree, image_tree))
                    distance_of_trees += 100

        k = pygame.time.get_ticks() % 2500
            
        if 1250 < k < 1300:
            num_of_pit = random_appear(4)
            if num_of_pit:
                pit = PitCoin(num_of_pit, -40, 'pit', False)
                pits.append(pit)

        if 700 < k < 750:
            num_of_coin = random_appear(4)
            coin = PitCoin(num_of_coin, -30, 'coin', False)
            coins.append(coin)

        if 100 < k < 150:
            if 0 <= car.money % 100 <= 10 and car.money != 0:
                
                road_speed_change += 1
                control += 2
                car.money = car.money + 10

            num_of_obstacles = random_appear(4)
            
            random_obstacle = random.randint(0, 8)
            block = Block(num_of_obstacles, -80, 'obstacle', random_obstacle)
            block.different_speeds_of_obstacles(road_speed_change, control)

            blocks.append(block)

        for pit_i in pits:
            if pit_i.name == "pit":
                screen.blit(image_pit, (pit_i.x, pit_i.y))
                screen.blit(image_car, (car.x, car.y))
                if car.collision(pit_i.x, pit_i.y, 40, 40):
                    if not pit_i.is_collision:
                        car.life -= 10
                        print("----LIFE + ", car.life, end="\n\n")
                        pit_i.is_collision = True
                    else:
                        pass

                pit_i.y += road_speed_change

            if pit_i.y > 700:
                pits.remove(pit_i)

        for block_i in blocks:
            if block_i.name == "obstacle":
                screen.blit(block_i.img, (block_i.x, block_i.y))
                if car.collision(block_i.x, block_i.y, 40, 80):
                    print("CRASH")
                    screen.blit(image_crash, (car.x, car.y+20))

                    done = True
                    main_menu()

                block_i.y += block_i.obstacle_speed_change 

            if block_i.y > 700:
                blocks.remove(block_i)

        for tree in trees:
            
            screen.blit(tree[1], (tree[0].x, tree[0].y))       
            if tree[0].y > 700:
                trees.remove(tree)

            tree[0].y += road_speed_change
     
        for coin in coins:
            if coin.name == "coin":
                screen.blit(image_coin, (coin.x, coin.y))
                coin.y += road_speed_change
                
                if coin.y > 700:
                    coins.remove(coin)

                if car.collision(coin.x, coin.y, 30, 30):
                    print("\n++money!!!!!\n")
                    car.money += 10
                    money += 1
                    coins.remove(coin)

        for life in lives: 
                screen.blit(image_life, (life.x, life.y))
                life.y += road_speed_change
                    
                if life.y > 700:
                    lives.remove(life)

                if car.collision(life.x, life.y, 30, 30):
                    car.life += 10 
                    print(f"{car.life}")
                    lives.remove(life)

        road_speed += road_speed_change

        screen.blit(surf, (380, 8))
        screen.blit(image_name("life.png", 16, 16), (480, 6))

        if car.life == 0:
            time.sleep(2)
            done = True
            main_menu()
        coin_display(money)
        pygame.display.flip()
        clock.tick(40)


main_menu()
