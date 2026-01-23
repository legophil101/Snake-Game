from turtle import Screen
import time
from menu import Menu
from snake import Snake
from food import Food
from scoreboard import Scoreboard
import pygame
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
pygame.mixer.init()

# Sound effects
intro_sound = pygame.mixer.Sound(
    os.path.join(BASE_DIR, "sounds", "snake_game_intro.wav")
)

eat_sound = pygame.mixer.Sound(
    os.path.join(BASE_DIR, "sounds", "snake_game_food.wav")
)

game_over_sound = pygame.mixer.Sound(
    os.path.join(BASE_DIR, "sounds", "snake_game_game_over.wav")
)

screen = Screen()
screen.setup(width=600, height=600)
screen.bgcolor("black")
screen.title("Snake Game")
screen.tracer(0)

# Create menu (shown at the start)
menu = Menu()
game_state = "MENU"  # Can be "MENU", "PLAYING", "PAUSED", or "GAME_OVER"

# Initialize safety fix:
# In the game loop, if the game has just started and the user hasn't pressed "Enter,"
# the variables (snake, food, scoreboard) may not exist yet, leading to a NameError.
snake = None
food = None
scoreboard = None


# ----------------------------------------------
# START GAME — called after menu selection
# ----------------------------------------------
def start_game():
    global game_state, snake, food, scoreboard

    if game_state != "MENU":
        return

    menu.clear_menu()
    game_state = "PLAYING"

    # Always ensure old objects are gone before making new ones
    cleanup_game_objects()

    # Stop intro music
    intro_sound.stop()

    snake = Snake()
    food = Food()
    food.showturtle()  # Ensure food is visible
    scoreboard = Scoreboard()
    scoreboard.update_score()

    # Bind movement
    screen.onkey(snake.up, "Up")
    screen.onkey(snake.down, "Down")
    screen.onkey(snake.left, "Left")
    screen.onkey(snake.right, "Right")


def trigger_game_over():
    global game_state
    if game_state == "PLAYING":
        # Save high score first
        if scoreboard:
            scoreboard.save_high_score()

        game_state = "GAME_OVER"
        pygame.mixer.stop()
        game_over_sound.play()
        menu.show_game_over()


def cleanup_game_objects():
    """Hide snake, food, and scoreboard to prevent duplication."""
    global snake, food, menu, scoreboard
    try:
        # Hide the snake segments properly
        if snake:
            for segment in snake.segments:
                segment.hideturtle()

        if food:
            food.hideturtle()

        if menu:
            menu.clear_menu()

        if scoreboard:
            scoreboard.clear()


    except (NameError, AttributeError):
        pass


def toggle_pause():
    global game_state
    if game_state == "PLAYING":
        game_state = "PAUSED"
        menu.show_pause_menu()
    elif game_state == "PAUSED":
        resume_game()


def resume_game():
    global game_state
    game_state = "PLAYING"
    menu.clear()


def handle_return_key():
    global game_state
    if game_state == "MENU":
        start_game()


def handle_m_key():
    global game_state
    if game_state == "GAME_OVER":
        # Save high score before going back to menu
        if scoreboard:
            scoreboard.save_high_score()

        cleanup_game_objects()
        menu.clear()
        game_state = "MENU"


def handle_n_key():
    """Logic for Restarting the game (N key)"""
    global game_state, snake, food
    if game_state == "GAME_OVER":
        cleanup_game_objects()

        # Reset the Scoreboard
        scoreboard.restart()

        # Reset the Snake
        snake = Snake()  # Create a fresh snake

        # FIX: Make the food visible and move it to a new spot
        food.showturtle()
        food.refresh()

        # Re-bind keys to the NEW snake object
        screen.onkey(snake.up, "Up")
        screen.onkey(snake.down, "Down")
        screen.onkey(snake.left, "Left")
        screen.onkey(snake.right, "Right")

        game_state = "PLAYING"


screen.listen()
screen.onkey(handle_return_key, "Return")
screen.onkey(handle_m_key, "m")
screen.onkey(handle_n_key, "n")
screen.onkey(toggle_pause, "p")

game_is_on = True

menu_drawn = False

# Play intro sound
intro_sound.play(loops=-1)

while game_is_on:
    screen.update()
    if game_state == "MENU":

        if not menu_drawn:
            menu.clear()
            menu.show_main_menu()
            menu_drawn = True
        continue
    else:
        menu_drawn = False

    if game_state == "PLAYING":
        time.sleep(0.1)
        snake.move()

        # Detect collision with food.
        if snake.head.distance(food) < 15:
            food.refresh()
            snake.extend()
            scoreboard.increase_score()
            eat_sound.play()

        # Detect collision with wall.
        if snake.head.xcor() > 280 or snake.head.xcor() < -280 or snake.head.ycor() > 280 or snake.head.ycor() < -280:
            trigger_game_over()

        # Detect collision with tail.
        for segment in snake.segments[1:]:
            if snake.head.distance(segment) < 10:
                trigger_game_over()

screen.exitonclick()
