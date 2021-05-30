import numpy as np
import pygame
from math import sqrt, pow
from scipy.constants import pi

G = -0.05


class Board:
    def __init__(self, width=600, height=400,  caption='Planets in space'):
        self.__caption = caption
        self.__width = width
        self.__height = height
        self.__size = width, height
        self.Green = (0, 255, 0)
        self.Red = (255, 0, 0)
        self.Yellow = (255, 255, 0)
        self.Black = (0, 0, 0)

        pygame.init()
        self.screen = pygame.display.set_mode(self.__size)
        pygame.display.set_caption(self.__caption)

        self.__running = None

    def set_up(self):
        self.__running = True

    def terminate(self):
        self.__running = False

    def is_running(self):
        return self.__running

    def draw(self, body):
        if isinstance(body, Planet):
            pygame.draw.circle(self.screen, body.color, body.position, body.R)
        else:
            pygame.draw.circle(self.screen, self.Red, body.position, body.R)

    def fill(self, been_there):
        self.screen.fill(self.Black)
        for dot in been_there:
            dot = round(dot[0]), round(dot[1])
            self.screen.set_at(dot, self.Yellow)


class Star:
    def __init__(self, mass, x, y):
        self.mass = mass
        self.X = x
        self.Y = y
        self.position = np.array([x, y], dtype=float)
        self.R = self._get_radius()

    def _get_radius(self):
        """
        getting the radius by the mass per density distribution
        assuming the density to all bodies is 1
        V=(4πr3)/3
        """
        return (3 * pi * self.mass / 4)**(1/3)


class Planet(Star):
    """My basic unit of time is 1"""
    def __init__(self, mass, x, y, v):
        super().__init__(mass, x, y)
        self.V = v
        self.color = tuple(np.random.randint(180, 250, size=3))

    def distance_from(self, other):
        """Pythagoras' theorem"""
        return sqrt(pow(self.X - other.X, 2) + pow(self.Y - other.Y, 2))

    def force_scalar_by(self, other):
        """neuton'ss laws of gravity"""
        try:
            return G * (self.mass * other.mass) / pow(self.distance_from(other), 2)
        except ZeroDivisionError:
            return np.zeros(2)

    def get_unit_vector_to(self, other):
        """vector divided by it's magnitude"""
        return np.true_divide(np.subtract(self.position, other.position), self.distance_from(other))

    def get_force(self, other):
        """scalar by vector"""
        return self.get_unit_vector_to(other) * self.force_scalar_by(other)

    def get_acceleration(self, force):
        """neuton's second law"""
        return np.true_divide(force, self.mass)

    def change_speed(self, combined_forces):
        """change speed by acceleration"""
        self.V = np.add(self.V, self.get_acceleration(combined_forces))

    def change_position(self):
        """change position by speed"""
        self.position += self.V



