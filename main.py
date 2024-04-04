import pygame
import sys
from Deck import Deck
from ResultCalculator import ResultCalculator
from InputBox import InputBox
# Initialize Pygame
pygame.init()

# Screen settings
screen_width = 1200
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Niu Niu Card Game")

# Colors
white = (255, 255, 255)
green = (0, 255, 0)
blue = (0, 0, 128)
black = (0, 0, 0)

#Button1 position
button1width = 350
button1height = 50

button1 = pygame.Rect(screen_width * 0.5 - button1width // 2, screen_height * 0.8 - button1height // 2, button1width, button1height)
# Button1 text position (centered)
button1textpos = (button1.x + button1.width // 2 - 150, button1.y + button1.height // 2 - 10)

#result position
result_pos = (screen_width * 0.7, screen_height * 0.5)
# Fonts
font = pygame.font.Font(None, 36)

# Initialize input box
input_box = InputBox(50, screen_height // 2 - 170, 140, 32)

# Initialize deck
deck = Deck()

def draw_button(color):
    pygame.draw.rect(screen, color, button1)
    text = font.render('Randomly Pick 5 Cards', True, black)
    screen.blit(text, button1textpos)

def draw_result(result, threeCard, twoCard):
    
    text = font.render("Result", True, white)
    text2 = font.render(result, True, white)
    
    screen.blit(text, result_pos)
    screen.blit(text2, (result_pos[0], result_pos[1] + 50)) 
    if result != "No Niu found":
        text3 = font.render("Three Cards", True, white)
        text4 = font.render("Two Cards", True, white)
        screen.blit(text3, (result_pos[0], result_pos[1] + 100))
        screen.blit(text4, (result_pos[0], result_pos[1] + 200))
        # display the value of the three cards
        for i, card in enumerate(threeCard):
            text5 = font.render(f"{card.value()}", True, white)
            screen.blit(text5, (result_pos[0] + i * 50, result_pos[1] + 150))
        # display the value of the two cards
        for i, card in enumerate(twoCard):
            text6 = font.render(f"{card.value()}", True, white)
            screen.blit(text6, (result_pos[0] + i * 50, result_pos[1] + 250))

def calculateResult(result):
    calculator = ResultCalculator()
    point = calculator.calculate_result(result)
    return point

# Load card images
def load_card_images(cards):
    images = []
    for card in cards:
        img_path = f"./img/{card.image_path()}"  # Assuming your script is run from the directory containing /img/
        try:
            image = pygame.image.load(img_path)
            image = pygame.transform.scale(image, (100, 140))  # Scale image to desired size
            images.append(image)
        except pygame.error as e:
            print(f"Error loading image: {img_path} - {e}")
            # Optionally, load a default 'card not found' image
    return images

def main():
    deck = Deck()
    button1color = green
    running = True
    cards_picked = False
    card_images = []
    picked_cards = []
    result = ""
    threeCard, twoCard = [], []
    input_box = InputBox(50, screen_height // 2 - 170, 140, 32)
    while running:
        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                running = False
            # when hover over button1, it will change color
            if event.type == pygame.MOUSEMOTION and event.buttons[0] == 0:
                mouse_pos = event.pos
                if button1.collidepoint(mouse_pos):
                    button1color = blue
                else:
                    button1color = green

            # Change button color on click
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = event.pos
                if button1.collidepoint(mouse_pos):
                    button1color = white  # Click color
             # Reset button color on mouse button release
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                ## if the position of the mouse is on the button, then change the color to blue
                mouse_pos = event.pos
                if button1.collidepoint(event.pos):
                    button1color = blue
                    picked_cards = deck.pick_5_cards()
                    card_images = load_card_images(picked_cards)
                    cards_picked = True
                    result, threeCard, twoCard = calculateResult(picked_cards)
                else:
                    button1color = green
            cardsByUser = input_box.handle_event(event)
            if cardsByUser:
                picked_cards = cardsByUser
                card_images = load_card_images(picked_cards)
                cards_picked = True
                result, threeCard, twoCard = calculateResult(picked_cards)

        screen.fill(black)  # Fill screen with white
        if cards_picked:
            # Display the picked card images
            for i, img in enumerate(card_images):
                screen.blit(img, (50 + i * 120, screen_height // 2 - 70))  # Adjust positioning as needed
        draw_result(result, threeCard, twoCard)
        draw_button(button1color)
        input_box.draw(screen)  # Draw the input box
        
        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
