import os
import random
import tkinter as tk
from PIL import Image, ImageTk

QUESTIONS_DIR = "C:/Users/Radek/Desktop/FRM Part 2/Zadania obliczeniowe/Pytania_Komplet"
ANSWERS_DIR = "C:/Users/Radek/Desktop/FRM Part 2/Zadania obliczeniowe/Odpowiedzi_Komplet"


class QuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Quiz")

        # fullscreen
        self.root.state('zoomed')

        # obsługa zamknięcia
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        self.correct = 0
        self.incorrect = 0
        self.wrong_questions = []

        self.available_questions = self.load_questions()
        random.shuffle(self.available_questions)

        # === UKŁAD ===
        self.main_frame = tk.Frame(root)
        self.main_frame.pack(fill="both", expand=True)

        self.left_label = tk.Label(self.main_frame)
        self.left_label.pack(side="left", expand=True)

        self.right_label = tk.Label(self.main_frame)
        self.right_label.pack(side="right", expand=True)

        self.buttons_frame = tk.Frame(root)
        self.buttons_frame.pack()

        self.score_label = tk.Label(root, text="Dobrze: 0 | Źle: 0")
        self.score_label.pack()

        self.next_button = tk.Button(root, text="Dalej", command=self.next_question)

        self.current_question = None
        self.left_img = None
        self.right_img = None

        self.show_question()

    def load_questions(self):
        files = os.listdir(QUESTIONS_DIR)
        return [f for f in files if f.lower().endswith((".png", ".jpg", ".jpeg"))]

    def show_question(self):
        if not self.available_questions:
            self.end_quiz()
            return

        self.current_question = self.available_questions.pop()

        path = os.path.join(QUESTIONS_DIR, self.current_question)
        self.display_image(path, side="left")

        self.right_label.config(image="")  # wyczyść prawą stronę

        self.clear_buttons()

        for i in range(4):
            btn = tk.Button(
                self.buttons_frame,
                text=f"Odpowiedź {i+1}",
                command=self.show_answer,
                font=("Arial", 16),
                width=15,
                height=2
            )
            btn.pack(side=tk.LEFT, padx=20, pady=20)

    def show_answer(self):
        q_path = os.path.join(QUESTIONS_DIR, self.current_question)
        a_path = os.path.join(ANSWERS_DIR, self.current_question)

        self.display_image(q_path, side="left")
        self.display_image(a_path, side="right")

        self.clear_buttons()

        tk.Button(self.buttons_frame, text="Dobrze",
                  command=self.mark_correct).pack(side=tk.LEFT)

        tk.Button(self.buttons_frame, text="Źle",
                  command=self.mark_incorrect).pack(side=tk.LEFT)

    def mark_correct(self):
        self.correct += 1
        self.after_answer()

    def mark_incorrect(self):
        self.incorrect += 1
        self.wrong_questions.append(self.current_question)
        self.after_answer()

    def after_answer(self):
        self.update_score()
        self.clear_buttons()
        self.next_button.pack()

    def next_question(self):
        self.next_button.pack_forget()
        self.show_question()

    def update_score(self):
        self.score_label.config(
            text=f"Dobrze: {self.correct} | Źle: {self.incorrect}"
        )

    def display_image(self, path, side="left"):
        img = Image.open(path)

        # dynamiczne skalowanie
        screen_w = self.root.winfo_screenwidth() // 2
        screen_h = self.root.winfo_screenheight()

        img.thumbnail((screen_w, screen_h))

        photo = ImageTk.PhotoImage(img)

        if side == "left":
            self.left_img = photo
            self.left_label.config(image=photo)
        else:
            self.right_img = photo
            self.right_label.config(image=photo)

    def clear_buttons(self):
        for widget in self.buttons_frame.winfo_children():
            widget.destroy()

    def end_quiz(self):
        print("\n=== KONIEC QUIZU ===")
        print(f"Dobrze: {self.correct}, Źle: {self.incorrect}")

        if self.wrong_questions:
            print("\nBłędne pytania:")
            for q in self.wrong_questions:
                print(q)

        with open("bledne.txt", "w") as f:
            for q in self.wrong_questions:
                f.write(q + "\n")

    def on_close(self):
        self.end_quiz()
        self.root.destroy()


root = tk.Tk()
app = QuizApp(root)
root.mainloop()