from tkinter import *
from random import *
import time
import math

cellsvert = [["n", "n", "n"], ["n", "n", "n"], ["n", "n", "n"]]
cellshorz = [["n", "n", "n"], ["n", "n", "n"], ["n", "n", "n"]]
cellsforbot = {0 : "n", 1 : "n", 2 : "n",
               3 : "n", 4 : "n", 5 : "n",
               6 : "n", 7 : "n", 8 : "n"}
xwin = ["X", "X", "X"]
owin = ["O", "O", "O"]
scores = {"X" : 0, "O" : 0}
haswon = False

class Board:
    def __init__(self, root):
        self.root = root

        self.first = True
        self.turn = choice(["X", "O"])
        self.resetvar = True
        self.dontchange = False

        self.canvas = Canvas(self.root, width=300, height=300, bg="white")
        self.canvas.grid(row=0, column=0)
        
        for x in range(1, 3):
            x *= 100
            self.canvas.create_line(x, 0, x, 300, tags=("line", "gridline"))
            self.canvas.create_line(0, x, 300, x, tags=("line", "gridline"))

    def getxy(self):
        for x in range(0, 201, 100):
            if self.xpos > x and self.xpos < x+100:
                self.xpos = x+20
                x = int(x/100)
                for y in range(0, 201, 100):
                    if self.ypos > y and self.ypos < y+100:
                        self.ypos = y+20
                        y = int(y/100)
                        if cellsvert[x][y] == "n":
                            cellindex = (3*x) + y
                            cellsvert[x][y] = self.turn
                            cellshorz[y][x] = self.turn
                            cellsforbot[cellindex] = self.turn
                        else:
                            self.dontchange = True

    def checkwin(self):
        for col in range(0,3):
            if cellsvert[col] == xwin:
                s = "X, col: " + str(col)
                n = col*100
                n += 50
                self.winlinexpos, self.winlineypos = n, 50
                self.won(s, "vert")
            elif cellsvert[col] == owin:
                s = "O, col: " + str(col)
                n = col*100
                n += 50
                self.winlinexpos, self.winlineypos = n, 50
                self.won(s, "vert")
        for row in range(0,3):
            if cellshorz[row] == xwin:
                s = "X, row: " + str(row)
                n = row*100
                n += 50
                self.winlinexpos, self.winlineypos = 50, n
                self.won(s, "horz")
            elif cellshorz[row] == owin:
                s = "O, row: " + str(row)
                n = row*100
                n += 50
                self.winlinexpos, self.winlineypos = 50, n
                self.won(s, "horz")
        diagwinlist_l = [cellsvert[0][0], cellsvert[1][1], cellsvert[2][2]]
        diagwinlist_r = [cellsvert[2][0], cellsvert[1][1], cellsvert[0][2]]
        if diagwinlist_l == xwin:
            self.won("X, diagonal left", "diag_l")
        elif diagwinlist_r == xwin:
            self.won("X, diagonal right", "diag_r")
        elif diagwinlist_l == owin:
            self.won("O, diagonal left", "diag_l")
        elif diagwinlist_r == owin:
            self.won("O, diagonal right", "diag_r")
        else:   
            n = 0
            for x in range(0,3):
                for y in range(0,3):
                    if cellsvert[x][y] != "n":
                        n += 1
            if n == 9:
                self.won("tie", "tie")

    def won(self, who, direction):
        self.haswon = True
        self.canvas.unbind("<Button-1>")
        if direction == "vert":
            self.canvas.create_line(self.winlinexpos, self.winlineypos, self.winlinexpos, self.winlineypos+200, width=15, tags=("line", "winline"))
        elif direction == "horz":
            self.canvas.create_line(self.winlinexpos, self.winlineypos, self.winlinexpos+200, self.winlineypos, width=15, tags=("line", "winline"))
        elif direction == "diag_l":
            self.canvas.create_line(50, 50, 250, 250, width=15, tags=("line", "winline"))
        elif direction == "diag_r":
            self.canvas.create_line(250, 50, 50, 250, width=15, tags=("line", "winline"))
        if "X" in who:
            winstring = "X WINS!"
            rhside.updatescores("X")
        elif "O" in who:
            winstring = "O WINS!"
            rhside.updatescores("O")
        elif who == "tie":
            winstring = "TIE!"
            
        self.canvas.create_text(150, 150, text=winstring, fill="green", font="Arial 35 bold", tags=("text", "wintext"))

    def draw(self, event):
        if self.turn == "X" and rhside.playeroptionvar.get() == 2:
            self.xpos, self.ypos = event.x, event.y
            
            self.getxy()
            
            if self.dontchange == False:
                self.canvas.create_line(self.xpos, self.ypos, self.xpos+57, self.ypos+57, width=10, fill="red", tags=("token", "cross"))
                self.canvas.create_line(self.xpos+57, self.ypos, self.xpos, self.ypos+57, width=10, fill="red", tags=("token", "cross"))
                self.turn = "O"
            else:
                self.dontchange = False 
            
            self.checkwin()

        elif self.turn == "O" and rhside.playeroptionvar.get() == 2:
            self.xpos, self.ypos = event.x, event.y

            self.getxy()

            if self.dontchange == False:
                self.canvas.create_oval(self.xpos, self.ypos, self.xpos+65, self.ypos+65, width=10, outline="blue", tags=("token", "nought"))
                self.turn = "X"
            else:
                self.dontchange = False
                
            self.checkwin()

        else:
            self.xpos, self.ypos = event.x, event.y
            
            self.getxy()
            
            if self.dontchange == False:
                self.canvas.create_line(self.xpos, self.ypos, self.xpos+57, self.ypos+57, width=10, fill="red", tags=("token", "cross"))
                self.canvas.create_line(self.xpos+57, self.ypos, self.xpos, self.ypos+57, width=10, fill="red", tags=("token", "cross"))
                self.turn = "O"
            else:
                self.dontchange = False
            
            self.checkwin()
            
            if self.haswon == False and self.dontchange == False:
                botmove = self.bot.move()
                x = math.floor(botmove/3)
                y = botmove % 3
                self.xpos = (x*100)+20
                self.ypos = (y*100)+20

                if cellsvert[x][y] == "n":
                    cellindex = (3*x) + y
                    cellsvert[x][y] = self.turn
                    cellshorz[y][x] = self.turn
                    cellsforbot[cellindex] = self.turn
                else:
                    self.dontchange = True

                if self.dontchange == False:
                    self.canvas.create_oval(self.xpos, self.ypos, self.xpos+65, self.ypos+65, width=10, outline="blue", tags=("token", "nought"))
                    self.turn = "X"
                else:
                    self.dontchange = False
                    
                self.checkwin()

    def clear(self):
        def doafter():
            self.canvas.delete("xstarts", "ostarts")
            self.turn = "X"
            self.canvas.bind("<Button-1>", self.draw)
        if self.first == True:
            rhside.resetbutton.configure(text="Reset")
            self.first = False

        self.haswon = False

        self.turn = choice(["X", "O"])
        if self.turn == "X":
            self.canvas.create_text(150, 150, text="X Goes First!", fill="red", font="Arial 35 bold", tags=("text", "xstarts"))
        else:
            self.canvas.create_text(150, 150, text="O Goes First!", fill="blue", font="Arial 35 bold", tags=("text", "ostarts"))

        self.resetvar = not self.resetvar

        self.canvas.delete("wintext", "token", "winline")
        rhside.resetbutton.after(2000, doafter)

        for x in range(0,3):
            for y in range(0,3):
                cellindex = (3*x) + y
                cellsvert[x][y] = "n"
                cellshorz[x][y] = "n"
                cellsforbot[cellindex] = "n"

        

