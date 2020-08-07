import pygame
import pygame_menu
import random


# fereastra jocului
pygame.init()
win = pygame.display.set_mode((1000, 800))
pygame.display.set_caption("Ball Crusher")

player_img = pygame.image.load("platform.png")
player_img.convert()
ball_img = pygame.image.load("ball.png")
ball_img.convert()
brick_img = pygame.image.load("brick.png")
brick_img.convert()

# jucatorul
class Player:
    x = 450
    y = 770
    speed = 5
    width = 100
    height = 15
    rect = player_img.convert()
    def movement(self):
        events = pygame.event.get()
        key = pygame.key.get_pressed()
        if key[pygame.K_ESCAPE]:
            exit()
        if key[pygame.K_LEFT] or key[pygame.K_a]:
            self.x -= self.speed
            if self.x < 0:
                self.x = 0
        if key[pygame.K_RIGHT] or key[pygame.K_d]:
            self.x += self.speed
            if self.x > 900:
                self.x = 900

    def draw_player(self):
        win.blit(player_img, (self.x, self.y))
        #pygame.draw.rect(win, (0, 0, 255), (self.x, self.y, self.width, self.height))
    def player_colision(self,ball):
        if (ball.y >= self.y and ball.y <= self.y+5) and (ball.x <= self.x + 100 and ball.x >= self.x) and ball.move:
            ball.velocity[1] = -ball.velocity[1]

class Ball:
    width = 15
    height = 15
    velocity = [random.choice([-3, -2, -1, 1, 2, 3]), 3]
    angle = 0
    move = False
    press_space = False
    balls_left = 5
    def __init__(self,player):
        self.x = player.x + 45
        self.y = player.y - 15

    def draw_ball(self):
        win.blit(ball_img, (self.x, self.y))
       # pygame.draw.rect(win, (0, 0, 255), (self.x, self.y, self.width, self.height))

    def ball_movement(self, player):
        key = pygame.key.get_pressed()
        if self.press_space == False:
            self.__init__(player)
        if key[pygame.K_SPACE]:
            self.press_space = True
        if self.press_space:
            self.x += self.velocity[0]
            self.y -= self.velocity[1]
            if self.x >= 1000:
                self.velocity[0] = -self.velocity[0]
                self.move = True
            if self.x <= 0:
                self.velocity[0] = -self.velocity[0]
                self.move = True
            if self.y > 800:
                self.press_space = False
                self.x = Player.x
                self.y = Player.y - 15
                self.balls_left -= 1
            if self.y < 0:
                self.velocity[1] = -self.velocity[1]
                self.move = True


class Brick:
    width = 80
    height = 20
    color = (0, 0, 255)
    crush = False
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def draw_brick(self):
        if self.crush == False:
            win.blit(brick_img,(self.x, self.y))
            #pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))
    def __del__(self):
        self.color = (0, 0, 0)


class Game:
    player = Player()
    ball = Ball(player)
    bricks = []
    def game_run(self, run):
        for j in range(5): # 5
            for i in range(10): # 10
                brick = Brick((i + 0.6) * 90, (j + 2.5) * 35)
                self.bricks.append(brick)

        while run:
            events = pygame.event.get()

            if menu.is_enabled():
                menu.update(events)
                menu.draw(win)

            font1 = pygame.font.SysFont('comicsansms', 30)
            img1 = font1.render('Balls left: ' + str(self.ball.balls_left), True, (255, 255, 255))

            win.fill((70, 70, 70))

            if self.all_bricks_crushed():
                font3 = pygame.font.SysFont('comicsansms', 60)
                img3 = font3.render('YOU WIN', True, (255, 255, 255))
                win.blit(img3, (350, 380))
            else:
                self.player.movement()
                self.ball_hit_brick()
                self.ball.ball_movement(self.player)
                self.player.player_colision(self.ball)


            if self.ball.balls_left == 0:
                font2 = pygame.font.SysFont('comicsansms', 60)
                img2 = font2.render('GAME OVER', True, (255, 255, 255))
                win.blit(img2, (350, 380))
            else:
                win.blit(img1, (15, 15))
                self.ball.draw_ball()



            for x in self.bricks:
                x.draw_brick()

            self.player.draw_player()

            pygame.display.update()



    def ball_hit_brick(self):
        for b in self.bricks:
            if (self.ball.x >= b.x + 0 and self.ball.x <= b.x+80) and (self.ball.y <= b.y+5 and self.ball.y>=b.y) and b.crush == False:
                self.ball.velocity[1] = -self.ball.velocity[1]
                b.crush = True
            if (self.ball.x >= b.x + 0 and self.ball.x <= b.x + 80) and (self.ball.y >= b.y + 15 and self.ball.y <=b.y+20) and b.crush == False:
                self.ball.velocity[1] = -self.ball.velocity[1]
                b.crush = True
            if (self.ball.y >= b.y and self.ball.y<=b.y+20) and (self.ball.x >= b.x+5 and self.ball.x<=b.x) and b.crush == False:
                self.ball.velocity[0] = -self.ball.velocity[0]
                b.crush = True
            if (self.ball.y >= b.y and self.ball.y<=b.y+20) and (self.ball.x >= b.x+75 and self.ball.x<=b.x+80) and b.crush == False:
                self.ball.velocity[0] = -self.ball.velocity[0]
                b.crush = True
            if b.crush:
                b.__del__()
                del b

    def all_bricks_crushed(self):
        ok = True
        for b in self.bricks:
            if b.crush == False:
                ok = False
        return ok

# actiunea jocului
def play_game(run):
    game = Game()
    game.game_run(run)



# inceperea jocului
def start_the_game():
    menu.clear()
    start = True
    play_game(start)

# definim tema meniului
mytheme = pygame_menu.themes.THEME_DEFAULT.copy()
mytheme.title_background_color = (0, 0, 0)
mytheme.widget_font = pygame_menu.font.FONT_8BIT
mytheme.title_bar_style = pygame_menu.widgets.MENUBAR_STYLE_NONE
mytheme.widget_shadow = True
mytheme.widget_shadow_color = (169, 169, 169)
mytheme.widget_font_size = 55


# creeam meniul jocului
menu = pygame_menu.Menu(800, 1000, '', theme=mytheme)

menu.add_text_input('', default='Name')
menu.add_button('Play', start_the_game)
menu.add_button('Quit', pygame_menu.events.EXIT)

menu.mainloop(win)








