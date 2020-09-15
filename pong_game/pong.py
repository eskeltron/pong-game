import pygame
import sys

pygame.init()

black = (0, 0, 0)
white = (255, 255, 255)
green = (0, 255, 0)
red   = (255, 0 , 0)

screen_size = (800, 600)

screen = pygame.display.set_mode(screen_size)
clock  = pygame.time.Clock()

height_player = 90
width_player = 15

player_one_pos = []
player_two_pos = []

player_one_speed = 0
player_two_speed = 0

player_one_score = 0
player_two_score = 0

ball_pos = []
ball_radius = 4
ball_speed = []

ball = None
player_one = None
player_two = None


def calculate_ball_direction(player_speed, touch_mid = False, is_player_one = True):
    global ball_speed

    if player_speed < 0:
        ball_speed[1] = -4
    elif player_speed > 0:
        ball_speed[1] = 4
    else:
        ball_speed[1] = 0

    if touch_mid:
        ball_speed[0] = 6 if is_player_one else -6 
    else:
        ball_speed[0] = 4 if is_player_one else -4

def ball_touch_player(ball, player, player_speed, is_player_one ):
    colision = ball.colliderect(player)
    third_part_player = height_player / 3
    player_touched = False
    if colision:
        if ball.y >= player.top + third_part_player and ball.y <= player.top + third_part_player * 2:
            calculate_ball_direction(player_speed, touch_mid=True, is_player_one = is_player_one)
            player_touched = True
        elif ball.y >= player.top and ball.y <= player.top + height_player:
            calculate_ball_direction(player_speed, touch_mid=False, is_player_one = is_player_one)
            player_touched = True
    return player_touched
def verify_if_ball_touch_player(ball, player, player_speed, playerOne = False):
    return ball_touch_player(ball, player, player_speed, playerOne)

def initialize_game(initialize_scores = True):
    global ball_pos
    global player_one_pos
    global player_two_pos
    global ball_speed
    global player_one_score
    global player_two_score
    global player_one
    global player_two
    global ball
    ball_pos = [int(screen_size[0] * 0.5), int(screen_size[1] * 0.5)]
    ball = pygame.draw.circle(screen, white, ball_pos, ball_radius)
    player_one_pos = [int(screen_size[0] - screen_size[0] * 0.90), int(screen_size[1] * 0.5 - height_player / 2)]
    player_two_pos = [int(screen_size[0] - screen_size[0] * 0.10), int(screen_size[1] * 0.5 - height_player / 2)]
    player_one = pygame.draw.rect(screen, red, (player_one_pos[0], player_one_pos[1], width_player, height_player))
    player_two = pygame.draw.rect(screen, red, (player_two_pos[0], player_two_pos[1], width_player, height_player))

    ball_speed = [4, 0]
    if initialize_scores:
        player_one_score = 0
        player_two_score = 0

def scored():
    initialize_game(initialize_scores=False)

def player_touch_limits(player_speed, player_pos_y):
    player_touch_limit = False
    if player_speed < 0 and player_pos_y == 0:
        player_touch_limit = True
    elif player_speed > 0 and player_pos_y >= screen_size[1] - height_player:
        player_touch_limit = True
    return player_touch_limit


font_score = pygame.font.Font('retro_computer_personal_use.ttf', 13)
font_menu  = pygame.font.Font('retro_computer_personal_use.ttf', 25)
font_menu.set_bold(True)

player_one_score_rendered = font_score.render('Score player one : 0', False, white)
player_two_score_rendered = font_score.render('Score player two : 0', False, white)
player_two_score_rendered = font_score.render('Score player two : 0', False, white)

exit_rendered = font_menu.render('EXIT', False, red)
play_rendered = font_menu.render('PLAY NOW', False, white)
resume_rendered = font_menu.render('RESUME', False, white)

exit_pos   = [int(screen_size[0] * 0.5 - exit_rendered.get_width() / 2), int(screen_size[1] * 0.7 - 25)]
play_pos   = [int(screen_size[0] * 0.5 - play_rendered.get_width() / 2), int(screen_size[1] * 0.3 - 25)]
resume_pos = [int(screen_size[0] * 0.5 - resume_rendered.get_width() / 2), int(screen_size[1] * 0.3 - 25)]

