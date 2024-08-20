# Imports
import pygame.font
from functions import *
from object_classes import *
from level_codes import *
import sys
import os

if getattr(sys, 'frozen', False):
    app_path = os.path.dirname(sys.executable)
else:
    app_path = os.path.dirname(os.path.abspath("levels.txt"))
print(app_path)

# Initialize
pygame.init()

run = True
level_code_list = [level_1, level_2, level_3, level_4, level_5, level_6, level_7, level_8, level_9, level_10]
current_level = 10
level_bookmark = 0
extra_screens = 'none'
start_detect = True
points = 0
lives = 3
heart_1_motion = 15
heart_2_motion = -15
ball_x = random.choice([1, -1])
ball_y = -1
y_dir = -1
x_dir = 0
cross_hair = 2
is_moving = False
file_levels = []
scores = []


# -------------------------------------------------------main(Or at least, should be)----------------------------------
# Normal vars
def main():
    global current_level, heart_1_motion, heart_2_motion, run, extra_screens, start_detect, points, ball_x, ball_y
    global is_moving, level_bookmark, x_dir, y_dir, cross_hair, lives, level_code_list, file_levels, scores
    run = True
    level_code_list = [level_1, level_2, level_3, level_4, level_5, level_6, level_7, level_8, level_9, level_10]
    current_level = 1
    level_bookmark = 0
    extra_screens = 'start'
    start_detect = True
    points = 0
    lives = 3
    heart_1_motion = 15
    heart_2_motion = -15
    ball_x = random.choice([1, -1])
    ball_y = -1
    y_dir = -1
    x_dir = 0
    cross_hair = 3
    is_moving = False
    skip_to_level = 1
    high_score = 0

    file_levels = []
    with open("levels.txt", "r") as file:
        level = file.readline()
        while level:
            level.strip()
            file_levels.append(level)
            level = file.readline()
    if len(file_levels) > 0:
        for a in file_levels:
            if a == '\n':
                file_levels.remove(a)
        skip_to_level = int(file_levels[-1])

    scores = []
    with open("scores.txt", "r") as dox:
        score = dox.readline()
        while score:
            score.strip()
            if score != '\n':
                scores.append(int(score))
            score = dox.readline()
    if len(scores) > 0:
        high_score = max(scores)

    # Screen
    screen = pygame.display.set_mode((s_width, s_height))

    # Heart movement USER EVENT
    h_event = pygame.USEREVENT + 1
    pygame.time.set_timer(h_event, 250)

    # Objects
    paddle = Paddle()
    ball = Ball()

    # Groups containing the sprites of every level
    lv_groups = []
    for y in range(len(level_code_list)):
        group = pygame.sprite.Group(paddle, ball)
        lv_groups.append(group)

    # Creating sprites for all levels and adding to groups
    for index in range(len(lv_groups)):
        decipher(level_code_list[index], lv_groups[index])

    # Except the ball
    except_ball_group_list = []
    for y in range(len(level_code_list)):
        group = pygame.sprite.Group()
        except_ball_group_list.append(group)

    for index in range(len(except_ball_group_list)):
        create_except_ball(ball, lv_groups[index], except_ball_group_list[index])

    # Immovable lists
    immovable_object_group_list = []
    for ind in range(len(level_code_list)):
        immovable_object_group_list.append(pygame.sprite.Group())

    for ind in range(len(except_ball_group_list)):
        for item in except_ball_group_list[ind]:
            if item.id == 'IM':
                except_ball_group_list[ind].remove(item)
                immovable_object_group_list[ind].add(item)

    # Ball group
    ball_group = pygame.sprite.Group(ball)

    # Pause screen sprites
    pause_bg = ExtraBG(s_width, s_height - 650, 216, 247, 213)
    game_font = pygame.font.SysFont('Arial', 35)
    end_font = pygame.font.SysFont('Arial', 60)
    line1 = game_font.render('Press R to resume the game', False, (66, 69, 245))
    line3 = game_font.render('Highest score: ' + str(high_score), False, (66, 69, 245))

    # Start screen sprites
    start_line_1 = game_font.render('Else, press S to start the game.', False, (255, 48, 55))
    start_line_2 = game_font.render('Press P to pause the game', False, (79, 120, 255))
    start_line_3 = game_font.render('Press the space-bar to launch the sprites', False, (84, 255, 69))
    start_line_4 = game_font.render('Hit the ball with as many blocks as you can!', False, (167, 4, 189))
    start_line_5 = game_font.render('If you want to start from where you left off, click Q.', False, (255, 48, 55))
    start_bg = ExtraBG(s_width, s_height - 530, 216, 247, 213)

    # End screen sprites
    end_bg = EndBG()
    retry = Retry()

    # Hearts
    heart_1 = Heart(s_width - 40, 350)
    heart_2 = Heart(s_width - 40, 400)
    heart_3 = Heart(s_width - 40, 450)
    hearts = [heart_3, heart_2, heart_1]

    # ---------------------------------------------------------------Functions----------------------------------------
    # Wall bounce
    def ball_wall_bounce():
        global ball_y, ball_x, is_moving, start_detect, lives

        # Top wall
        if ball.rect.top < 0:
            ball_y = -ball_y

        # Side walls
        elif ball.rect.left < 0 or ball.rect.right > s_width:
            ball_x = -ball_x

        # Bottom wall
        if ball.rect.top > s_height:
            is_moving = False
            start_detect = True
            lives -= 1
            hearts.remove(random.choice(hearts))
            reset()

    # def ball motion
    def ball_block_bounce(coll_sprite):
        global ball_y, ball_x, points, cross_hair, y_dir, x_dir

        if ball_y < 0:
            y_dir = -1
        else:
            y_dir = 1

        if x_dir < 0:
            x_dir = -1
        else:
            x_dir = 1

        # Collide with enemy's right
        if (coll_sprite.rect.right - cross_hair < ball.rect.left < coll_sprite.rect.right) and \
                ((coll_sprite.rect.top < ball.rect.top < coll_sprite.rect.bottom)
                 or
                 (coll_sprite.rect.top < ball.rect.bottom < coll_sprite.rect.bottom)):
            ball_x = -ball_x

        # Collide with enemy's left
        elif (coll_sprite.rect.left + cross_hair > ball.rect.right > coll_sprite.rect.left) and \
                ((coll_sprite.rect.top < ball.rect.top < coll_sprite.rect.bottom)
                 or
                 (coll_sprite.rect.top < ball.rect.bottom < coll_sprite.rect.bottom)):
            ball_x = -ball_x

        # Collide with enemy's bottom
        if (coll_sprite.rect.bottom - cross_hair < ball.rect.top < coll_sprite.rect.bottom) and \
                ((coll_sprite.rect.left < ball.rect.left < coll_sprite.rect.right)
                 or
                 (coll_sprite.rect.left < ball.rect.right < coll_sprite.rect.right)) and y_dir == -1:
            ball_y = -ball_y

        # Collide with enemy's top
        elif (coll_sprite.rect.top + cross_hair > ball.rect.bottom > coll_sprite.rect.top) and \
                ((coll_sprite.rect.left < ball.rect.left < coll_sprite.rect.right)
                 or
                 (coll_sprite.rect.left < ball.rect.right < coll_sprite.rect.right)) and y_dir == 1:
            ball_y = -ball_y

    def destroy_blocks():
        global points
        # Block and paddle bounce
        for block in except_ball_group_list[current_level - 1]:
            # Except_ball_group is the except_ball_group of the current level

            if pygame.sprite.spritecollideany(block, ball_group):
                # Except_ball_group[index] stands for the object in this group

                ball_block_bounce(block)

                if block != paddle:
                    points += 1
                    lv_groups[current_level - 1].remove(block)
                    except_ball_group_list[current_level - 1].remove(block)

        for im_block in immovable_object_group_list[current_level - 1]:
            if pygame.sprite.spritecollideany(im_block, ball_group):
                ball_block_bounce(im_block)

    # Detect events
    def detect_esc():
        global run, is_moving, start_detect, ball_x, ball_y, level_bookmark, current_level, extra_screens
        global heart_1_motion, heart_2_motion

        # Detection
        for event in pygame.event.get():
            if event.type == QUIT:
                run = False

            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    run = False

                # Movement
                if event.key == K_SPACE and start_detect and extra_screens != 'pause' and extra_screens != 'start':
                    is_moving = True
                    start_detect = False
                    ball_x = random.choice([1, -1])
                    ball_y = -1

                # Pause detect
                if event.key == K_p:
                    # Level bookmarks
                    extra_screens = 'pause'
                    is_moving = False
                    file_levels.append(str(current_level))

                # Resume detect
                if event.key == K_r and extra_screens == 'pause':
                    extra_screens = 'none'
                    is_moving = True

                # Game start detect
                if event.key == K_s and extra_screens == 'start':
                    extra_screens = 'none'

                # Easy start
                if event.key == K_q and extra_screens == 'start':
                    current_level = skip_to_level
                    extra_screens = 'none'

            # Hearts motion
            if event.type == h_event:
                heart_1.rect.move_ip(heart_1_motion, 0)
                heart_2.rect.move_ip(heart_2_motion, 0)
                heart_3.rect.move_ip(heart_1_motion, 0)
                heart_1_motion = -heart_1_motion
                heart_2_motion = -heart_2_motion

            # Retry click
            if extra_screens == 'end':
                if retry.rect.collidepoint(pygame.mouse.get_pos()):
                    retry.image = pygame.transform.smoothscale(retry.image, (240, 110))
                    retry.rect = retry.image.get_rect(center=retry.rect.center)
                    if event.type == MOUSEBUTTONDOWN:
                        file_levels.append(str(current_level))
                        with open("levels.txt", "w") as lv_fl:
                            for z in file_levels:
                                lv_fl.writelines(z)
                                lv_fl.writelines('\n')
                        scores.append(points)
                        with open("scores.txt", "w") as sc_fl:
                            for z in scores:
                                sc_fl.writelines(str(z))
                                sc_fl.writelines('\n')
                        main()
                else:
                    retry.image = pygame.transform.smoothscale(retry.image, (220, 100))
                    retry.rect = retry.image.get_rect(center=retry.rect.center)

    # Switching levels
    def switch_levels():
        global current_level, is_moving, start_detect
        if len(except_ball_group_list[current_level - 1]) == 1:
            current_level += 1
            # Reassigning booleans
            is_moving = False
            start_detect = True

    # Level blit
    def level_blit():
        for spr in lv_groups[current_level - 1]:
            screen.blit(spr.image, spr.rect)

    # Reset
    def reset():
        if not is_moving and extra_screens != 'pause':
            paddle.rect.center = (s_width / 2, s_height - 70)
            ball.rect.center = (s_width / 2, s_height - 105)

    # Everything in a level
    def level_stuff():
        reset()
        detect_esc()
        destroy_blocks()
        level_blit()
        switch_levels()

    # Main loop

    while run:
        # Screen fill
        screen.fill((0, 0, 0))

        # Presses
        pressed = pygame.key.get_pressed()

        # Level1
        if current_level == 1:
            detect_esc()
            switch_levels()
            destroy_blocks()
            level_blit()

        # All levels in between
        elif current_level in range(2, len(level_code_list)):
            level_stuff()

        # The last level
        elif current_level == len(level_code_list):
            detect_esc()
            reset()
            destroy_blocks()
            level_blit()
            if len(except_ball_group_list[current_level - 1]) == 1:
                extra_screens = 'end'
                is_moving = False

        # Pause screen
        if extra_screens == 'pause':
            # BG
            screen.blit(pause_bg.image, pause_bg.rect)
            pause_bg.rect.move_ip(0, 3)
            if pause_bg.rect.centery > s_height / 2:
                pause_bg.rect.centery = s_height / 2

            line2 = game_font.render('Your score ' + str(points), False, (66, 69, 245))
            if pause_bg.rect.centery > s_width / 2 - 5:
                screen.blit(line1, (150, 335))
                screen.blit(line2, (250, 385))
                screen.blit(line3, (230, 435))

        elif extra_screens != 'pause':
            pause_bg.rect.centery = -s_height / 2

        # End screen
        if extra_screens == 'end':
            # Killing hearts
            for y in hearts:
                hearts.remove(y)
            # BG
            end_bg.rect.move_ip(0, 2)
            if end_bg.rect.bottom > s_height:
                end_bg.rect.bottom = s_height

            # Congrats line
            if len(except_ball_group_list[-1]) == 1:
                congrats_line = end_font.render('Congrats! You win!', False, (255, 255, 255))
            else:
                congrats_line = end_font.render('Level reached: ' + str(current_level), False, (255, 255, 255))
            # Point line
            point_line = end_font.render('Your score: ' + str(points), False, (255, 255, 255))
            # Blit
            screen.blit(end_bg.image, end_bg.rect)
            if end_bg.rect.bottom > 0.75 * s_height:
                screen.blit(point_line, (200, 360))
                screen.blit(congrats_line, (160, 420))
                screen.blit(retry.image, retry.rect)

        # Start screen
        if extra_screens == 'start':
            # BG
            start_bg.rect.move_ip(0, 2)
            if start_bg.rect.centery > s_height / 2:
                start_bg.rect.centery = s_height / 2
            screen.blit(start_bg.image, start_bg.rect)

            if start_bg.rect.centery > s_height / 2 - 5:
                screen.blit(start_line_1, (130, 320))
                screen.blit(start_line_2, (170, 370))
                screen.blit(start_line_3, (90, 420))
                screen.blit(start_line_4, (70, 470))
                screen.blit(start_line_5, (30, 270))

        # Wall bounce
        ball_wall_bounce()

        # Paddle movement
        if is_moving:
            paddle.paddle_motion(pressed, 2 * abs(ball_x))
            ball.rect.move_ip(ball_x, ball_y)

        # Movables motion
        for y in lv_groups[current_level - 1]:
            if y.id == 'MB':
                y.motion()
                if pygame.sprite.collide_rect(y, ball):
                    lv_groups[current_level - 1].remove(y)
                if pygame.sprite.spritecollideany(y, immovable_object_group_list[current_level - 1]):
                    y.vel = -y.vel

        # Hearts
        if extra_screens != 'start':
            for y in hearts:
                screen.blit(y.image, y.rect)

        # Game over
        if lives == 0:
            extra_screens = 'end'
            is_moving = False

        # Flip
        pygame.display.flip()
        pygame.time.Clock().tick(750)


# Final call
main()

file_levels.append(str(current_level))
with open("levels.txt", "w") as fl:
    for x in file_levels:
        fl.writelines(x)
        fl.writelines('\n')

scores.append(points)
with open("scores.txt", "w") as c:
    for x in scores:
        c.writelines(str(x))
        c.writelines('\n')