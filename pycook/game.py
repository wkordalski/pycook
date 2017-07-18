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
        self.static_objects = []
        self.floor = []
        self.ceiling = []
        self.overlays = []
        self.traps = []
        self.level = level
        self.logic_thread = threading.Thread(target=level.start, args=(self,))
        self.draw_collisions = False

    def loop(self):
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

                for trap in self.traps:
                    trap.start_visiting()
                    for obj in self.objects:
                        trap.visit(obj)
                    trap.end_visiting()
                
                self.floor = sorted(self.floor)
                for (height, obj) in self.floor:
                    obj.draw(self)

                for obj in self.static_objects:
                    obj.draw(self)

                for obj in self.objects:
                    obj.draw(self)

                self.ceiling = sorted(self.ceiling)
                for (height, obj) in self.ceiling:
                    obj.draw(self)

                self.overlays = sorted(self.overlays)
                for (height, obj) in self.overlays:
                    obj.draw(self)

                if self.draw_collisions:
                    for obj in self.static_objects:
                        obj.collision.draw(self.screen, (255, 0, 0), 2)
                    for obj in self.objects:
                        obj.collision.draw(self.screen, (0, 255, 0), 2)
                
                pygame.display.flip()
                duration = self.clock.tick(60)
        finally:
            self.level.kill()
            self.logic_thread.join()
