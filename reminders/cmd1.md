What We Know For Sure:
✅ Complete Command Structure:
text

ff 55 0d 00 02 03 02 [SLOT] [EN] [HH] [MM] [DAYS] 00
SLOT: 00-07 (slots 1-8)
EN: 01 = enabled, 00 = disabled (needs testing)
HH: Hour (24-hour format, hex)
MM: Minute (hex)
DAYS: Day-of-week bitmap (needs final confirmation)
Terminator: 00
✅ Confirmed Day Flags:
0x02 = Sunday only
0x20 = Wednesday only
0x2a = Sun + Wed + Fri (or Thu?)
0xfe = Everyday
0x80 = Today only (one-time)
0x7c = Tue-Sat

📊 Day Flag Quick Reference:
DAY_SUNDAY    = 0x02
DAY_SATURDAY  = 0x04
DAY_FRIDAY    = 0x08
DAY_THURSDAY  = 0x10
DAY_WEDNESDAY = 0x20
DAY_TUESDAY   = 0x40
DAY_MONDAY    = 0x80

DAY_EVERYDAY  = 0xFE  # All days
DAY_WEEKDAYS  = 0xF8  # Mon-Fri (0x80|0x40|0x20|0x10|0x08 = 0xF8)
DAY_WEEKEND   = 0x06  # Sat-Sun (0x04|0x02)
DAY_ONCE      = 0x80  # One-time (if bit 7 is special)

Wait, let me recalculate weekdays:
Mon(80) + Tue(40) + Wed(20) + Thu(10) + Fri(08) = 0xF8

But earlier you had 0x7c for workdays... let me check:

0x7c = Tue-Sat you said, which would be:
Tue(40) + Wed(20) + Thu(10) + Fri(08) + Sat(04) = 0x7C ✓

So Mon-Fri would be:
Mon(80) + Tue(40) + Wed(20) + Thu(10) + Fri(08) = 0xF8

