import curses
from curses import wrapper
from time import sleep

class Menu(object):
    def __init__(self,flow_def):
        curses.curs_set(0)
        stdscr = curses.initscr()
        self.items = self.generate_items(flow_def)
        self.window = stdscr.subwin(10,30,0,0)
        self.position = 0
        self.flag = -1
    
    def generate_items(self,flow_def):
        res = []
        for flow in flow_def:
            str = flow["node"] + " " + flow["action_handle"]
            res.append(str)
        return res

    def navigate(self,n):
        """
        Make sure the cursor is not out of boundry
        """
        self.position+=n
        if self.position<0:
            self.position = 0
        elif self.position >= len(self.items):
            self.position = len(self.items) - 1

    def display(self):
        """
        Update menu display
        """
        for index, item in enumerate(self.items):
            if index == self.position:
                mode = curses.A_REVERSE
            else:
                mode = curses.A_NORMAL

            msg = "%d. %s" % (index, item)
            self.window.addstr(1 + index, 1, msg, mode)

        # if key in [curses.KEY_ENTER, ord("\n")]:
        #     if self.position == len(self.items) - 1:
        #         return True
        #     else:
        #         self.flag = self.position
        self.navigate(1)
        self.window.refresh()
    

def main(stdscr):
    flow_def = [
        {'node':'sciclops_node','action_handle':'get_plate','action_vars':{'pos':'tower1'}},
        {'node':'pf400_node','action_handle':'transfer','action_vars':{'pos1':'cyclops_ext','pos2':'sealerPos'}},
        {'node':'sealer_node','action_handle':'seal','action_vars':{'time':175,'temp':3}},
        {'node':'pf400_node','action_handle':'transfer','action_vars':{'pos1':'sealerPos','pos2':'peelerPos'}},
        {'node':'peeler_node','action_handle':'peel','action_vars':{}},
        {'node':'pf400_node','action_handle':'transfer','action_vars':{'pos1':'peelerPos','pos2':'cyclops_ext'}}
        ]
    menu = Menu(flow_def)
    for i in range(len(flow_def)):
        menu.display()
        sleep(1)
if __name__=="__main__":
    wrapper(main)

    