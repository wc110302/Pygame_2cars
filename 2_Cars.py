from random import randint
from threading import Thread
from time import sleep
import pygame
import easygui

Black = (0, 0, 0)
LEFT = 1
RIGHT = 2
LEFT2 = 3
RIGHT2 = 4

Food1 = 'food1.png'
Food2 = 'food2.png'
Play1 = 'play1.png'
Play2 = 'play2.png'

class Button(object): # 按钮
    def __init__(self, upimage, downimage, position):
        self.imageUp = pygame.image.load(upimage).convert_alpha()
        self.imageDown = pygame.image.load(downimage).convert_alpha()
        self.position = position
        self.button_out = True

    def isClick(self):
        point_x, point_y = pygame.mouse.get_pos()
        x, y = self.position
        w, h = self.imageUp.get_size()

        in_x = x - w / 2 < point_x < x + w / 2
        in_y = y - h / 2 < point_y < y + h / 2
        return in_x and in_y

    def render(self, screen):
        w, h = self.imageUp.get_size()
        x, y = self.position
        if self.isClick():
            screen.blit(self.imageDown, (x - w / 2, y - h / 2))
            if self.button_out == True:
                # buttonmusic.play()
                self.button_out = False
        else:
            screen.blit(self.imageUp, (x - w / 2, y - h / 2))
            self.button_out = True


class Cars(object):
    def __init__(self, screen):
        self._screen = screen
        self.car1 = 'newcar1.png'
        self.car2 = 'newcar2.png'
        self.x1 = 120
        self.x2 = 220
        self.y = 450

    def draw(self):
        car1 = pygame.image.load(self.car1).convert_alpha()
        car2 = pygame.image.load(self.car2).convert_alpha()
        self._screen.blit(car1, (self.x1, self.y))
        self._screen.blit(car2, (self.x2, self.y))

    def move(self, new_dir):
        if new_dir == 1:
            if self.x1 == 120:
                self.x1 -= 100
        elif new_dir == 2:
            if self.x1 == 20:
                self.x1 += 100
        elif new_dir == 3:
            if self.x2 == 320:
                self.x2 -= 100
        elif new_dir == 4:
            if self.x2 == 220:
                self.x2 += 100


class Food(object):

    def __init__(self, screen, x1, y1, x2, y2):
        self.screen = screen
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.food1 = 'food1.png'
        self.food2 = 'food2.png'

    def draw(self):
        food1 = pygame.image.load(self.food1).convert_alpha()
        food2 = pygame.image.load(self.food2).convert_alpha()
        self.screen.blit(food1, (self.x1, self.y1))
        self.screen.blit(food2, (self.x2, self.y2))

    def move(self, score):
        if score <= 9:
            a = 1
        elif score < 20:
            a = 1.5
        elif score < 30:
            a = 2
        else:
            a = 2.5
        self.y1 += a
        self.y2 += a
        if self.y1 > 600:
            if randint(0, 100) > 50:
                if self.food2 == 'food2.png':
                    b = 'food2.png'
                    self.food1 = b
            else:
                self.food1 = 'food1.png'
            self.y1 = -50
            if randint(0, 100) > 50:
                self.x1 = 20
            else:
                self.x1 = 120
        if self.y2 > 600:
            if randint(0, 100) > 50:
                if self.food1 == 'food1.png':
                    b = 'food1.png'
                    self.food2 = b
            else:
                self.food2 = 'food2.png'
            self.y2 = -50
            if randint(0, 100) > 50:
                self.x2 = 220
            else:
                self.x2 = 320


