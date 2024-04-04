import pygame
import Card as Card
class InputBox:
    def __init__(self, x, y, w, h, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = pygame.Color('white')  # Input box color
        #text color
        self.text_color = pygame.Color('white')
        self.text = text
        self.font = pygame.font.Font(None, 32)  # Using default font and setting size to 32
        self.txt_surface = self.font.render(text, True, self.color)
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            self.color = pygame.Color('dodgerblue2') if self.active else pygame.Color('lightskyblue1')
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    print(self.text)  # Do something with the input text
                    generated_cards = self.generate_cards(self.text)
                    self.text = ''  # Reset text
                    self.txt_surface = self.font.render(self.text, True, self.color)
                    return generated_cards
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                # Re-render the text.
                self.txt_surface = self.font.render(self.text, True, self.color)
    def draw(self, screen):
        # render a text to hint the user to input 5 cards
        text = self.font.render("Input 5 cards and see the result! (split with spaces)", True, self.text_color)
        text2 = self.font.render("Format: A for Spades A, 1 to 10, J, Q, K, A without suit", True, self.text_color)
        screen.blit(text, (self.rect.x, self.rect.y - 60))
        screen.blit(text2, (self.rect.x, self.rect.y - 30))

        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        # Blit the rect.
        pygame.draw.rect(screen, self.color, self.rect, 2)

    def generate_cards(self, text):
        # Generate cards from the input text
        # input format: 1 to 10, J, Q, K, A without suit, A means "Ace of Spades", 1 means other Aces
        cards = []
        split_text = text.split()
        if len(split_text) != 5:
            return None
        for card in text.split():
            if card.upper() == 'A':
                cards.append(Card.Card('Ace', 'Spades'))
            elif card == '1':
                # if ace of hearts, clubs or diamonds
                isAdded = False
                for c in cards:
                    if c.rank == 'Ace' and c.suit == 'Hearts':
                        isAdded = True
                        cards.append(Card.Card('Ace', 'Clubs'))
                        break
                    elif c.rank == 'Ace' and c.suit == 'Clubs':
                        cards.append(Card.Card('Ace', 'Diamonds'))
                        isAdded = True
                        break
                if not isAdded:
                    cards.append(Card.Card('Ace', 'Hearts'))
            elif card.upper() == 'J':
                cards = self.addCard(cards, "Jack")
            elif card.upper() == 'Q':
                cards = self.addCard(cards, "Queen")
            elif card.upper() == 'K':
                cards = self.addCard(cards, "King")
            else:
                cards = self.addCard(cards, card)
        return cards
    
    def addCard(self, cards, rank):
        # check if the rank is already in the cards, if have, add other suit
        # add suit in this order : Spades, Hearts, Clubs, Diamonds
        for card in cards:
            if card.rank == rank:
                if card.suit == 'Spades':
                    cards.append(Card.Card(rank, 'Hearts'))
                elif card.suit == 'Hearts':
                    cards.append(Card.Card(rank, 'Clubs'))
                elif card.suit == 'Clubs':
                    cards.append(Card.Card(rank, 'Diamonds'))

                break 
        # if the rank is not in the cards, add the first suit
        else:
            cards.append(Card.Card(rank, 'Spades'))
        return cards

