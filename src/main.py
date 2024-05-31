from Maze import Maze
from graphics import Window,Line,Point,Cell


def main():
    win = Window(800,800)
    # l = Line(Point(50,50),Point(400,400))
    # win.draw_line(l,"black")
    # cell = Cell(win,has_left_wall=True,has_right_wall=True,has_top_wall=True,has_bottom_wall=True,_x1= 100,_x2=400,_y1=100,_y2=400)
    # cell.draw()
    # cell2 = Cell(win,has_left_wall=True,has_right_wall=True,has_top_wall=True,has_bottom_wall=True,_x1= 400,_x2=700,_y1=100,_y2=400)
    # cell2.draw()
    # cell2.draw_move(cell,False)
    maze = Maze(50,50,60,60,None,None,win,20)

    

    win.wait_for_close()




main()