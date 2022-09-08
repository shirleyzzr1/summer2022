from curses import wrapper
import curses

# def main(stdscr):
#     curses.init_pair(1,curses.COLOR_BLUE,curses.COLOR_YELLOW)
#     curses.init_pair(2,curses.COLOR_GREEN,curses.COLOR_BLACK)
#     BLUE_AND_YELLOW = curses.color_pair(1)
#     GREEN_AND_BLACK = curses.color_pair(2)
#     x,y = 0,0
#     while True:
#         key = stdscr.getkey()
#         if key =="KEY_LEFT":
#             x -=1
#         elif key=="KEY_RIGHT":
#             x+=1
#         elif key=="KEY_UP":
#             y-=1
#         elif key=="KEY_DOWN":
#             y+=1

#         stdscr.clear()
#         stdscr.addstr(y,x,"0")
#         stdscr.refresh()
#     stdscr.clear()
#     stdscr.addstr(10,10,"helloworld",BLUE_AND_YELLOW)
#     stdscr.addstr(10,12,"overwritten")
#     stdscr.addstr(15,25,"great job",GREEN_AND_BLACK | curses.A_BOLD)

#     key = stdscr.getkey()
#     stdscr.addstr(5,5,f"Key: {key}")

#     stdscr.refresh()
#     stdscr.getch()

def kbhit():
    ch = stdscr.getch()
    if ch!=curses.ERR:
        curses.ungetch(ch)
        return True
    else:
        return False

# wrapper(main)
stdscr = curses.initscr()
curses.noecho()
curses.cbreak()
curses.start_color()
stdscr.keypad(True)
stdscr.nodelay(True)
curses.init_pair(1,curses.COLOR_BLUE,curses.COLOR_YELLOW)
curses.init_pair(2,curses.COLOR_GREEN,curses.COLOR_BLACK)
BLUE_AND_YELLOW = curses.color_pair(1)
GREEN_AND_BLACK = curses.color_pair(2)
x,y = 0,0
res = ""
while True:
    # stdscr.clear()
    # key = stdscr.getkey()
    # if key =="KEY_LEFT":
    #     x -=1
    # elif key=="KEY_RIGHT":
    #     x+=1
    # elif key=="KEY_UP":
    #     y-=1
    # elif key=="KEY_DOWN":
    #     y+=1
    # stdscr.clear()
    # stdscr.addstr(y,x,"0")
    # stdscr.refresh()

    if kbhit():
        res = "key was pressed: {}".format(stdscr.getch())
    else:
        res = "no key pressed"
    stdscr.addstr(y,x,res)
    stdscr.refresh()

