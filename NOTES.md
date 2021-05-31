# DMAIC: Pressure drop - Restructure code
## Define
After editingFinished in one of the line edits a method is called. This method takes the string from the line edit and 
feeds it into object from class CheckInput. The string is converted into a float and, passed to the calc object.  
Next the calculation in the calc object is started and runs all calculations. The last step is generating the output 
which basically is a reformat of all input fields to uniform scientific notation and filling the output fields with the 
known values.  
When adding a message in the method started after editingFinished I noticed the message came twice. In case od a dialog
,not taking focus, a recursive error popped up. (the dialog was called when is was not closed yet.)
## Measure
The issue is caused by reformatting the line edit field in the output which triggers the method after editingFinished 
once again. Unless the error handling is done by a validator in the lineEdit field. The latter might be a pain in the 
ass for the user
## Analyze
Reformatting the line input field by code is to be avoided for this leads to the above issues. I still want to have the 
in- and output on the same screen which is possible since the amount of data is not very big. Each line edit will have a
label which shows the reformatted input. 
## Improve
A total revision of the user interface - to do  
Change code PrControl.py:
- Class MainWindowExec to be changed according to the new user interface todo
- Class Calculate basically not to be changed consider subclasses - todo
- Class CheckInput - No change required
- Class DialogGeneral - No change required
## Control
testing to be defined