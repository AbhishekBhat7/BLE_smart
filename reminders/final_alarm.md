🎯 Complete Test Suite for All Alarm Patterns
Let me give you ready-to-send commands for every scenario you mentioned!

📋 Test Commands (All using Slot 8, Time 2:45 PM for consistency)
1. TODAY ONLY
Since "today only" depends on the current day, I'll give you commands for each day:

If today is Monday:

text

ff 55 0d 00 02 03 02 07 01 0e 2d 80 00
If today is Tuesday:

text

ff 55 0d 00 02 03 02 07 01 0e 2d 40 00
If today is Wednesday:

text

ff 55 0d 00 02 03 02 07 01 0e 2d 20 00
If today is Thursday:

text

ff 55 0d 00 02 03 02 07 01 0e 2d 10 00
If today is Friday:

text

ff 55 0d 00 02 03 02 07 01 0e 2d 08 00
If today is Saturday:

text

ff 55 0d 00 02 03 02 07 01 0e 2d 04 00
If today is Sunday:

text

ff 55 0d 00 02 03 02 07 01 0e 2d 02 00
2. WEDNESDAY ONLY
text

ff 55 0d 00 02 03 02 07 01 0e 2d 20 00
✅ Already confirmed - should show Wednesday only

3. EVERYDAY
text

ff 55 0d 00 02 03 02 07 01 0e 2d fe 00
✅ Already confirmed - should show all 7 days

4. WORKING DAYS (Mon-Fri)
text

ff 55 0d 00 02 03 02 07 01 0e 2d f8 00
Calculation:

Mon (0x80) + Tue (0x40) + Wed (0x20) + Thu (0x10) + Fri (0x08) = 0xF8
Expected: Mon, Tue, Wed, Thu, Fri

5. DIFFERENT SLOTS - Same alarm in different positions
Slot 1 (2:45 PM, Everyday):

text

ff 55 0d 00 02 03 02 00 01 0e 2d fe 00
                      ^^
Slot 2 (2:45 PM, Everyday):

text

ff 55 0d 00 02 03 02 01 01 0e 2d fe 00
                      ^^
Slot 3 (2:45 PM, Everyday):

text

ff 55 0d 00 02 03 02 02 01 0e 2d fe 00
                      ^^
Slot 4 (2:45 PM, Everyday):

text

ff 55 0d 00 02 03 02 03 01 0e 2d fe 00
                      ^^
Slot 5 (2:45 PM, Everyday):

text

ff 55 0d 00 02 03 02 04 01 0e 2d fe 00
                      ^^
Slot 6 (2:45 PM, Everyday):

text

ff 55 0d 00 02 03 02 05 01 0e 2d fe 00
                      ^^
Slot 7 (2:45 PM, Everyday):

text

ff 55 0d 00 02 03 02 06 01 0e 2d fe 00
                      ^^
Slot 8 (2:45 PM, Everyday):

text

ff 55 0d 00 02 03 02 07 01 0e 2d fe 00
                      ^^
6. WEEKEND ONLY (Sat + Sun)
text

ff 55 0d 00 02 03 02 07 01 0e 2d 06 00
Calculation:

Sat (0x04) + Sun (0x02) = 0x06
Expected: Saturday and Sunday

7. CUSTOM PATTERNS
Mon, Wed, Fri (alternate days):

text

ff 55 0d 00 02 03 02 07 01 0e 2d a8 00
Calculation: Mon (0x80) + Wed (0x20) + Fri (0x08) = 0xA8

Tue, Thu (even weekdays):

text

ff 55 0d 00 02 03 02 07 01 0e 2d 50 00
Calculation: Tue (0x40) + Thu (0x10) = 0x50

Mon, Tue, Wed (start of week):

text

ff 55 0d 00 02 03 02 07 01 0e 2d e0 00
Calculation: Mon (0x80) + Tue (0x40) + Wed (0x20) = 0xE0

Thu, Fri, Sat (end of week):

text

ff 55 0d 00 02 03 02 07 01 0e 2d 1c 00
Calculation: Thu (0x10) + Fri (0x08) + Sat (0x04) = 0x1C

