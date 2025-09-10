from deck import Deck


class Character:
    def __init__(self):
        self.deck = Deck()
        self.drawn_cards = []
        self.drawn_cards.extend(self.deck.draw(3))
        self.hand = []

        self.selected_card = None
        self.selected_card_position = None
        self.deckbuilder_selected_card_key = None
        self.life = 100
        self.poison = 0
        self.shield = 0
        self.damage_value = 0

        self.mana = 1

        self.enemy_card_start_time = 0
        self.ENEMY_DISPLAY_TIME = 750

    def end_turn(self, enemy):
        enemy.life -= enemy.poison

        enemy.life = enemy.life - max(0, self.damage_value - enemy.shield)
        enemy.shield = max(0, enemy.shield - 2)
        self.poison = max(0, self.poison - 2)

        if self.mana < 0:
            enemy.mana = abs(self.mana)

        self.damage_value = 0

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
        if suit == 'Clubs':
            self.process_clubs(value, enemy)
        elif suit == 'Spades':
            self.damage_value = value
        elif suit == 'Diamonds':
            self.process_diamonds(value, enemy)
        elif suit == 'Hearts':
            self.life += value

    def process_diamonds(self, value, enemy):
        if value % 2:
            self.shield += 2 * value
        else:
            enemy.shield = max(0, enemy.shield - value)
            self.damage_value = self.shield

    def process_clubs(self, value, enemy):
        if value % 2:
            enemy.poison += value
        else:
            self.poison = max(0, self.poison - (value-1))

