import pygame

from core.constants import (
    ENEMY_COLOR,
    ENEMY_WIDTH,
    ENEMY_HEIGHT,
    ENEMY_SPEED,
)

class Enemy:
    def __init__(self, x: int, y: int) -> None:
        self.rect = pygame.Rect(
            x,
            y,
            ENEMY_WIDTH,
            ENEMY_HEIGHT
        )

        self.speed = ENEMY_SPEED

    def update(self) -> None:
        self.rect.x -= self.speed

    def draw(self, screen: pygame.Surface) -> None:
        pygame.draw.rect(
            screen,
            ENEMY_COLOR,
            self.rect,
            border_radius=8
        )
