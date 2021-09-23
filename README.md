# sediMETU v1.0.1
sediMETU is a basic calculator for sediment-related parameters with a simple GUI.
Developed by Yagiz Arda Cicek, Ⓒ 2021 in METU using the formulas obtained from Soulsby, 1997.
You can switch between Current, Wave, and Current+Wave modes using the tabs at the top. Fill the input section with known parameters and hit "Calculate!".

NOTE 1: If you get "Windows protected your PC" error, click on "More info" and press "Run anyway". This error is caused by lack of certification/sign (too expensive to buy, sorry).

NOTE 2: You may also compile the software by using "pyinstaller --onefile -w --icon app.ico sediMETU.py" command without the quotation marks. Make sure Python 3.8.6 and the related libraries (PyQt5, numpy etc.) are installed too.

This software is developed only for educational purposes and might contain errors. Please use it with caution.
Contact ciceka@metu.edu.tr if you encounter any problems or calculation errors.

What's new in v.1.0.1 (22.09.2021):
- Program returns NaN values for out of limit conditions,
- Better input error handling algorithm,
- d50 is now entered as mm,
- v (kinematic viscosity) should be entered as (v_actual)/10^-6, e.g. for 0.00000136 -> enter 1.36,
- Table 7 dropdown list is added for Wave module (you can now directly select the bed-type from the list),
- Bug fixes for formulas.
