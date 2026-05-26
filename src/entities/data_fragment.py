import pygame

class DataFragment:
    def __init__(self, x: int, y: int) -> None:
        self.rect = pygame.Rect(x, y, 28, 28)

    def draw(self, screen: pygame.Surface) -> None:
        pygame.draw.rect(
            screen,
            (80, 220, 255),
            self.rect,
            border_radius=6,
        )