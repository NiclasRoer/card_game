import pygame
import random
import sys

from computing_helperfunctions import card_name_to_filename
from drawing import UI, draw_arrow
from character import Character
from animations import Animator
from sounds import Sound_Manager


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
    return None, None


def enqueue_draw_animations_for_new_cards(actor, new_cards):
    if not new_cards:
        return

    visible_cards = actor.drawn_cards[-5:]
    for card_name in new_cards:
        if card_name not in visible_cards:
            continue
        card_key = card_name_to_filename(card_name)
        card_front = actor.deck.images.get(card_key)
        card_back = actor.deck.images.get("card_back")
        target_index = visible_cards.index(card_name)
        start_center = ui.get_deck_center(enemy=actor.is_enemy)
        target_center = ui.get_card_slot_center(len(visible_cards), target_index, enemy=actor.is_enemy)
        if card_back and card_front:
            animator.queue_draw_animation(card_back, card_front, start_center, target_center, 600, card_name=card_name, target_index=target_index, enemy=actor.is_enemy)

    overflow = max(0, len(actor.drawn_cards) - 5)
    if overflow > 0:
        discard_cards = actor.drawn_cards[:overflow]
        for discard_name in discard_cards:
            discard_key = card_name_to_filename(discard_name)
            discard_img = actor.deck.images.get(discard_key)
            toss_start = ui.get_card_slot_center(len(actor.drawn_cards), 0, enemy=actor.is_enemy)
            toss_end = (-100 if not actor.is_enemy else WIDTH + 100, toss_start[1])
            if discard_img:
                animator.prepare_toss_animation(discard_img, toss_start, toss_end, 600, card_name=discard_name, target_index=0)
            actor.drawn_cards = actor.drawn_cards[1:]


# -------------------------------
# Pygame setup
# -------------------------------
pygame.init()
WIDTH, HEIGHT = 1280, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Card Draw Game")

font = pygame.font.SysFont(None, 32)

sound_manager = Sound_Manager(pygame)
ui = UI(screen)
animator = Animator(screen)
player = Character()
player.is_enemy = False
enemy = Character()
enemy.is_enemy = True

player.draw_hook = lambda new_cards, actor: enqueue_draw_animations_for_new_cards(actor, new_cards)
enemy.draw_hook = lambda new_cards, actor: enqueue_draw_animations_for_new_cards(actor, new_cards)

### MAIN MENU
main_menu = True
show_deck_builder = False
show_tutorial = False

while main_menu:
    ui.draw_main()

    if show_deck_builder:
        ui.draw_deck_builder(player)
    elif show_tutorial:
        ui.draw_tutorial_text(410, 10)

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

enemy_turn_step = None

played_card = None
player_turn = True

selected = None
index = None

# player.deck.load_deck('')
# enemy.deck.load_deck('')
while True:
    screen.fill((34, 34, 34))  # green table background
    ui.draw_tutorial_duel(player, enemy, animator, sound_manager, select_card, event, selected, index)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # if ui.button_hover(150, 500, 200, 50):  # Start Game
            ui.tutorial_step += 1
    if ui.tutorial_step == 5:
        break
    pygame.display.flip()

