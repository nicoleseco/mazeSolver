from tkinter import *
import time 
import random

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
        self.visited = False

    def draw(self):
        background_color = "#d9d9d9"
        if self.has_left_wall:
            self._win.draw_line(Line(Point(self._x1, self._y1), Point(self._x1, self._y2)), "black")
        else:
            self._win.draw_line(Line(Point(self._x1, self._y1), Point(self._x1, self._y2)), background_color)
        if self.has_top_wall:
            self._win.draw_line(Line(Point(self._x1, self._y1), Point(self._x2, self._y1)), "black")
        else:
            self._win.draw_line(Line(Point(self._x1, self._y1), Point(self._x2, self._y1)), background_color)
        if self.has_right_wall:
            self._win.draw_line(Line(Point(self._x2, self._y1), Point(self._x2, self._y2)), "black")
        else:
            self._win.draw_line(Line(Point(self._x2, self._y1), Point(self._x2, self._y2)), background_color)
        if self.has_bottom_wall:
            self._win.draw_line(Line(Point(self._x2, self._y2), Point(self._x1, self._y2)), "black")
        else:
            self._win.draw_line(Line(Point(self._x2, self._y2), Point(self._x1, self._y2)), background_color)
        

    def draw_move(self, to_cell, undo=False):
        color = "gray" if undo else "red"

    # Start point: center of current cell
        x1 = (self._x1 + self._x2) // 2
        y1 = (self._y1 + self._y2) // 2

    # End point: center of to_cell
        x2 = (to_cell._x1 + to_cell._x2) // 2
        y2 = (to_cell._y1 + to_cell._y2) // 2

        self._win.draw_line(Line(Point(x1, y1), Point(x2, y2)), color)


class Maze:
    def __init__(self, x1, y1, num_rows, num_cols, cell_size_x, cell_size_y, win, seed=None):
        self._x1 = x1
        self._y1 = y1
        self._num_rows = num_rows
        self._num_cols = num_cols
        self._cell_size_x = cell_size_x
        self._cell_size_y = cell_size_y
        self._win = win
        self._cells = []

        if seed is not None:
            random.seed(seed)

        self._create_cells()
        self._break_entrance_and_exit()


    def _create_cells(self): 
        for col in range(self._num_cols):
            column = []
            for row in range(self._num_rows):
                x1 = self._x1 + col * self._cell_size_x
                y1 = self._y1 + col * self._cell_size_y
                x2 = x1 + self._cell_size_x
                y2 = y1 + self._cell_size_y

                cell=Cell(s1, y1, x2, y2, self._win)
                column.append(cell)
            self._cells.append(column)

        for col in range(self._num_cols):
            for row in range(self._num_rows):
                self._draw_cell(col, row)
    
    def _draw_cell(self, i, j):
        cell = self._cells[i][j]
        cell.draw()
        self._animate()

    def _animate(self):
        self._win.redraw()
        time.sleep(0.05)
    
    def _break_entrance_and_exit(self):
        entrance_cell = self._cells[0][0]
        entrance_cell.has_top_wall = False
        self._draw_cell(0,0)

        exit_cell = self._cells[self._num_cols - 1][self._num_rows-1]
        exit_cell.has_bottom_wall = False
        self._draw_cell(self._num_cols -1, self._num_rows -1)

    def _break_walls_r(self, i, j):
        current = self._cells[i][j]
        current.visited = True

        while True: 
            neighbors = []

            if i > 0 and not self._cells[i-1][j].visited:
                neighbors.append(("left", i-1,j))
            if i < self._num_cols - 1 and not self._cells[i+1][j].visited:
                neighbors.append(("right", i+1, j))
            if j > 0 and not self._cells[i][j-1].visited:
                neighbors.append(("up", i, j-1))
            if j < self._num_rows - 1 and not self._cells[i][j +1].visited:
                neighbors.append(("down", i, j+1))


            if len(neighbors) == 0:
                self._draw_cell(i,j)
                return
            
            direction, next_i, next_j = random.choice(neighbors)

            if direction == "left":
                current.has_left_wall = False
                self._cells[next_i][next_j].has_right_wall = False
            elif direction == "right":
                current.has_right_wall = False
                self._cells[next_i][next_j].has_left_wall = False
            elif direction == "up":
                current.has_top_wall = False
                self._cells[next_i][next_j].has_bottom_wall = False
            elif direction == "down":
                current.has_bottom_wall = False
                self._cells[next_i][next_j].has_top_wall = False

            self._draw_cell(i, j)
            self._draw_cell(next_i,next_j)

            self._break_walls_r(next_i, next_j)


    def _reset_cells_visited(self):
        for i in range(self._num_cols):
            for j in range(self._num_rows):
                self._cells[i][j].visited = False

    def solve(self):
       return self._solve_r(0, 0)
    
    def _solve_r(self, i, j):
        self._animate()
        current_cell = self._cells[i][j]
        current_cell.visited = True
        
        if i == self._num_cols - 1 and j == self._num_rows - 1:
            return True

        if i + 1 < self._num_cols and not current_cell.has_right_wall and not self._cells[i + 1][j].visited:
            current_cell.draw_move(self._cells[i+1][j])

            if self._solve_r(i+1, j):
                return True
            
            current_cell.draw_move(self._cells[i+1][j], undo=True)

        if j + 1 < self._num_rows and not current_cell.has_bottom_wall and not self._cells[i][j+1].visited:
            current_cell.draw_move(self._cells[i][j+1])
            if self._solve_r(i, j+ 1):
                return True
            current_cell.draw_move(self._cells[i][j+1], undo=True)

        if i - 1 >= 0 and not current_cell.has_left_wall and not self._cells[i-1][j].visited:
            current_cell.draw_move(self._cells[i-1][j])
            if self._solve_r(i-1, j):
                return True
            current_cell.draw_move(self._cells[i-1][j], undo=True)

        if j - 1 >= 0 and not current_cell.has_top_wall and not self._cells[i][j-1].visited:
            current_cell.draw_move(self._cells[i][j-1])
            if self._solve_r(i,j-1):
                return True
            current_cell.draw_move(self._cells[i][j-1], undo=True)

        return False

def main():
    win = Window(800, 600)

    cell = Cell(100, 100, 150, 150, win)
    cell.draw()

    win.wait_for_close()
    maze.solve()

if __name__ == "__main__":
    main()