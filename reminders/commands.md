ff 55 0d 00 02 03 02 07 01 0e 2d fe 00
ff 55          → Header
0d             → Length/command type
00 02 03 02 07 01 → Fixed alarm command prefix
0e             → Hour = 14 (2 PM in 24h)
2d             → Minute = 45
fe             → Everyday flag
00             → Terminator

Bit 7 6 5 4 3 2 1 0
    | | | | | | | |
    | | | | | | | +-- Monday (or Sunday)
    | | | | | | +---- Tuesday (or Monday)
    | | | | | +------ Wednesday (or Tuesday)
    | | | | +-------- Thursday (or Wednesday)
    | | | +---------- Friday (or Thursday)
    | | +------------ Saturday (or Friday)
    | +-------------- Sunday (or Saturday)
    +---------------- Enable/Once flag?





✨ Full Protocol Decoded:

ff 55 0d 00 02 03 02 [SLOT] 01 [HH] [MM] [DAYS] 00
Where:

ff 55 = Header
0d 00 02 03 02 = Fixed alarm command prefix
[SLOT] = Alarm slot (0x00-0x07 for slots 1-8)
01 = Enable flag (probably 00 = disable)
[HH] = Hour (24-hour, hex)
[MM] = Minute (hex)
[DAYS] = Day-of-week flags
00 = Terminator


Bit 0 (0x01) = Sunday
Bit 1 (0x02) = Monday  
Bit 2 (0x04) = Tuesday
Bit 3 (0x08) = Wednesday
Bit 4 (0x10) = Thursday
Bit 5 (0x20) = Friday
Bit 6 (0x40) = Saturday
Bit 7 (0x80) = One-time/Today-only flag


for perticular slots
ff 55 0d 00 02 03 02 00 01 0e 2d fe 00
                      ^^
                      Slot 0 (first slot)

                      