def view_menu_stop():
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos_mouse = pygame.mouse.get_pos()
                if resume_rendered.get_rect(topleft=resume_pos).collidepoint(pos_mouse):
                    waiting = False
                elif exit_rendered.get_rect(topleft=exit_pos).collidepoint(pos_mouse):
                    pygame.quit()
                    sys.exit()
                    
        screen.fill(black)

        screen.blit(exit_rendered, exit_pos)
        screen.blit(resume_rendered, resume_pos)

        pygame.display.flip()
        clock.tick(60)

def view_game():
    global player_one_score
    global player_two_score
    global player_one_speed
    global player_two_speed
    global player_one_pos
    global player_two_pos
    global player_one_score_rendered
    global player_two_score_rendered
    global ball;
    global player_one;
    global player_two;
    game_finished = False
    restart_positions = False
    while not game_finished:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    view_menu_stop()
                if event.key == pygame.K_w:
                    player_one_speed = -5
                elif event.key == pygame.K_s:
                    player_one_speed = 5
                elif event.key == pygame.K_UP:
                    player_two_speed = -5
                elif event.key == pygame.K_DOWN:
                    player_two_speed = 5
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_w:
                    player_one_speed = 0
                elif event.key == pygame.K_s:
                    player_one_speed = 0
                elif event.key == pygame.K_UP:
                    player_two_speed = 0
                elif event.key == pygame.K_DOWN:
                    player_two_speed = 0

        if player_touch_limits(player_one_speed, player_one_pos[1]):
            player_one_speed = 0.0
        if player_touch_limits(player_two_speed, player_two_pos[1]):
            player_two_speed = 0.0

        #Calculate if ball touch any border or if player scored
        
        if ball_pos[0] <= 0:
            player_two_score += 1
            restart_positions = True
            player_two_score_rendered = font_score.render('Score player two : {}'.format(player_two_score), False, white)
        elif ball_pos[0] >= screen_size[0]:
            player_one_score += 1
            player_one_score_rendered = font_score.render('Score player one : {}'.format(player_one_score), False, white)
            restart_positions = True
        if ball_pos[1] <= 0 or ball_pos[1] >= screen_size[1]:
            ball_speed[1] *=-1

        if player_one_score == 3 or player_two_score == 3:
            game_finished = True;

        if restart_positions:
            scored()
            restart_positions = False

        if not verify_if_ball_touch_player(ball, player_one, player_one_speed, playerOne = True):
            verify_if_ball_touch_player(ball, player_two, player_two_speed)
        
        screen.fill(black)

        player_one_pos_x = player_one_pos[0]
        player_one_pos[1] += player_one_speed
        player_one_pos_y = player_one_pos[1]
        
        player_two_pos_x = player_two_pos[0]
        player_two_pos[1] += player_two_speed
        player_two_pos_y = player_two_pos[1]

        ball_pos[0] += ball_speed[0]
        ball_pos[1] += ball_speed[1]

        ball = pygame.draw.circle(screen, white, ball_pos, ball_radius)
        
        player_one = pygame.draw.rect(screen, red, (int(player_one_pos_x), int(player_one_pos_y), width_player, height_player))
        player_two = pygame.draw.rect(screen, red, (int(player_two_pos_x), int(player_two_pos_y), width_player, height_player))


        screen.blit(player_one_score_rendered, [int(screen_size[0] * 0.2), 10])
        screen.blit(player_two_score_rendered, [int(screen_size[0] * 0.6), 10])

        pygame.display.flip()
        clock.tick(60)

def view_menu_screen():
    menu_screen = True
    while menu_screen:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos_mouse = pygame.mouse.get_pos()
                if play_rendered.get_rect(topleft=play_pos).collidepoint(pos_mouse):
                    initialize_game()
                    view_game()
                elif exit_rendered.get_rect(topleft=exit_pos).collidepoint(pos_mouse):
                    pygame.quit()
                    sys.exit()
                    
        screen.fill(black)

        screen.blit(exit_rendered, exit_pos)
        screen.blit(play_rendered, play_pos)

        pygame.display.flip()
        clock.tick(60)

view_menu_screen()