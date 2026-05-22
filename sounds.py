from computing_helperfunctions import get_asset_path
import os


class _DummySound:
    def __init__(self, *args, **kwargs):
        pass

    def play(self):
        return None

    def set_volume(self, _v):
        return None


class Sound_Manager:
    def __init__(self, pygame):
        self.pygame = pygame
        self.enabled = True
        # Try to initialize the mixer; if it fails, try alternate drivers then fall back to dummy
        try:
            pygame.mixer.init()
        except Exception:
            # try a few common SDL audio drivers on Windows as a fallback
            for driver in ("directsound", "winmm", "dsound", "dummy"):
                try:
                    os.environ["SDL_AUDIODRIVER"] = driver
                    try:
                        pygame.mixer.quit()
                    except Exception:
                        pass
                    pygame.mixer.init()
                    break
                except Exception:
                    continue
            else:
                # all attempts failed; run without sound
                self.enabled = False

        # Load sounds if mixer is available, otherwise use dummy objects
        try:
            if self.enabled:
                self.card_select_sound = pygame.mixer.Sound(get_asset_path("sounds/Dry Fire Gun-SoundBible.com-2053652037.mp3"))
            else:
                self.card_select_sound = _DummySound()
        except Exception:
            self.card_select_sound = _DummySound()

        self.card_select_sound_timer = 0

        try:
            if self.enabled:
                self.card_hover_sound = pygame.mixer.Sound(get_asset_path("sounds/Branch Wood Stress Cracking-SoundBible.com-2062541157.mp3"))
                self.card_hover_sound.set_volume(0.3)
            else:
                self.card_hover_sound = _DummySound()
        except Exception:
            self.card_hover_sound = _DummySound()

        self.card_hover_sound_active = [True, True, True, True, True]

        try:
            if self.enabled:
                # self.drawing_sound = pygame.mixer.Sound(get_asset_path('sounds/Drawer Opening-SoundBible.com-1100475088.mp3'))
                self.drawing_sound = pygame.mixer.Sound(get_asset_path('sounds/steampunk-mechanical-gadget-188052.mp3'))
                self.drawing_sound.set_volume(0.5)
            else:
                self.drawing_sound = _DummySound()
        except Exception:
            self.drawing_sound = _DummySound()

    def play_card_select(self):
        if self.card_select_sound_timer + 200 <= self.pygame.time.get_ticks():
            self.card_select_sound.play()
            self.card_select_sound_timer = self.pygame.time.get_ticks()

    def play_card_hover(self, handcard_index):
        if self.card_hover_sound_active[handcard_index]:
            self.card_hover_sound.play()
            self.card_hover_sound_active[handcard_index] = False

    def reactive_hover(self):
        try:
            index = self.card_hover_sound_active.index(False)

            mouse_x, mouse_y = self.pygame.mouse.get_pos()
            start_x = (1280 - (5 * 100 + 4 * 10)) // 2 + index * (145 + 10)
            start_y = 720 - 145 - 20
            if not start_x <= mouse_x <= start_x + 100 and not start_y <= mouse_y <= start_y + 145:
                self.card_hover_sound_active[index] = True
        except:
            pass

    def play_draw(self):
        self.drawing_sound.play()