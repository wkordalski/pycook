# here will be main loop that is running in separate thread
import pygame
import threading


class Game:
    def __init__(self, level):
        """
        Runs separate thread with Stackless.

        It initializes objects, create tasklets and channels, run scheduler.
        """
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        self.clock = pygame.time.Clock()
        self.exit = False
        self.objects = []
        self.level = level
        self.logic_thread = threading.Thread(target=level.start, args=(self,))

    def loop(self):
        #is_blue = True
        self.logic_thread.start()
        duration = 1
        try:
            while not self.exit:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.exit = True

                self.screen.fill((0, 0, 0))
                for obj in self.objects:
                    obj.physics(self, duration)
                for obj in self.objects:
                    obj.draw(self)
                # if is_blue:
                #     color = (0, 128, 255)
                # else:
                #     color = (255, 100, 0)
                # pygame.draw.rect(self.screen, color, pygame.Rect(30, 30, 60, 60))
                pygame.display.flip()
                duration = self.clock.tick(60)
        finally:
            self.level.kill()
            self.logic_thread.join()
