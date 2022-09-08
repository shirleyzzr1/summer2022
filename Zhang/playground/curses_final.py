import curses
from curses.textpad import Textbox, rectangle
import yaml
class Menu(object):
    def __init__(self,items,stdscr):
        self.window = stdscr.subwin(10,60,13,10)
        self.position = 0
        self.items = items
        self.items.append("exit")
        self.flag = -1
    
    def navigate(self,n):
        self.position+=n
        if self.position<0:
            self.position = 0
        elif self.position >= len(self.items):
            self.position = len(self.items) - 1

    def display(self,key):
        for index, item in enumerate(self.items):
            if index == self.position:
                mode = curses.A_REVERSE
            else:
                mode = curses.A_NORMAL

            msg = "%d. %s" % (index, item)
            self.window.addstr(1 + index, 1, msg, mode)

        if key in [curses.KEY_ENTER, ord("\n")]:
            if self.position == len(self.items) - 1:
                return True
            else:
                self.flag = self.position
                self.window.addstr(2, 30, "{} success!".format(self.items[self.position]))


        elif key == curses.KEY_UP:
            self.navigate(-1)

        elif key == curses.KEY_DOWN:
            self.navigate(1)
        self.window.refresh()
        self.flag=-1

class DrawCurses(object):
    def __init__(self,machines) -> None:
        self.stdscr = curses.initscr()
        self.curses_init()
        self.machines = machines
        self.wins = []
        self.draw_init()


    def curses_init(self):
        curses.curs_set(0)
        self.stdscr.keypad(True)
        self.stdscr.nodelay(True)
        self.stdscr.clear()

        curses.init_pair(1,curses.COLOR_GREEN,curses.COLOR_BLACK)
        curses.init_pair(2,curses.COLOR_RED,curses.COLOR_BLACK)
        self.GREEN_AND_BLACK = curses.color_pair(1)
        self.RED_AND_BLACK = curses.color_pair(2)

    def draw_init(self):
        for i in range(len(self.machines)):
            rectangle(self.stdscr,2,10+20*i,10,25+20*i)
            self.stdscr.addstr(2,15+20*i,self.machines[i][0])
            type = "type: {}".format(self.machines[i][1])
            self.stdscr.addstr(4,11+20*i,type)
            self.stdscr.addstr(5,11+20*i,"State:ERROR",self.RED_AND_BLACK)
            wins = curses.newwin(1,14,5,11+20*i)
            self.wins.append(wins)


    def update_state(self,states):
        for i in range(len(self.wins)):
            state = "State: {}".format(states[self.machines[i][0]])
            self.wins[i].addstr(0,0,state,self.GREEN_AND_BLACK)
            self.wins[i].refresh() 

def main(stdscr):
    user_path = "./example_ws.yml"
    workcell_data = yaml.safe_load(open(user_path))
    machines= workcell_data['modules']
    names = []
    states = {}
    for m in machines:
        names.append([m['name'],m['type']])
        states[m['name']]="BUSY"
    drawcurses = DrawCurses(names)
    items = ["Start Execution","Raise Emergency","Clear Emergency"]
    menu = Menu(items,drawcurses.stdscr)


    while True:
        # stdscr.clear()
        try:
            k = drawcurses.stdscr.getch()
        except:
            k = None
        drawcurses.update_state(states)
        if menu.display(k):
            break
        # drawcurses.stdscr.refresh()
        # drawcurses.stdscr.getch()
if __name__=="__main__":
    curses.wrapper(main)
