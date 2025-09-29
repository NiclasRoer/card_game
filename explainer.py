
class Tutorial:
    def __init__(self):
        self.tutorial_text_duel = None
        self.tutorial_text = None
        self.tool_tip = None

        self.create_tutorial_text()
        self.creat_tutorial_text_duel()
        self.create_tool_tip()

    def create_tutorial_text(self):
        self.tutorial_text = ["Hearts ♥: Heal according to the cards value.",
                              "Diamonds ♦: Odd Deal Damage according to your shield value.",
                              "            Even add shield according to the cards value.",
                              "Clubs ♣: Add poison to your enemy according to the cards value.",
                              "Spades ♠:  Odd: Draw cards according to half the cards value - 1.",
                              "           Even: Deal damage according to the cards value."]

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
                                        'the skull are your poison stacks, the shield your armor. Poison does damage',
                                        'to you, armor prevents physical damage...'])

    def create_tool_tip(self):
        self.tool_tip = "Tool Tip"

