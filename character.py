from deck import Deck
import random


class Character:
    def __init__(self):
        self.deck = Deck()
        self.reset_character(begin_duel=False)
        self.process_conditions()

        self.deckbuilder_selected_card_key = None

        self.enemy_card_start_time = 0
        self.ENEMY_DISPLAY_TIME = 1000

    def process_conditions(self):
        self.conditions = {'Overclock': 0, 'Corrosion': 0, 'Upgrade': 0}

    def reset_character(self, begin_duel=True):
        self.drawn_cards = []
        self.hand = []
        self.turn_played_cards = []
        self.discarded_cards = []
        self.selected_card = None
        self.selected_card_position = None
        self.life = 100
        self.poison = 0
        self.shield = 0
        self.damage_value = 0
        self.mana = 1
        if begin_duel:
            self.deck.shuffle()
            self.drawn_cards.extend(self.deck.draw(3))

    def end_turn(self, enemy):
        enemy.life -= enemy.poison

        enemy.life = enemy.life - max(0, self.damage_value - enemy.shield)
        enemy.shield = max(0, enemy.shield - 2)
        self.poison = max(0, self.poison - 2)

        if self.mana < 0:
            enemy.mana = abs(self.mana)

        self.damage_value = 0
        enemy.discarded_cards.extend(self.turn_played_cards)
        enemy.turn_played_cards = []

    def calc_damage(self, card_str, enemy):
        rank_str, suit = card_str.split(" of ")

        rank_map = {
            "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7,
            "8": 8, "9": 9, "10": 10,
            "Jack": 11, "Queen": 12, "King": 13, "Ace": 14,
            "": 0
        }
        value = rank_map.get(rank_str, None)

        self.mana -= value

        if self.deck.reverse_flags[card_str]:
            if suit == 'Clubs':
                self.process_clubs_reverse(value)
            elif suit == 'Spades':
                self.process_spades_reverse(enemy)
            elif suit == 'Diamonds':
                self.process_diamonds_reverse(value, enemy)
            elif suit == 'Hearts':
                self.process_hearts_reverse(value)
        else:
            if suit == 'Clubs':
                self.process_clubs(value, enemy)
            elif suit == 'Spades':
                self.process_spades(value)
            elif suit == 'Diamonds':
                self.process_diamonds(value, enemy)
            elif suit == 'Hearts':
                self.process_hearts(value)

    def process_diamonds(self, value, enemy):
        if value % 2:
            self.shield += 2 * value
        else:
            enemy.shield = max(0, enemy.shield - value)
            self.damage_value = self.shield

    def process_clubs(self, value, enemy):
        enemy.poison += value

    def process_spades(self, value):
        if value % 2:
            self.damage_value = value
        else:
            new_cards = self.deck.draw(int(value / 2))
            self.drawn_cards.extend(new_cards)

    def process_hearts(self, value):
        self.life += value


    def process_diamonds_reverse(self, value, enemy):
        if value % 2:
            self.shield += 2 * value
        else:
            enemy.shield = max(0, enemy.shield - value)
            self.damage_value = self.shield

    def process_clubs_reverse(self, value):
        self.conditions['Corrosion'] = value + self.conditions['Corrosion']

    def process_spades_reverse(self, enemy):
        discard_card = random.choice(enemy.drawn_cards) if len(enemy.drawn_cards) > 0 else ""
        index = enemy.drawn_cards.index(discard_card)
        enemy.drawn_cards.pop(index)

    def process_hearts_reverse(self, value):
        self.conditions['Overclock'] = value + self.conditions['Overclock']