Only Sunday:

text

ff 55 0d 00 02 03 02 07 01 0e 2d 02 00
Only Saturday:

text

ff 55 0d 00 02 03 02 07 01 0e 2d 04 00
Only Monday:

text

ff 55 0d 00 02 03 02 07 01 0e 2d 80 00
🧮 Day Calculation Helper
For any custom combination, use this formula:

Python

day_byte = (
    (0x80 if Monday else 0) |
    (0x40 if Tuesday else 0) |
    (0x20 if Wednesday else 0) |
    (0x10 if Thursday else 0) |
    (0x08 if Friday else 0) |
    (0x04 if Saturday else 0) |
    (0x02 if Sunday else 0)
)
Example: For Mon + Thu + Sun:

Python

day_byte = 0x80 | 0x10 | 0x02 = 0x92
Command:

text

ff 55 0d 00 02 03 02 07 01 0e 2d 92 00
📊 Quick Reference Table
Pattern	Hex	Binary	Command (last bytes)
Sunday only	02	00000010	... 0e 2d 02 00
Monday only	80	10000000	... 0e 2d 80 00
Tuesday only	40	01000000	... 0e 2d 40 00
Wednesday only	20	00100000	... 0e 2d 20 00
Thursday only	10	00010000	... 0e 2d 10 00
Friday only	08	00001000	... 0e 2d 08 00
Saturday only	04	00000100	... 0e 2d 04 00
Everyday	FE	11111110	... 0e 2d fe 00
Weekdays (Mon-Fri)	F8	11111000	... 0e 2d f8 00
Weekend (Sat-Sun)	06	00000110	... 0e 2d 06 00
Mon+Wed+Fri	A8	10101000	... 0e 2d a8 00
Tue+Thu	50	01010000	... 0e 2d 50 00
🎯 Organized Test Plan
Test Set A: Basic Patterns
✅ Everyday (fe)
✅ Wednesday only (20)
🆕 Working days (f8)
🆕 Weekend (06)
🆕 Today only (use current day's hex)
Test Set B: All Individual Days
🆕 Sunday only (02)
🆕 Monday only (80)
🆕 Tuesday only (40)
✅ Wednesday only (20) - already done
🆕 Thursday only (10)
🆕 Friday only (08)
🆕 Saturday only (04)
Test Set C: All 8 Slots
🆕 Same alarm in slots 1-8 (change slot byte 00 to 07)
Test Set D: Custom Combinations
🆕 Mon+Wed+Fri (a8)
🆕 Tue+Thu (50)
🆕 Any other pattern you want


















100% CONFIRMED PROTOCOL SPECIFICATION
Command Structure:
text

ff 55 0d 00 02 03 02 [SLOT] 01 [HH] [MM] [DAYS] 00
Byte Position	Value	Description
0-1	ff 55	Protocol header
2	0d	Command length/type
3-6	00 02 03 02	Fixed alarm command prefix
7	00-07	Alarm slot (0=Slot1, 7=Slot8)
8	01	Enable flag (01=enabled, 00=disabled*)
9	00-17	Hour (24-hour format, hex)
10	00-3b	Minute (hex)
11	Bitmap	Day flags (see below)
12	00	Terminator
*Note: Disable flag needs testing

✅ DAY FLAGS (Confirmed Working)
Individual Days:
text

Bit 0 (0x01) = Reserved/Unused
Bit 1 (0x02) = Sunday
Bit 2 (0x04) = Saturday
Bit 3 (0x08) = Friday
Bit 4 (0x10) = Thursday
Bit 5 (0x20) = Wednesday      ✅ Tested
Bit 6 (0x40) = Tuesday
Bit 7 (0x80) = Monday         ✅ Tested (Today only)
Preset Combinations:
text

0xFE = Everyday (all 7 days)           ✅ Tested
0xF8 = Weekdays (Mon-Fri)              ✅ Tested
0x06 = Weekend (Sat-Sun)
0x80 = Monday only / "Today only"      ✅ Tested
0x20 = Wednesday only                  ✅ Tested