def main():

    def refresh(num, score, myplay, myclick, numcount):
        screen.fill((162, 181, 205))
        pygame.draw.line(screen, Black, [100, 0], [100, 600])
        pygame.draw.line(screen, Black, [200, 0], [200, 600], 4)
        pygame.draw.line(screen, Black, [300, 0], [300, 600])
        if myplay:
            button.render(screen)
        car.draw()
        food1.draw()
        if myclick:
            food1.move(score)
            myplay = not myplay
            if num >= 200:
                food2.draw()
                food2.move(score)
        if score % 10 == 0 and score != 0 and numcount > 200:
            my_font = pygame.font.SysFont('楷体', 30)
            attention = my_font.render('Attention,Speed Up!', False, [255, 0, 0])
            screen.blit(attention, (100, 250))
            numcount = 0

        count_txt(score)
        pygame.display.flip()

    def handle_key_event(key_event):
        key = key_event.key
        if key == pygame.K_a:
            new_dir = LEFT
        elif key == pygame.K_d:
            new_dir = RIGHT
        elif key == pygame.K_LEFT:
            new_dir = LEFT2
        elif key == pygame.K_RIGHT:
            new_dir = RIGHT2
        else:
            new_dir = 0
        car.move(new_dir)

    def xy(x1, y1, n=1):
        x1 = int(x1)

        x2 = int(x1 + 60)

        y1 = int(y1)
        if n == 1:
            y2 = int(y1 + 100)
        if n == 2:
            y2 = int(y1 + 60)
        return (range(x1, x2 + 1), range(y1, y2 + 1))

    def is_cross(a, b):
        for each in a:
            if each in b:
                return True
        return False

    def mylisy(list1):
        f = []
        for x in list1:
            f.append(x)
        return f

    def myscore():
        if (food1.food1 == 'food1.png') and \
            ((is_cross(list_car1X, list_food11X) and
                is_cross(list_car1Y, list_food11Y))):
                food1.y1 += 600
                return 1

        # if (food1.food2 == 'food1.png') and \
        #         ((is_cross(list_car1X, list_food11X) and
        #           is_cross(list_car1Y, list_food11Y))) :
        #         food1.y1 += 600
        #         return 1
        if (food1.food2 == 'food1.png') and \
                ((is_cross(list_car2X, list_food12X) and
                  is_cross(list_car2Y, list_food12Y))):
                food1.y2 += 600
                return 1

        if (food2.food1 == 'food1.png') and \
                ((is_cross(list_car1X, list_food21X) and
                  is_cross(list_car1Y, list_food21Y))):
                food2.y1 += 600
                return 1

        # if (food2.food2 == 'food1.png') and \
        #         ((is_cross(list_car1X, list_food21X) and
        #           is_cross(list_car1Y, list_food21Y))):
        #         food2.y1 += 600
        #         return 1
        if (food2.food2 == 'food1.png') and \
                ((is_cross(list_car2X, list_food22X) and
                  is_cross(list_car2Y, list_food22Y))):
                food2.y2 += 600
                return 1
        return 0

    def count_txt(score):
        my_font = pygame.font.SysFont('楷体', 30)
        score = my_font.render('score:' + str(score), False, [255, 0, 0])
        screen.blit(score, (315, 0))

    def game_over():
        if (food1.food1 == 'food2.png') and \
                ((is_cross(list_car1X, list_food11X) and
                  is_cross(list_car1Y, list_food11Y))):
            return 1

        if (food1.food2 == 'food2.png') and \
                ((is_cross(list_car2X, list_food12X) and
                  is_cross(list_car2Y, list_food12Y))):
            return 1

        if (food2.food1 == 'food2.png') and \
                ((is_cross(list_car1X, list_food21X) and
                is_cross(list_car1Y, list_food21Y))) :
            return 1

        if (food2.food2 == 'food2.png') and \
                ((is_cross(list_car2X, list_food22X) and
                is_cross(list_car2Y, list_food22Y))):
            return 1

        if (food1.food1 == 'food1.png') and food1.y1 == 540:
            return 1
        if (food1.food2 == 'food1.png') and food1.y2 == 540:
            return 1
        if (food2.food1 == 'food1.png') and food2.y1 == 540:
            return 1
        if (food2.food2 == 'food1.png') and food2.y2 == 540:
            return 1
        return 0

    pygame.init()
    screen = pygame.display.set_mode((400, 600))
    pygame.display.set_caption('2_Cars')
    running = True
    car = Cars(screen)
    food1 = Food(screen,120,180,320,0)
    food2 = Food(screen,20,0,220,0)
    button = Button(Play1, Play2, (200, 300))
    # slid(screen)
    clock = pygame.time.Clock()
    pygame.display.flip()
    num = 0
    score = 0
    score_count = 0
    speed = 0
    myrun = True
    myplay = True
    myclick = False
    numcount = 0
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    myrun = not myrun
                if myclick:
                    handle_key_event(event)
        list_car1X, list_car1Y = xy(car.x1, car.y)
        list_car2X, list_car2Y = xy(car.x2, car.y)
        list_food11X, list_food11Y = xy(food1.x1, food1.y1, 2)
        list_food12X, list_food12Y = xy(food1.x2, food1.y2, 2)
        list_food21X, list_food21Y = xy(food2.x1, food2.y1, 2)
        list_food22X, list_food22Y = xy(food2.x2, food2.y2, 2)
        list_car1X = mylisy(list_car1X)
        list_car1Y = mylisy(list_car1Y)
        list_car2X = mylisy(list_car2X)
        list_car2X = mylisy(list_car2X)
        list_food11X = mylisy(list_food11X)
        list_food12X = mylisy(list_food12X)
        list_food11Y = mylisy(list_food11Y)
        list_food12Y = mylisy(list_food12Y)
        list_food21X = mylisy(list_food21X)
        list_food22X = mylisy(list_food22X)
        list_food21Y = mylisy(list_food21Y)
        list_food22Y = mylisy(list_food22Y)
        if -180 < food1.y1 - food2.y1 < 0:
            food1.y1 -= 180
        elif 0 <= food1.y1 - food2.y1 < 180:
            food2.y1 -= 180
        if -180 < food1.y2 - food2.y2 < 0:
            food1.y2 -= 180
        elif 0 <= food1.y2 - food2.y2 < 180:
            food2.y2 -= 180
        if -180 < food1.y1 - food1.y2 < 0:
            food1.y1 -= 180
        elif 0 <= food1.y1 - food1.y2 < 180:
            food1.y2 -= 180
        if -180 < food2.y1 - food2.y2 < 0:
            food2.y1 -= 180
        elif 0 <= food2.y1 - food2.y2 < 180:
            food2.y2 -= 180
        num += 1
        numcount += 1
        if myrun:
            refresh(num, score, myplay, myclick, numcount)
        if(event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and button.isClick()) or not myplay:
            myclick = True
            myplay = False
        if game_over():
            Yes_or_No = easygui.buttonbox("不好意思，游戏结束", choices=['我不服我还要玩', '我不玩了886'])
            if Yes_or_No == '我不服我还要玩':
                food1 = Food(screen, 120, 180, 320, 0)
                food2 = Food(screen, 20, 0, 220, 0)
                score = 0
            else:
                running = 0
        if myscore():
            score += 1
    pygame.quit()


if __name__ == '__main__':
    main()