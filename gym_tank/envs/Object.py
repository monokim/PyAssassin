import random
import math
import pygame

screen_width = 1200
screen_height = 800

class Tank:
    size = 30
    alive = True
    def __init__(self, side, screen):
        self.screen = screen
        self.side = side
        self.c_len = 300
        if side == 0:
            self.position = [screen_width - 100, screen_height - 100]
            #self.position = [random.randrange(50, screen_width - 50), random.randrange(50, screen_height - 50)]
            self.color = (0, 0, 255)
        else:
            self.position = [350, 250]
            #self.position = [random.randrange(50, screen_width - 50), random.randrange(50, screen_height - 50)]
            self.color = (255, 0, 0)

        self.grid = get_grid(self.position)
        self.angle = 0

    def draw(self):
        pygame.draw.circle(self.screen, self.color, [int(self.position[0]), int(self.position[1])], self.size)
        if self.side == 1:
            t_x = self.position[0] + math.cos(math.radians(self.angle - 5)) * self.c_len
            t_y = self.position[1] - math.sin(math.radians(self.angle - 5)) * self.c_len
            pygame.draw.line(self.screen, (10, 150, 10), (self.position[0], self.position[1]), (t_x, t_y), 5)
            t_x = self.position[0] + math.cos(math.radians(self.angle + 5)) * self.c_len
            t_y = self.position[1] - math.sin(math.radians(self.angle + 5)) * self.c_len
            pygame.draw.line(self.screen, (10, 150, 10), (self.position[0], self.position[1]), (t_x, t_y), 5)

    def update_status(self, enemy = None):
        self.angle -= 3
        self.angle = (self.angle + 360) % 360
        if self.side == 0:
            self.is_found(enemy)
        if self.side == 1:
            self.is_hit(enemy)
        self.grid = get_grid(self.position)

    def is_hit(self, enemy):
        if get_grid(enemy.position) == self.grid:
            self.alive = False

    def is_found(self, enemy):
        angle = get_angle(enemy.position, self.position)
        distance = get_distance(enemy.position, self.position)
        #print(angle, self.angle)
        if abs(angle - self.angle) <= 10 and distance <= self.c_len:
            self.alive = False

#util
def get_grid(position):
    return [int(position[0] / 100), int(position[1] / 100)]

def get_angle(p1, p2):
	return (math.degrees(math.atan2(p1[1] - p2[1], p2[0] - p1[0])) + 360) % 360

def get_distance(p1, p2):
	return math.sqrt(math.pow((p1[0] - p2[0]), 2) + math.pow((p1[1] - p2[1]), 2))
