from tkinter import *
from tkinter.messagebox import showerror, showinfo
from random import randint


class Arcanoid(Canvas):
    def __init__(self,
                 master,
                 fps=20,
                 width=500,
                 height=300,
                 bg='#000',
                 rw=100,
                 rh=20,
                 rc='#0f0',
                 rs=20,
                 bs=10,
                 br=20,
                 bc='#0ff',
                 wc=5,
                 wr=2,
                 wh=100,
                 wg='#f0f'):
        super().__init__(master, width=width, height=height, bg=bg)
        self.rs = rs
        self.bs = bs
        self.bm = [0, bs]
        self.fps = fps
        self.gameover = False

        self.racket = self.create_rectangle(int((width - rw) / 2), (height - rh),
                                            int((width + rw) / 2),
                                            height,
                                            fill=rc,
                                            outline=rc)
        self.ball = self.create_oval(int(width / 2) - br,
                                     int(height / 2) - br,
                                     int(width / 2) + br,
                                     int(height / 2) + br,
                                     fill=bc,
                                     outline=bc)
        self.wall = [[self.create_rectangle(int(width/wc)*j, int(wh/wr)*i, int(width/wc)*(
            j+1), int(wh/wr)*(i+1), fill=wg, outline=wg) for j in range(wc)] for i in range(wr)]

        self.physics()
        self.bind('<Key>', self.drive)
        self.focus_set()

    def physics(self):
        self.move(self.ball, *self.bm)
        bc = self.coords(self.ball)
        rc = self.coords(self.racket)

        if bc[0] <= 0 or bc[2] >= int(self['width']):
            self.bm[0] = -self.bm[0]
        if bc[1] <= 0:
            self.bm[1] = self.bs

        for row in self.wall:
            for brick in row:
                wc = self.coords(brick)
                if self.ball in list(self.find_overlapping(*wc)):
                    self.bm[1] = self.bs
                    self.delete(brick)
                    for i in range(len(self.wall)):
                        if brick in self.wall[i]:
                            self.wall[i].remove(brick)
                        if self.wall[i] == []:
                            del self.wall[i]
                    break

        if bc[0] >= rc[0] and bc[2] <= rc[2] and bc[3] >= rc[1]:
                self.bm[1] = -self.bs
        elif bc[3] >= int(self['height']):
                self.gameover = True

        if not self.gameover and self.wall != []:
            self.after(int(1000 / self.fps), self.physics)
        elif self.wall != []:
            def gameover():
                showerror('ERROR', 'ERROR: GAME OVER!')
                exit(1)
            self.after(randint(10, 30)*100, gameover)
        else:
            def gameover():
                showinfo('CONGRATULATIONS', 'CONGRATULATIONS: YOU WIN!')
                exit(0)
            self.after(randint(10, 30)*100, gameover)

    def drive(self, key):
        if self.gameover or self.wall == []:
            return
        key = key.char
        rc = self.coords(self.racket)
        bc = self.coords(self.ball)
        if key == 'a' and rc[0] > 0:
            self.move(self.racket, -self.rs, 0)
            if bc[0] >= rc[0] and bc[2] <= rc[2]:
                if bc[3] >= rc[1]:
                    self.bm[0] = -self.bs
        elif key == 'd' and rc[2] < int(self['width']):
            self.move(self.racket, self.rs, 0)
            if bc[0] >= rc[0] and bc[2] <= rc[2]:
                if bc[3] >= rc[1]:
                    self.bm[0] = self.bs


if __name__ == "__main__":
    win = Tk()
    win.title(Arcanoid.__name__)
    Arcanoid(win).pack()
    win.mainloop()

