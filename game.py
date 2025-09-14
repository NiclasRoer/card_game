import pygame
import random
import sys

from drawing import UI, draw_arrow, card_name_to_filename
from character import Character
from animations import Animator


def select_card(mouse_pos, last_cards, start_x, y_pos, box_width=100, box_height=145, spacing=10):
    """
    Check if the mouse clicked on one of the displayed card boxes.

    Parameters:
        mouse_pos: tuple (x, y) of mouse click
        last_cards: list of currently displayed cards (up to 5)
        start_x, y_pos: top-left position of the first card box
        box_width, box_height: size of each card box
        spacing: space between boxes

    Returns:
        The card name if a box was clicked, otherwise None
    """
    for i in range(len(last_cards)):
        rect = pygame.Rect(start_x + i * (box_width + spacing), y_pos, box_width, box_height)
        if rect.collidepoint(mouse_pos):
            return last_cards[i], i  # return the card clicked
    return None


# -------------------------------
# Pygame setup
# -------------------------------
pygame.init()
WIDTH, HEIGHT = 1280, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Card Draw Game")

font = pygame.font.SysFont(None, 32)

ui = UI(screen)
animator = Animator(screen)
player = Character()
enemy = Character()

### MAIN MENU
main_menu = True
show_deck_builder = False
show_tutorial = False

while main_menu:
    ui.draw_main()

    if show_deck_builder:
        ui.draw_deck_builder(player)
    elif show_tutorial:
        ui.draw_tutorial(410, 10)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Mouse click events
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if ui.button_hover(150, 200, 200, 50):  # Start Game
                print("Start Game clicked")
                main_menu = False
                # Call the function to start the game (you can transition here)
            elif ui.button_hover(150, 275, 200, 50):  # Deck
                print("Deckbuilder clicked")
                show_deck_builder = not show_deck_builder
                player.deckbuilder_selected_card_key = None
            elif ui.button_hover(150, 350, 200, 50):
                player.deck.load_deck('saved_deck.txt', force_root_dir=True)
                print('Deck loaded')
            elif ui.button_hover(150, 425, 200, 50):  # Options
                print("Tutorial clicked")
                show_tutorial = not show_tutorial
            elif ui.button_hover(150, 500, 200, 50):  # Options
                print("Options clicked")
            elif ui.button_hover(WIDTH - 100, HEIGHT - 100, 50, 50) and show_deck_builder:
                player.deck.save_deck('saved_deck.txt')
                print('save deck')

            elif ui.button_hover(150, 575, 200, 50):  # Quit
                pygame.quit()
                sys.exit()

    pygame.display.flip()
    ui.clock.tick(60)

### MAIN GAME
# player.deck.load_deck('test_deck.txt')

enemy_turn_step = None

played_card = None
player_turn = True

