import pygame

from core.constants import (
    BACKGROUND,
    BLACK,
    HEIGHT,
    FPS,
    SPAWN_INTERVAL,
    WHITE,
    WIDTH,
)
from entities.enemy import Enemy
from entities.player import Player
from entities.projectile import Projectile

class PlayingState:
    def __init__(self, game) -> None:
        self.game = game
        self.player = Player()

        self.projectiles: list[Projectile] = []
        self.enemies = []

        self.score = 0
        self.lives = 3

        self.spawn_timer = 0
        self.font = pygame.font.SysFont("Arial", 30)

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.shoot()

            elif event.key == pygame.K_ESCAPE:
                self.game.change_state("game_over", final_score=self.score)

    def handle_input(self) -> None:
        keys = pygame.key.get_pressed()
        self.player.update(keys)

    def update(self) -> None:
        self.spawn_timer += 1

        if self.spawn_timer >= SPAWN_INTERVAL:
            self.spawn_timer = 0
            self.spawn_enemy()

        for projectile in self.projectiles[:]:
            projectile.update()

            if projectile.is_off_screen():
                self.projectiles.remove(projectile)

        for enemy in self.enemies[:]:
            enemy.update()

            if enemy.rect.right < 0:
                self.enemies.remove(enemy)

            elif enemy.rect.colliderect(self.player.rect):
                self.enemies.remove(enemy)
                self.lives -= 1

                if self.lives <= 0:
                    self.game.change_state("game_over", final_score=self.score)
                    return
                
        self.check_projectile_collisions()

    def draw(self, screen: pygame.Surface) -> None:
        screen.fill(BACKGROUND)

        self.player.draw(screen)

        for projectile in self.projectiles:
            projectile.draw(screen)

        for enemy in self.enemies:
            enemy.draw(screen)

        hud_rect = pygame.Rect(10, 10, 220, 90)
        pygame.draw.rect(screen, WHITE, hud_rect, border_radius=10)
        pygame.draw.rect(screen, BLACK, hud_rect, width=2, border_radius=10)

        score_text = self.font.render(f"Score: {self.score}", True, BLACK)
        lives_text = self.font.render(f"Lives: {self.lives}", True, BLACK)

        screen.blit(score_text, (20, 20))
        screen.blit(lives_text, (20, 60))

    def shoot(self) -> None:
        projectile_x = self.player.rect.right
        projectile_y = self.player.rect.centery - 2
        self.projectiles.append(Projectile(projectile_x, projectile_y))

    def spawn_enemy(self) -> None:
        import random
        enemy_x = WIDTH
        enemy_y= random.randint(40, HEIGHT - 80)

        self.enemies.append(Enemy(enemy_x, enemy_y))

    def check_projectile_collisions(self) -> None:
        for projectile in self.projectiles[:]:
            for enemy in self.enemies[:]:
                if projectile.rect.colliderect(enemy.rect):
                    if projectile in self.projectiles:
                        self.projectiles.remove(projectile)

                    if enemy in self.enemies:
                        self.enemies.remove(enemy)

                    self.score += 10
                    break