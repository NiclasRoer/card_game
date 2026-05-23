from deck import Deck
import random

from computing_helperfunctions import compute_card_value


class Character:
    def __init__(self):
        self.deck = Deck()
        self.draw_hook = None
        self.is_enemy = False
        self.animator = None  # Will be set from game.py
        self.reset_character(begin_duel=False)
        self.process_conditions()

        self.deckbuilder_selected_card_key = None

        self.enemy_card_start_time = 0
        self.ENEMY_DISPLAY_TIME = 1000

        self.field_suit = ''
        self.field_suit_number = 0

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
        self.fuel = 0
        self.dead_draw = 0
        self.damage_value = 0
        self.mana = 1
        if begin_duel:
            self.deck.shuffle()
            self.drawn_cards.extend(self.processes_drawing(3))

    def trigger_glow_for(self, stat, target_self=True):
        if not self.animator:
            return
        if target_self:
            glow_target = 'enemy' if self.is_enemy else 'player'
        else:
            glow_target = 'player' if self.is_enemy else 'enemy'
        self.animator.trigger_glow(f"{glow_target}_{stat}")

    def end_turn(self, enemy):
        # Poison damage
        if enemy.poison > 0:
            enemy.life -= enemy.poison
            self.trigger_glow_for('poison', target_self=False)
            self.trigger_glow_for('life', target_self=False)

        # Direct damage
        damage_taken = max(0, self.damage_value - enemy.shield)
        if damage_taken > 0:
            enemy.life -= damage_taken
            self.trigger_glow_for('life', target_self=False)

        # enemy.shield = max(0, enemy.shield - 2)
        self.poison = max(0, self.poison - 2)

        if self.mana < 0:
            enemy.mana = abs(self.mana)

        self.damage_value = 0

    def clear_played_cards(self):
        self.discarded_cards.extend(self.turn_played_cards)
        self.turn_played_cards = []

    def calc_damage(self, card_str, enemy):
        value, suit = compute_card_value(card_str)

        self.mana -= value

        if value == 14:
            if self.field_suit == suit:
                self.field_suit_number += 1
            else:
                self.field_suit_number = 1
                self.field_suit = suit

        if self.deck.reverse_flags[card_str]:
            if suit == 'Clubs':
                self.process_clubs_reverse(value, enemy)
            elif suit == 'Spades':
                self.process_spades_reverse(value, enemy)
            elif suit == 'Diamonds':
                self.process_diamonds_reverse(value, enemy)
            elif suit == 'Hearts':
                self.process_hearts_reverse(value)
        else:
            if suit == 'Clubs':
                self.process_clubs(value, enemy)
            elif suit == 'Spades':
                self.process_spades(value, enemy)
            elif suit == 'Diamonds':
                self.process_diamonds(value, enemy)
            elif suit == 'Hearts':
                self.process_hearts(value)

    def process_diamonds(self, value, enemy):
        modifier = self.field_suit_number if self.field_suit == 'Diamonds' else 0

        if value <= 10:
            if value % 2:
                enemy.shield = max(0, enemy.shield - value)
                self.damage_value = self.shield + self.fuel
                self.trigger_glow_for('shield', target_self=False)
            else:
                self.shield += 2 * (value + modifier * modifier)
                self.trigger_glow_for('shield', target_self=True)
        else:
            stolen = enemy.shield - max(0, enemy.shield - 10 - modifier * modifier)
            if stolen > 0:
                self.shield += stolen
                enemy.shield -= stolen
                self.trigger_glow_for('shield', target_self=True)
                self.trigger_glow_for('shield', target_self=False)


    def process_clubs(self, value, enemy):
        modifier = self.field_suit_number if self.field_suit == 'Clubs' else 0

        if value <= 10:
            if value % 2:
                enemy.poison += value + modifier * modifier
                self.trigger_glow_for('poison', target_self=False)
            else:
                self.poison -= value + modifier * modifier
                self.trigger_glow_for('poison', target_self=True)
        else:
            if enemy.field_suit != '':
                enemy.field_suit_number -= 1
                if enemy.field_suit_number < 1:
                    enemy.field_suit = ''

    def process_spades(self, value, enemy):
        modifier = self.field_suit_number if self.field_suit == 'Spades' else 0

        if value <= 10:
            if value % 2:
                new_cards = self.processes_drawing(int(value / 2) - 1)
                self.drawn_cards.extend(new_cards)
                if self.draw_hook and new_cards:
                    self.draw_hook(new_cards, self)
            else:
                enemy.fuel -= int(value / 2)
                self.trigger_glow_for('fuel', target_self=False)
        else:
            if len(enemy.drawn_cards) >= 1:
                enemy.drawn_cards.pop(random.randrange(len(enemy.drawn_cards) + modifier))


    def process_hearts(self, value):
        modifier = self.field_suit_number if self.field_suit == 'Hearts' else 0

        if value <= 10:
            if value % 2:
                self.life += value
                self.trigger_glow_for('life', target_self=True)
            else:
                self.fuel += int(value / 2)
                self.trigger_glow_for('fuel', target_self=True)
        else:
            # Change to recycling cards
            self.life = int(self.life * 0.75 + modifier*modifier)
            self.damage_value = int(self.life * 0.33) + modifier*modifier + self.fuel
            self.trigger_glow_for('life', target_self=True)


    def process_diamonds_reverse(self, value, enemy):
        self.process_diamonds(value, enemy)

    def process_clubs_reverse(self, value, enemy):
        # self.conditions['Corrosion'] = value + self.conditions['Corrosion']
        self.process_clubs(value, enemy)

    def process_spades_reverse(self, value, enemy):
        self.process_spades(value, enemy)

    def process_hearts_reverse(self, value):
        # self.conditions['Overclock'] = value + self.conditions['Overclock']
        self.process_hearts(value)

    def processes_drawing(self, number_of_cards):
        new_cards = self.deck.draw(number_of_cards)
        if not new_cards:
            self.dead_draw += 1
            self.life -= self.dead_draw
        return new_cards