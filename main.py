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
    def load_img(file_name, size):
        path = "./img/" + file_name
        tmp_img = pygame.image.load(path)
        return pygame.transform.scale(tmp_img, size)
    board = load_img("board.png", (size[1], size[1]))
    red_card_img = load_img("red_land_card.png", (size[1]*7/26, size[1]*7/26))
    green_card_img = load_img("green_land_card.png", (size[1]*7/26, size[1]*7/26))
    blue_card_img = load_img("blue_land_card.png", (size[1]*7/26, size[1]*7/26))
    black_card_img = load_img("black_land_card.png", (size[1]*7/26, size[1]*7/26))

    golden_hammer = []
    golden_hammer.append(load_img("golden_hammer_back.png", (size[1]*7/26, size[1]*7/26)))
    golden_hammer.append(load_img("golden_hammer_front.png", (size[1]*8/13, size[1]*7/26)))

    house = []
    building_y = size[1]*2/39
    house_size = [166/139, 222/148, 260/155]
    for i in range(3):
        house.append(load_img(f"house{i+1}.png", (building_y*house_size[i], building_y)))
    building = load_img("building.png", (building_y*112/146, building_y))
    hotel = load_img("hotel.png", (building_y*178/118, building_y))
    landmark = load_img("landmark.png", (building_y, building_y))
    print(type(landmark))
    
    dice = []
    for i in range(6):
        dice.append(load_img(f"dice{i+1}.png", (size[1]*7/26, size[1]*7/26)))

@cache
def font(size):
    return pygame.font.Font('./font/NotoSansKR-Medium.otf', size)

