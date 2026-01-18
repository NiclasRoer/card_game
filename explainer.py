from computing_helperfunctions import compute_card_value

class Tutorial:
    def __init__(self):
        self.tutorial_text_duel = None
        self.tutorial_text = None
        self.tool_tip = None

        self.create_tutorial_text()
        self.creat_tutorial_text_duel()
        self.create_tool_tip()

    def create_tutorial_text(self):
        self.tutorial_text = ["Hearts ♥:   Odd     - Heal according to the cards value.",
                              "            Even    - Add fuel counters, to increase physical damage.",
                              "            Picture - Pay 25% life to deal 33% total physical damage.",
                              "Diamonds ♦: Odd     - Deal physical damage according to 2 * your shield value.",
                              "            Even    - Add shield according to the cards value.",
                              "            Picture - Steal 10 shield from your enemy.",
                              "",
                              "",
                              "",
                              "",
                              "Clubs ♣:    Odd     - Add poison stacks to your enemy according to cards value.",
                              "            Even    - Reduce your poison stacks according to cards value.",
                              "            Picture - Destroy one of your enemies ace stacks.",
                              "Spades ♠:   Odd     - Draw cards according to half the cards value - 1.",
                              "            Even    - Reduce enemies fuel by cards value.",
                              "            Picture - Enemy discards a random card.",
                              "",
                              "Aces increase the effectiveness of a suit and can be stacked. Only one suit can be stacked at a time."]

    def creat_tutorial_text_duel(self):
        self.tutorial_text_duel = []
        self.tutorial_text_duel.append(['This is the Tutorial. Click with your left mouse button to progress...'])
        self.tutorial_text_duel.append(['These are your card slots. You can select cards from your hand. The icons',
                                        'are currently meaningless...'])
        self.tutorial_text_duel.append(['These hexagons show your mana for the turn. Each card costs mana depending',
                                        'on its value. If you drop below 0, the turn changes. Your opponent receives',
                                        'mana equal to the amount by which you fall below 0.'])
        self.tutorial_text_duel.append(['These are your actions. You can play your selected card from your hand,',
                                        'draw a card for 1 mana, check the symbols effects or reverse the card.',
                                        'Reversing the card has currently no effect...'])
        self.tutorial_text_duel.append(['These are your characters status values. Life indicates your health points,',
                                        'the skull are your poison stacks, the shield your armor, the flame your fuel.',
                                        'Poison does damage to you after each turn, armor prevents physical damage and',
                                        'fuel in- or decreases physical damage...'])

    def create_tool_tip(self):
        self.tool_tip = {
            'Hearts': {'even': 'Powerup your attacks', 'odd': 'Heal yourself', 'img': 'Pay life to deal damage', 'ace': 'Strengthen your hearts cards'},
            'Diamonds': {'even': 'Gives shield value', 'odd': 'Does physical damage', 'img': 'Steal shield value', 'ace': 'Strengthen your diamond cards'},
            'Clubs': {'even': 'Reduce your poison stacks', 'odd': 'Poison the enemy', 'img': 'Destroy enemies ace stack', 'ace': 'Strengthen your club cards'},
            'Spades': {'even': 'Debuff enemies attacks', 'odd': 'Draw cards', 'img': 'Opponent discards a card', 'ace': 'Strengthen your spade cards'},
        }


    def provide_tool_tip(self, card_name):
        value, suit = compute_card_value(card_name)

        if value == 14:
            category = 'ace'
        elif value > 10:
            category = 'img'
        elif value % 2 == 0:
            category = 'even'
        else:
            category = 'odd'
        return self.tool_tip[suit][category]
