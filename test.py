from functools import cache
import pygame
import time
import random

pygame.init()
pygame.display.set_caption("title")

WHITE = (255, 255, 255)
BLACK = (0, 0 ,0)
FPS = 60
size = (1200, 600)
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
done = False

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

def run():
    global done
    while not done:
        clock.tick(FPS)
        screen.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    done = True

        text = "당신의 친구가 사정이 생겨 알바를 대신 해달라고 합니다. 당신은 친구를 위해 하루 동안 알바를 뛰고 시급을 받았습니다. 당신은 우연히 야외 방송을 진행하는 유명 유튜버를 만났습니다. 시청자들이 당신을 좋아하는 것 같군요. 빨간색 혹은 초록색의 땅 중 하나에 디즈니랜드가 들어옵니다. 이유가 뭐든 좋은 게 좋은 거죠."
        texts = cut_txt(text, 20, 1000)
        for i in range(len(texts)):
            write(texts[i], 20, WHITE, (0, 20*i), "topleft")

        pygame.display.update()

run()
pygame.quit()