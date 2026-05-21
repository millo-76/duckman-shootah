import pygame

from core.constants import (
    PROJECTILE_COLOR,
    PROJECTILE_WIDTH,
    PROJECTILE_HEIGHT,
    PROJECTILE_SPEED,
    WIDTH,
)

class Projectile:
    def __init__(self, x: int, y: int) -> None:
        self.rect = pygame.Rect(
            x,
            y,
            PROJECTILE_WIDTH,
            PROJECTILE_HEIGHT
        )

        self.speed = PROJECTILE_SPEED

    def update(self) -> None:
        self.rect.x += self.speed

    def draw(self, screen: pygame.Surface) -> None:
        pygame.draw.rect(
            screen,
            PROJECTILE_COLOR,
            self.rect,
            border_radius=4
        )

    def is_off_screen(self) -> bool:
        return self.rect.left > WIDTH