from tkinter import *


class Arcanoid(Canvas):
    def __init__(self, master, fps=50, width=1600, height=800, bg='#000', rw=400, rh=40, rc='#0f0', rs=20, bs=10, br=40, bc='#f0f'):
        super().__init__(master, width=width, height=height, bg=bg)
        self.rs = rs
        self.bs = bs
        self.bm = [0, bs]
        self.fps = fps
        self.gameover = False

        self.racket = self.create_rectangle(
            int((width-rw)/2), (height-rh), int((width+rw)/2), height, fill=rc, outline=rc)
        self.ball = self.create_oval(int(
            width/2)-br, int(height/2)-br, int(width/2)+br, int(height/2)+br, fill=bc, outline=bc)

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
        if bc[0] >= rc[0] and bc[2] <= rc[2]:
            if bc[3] >= rc[1]:
                self.bm[1] = -self.bs
        else:
            if bc[3] >= int(self['height']):
                self.gameover = True
        if not self.gameover:
            self.after(int(1000/self.fps), self.physics)

    def drive(self, key):
        if self.gameover:
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
    win.title('Arcanoid')
    Arcanoid(win).pack()
    win.mainloop()