# -------------------------------
# Main loop
# -------------------------------
mid_screen = False
main_game = True
run_duel = True
while main_game:
    player.reset_character()
    enemy.reset_character()
    enemy.mana = 0

    while run_duel:
        screen.fill((34, 139, 34))  # green table background

        ui.draw_game(player, enemy)
        if show_tutorial:
            ui.draw_tutorial(50, HEIGHT/2 + 50, font='small')

        center = pygame.Vector2(WIDTH / 2 - 350, 95 if not player_turn else 630)
        end = pygame.Vector2(WIDTH / 2 - 300, 95 if not player_turn else 630)
        # draw_arrow(screen, center, end, pygame.Color("dodgerblue"), 10, 20, 12)
        draw_arrow(screen, center, end, pygame.Color(0, 0, 0), 10, 20, 12)

        # --- Draw 5 card boxes at the bottom
        box_width = 100
        box_height = 145
        spacing = 10
        start_x = (WIDTH - (5 * box_width + 4 * spacing)) // 2
        y_pos = HEIGHT - box_height - 20

        last_cards = player.drawn_cards[-5:]
        enemy_last_cards = enemy.drawn_cards[-5:]

        # Draw Card Slots and cards
        for i in range(5):
            card_slot_rect = pygame.Rect(start_x + i * (box_width + spacing), y_pos, box_width, box_height)
            enemy_card_slot_rect = pygame.Rect(start_x + i * (box_width + spacing), 20, box_width, box_height)

            # Draw empty box
            pygame.draw.rect(screen, (200, 200, 200), card_slot_rect, border_radius=5)
            pygame.draw.rect(screen, (200, 200, 200), enemy_card_slot_rect, border_radius=5)

            # Decide border color
            if i < len(last_cards) and last_cards[i] == player.selected_card and i == player.selected_card_position:
                border_color = (255, 215, 0)  # highlight
                animator.card_position = (start_x + i * (box_width + spacing), y_pos)
            else:
                border_color = (0, 0, 0)
            pygame.draw.rect(screen, border_color, card_slot_rect, 3, border_radius=5)

            if i < len(enemy_last_cards) and enemy_last_cards[i] == enemy.selected_card:
                border_color = (255, 215, 0)  # highlight
                animator.card_position = (start_x + i * (box_width + spacing), 20)
            else:
                border_color = (0, 0, 0)
            pygame.draw.rect(screen, border_color, enemy_card_slot_rect, 3, border_radius=5)

            # Draw card image if it exists
            if i < len(last_cards):
                card_key = card_name_to_filename(last_cards[i])
                card_img = player.deck.images.get(card_key)
                if card_img:
                    img_rect = card_img.get_rect(center=card_slot_rect.center)
                    screen.blit(card_img, img_rect)

            if i < len(enemy_last_cards):
                card_key = card_name_to_filename(enemy_last_cards[i])
                card_img = enemy.deck.images.get(card_key)
                if card_img:
                    img_rect = card_img.get_rect(center=enemy_card_slot_rect.center)
                    screen.blit(card_img, img_rect)

            if played_card:
                card_key = card_name_to_filename(played_card)
                card_img = player.deck.images.get(card_key) if not player_turn else enemy.deck.images.get(card_key)
                if card_img:
                    # Scale to fit nicely in the center
                    center_img = pygame.transform.scale(card_img, (200, 290))  # adjust size
                    center_rect = center_img.get_rect(center=(WIDTH // 2, HEIGHT // 2))
                    screen.blit(center_img, center_rect)

        # Draw tooltips
        for i in range(5):
            if ui.button_hover(start_x + i * (box_width + spacing), y_pos, box_width, box_height):
                ui.draw_tooltip(ui.tutorial.tool_tip)
            if ui.button_hover(start_x + i * (box_width + spacing), 20, box_width, box_height):
                ui.draw_tooltip(ui.tutorial.tool_tip)

        if animator.animation_running:
            elapsed = pygame.time.get_ticks() - player.enemy_card_start_time
            if elapsed <= player.ENEMY_DISPLAY_TIME:
                animator.play_card_animation()
            else:
                animator.animation_running = False

                # Needed to step into the regular loop without an active event anymore
                # custom_event = pygame.event.Event(pygame.USEREVENT + 1, data={"message": "Hello from custom event!"})
                # pygame.event.post(custom_event)

        elif player_turn:

            # --- Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_e:
                        player.deck.add_card('Jack of Spades')

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if ui.button_rect.collidepoint(event.pos):
                        # Draw a new card
                        player.mana -= 1
                        new_cards = player.deck.draw(1)
                        player.drawn_cards.extend(new_cards)
                        if len(player.drawn_cards) >= 6:
                            player.drawn_cards = player.drawn_cards[1:]
                        # Deselect if selected card is no longer in hand
                        if player.selected_card not in player.drawn_cards:
                            selected_card = None
                            selected = None

                    elif ui.reverse_button_rect.collidepoint(event.pos):
                        # Reverse colors of selected card
                        if player.selected_card:
                            card_key = card_name_to_filename(player.selected_card)
                            if card_key in player.deck.images:
                                player.deck.invert_card_colors(card_key)

                    elif ui.play_button_rect.collidepoint(event.pos):
                        # Play the selected card
                        played_card = player.selected_card
                        if player.selected_card in player.drawn_cards:
                            player.calc_damage(played_card, enemy)
                            player.drawn_cards.remove(player.selected_card)
                            player.selected_card = None  # deselect immediately
                            selected = None
                            animator.animation_running = True

                            animation_card_key = card_name_to_filename(played_card)
                            animation_card_img = player.deck.images.get(animation_card_key)
                            center_img = pygame.transform.scale(animation_card_img, (100, 145))
                            animator.prepare_animation(center_img)
                            player.enemy_card_start_time = pygame.time.get_ticks()

                    elif ui.tutorial_button_rect.collidepoint(event.pos):
                        show_tutorial = not show_tutorial

                    else:
                        # Check if a card box was clicked
                        selected, index = select_card(event.pos, player.drawn_cards[-5:], start_x, y_pos)
                        if selected and selected in player.drawn_cards:
                            player.selected_card = selected
                            player.selected_card_position = index

                elif player.mana < 0:
                    player_turn = not player_turn
                    enemy_card = enemy.deck.draw(1)
                    enemy.drawn_cards.extend(enemy_card)
                    if len(enemy.drawn_cards) >= 6:
                        enemy.drawn_cards = enemy.drawn_cards[1:]
                    enemy_turn_step = 1
                    if enemy_turn_step:
                        enemy_card = enemy_card[0] if len(enemy_card) > 0 else ""
                        enemy.enemy_card_start_time = pygame.time.get_ticks()
                    player.end_turn(enemy)

        # Enemy turn
        else:
            for event in pygame.event.get():
                pass

            if enemy_turn_step == 1:
                elapsed = pygame.time.get_ticks() - enemy.enemy_card_start_time
                if elapsed <= enemy.ENEMY_DISPLAY_TIME and enemy_card != "":
                    card_key = card_name_to_filename(enemy_card)
                    card_img = enemy.deck.images.get(card_key)
                    if card_img:
                        # Draw on the left side
                        enemy_img = pygame.transform.scale(card_img, (100, 145))  # adjust size
                        enemy_rect = enemy_img.get_rect(midleft=(20, HEIGHT // 2))
                        screen.blit(enemy_img, enemy_rect)
                else:
                    enemy_turn_step += 1
                    enemy.enemy_card_start_time = pygame.time.get_ticks()

            elif enemy_turn_step == 2:
                elapsed = pygame.time.get_ticks() - enemy.enemy_card_start_time
                if elapsed <= enemy.ENEMY_DISPLAY_TIME:
                    if not enemy.selected_card:
                        enemy.selected_card = random.choice(enemy.drawn_cards) if len(enemy.drawn_cards) > 0 else ""
                else:
                    enemy_turn_step = 3
                    enemy.enemy_card_start_time = pygame.time.get_ticks()

                    animation_card_key = card_name_to_filename(enemy.selected_card)
                    animation_card_img = enemy.deck.images.get(animation_card_key)
                    animator.prepare_animation(animation_card_img)

            elif enemy_turn_step == 3:
                # ANIMATION
                elapsed = pygame.time.get_ticks() - enemy.enemy_card_start_time
                if elapsed <= enemy.ENEMY_DISPLAY_TIME:
                    animator.play_card_animation()
                else:
                    enemy_turn_step = 4
                    enemy.enemy_card_start_time = pygame.time.get_ticks()

            elif enemy_turn_step == 4:
                elapsed = pygame.time.get_ticks() - enemy.enemy_card_start_time
                if elapsed <= enemy.ENEMY_DISPLAY_TIME:
                    if enemy.selected_card in enemy.drawn_cards:
                        played_card = enemy.selected_card
                        enemy.calc_damage(played_card, player)
                        enemy.drawn_cards.remove(enemy.selected_card)
                        enemy.selected_card = None  # deselect immediately
                        selected = None
                else:
                    enemy_turn_step = 5

            elif enemy_turn_step == 5:
                if enemy.mana < 0:
                    enemy_turn_step = 6
                elif len(enemy.drawn_cards) == 0:
                        enemy.deck.draw(1)
                        enemy.mana -= 1
                else:
                    enemy_turn_step = 1

            if enemy_turn_step == 6:
                new_cards = player.deck.draw(1)
                player.drawn_cards.extend(new_cards)
                if len(player.drawn_cards) >= 6:
                    player.drawn_cards = player.drawn_cards[1:]
                player_turn = not player_turn
                enemy.end_turn(player)

        if enemy.life <= 0:
            mid_screen = True
            run_duel = False
        elif player.life <= 0:
            main_game = False
            run_duel = False
        pygame.display.flip()
        ui.clock.tick(60)

    while mid_screen:
        ui.draw_mid_screen()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    mouse_pos = pygame.mouse.get_pos()
                    if ui.next_game_button.collidepoint(mouse_pos):
                        run_duel = True
                        mid_screen = False
                    if ui.end_game_button.collidepoint(mouse_pos):
                        main_game = False
                        mid_screen = False
        pygame.display.flip()
        ui.clock.tick(60)

while True:
    ui.draw_end_screen(enemy.life < player.life)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
            pygame.quit()
            sys.exit()

    pygame.display.flip()