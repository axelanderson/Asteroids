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
            # I wanted to make the background yellow when you win.
            for sprite1 in sprites:
                for sprite2 in sprites:
                    if sprite1 != sprite2:
                        if self.collision_check(sprite1, sprite2):
                            sys.exit(0)

            events = pygame.event.get()

            for event in events:
                if event.type == pygame.QUIT:
                    self.running = False
                  
            # Refresh the screen
            self.screen.fill(self.background_type)
            self.player.handle_events()


            for i in range(len(sprites) - 1, -1, -1):
                if type(sprites[i]) == Bullet:
                    if sprites[i].travel_distance() > sprites[i].travel_range:
                        sprites.pop(i)
                        continue
                sprites[i].draw(self.screen)

            pygame.display.flip()

            self.clock.tick(60)

        pygame.quit()

    def collision_check(self, entity1, entity2):
        is_player_or_bullet_1 = type(entity1) == Player or type(entity1) == Bullet
        is_player_or_bullet_2 = type(entity2) == Player or type(entity2) == Bullet

        if is_player_or_bullet_1 and is_player_or_bullet_2:
            return False

        x_collision = False
        if (entity1.x >= entity2.x and entity1.x <= entity2.x + entity2.size) or (entity1.x + entity1.size >= entity2.x and entity2.x and entity1.x + entity1.size <= entity2.x + entity2.size):
            x_collision = True

        y_collision = False
        if (entity1.y >= entity2.y and entity1.y <= entity2.y + entity2.size) or (entity1.y + entity1.size>= entity2.y and entity2.y and entity1.y + entity1.size <= entity2.y + entity2.size):
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
        self.x = random.randint(0, MAX_SIZE_X)
        self.y = 0
        self.size = random.randint(25, 50)
        self.radius = self.size // 2

        # Generate a random number of points and their relative positions for the asteroid
        self.num_points = random.randint(5, 10)
        self.relative_coords = [((math.cos(2 * math.pi / self.num_points * i) * self.size) + random.randint(-10, 10),
                        (math.sin(2 * math.pi / self.num_points * i) * self.size) + random.randint(-10, 10)) for i in range(self.num_points)]
        
        # Velocity
        self.vel_x = random.randint(1, 3)
        self.vel_y = random.randint(3, 3)

    def move(self):
        self.x += self.vel_x
        self.y += self.vel_y

        # Wrap the asteroid around if it goes off the screen
        if self.x < 0: self.x = MAX_SIZE_X
        if self.x > MAX_SIZE_X: self.x = 0
        if self.y < 0: self.y = MAX_SIZE_Y
        if self.y > MAX_SIZE_Y: self.y = 0

    def get_absolute_coords(self):
        return [(self.x + dx, self.y + dy) for (dx, dy) in self.relative_coords]

    def draw(self, screen):
        # Get the actual positions
        self.move()
        pygame.draw.polygon(screen, GREEN, self.get_absolute_coords(), 1)


class Player(Sprite):
    def __init__(self, x, y):
        self.size = 100
        self.radius = 50

        self.x = x
        self.y = y - self.radius

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
        bullet = Bullet(self.y, self.x + self.radius / 2)
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
        pygame.draw.rect(window, RED, (self.x, self.y, self.radius, self.radius))


class Bullet(Sprite):
    def __init__(self, y, x):
       self.speed = 25
       self.radius = 5

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
        pygame.draw.rect(window, BLUE, (self.x, self.y, self.radius, self.radius))
    

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