class RHSide:
    def __init__(self, root):
        self.root = root

        self.playeroptionvar = IntVar()
        self.playeroptionvar.set(2)
        
        self.rhframe = Frame(self.root)
        self.rhframe.grid(row=0, column=1)

        self.playeroptionframe = Frame(self.rhframe)
        self.playeroptionframe.grid(row=0, column=0)

        self.titlelabel = Label(self.playeroptionframe, text="Tic Tac Toe", font="Arial 20 bold", height=5)
        self.titlelabel.grid(row=0, column=0)

        self.scorelabelxvar = StringVar()
        self.scorelabelxvar.set("X: {}".format(scores["X"]))
        self.scorelabelx = Label(self.playeroptionframe, textvariable=self.scorelabelxvar)
        self.scorelabelx.grid(row=1, column=0)
        
        self.scorelabelovar = StringVar()
        if self.playeroptionvar.get() == 2:
            self.scorelabelovar.set("O: {}".format(scores["O"]))
        else:
            self.scorelabelovar.set("O (bot): {}".format(scores["O"]))
        self.scorelabelo = Label(self.playeroptionframe, textvariable=self.scorelabelovar)
        self.scorelabelo.grid(row=2, column=0)
        
        r = Radiobutton(self.playeroptionframe, text="Multiplayer", variable=self.playeroptionvar, value=2, indicatoron=0, width=17, command=self.updatemode)
        r.select()
        r.grid(row=3, column=0)
        r = Radiobutton(self.playeroptionframe, text="Single Player (vs. bot)", variable=self.playeroptionvar, value=1, indicatoron=0, width=17, command=self.updatemode)
        r.grid(row=4, column=0)

        self.resetbuttonframe = Frame(self.rhframe)
        self.resetbuttonframe.grid(row=1, column=0)

        self.resetbutton = Button(self.resetbuttonframe, text="Start", height=3, width=17, command=board.clear)
        self.resetbutton.grid(row=0, column=0)

    def updatescores(self, player):

        scores[player] += 1
        
        self.scorelabelxvar.set("X: {}".format(scores["X"]))
        if self.playeroptionvar.get() == 2:
            self.scorelabelovar.set("O: {}".format(scores["O"]))
        else:
            self.scorelabelovar.set("O (bot): {}".format(scores["O"]))

    def updatemode(self):
        self.playeroptionvar.set(self.playeroptionvar.get())
        if self.playeroptionvar.get() == 2:
            self.scorelabelovar.set("O: {}".format(scores["O"]))
        else:
            self.scorelabelovar.set("O (bot): {}".format(scores["O"]))

        if self.playeroptionvar.get() == 1:
            board.bot = Bot()
        



