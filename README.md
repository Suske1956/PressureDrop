# SiPreDroCal  (Simple Pressure Drop Calculator)
Version 1.1 November 1st, 2021 Development see V1.1_notes.md

Simple Pressure drop calculator programmed in Python  
License: GNU General Public License v3.0

Versions for programming and testing:  
Python: version 3.9.2  
Qt:     version 5.15.2

Python scripts: PresDr.py, and PresDrControl.py should be copied to a directory.  
Obviously Python is a requirement. On Mac and Linux it is usually preinstalled  
Make sure sys, math, pyqt5, and scipy are installed. Installation procedure depends 
on your platform.  
Start from cli with: python PresDrControl.py 

The current version (1.0) is very basic and presents values in SI units and scientific notation.  
Calculation methods used: laminar flow, Blasius, Colebrook-White.  
In version 1.1 including fittings in the pipeline will be added. 

I appreciate any suggestion.
