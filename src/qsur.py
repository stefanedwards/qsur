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
qstat_lines = 0

def get_qstat(user=USER):
  #p1 = Popen(['qstat', '-u', user], shell=FALSE, stdout=PIPE)
  output = check_output(['qstat', '-u', user], shell=False)
  output = output.split('\n')[2:]
  output = '\n'.join(output)
  return output

def print_qstat(stdscr, y=3, x_offset=1):
  global qstat_lines
  qstat = [l.rstrip() for l in get_qstat().split('\n')]
  stdscr.addstr(y, x_offset, qstat[0])
  y += 1
  stdscr.addstr(y, x_offset, qstat[1])
  y += 1
  stdscr.addstr(y, x_offset, qstat[2])
  y += 1  

  if qstat_lines > len(qstat):
    stdscr.clearok(1)
  qstat_lines = len(qstat)

  for l in qstat[3:]:
    # goto state:
    state = re_state.search(l, pos=80, endpos=93)
    if state is None:
      try:
        stdscr.addstr(y, x_offset, l)
      except curses.error:
        pass
    else:
      start = state.start(1)
      end   = state.span(1)[1]
      state = state.groups()[0]

      state_att = curses.A_NORMAL
      line_att = curses.A_NORMAL
 
      #stdscr.addstr(6,2, state.group())
      if state == 'E' or state == 'C':
        state_att = curses.A_BLINK
      if state == 'W':
        state_att = curses.A_DIM
        line_att = curses.A_DIM
      try:
        stdscr.addstr(y, x_offset, l[:start], line_att)
        stdscr.addstr(l[start], state_att) ## write state
        stdscr.addstr(l[end:], line_att)  ## remaining line
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
  print_qstat(stdscr)
  #stdscr.refresh()

  #qstat_win = curses.newwin(8, 94, 3, 1)


  stdscr.nodelay(1)  # getch is non-blocking
  start = time()
  wait = time()
  while True:
    print_right_time(stdscr, y=1)
    c = stdscr.getch()
    if c == ord('q') or c == ord('Q'):
      break
    if time() >= wait + 5:
      print_qstat(stdscr)
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
