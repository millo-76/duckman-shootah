import pygame


class Pickup:
    def __init__(self, x: int, y: int, kind: str) -> None:
        self.kind = kind
        self.rect = pygame.Rect(0, 0, 22, 22)
        self.rect.center = (x, y)

    def draw(self, screen: pygame.Surface) -> None:
        if self.kind == "key":
            color = (255, 215, 80)
        elif self.kind == "one_up":
            color = (80, 255, 120)
        else:
            color = (255, 255, 255)

        pygame.draw.rect(screen, color, self.rect, border_radius=6)