def write(txt, font_size, color, pos, criterion="center", bg_color=()):
    if bg_color == ():
        text = font(font_size).render(txt, True, color)
    else:
        text = font(font_size).render(txt, True, color, bg_color)
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

    class Player:
        def __init__(self, color, turn):
            self.color = color
            self.turn = turn
            self.money = 1000_0000
            self.pos = 0
            self.size = (size[1]/39, size[1]/39)
            self.name = "player_name"
            self.state = {
                "skip_turn":0, 
                "building_10%_off":0, 
                "esc_island":0, 
                "free_from_fee":0, 
                "space_trip":0, 
                "pay_20":[], 
                "move_to":0, 
                "land&fee_50%":0, 
                "cant_buy":0, 
                "in_island":0
            }
        
        def move(self, num):
            self.pos += num
            if self.pos >= 40:
                self.pos -= 40
            return num-1
        
        def get_abs_coord(self):
            std_pos = space_pos[self.pos]
            turn = self.turn
            if self.pos%10 == 0:
                if turn == 1:
                    return (std_pos[0] + size[1]*2/39, std_pos[1] + size[1]/13)
                elif turn == 2:
                    return (std_pos[0] + size[1]/13, std_pos[1] + size[1]/13)
                elif turn == 3:
                    return (std_pos[0] + size[1]*2/39, std_pos[1] + size[1]*4/39)
                elif turn == 4:
                    return (std_pos[0] + size[1]/13, std_pos[1] + size[1]*4/39)
            elif self.pos//10 == 0:
                if turn == 1:
                    return (std_pos[0] + size[1]/78, std_pos[1] + size[1]/13)
                if turn == 2:
                    return (std_pos[0] + size[1]/26, std_pos[1] + size[1]/13)
                if turn == 3:
                    return (std_pos[0] + size[1]/78, std_pos[1] + size[1]*4/39)
                if turn == 4:
                    return (std_pos[0] + size[1]/26, std_pos[1] + size[1]*4/39)
            elif self.pos//10 == 1:
                if turn == 1:
                    return (std_pos[0] + size[1]*2/39, std_pos[1] + size[1]/78)
                if turn == 2:
                    return (std_pos[0] + size[1]*2/39, std_pos[1] + size[1]/26)
                if turn == 3:
                    return (std_pos[0] + size[1]/39, std_pos[1] + size[1]/78)
                if turn == 4:
                    return (std_pos[0] + size[1]/39, std_pos[1] + size[1]/26)
            elif self.pos//10 == 2:
                if turn == 1:
                    return (std_pos[0] + size[1]/26, std_pos[1] + size[1]*2/39)
                if turn == 2:
                    return (std_pos[0] + size[1]/78, std_pos[1] + size[1]*2/39)
                if turn == 3:
                    return (std_pos[0] + size[1]/26, std_pos[1] + size[1]/39)
                if turn == 4:
                    return (std_pos[0] + size[1]/78, std_pos[1] + size[1]/39)
            elif self.pos//10 == 3:
                if turn == 1:
                    return (std_pos[0] + size[1]/13, std_pos[1] + size[1]/26)
                if turn == 2:
                    return (std_pos[0] + size[1]/13, std_pos[1] + size[1]/78)
                if turn == 3:
                    return (std_pos[0] + size[1]*4/39, std_pos[1] + size[1]/26)
                if turn == 4:
                    return (std_pos[0] + size[1]*4/39, std_pos[1] + size[1]/78)

        def cursor_on(self, cursor_coord):
            coord = self.get_abs_coord()
            length = (cursor_coord[0] - coord[0], cursor_coord[1] - coord[1])

            if length[0] < 0 or length[1] < 0:
                return False
            if length[1] <= self.size[0] and length[1] <= self.size[1]:
                return True

        def show(self):
            coord = self.get_abs_coord()
            pygame.draw.rect(screen, self.color, (coord[0], coord[1], self.size[0], self.size[1]))

    class Button:
        def __init__(self, img:pygame.Surface, coord):
            self.img = img
            self.coord = coord
            self.size = (img.get_width(), img.get_height())

        def cursor_on(self):
            length = (cursor_coord[0] - self.coord[0], cursor_coord[1] - self.coord[1])
            if length[0] < 0 or length[1] < 0:
                return False
            if length[1] <= self.size[0] and length[1] <= self.size[1]:
                return True

        def show(self, text, font_size, color):
            screen.blit(self.img, self.coord)
            write(text, font_size, color, self.coord, "topleft")

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

        spaces:list[Space] = []
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

        cities:list[City] = []
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
        
        players = (Player((255, 0, 0), 1), Player((0, 255, 0), 2), Player((0, 0, 255), 3), Player((0, 0, 0), 4))

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
        if type(cursor_coord) in (list, tuple):
            pos = coord_to_pos(cursor_coord)
        else:
            pos = cursor_coord

        if pos == -1:
            return False
        img_coord = (size[0]/2 - size[1]*4/13, size[1]*5/26)
        if arrived:
            img_coord = (size[0]/2 + size[1]/26, size[1]*5/26)

        if pos%10 == 0:
            return False
        elif pos in (5, 8, 12, 18, 22, 28, 35):
            screen.blit(golden_hammer[0], img_coord)
            return True
        elif pos in (2, 15, 25, 32, 38):
            return True

        cities[pos].show_card(arrived)
        return True

    def roll_dice():
        dice_list = [list(range(6)), list(range(6))]
        return [random.choice(dice_list[0]), random.choice(dice_list[1])]

    def show_golden_task(card_num, task_done):
        global case9

        title = golden_txt[card_num].title
        content = golden_txt[card_num].content.split("\n")
        effect = golden_txt[card_num].effect

        if task_done:
            card_num = 0
        match (card_num):
            case 0:
                pass
            case 1:
                players[turn%4].money -= 5000
            case 2:
                players[turn%4].money += 1_0000
                players[turn%4].golden["skip_turn"] += 1
            case 3:
                players[turn%4].money += 1_5000
                tmp_list = list(range(4))
                del tmp_list[turn%4]
                for i in tmp_list:
                    players[i].money -= 5000
            case 4:
                # 자기 건물 가격의 10% 지불
                pass
            case 5:
                random_num = random.uniform(0, 100)
                if random_num <= 0.01:
                    players[turn%4].money += 5000_0000*7//10
                    golden_txt[5].title = "복권 당첨 (1등, 5000만원)"
                    golden_txt[5].content = "당신은 5천원을 주고 복권을 구매했습니다.\n1등 당첨!! 당첨자가 한동안 없었나보군요!"
                    golden_txt[5].effect = "5천원 지불 및 3500만원 지급"
                elif random_num <= 0.1:
                    players[turn%4].money += 500_0000*7//10
                    golden_txt[5].title = "복권 당첨 (1등, 500만원)"
                    golden_txt[5].content = "당신은 5천원을 주고 복권을 구매했습니다.\n1등 당첨!! 운이 아주 좋았네요!"
                    golden_txt[5].effect = "5천원 지불 및 350만원 지급"
                elif random_num <= 1:
                    players[turn%4].money += 100_0000*7//10
                    golden_txt[5].title = "복권 당첨 (2등, 100만원)"
                    golden_txt[5].content = "당신은 5천원을 주고 복권을 구매했습니다.\n2등이라니! 세금을 제외해도 70만원입니다!"
                    golden_txt[5].effect = "5천원 지불 및 70만원 지급"
                elif random_num <= 5:
                    players[turn%4].money += 10_0000
                    golden_txt[5].title = "복권 당첨 (3등, 10만원)"
                    golden_txt[5].content = "당신은 5천원을 주고 복권을 구매했습니다.\n3등이라니! 꽤 운이 좋았군요."
                    golden_txt[5].effect = "5천원 지불 및 10만원 지급"
                elif random_num <= 20:
                    players[turn%4].money += 5_0000
                    golden_txt[5].title = "복권 당첨 (4등, 5만원)"
                    golden_txt[5].content = "당신은 5천원을 주고 복권을 구매했습니다.\n4등이라면 나쁘지 않은 결과네요."
                    golden_txt[5].effect = "5천원 지불 및 5만원 지급"
                else:
                    players[turn%4].money += 1_0000
                    golden_txt[5].title = "복권 당첨 (5등, 1만원)"
                    golden_txt[5].content = "당신은 5천원을 주고 복권을 구매했습니다.\n비록 5등이지만 그래도 5천원은 벌었네요."
                    golden_txt[5].effect = "5천원 지불 및 1만원 지급"
                players[turn%4].money -= 5000
            case 6:
                # 건설비용 10% 할인권 지급
                players[turn%4].state["building_10%_off"] += 1
            case 7:
                # 무인도 탈출권 지급
                players[turn%4].state["esc_island"] += 1
                pass
            case 8:
                # 다음 통행료 면제, 해당 땅 주인 1턴 쉬기
                players[turn%4].state["free_from_fee"] += 1
                pass
            case 9:
                # 플레이어 지목해서 1만원 깎고 1만원 추가
                case9 = True
            case 10:
                players[turn%4].state["skip_turn"] += 2
                pass
            case 11:
                for i in players:
                    i.money += 10_0000
            case 12:
                if turn%4 == 3:
                    players[0].state["skip_turn"] += 1
                else:
                    players[turn%4+1].state["skip_turn"] += 1
                pass
            case 13:
                players[turn%4].money -= 5_0000
                players[turn%4].state["skip_turn"] += 1
            case 14:
                # 우주여행권 지급
                players[turn%4].state["space_trip"] += 1
                pass
            case 15:
                # 기능 없음
                pass
            case 16:
                players[turn%4].money -= random.randint(5, 10)*1000
            case 17:
                players[turn%4].money += 10_0000
                players[turn%4].state["pay_20"].append(3)
                # 3턴 뒤 20만원 깎기
            case 18:
                # 보유한 땅 중 1개 랜덤으로 통행료 50% 영구 상승
                pass
            case 19:
                # 빨강, 초록 땅 중 하나의 통행료 50% 영구 상승 (본인 땅이 아니어도 OK)
                pass
            case 20:
                players[turn%4].money -= 2_0000
            case 21:
                players[turn%4].money -= 2_0000
            case 22:
                players[turn%4].money -= 5_0000
            case 23:
                # 3턴간 통행료 50%
                pass
            case 24:
                # 기능 없음
                pass
            case 25:
                # 3턴간 본인 소유의 땅 중 랜덤한 하나 통행료 50% 감소
                pass
            case 26:
                players[turn%4].state["skip_turn"] += 2
                # 플레이어 지목해서 10만원 받기
            case 27:
                # 기능 없음
                pass
            case 28:
                # 다음 턴에 카지노로 이동
                players[turn%4].state["move_to"] = 15 - players[turn%4].pos if players[turn%4].pos < 15 else 55 - players[turn%4].pos
            case 29:
                # 3턴간 땅의 가격과 통행료 50% 증가
                players[turn%4].state["land&fee_50%"] += 3
            case 30:
                tmp_list = list(range(4))
                del tmp_list[turn%4]
                tmp_index = [1] if turn%4 == 0 else [0]
                for i in range(1, 3):
                    if players[tmp_index[0]].money > players[tmp_list[i]].money:
                        tmp_index = [tmp_list[i]]
                    elif players[tmp_index[0]].money == players[tmp_list[i]].money:
                        tmp_index.append(tmp_list[i])
                for i in tmp_index:
                    players[i].money += 15_0000//len(tmp_index)
                players[turn%4].money -= 15_0000
            case 31:
                # 2턴간 구입 불가
                players[turn%4].state["cant_buy"] += 2
            case 32:
                # 랜덤한 땅 1개 구매비용 돌려받기
                pass
            case 33:
                # 사회복지기금 획득
                players[turn%4].state["skip_turn"] += 2
            case 34:
                players[turn%4].state["move_to"] = 10 - players[turn%4].pos if players[turn%4].pos < 10 else 50 - players[turn%4].pos
            case 35:
                players[turn%4].money -= players[turn%4].money//10

        write(title, size[1]//39, BLACK, (size[0]/2 - size[1]*7/26, size[1]*15/26), "topleft")
        write(effect, size[1]//39, BLACK, (size[0]/2 - size[1]*7/26, size[1]*19/26), "topleft")
        for i in range(len(content)):
            write(content[i], size[1]//39, BLACK, (size[0]/2 - size[1]*7/26, size[1]*16/26 + size[1]*(i+1)/39), "topleft")
        return True

    fixed = False
    turn = -1
    dice_num = [0, 0]
    show_dice = True
    roll = False
    move_num = 0
    move_t = time()
    golden_task_done = False

    while True:
        clock.tick(FPS)
        screen.fill(WHITE)

        screen.blit(board, (size[0]//2 - size[1]//2, 0))
        pressed_key = -1
        clicked = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 0
            if event.type == pygame.KEYDOWN:
                pressed_key = event.key
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                clicked = True

        # 키 입력에 대한 처리
        if pressed_key == pygame.K_ESCAPE:
            return 0
        elif pressed_key == pygame.K_SPACE:
            if move_num == 0:
                roll = not roll
                if not roll:
                    move_num = dice_num[0] + dice_num[1] + 2
                    golden_task_done = False
                    turn += 1

        # 보드판의 각 구역 클릭 시 정보 카드 고정
        if not fixed:
            cursor_coord = pygame.mouse.get_pos()
        if show_card(cursor_coord, False):
            if fixed and clicked:
                fixed = False
            elif clicked:
                fixed = True
        if move_num == 0:
            show_card(players[turn%4].pos, True)
        
        # 주사위 눈 수만큼 움직이기
        if move_num != 0 and time()-move_t >= 0.1:
            players[turn%4].move(1)
            move_t = time()
            move_num -= 1
            if players[turn%4].pos == 0:
                players[turn%4].money += 10_0000 # 월급

        # 주사위 굴리기 및 보이기
        if roll:
            dice_num = roll_dice()
            show_dice = True
        if show_dice:
            screen.blit(dice[dice_num[0]], (size[0]/2 - size[1]*4/13, size[1]*7/13))
            screen.blit(dice[dice_num[1]], (size[0]/2 + size[1]/26, size[1]*7/13))

        # 황금망치에 도착
        if move_num == 0 and not roll and time()-move_t >= 0.5:
            if players[turn%4].pos in (5, 8, 12, 18, 22, 28, 35):
                screen.blit(golden_hammer[1], (size[0]/2 - size[1]*4/13, size[1]*7/13))
                golden_task_done = show_golden_task(5, golden_task_done)
                show_dice = False
            elif players[turn%4].pos%10 in (2, 5, 8):
                pass
            elif players[turn%4].pos%10 == 0:
                pass
            else:
                screen.blit(golden_hammer[1], (size[0]/2 - size[1]*4/13, size[1]*7/13))
                show_dice = False

                building_state = cities[players[turn%4].pos].building_state
                if building_state == [0, 0, 0, 0, 0, 0, 0]:
                    pass
                else:
                    for i in range(3):
                        if building_state[i] == 1:
                            continue
                        else:
                            screen.blit(house[i], (size[0]/2 - size[1]*7/26, size[1]*15/26))
                            break
                    screen.blit(building, (size[0]/2, size[1]*15/26))

        for player in players:
            player.show()
            write(f"{player.money}", 50, BLACK, (0, 50*players.index(player)), "topleft")
        for player in players:
            if player.cursor_on(cursor_coord):
                color = player.color
                is_dark = 0.2126*color[0] + 0.7152*color[1] + 0.0722*color[2] < 127.5
                txt_color = WHITE if is_dark else BLACK
                write(f"{player.name}", 20, txt_color, cursor_coord, "bottomleft", player.color)

        pygame.display.update()

runGame()
pygame.quit()