from turtle import Turtle


class Menu(Turtle):
    """A simple menu system for choosing game mode and CPU difficulty."""

    def __init__(self):
        super().__init__()
        self.color("green")
        self.penup()
        self.hideturtle()
        self.current_screen = "MAIN"

        # Draw the main menu on initialization.
        self.show_main_menu()

    # ----------------------------------------------------------- #
    # MAIN MENU
    # ----------------------------------------------------------- #
    def show_main_menu(self):
        """Displays title and initial game mode options."""
        self.clear()
        self.current_screen = "MAIN"

        # Title
        self.goto(0, 50)
        self.write("Snake", align="center", font=("Courier", 40, "bold"))

        # Start Game
        self.goto(0, -50)
        self.write("Press Start",
                   align="center", font=("Courier", 20, "normal"))

    def show_pause_menu(self):
        self.clear()
        self.goto(0, 120)
        self.write("Paused", align="center", font=("Courier", 30, "bold"))
        #
        # self.goto(0, 40)
        # self.write("Press R to Resume", align="center", font=("Courier", 20))
        #
        # self.goto(0, 0)
        # self.write("Press T to Restart Match", align="center", font=("Courier", 20))
        #
        # self.goto(0, -40)
        # self.write("Press M for Main Menu", align="center", font=("Courier", 20))

        # self.goto(0, -120)
        # self.write("Press B to Back", align="center", font=("Courier", 20))

    # In menu.py
    def show_game_over(self):
        """Display game over screen with winner and options."""
        self.current_screen = "GAME_OVER"
        self.clear()
        self.goto(0, 50)
        self.write(f"Game Over", align="center", font=("Courier", 30, "bold"))
        self.goto(0, -20)
        self.write("Press N to Restart Match", align="center", font=("Courier", 20, "normal"))
        self.goto(0, -60)
        self.write("Press M for Main Menu", align="center", font=("Courier", 20, "normal"))

    # ----------------------------------------------------------- #
    # CLEAR MENU
    # ----------------------------------------------------------- #
    def clear_menu(self):
        """Erase all menu text before starting the game."""
        self.clear()
