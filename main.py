import pygame
import random
import math
import sys


class Main:
    """main game class"""

    def __init__(self):
        # initialize pygame
        pygame.init()

        # set display, window size
        self.screen = pygame.display.set_mode((500, 500))
        self.rect = self.screen.get_rect()

        # set window title/name
        pygame.display.set_caption("Aim-Lab")

        # background color
        self.br_color = "#050103"
        # clock object to handle time related data and operations
        self.clock = pygame.time.Clock()

        # initialize score and timer label #
        self.score_label = TextLabel(0, 180, self.screen, self.rect)
        self.timer_label = TextLabel(30, 48, self.screen, self.rect, "top")

        # initialize manager #
        self.manager = Manager(self)
        self.manager.start_new_game()

    def run(self):
        """game loop"""
        while True:
            self.user_input()
            self.update()
            self.render()

            # ensure that loop is called 60 times every second
            self.clock.tick(60)

    def user_input(self):
        """event loop, checks for user's input"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                # start new game #
                self.manager.start_new_game()
            elif event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:
                # check if a ball was hit #
                self.manager.shoot(pygame.mouse.get_pos())

    def update(self):
        """updates game elements"""
        # countdown timer #
        self.manager.update_timer()

    def render(self):
        """render game elements on screen"""
        # fill window with background color
        self.screen.fill(self.br_color)

        # draw score and timer label on screen #
        self.score_label.render()
        self.timer_label.render()

        # draw balls on screen #
        self.manager.render_balls()

        # show most recent frame
        pygame.display.flip()


class TextLabel:
    """keeps track of and displays player's score"""

    def __init__(self, text, size, parent_surf, parent_rect, layout="center"):
        # parent's attributes
        self.parent_surf = parent_surf
        self.parent_rect = parent_rect

        # score label color and font
        self.color = "#332925"
        self.font = pygame.font.Font(None, size)

        # placeholders for score label surface and rect
        self.surf = None
        self.rect = None

        # text label layout
        self.layout = layout

        self.set_label(text)

    def set_label(self, text):
        """set text label surface and position it on the screen"""
        self.surf = self.font.render(str(text), True, self.color)
        self.rect = self.surf.get_rect()

        if self.layout == "center":
            self.rect.center = self.parent_rect.center
        elif self.layout == "top":
            self.rect.midtop = self.parent_rect.midtop
            # add margin
            self.rect.y += 10

    def render(self):
        """render text label to the screen"""
        self.parent_surf.blit(self.surf, self.rect)


class Ball:
    """target ball class"""

    def __init__(self, center, radius, parent_surf):
        # parent attributes
        self.parent_surf = parent_surf

        # ball's position and radius
        self.center = center
        self.radius = radius

        # ball's color
        self.color = "#d95338"

    def collide_point(self, point):
        """return true is point collided with ball"""
        # get the distance between point and ball
        x_diff = self.center[0] - point[0]
        y_diff = self.center[1] - point[1]
        distance = math.sqrt(x_diff*x_diff + y_diff*y_diff)

        if distance < self.radius:
            return True

        return False

    def render(self):
        """draw ball on screen"""
        pygame.draw.circle(self.parent_surf, self.color, self.center, self.radius)


class Manager:
    """manager target balls, score, and timer"""

    def __init__(self, main):
        # parent attributes
        self.main = main
        self.parent_surf = main.screen
        self.parent_rect = main.rect

        # score and timer
        self.score = 0
        self.timer = 30

        # target ball list
        self.balls = []
        self.game_active = False

    def start_new_game(self):
        """start a new game"""
        # reset score and timer
        self.score = 0
        self.timer = 30
        self.main.score_label.set_label(self.score)
        self.main.timer_label.set_label(self.timer)

        # reset target balls
        self.balls.clear()
        for _ in range(10):
            self.spawn_ball()

        # set game active
        self.game_active = True

    def spawn_ball(self):
        """add a new ball object to list of balls"""
        # get a random position for the target ball
        margin = 20
        center = (
            random.randint(margin, self.parent_rect.width-margin),
            random.randint(margin, self.parent_rect.height-margin)
        )
        # create and add new ball object to balls list
        new_ball = Ball(center, 15, self.parent_surf)
        self.balls.append(new_ball)

    def shoot(self, pos):
        """check if any ball was shit"""
        for index, ball in enumerate(self.balls):
            if ball.collide_point(pos):
                del self.balls[index]
                # increment score and add a new ball
                self.spawn_ball()
                self.add_point()
                return

    def add_point(self):
        """add one point to score"""
        self.score += 1
        self.main.score_label.set_label(self.score)

    def update_timer(self):
        """timer countdown"""
        if self.game_active:
            if self.timer > 0:
                time_passed = self.main.clock.get_time() / 1000
                self.timer -= time_passed
                self.main.timer_label.set_label(math.floor(self.timer))
            else:
                self.game_active = False
                self.balls.clear()
                self.main.timer_label.set_label("press 'space' to restart game")

    def render_balls(self):
        """draw target balls on the screen"""
        for ball in self.balls:
            ball.render()


Main().run()