### MAIN GAME
# player.deck.load_deck('test_deck.txt')

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
    enqueue_draw_animations_for_new_cards(player, player.drawn_cards)
    enqueue_draw_animations_for_new_cards(enemy, enemy.drawn_cards)

    while run_duel:
        screen.fill((34, 139, 34))  # green table background

        ui.draw_game(player, enemy, animator, sound_manager, select_card, event, selected, index)
        if show_tutorial:
            # ui.draw_tutorial_text(50, HEIGHT / 2 + 50, font='small')
            ui.draw_tutorial_text(50, HEIGHT / 2 - 120, font='small')

        center = pygame.Vector2(WIDTH / 2 - 350, 95 if not player_turn else 630)
        end = pygame.Vector2(WIDTH / 2 - 300, 95 if not player_turn else 630)
        # draw_arrow(screen, center, end, pygame.Color("dodgerblue"), 10, 20, 12)
        draw_arrow(screen, center, end, pygame.Color(0, 0, 0), 10, 20, 12)

            # if played_card and not animator.animation_running and enemy_turn_step != 3 and enemy_turn_step != 4:
            #     card_key = card_name_to_filename(played_card)
            #     card_img = player.deck.images.get(card_key) if not player_turn else enemy.deck.images.get(card_key)
            #     if card_img:
            #         # Scale to fit nicely in the center
            #         center_img = pygame.transform.scale(card_img, (200, 290))  # adjust size
            #         center_rect = center_img.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            #         screen.blit(center_img, center_rect)

        if animator.draw_animation_running:
            elapsed = pygame.time.get_ticks() - animator.draw_card_start_time
            animator.play_draw_animation(elapsed)

        if animator.toss_animation_running:
            elapsed = pygame.time.get_ticks() - animator.toss_card_start_time
            animator.play_toss_animation(elapsed)

        if animator.turn_transition_running:
            elapsed = pygame.time.get_ticks() - animator.turn_transition_start_time
            animator.play_turn_transition(elapsed)
            pygame.display.flip()
            ui.clock.tick(60)
            continue

        if animator.animation_running and (player_turn or enemy_turn_step == 4):
            start_time = player.enemy_card_start_time if player_turn else enemy.enemy_card_start_time
            elapsed = pygame.time.get_ticks() - start_time
            runtime = player.ENEMY_DISPLAY_TIME if player_turn else enemy.ENEMY_DISPLAY_TIME
            if elapsed <= runtime:
                animator.play_card_animation(elapsed)
            else:
                animator.animation_running = False
                if player_turn and played_card:
                    player.turn_played_cards.append(played_card)
                elif not player_turn:
                    enemy_turn_step = 5
                    enemy.turn_played_cards.append(played_card)
                played_card = None

                if player_turn and player.mana < 0:
                    def complete_player_transition():
                        global player_turn, enemy_turn_step, enemy_card
                        player.end_turn(enemy)
                        player_turn = False
                        enemy_turn_step = 1
                        enemy_card = enemy.processes_drawing(1)
                        enemy.drawn_cards.extend(enemy_card)
                        enqueue_draw_animations_for_new_cards(enemy, enemy_card)
                        sound_manager.play_draw()
                        enemy_card = enemy_card[0] if len(enemy_card) > 0 else ""
                        enemy.enemy_card_start_time = pygame.time.get_ticks()

                    turn_images = []
                    start_positions = []
                    end_positions = []
                    for idx, card_name in enumerate(player.turn_played_cards):
                        card_key = card_name_to_filename(card_name)
                        card_img = player.deck.images.get(card_key)
                        if card_img:
                            turn_images.append(card_img)
                            start_positions.append(ui.get_played_card_center(idx, enemy=False))
                            end_positions.append((-150, HEIGHT - 120 + idx * 12))

                    if turn_images:
                        animator.prepare_turn_transition(turn_images, start_positions, end_positions, enemy=False, on_complete=complete_player_transition)
                    else:
                        complete_player_transition()

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
                        new_cards = player.processes_drawing(1)
                        if new_cards:
                            player.drawn_cards.extend(new_cards)
                            enqueue_draw_animations_for_new_cards(player, new_cards)
                            sound_manager.play_draw()

                        # Deselect if selected card is no longer in hand
                        if player.selected_card not in player.drawn_cards:
                            selected_card = None
                            selected = None
                        animator.animation_running = player.mana < 0
                        # player.enemy_card_start_time = 0

                    elif ui.reverse_button_rect.collidepoint(event.pos):
                        # Reverse colors of selected card
                        if player.selected_card:
                            card_key = card_name_to_filename(player.selected_card)
                            if card_key in player.deck.images:
                                player.deck.invert_card_colors(card_key, player.selected_card)

                    elif ui.play_button_rect.collidepoint(event.pos):
                        # Play the selected card
                        played_card = player.selected_card
                        if player.selected_card in player.drawn_cards:
                            start_pos = ui.get_card_slot_center(len(player.drawn_cards), player.selected_card_position, enemy=False)
                            end_pos = ui.get_played_card_center(len(player.turn_played_cards), enemy=False)

                            player.calc_damage(played_card, enemy)
                            player.drawn_cards.remove(player.selected_card)

                            player.selected_card = None  # deselect immediately
                            selected = None
                            animator.animation_running = True

                            animation_card_key = card_name_to_filename(played_card)
                            animation_card_img = player.deck.images.get(animation_card_key)
                            if animation_card_img:
                                center_img = pygame.transform.scale(animation_card_img, (100, 145))
                                animator.prepare_animation(center_img, player.ENEMY_DISPLAY_TIME, start_pos, end_pos)
                            player.enemy_card_start_time = pygame.time.get_ticks()

                    elif ui.tutorial_button_rect.collidepoint(event.pos):
                        show_tutorial = not show_tutorial

                    else:
                        # Check if a card box was clicked
                        card_slot_area_x = (WIDTH - (5 * 100 + 4 * 10)) // 2
                        card_slot_area_y = HEIGHT - 145 - 20
                        selected, index = select_card(event.pos, player.drawn_cards[-5:], card_slot_area_x, card_slot_area_y)
                        if selected and selected in player.drawn_cards:
                            sound_manager.play_card_select()
                            if selected == player.selected_card:
                                player.selected_card = None
                                player.selected_card_position = None
                            else:
                                player.selected_card = selected
                                player.selected_card_position = index

            # Sound timing
            sound_manager.reactive_hover()

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
                        enemy_img = pygame.transform.scale(card_img, (100, 145))
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
                    if enemy.selected_card:
                        animation_card_key = card_name_to_filename(enemy.selected_card)
                        animation_card_img = enemy.deck.images.get(animation_card_key)
                        if animation_card_img:
                            start_pos = ui.get_card_slot_center(len(enemy.drawn_cards), enemy.drawn_cards.index(enemy.selected_card), enemy=True)
                            end_pos = ui.get_played_card_center(len(enemy.turn_played_cards), enemy=True)
                            animator.prepare_animation(animation_card_img, enemy.ENEMY_DISPLAY_TIME, start_pos, end_pos)

            elif enemy_turn_step == 3:
                elapsed = pygame.time.get_ticks() - enemy.enemy_card_start_time
                if enemy.selected_card in enemy.drawn_cards:
                    if elapsed <= enemy.ENEMY_DISPLAY_TIME:
                        played_card = enemy.selected_card
                        enemy.calc_damage(played_card, player)
                        index = enemy.drawn_cards.index(enemy.selected_card)
                        enemy.drawn_cards.pop(index)
                        enemy_turn_step = 4
                        enemy.enemy_card_start_time = pygame.time.get_ticks()
                        enemy.selected_card = None  # deselect immediately
                        selected = None
                    else:
                        played_card = enemy.selected_card
                        enemy.calc_damage(played_card, player)
                        index = enemy.drawn_cards.index(enemy.selected_card)
                        enemy.drawn_cards.pop(index)
                        enemy_turn_step = 4
                        enemy.enemy_card_start_time = pygame.time.get_ticks()
                        enemy.selected_card = None
                        selected = None

            elif enemy_turn_step == 4:
                # ANIMATION
                elapsed = pygame.time.get_ticks() - enemy.enemy_card_start_time
                if elapsed <= enemy.ENEMY_DISPLAY_TIME:
                    animator.play_card_animation(elapsed)
                else:
                    enemy_turn_step = 5
                    enemy.turn_played_cards.append(played_card)
                    played_card = None

            elif enemy_turn_step == 5:
                if enemy.mana < 0:
                    enemy_turn_step = 6
                elif len(enemy.drawn_cards) == 0:
                    new_cards = enemy.processes_drawing(1)
                    if new_cards:
                        enemy.drawn_cards.extend(new_cards)
                        enqueue_draw_animations_for_new_cards(enemy, new_cards)
                    enemy.mana -= 1
                else:
                    enemy_turn_step = 1

            if enemy_turn_step == 6:
                new_cards = player.processes_drawing(1)
                player.drawn_cards.extend(new_cards)
                enqueue_draw_animations_for_new_cards(player, new_cards)
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