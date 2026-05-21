import pygame

from core.constants import (
    WIDTH,
    HEIGHT,
    PLAYER_WIDTH,
    PLAYER_HEIGHT,
    PLAYER_SPEED,
)

class Player:
    def __init__(self) -> None:
        self.rect = pygame.Rect(
            100,
            HEIGHT // 2,
            PLAYER_WIDTH,
            PLAYER_HEIGHT
        )

        self.speed = PLAYER_SPEED

    def update(self, keys: pygame.key.ScancodeWrapper) -> None:
        if keys[pygame.K_w] and self.rect.top > 0:
            self.rect.y -= self.speed
        if keys[pygame.K_s] and self.rect.bottom < HEIGHT:
            self.rect.y += self.speed
        if keys[pygame.K_a] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_d] and self.rect.right < WIDTH:
            self.rect.x += self.speed

    def draw(self, screen: pygame.Surface) -> None:
        pygame.draw.rect(
            screen,
            (255, 215, 0),
            self.rect,
            border_radius=12
        )