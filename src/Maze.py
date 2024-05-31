from graphics import Cell, Point, Window
import random
import time

class Maze:
    def __init__(self, x1, y1, cell_size_x, cell_size_y, _num_rows=None, _num_cols=None, _win=None, seed=None):
        self.x1 = x1
        self.y1 = y1
        self._num_rows = _num_rows
        self._num_cols = _num_cols
        self.cell_size_x = cell_size_x
        self.cell_size_y = cell_size_y
        self._win = _win
        self.seed = seed
        self._cells = []
        
        if self.seed is not None:
            random.seed(self.seed)
            self._num_rows, self._num_cols = [random.randrange(5, 15) for _ in range(2)]

        self._create_cells()
        self._break_entrance_and_exit()
        self._break_walls_r(0, 0)
        
        for column in self._cells:
            for cell in column:
                self._draw_cell(cell, "black")
                self._animate()
        self._reset_cells_visited()
        
        self._solve()

    def _create_cells(self):
        self._cells = []
        for row in range(self._num_rows):
            column = []
            for col in range(self._num_cols):
                x1 = self.x1 + col * self.cell_size_x
                y1 = self.y1 + row * self.cell_size_y
                x2 = x1 + self.cell_size_x
                y2 = y1 + self.cell_size_y

                has_left_wall = True
                has_right_wall = True
                has_top_wall = True
                has_bottom_wall = True

                cell = Cell(has_left_wall, has_right_wall, has_top_wall, has_bottom_wall, x1, x2, y1, y2, self._win)
                cell.visited = False
                column.append(cell)

            self._cells.append(column)

        for column in self._cells:
            for cell in column:
                self._draw_cell(cell, "#d9d9d9")
                self._animate()

    def _draw_cell(self, cell, color="black"):
        cell.draw(color)

    def _animate(self):
        self._win.redraw()
        time.sleep(0.05)

    def _break_entrance_and_exit(self):
        self._cells[0][0].has_top_wall = False
        self._draw_cell(self._cells[0][0], "black")

        self._cells[self._num_rows - 1][self._num_cols - 1].has_bottom_wall = False
        self._draw_cell(self._cells[self._num_rows - 1][self._num_cols - 1], "black")

        # for column in self._cells:
        #     for cell in column:
        #         self._draw_cell(cell, "black")
        #         self._animate()
    
    def _break_wall(self, cell1, cell2):
        if cell1.x1 == cell2.x1 and cell1.y1 < cell2.y1:  # cell2 is below cell1
            cell1.has_bottom_wall = False
            cell2.has_top_wall = False
        elif cell1.x1 == cell2.x1 and cell1.y1 > cell2.y1:  # cell2 is above cell1
            cell1.has_top_wall = False
            cell2.has_bottom_wall = False
        elif cell1.y1 == cell2.y1 and cell1.x1 < cell2.x1:  # cell2 is to the right of cell1
            cell1.has_right_wall = False
            cell2.has_left_wall = False
        elif cell1.y1 == cell2.y1 and cell1.x1 > cell2.x1:  # cell2 is to the left of cell1
            cell1.has_left_wall = False
            cell2.has_right_wall = False

        self._draw_cell(cell1, "black")
        self._draw_cell(cell2, "black")
        self._animate()

    def _break_walls_r(self, i, j):
        self._cells[i][j].visited = True
        while True:
            next_index_list = []

            if i > 0 and not self._cells[i - 1][j].visited:
                next_index_list.append((i - 1, j))
            if i < self._num_rows - 1 and not self._cells[i + 1][j].visited:
                next_index_list.append((i + 1, j))
            if j > 0 and not self._cells[i][j - 1].visited:
                next_index_list.append((i, j - 1))
            if j < self._num_cols - 1 and not self._cells[i][j + 1].visited:
                next_index_list.append((i, j + 1))

            if len(next_index_list) == 0:
                self._draw_cell(self._cells[i][j], "black")
                return

            direction_index = random.randrange(len(next_index_list))
            next_index = next_index_list[direction_index]

            if next_index[0] == i + 1:
                self._cells[i][j].has_right_wall = False
                self._cells[i + 1][j].has_left_wall = False
            if next_index[0] == i - 1:
                self._cells[i][j].has_left_wall = False
                self._cells[i - 1][j].has_right_wall = False
            if next_index[1] == j + 1:
                self._cells[i][j].has_bottom_wall = False
                self._cells[i][j + 1].has_top_wall = False
            if next_index[1] == j - 1:
                self._cells[i][j].has_top_wall = False
                self._cells[i][j - 1].has_bottom_wall = False

            self._break_walls_r(next_index[0], next_index[1])

    def _reset_cells_visited(self):
        for column in self._cells:
            for cell in column:
                cell.visited = False

    def _solve(self):
        return self._solve_r(0, 0)

    def _solve_r(self, i, j):
        self._animate()

        self._cells[i][j].visited = True

        if i == self._num_rows - 1 and j == self._num_cols - 1:
            return True

        next_index_list = []

        if i > 0 and not self._cells[i - 1][j].visited:
            next_index_list.append((i - 1, j))
        if i < self._num_rows - 1 and not self._cells[i + 1][j].visited:
            next_index_list.append((i + 1, j))
        if j > 0 and not self._cells[i][j - 1].visited:
            next_index_list.append((i, j - 1))
        if j < self._num_cols - 1 and not self._cells[i][j + 1].visited:
            next_index_list.append((i, j + 1))

        for next_index in next_index_list:
            ni, nj = next_index
            if not self._cells[i][j].has_right_wall and ni == i + 1:
                self._cells[i][j].draw_move(self._cells[ni][nj])
                if self._solve_r(ni, nj):
                    return True
                self._cells[i][j].draw_move(self._cells[ni][nj], undo=True)
            if not self._cells[i][j].has_left_wall and ni == i - 1:
                self._cells[i][j].draw_move(self._cells[ni][nj])
                if self._solve_r(ni, nj):
                    return True
                self._cells[i][j].draw_move(self._cells[ni][nj], undo=True)
            if not self._cells[i][j].has_bottom_wall and nj == j + 1:
                self._cells[i][j].draw_move(self._cells[ni][nj])
                if self._solve_r(ni, nj):
                    return True
                self._cells[i][j].draw_move(self._cells[ni][nj], undo=True)
            if not self._cells[i][j].has_top_wall and nj == j - 1:
                self._cells[i][j].draw_move(self._cells[ni][nj])
                if self._solve_r(ni, nj):
                    return True
                self._cells[i][j].draw_move(self._cells[ni][nj], undo=True)

        return False
