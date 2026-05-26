import pygame

from core.constants import (
    ENEMY_COLOR,
    ENEMY_WIDTH,
    ENEMY_HEIGHT,
    ENEMY_SPEED,
    HEIGHT,
)

class Enemy:
    def __init__(self, x: int, y: int, target_player: bool = False) -> None:
        self.rect = pygame.Rect(
            x,
            y,
            ENEMY_WIDTH,
            ENEMY_HEIGHT
        )

        self.speed = ENEMY_SPEED
        self.target_player = target_player
        self.vertical_speed = 2

    def update(self, player_rect: pygame.Rect | None = None) -> None:
        self.rect.x -= self.speed

        if self.target_player and player_rect is not None:
            enemy_center = self.rect.centery
            player_center = player_rect.centery

            if enemy_center < player_center:
                self.rect.y += self.vertical_speed
            elif enemy_center > player_center:
                self.rect.y -= self.vertical_speed

            self.rect.y = max(0, min(self.rect.y, HEIGHT - self.rect.height))

    def draw(self, screen: pygame.Surface) -> None:
        pygame.draw.rect(
            screen,
            ENEMY_COLOR,
            self.rect,
            border_radius=8
        )
