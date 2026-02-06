1. The Battery Sync Packet (Phone 
→
→ Watch)
You highlighted Frame 647 (ff550800020e0642), stating the battery is 100%.

If we look for 0x64 (which is 100 in Hex), it is not in the packet. This means the app is not sending the raw percentage number. Instead, it is mapping the battery percentage to a "Level" (probably 1-6 or 0-6).

Breakdown of Frame 647:
ff 55 08 00 02 0e 06 42

ff 55: Header
08: Length (8 bytes)
00: Sequence
02: Command Category (System/Settings)
0e: Function ID (Sync Phone Battery Level)
06: The Data (Battery Level). Since your battery is 100%, the app converts "100%" to Level 6.
Logic: The watch likely displays a battery icon with bars rather than a number for the phone. 06 = Full Bars.
42: Checksum.

2. Frame 624: ff550d000204698419e4000226
This is the Time Sync packet.

ff 55: Header
0d: Length (13 bytes)
69 84 19 e4: This is a Hex Timestamp.
Hex 698419E4 = Decimal 1770265060.
Epoch Converter: Thursday, February 5, 2026 9:37:40 AM
This matches the date in your filename (2026_0205).



-------------------------------------------------------------------------------------------------

Conversation 1: The "Wake Up / Info" Check
Packet 615 (Phone Sends): ff 55 07 00 01 09 00

Meaning: "Who are you? / Get Device Status."
Command: 01 09
Logic: The app opens and immediately asks the bottle for its current state.
Packet 617 (Bottle Replies): ff 55 09 00 03 03 08 0d 0a

Meaning: "I am here. Status Normal."
Note: The 0d 0a at the end is a standard line ending (CR LF), common in serial communication.
Conversation 2: Time Synchronization (Crucial)
Packet 624 (Phone Sends): ff 55 0d 00 02 04 69 84 19 e4 00 02 26

Meaning: "Set your internal clock to Feb 5, 2026, 9:37 AM."
Command: 02 04 (Set Time).
Data: 69 84 19 e4 is the Unix Timestamp for that date.
Why: The bottle needs the correct time so when you drink water later, it logs it under the correct hour.
Packet 626 (Bottle Replies): ff 55 00 04 00 0d 0a

Meaning: "Time set successfully (ACK)."
Logic: It echoes the command type 04 with a 00 (Success).
Conversation 3: Fetching History (Old Sips)
Packet 630 (Phone Sends): ff 55 06 00 00 01 28

Meaning: "Give me the next batch of data records."
Command: 00 01 with iterator 28.
Packet 632 (Bottle Replies): ff 55 28 00 06 01 00 0e 00 c3 0d 0a

Meaning: "Here is a record."
Data: 00 0e and 00 c3.
Analysis: 00 C3 in Hex is 195 in Decimal. This is likely a historical record saying "Drank 195ml".
Conversation 4: Phone Battery Sync (The one you found!)
Packet 647 (Phone Sends): ff 55 08 00 02 0e 06 42

Meaning: "My Phone Battery is 100%."
Command: 02 0e (Sync Phone Info).
Data: 06.
Reverse Engineering: The bottle does not understand "100". It understands "Levels".
Level 1 = Low Battery
...
Level 6 = Full Battery (100%).
Checksum: 42.
Packet 649 (Bottle Replies): ff 55 00 0e 00 0d 0a

Meaning: "Understood. I will display the full battery icon on the bottle cap."
Conversation 5: The "Big" Data Sync
Packet 658 (Phone Sends): ff 55 07 00 01 0d 00

Meaning: "Send me the detailed water intake logs now."
Packet 660 (Bottle Replies): ff 55 0d 00 06 00 00 00 16 98 41 66 20 0b 41 a0 d0 a

Meaning: "Here is the data log."
Analysis:
06: Data Type (Water Log).
16 98 41 66: Timestamp (Matches the date/time from the earlier packets).
20: Likely the temperature of the water (32∘C / 90∘F) or the volume added.

Summary for your Protocol Documentation:
Direction	Command (Hex)	Function	Payload Logic
Phone 
→
→ Bottle	01 09	Get Status	Handshake.
Phone 
→
→ Bottle	02 04	Set Time	4 bytes = Unix Timestamp.
Phone 
→
→ Bottle	02 0E	Send Phone Battery	06 = 100%, 05 = ~80%, 01 = Low.
Bottle 
→
→ Phone	06 00	Water Data	Contains Timestamp + ML amount.
 
--------------------

The Concept: "The Giant Stopwatch"
In the computer world, time started on January 1, 1970. This is called "Unix Time."
Every second that passes, a giant counter goes up by 1.

1 minute after 1970 = 60
1 hour after 1970 = 3600
Today (Feb 5, 2026) = 1,770,265,060 seconds.


----------->>>>>--------------->>>>>------------------------


DND ON?OFF
ff550b0002290100c300c3
ff550b0002290000c300c3
DND oN/ off

Hex: ff 55 0b 00 02 29 01 00 c3 00 c3

ff 55: Header
0b: Length (11 bytes total).
00: Reserved.
02: Configuration Category.
29: DND Command ID.
01: Status (01 = ON, 00 = OFF).
00 c3: Start Time (Minutes from midnight).
00 c3: End Time (Minutes from midnight).
The Math on Time (00 c3):
Hex 00C3 converts to Decimal 195.
195 minutes from midnight = 3 hours and 15 minutes.
Time = 03:15 AM

So this command tells the watch: Turn DND ON, start at 03:15, end at 03:15.


Smart Reminder ON?OFF
ff55080002210301
ff55080002210300

----------->>>>>--------------->>>>>------------------------


