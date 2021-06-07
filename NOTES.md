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
### User interface
A total revision of the user interface: Groupbox "Input" added, containing all the input data in 
scientific notation. The label fields have the name op the input fields with _4Calc added. Further no changes. 
###Change code PrControl.py:
- Class MainWindowExec to be changed according to the new user interface: output is sent to "4Calc" fields. revision of 
  the methods triggered by line edit do not require any change. 
- Add Class "warning" to communicate inconsistencies as roughness is greater than diameter - Reading the documentation 
  of QDialog gave the insight that the module PD_Dialog.py is overdone to show messages in pyqt5. QMessagebox gives 
  enough functionality for this job. A new class Messages is introduced making PD_Dialog and class DialogGeneral 
  obsolete for now a message, and a warning are added to the class. This class is to be extended and probably to be 
  moved to a module. A message is already introduced at roughness and diameter
- Deal with input error diameter < roughness - Method Calculate-calculate_friction_factor updated to deal with the error
  and give the correct output. Class calc calculation methods started in right sequence by calculation_start() which is 
  called by gui. number arguments zero instead of none. some bugs eliminated each method checks its own prerequisites. 
  Class calc can stand on its own now. Warning message in line_diameter_start() and line_roughness_start() 
- Class Calculate basically not to be changed consider subclasses - better not to have subclasses since all the args 
  remain in one class/object. Class Calculation is beneficial for it can work wit a cli as well. 
- Class CheckInput - No change required
- Class DialogGeneral - Not required anymore
## Control
See V1.0_tests.md
modifications based on the outcome of the tests:
- Correction layout
- Outcome in bar and in Pa
- Fixed bug in class CheckInput
- Improved behaviour of radio buttons
- Class Calculate deals with divisions by zero and negative values
- Modification class CheckInput: add error message. In case of an error always return 0. 
