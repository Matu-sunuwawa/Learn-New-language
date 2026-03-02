from tkinter import *
from tkinter import messagebox
import pandas, random

BACKGROUND_COLOR = "#B1DDC6"

original_df = pandas.read_csv("./data/french_words.csv")

match_words = [{row["French"]:row["English"]} for index, row in original_df.iterrows()]

try:
    new_df = pandas.read_csv("./data/words_to_learn.csv")
except FileNotFoundError:
    # Initialize
    french_list = original_df["French"].to_list()
    english_list = original_df["English"].to_list()
    new_df = {
        "French": french_list,
        "English": english_list
    }
else:
    french_list = new_df["French"].to_list()
    english_list = new_df["English"].to_list()
    new_df = {
        "French": french_list,
        "English": english_list
    }

# ----------------------------------- save words words_to_learn.csv ----------------------------------- #
def save_to_learn():
    en_word = [dict[prev_word_store] for dict in match_words if prev_word_store in dict]
    try:
        french_list.remove(prev_word_store)
        english_list.remove(en_word[0])
    except ValueError:
        messagebox.showinfo(title="Congratulations!",
                            message="You completed most frequent word list successfully!", icon="info")
    df = pandas.DataFrame(new_df)
    df.to_csv("./data/words_to_learn.csv", index=False)
# ----------------------------------- flip word ----------------------------------- #
prev_word_store = ""
def flip_word():
    global canvas_card, prev_word_store
    canvas.itemconfig(canvas_title, text="English")
    trans_word_text = canvas.itemcget(trans_word, 'text')
    prev_word_store = trans_word_text
    en_word = [dict[trans_word_text] for dict in match_words if trans_word_text in dict]
    canvas.itemconfig(trans_word, text=en_word[0])
    canvas_card = PhotoImage(file="./images/card_back.png")
    canvas.itemconfig(bg_image, image=canvas_card)
    wrong_btn["state"] = "normal"
    right_btn["state"] = "normal"
# ----------------------------------- pick word ----------------------------------- #
def pick_word(word):
    global canvas_card
    if prev_word_store != "" and word == "right":
        save_to_learn()
    try:
        canvas.itemconfig(canvas_title, text="French")
        fr_word = random.choice(french_list)
        canvas.itemconfig(trans_word, text=fr_word)
        canvas_card = PhotoImage(file="./images/card_front.png")
        canvas.itemconfig(bg_image, image=canvas_card)

        window.after(3000, flip_word)
        wrong_btn["state"] = "disabled"
        right_btn["state"] = "disabled"
        window.after_cancel(flip_word)
    except IndexError:
        canvas.itemconfig(canvas_title, text="Let's go to next challenge!")
        canvas.itemconfig(trans_word, text="")
        wrong_btn["state"] = "disabled"
        right_btn["state"] = "disabled"
        messagebox.showinfo(title="Congratulations!", message="You completed most frequent word list successfully!",
                            icon="info")
# ----------------------------------- Flash Card UI ----------------------------------- #
window = Tk()
window.title("Flashy")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

# Create Canvas
canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
canvas_card = PhotoImage(file="./images/card_front.png")
bg_image = canvas.create_image(410, 260, image=canvas_card)
canvas_title = canvas.create_text(400, 150,text="French", font=("Ariel", 40, "italic"))
trans_word = canvas.create_text(400, 263, text="", font=("Ariel", 60, "bold"))
canvas.grid(row=0, column=0, columnspan=2)

# Create Buttons
wrong_img = PhotoImage(file="./images/wrong.png")
wrong_btn = Button(image=wrong_img, highlightthickness=0, command=lambda wrong="wrong": pick_word(wrong))
wrong_btn.grid(row=1, column=0)

right_img = PhotoImage(file="./images/right.png")
right_btn = Button(image=right_img, highlightthickness=0, command=lambda right="right": pick_word(right))
right_btn.grid(row=1, column=1)

pick_word("wrong")


window.mainloop()
