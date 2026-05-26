import pygame
import random

from core.constants import (
    BACKGROUND,
    BLACK,
    FPS,
    HEIGHT,
    MISSION_CYCLE,
    MISSION_DATA,
    MISSION_KEYS,
    MISSION_SURVIVAL,
    SPAWN_INTERVAL,
    WHITE,
    WIDTH,
)
from entities.data_fragment import DataFragment
from entities.enemy import Enemy
from entities.pickup import Pickup
from entities.player import Player
from entities.projectile import Projectile

class PlayingState:
    def __init__(self, game) -> None:
        self.game = game
        self.player = Player()

        self.projectiles: list[Projectile] = []
        self.enemies = []

        self.data_fragments = []
        self.key_drops: list[Pickup] = []
        self.one_up_drop: Pickup | None = None

        self.score = 0
        self.lives = 3

        self.spawn_timer = 0
        self.font = pygame.font.SysFont("Arial", 30)

        self.level = 1

        self.current_mission = MISSION_CYCLE[0]

        self.mission_target = 3
        self.mission_progress = 0

        self.combo = 0
        self.survival_timer = 0
        self.spawn_interval_current = SPAWN_INTERVAL

        self.exit_unlocked = False
        self.exit_rect = pygame.Rect(WIDTH - 52, HEIGHT // 2 - 60, 36, 120)

        self.setup_level()

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

        if self.spawn_timer >= self.spawn_interval_current:
            self.spawn_timer = 0
            self.spawn_enemy()

        for projectile in self.projectiles[:]:
            projectile.update()

            if projectile.is_off_screen():
                self.projectiles.remove(projectile)

        for enemy in self.enemies[:]:
            enemy.update(self.player.rect)

            if enemy.rect.right < 0:
                self.enemies.remove(enemy)

            elif enemy.rect.colliderect(self.player.rect):
                self.enemies.remove(enemy)
                self.lives -= 1

                if self.lives <= 0:
                    self.game.change_state("game_over", final_score=self.score)
                    return
                
        for fragment in self.data_fragments[:]:
            if fragment.rect.colliderect(self.player.rect):
                self.data_fragments.remove(fragment)

                self.mission_progress += 1
                self.score += 50

                if self.mission_progress >= self.mission_target:
                    self.exit_unlocked = True

        for key_drop in self.key_drops[:]:
            if key_drop.rect.colliderect(self.player.rect):
                self.key_drops.remove(key_drop)
                self.mission_progress += 1
                self.score += 75

                if self.mission_progress >= self.mission_target:
                    self.exit_unlocked = True

        if self.one_up_drop is not None and self.one_up_drop.rect.colliderect(self.player.rect):
            self.one_up_drop = None
            self.lives += 1
            self.score += 150
            self.exit_unlocked = True

        if self.current_mission == MISSION_SURVIVAL and self.one_up_drop is None:
            self.survival_timer += 1
            survived_seconds = self.survival_timer // FPS
            self.mission_progress = min(survived_seconds, self.mission_target)

            if self.survival_timer >= self.mission_target * FPS:
                self.spawn_one_up_drop()

        self.check_projectile_collisions()

        if self.exit_unlocked and self.player.rect.colliderect(self.exit_rect):
            self.level += 1
            self.setup_level()

    def draw(self, screen: pygame.Surface) -> None:
        screen.fill(BACKGROUND)

        self.player.draw(screen)

        for projectile in self.projectiles:
            projectile.draw(screen)

        for enemy in self.enemies:
            enemy.draw(screen)

        for fragment in self.data_fragments:
            fragment.draw(screen)

        for key_drop in self.key_drops:
            key_drop.draw(screen)

        if self.one_up_drop is not None:
            self.one_up_drop.draw(screen)

        if self.exit_unlocked:
            pygame.draw.rect(screen, (80, 255, 130), self.exit_rect, border_radius=10)
        else:
            pygame.draw.rect(screen, (80, 80, 90), self.exit_rect, border_radius=10)

        hud_rect = pygame.Rect(10, 10, 220, 120)
        pygame.draw.rect(screen, WHITE, hud_rect, border_radius=10)
        pygame.draw.rect(screen, BLACK, hud_rect, width=2, border_radius=10)

        score_text = self.font.render(f"Score: {self.score}", True, BLACK)
        lives_text = self.font.render(f"Lives: {self.lives}", True, BLACK)

        screen.blit(score_text, (20, 20))
        screen.blit(lives_text, (20, 60))

        mission_text = self.font.render(
            f"{self.current_mission.upper()}: "
            f"{self.mission_progress}/{self.mission_target}",
            True,
            BLACK,
        )

        if self.exit_unlocked:
            exit_text = self.font.render("Exit unlocked ->", True, WHITE)
            screen.blit(exit_text, (WIDTH - 260, 20))
        elif self.current_mission == MISSION_KEYS:
            key_text = self.font.render("Pick up dropped keys", True, WHITE)
            screen.blit(key_text, (WIDTH - 340, 20))
        elif self.current_mission == MISSION_SURVIVAL and self.one_up_drop is not None:
            one_up_text = self.font.render("Grab 1UP to unlock exit", True, WHITE)
            screen.blit(one_up_text, (WIDTH - 380, 20))

        screen.blit(mission_text, (25, 90))

    def shoot(self) -> None:
        projectile_x = self.player.rect.right
        projectile_y = self.player.rect.centery - 2
        self.projectiles.append(Projectile(projectile_x, projectile_y))

    def spawn_enemy(self) -> None:
        enemy_x = WIDTH
        enemy_y = random.randint(40, HEIGHT - 80)

        if self.current_mission == MISSION_KEYS:
            target_chance = 0.12
        elif self.current_mission == MISSION_SURVIVAL:
            target_chance = 0.18
        else:
            target_chance = 0.10

        is_targeting = random.random() < target_chance

        self.enemies.append(Enemy(enemy_x, enemy_y, target_player=is_targeting))

    def check_projectile_collisions(self) -> None:
        for projectile in self.projectiles[:]:
            for enemy in self.enemies[:]:
                if projectile.rect.colliderect(enemy.rect):
                    if projectile in self.projectiles:
                        self.projectiles.remove(projectile)

                    if enemy in self.enemies:
                        self.enemies.remove(enemy)

                    self.score += 10

                    if self.current_mission == MISSION_KEYS:
                        self.key_drops.append(
                            Pickup(enemy.rect.centerx, enemy.rect.centery, "key")
                        )

                    break

    def spawn_one_up_drop(self) -> None:
        x = random.randint(250, WIDTH - 100)
        y = random.randint(60, HEIGHT - 60)
        self.one_up_drop = Pickup(x, y, "one_up")

    def spawn_data_fragments(self) -> None:
        self.data_fragments.clear()

        for _ in range(self.mission_target):
            x = random.randint(250, WIDTH - 100)
            y = random.randint(60, HEIGHT - 60)

            self.data_fragments.append(
                DataFragment(x, y)
            )

    def setup_level(self) -> None:
        self.current_mission = MISSION_CYCLE[(self.level - 1) % len(MISSION_CYCLE)]
        self.mission_progress = 0
        self.exit_unlocked = False
        self.survival_timer = 0
        self.spawn_timer = 0
        self.projectiles.clear()
        self.enemies.clear()
        self.data_fragments.clear()
        self.key_drops.clear()
        self.one_up_drop = None

        self.player.rect.x = 100
        self.player.rect.y = HEIGHT // 2

        if self.current_mission == MISSION_DATA:
            self.mission_target = 3 + (self.level // 2)
            self.spawn_interval_current = SPAWN_INTERVAL
            self.spawn_data_fragments()

        elif self.current_mission == MISSION_KEYS:
            self.mission_target = 2 + (self.level // 3)
            self.spawn_interval_current = SPAWN_INTERVAL + 15

        elif self.current_mission == MISSION_SURVIVAL:
            self.mission_target = 20 + (self.level // 2)
            self.spawn_interval_current = max(35, SPAWN_INTERVAL - 10)