class Bot:
    def __init__(self):
        pass

    def move(self):
        r = randint(1,11)
        if r <= 9:
            for i in range(0,9):
                boardcopy = cellsforbot.copy()
                if boardcopy[i] == "n":
                    boardcopy[i] = "O"
                    if self.iswinner(boardcopy, "O"):
                        return i

        r = randint(1,11)
        if r <= 9:
            for i in range(0,9):
                boardcopy = cellsforbot.copy()
                if boardcopy[i] == "n":
                    boardcopy[i] = "X"
                    if self.iswinner(boardcopy, "X"):
                        return i

        possiblemoves = []
        for i in [0, 2, 6, 8]:
            if cellsforbot[i] == "n":
                possiblemoves.append(i)
        if len(possiblemoves) != 0:
            return choice(possiblemoves)

        if cellsforbot[5] == "n":
            return 5

        possiblemoves = []
        for i in [1, 5, 7, 3]:
            if cellsforbot[i] == "n":
                possiblemoves.append(i)
        if len(possiblemoves) != 0:
            return choice(possiblemoves)

        

    def iswinner(self, bo, le):
        return ((bo[0] == le and bo[1] == le and bo[2] == le) or
        (bo[3] == le and bo[4] == le and bo[5] == le) or
        (bo[6] == le and bo[7] == le and bo[8] == le) or
        (bo[2] == le and bo[4] == le and bo[6] == le) or
        (bo[0] == le and bo[3] == le and bo[6] == le) or
        (bo[1] == le and bo[4] == le and bo[7] == le) or
        (bo[2] == le and bo[5] == le and bo[8] == le) or
        (bo[0] == le and bo[4] == le and bo[8] == le))


root = Tk()
root.title("Tic Tac Toe")
board = Board(root)
rhside = RHSide(root)

root.mainloop()
