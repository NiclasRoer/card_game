import pygame
import math

class Animator:
    def __init__(self, screen, width=1280, height=720):
        self.frame = 0
        self.card_position = (0, 0)
        self.animation_running = False
        self.animation_runtime = 0.
        self.image = None
        self.rect = None
        self.original_rect = None
        self.WIDTH = width
        self.HEIGHT = height

        self.screen = screen

    def prepare_animation(self, image, runtime):
        self.image = pygame.transform.scale(image, (100, 145))
        self.rect = self.image.get_rect(topleft=self.card_position)
        self.original_rect = self.image.get_rect(topleft=self.card_position)
        self.animation_runtime = runtime

    def play_card_animation(self, timestamp):

        dx = self.WIDTH // 2 - self.rect.centerx
        dy = self.HEIGHT // 2 - self.rect.centery
        distance = math.sqrt(dx ** 2 + dy ** 2)
        dx_normalized = dx / distance
        dy_normalized = dy / distance

        max_scale = 2.0

        scale_factor = 1 + (max_scale - 1) * (timestamp / self.animation_runtime)  # Enlarge
        if timestamp > self.animation_runtime / 2:
            scale_factor = max_scale - (max_scale - 1) * ((timestamp - self.animation_runtime / 2) / (self.animation_runtime / 2))

        # Apply the scaling
        new_width = int(self.original_rect.width * scale_factor)
        new_height = int(self.original_rect.height * scale_factor)
        scaled_image = pygame.transform.scale(self.image, (new_width, new_height))
        scaled_rect = scaled_image.get_rect(center=self.rect.center)

        # Move the image along the normalized vector (dx_normalized, dy_normalized) with a fixed speed
        if timestamp > self.animation_runtime / 2:
            self.rect.x += dx_normalized * 10
            self.rect.y += dy_normalized * 10

        # Blit the scaled image to the screen
        # self.screen.fill((0, 0, 0))  # Fill the screen with black or transparent background
        self.screen.blit(scaled_image, scaled_rect)
        pygame.display.flip()

        pygame.time.Clock().tick(60)