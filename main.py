from tkinter import *

class Window:
    def __init__(self, width, height):
        self.width = width 
        self.height = height
        #create root window using tk()
        self.root = Tk()

        #set title
        self.root.title("My Window")

        #set window size
        self.root.geometry(f"{width}x{height}")

        #create and pack canvas
        self.canvas = Canvas(self.root, width=width, height=height)
        self.canvas.pack()

        #track if window running
        self.running = False

        #connect close to self.close
        self.root.protocol("WM_DELETE_WINDOW", self.close)

    def redraw(self):
        self.root.update_idletasks()
        self.root.update()

    def wait_for_close(self):
        self.running = True
        while self.running: 
            self.redraw()
        
    def close(self):
        self.running = False

    def draw_line(self, line, fill_color):
        line.draw(self.canvas, fill_color)


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y 

class Line:
    def __init__(self, point1, point2):
        self.point1 = point1
        self.point2 = point2

    def draw(self, canvas, fill_color):
        canvas.create_line(
            self.point1.x, self.point1.y, self.point2.x, self.point2.y, fill=fill_color, width=2
        )

class Cell:
    def __init__(self, x1, y1, x2, y2, win):
        self._x1 = x1
        self._y1 = y1
        self._x2 = x2 
        self._y2 = y2 
        self._win = win
        self.has_left_wall = True
        self.has_right_wall = True
        self.has_top_wall = True
        self.has_bottom_wall = True

    def draw(self):
        if self.has_left_wall:
            self._win.draw_line(Line(Point(self._x1, self._y1), Point(self._x1, self._y2)), "black")
        if self.has_top_wall:
            self._win.draw_line(Line(Point(self._x1, self._y1), Point(self._x2, self._y1)), "black")
        if self.has_right_wall:
            self._win.draw_line(Line(Point(self._x2, self._y1), Point(self._x2, self._y2)), "black")
        if self.has_bottom_wall:
            self._win.draw_line(Line(Point(self._x2, self._y2), Point(self._x1, self._y2)), "black")
        

def main():
    win = Window(800, 600)

    cell = Cell(100, 100, 150, 150, win)
    cell.draw()

    win.wait_for_close()

if __name__ == "__main__":
    main()