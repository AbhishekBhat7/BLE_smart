Sent ff550700010900
rcvd ff5509000302000d0a

Sent ff550700010b00
RCVD ff550b0001000d0a

ff550700010100
ff550100011a0d0a

ff550700010200
ff55020001020d0a
ff550100011a0d0a

ff550d00020469846a18000226
ff550004000d0a

ff550600011e
ff551e0001000d0a

ff550600011c
ff551c0001000d0a

ff550600011d
ff551d0001010d0a

ff550800020e0739
ff55000e000d0a

ff550700010c00
ff550c0001000d0a

ff550700010d00
ff550d00060000000d0a

ff550700021000
ff550010000d0a

ff55080002120557
ff550012000d0a


hey i am doing reverse engineering to find out the packets were used in so i got the bug report and used that in the wireshark to get the above value so these packets are captured when i am going to connect the device so here the official app do data syncing and finding the battery , level of the waters and temp of it so find the exact data from them 



1. ff550700010100
ff 55 01 00 01 18 0D 0A
2. ff550700010d00 this requ
respo : ff 55 0d 00 06 00 00 00 0d 0a,  ff 55 00 10 00 0d 0a, ff 55 00 12 00 0d 0a
3. ff550700010200 this requ
respo: ff 55 02 00 01 02 0d 0a
4. ff550700010c00 this requ
respo: ff 55 0c 00 01  00 0d 0a,ff 55 0d 00 06 00 00 00 0d 0a, ff 55 00 10 00 0d 0a, ff 55 00 12 00 0d 0a
5. ff550600011c
respo : ff 55 1c 00 01 00 0d 0a
6. ff550600011d 
respo: ff 55 1d 00 01 06 0d 0a
7. ff550600011e
respo:  ff 55 1e 00 01 00 0d 0a