import pygame
import math
from gym_tank.envs.Object import Tank

screen_width = 1200
screen_height = 800

class PyTank2D:
    def __init__(self, is_render = True):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        self.font = pygame.font.SysFont("Arial", 150)
        self.game_speed = 60

        self.my_tank = Tank(0, self.screen)
        self.enemy = Tank(1, self.screen)
        self.is_render = is_render
        self.prev_distance = 0
        self.cur_distance = 0

    def action(self, action):
        self.prev_distance = self.cur_distance

        speed = 10
        if action == 0:
            self.my_tank.position[0] -= speed
            if self.my_tank.position[0] < 30:
                self.my_tank.position[0] = 30
        elif action == 1:
            self.my_tank.position[0] += speed
            if self.my_tank.position[0] > 1170:
                self.my_tank.position[0] = 1170
        elif action == 2:
            self.my_tank.position[1] -= speed
            if self.my_tank.position[1] < 30:
                self.my_tank.position[1] = 30
        elif action == 3:
            self.my_tank.position[1] += speed
            if self.my_tank.position[1] > 770:
                self.my_tank.position[1] = 770

        self.my_tank.update_status(self.enemy)
        self.enemy.update_status(self.my_tank)
        
        if not self.my_tank.alive:
            text = self.font.render("Spotted", True, (100, 255, 0))
            text_rect = text.get_rect()
            text_rect.center = (600, 350)
            self.screen.blit(text, text_rect)
            pygame.display.flip()
            self.clock.tick(1)

        if not self.enemy.alive:
            text = self.font.render("Assasinated", True, (255, 0, 0))
            text_rect = text.get_rect()
            text_rect.center = (600, 400)
            self.screen.blit(text, text_rect)
            pygame.display.flip()
            self.clock.tick(1)

        self.cur_distance = get_distance(self.my_tank.position, self.enemy.position)

    def observe(self):
        # return dif_w, dif_h, e_angle
        dif_w = self.my_tank.grid[0] - self.enemy.grid[0]
        dif_h = self.my_tank.grid[1] - self.enemy.grid[1]
        e_angle = int((int(self.enemy.angle) - (int(self.enemy.angle) % 3)) / 3)
        return dif_w, dif_h, e_angle

    def evaluate(self):
        reward = -1
        if self.cur_distance < self.prev_distance:
            reward = 1
        if self.my_tank.alive == False:
            reward = -1000
        if self.enemy.alive == False:
            reward = 1000
        return reward

    def is_done(self):
        if not self.enemy.alive or not self.my_tank.alive:
            self.enemy.alive = True
            self.my_tank.alive = True
            return True
        return False

    def view(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.display.quit()
                pygame.quit()
                return True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_PAGEUP:
                    self.game_speed += 30
                elif event.key == pygame.K_PAGEDOWN:
                    self.game_speed -= 30
                if self.game_speed < 0:
                    self.game_speed = 0
                elif self.game_speed > 150:
                    self.game_speed = 150

        self.screen.fill((255, 255, 255))
        self.my_tank.draw()
        self.enemy.draw()

        self.draw_grid()

        pygame.display.flip()
        self.clock.tick(self.game_speed)

    def draw_grid(self):
        len = 100
        for w in range(int(screen_width / len)):
            pygame.draw.line(self.screen, (0, 0, 0), (w * len, 0), (w * len, screen_height))

        for h in range(int(screen_height / len)):
            pygame.draw.line(self.screen, (0, 0, 0), (0, h * len), (screen_width, h * len))

        #draw rectangle
        m_pos = self.my_tank.position
        m_rect = [m_pos[0] - (m_pos[0] % 100), m_pos[1] - (m_pos[1] % 100), 100, 100]
        pygame.draw.rect(self.screen, (0, 0, 255), m_rect, 3)

        e_pos = self.enemy.position
        e_rect = [e_pos[0] - (e_pos[0] % 100), e_pos[1] - (e_pos[1] % 100), 100, 100]
        pygame.draw.rect(self.screen, (255, 0, 0), e_rect, 3)

#util
def get_distance(p1, p2):
	return math.sqrt(math.pow((p1[0] - p2[0]), 2) + math.pow((p1[1] - p2[1]), 2))
