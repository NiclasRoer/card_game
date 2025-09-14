import pygame
import math

class Animator:
    def __init__(self, screen, width=1280, height=720):
        self.frame = 0
        self.card_position = (0, 0)
        self.animation_running = False
        self.image = None
        self.rect = None
        self.WIDTH = width
        self.HEIGHT = height

        self.screen = screen

    def prepare_animation(self, image):
        self.image = pygame.transform.scale(image, (100, 145))
        self.rect = self.image.get_rect(topleft=self.card_position)

    def play_card_animation(self):
        # Calculate the difference in position (dx, dy)
        dx = self.WIDTH // 2 - self.rect.centerx
        dy = self.HEIGHT // 2 - self.rect.centery

        # Calculate distance to the target (center)
        distance = math.sqrt(dx ** 2 + dy ** 2)

        # Normalize the direction vector (dx, dy) to ensure consistent speed
        dx_normalized = dx / distance
        dy_normalized = dy / distance

        # Move the image along the normalized vector (dx_normalized, dy_normalized) with a fixed speed
        self.rect.x += dx_normalized * 7
        self.rect.y += dy_normalized * 7

        self.screen.blit(self.image, self.rect)
        pygame.display.flip()
        pygame.time.Clock().tick(60)