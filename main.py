from tkinter import Tk, BOTH, Canvas

class Window:
    def __init__(self, width, height):
        self.width = width 
        self.height = height
        #create root window using tk()
        self.root = tk.Tk()

        #set title
        self.root.title("My Window")

        #set window size
        self.root.geometry(f"{width}x{height}")

        #create and pack canvas
        self.canvas = tk.Canvas(self.root, width=width, height=height)
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

def main():
    win = Window(800, 600)
    win.wait_for_close()