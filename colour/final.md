1) Phantom Lighting  

ff 55 0b 00 02 28 01 [AA BB] [AA BB]

here AA BB represents the colour degree decimal value 
ex 4 deg means 00 04 which should be repeated twise as it contains 2 leds (Dual Channel Control)

ff550800022b0000.   for red reminder
ff550800022b00e6    for blue reminder





3) Phantom page reminder
ff550b00022801000e00d7      :-> phantom page slider
ff550700022701.  :-> auto stand by 10s  ( here last data can go upto 3) (00, 01, 02, 03)
ff550700022a01.  :-> Gradient mode (00,01,02)


2) Reminder
ff 55 08 00 02 2b 00 [AB]
here AB represents Hue of the colour 
the wheel is circle so (0 to 360 ) so in a single hex byte value ranges from 0 to 255 (0 to FF)

formula = (deg/360) * 255 = decimal value -> hex value


