import abc
import math
import pygame
import random
import sys


print (":)")

sprites = []
# Colors
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

MAX_SIZE_X = 640
MAX_SIZE_Y = 480


class Game:
    def __init__(self, size, player, astroid1):
        pygame.init()
        self.running = True
        self.screen = pygame.display.set_mode(size)
        self.clock = pygame.time.Clock()
        self.player = player
        self.background_color_win = (YELLOW)
        #self.background_color = ("red")
        self.background_color_game = (0, 0, 0)
        self.astroid1 = astroid1
        #self.win = False
        #self.win_time = 0

    def game_loop(self):
        while self.running:
            self.background_type = self.background_color_game
            '''
            if self.win:
                self.win_time = self.win_time + 1
            if self.win_time == 10:
                self.win = False
                self.background_type = self.background_color_game
                '''
            for sprite1 in sprites:
                for sprite2 in sprites:
                    if sprite1 != sprite2:
                        if self.collision_check(sprite1, sprite2):
                            sys.exit(0)
                        '''
                            if sprite1 == Bullet and sprite2 == astroid1 or sprite1 == astroid1 and sprite2 == Bullet:
                                background_type = self.back_ground_color_win
                                self.win = True
                                self.win_time = 0
                                print("ummm")
                                '''

            events = pygame.event.get()

            for event in events:
                if event.type == pygame.QUIT:
                    self.running = False
                  
            # Refresh the screen
            self.screen.fill(self.background_type)
            self.player.handle_events()


            for i in range(len(sprites) - 1, -1, -1):
                if type(sprites[i]) == Bullet:
                    print(sprites[i].y)
                    if sprites[i].travel_distance() > sprites[i].travel_range:
                        sprites.pop(i)
                        continue
                sprites[i].draw(self.screen)

            print(len(sprites))
            pygame.display.flip()

            self.clock.tick(60)

        pygame.quit()

    def collision_check(self, entity1, entity2):
        is_player_or_bullet_1 = type(entity1) == Player or type(entity1) == Bullet
        is_player_or_bullet_2 = type(entity2) == Player or type(entity2) == Bullet

        if is_player_or_bullet_1 and is_player_or_bullet_2:
            return False

        x_collision = False
        if (entity1.x >= entity2.x and entity1.x <= entity2.x + entity2.size[0]) or (entity1.x + entity1.size[0] >= entity2.x and entity2.x and entity1.x + entity1.size[0] <= entity2.x + entity2.size[0]):
            x_collision = True

        y_collision = False
        if (entity1.y >= entity2.y and entity1.y <= entity2.y + entity2.size[1]) or (entity1.y + entity1.size[1]>= entity2.y and entity2.y and entity1.y + entity1.size[1] <= entity2.y + entity2.size[1]):
            y_collision = True

        if x_collision and y_collision:
            return True
        



class Sprite(abc.ABC):

    @abc.abstractmethod
    def draw(self):
        ''' Draws the cool sprite in a cool place doing cool things '''
        pass


class Astroid(Sprite):
    
    def __init__(self):
        self.size = (random.randint(25, 50), random.randint(25, 50))
        self.speed1 = random.randint(-5, 5)
        self.speed2 = random.randint(-5, 5)
        self.x = random.randint(0, MAX_SIZE_X)
        self.y = 0

    def move(self):
        self.y = self.y + self.speed1
        self.x = self.x + self.speed2
        if self.y < 0 - self.size[0]:
            self.y = MAX_SIZE_Y
        if self.y > MAX_SIZE_Y:
            self.y = 0 - self.size[0]
        if self.x > MAX_SIZE_X:
            self.x = 0 - self.size[0]
        if self.x < 0 - self.size[0]:
            self.x = MAX_SIZE_X

    def draw(self, window):
        self.move()
        pygame.draw.rect(window, GREEN, (self.x, self.y, self.size[1], self.size[0]))


class Player(Sprite):
    def __init__(self, x, y):
        self.width = 50
        self.height = 50
        self.size = (self.height, self.width)

        self.x = x
        self.y = y - self.height

        self.speed = 5

    def left(self):
        self.x = self.x - self.speed
        if self.x < -50:
            self.x = MAX_SIZE_X 

    def right(self):
        self.x = self.x + self.speed 
        if self.x > MAX_SIZE_X:
            self.x = -50
    def up(self):
        self.y = self.y - self.speed
        if self.y < -50:
            self.y = MAX_SIZE_Y

    def down(self):
        self.y = self.y + self.speed
        if self.y > MAX_SIZE_Y:
            self.y = -50

    def shoot(self):
        bullet = Bullet(self.y, self.x + self.width / 2)
        sprites.append(bullet)

    def handle_events(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.left()
        if keys[pygame.K_d]:
            self.right()
        if keys[pygame.K_w]:
            self.up()
        if keys[pygame.K_s]:
            self.down()
        if keys[pygame.K_SPACE]:
            self.shoot()

    def draw(self, window):
        pygame.draw.rect(window, RED, (self.x, self.y, self.width, self.height))


class Bullet(Sprite):
    def __init__(self, y, x):
       self.speed = 25
       self.size = (5, 50)

       self.start_x = x
       self.start_y = y

       self.x = x
       self.y = y

       self.travel_range = 250

    def travel_distance(self):
        ''' Returns the distance the bullet has travelled '''
        return math.sqrt((self.start_x - self.x)**2 + (self.start_y - self.y)**2)

    def draw(self, window):
        self.y = self.y - self.speed
        pygame.draw.rect(window, BLUE, (self.x, self.y, self.size[0], self.size[1]))
    

if __name__ == "__main__":
    size = (MAX_SIZE_X, MAX_SIZE_Y)
    position = (size[0] / 2, size[1] / 2)
    # size[1] == 480, meaning bottom of the screen
    player = Player(position[0], position[1])
    sprites.append(player)
    astroid1 = Astroid()
    sprites.append(astroid1)
    game = Game(size, player, astroid1)
    game.game_loop()
