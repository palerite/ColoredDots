import random
from tkinter import *
from random import random as rnd
import time
import math
pi = math.pi


def points_in_circle(ra, n=10):  # thank you Abhijit from StackOverflow
    return [(math.cos(2 * pi / n * x) * ra, math.sin(2 * pi / n * x) * ra) for x in range(0, n + 1)]


class Dot:
    def __init__(self, canvas, color, n, x, y):
        global dots
        global dots_matrix
        self.canvas = canvas
        self.color = color
        self.n = n
        self.x = x
        self.y = y

    def infect(self):
        global dots
        if self.color != "green" and self.color != "red":
            for dot in [dots[j].color for j in dots_matrix[self.n]]:
                if dot == "red" and rnd() <= p:
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
        if self.color == "red" and rnd() <= q and self.color != "green":
            self.color = "black"

    def immune_no_more(self):
        if self.color == "green" and rnd() <= r and self.color != "white":
            self.color = "brown"

    def draw(self):
        c.create_oval(self.x, self.y, self.x + dot_diameter, self.y + dot_diameter, fill=self.color, outline='black')


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
    for dot in dots:
        if drawing:
            dot.draw()
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
    c.delete(all)
    for dot in dots:
        if drawing:
            dot.draw()
        if dot.color == "red":
            count += 1
    if turn >= 10000 or dots[-1].color == "red" or not count and count_mode:
        if dots[-1].color == "red":
            runs_success += 1
        else:
            runs_failed += 1
        runs_total += 1
        if runs_total >= 99990:
            print(f"Chance on step {runs_total}:", runs_success / runs_total,
                  f"and there were {runs_success} successful runs.")
        if runs_total >= 100000:
            print("--------------------------------------------")
            print("\nChance:", runs_success / runs_total)
            queue_free()
        restart()


def restart():
    global dots
    global turn
    global dots_matrix
    turn = 0
    dots = list()
    dots_matrix = list()
    nu = 10
    corner = 7
    posx = 10
    posy = h // 2
    c.delete("all")
    points_array = points_in_circle(200, n=nu)
    for j in range(nu):
        if placing_mode == "random":
            posx = random.randint(20, w - 20)
            posy = random.randint(20, h - 20)
        elif placing_mode == "geometrical":
            posx += round(dot_diameter * 1.5)
            posy += -dot_diameter + (j % corner) * 2 if j < corner else dot_diameter - (j % corner) * 5
        else:
            posx, posy = points_array[j]
            posx += w // 2
            posy += h // 2
        # [j + 1] if j == 0 else ([j - 1] if j == nu - 1 else [j - 1, j + 1])
        dots.append(Dot(c, "red" if j == 0 else "white", j, posx, posy))
        dots_matrix.append([j - 1, j + 1] if j not in (0, nu - 1) else ([j - 1] if j == nu - 1 else [j + 1]))
    # for i in range(nu):
    #     dots_matrix[i].append((i + (random.randint(5, nu))) % nu)
    for i in range(len(dots_matrix)):
        for j in range(len(dots_matrix)):
            if i in dots_matrix[j] and j not in dots_matrix[i]:
                dots_matrix[i].append(j)
            if j in dots_matrix[i] and i not in dots_matrix[j]:
                dots_matrix[j].append(i)
    if drawing:
        for dot in dots:
            dot.draw()
            for i in dots_matrix[dot.n]:
                c.create_line(dot.x + dot_diameter // 2, dot.y + dot_diameter // 2,
                              dots[i].x + dot_diameter // 2, dots[i].y + dot_diameter // 2, arrow="both")


def queue_free():
    global application_exists
    application_exists = False


dot_diameter = 20
dots = list()
dots_matrix = list()
rules = 1
placing_mode = "radial"
playing = True
interval = 1
turn = 1
runs_total = 0
runs_success = 0
runs_failed = 0

drawing = True

count_mode = False

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
w = 800
h = 500
c = Canvas(root, width=w, height=h, bg="white")
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
pEntry.insert(0, "0.8")
qEntry.insert(0, "0.6")
rEntry.insert(0, "0.5")

application_exists = True  # Dot(c, "red", 0)

restart()

while application_exists:
    p = float(pVar.get())
    r = float(rVar.get())
    q = float(qVar.get())
    if not count_mode:
        if playing and time.time() - last_update > interval:
            step()
    else:
        step()
    root.update()
    root.update_idletasks()
    root.protocol("WM_DELETE_WINDOW", queue_free)
