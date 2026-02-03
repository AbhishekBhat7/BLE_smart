# import asyncio
# from bleak import BleakClient, BleakScanner

# # REPLACE THIS WITH YOUR BAND'S MAC ADDRESS
# # You can find this in nRF Connect (e.g., AA:BB:CC:11:22:33)
# DEVICE_MAC_ADDRESS = "64:62:27:00:4F:AE"

# # THIS IS THE UUID YOU WRITE TO
# # You need to find the "Write" Characteristic UUID in nRF Connect
# # It usually looks like 0000xxxx-0000-1000-8000-00805f9b34fb
# WRITE_CHARACTERISTIC_UUID = "0000ff01-0451-4000-b000-00805f9b34fb" # Example UUID

# def create_alarm_packet(hour, minute):
#     """
#     Creates the Hex string to set the alarm time.
#     Structure: Header(FE) + Len(06) + Cmd(01) + Hour + Minute
#     """
#     # 1. Start Header
#     packet = bytearray([0xFE, 0x00, 0x06, 0x01])
    
#     # 2. Add Time (Convert decimal to hex byte)
#     packet.append(hour)   # e.g., 17 for 5pm
#     packet.append(minute) # e.g., 35 for 35min
    
#     return packet

# async def set_time(address):
#     print(f"Searching for device {address}...")
#     device = await BleakScanner.find_device_by_address(address)
    
#     if not device:
#         print("Device not found. Make sure it is close and Bluetooth is ON.")
#         return

#     async with BleakClient(device) as client:
#         print("Connected!")
        
#         # --- SETTING ALARM FOR 8:45 PM ---
#         target_hour = 20  # 8 PM (24-hour format)
#         target_min = 45   # 45 Minutes
        
#         # Generate the packet
#         data_to_send = create_alarm_packet(target_hour, target_min)
        
#         print(f"Sending Hex: {data_to_send.hex()}")
        
#         # Send to device
#         await client.write_gatt_char(WRITE_CHARACTERISTIC_UUID, data_to_send)
        
#         print("Command Sent! Check your band.")

# # Run the script
# if __name__ == "__main__":
#     asyncio.run(set_time(DEVICE_MAC_ADDRESS))



import asyncio
from bleak import BleakScanner

async def scan_devices():
    print("Scanning for devices... (Wait 5 seconds)")
    devices = await BleakScanner.discover()
    
    found = False
    for d in devices:
        # We look for devices with names
        if d.name and d.name != "Unknown":
            print(f"Name: {d.name}")
            print(f"ID (Use this on Mac): {d.address}")
            print("-" * 20)
            
            # If we see SGUAI-T30 (from your screenshot), point it out
            if "SGUAI" in d.name or "T30" in d.name:
                print("!!! FOUND IT - COPY THE ID ABOVE !!!")
                found = True

    if not found:
        print("Could not find the band. Is Bluetooth OFF on your phone?")

if __name__ == "__main__":
    asyncio.run(scan_devices())