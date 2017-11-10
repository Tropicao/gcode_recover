# GCode recover tool

Based on last filament output, it will create a new G-code file to resume an interrupted print

* **Author**: Alexis Lothore
* **Contributors**: Romain TAPREST
* **Python versions**: 2.7, 3.6

## Why this tool ?
Since the electrical wiring is quite old in my apartment, my 3D printer often stops its print while in progress, because of electrical parasites. Instead of completely restarting my print when this event occurs, I want to "truncate" the already-printed part of the GCode file, to be able to "resume" the print.

## How to use it
* When a crash occurs, you must at least know the last "consumed filament" status. In my Repetier setup, the relevant information looks like this :

  `14:52:49.115 : N27380 G1 X3.259 Y-6.3 E4517.904*115`

  The interesting part is `E4517.904`

* Start the script passing two parameters : the previously retrieved variable and the original file path.

Example : `python gcode_recover.py E4517.904 ~/USBHolder.gcode`

This call, if successfull, will generate file recovery.gcode wich will be able to restart print at interrupted point
