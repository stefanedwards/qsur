qsur
====

Python script that demonstrates curses by a qsub surveillance example.

The `qsub` is a job-queing system where we can look at our current jobs with the command `qstat -u <user>`.
This is a static output to stdout - but if we want to keep an active eye on our jobs (e.g. waiting for something to finish) ala `top`, we can use this script.

To use
------

Get the `qsur.py` file, run in a terminal as `python qsur.py`. 
Does not run in Windows as the `curses`-library is not supported here.


curses
------
Terminal handling for character-cell displays, it basically allows you to make text based GUI. Look at e.g. `top`.

To use with python look at a small introduction at http://docs.python.org/2/howto/curses.html and the documentation at http://docs.python.org/2/library/curses.html

- [ ] Make simple curses example, e.g. curse_example.py

