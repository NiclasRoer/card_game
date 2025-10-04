from drawing import get_asset_path

class Sound_Manager:
    def __init__(self, pygame):
        pygame.mixer.init()
        self.pygame = pygame
        self.card_select_sound = pygame.mixer.Sound(get_asset_path("sounds/Dry Fire Gun-SoundBible.com-2053652037.mp3"))
        self.card_select_sound_timer = 0
        self.card_hover_sound = pygame.mixer.Sound(get_asset_path("sounds/Branch Wood Stress Cracking-SoundBible.com-2062541157.mp3"))
        self.card_hover_sound.set_volume(0.3)
        self.card_hover_sound_active = [True, True, True, True, True]
        # self.drawing_sound = pygame.mixer.Sound(get_asset_path('sounds/Drawer Opening-SoundBible.com-1100475088.mp3'))
        self.drawing_sound = pygame.mixer.Sound(get_asset_path('sounds/steampunk-mechanical-gadget-188052.mp3'))
        self.drawing_sound.set_volume(0.5)

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