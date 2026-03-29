import tkinter as tk
from tkinter import ttk
import random
import time
import pygame
from typing import Optional

try:
    pygame.mixer.init()
except pygame.error:
    pass

def play_sound(file):
    try:
        pygame.mixer.Sound(file).play()
    except pygame.error:
        pass
    except FileNotFoundError:
        pass


class Game:
    def __init__(self, low, high, max_attempts):
        self.low = low
        self.high = high
        self.max_attempts = max_attempts
        self.num = random.randint(low, high)
        self.attempts = 0
        self.ai_low = low
        self.ai_high = high

    def check_guess(self, guess):
        self.attempts += 1

        if guess == self.num:
            score = self.max_attempts - self.attempts + 1
            return {"status": "win", "score": score}

        elif guess < self.num:
            self.ai_low = max(self.ai_low, guess + 1)
            return {"status": "low"}

        else:
            self.ai_high = min(self.ai_high, guess - 1)
            return {"status": "high"}

    def get_hint(self, guess):
        diff = abs(self.num - guess)
        if diff <= 2:
            return "Super Close!"
        elif diff <= 5:
            return "Very Close!"
        elif diff <= 10:
            return "Getting there..."
        else:
            return "Way off!"

    def get_ai(self):
        return (self.ai_low + self.ai_high) // 2


game: Optional[Game] = None
best_score = 0
streak = 0
mode = 1
start_time = 0


def start_game():
    global game, mode, start_time

    play_sound("click.wav")

    mode = int(mode_var.get())
    difficulty = diff_var.get()

    if difficulty == "Easy":
        low, high, max_attempts = 1, 10, 5
    elif difficulty == "Medium":
        low, high, max_attempts = 1, 20, 10
    elif difficulty == "Hard":
        low, high, max_attempts = 1, 50, 15
    else:
        low, high, max_attempts = 1, 100, 10

    game = Game(low, high, max_attempts)
    start_time = time.time()

    info_label.config(text=f"Guess a number between {low}-{high}.")
    result_label.config(text="Game Started!")

    progress['maximum'] = max_attempts
    progress['value'] = 0

    entry.config(state="normal")
    entry.delete(0, tk.END)


def check_guess():
    global best_score, streak, start_time

    if game is None:
        result_label.config(text="Press Start first!")
        return

    current_game = game

    try:
        guess = int(entry.get())
    except ValueError:
        result_label.config(text="Enter valid number")
        return

    if guess < current_game.low or guess > current_game.high:
        result_label.config(text="Out of range!")
        entry.delete(0, tk.END)
        return

    play_sound("click.wav")

    if mode == 3:
        if time.time() - start_time > 10:
            result_label.config(text="Too slow!")
            current_game.attempts += 1
            progress['value'] = current_game.attempts
            start_time = time.time()
            entry.delete(0, tk.END)
            return

    result = current_game.check_guess(guess)
    progress['value'] = current_game.attempts

    start_time = time.time()

    if result["status"] == "win":
        play_sound("win.wav")

        score = result["score"]
        msg = f"Correct! Score: {score}"

        if current_game.attempts == 1:
            msg += "\nFIRST TRY! GOD MODE!"

        result_label.config(text=msg)

        if score > best_score:
            best_score = score
            best_label.config(text=f"Best: {best_score}")

        streak += 1
        streak_label.config(text=f"Streak: {streak}")

        entry.config(state="disabled")
        entry.delete(0, tk.END)
        return

    if result["status"] == "low":
        msg = "📉 Too Low!"
    else:
        msg = "📈 Too High!"

    if mode != 2:
        hint = current_game.get_hint(guess)
        ai = current_game.get_ai()
        result_label.config(text=f"{msg}\n{hint}\nTry {ai}.")
    else:
        result_label.config(text=msg)

    if current_game.attempts >= current_game.max_attempts:
        play_sound("lose.wav")
        result_label.config(text=f"Game Over! Number was {current_game.num}.")
        streak = 0
        streak_label.config(text="Streak: 0")
        entry.config(state="disabled")

    entry.delete(0, tk.END)


# ---------------- UI ----------------
root = tk.Tk()
root.title("The Final Guess")
root.geometry("420x550")
root.configure(bg="#020617")

style = ttk.Style()
style.theme_use('default')
style.configure("TProgressbar", thickness=20)

tk.Label(root, text="🎮 THE FINAL GUESS",
         font=("Arial", 18, "bold"),
         fg="#22c55e", bg="#020617").pack(pady=10)

mode_var = tk.StringVar(value="1")
ttk.Combobox(root, textvariable=mode_var,
             values=["1", "2", "3"],
             state="readonly").pack()

diff_var = tk.StringVar(value="Easy")
ttk.Combobox(root, textvariable=diff_var,
             values=["Easy", "Medium", "Hard", "Boss"],
             state="readonly").pack(pady=5)

info_label = tk.Label(root, text="", fg="#38bdf8", bg="#020617")
info_label.pack()

entry = tk.Entry(root, font=("Arial", 14), justify="center")
entry.pack(pady=10)

tk.Button(root, text="Start", command=start_game,
          bg="#3b82f6", fg="white").pack()

tk.Button(root, text="Guess", command=check_guess,
          bg="#22c55e").pack(pady=5)

progress = ttk.Progressbar(root, length=300)
progress.pack(pady=10)

result_label = tk.Label(root, text="", fg="white", bg="#020617")
result_label.pack()

best_label = tk.Label(root, text="Best: 0", fg="#facc15", bg="#020617")
best_label.pack()

streak_label = tk.Label(root, text="Streak: 0", fg="#f97316", bg="#020617")
streak_label.pack()

tk.Label(root, text="Made by Azlan", fg="#64748b", bg="#020617").pack(pady=10)

root.mainloop()
