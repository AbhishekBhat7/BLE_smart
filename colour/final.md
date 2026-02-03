1) Phantom Lighting  

ff 55 0b 00 02 28 01 [AA BB] [AA BB]

here AA BB represents the colour degree decimal value 
ex 4 deg means 00 04 which should be repeated twise as it contains 2 leds (Dual Channel Control)


2) Reminder
ff 55 08 00 02 2b 00 [AB]
here AB represents Hue of the colour 
the wheel is circle so (0 to 360 ) so in a single hex byte value ranges from 0 to 255 (0 to FF)

formula = (deg/360) * 255 = decimal value -> hex value


