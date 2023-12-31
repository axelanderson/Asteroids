import abc
import math
import pygame
import random
import sys
import time

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
    def __init__(self, size, player):
        pygame.init()
        self.running = True
        self.screen = pygame.display.set_mode(size)
        self.clock = pygame.time.Clock()
        self.player = player
        self.background_color_win = (YELLOW)
        #self.background_color = ("red")
        self.background_color_game = (0, 0, 0)
        #self.win = False
        #self.win_time = 0

    def game_loop(self):
        while self.running:
            self.background_type = self.background_color_game
            # I wanted to make the background yellow when you win.

            if player not in sprites:
                sys.exit(0)

            # If no more asteroids, you win!
            has_asteroid = False
            for sprite in sprites:
                if type(sprite) == Asteroid:
                    has_asteroid = True
                    break
            if not has_asteroid:
                make_asteroids(5)

            collisions = []
            for i in range(len(sprites)):
                sprite1 = sprites[i]
                for j in range(i+1, len(sprites)):
                    sprite2 = sprites[j]
                    if sprite1 != sprite2:
                        if self.collision_check(sprite1, sprite2):
                            collisions.append(sprite1)
                            collisions.append(sprite2)

            # Remove any sprites that had a collision
            for i in range(len(sprites) - 1, -1, -1):
                if sprites[i] in collisions:
                    sprites.pop(i)


            events = pygame.event.get()

            for event in events:
                if event.type == pygame.QUIT:
                    self.running = False
                  
            # Refresh the screen
            self.screen.fill(self.background_type)
            self.player.handle_events()

            # Get rid of bullets that have travelled too far
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
        is_both_asteroids = type(entity1) == Asteroid and type(entity2) == Asteroid

        if is_player_or_bullet_1 and is_player_or_bullet_2 or is_both_asteroids:
            return False

        d = math.sqrt((entity1.x - entity2.x)**2 + (entity1.y - entity2.y)**2)

        return d - entity1.radius - entity2.radius < 0


class Sprite(abc.ABC):

    @abc.abstractmethod
    def draw(self):
        pass


class Asteroid(Sprite):
    
    def __init__(self):
        self.x = random.randint(0, MAX_SIZE_X)
        self.y = 0
        self.size = random.randint(25, 50)
        self.radius = self.size // 2

        # Generate a random number of points and their relative positions for the asteroid
        self.num_points = 8
        #self.num_points = random.randint(350, 500)
        self.relative_coords = [((math.cos(2 * math.pi / self.num_points * i) * self.size) + random.randint(-10, 10),
                        (math.sin(2 * math.pi / self.num_points * i) * self.size) + random.randint(-10, 10)) for i in range(self.num_points)]
        
        # Velocity
        self.vel_x = random.randint(-4, 4)
        self.vel_y = random.randint(-4, 4)

        while self.vel_x == 0 and self.vel_y == 0:
            self.vel_x = random.randint(-4, 4)
            self.vel_y = random.randint(-4, 4)

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
        self.size = 50
        self.radius = self.size // 2

        self.shoot_speed = 0.2
        self.time_last_shot = self.shoot_speed

        self.x = x
        self.y = y - self.radius

        # In radians
        self.direction = 0
        self.direction_change_speed = 0.2

        self.speed = 5

    def turn_left(self):
        self.x = self.x - self.speed
        if self.x < -50:
            self.x = MAX_SIZE_X 
        self.direction -= self.direction_change_speed

    def turn_right(self):
        self.x = self.x + self.speed 
        if self.x > MAX_SIZE_X:
            self.x = -50
        self.direction += self.direction_change_speed

    def up(self):
        self.y = self.y - self.speed
        if self.y < -50:
            self.y = MAX_SIZE_Y

    def down(self):
        self.y = self.y + self.speed
        if self.y > MAX_SIZE_Y:
            self.y = -50

    def shoot(self):
        shoot_now = time.time()
        if shoot_now - self.time_last_shot < self.shoot_speed:
            return

        self.time_last_shot = shoot_now

        bullet = Bullet(self.y, self.x)
        sprites.append(bullet)

    def handle_events(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.turn_left()
        if keys[pygame.K_d]:
            self.turn_right()
        if keys[pygame.K_w]:
            self.up()
        if keys[pygame.K_s]:
            self.down()
        if keys[pygame.K_SPACE]:
            self.shoot()

    def draw(self, window):
        pygame.draw.polygon(window, RED, [(self.x - self.radius, self.y), (self.x + self.radius, self.y), (self.x, self.y - self.size)], 0)


class Bullet(Sprite):
    def __init__(self, y, x):
       self.speed = 10
       self.size = 10
       self.radius = self.size // 2

       self.start_x = x
       self.start_y = y

       self.x = x
       self.y = y

       self.travel_range = MAX_SIZE_Y

    def travel_distance(self):
        ''' Returns the distance the bullet has travelled '''
        return math.sqrt((self.start_x - self.x)**2 + (self.start_y - self.y)**2)

    def draw(self, window):
        self.y = self.y - self.speed
        pygame.draw.circle(window, BLUE, (self.x, self.y), self.radius)
    
def make_asteroids(num_asteroids):
    for i in range(num_asteroids):
        asteroid = Asteroid()
        sprites.append(asteroid)


if __name__ == "__main__":
    size = (MAX_SIZE_X, MAX_SIZE_Y)
    position = (size[0] / 2, size[1] / 2)
    # size[1] == 480, meaning bottom of the screen
    player = Player(position[0], position[1])
    sprites.append(player)

    game = Game(size, player)
    game.game_loop()
