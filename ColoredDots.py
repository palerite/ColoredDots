from tkinter import *
from random import random as rnd
import time


class Dot:
    def __init__(self, canvas, color, n):
        self.canvas = canvas
        self.color = color
        self.n = n
        self.id = c.create_oval(20 + n * 50, 180, 40 + n * 50, 200, fill=self.color, outline='black')

    def infect(self):
        global dots
        if rnd() <= p and self.color != "green":
            if self.n not in [0, len(dots) - 1]:
                if "red" in [dots[self.n - 1].color, dots[self.n + 1].color]:
                    self.color = "blue"
            elif self.n != 0:
                if "red" == dots[self.n - 1].color:
                    self.color = "blue"
            else:
                if "red" == dots[self.n + 1].color:
                    self.color = "blue"

    def fix(self):
        global dots
        if self.color == "blue":
            self.color = "red"
        if self.color == "black":
            self.color = "green"
        if self.color == "brown":
            self.color = "white"

    def cure(self):
        if self.color == "red":
            self.color = "white"

    def immune(self):
        if self.color == "red" and rnd() <= q:
            self.color = "black"

    def immune_no_more(self):
        if self.color == "green" and rnd() <= r:
            self.color = "brown"

    def draw(self):
        c.create_oval(20 + self.n * 50, 180, 40 + self.n * 50, 200, fill=self.color, outline='black')


def play():
    global playing
    playing = not playing
    Play.config(text=("Play" if not playing else "Pause"))


def step():
    global last_update
    global dots
    global c
    global playing
    global turn
    global runs_total
    global runs_success
    global runs_failed
    turn += 1
    last_update = time.time()
    c.delete(all)
    for dot in dots:
        dot.infect()
    if rules == 1:
        for dot in dots:
            dot.immune()
    for dot in dots:
        if rules == 1:
            dot.immune_no_more()
        else:
            dot.cure()
        dot.fix()
    count = 0
    for dot in dots:
        dot.draw()
        if dot.color == "red":
            count += 1
    # if turn >= 10000 or dots[-1].color == "red" or not count:
    #     if dots[-1].color == "red":
    #         runs_success += 1
    #     else:
    #         runs_failed += 1
    #     runs_total += 1
    #     print(f"Chance on step {runs_total}:", runs_success / runs_total,
    #           f"and there were {runs_success} successful runs.")
    #     if runs_total >= 10000:
    #         print("\nChance:", runs_success / runs_total)
    #         queue_free()
    #     restart()


def restart():
    global dots
    global turn
    turn = 0
    dots = [Dot(c, "red", 0)] + [Dot(c, "white", i + 1) for i in range(9)]


def queue_free():
    global application_exists
    application_exists = False


rules = 1
playing = True
interval = 1
turn = 1
runs_total = 0
runs_success = 0
runs_failed = 0
last_update = time.time() - interval
root = Tk()
root.title("ColoredDots")
top = Frame(root)
top.pack(side=TOP)
b1 = Frame(root)
b1.pack(side=BOTTOM)
b2 = Frame(root)
b2.pack(side=BOTTOM)
b3 = Frame(root)
b3.pack(side=BOTTOM)
c = Canvas(root, width=500, height=300, bg="white")
c.create_line(30, 190, 480, 190)
Play = Button(root, text="Pause", command=play)
Play.pack(in_=top, side=LEFT)
Step = Button(root, text="Step", command=step)
Step.pack(in_=top, side=LEFT)
Step = Button(root, text="Restart", command=restart)
Step.pack(in_=top, side=LEFT)
c.pack()


pVar = StringVar()
qVar = StringVar()
rVar = StringVar()

pEntry = Entry(root, textvariable=pVar)
pLabel = Label(root, text="p: ")
qEntry = Entry(root, textvariable=qVar)
qLabel = Label(root, text="q: ")
rEntry = Entry(root, textvariable=rVar)
rLabel = Label(root, text="r: ")
pLabel.pack(in_=b3, side=LEFT)
qLabel.pack(in_=b2, side=LEFT)
rLabel.pack(in_=b1, side=LEFT)
pEntry.pack(in_=b3, side=LEFT)
qEntry.pack(in_=b2, side=LEFT)
rEntry.pack(in_=b1, side=LEFT)
pEntry.insert(0, "0.9")
qEntry.insert(0, "0.8")
rEntry.insert(0, "0.9")

application_exists = True
dots = [Dot(c, "red", 0)] + [Dot(c, "white", i + 1) for i in range(9)]

while application_exists:
    p = float(pVar.get())
    r = float(rVar.get())
    q = float(qVar.get())
    if playing and time.time() - last_update > interval:
        step()
    root.update()
    root.update_idletasks()
    root.protocol("WM_DELETE_WINDOW", queue_free)
