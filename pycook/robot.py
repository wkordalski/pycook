import math
import pygame


class Robot:
    def __init__(self, position):
        self.x = position[0]
        self.y = position[1]
        self.r = 00
        self.tm = None
        self.tr = None
        self.vm = 0.15
        self.vr = 0.2
        self.target_reach = None
        self.image = pygame.image.load('images/ball.png')

    def draw(self, game):
        rimg = pygame.transform.rotate(self.image, self.r)
        size = rimg.get_rect().size
        game.screen.blit(rimg, (self.x - size[0]/2, self.y - size[1]/2))

    def physics(self, game, duration):
        def treach():
            tr = self.target_reach
            if tr is not None:
                self.target_reach = None
                tr()

        if self.tr is not None:
            if abs(self.tr) < self.vr * duration:
                self.r += self.tr
                self.tr = None
                treach()
            else:
                dr = self.tr / abs(self.tr) * self.vr * duration
                self.r += dr
                self.tr -= dr
                if self.r >= 360:
                    self.r -= 360
                if self.r < 0:
                    self.r += 360

        if self.tm is not None:
            if self.tm < self.vm * duration:
                self.x -= self.tm * math.sin(self.r * math.pi / 180)
                self.y -= self.tm * math.cos(self.r * math.pi / 180)
                self.tm = None
                treach()
            else:
                dst = self.vm * duration
                self.x -= dst * math.sin(self.r * math.pi / 180)
                self.y -= dst * math.cos(self.r * math.pi / 180)
                self.tm -= dst

    def rotate(self, angle):
        import pycook.sleep

        if angle > 360:
            angle = angle % 360

        if angle < -360:
            angle = - (abs(angle) % 360)

        def setter(trigger):
            self.tr = angle
            self.target_reach = trigger
        pycook.sleep.wait_for_signal(setter)

    def forward(self, distance):
        import pycook.sleep

        def setter(trigger):
            self.tm = distance
            self.target_reach = trigger
        pycook.sleep.wait_for_signal(setter)