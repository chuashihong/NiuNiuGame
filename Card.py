class Card:
    def __init__(self, rank, suit):
        """
        Initialize a new Card instance.

        :param rank: The rank of the card (e.g., '2', '3', ..., 'King', 'Ace')
        :param suit: The suit of the card ('Clubs', 'Diamonds', 'Hearts', 'Spades')
        """
        self.rank = rank
        self.suit = suit
    
    def value(self):
        """
        Return the value of the card.
        """
        if self.rank in ['Jack', 'Queen', 'King']:
            return 10
        elif self.rank == 'Ace':
            return 1
        else:
            return int(self.rank)
        
    def rank(self):
        return self.rank
    
    def image_path(self):
        """Return the filename of the card's image."""
        return f"{self.rank}_of_{self.suit}.png".lower()

    def __repr__(self):
        """
        Return a string representation of the card, useful for debugging.
        """
        return f"Card('{self.rank}', '{self.suit}')"

    def __str__(self):
        """
        Return a user-friendly string representation of the card.
        """
        return f"{self.rank} of {self.suit}"

    def __eq__(self, value: object) -> bool:
        """
        Check if two cards are equal.
        """
        return self.rank == value.rank
    
    def __lt__(self, other):
        """
        Compare two cards based on their value.
        """
        return self.value() < other.value()
    def __hash__(self):
        return hash((self.rank, self.suit))

