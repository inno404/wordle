import tkinter as tk
from tkinter import messagebox
import random
import time

class WordleApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Wordle Game")
        self.master.geometry("400x300")

        self.word = self.generate_word()
        self.guesses_left = 6
        self.guess = tk.StringVar()
        self.hint_count = 3
        self.score = 0
        self.timer_running = False

        self.init_widgets()
        self.start_timer()

    def init_widgets(self):
        self.word_label = tk.Label(self.master, text=self.hide_word(), font=("Arial", 20))
        self.word_label.pack(pady=10)

        self.guess_entry = tk.Entry(self.master, textvariable=self.guess, font=("Arial", 12), width=20)
        self.guess_entry.pack(pady=10)

        self.guess_button = tk.Button(self.master, text="Guess", command=self.check_guess, font=("Arial", 12), bg="lightblue")
        self.guess_button.pack()

        self.hint_button = tk.Button(self.master, text="Hint", command=self.reveal_hint, font=("Arial", 12), bg="lightgreen")
        self.hint_button.pack()

        self.score_label = tk.Label(self.master, text=f"Score: {self.score}", font=("Arial", 12))
        self.score_label.pack()

        self.info_label = tk.Label(self.master, text=f"Guesses Left: {self.guesses_left}", font=("Arial", 12))
        self.info_label.pack()

    def start_timer(self):
        self.timer_running = True
        self.remaining_time = 60
        self.timer_label = tk.Label(self.master, text=f"Time Left: {self.remaining_time} seconds", font=("Arial", 12))
        self.timer_label.pack(pady=10)
        self.update_timer()

    def update_timer(self):
        if self.remaining_time <= 0:
            self.timer_label.config(text="Time's up!")
            self.timer_running = False
            self.master.after(1000, self.end_game)
        elif self.timer_running:
            self.remaining_time -= 1
            self.timer_label.config(text=f"Time Left: {self.remaining_time} seconds")
            self.master.after(1000, self.update_timer)

    def generate_word(self):
        words = ["apple", "banana", "cherry", "orange", "grape"]
        return random.choice(words)

    def hide_word(self):
        return ' '.join(['*' for _ in self.word])

    def check_guess(self):
        if not self.timer_running:
            return

        guess = self.guess.get().lower()
        if len(guess) != len(self.word):
            messagebox.showerror("Error", "Guess should have the same length as the word!")
            return

        self.guesses_left -= 1
        correct_guesses = sum(1 for x, y in zip(guess, self.word) if x == y)

        if correct_guesses == len(self.word):
            self.score += 10
            self.score_label.config(text=f"Score: {self.score}")
            messagebox.showinfo("Congratulations!", "You've guessed the word!")
            self.master.destroy()
        elif self.guesses_left == 0:
            messagebox.showinfo("Game Over", f"You've run out of guesses! The word was {self.word}.")
            self.master.destroy()
        else:
            self.info_label.config(text=f"Guesses Left: {self.guesses_left}")
            self.update_word_display(guess)

    def update_word_display(self, guess):
        word_display = ''
        for g, w in zip(guess, self.word):
            if g == w:
                word_display += g
            elif g in self.word:
                word_display += g.upper()
            else:
                word_display += '*'
            word_display += ' '
        self.word_label.config(text=word_display.strip())

    def reveal_hint(self):
        if self.hint_count > 0 and self.timer_running:
            hidden_indices = [i for i, letter in enumerate(self.word) if letter == '*']
            if hidden_indices:
                hint_index = random.choice(hidden_indices)
                self.word_label.config(text=self.word_label.cget("text")[:2*hint_index] +
                                              self.word[hint_index].upper() +
                                              self.word_label.cget("text")[2*hint_index+1:])
                self.hint_count -= 1
                messagebox.showinfo("Hint", f"A letter has been revealed! {self.hint_count} hints left.")
            else:
                messagebox.showinfo("Hint", "All letters have already been revealed!")
        elif not self.timer_running:
            messagebox.showinfo("Time's Up!", "No hints can be revealed after the game is over.")
        else:
            messagebox.showinfo("No Hints Left", "You have no more hints left.")

    def end_game(self):
        self.master.destroy()

def main():
    root = tk.Tk()
    app = WordleApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()