import pygame
import random
import os
from drawing import get_asset_path

class Deck:
    def __init__(self):
        self.cards = self.create_new_deck()
        self.asset_names = self.load_asset_names()
        self.images = {}
        self.load_card_images()
        self.shuffle()

    def shuffle(self):
        random.shuffle(self.cards)

    def draw(self, n=1):
        if n > len(self.cards):
            return []
        drawn = self.cards[:n]
        self.cards = self.cards[n:]
        return drawn

    def put_back(self, card):
        self.cards.append(card)

    def load_card_images(self, path="card_images/PNG/Cards (medium)"):
        self.images = {}
        for filename in self.asset_names:
            if filename.endswith(".png"):
                key = filename.replace(".png", "")
                asset_path = get_asset_path(os.path.join(path, filename))
                img = pygame.image.load(asset_path).convert_alpha()
                img = pygame.transform.scale(img, (100, 145))  # scale to fit boxes
                self.images[key] = img

    def invert_card_colors(self, card_key):
        """Return a new surface with inverted colors"""
        card_img = self.images[card_key]
        inverted = pygame.Surface(card_img.get_size(), pygame.SRCALPHA)
        arr = pygame.surfarray.array3d(card_img)
        inv_arr = 255 - arr
        alpha = pygame.surfarray.array_alpha(card_img)
        pygame.surfarray.blit_array(inverted, inv_arr)
        pygame.surfarray.use_arraytype('numpy')  # ensure numpy is used
        pygame.surfarray.pixels_alpha(inverted)[:, :] = alpha  # restore alpha

        self.images[card_key] = inverted

    def create_new_deck(self):
        suits = ["Hearts", "Diamonds", "Clubs", "Spades"]
        ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "10",
                 "Jack", "Queen", "King", "Ace"]
        return [f"{rank} of {suit}" for suit in suits for rank in ranks]


    def load_deck(self, deck_filename):
        filename = get_asset_path(deck_filename)
        with open(filename, 'r', encoding='utf-8') as file:
            self.cards = [line.strip() for line in file]
        self.shuffle()

    def swap_card(self, card_key, card_index, new_card):

        card_name = f"{card_key.split('_')[2]} of {card_key.split('_')[1].capitalize()}"
        if card_name[0] == '0':
            card_name = card_name[1:]
        elif card_name[0] != '1':
            face_cards = {"A": "Ace", "J": "Jack", "Q": "Queen", "K": "King"}
            rank, suit = card_name.split(" of ")
            if rank in face_cards:
                rank = face_cards[rank]
            card_name = f"{rank} of {suit}"

        if card_name not in self.cards:
            print(self.cards)
            print(f"Card '{card_name}' not found in the deck.")
            return

        # index = self.cards.index(card_name)
        print(len(self.cards), card_index, new_card)
        # self.cards[card_index] = random.choice(self.cards)
        self.cards[card_index] = new_card
        return self.cards[card_index]
        #
        # # Update the image for the new card
        # new_image_key = new_card.replace(" ", "_").lower()
        #
        # if card_key in self.asset_names:
        #     asset_path = get_asset_path(os.path.join("card_images/PNG/Cards (medium)", card_key + ".png"))
        #     img = pygame.image.load(asset_path).convert_alpha()
        #     img = pygame.transform.scale(img, (100, 145))
        #     self.images[card_key] = img
        # else:
        #     print(f"Image for {new_card} not found.")

    def load_asset_names(self):
        return [# 'card_back.png',
                'card_clubs_02.png', 'card_clubs_03.png', 'card_clubs_04.png',
                'card_clubs_05.png', 'card_clubs_06.png', 'card_clubs_07.png', 'card_clubs_08.png',
                'card_clubs_09.png', 'card_clubs_10.png', 'card_clubs_A.png', 'card_clubs_J.png',
                'card_clubs_K.png', 'card_clubs_Q.png', 'card_diamonds_02.png',
                'card_diamonds_03.png', 'card_diamonds_04.png', 'card_diamonds_05.png',
                'card_diamonds_06.png', 'card_diamonds_07.png', 'card_diamonds_08.png',
                'card_diamonds_09.png', 'card_diamonds_10.png', 'card_diamonds_A.png',
                'card_diamonds_J.png', 'card_diamonds_K.png', 'card_diamonds_Q.png',
                'card_hearts_02.png', 'card_hearts_03.png',
                'card_hearts_04.png', 'card_hearts_05.png', 'card_hearts_06.png', 'card_hearts_07.png',
                'card_hearts_08.png', 'card_hearts_09.png', 'card_hearts_10.png', 'card_hearts_A.png',
                'card_hearts_J.png', 'card_hearts_K.png', 'card_hearts_Q.png',
                'card_spades_02.png', 'card_spades_03.png',
                'card_spades_04.png', 'card_spades_05.png', 'card_spades_06.png', 'card_spades_07.png',
                'card_spades_08.png', 'card_spades_09.png', 'card_spades_10.png', 'card_spades_A.png',
                'card_spades_J.png', 'card_spades_K.png', 'card_spades_Q.png',
                # 'color_back.png', 'color_draw.png', 'color_empty.png', 'color_green_0.png',
                # 'color_green_1.png', 'color_green_2.png', 'color_green_3.png', 'color_green_4.png',
                # 'color_green_5.png', 'color_green_6.png', 'color_green_7.png', 'color_green_8.png',
                # 'color_green_9.png', 'color_green_draw.png', 'color_green_empty.png',
                # 'color_green_reverse.png', 'color_green_skip.png', 'color_purple_0.png',
                # 'color_purple_1.png', 'color_purple_2.png', 'color_purple_3.png', 'color_purple_4.png',
                # 'color_purple_5.png', 'color_purple_6.png', 'color_purple_7.png', 'color_purple_8.png',
                # 'color_purple_9.png', 'color_purple_draw.png', 'color_purple_empty.png', 'color_purple_reverse.png',
                # 'color_purple_skip.png', 'color_red_0.png', 'color_red_1.png', 'color_red_2.png', 'color_red_3.png',
                # 'color_red_4.png', 'color_red_5.png', 'color_red_6.png', 'color_red_7.png', 'color_red_8.png',
                # 'color_red_9.png', 'color_red_draw.png', 'color_red_empty.png', 'color_red_reverse.png',
                # 'color_red_skip.png', 'color_wild.png', 'color_yellow_0.png', 'color_yellow_1.png',
                # 'color_yellow_2.png', 'color_yellow_3.png', 'color_yellow_4.png', 'color_yellow_5.png',
                # 'color_yellow_6.png', 'color_yellow_7.png', 'color_yellow_8.png', 'color_yellow_9.png',
                # 'color_yellow_draw.png', 'color_yellow_empty.png', 'color_yellow_reverse.png',
                # 'color_yellow_skip.png', 'dice_1.png', 'dice_2.png', 'dice_3.png', 'dice_4.png',
                # 'dice_5.png', 'dice_6.png', 'dice_decorated_1.png', 'dice_decorated_2.png',
                # 'dice_decorated_3.png', 'dice_decorated_4.png', 'dice_decorated_5.png', 'dice_decorated_6.png',
                # 'dice_decorated_empty.png', 'dice_decorated_question.png', 'dice_empty.png',
                # 'dice_question.png', '_cards.csv'
                ]



# Example usage:
if __name__ == "__main__":
    deck = Deck()
    print(f"Deck has {len(deck)} cards.")
    hand = deck.draw(5)
    print("You drew:", hand)
    print(f"Deck now has {len(deck)} cards.")