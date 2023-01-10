from dataclasses import dataclass
from functools import cache
from copy import deepcopy
import pygame
import random
import pickle # 진행상황 저장용
import ctypes
import math
from time import time

from data import lands_info as city_info
from data import golden_txt

pygame.init()
pygame.display.set_caption("불후마불")

WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
GREEN = (50, 255, 50)
GRAY = (50, 50, 50)
BLACK = (0, 0 ,0)
FPS = 200
u32 = ctypes.windll.user32
size = (u32.GetSystemMetrics(0), u32.GetSystemMetrics(1)) # (1536, 864)
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()

# 이미지 로드
if True:
    def load_img(path, size):
        tmp_img = pygame.image.load(path)
        return pygame.transform.scale(tmp_img, size)
    board = load_img("./img/board.png", (size[1], size[1]))
    red_card_img = load_img("./img/red_land_card.png", (size[1]*7/26, size[1]*7/26))
    green_card_img = load_img("./img/green_land_card.png", (size[1]*7/26, size[1]*7/26))
    blue_card_img = load_img("./img/blue_land_card.png", (size[1]*7/26, size[1]*7/26))
    black_card_img = load_img("./img/black_land_card.png", (size[1]*7/26, size[1]*7/26))

    golden_hammer = []
    golden_hammer.append(load_img("./img/golden_hammer_back.png", (size[1]*7/26, size[1]*7/26)))
    golden_hammer.append(load_img("./img/golden_hammer_front.png", (size[1]*8/13, size[1]*7/26)))
    
    dice = []
    for i in range(6):
        dice.append(load_img(f"./img/dice{i+1}.png", (size[1]*7/26, size[1]*7/26)))

@cache
def font(size):
    return pygame.font.Font('./font/NotoSansKR-Medium.otf', size)

def write(txt, font_size, color, pos, criterion="center"):
    text = font(font_size).render(txt, True, color)
    text_pos = text.get_rect()
    if criterion == "center":
        text_pos.center = pos
    elif criterion == "top":
        text_pos.top = pos
    elif criterion == "topleft":
        text_pos.topleft = pos
    elif criterion == "topright":
        text_pos.topright = pos
    elif criterion == "bottom":
        text_pos.bottom = pos
    elif criterion == "bottomleft":
        text_pos.bottomleft = pos
    elif criterion == "bottomright":
        text_pos.bottomright = pos
    screen.blit(text, text_pos)

def cut_txt(text, font_size, max_len):
    def get_line(split_text):
        current_text = split_text[0]
        next_text = split_text[0]
        for i in range(1, len(split_text)):
            next_text = current_text + ' ' + split_text[i]
            text_rect = font(font_size).render(next_text, True, BLACK).get_rect()
            if text_rect.width >= max_len:
                return current_text, i
            current_text += ' ' + split_text[i]
        return current_text, 0
    
    split_text = text.split(' ')
    text_list = []
    while True:
        append_text, i = get_line(split_text)
        text_list.append(append_text)
        if i:
            for j in range(i):
                del split_text[0]
        else:
            break
    return text_list

