from deck import Deck

deck = Deck()
print(f"Deck has {len(deck)} cards.")
hand = deck.draw(5)
print("You drew:", hand)
print(f"Deck now has {len(deck)} cards.")