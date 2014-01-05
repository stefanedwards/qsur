#!/usr/bin/python2.7

from __future__ import print_function
import curses
import os
from time import sleep, strftime, time

USER = os.environ['USER']

def print_time(stdscr, y=2, x=1):
  stdscr.addstr(y, x, strftime('%Y-%m-%d %H:%m:%S'))


def print_right_time(stdscr, y=3):
  time_length = 19
  x = stdscr.getmaxyx()[1] - time_length
  print_time(stdscr, y, x)


def main(stdscr):
  curses.curs_set(0)  ## sets cursor to be invisible
  stdscr.addstr(1,1, 'qstat for user ')
  stdscr.addstr(USER, curses.A_BOLD) 
  print_right_time(stdscr, y=1)
  stdscr.refresh()

  stdscr.nodelay(1)  # set nodelay(1) to make getch non-blocking
  start = time()
  wait = time()
  while True:
    print_right_time(stdscr, y=1)
    stdscr.refresh()
    c = stdscr.getch()  ## without nodelay(1), code stops here and waits for input
                        ## getch returns ascii code, so to compare with a character, use `ord`-function.
    if c == ord('q') or c == ord('Q'):
      break
    if time() >= start + 60: ## limits total running time to 60 seconds
      print_qstat(stdscr)
    sleep(1)


## normally, you could do the below
#stdscr = curses.initscr()
#curses.noecho()  ## disables echoing of keys to the screen
#curses.cbreak()  ## react to keys instantly (i.e. do not wait for Enter)
#stdscr.keypad(1) ## enable use of special keys (Page Up, Home, etc.)
# main(stdscr)
## When exiting:
#curses.nocbreak(); stdscr.keypad(0); curses.echo()
#curses.endwin()
## but instead, we use the wrapper function 
## -- the function `main` receivies the "main window" as an argument.

curses.wrapper(main)