def runGame():
    class City:
        def __init__(self, city_info, building_state, coordinate, size, card_img):
            self.info = city_info
            self.building_state = building_state
            self.coord = coordinate
            self.size = size
            self.img = card_img
            self.owner = 4

        def get_fee(self):
            fee = 5
            building_fee = (10, 20, 50, 50, 75, 40)

            for i in range(len(self.building_state)):
                if self.building_state[i]:
                    fee += building_fee[i]
            
            return self.info.land // 100 * fee

        def show_card(self, arrived):
            txt = self.info.name
            if arrived:
                card_txt_pos = ((size[0]/2 + size[1]*11/78, size[1]*25/78), (size[0]/2 + size[1]*20/78, size[1]*25/78), \
                                (size[0]/2 + size[1]*11/78, size[1]*14/39), (size[0]/2 + size[1]*20/78, size[1]*14/39), \
                                (size[0]/2 + size[1]*11/78, size[1]*31/78), (size[0]/2 + size[1]*20/78, size[1]*31/78), \
                                (size[0]/2 + size[1]*9/52, size[1]*7/26), (size[0]/2 + size[1]*9/52, size[1]*45/104))

                screen.blit(self.img, (size[0]/2 + size[1]/26, size[1]*5/26))
                write(txt, size[1]//40, BLACK, (size[0]/2 + size[1]*9/52, size[1]*11/52))
            else:
                card_txt_pos = ((size[0]/2 - size[1]*8/39, size[1]*25/78), (size[0]/2 - size[1]*7/78, size[1]*25/78), \
                                (size[0]/2 - size[1]*8/39, size[1]*14/39), (size[0]/2 - size[1]*7/78, size[1]*14/39), \
                                (size[0]/2 - size[1]*8/39, size[1]*31/78), (size[0]/2 - size[1]*7/78, size[1]*31/78), \
                                (size[0]/2 - size[1]*9/52, size[1]*7/26), (size[0]/2 - size[1]*9/52, size[1]*45/104))

                screen.blit(self.img, (size[0]/2 - size[1]*4/13, size[1]*5/26))
                write(txt, size[1]//40, BLACK, (size[0]/2 - size[1]*9/52, size[1]*11/52))
            
            @cache
            def get_prices(city):
                return (city.house1, city.house2, city.house3, city.building, city.hotel, city.landmark)

            def write_info():
                for j in range(6):
                    price_txt = f"{get_prices(self.info)[j]//10000}만"
                    price_txt += "" if get_prices(self.info)[j]%10000 == 0 else f" {get_prices(self.info)[j]%10000//1000}천"
                    write(price_txt, size[1]//50, BLACK, card_txt_pos[j])
                write(f"{self.info.land//10000}만", size[1]//30, BLACK, card_txt_pos[-2])

                price_txt = "통행요금 :"
                price_txt += "" if self.get_fee()//10000 == 0 else f" {self.get_fee()//10000}만"
                price_txt += "" if self.get_fee()%10000 == 0 else f" {self.get_fee()%10000//1000}천"
                price_txt += "" if self.get_fee()%1000 == 0 else f" {self.get_fee()%1000//100}백"
                price_txt += " 0" if price_txt == "통행요금 :" else ""
                write(price_txt, size[1]//60, BLACK, card_txt_pos[-1])
            
            write_info()

    class Space:
        def __init__(self, space_info, coordinate, size, card_img):
            self.info = space_info
            self.coord = coordinate
            self.size = size
            self.img = card_img

    if True:
        bottom_pos = [(size[0]/2 + size[1]/2 - size[1]*2/13, size[1]*11/13)]
        left_pos = [(size[0]/2 - size[1]/2, size[1]*11/13)]
        top_pos = [(size[0]/2 - size[1]/2, 0)]
        right_pos = [(size[0]//2 + size[1]/2 - size[1]*2/13, 0)]
        for i in range(9):
            bottom_pos.append((size[0]/2 + size[1]/2 - size[1]*(3+i)/13, size[1]*11/13))
            left_pos.append((size[0]/2 - size[1]/2, size[1]*(10-i)/13))
            top_pos.append((size[0]/2 - size[1]//2 + size[1]*(2+i)/13, 0))
            right_pos.append((size[0]/2 + size[1]/2 - size[1]*2/13, size[1]*(2+i)/13))
        space_pos = bottom_pos + left_pos + top_pos + right_pos

        spaces = []
        for i in range(40):
            if i%10 == 0:
                space_size = (size[1]*2/13, size[1]*2/13)
            else:
                tmp_size = ((size[1]/13, size[1]*2/13), (size[1]*2/13, size[1]/13))
                space_size = tmp_size[i//10%2]
            spaces.append(Space("info", space_pos[i], space_size, "img"))

        red_pos = deepcopy(bottom_pos)
        green_pos = deepcopy(left_pos)
        blue_pos = deepcopy(top_pos)
        black_pos = deepcopy(right_pos)

        for i in [8, 5, 2, 0]:
            red_pos[i] = (0, 0)
            green_pos[i] = (0, 0)
            blue_pos[i] = (0, 0)
            black_pos[i] = (0, 0)

        cities = []
        card_imgs = (red_card_img, green_card_img, blue_card_img, black_card_img)
        cities_pos = (red_pos, green_pos, blue_pos, black_pos)
        cities_size = ((size[1]/13, size[1]*2/13), (size[1]*2/13, size[1]/13))
        for i in range(len(card_imgs)):
            tmp = -1
            for j in range(len(cities_pos[i])):
                if j in [8, 5, 2, 0]:
                    tmp -= 1
                tmp += 1
                cities.append(City(city_info[i][tmp], [0, 0, 0 ,0, 0, 0], cities_pos[i][j], cities_size[i%2], card_imgs[i]))

    def pos_to_coord(pos):
        return spaces[pos].coord

    def coord_to_pos(coord):
        for i in spaces:
            length = (coord[0] - i.coord[0], coord[1] - i.coord[1])
            if length[0] < 0 or length[1] < 0:
                continue
            if length[0] <= i.size[0] and length[1] <= i.size[1]:
                return spaces.index(i)
        return -1

    def show_card(cursor_coord, arrived):
        pos = coord_to_pos(cursor_coord)

        if pos == -1:
            return False
        if arrived:
            img_coord = (size[0]/2 + size[1]/26, size[1]*5/26)
        img_coord = (size[0]/2 - size[1]*4/13, size[1]*5/26)

        if pos%10 == 0:
            return False
        elif pos in (5, 8, 12, 18, 22, 28, 35):
            screen.blit(golden_hammer[0], img_coord)
            return True
        elif pos in (2, 15, 25, 32, 38):
            return True

        cities[pos].show_card(arrived)
        return True

    while True:
        clock.tick(FPS)
        screen.fill(WHITE)

        screen.blit(board, (size[0]//2 - size[1]//2, 0))
        pressed_key = -1
        clicked = False

        cursor_coord = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 0
            if event.type == pygame.KEYDOWN:
                pressed_key = event.key
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                clicked = True

        if pressed_key == pygame.K_ESCAPE:
            return 0

        if clicked:
            print(coord_to_pos(cursor_coord))
        
        show_card(cursor_coord, False)

        pygame.display.update()

runGame()
pygame.quit()