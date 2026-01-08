from turtle import Turtle
import os

# Absolute path for data.txt
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "data.txt")


class Scoreboard(Turtle):

    def __init__(self):
        super().__init__()
        self.color("white")
        self.penup()
        self.hideturtle()
        self.goto(0, 270)
        self.score = 0

        # Ensure data file exists
        if not os.path.exists(DATA_FILE):
            with open(DATA_FILE, "w") as f:
                f.write("0")

        # Load high score
        with open(DATA_FILE) as data:
            self.high_score = int(data.read())

        self.update_score()

    def update_score(self):
        self.clear()
        self.write(arg=f"Score: {self.score} High Score: {self.high_score}",
                   align="center", font=('Arial', 18, 'bold'))

    def restart(self):
        """Reset current score and save high score if needed"""
        self.save_high_score()
        self.score = 0
        self.update_score()

    def increase_score(self):
        self.score += 1
        self.update_score()

    def save_high_score(self):
        """Save the high score to data.txt if current score is higher"""
        if self.score > self.high_score:
            self.high_score = self.score
            with open(DATA_FILE, mode="w") as data:
                data.write(f"{self.high_score}")
