from tkinter import Tk, BOTH, Canvas

class Window:
    def __init__(self, width, height) -> None:
        self.__root = Tk()
        self.__root.title("maze solver")
        self.__root.protocol("WM_DELETE_WINDOW", self.close)
        self.__canvas = Canvas(self.__root, bg="white", height=height, width=width)
        self.__canvas.pack(fill=BOTH, expand=1)
        self.__running = False

    def redraw(self):
        self.__root.update_idletasks()
        self.__root.update()
    
    def wait_for_close(self):
        self.__running = True
        while self.__running:
            self.redraw()
        print("window closed...")
    
    def draw_line(self, line, fill_color="black"):
        line.draw(self.__canvas, fill_color)
    
    def close(self):
        self.__running = False
        self.__root.quit()

class Point:
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y

class Line:
    def __init__(self, p1, p2) -> None:
        self.p1 = p1
        self.p2 = p2

    def draw(self, canvas, fill_color="black"):
        canvas.create_line(
            self.p1.x, self.p1.y, self.p2.x, self.p2.y, fill=fill_color, width=2
        )

class Cell:
    def __init__(self, has_left_wall, has_right_wall, has_top_wall, has_bottom_wall, _x1, _x2, _y1, _y2, _window=None) -> None:
        self.__window = _window
        self.has_left_wall = has_left_wall
        self.has_right_wall = has_right_wall
        self.has_top_wall = has_top_wall
        self.has_bottom_wall = has_bottom_wall
        self._x1 = _x1
        self._x2 = _x2
        self._y1 = _y1
        self._y2 = _y2
        self.visited = False

    def draw(self, _color="black"):
        x1, y1, x2, y2 = self._x1, self._y1, self._x2, self._y2

        if self.has_top_wall:
            l = Line(Point(x1, y1), Point(x2, y1))
            self.__window.draw_line(l, _color)

        if self.has_left_wall:
            l = Line(Point(x1, y1), Point(x1, y2))
            self.__window.draw_line(l, _color)
        if self.has_right_wall:
            l = Line(Point(x2, y1), Point(x2, y2))
            self.__window.draw_line(l, _color)
        if self.has_bottom_wall:
            l = Line(Point(x1, y2), Point(x2, y2))
            self.__window.draw_line(l, _color)

    def mid_point(self):
        return Point((self._x1 + self._x2) / 2, (self._y1 + self._y2) / 2)

    def draw_move(self, to_cell, undo=False):
        line = Line(self.mid_point(), to_cell.mid_point())
        if undo:
            self.__window.draw_line(line, "gray")
        else:
            self.__window.draw_line(line, "red")


