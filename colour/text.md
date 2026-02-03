ff 55 00 28 00 0D 0A got this after sliding

hey i am going to reverse engineer the ble devices using the wireshark so i sniffed and created the bug reports and sent to the wireshark and i got some packets and i found the colur settings means in the official app i can able to set the colour to blink so i am using the SGUAI app to connect the smart device so when i clicked on the colourful lights there i can see the option phantom lighting and reminder light here i didnt got the command for the reminder light but for the circular pattern which contains rgb colours so i tried there with so many patterns of colours and like red, yellow,pink and red and i found the packets so can u predict the all the colours used here 

hex value
ff550b0002280100c300c3 blue
ff550b00022801004c004c yellow
ff550b00022801014f014f pink 
ff550b0002280100040004  red



ff 55 00 28 00 0D 0A here if we get 28 that is from the gradient 
if 27 then auto stand by
if 2A then intervals 
if 2b means reminder 


ff550800022b0000.   for red reminder
ff550800022b00e6    for blue reminder





3) Phantom page reminder
ff550b00022801000e00d7      :-> phantom page slider
ff550700022701.  :-> auto stand by 10s  ( here last data can go upto 3) (00, 01, 02, 03)
ff550700022a01.  :-> Gradient mode (00,01,02)


822 to 888 here the value is for data syncing