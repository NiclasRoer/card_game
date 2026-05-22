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
        self.card_start_pos = pygame.Vector2(0, 0)
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
        self.turn_transition_running = False
        self.turn_transition_start_time = 0
        self.turn_transition_duration = 500
        self.turn_transition_enemy = False
        self.turn_transition_cards = []
        self.turn_transition_callback = None
        self.toss_image = None
        self.toss_start_pos = pygame.Vector2(0, 0)
        self.toss_end_pos = pygame.Vector2(0, 0)
        self.toss_duration = 0.
        self.toss_card_name = None
        self.toss_target_index = None
        self.toss_card_start_time = 0
        self.toss_queue = []

        self.screen = screen

    def prepare_animation(self, image, runtime, start_pos, end_pos):
        self.image = pygame.transform.scale(image, (100, 145))
        self.card_start_pos = pygame.Vector2(start_pos)
        self.end_position = pygame.Vector2(end_pos)
        self.rect = self.image.get_rect(center=self.card_start_pos)
        self.original_rect = self.image.get_rect(center=self.card_start_pos)
        self.animation_runtime = runtime
        self.animation_running = True

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

    def prepare_turn_transition(self, card_images, start_positions, end_positions, enemy=False, duration=500, on_complete=None):
        self.turn_transition_cards = []
        self.turn_transition_enemy = enemy
        self.turn_transition_duration = duration
        self.turn_transition_callback = on_complete
        for img, start_pos, end_pos in zip(card_images, start_positions, end_positions):
            self.turn_transition_cards.append({
                'image': pygame.transform.scale(img, (100, 145)),
                'start': pygame.Vector2(start_pos),
                'end': pygame.Vector2(end_pos),
                'enemy': enemy,
            })
        self.turn_transition_running = True
        self.turn_transition_start_time = pygame.time.get_ticks()

    def play_turn_transition(self, timestamp):
        if not self.turn_transition_running or self.turn_transition_duration <= 0:
            return

        progress = min(timestamp / self.turn_transition_duration, 1.0)
        for item in self.turn_transition_cards:
            current_pos = item['start'].lerp(item['end'], progress)
            offset = pygame.Vector2((item['end'].x - item['start'].x) * 0.1, -30 * progress)
            draw_pos = current_pos + offset
            scaled = pygame.transform.rotozoom(item['image'], -30 * progress, 1 - 0.15 * progress)
            temp = scaled.copy()
            temp.set_alpha(max(40, int(255 * (1 - progress))))
            self.screen.blit(temp, temp.get_rect(center=draw_pos))

        if progress >= 1.0:
            self.turn_transition_running = False
            self.turn_transition_cards = []
            if self.turn_transition_callback:
                self.turn_transition_callback()
                self.turn_transition_callback = None

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
        if not self.animation_running or self.animation_runtime <= 0:
            return

        progress = min(timestamp / self.animation_runtime, 1.0)
        max_scale = 2.0
        if progress < 0.5:
            scale_factor = 1 + (max_scale - 1) * (progress / 0.5)
        else:
            scale_factor = max_scale - (max_scale - 1) * ((progress - 0.5) / 0.5)

        current_pos = self.card_start_pos.lerp(self.end_position, progress)
        new_width = max(1, int(self.original_rect.width * scale_factor))
        new_height = max(1, int(self.original_rect.height * scale_factor))
        scaled_image = pygame.transform.scale(self.image, (new_width, new_height))
        scaled_rect = scaled_image.get_rect(center=current_pos)
        self.screen.blit(scaled_image, scaled_rect)

        if progress >= 1.0:
            self.animation_running = False