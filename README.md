# PressureDrop
Simple Pressure drop calculator programmed in Python
The program is licensed under GNU General Public License v3.0

Versions: the program was programmed and tested in:
Python: version 3.7.3
Qt:     version 5.11.3

Both Python scripts: PresDr.py and PresDrControl.py should be copied to a directory. 
Obviously Python is required. On Mac and Linux it is usually preinstalled
Make sure sys, math, pyqt5, and scipy are installed. Installation procedure depends 
on your platform. 
Start from cli with 
    python PresDrControl.py 

The current version is very basic and uses SI units in scientific notation only. 
In future a want to add some convenience and also the possibility to include valves, 
bends etc. 

Please take into account that currently there is one issue: a roughness larger than 
the pipe diameter causes a crash. Fixing this will be the first update.

Any suggestion is appreciated
