import sys
import pygame

from core.constants import FPS, HEIGHT, TITLE, WIDTH
from states.playing import PlayingState


class Game:
    def __init__(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.running = True
        self.state = PlayingState(self)

    def change_state(self, state_name: str, **kwargs) -> None:
        if state_name == "playing":
            self.state = PlayingState(self)
        elif state_name == "game_over":
            self.running = False

    def _handle_event(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            else:
                self.state.handle_event(event)

    def run(self) -> None:
        while self.running:
            self._handle_event()
            self.state.handle_input()
            self.state.update()
            self.state.draw(self.screen)

            pygame.display.flip()
            self.clock.tick(FPS)

        pygame.quit()
        sys.exit()