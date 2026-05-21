import pygame
import math

class Animator:
    def __init__(self, screen, width=1280, height=720):
        self.frame = 0
        self.card_position = (0, 0)
        self.end_position = (0, 0)
        self.animation_running = False
        self.animation_runtime = 0.
        self.image = None
        self.rect = None
        self.original_rect = None
        self.WIDTH = width
        self.HEIGHT = height

        self.draw_animation_running = False
        self.draw_back_image = None
        self.draw_front_image = None
        self.draw_card_name = None
        self.draw_target_index = None
        self.draw_start_pos = pygame.Vector2(0, 0)
        self.draw_end_pos = pygame.Vector2(0, 0)
        self.draw_duration = 0.
        self.draw_card_start_time = 0
        self.draw_queue = []
        self.pending_draws = []

        self.toss_animation_running = False
        self.toss_image = None
        self.toss_start_pos = pygame.Vector2(0, 0)
        self.toss_end_pos = pygame.Vector2(0, 0)
        self.toss_duration = 0.
        self.toss_card_name = None
        self.toss_target_index = None
        self.toss_card_start_time = 0
        self.toss_queue = []

        self.screen = screen

    def prepare_animation(self, image, runtime, cards_played_this_turn, player_turn):
        self.image = pygame.transform.scale(image, (100, 145))
        self.rect = self.image.get_rect(topleft=self.card_position)
        self.original_rect = self.image.get_rect(topleft=self.card_position)
        self.animation_runtime = runtime
        self.end_position = (self.WIDTH // 3 + 50*cards_played_this_turn, self.HEIGHT // 2 - 100*player_turn + 100*int(not player_turn))

    def prepare_draw_animation(self, back_image, front_image, start_pos, end_pos, duration=600, card_name=None, target_index=None):
        self.draw_back_image = pygame.transform.scale(back_image, (100, 145))
        self.draw_front_image = pygame.transform.scale(front_image, (100, 145))
        self.draw_start_pos = pygame.Vector2(start_pos)
        self.draw_end_pos = pygame.Vector2(end_pos)
        self.draw_duration = duration
        self.draw_card_name = card_name
        self.draw_target_index = target_index
        self.draw_animation_running = True
        self.draw_card_start_time = pygame.time.get_ticks()

    def queue_draw_animation(self, back_image, front_image, start_pos, end_pos, duration=600, card_name=None, target_index=None, enemy=False):
        entry = {
            'back_image': back_image,
            'front_image': front_image,
            'start_pos': start_pos,
            'end_pos': end_pos,
            'duration': duration,
            'card_name': card_name,
            'target_index': target_index,
            'enemy': enemy,
        }
        self.draw_queue.append(entry)
        self.pending_draws.append(entry)
        if not self.draw_animation_running:
            self._start_next_draw_animation()

    def _start_next_draw_animation(self):
        if self.draw_animation_running or not self.draw_queue:
            return
        item = self.draw_queue.pop(0)
        self.prepare_draw_animation(
            item['back_image'],
            item['front_image'],
            item['start_pos'],
            item['end_pos'],
            item['duration'],
            card_name=item['card_name'],
            target_index=item['target_index'],
        )

    def play_draw_animation(self, timestamp):
        if not self.draw_animation_running or self.draw_duration <= 0:
            return

        progress = min(timestamp / self.draw_duration, 1.0)
        current_pos = self.draw_start_pos.lerp(self.draw_end_pos, progress)

        flip_angle = math.pi * progress
        width_scale = max(abs(math.cos(flip_angle)), 0.05)
        image = self.draw_back_image if progress < 0.5 else self.draw_front_image
        scaled_width = max(1, int(self.draw_back_image.get_width() * width_scale))
        scaled_image = pygame.transform.scale(image, (scaled_width, self.draw_back_image.get_height()))
        scaled_rect = scaled_image.get_rect(center=current_pos)
        self.screen.blit(scaled_image, scaled_rect)

        if progress >= 1.0:
            self.draw_animation_running = False
            for i, pending in enumerate(self.pending_draws):
                if (pending['card_name'] == self.draw_card_name and
                        pending['target_index'] == self.draw_target_index):
                    self.pending_draws.pop(i)
                    break
            self.draw_card_name = None
            self.draw_target_index = None
            self.draw_back_image = None
            self.draw_front_image = None
            self._start_next_draw_animation()

    def prepare_toss_animation(self, card_image, start_pos, end_pos, duration=600, card_name=None, target_index=None):
        self.toss_queue.append({
            'card_image': card_image,
            'start_pos': start_pos,
            'end_pos': end_pos,
            'duration': duration,
            'card_name': card_name,
            'target_index': target_index,
        })
        if not self.toss_animation_running:
            self._start_next_toss_animation()

    def _start_next_toss_animation(self):
        if self.toss_animation_running or not self.toss_queue:
            return
        item = self.toss_queue.pop(0)
        self.toss_image = pygame.transform.scale(item['card_image'], (100, 145))
        self.toss_start_pos = pygame.Vector2(item['start_pos'])
        self.toss_end_pos = pygame.Vector2(item['end_pos'])
        self.toss_duration = item['duration']
        self.toss_card_name = item['card_name']
        self.toss_target_index = item['target_index']
        self.toss_animation_running = True
        self.toss_card_start_time = pygame.time.get_ticks()

    def play_toss_animation(self, timestamp):
        if not self.toss_animation_running or self.toss_duration <= 0:
            return

        progress = min(timestamp / self.toss_duration, 1.0)
        current_pos = self.toss_start_pos.lerp(self.toss_end_pos, progress)

        angle = -60 * progress
        offset = pygame.Vector2(-progress * 120, -progress * 20)
        rotated = pygame.transform.rotozoom(self.toss_image, angle, 1 - 0.1 * progress)
        scaled_rect = rotated.get_rect(center=current_pos + offset)
        self.screen.blit(rotated, scaled_rect)

        if progress >= 1.0:
            self.toss_animation_running = False
            self.toss_image = None
            self.toss_card_name = None
            self.toss_target_index = None
            self._start_next_toss_animation()

    def play_card_animation(self, timestamp):

        dx = self.end_position[0] - self.rect.centerx
        dy = self.end_position[1] - self.rect.centery
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
            self.rect.x += dx_normalized * 8
            self.rect.y += dy_normalized * 8

        # Blit the scaled image to the screen
        # self.screen.fill((0, 0, 0))  # Fill the screen with black or transparent background
        self.screen.blit(scaled_image, scaled_rect)
        pygame.display.flip()

        pygame.time.Clock().tick(60)