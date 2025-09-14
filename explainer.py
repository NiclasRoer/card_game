
class Tutorial:
    def __init__(self):
        self.tutorial_text = None
        self.tool_tip = None

        self.create_tutorial_text()
        self.create_tool_tip()

    def create_tutorial_text(self):
        self.tutorial_text = ["Hearts ♥: Heal according to the cards value.",
                              "Diamonds ♦: Odd Deal Damage according to your shield value.",
                              "            Even add shield according to the cards value.",
                              "Clubs ♣: Add poison to your enemy according to the cards value.",
                              "Spades ♠:  Odd: Draw cards according to half the cards value - 1.",
                              "           Even: Deal damage according to the cards value."]

    def create_tool_tip(self):
        self.tool_tip = "Tool Tip"