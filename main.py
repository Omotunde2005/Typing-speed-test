from tkinter import *
from tkinter import messagebox
import math
BACKGROUND = "#6E85B7"


def reset():

    try:
        selection = listbox.get(listbox.curselection())
    except TclError:
        messagebox.showinfo("Choose a timer to start test")
    else:
        text = Text(width=70, height=10)
        text.config()
        text.grid(columnspan=3, row=6, column=0)
        text.focus()
        score_label.config(text="")
        with open("record.txt", mode="r") as record_file:
            score = record_file.readlines()
        highest_score.config(text=f"Highest score: {score[0]}")
        button.config(text="Reset")
        button["state"] = "disable"
        timer(selection * 60, text, selection)


def timer(count, text, selection):
    def update(event):
        num = str(len(text.get("1.0", 'end-1c')))
        new_label.config(text=f"Total Characters: {num}",
                         font=("Arial", 16, "bold"), bg=BACKGROUND, fg="green")
        new_label.grid(column=1, row=5)
        return num

    minutes = math.floor(count / 60)
    seconds = count % 60

    if seconds < 10:
        seconds = f"0{seconds}"

    label = Label(text=f"{minutes}:{seconds}")
    label.config(pady=10, padx=10, font=("Arial", "20", "bold"), fg="green")
    label.grid(column=0, row=5)
    new_label = Label(text="Nothing")
    text.bind('<KeyPress>', update)
    text.bind('<KeyRelease>', update)

    if count > 0:
        window.after(1000, timer, count - 1, text, selection)

    elif count <= 0:
        number = update(text)
        button["state"] = "normal"

        if int(number) < 80:
            score_label.config(text="You did poorly", fg='red', font=("Arial", 20, 'italic'))
            button.config(text="Try Again", bg="white")
            button.grid(row=8, column=1)
            with open("record.txt", mode="r") as record_file:
                score = record_file.readlines()
                if int(number) > int(score[0]):
                    with open("record.txt", mode="w") as data:
                        data.write(f"{number}")

        else:
            score_label.config(text="Good performance", fg='green', font=("Arial", 20, 'normal'))
            button.config(text="Restart", command=reset)
            with open("record.txt", mode="r") as record_file:
                score = record_file.readlines()
                if int(number) > int(score[0]):
                    with open("record.txt", mode="w") as data:
                        data.write(f"{number}")
        text.delete("1.0", 'end-1c')


def start_timer():
    try:
        selection = listbox.get(listbox.curselection())

    # Incase a user forgot to choose a timer.
    except TclError:
        messagebox.showinfo("Choose a timer to start test")
    else:
        text = Text(width=70, height=10)
        text.config()
        text.grid(columnspan=3, row=6, column=0)
        text.focus()
        score_label.config(text="")
        button["state"] = "disabled"
        timer(selection * 60, text, selection)


window = Tk()
window.title("Typing Speed Test")
window.config(padx=10, pady=10, bg=BACKGROUND)
logo = Label(text="FastFingers🖐️")
logo.config(font=("Calibri", 18, "bold"), bg=BACKGROUND, highlightthickness=2, highlightcolor="white")
logo.grid(row=0, column=0)

score_label = Label(text="")
score_label.config(bg=BACKGROUND)
score_label.grid(row=7, column=1)

label_one = Label(text="How fast are your fingers? Take a typing speed test to check")
label_one.config(font=("Courier", 20, 'bold'), bg=BACKGROUND, fg="white")
label_one.grid(row=1, column=1, columnspan=2, pady=30, padx=10)

try:
    with open("record.txt", mode="r") as file:
        records = file.readlines()

except FileNotFoundError:
    with open("record.txt", mode="w") as new_file:
        new_file.write("0")
        highest_score = Label(text=f"Highest score: 0")
        highest_score.config(font=("Arial", 20, 'bold'), bg=BACKGROUND, fg="white")
        highest_score.grid(column=2, row=2)

else:
    highest_score = Label(text=f"Highest score: {records[0]}")
    highest_score.config(font=("Arial", 20, 'bold'), bg=BACKGROUND, fg="white")
    highest_score.grid(column=2, row=4)


list_label = Label(text="Choose your preferred timer(in minutes) 🕔")
list_label.config(font=("Courier", 17, 'italic'), bg=BACKGROUND, fg="white")
list_label.grid(column=1, row=2, pady=30, padx=10)

listbox = Listbox(height=3)

list_of_time = [1, 3, 5]
for items in list_of_time:
    listbox.insert(list_of_time.index(items), items)

listbox.grid(column=1, row=3, padx=10, pady=30)
button = Button(text="Begin test", width=15, command=start_timer)
button.grid(column=1, row=4)
window.mainloop()