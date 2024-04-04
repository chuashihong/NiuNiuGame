import random
from Card import Card

class Deck:
    def __init__(self):
        self.cards = []
        self.build()
        self.shuffle()

    def build(self):
        suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
        ranks = ['Ace', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King']

        for suit in suits:
            for rank in ranks:
                self.cards.append(Card(rank, suit))

    def shuffle(self):
        random.shuffle(self.cards)

    def draw(self):
        if len(self.cards) > 0:
            return self.cards.pop()
        else:
            return None
        
    def pick_5_cards(self):
        # always create a new deck when picking 5 cards
        self.reset()
        self.shuffle()
        return [self.draw() for _ in range(5)]

    def reset(self):
        self.cards = []
        self.build()