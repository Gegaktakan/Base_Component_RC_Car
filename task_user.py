"""

task_user takes user usb keyboard imput and changes the runmode, speed, angle
and esc shared variables

"""

#import curses to not freeze waiting for user input
import curses

#import shared variables
import config

class userInput:
    def __init__(self):
        #initiate a curses screen
        global stdscr
        stdscr = curses.initscr()   
        curses.noecho()
        stdscr.keypad(True)
        curses.cbreak()
        stdscr.addstr("init hit\n")

    def check_input(self):
        stdscr.nodelay(1)
        #recieve last character entered from curses
        entered = stdscr.getch()

        # Mode control if 0,1,2 or q are entered
        if entered==ord('0'):
            #stdscr.addstr("key 0\n")
            config.runMode = 0
        elif entered==ord('1'):
            #stdscr.addstr("key 1\n")
            config.runMode = 1
        elif entered==ord('2'):
            #stdscr.addstr("key 2\n")
            config.runMode = 2
        elif entered==ord('q'):
            #q exits program
            stdscr.addstr("exit\n")
            config.esc = 1
            self.user_exit()

        #if in manual a, w, s, and d control incrementer    
        elif config.runMode==1:    
            if entered==ord('w'):
                #stdscr.addstr("key w\n")
                if(config.speed<4000):
                    config.speed = config.speed+400
            elif entered==ord('s'):
                #stdscr.addstr("key s\n")
                if(config.speed>-4000):
                    config.speed = config.speed-400
            elif entered==ord('a'):
                #stdscr.addstr('key a, ang:{}\n'.format(config.ang))
                if(config.ang<490):
                    config.ang = config.ang+((490.0-310.0))*.1
            elif entered==ord('d'):
                #stdscr.addstr('key d, ang:{}\n'.format(config.ang))
                if(config.ang>310):
                    config.ang = config.ang-((490.0-310.0))*.1

    #exit curses nicely
    def user_exit(self):
        curses.echo()
        stdscr.keypad(False)
        curses.nocbreak()
        curses.endwin()


