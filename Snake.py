# import modules
import random
import os
import pygame as pg

pg.mixer.init()
pg.mixer.music.load("Back.mp3")
pg.mixer.music.play()

display = pg.display
# initializing of all pygame module's all module
z = pg.init()

# colors
white = (255, 255, 255)
red = (255, 0, 0)
black = (0, 0, 0)
green = (0, 255, 0)
unknown = (255, 240, 179)
unknown2 = (96, 96, 96)
unknown3 = (245, 245, 245)

# creating windows
screen_width = 750
screen_height = 750
game_window = display.set_mode((screen_width, screen_height))

# images
welcomeimage = pg.image.load("Welcome.png")
welcomeimage = pg.transform.scale(welcomeimage, (screen_width, screen_height)).convert_alpha()

# game title
display.set_caption("Snakes")
display.update()

exit_game = False
over_game = False

clock = pg.time.Clock()  # clock for a game

pg.font.init()
font = pg.font.Font("PlayfairDisplay-BoldItalic.ttf", 40)
font1 = pg.font.Font("PlayfairDisplay-BoldItalic.ttf", 55)
font2 = pg.font.Font("PlayfairDisplay-BoldItalic.ttf", 100)


def text_screen(text, color, x, y, f):
    scree_text = f.render(text, True, color)
    game_window.blit(scree_text, [x, y])


def snake_plot(game_window, color, snake_list, snake_size):
    for x, y in snake_list:
        pg.draw.rect(game_window, color, [x, y, snake_size, snake_size])


# welcome screen
def welcome():
    exit_game = False

    while not exit_game:
        pg.mixer.music.load("Back.mp3")
        pg.mixer.music.play()

        game_window.blit(welcomeimage, (0, 0))

        for event in pg.event.get():
            if event.type == pg.QUIT:
                exit_game = True

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    gameloop()

        pg.display.update()
        clock.tick(60)


# creating a game loop
def gameloop():
    # specific variables
    exit_game = False
    over_game = False

    game_width = 500
    game_height = 500

    snake_x = 250
    snake_y = 250

    snake_size = 10

    velocity_x = 0
    velocity_y = 0
    init_velocity = 5

    food_x = random.randint(125, 615)
    food_y = random.randint(150, 640)

    fps = 30

    score = 0

    snake_list = []
    snake_length = 1

    if not (os.path.exists("high_score.txt")):
        with open("high_score.txt", "w") as f:
            f.write(str(0))

    with open("high_score.txt", "r") as f:
        high_score = f.read()

    while not exit_game:
        if over_game:
            with open("high_score.txt", "w") as f:
                f.write(str(high_score))

            # game over screen
            game_window.fill(unknown3)
            text_screen("Game Over", unknown2, 120, 250, font2)
            text_screen("Press Enter to Continue", unknown2, 75, 360, font1)
            text_screen("Your Score: " + str(score), unknown2, 250, 430, font)
            text_screen("High-Score: " + str(high_score), unknown2, 240, 480, font)

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    exit_game = True

                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_RETURN:
                        welcome()

        else:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    exit_game = True

                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_UP:
                        velocity_y = -init_velocity
                        velocity_x = 0

                    if event.key == pg.K_DOWN:
                        velocity_y = init_velocity
                        velocity_x = 0

                    if event.key == pg.K_RIGHT:
                        velocity_x = init_velocity
                        velocity_y = 0

                    if event.key == pg.K_LEFT:
                        velocity_x = -init_velocity
                        velocity_y = 0

            snake_x = snake_x + velocity_x
            snake_y = snake_y + velocity_y

            # if snake will eat the food
            if abs(food_x - snake_x) < 5 and abs(food_y - snake_y) < 5:
                # score increasing
                score = score + 1

                # music when snake will eat food
                pg.mixer.music.load("Beep.mp3")
                pg.mixer.music.play()

                # new food
                food_x = random.randint(125, 615)
                food_y = random.randint(150, 640)

                # after eating food snake length will increase
                snake_length = snake_length + 1

                # about high-score
                if score > int(high_score):
                    high_score = score

            # background
            game_window.fill(unknown)
            pg.draw.rect(game_window, black, [115, 90, game_width + 20, game_height + 70])
            pg.draw.rect(game_window, green, [125, 150, game_width, game_height])

            # score
            text_screen("Score: " + str(score), red, 130, 90, font)
            text_screen("High-Score: " + str(high_score), red, 350, 90, font)

            # food maker
            pg.draw.rect(game_window, red, [food_x, food_y, 10, 10])

            # snake body
            head = []
            head.append(snake_x)
            head.append(snake_y)
            snake_list.append(head)

            if len(snake_list) > snake_length:
                del snake_list[0]

            # if snake eat own body
            if head in snake_list[:-1]:
                over_game = True
                pg.mixer.music.load("End.mp3")
                pg.mixer.music.play()

            # if snake try to goes out of the range
            if snake_x < 125 or snake_x > 615 or snake_y < 150 or snake_y > 640:
                over_game = True
                pg.mixer.music.load("End.mp3")
                pg.mixer.music.play()

            # where will run body of snake
            snake_plot(game_window, black, snake_list, snake_size)

        display.update()
        clock.tick(fps)

    pg.quit()
    quit()


welcome()
