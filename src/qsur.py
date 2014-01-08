#!/usr/bin/python2.7

from __future__ import print_function
from subprocess import *
import curses
import os
import sys
from time import sleep, strftime, time
import re

USER = os.environ['USER']

re_state = re.compile(' ([CHERW]) ')

def get_qstat(user=USER):
  #p1 = Popen(['qstat', '-u', user], shell=FALSE, stdout=PIPE)
  output = check_output(['qstat', '-u', user], shell=False)
  output = output.split('\n')[2:]
  output = '\n'.join(output)
  return output

def print_qstat_head(stdscr, qstat, y=3, x_offset=1):
  stdscr.addstr(y, x_offset, qstat[0])
  y += 1
  stdscr.addstr(y, x_offset, qstat[1])
  y += 1
  stdscr.addstr(y, x_offset, qstat[2])
  y += 1  
    
def print_qstat_jobs(stdscr, qstat, y=6, x_offset=1):
  for l in qstat:
    # goto state:
    state = re_state.search(l, pos=80, endpos=93)
    try:
      stdscr.addstr(y, x_offset, l)
    except curses.error:
      pass

    if state is not None:
      start = state.start(1)
      end   = state.span(1)[1]
      state = state.groups()[0]

      state_att = curses.A_NORMAL
      line_att = curses.A_NORMAL
 
      if state == 'E' or state == 'C':
        state_att = curses.A_BLINK
      if state == 'W':
        state_att = curses.A_DIM
        line_att = curses.A_DIM
      try:
        if line_att != curses.A_NORMAL:
          stdscr.addstr(y, x_offset, l, line_att)
        if state_att != curses.A_NORMAL:
          stdscr.addstr(y, x_offset+start, state, state_att)
      except curses.error:
        pass
    y += 1
  stdscr.refresh()

def print_time(stdscr, y=2, x=1):
  stdscr.addstr(y, x, strftime('%Y-%m-%d %H:%M:%S  '))
  stdscr.refresh()

def print_right_time(stdscr, y=3):
  time_length = 20
  x = stdscr.getmaxyx()[1] - time_length
  print_time(stdscr, y, x)

def main(stdscr):
  #print('Qstat for user', USER)
  #print('Hello world!')
  #print(get_qstat())
  curses.curs_set(0)
  stdscr.move(5,5)
  stdscr.addstr(1,1, 'qstat for user ')
  stdscr.addstr(USER, curses.A_BOLD) 
  print_right_time(stdscr, y=1)
  qstat = [l.rstrip() for l in get_qstat().split('\n')]
  print_qstat_head(stdscr, qstat)
  if len(qstat) > 3:
    print_qstat_jobs(stdscr, qstat[3:])

  #print_qstat(stdscr)
  #stdscr.refresh()

  #qstat_win = curses.newwin(8, 94, 3, 1)
  qstat_lines = 0

  stdscr.nodelay(1)  # getch is non-blocking
  start = time()
  wait = time()
  while True:
    print_right_time(stdscr, y=1)
    c = stdscr.getch()
    if c == ord('q') or c == ord('Q'):
      break
    if time() >= wait + 30:
      qstat = [l.rstrip() for l in get_qstat().split('\n')]
      if len(qstat) != qstat_lines:
        stdscr.clear()
        print_qstat_head(stdscr, qstat)
        qstat_lines = len(qstat)
      if len(qstat) > 3:
        print_qstat_jobs(stdscr, qstat[3:])
      wait = time()
    #if time() >= start + 30:
    #  break
    sleep(1)
  #stdscr.addstr(3,1, get_qstat())
  #stdscr.refresh()
  #sleep(2)

#main()

curses.wrapper(main)

#print(get_qstat())

#print(USER)
#print(get_qstat())

#stdscr = curses.initscr()
#curses.noecho()  ## disables echoing of keys to the screen
#curses.cbreak()  ## react to keys instantly (i.e. do not wait for Enter)
#stdscr.keypad(1) ## enable use of special keys (Page Up, Home, etc.)

## When exiting:
#curses.nocbreak(); stdscr.keypad(0); curses.echo()
#curses.endwin()
