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

def main():
    win = Window(800, 600)
    p1 = Point(100, 100)
    p2 = Point(300, 100)
    p3 = Point(300, 300)
    p4 = Point(100, 300)

    # Create lines using the points
    line1 = Line(p1, p2)
    line2 = Line(p2, p3)
    line3 = Line(p3, p4)
    line4 = Line(p4, p1)

    # Draw lines on the window
    win.draw_line(line1, "red")
    win.draw_line(line2, "blue")
    win.draw_line(line3, "green")
    win.draw_line(line4, "purple")
    win.wait_for_close()

if __name__ == "__main__":
    main()