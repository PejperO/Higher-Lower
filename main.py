import pygame
import random
import sys

# initialize pygame
pygame.init()

# screen
WIDTH, HEIGHT = 800, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Higher or Lower - Card Game")

# colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 180, 0)
RED = (200, 0, 0)
BLUE = (0, 120, 200)
GRAY = (200, 200, 200)

# fonts
FONT = pygame.font.SysFont("Arial", 36)
SMALL = pygame.font.SysFont("Arial", 20)
SUIT_FONT = pygame.font.SysFont("Arial", 40)

# card values (A = 14)
CARD_VALUES = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
CARD_MAP = {val: i+2 for i, val in enumerate(CARD_VALUES)}

# suits and their display
SUITS = ['♠', '♥', '♦', '♣']  # spade, heart, diamond, club


def draw_card(rank, suit, x, y, hidden=False):
    """Draw a playing card rectangle with rank and suit. Suits colored like online poker."""
    card_w, card_h = 100, 150
    pygame.draw.rect(WIN, WHITE, (x, y, card_w, card_h), border_radius=8)
    pygame.draw.rect(WIN, BLACK, (x, y, card_w, card_h), 3, border_radius=8)
    if hidden:
        q = FONT.render("?", True, RED)
        WIN.blit(q, (x + card_w//2 - q.get_width()//2, y + card_h//2 - q.get_height()//2))
    else:
        # suit color: hearts and diamonds are red, others black
        suit_color = RED if suit in ['♥', '♦'] else BLACK
        # rank text (top-left)
        rtext = SMALL.render(rank, True, BLACK)
        WIN.blit(rtext, (x + 8, y + 8))
        # suit symbol (center)
        stext = SUIT_FONT.render(suit, True, suit_color)
        WIN.blit(stext, (x + card_w//2 - stext.get_width()//2, y + card_h//2 - stext.get_height()//2))
        # rank small in bottom-right
        rtext2 = SMALL.render(rank, True, BLACK)
        WIN.blit(rtext2, (x + card_w - rtext2.get_width() - 8, y + card_h - rtext2.get_height() - 8))


def message(text, color, y):
    msg = FONT.render(text, True, color)
    WIN.blit(msg, (WIDTH//2 - msg.get_width()//2, y))


def new_game():
    # return list of (rank_str, suit_str)
    return [(random.choice(CARD_VALUES), random.choice(SUITS)) for _ in range(3)]


def main():
    clock = pygame.time.Clock()
    running = True

    cards = new_game()
    step = 0  # 0 = bet between card1 and card2, 1 = bet between card2 and card3
    game_over = False
    result_msg = ""
    result_state = None  # 'win' or 'loss'

    while running:
        WIN.fill(GRAY)

        # draw cards (reveal logic: reveal hidden depending on step and game_over)
        draw_card(cards[0][0], cards[0][1], 150, 200, hidden=False)
        draw_card(cards[1][0], cards[1][1], 350, 200, hidden=(step == 0 and not game_over))
        draw_card(cards[2][0], cards[2][1], 550, 200, hidden=(step <= 1 and not game_over))

        if not game_over:
            # vertical buttons: higher on top, lower below
            higher_btn = pygame.Rect(WIDTH//2 - 75, 400, 150, 60)
            lower_btn = pygame.Rect(WIDTH//2 - 75, 480, 150, 60)
            pygame.draw.rect(WIN, GREEN, higher_btn, border_radius=8)
            pygame.draw.rect(WIN, RED, lower_btn, border_radius=8)
            WIN.blit(FONT.render("Higher", True, WHITE), (higher_btn.x + 20, higher_btn.y + 12))
            WIN.blit(FONT.render("Lower", True, WHITE), (lower_btn.x + 30, lower_btn.y + 12))

            hint = SMALL.render("Or use ↑ for Higher, ↓ for Lower", True, BLACK)
            WIN.blit(hint, (WIDTH//2 - hint.get_width()//2, 360))
        else:
            # show result message with color depending on win/loss
            color = GREEN if result_state == 'win' else RED
            message(result_msg, color, 100)
            # reset button
            reset_btn = pygame.Rect(WIDTH//2 - 75, 450, 150, 60)
            pygame.draw.rect(WIN, BLUE, reset_btn, border_radius=8)
            WIN.blit(FONT.render("Reset", True, WHITE), (reset_btn.x + 35, reset_btn.y + 12))
            restart_msg = SMALL.render("Press SPACE to play again", True, BLACK)
            WIN.blit(restart_msg, (WIDTH//2 - restart_msg.get_width()//2, 520))

        pygame.display.flip()

        # event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if game_over and event.key == pygame.K_SPACE:
                    cards = new_game()
                    step = 0
                    game_over = False
                    result_msg = ""
                    result_state = None
                elif not game_over:
                    if event.key == pygame.K_UP:
                        guess_higher = True
                    elif event.key == pygame.K_DOWN:
                        guess_higher = False
                    else:
                        guess_higher = None

                    if guess_higher is not None:
                        # first bet or second
                        if step == 0:
                            val1 = CARD_MAP[cards[0][0]]
                            val2 = CARD_MAP[cards[1][0]]
                            if val2 == val1:
                                result_msg = "Tie — you lose!"
                                result_state = 'loss'
                                game_over = True
                            elif (guess_higher and val2 > val1) or (not guess_higher and val2 < val1):
                                step = 1
                            else:
                                result_msg = "You lost!"
                                result_state = 'loss'
                                game_over = True
                        elif step == 1:
                            val2 = CARD_MAP[cards[1][0]]
                            val3 = CARD_MAP[cards[2][0]]
                            if val3 == val2:
                                result_msg = "Tie — you lose!"
                                result_state = 'loss'
                            elif (guess_higher and val3 > val2) or (not guess_higher and val3 < val2):
                                result_msg = "You won!"
                                result_state = 'win'
                            else:
                                result_msg = "You lost!"
                                result_state = 'loss'
                            game_over = True

            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                if not game_over:
                    higher_btn = pygame.Rect(WIDTH//2 - 75, 400, 150, 60)
                    lower_btn = pygame.Rect(WIDTH//2 - 75, 480, 150, 60)
                    if higher_btn.collidepoint(mx, my) or lower_btn.collidepoint(mx, my):
                        guess_higher = higher_btn.collidepoint(mx, my)
                        if step == 0:
                            val1 = CARD_MAP[cards[0][0]]
                            val2 = CARD_MAP[cards[1][0]]
                            if val2 == val1:
                                result_msg = "Tie — you lose!"
                                result_state = 'loss'
                                game_over = True
                            elif (guess_higher and val2 > val1) or (not guess_higher and val2 < val1):
                                step = 1
                            else:
                                result_msg = "You lost!"
                                result_state = 'loss'
                                game_over = True
                        elif step == 1:
                            val2 = CARD_MAP[cards[1][0]]
                            val3 = CARD_MAP[cards[2][0]]
                            if val3 == val2:
                                result_msg = "Tie — you lose!"
                                result_state = 'loss'
                            elif (guess_higher and val3 > val2) or (not guess_higher and val3 < val2):
                                result_msg = "You won!"
                                result_state = 'win'
                            else:
                                result_msg = "You lost!"
                                result_state = 'loss'
                            game_over = True
                else:
                    reset_btn = pygame.Rect(WIDTH//2 - 75, 450, 150, 60)
                    if reset_btn.collidepoint(mx, my):
                        cards = new_game()
                        step = 0
                        game_over = False
                        result_msg = ""
                        result_state = None

        clock.tick(30)


if __name__ == "__main__":
    main()
