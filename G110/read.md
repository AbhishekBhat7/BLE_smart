1) for this the reminder commands will be same as t-30 
2) for the manual sterilization cmd will be ff 55 07 00 02 1c 01
3) for the automated sterilization cmd will be ff550700021d 01(02,03,04,05)
4) this is the temp values  ff550700010100
    ff 55 01 00 01 18 0D 0A --> here 18 => 0x18 = decimal(24C)

5) we are sending the date and time to the smart device as :    ff550d00020469847a8a000226
 Hex Bytes: 69 84 7a 8a
Decimal Value: 1,770,310,282
here that is in the unix timestamp 
Converted Time: Thu Feb 05 2026 16:51:22 UTC