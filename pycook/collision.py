from math import cos, sin, radians
import pygame


class Entity:
    pass


class Rectangle(Entity):
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def move(self, x, y):
        return Rectangle(self.x + x, self.y + y, self.w, self.h)

    def draw(self, surface, color, width=0):
        pygame.draw.rect(
            surface, color,
            pygame.Rect(int(self.x), int(self.y), int(self.w), int(self.h)),
            width
        )


class Circle(Entity):
    def __init__(self, x, y, r):
        self.x = x
        self.y = y
        self.r = r
    
    def move(self, x, y):
        return Circle(self.x + x, self.y + y, self.r)

    def draw(self, surface, color, width=0):
        pygame.draw.circle(
            surface, color, (int(self.x), int(self.y)), self.r, width
        )


class Polygon(Entity):
    def __init__(self, points):
        self.points = points
    
    def move(self, x, y):
        return Polygon([(xx + x, yy + y) for (xx, yy) in self.points])

    def rotate(self, angle, origin=(0, 0)):
        return Polygon(rotate_points(self.points, origin, angle))

    def draw(self, surface, color, width=0):
        pygame.draw.polygon(
            surface, color,
            list(map(lambda p: (int(p[0]), int(p[1])), self.points)),
            width)


def contains(a, b):
    if isinstance(a, Rectangle):
        if isinstance(b, Rectangle):
            return (
                a.x <= b.x <= b.x + b.w <= a.x + a.w and
                a.y <= b.y <= b.y + b.h <= a.y + a.h
            )
        elif isinstance(b, Circle):
            return (
                a.x <= b.x - b.r <= b.x + b.r <= a.x + a.w and
                a.y <= b.y - b.r <= b.y + b.r <= a.y + a.h
            )
        elif isinstance(b, Polygon):
            return all(
                a.x <= x <= a.x + a.w and a.y <= y <= a.y + a.h
                for (x, y) in b.points
            )

    raise NotImplementedError


def rotate_points(points, origin, angle):
    a = -radians(angle)
    orgpts = map(lambda p: (p[0] - origin[0], p[1] - origin[1]), points)
    rpts = map(
        lambda p: (p[0]*cos(a) - p[1]*sin(a), p[0]*sin(a) + p[1]*cos(a)),
        orgpts
    )
    return list(map(lambda p: (p[0] + origin[0], p[1] + origin[1]), rpts))