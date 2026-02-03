hey i am working on the reverse engineering the ble using the wire shark so i created the bug reports from the mobile and went to see the packets on the wireshark so there i found the so many hex values so i tried to decode it and finally now i found that set alarm command at around 12:13 PM, 12:14 pm and 12:15pm i setted the alarm with first 2 are setted as everyday , and last one is setted as today itself and one more thing in the app i can see 3 options after setting the time i need to enter checkbox as everyday, it will show all the days from mon to sun then , working day it will show dates from mon to friday and then we our self set the time for the perticular day that by clicking on the perticular days


***********
hey i am working on the reverse engineering the ble using the wire shark so i created the bug reports from the mobile and went to see the packets on the wireshark so there i found the so many hex values so i tried to decode it and finally now i found that set alarm command at around 12:13 PM, 12:14 pm and 12:15pm i setted the alarm with first 2 are setted as everyday , and last one is setted as today itself and one more thing in the app i can see 3 options after setting the time i need to enter checkbox as everyday, it will show all the days from mon to sun then , working day it will show dates from mon to friday and then we our self set the time for the perticular day that by clicking on the perticular days

so these are the below shown the hex value i had got 
1) ff550d0002030207010c0cfe00
frequently recived ff550003000d0a

after that these 3 pairs are recieved together
ff550300060800000921fe0001000922fe000201
0b25fe0003010924fe0004010925fe0005010c23
fe0006010c24100007010c0cfe000d0a


2) ff550d0002030207010c0dfe00
frequent rcvd ff550003000d0a

3 pairs
ff550300060800000921fe0001000922fe000201
0b25fe0003010924fe0004010925fe0005010c23
fe0006010c24100007010c0dfe000d0a


3) ff550d0002030207010c0efe00
 frequent rcvd ff550003000d0a

3 pairs
ff550300060800000921fe0001000922fe000201
0b25fe0003010924fe0004010925fe0005010c23
fe0006010c24100007010c0dfe000d0a


4) ff550d0002030207010c0f8000
 frequent rcvd ff550003000d0a

3 pairs
ff550300060800000921fe0001000922fe000201
0b25fe0003010924fe0004010925fe0005010c23
fe0006010c24100007010c0dfe000d0a



here i checked on ur request so when i pass this request 
1) ff 55 0d 00 02 03 02 07 01 0e 2d fe 00 
in the official app i can see the time 2:45 PM setted on everyday

2) ff 55 0d 00 02 03 02 07 01 0f 1e 7c 00
in the official app we can see that we seted the time at 3:30PM customized as from tue to saturday 

3) ff 55 0d 00 02 03 02 07 01 06 00 fe 00
in the official app i can see the time 6:00 AM setted on everyday

4) ff 55 0d 00 02 03 02 07 01 17 3b 80 00
in the official app i can see the time 23:59 PM setted on today only(Monday)


but i saw one more things here in the official app we can see the 8 slots to update the timer but here i can see only the 8th timer is updating and one more thing u can note that in the 8 slots first 2 are now off and bottom 6 fields are in on state check this 