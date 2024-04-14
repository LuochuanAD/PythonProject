import sys
import pygame
import random
from pygame.locals import *
class SnakeGameConf():
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 800
    FPS = 3
    BG_COLOR = (255, 255, 255)
    SNAKE_COLOR = (0, 255, 255)
    SNAKE_BODY = [[100,100],[80, 100],[60,100],[40,100],[20,100]]
    FOOD_COlOR = (255, 0, 0)
    FOOD_SIZE = 20
    FOOD_POSITION = [300, 300]
    SCORE = 0
    FOOD_TOTAL = 1
    BUTTON_RECT = pygame.Rect(300,SCREEN_HEIGHT/2+100,200,50)
class Snake(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.curDirection = pygame.K_RIGHT
        self.body = SnakeGameConf.SNAKE_BODY[:]
    def drawSnake(self,body,Screen):
        for i in body:
            pygame.draw.rect(Screen, SnakeGameConf.SNAKE_COLOR, Rect(i[0],i[1], SnakeGameConf.FOOD_SIZE,SnakeGameConf.FOOD_SIZE))
    def changeDirection(self, direction):
        LR = [pygame.K_LEFT, pygame.K_RIGHT]
        UD = [pygame.K_UP, pygame.K_DOWN]
        if direction in LR + UD:
            if direction in LR and self.curDirection in LR:
                return
            if direction in UD and self.curDirection in UD:
                return
            self.curDirection = direction
    def addNode(self):
        left, top = [0,0]
        if self.body:
            left = self.body[0][0]
            top = self.body[0][1]

        if self.curDirection == pygame.K_LEFT:
            left -= SnakeGameConf.FOOD_SIZE
        elif self.curDirection == pygame.K_RIGHT:
            left += SnakeGameConf.FOOD_SIZE
        elif self.curDirection == pygame.K_UP:
            top -= SnakeGameConf.FOOD_SIZE
        elif self.curDirection == pygame.K_DOWN:
            top += SnakeGameConf.FOOD_SIZE

        self.body.insert(0, [left, top])
    def deleteNode(self):
        self.body.pop()
    def snakeMove(self):
        self.addNode()
        self.deleteNode()
    def isDead(self):
        # 贪吃蛇碰到四周边界,或自己身体,死
        if self.body[0][0] > SnakeGameConf.SCREEN_WIDTH or self.body[0][0] < 0 or self.body[0][1] > SnakeGameConf.SCREEN_HEIGHT or self.body[0][1] < 0:
            return True
        for i in range(len(self.body)):
            if self.body[0][0] == self.body[i][0] and self.body[0][1] == self.body[i][1]:
                if i !=0: return True

        return False
class Food(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.rect = pygame.Rect(SnakeGameConf.FOOD_POSITION[0], SnakeGameConf.FOOD_POSITION[1], SnakeGameConf.FOOD_SIZE, SnakeGameConf.FOOD_SIZE)
    def drawFood(self,foodLocation,Screen):
        pygame.draw.rect(Screen, SnakeGameConf.FOOD_COlOR,Rect(foodLocation[0], foodLocation[1],SnakeGameConf.FOOD_SIZE,SnakeGameConf.FOOD_SIZE))
    def removeFood(self):
        self.rect.x = -SnakeGameConf.FOOD_SIZE
    def set(self,snakeLocation):
        if self.rect.x == -SnakeGameConf.FOOD_SIZE:
            allpos = []
            for pos in range(SnakeGameConf.FOOD_SIZE, SnakeGameConf.SCREEN_WIDTH - SnakeGameConf.FOOD_SIZE, SnakeGameConf.FOOD_SIZE):
                allpos.append(pos)
            self.rect.left = random.choice(allpos)
            self.rect.top = random.choice(allpos)
            while (self.rect.left,self.rect.top) in snakeLocation:
                self.rect.left = random.choice(allpos)
                self.rect.top = random.choice(allpos)

            SnakeGameConf.FOOD_POSITION = [self.rect.left, self.rect.top]
class UISettings():
    def show_text(self, screen, pos, text, color, font_bold = False, font_size = 60, font_italic = False):
        cur_font = pygame.font.SysFont('宋体', font_size)
        cur_font.set_bold(font_bold)
        cur_font.set_italic(font_italic)
        text_fmt = cur_font.render(text, 1, color)
        screen.blit(text_fmt, pos)
    def shaw_button(self, screen,rect, button_color, text,text_color,text_font):
        text = pygame.font.Font(None,text_font).render(text,True,text_color)
        text_rect = text.get_rect(center=rect.center)
        pygame.draw.rect(screen,button_color,rect)
        screen.blit(text,text_rect)
def main():
    pygame.init()
    pygame.display.set_caption('Snake Game')
    screen = pygame.display.set_mode((SnakeGameConf.SCREEN_WIDTH, SnakeGameConf.SCREEN_HEIGHT))
    uisettings = UISettings()
    snakeconf = SnakeGameConf()
    snake = Snake()
    food = Food()
    snake.drawSnake(snake.body,screen)
    food.drawFood(snakeconf.FOOD_POSITION, screen)
    clock = pygame.time.Clock()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                snake.changeDirection(event.key)
            if event.type == MOUSEBUTTONDOWN:
                if snakeconf.BUTTON_RECT.collidepoint(pygame.mouse.get_pos()):
                    '''重新开始,重置默认参数'''
                    snake.curDirection = pygame.K_RIGHT
                    snake.body = snakeconf.SNAKE_BODY[:]
                    snakeconf.SCORE = 0
                    snakeconf.FOOD_TOTAL = 0
                    snakeconf.FPS = 3
        screen.fill(snakeconf.BG_COLOR)
        if snake.isDead():
            uisettings.show_text(screen,[200,SnakeGameConf.SCREEN_HEIGHT/2],'Game Over!', 'red',True,100,True)
            uisettings.shaw_button(screen,snakeconf.BUTTON_RECT,'green','again','white',30)
        else:
            snake.snakeMove()
            snakeconf.SCORE += 1
            snake.drawSnake(snake.body, screen)
        '''判断是否吃到食物'''
        if snake.body[0] == snakeconf.FOOD_POSITION:
            food.removeFood()
            snake.addNode()
            food.set(snake.body)
            snakeconf.SCORE += 50
            snakeconf.FOOD_TOTAL += 1
            snakeconf.FPS += 3
        food.drawFood(food.rect, screen)
        uisettings.show_text(screen,[20,SnakeGameConf.SCREEN_HEIGHT-50],'Level: '+ str(snakeconf.FOOD_TOTAL) +'  Scors: '+str(snakeconf.SCORE), 'pink',True,50,True)
        pygame.display.update()
        clock.tick(snakeconf.FPS)

if __name__ == '__main__': main()
