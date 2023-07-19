import random
from tkinter import *
import pandas

BACKGROUND_COLOR = "#B1DDC6"
current_card = {}
to_learn = {}

try:
    data = pandas.read_csv("data/french_words.csv")
except FileNotFoundError:
    original_data = pandas.read_orc("data/french_words.csv")
    to_learn= original_data.to_dict(orient="records")
else:
    to_learn = data.to_dict(orient="records")


def next_card():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = random.choice((to_learn))
    canvas.itemconfig(card_title, text="French", fill="black")
    canvas.itemconfig(card_text, text=current_card["French"], fill="black")
    canvas.itemconfig(card_bg, image=card_front)
    flip_timer = window.after(3000, func=flip_card)

def flip_card():
    canvas.itemconfig(card_title, text="English",fill="white")
    canvas.itemconfig(card_text, text=current_card["English"], fill="white")
    canvas.itemconfig(card_bg, image=card_back_img)

def is_known():
    to_learn.remove(current_card)
    data= pandas.DataFrame(to_learn)
    data.to_csv("words_lean_from.csv")
    next_card()


window = Tk()
window.title("Test French")
window.config(padx= 50, pady=50,bg= BACKGROUND_COLOR)

flip_timer = window.after(3000, func=flip_card)

canvas = Canvas(width=800, height=526)
card_front = PhotoImage(file="images/card_front.png")
card_back_img = PhotoImage(file="images/card_back.png")
card_bg_img = PhotoImage(file="images/card_back.png")
card_bg =canvas.create_image(400, 273, image=card_front)
card_title = canvas.create_text(400, 150, text="Title", font=("Ariel", 40, "italic"))
card_text = canvas.create_text(400, 263, text= "word", font=("Ariel", 60, "italic"))
canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
canvas.grid(row=0, column=0, columnspan=2)


cross_img = PhotoImage(file="images/wrong.png")
wrong_button = Button(image=cross_img, highlightthickness=0, command=next_card)
wrong_button.grid(row=1, column=0)

tick_img = PhotoImage(file="images/right.png")
correct_button = Button(image=tick_img, highlightthickness=0, command=is_known)
correct_button.grid(row=1,column=1)

next_card()

window.mainloop()