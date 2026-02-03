# import asyncio
# from bleak import BleakClient

# DEVICE_ID = "0443CC0C-A400-4513-8C20-A2E21B412D01"
# WRITE_UUID = "0000ff01-0000-1000-8000-00805f9b34fb"
# NOTIFY_UUID = "0000ff02-0000-1000-8000-00805f9b34fb"

# # 3:10 PM = 15:10
# # Hour: 0F
# # Min:  0A

# # Variation 1: Command 08 (Standard Alarm)
# # Structure: Header + Len + Cmd(08) + Hour(0F) + Min(0A) + ID(01) + Footer
# CMD_08 = bytearray([0xFF, 0x55, 0x0A, 0x00, 0x08, 0x0F, 0x0A, 0x01, 0x00, 0x0D, 0x0A])

# # Variation 2: Command 04 (Time Set)
# CMD_04 = bytearray([0xFF, 0x55, 0x0A, 0x00, 0x04, 0x0F, 0x0A, 0x01, 0x00, 0x0D, 0x0A])

# # Variation 3: The "Split" Packet (Older method, just in case)
# CMD_FE = bytearray([0xFE, 0x00, 0x06, 0x01, 0x0F, 0x0A]) # 15:10

# def callback(sender, data):
#     print(f">>> BOTTLE REPLY: {data.hex().upper()}")

# async def set_alarm_310(address):
#     print(f"Connecting to {address}...")
#     async with BleakClient(address) as client:
#         print("Connected!")
#         await client.start_notify(NOTIFY_UUID, callback)
        
#         # 1. Handshake
#         print("Sending Handshake...")
#         await client.write_gatt_char(WRITE_UUID, bytearray([0xFF, 0x55, 0x07, 0x00, 0x01, 0x02, 0x00]), response=True)
#         await asyncio.sleep(1)

#         # 2. Try Command 08 (Most Likely)
#         print(f"Trying Command 08 (Hex: {CMD_08.hex()})...")
#         await client.write_gatt_char(WRITE_UUID, CMD_08, response=True)
#         await asyncio.sleep(3)

#         # 3. Try Command 04
#         print(f"Trying Command 04 (Hex: {CMD_04.hex()})...")
#         await client.write_gatt_char(WRITE_UUID, CMD_04, response=True)
#         await asyncio.sleep(3)
        
#         # 4. Try Command FE (Backup)
#         print(f"Trying Command FE (Hex: {CMD_FE.hex()})...")
#         await client.write_gatt_char(WRITE_UUID, CMD_FE, response=True)
        
#         print("Done. Check for 3:10 PM.")

# if __name__ == "__main__":
#     asyncio.run(set_alarm_310(DEVICE_ID))



import asyncio
from bleak import BleakClient

DEVICE_ID = "0443CC0C-A400-4513-8C20-A2E21B412D01"
WRITE_UUID = "0000ff01-0000-1000-8000-00805f9b34fb"
NOTIFY_UUID = "0000ff02-0000-1000-8000-00805f9b34fb"

# We want to set 6:15 PM (18:15)
# Hour: 12 (Hex)
# Min:  0F (Hex)
HEX_HOUR = 0x12
HEX_MIN  = 0x0F

def callback(sender, data):
    print(f">>> BOTTLE REPLIED: {data.hex().upper()}")

async def fuzz_commands(address):
    print(f"Connecting to {address}...")
    async with BleakClient(address) as client:
        print("Connected! Starting Lockpicker...")
        await client.start_notify(NOTIFY_UUID, callback)
        
        # 1. Handshake first
        await client.write_gatt_char(WRITE_UUID, bytearray([0xFF, 0x55, 0x07, 0x00, 0x01, 0x02, 0x00]), response=True)
        await asyncio.sleep(1)

        # 2. Try Command IDs from 1 to 20
        for cmd_id in range(1, 21):
            print(f"--- Trying Command ID: {cmd_id:02X} ---")
            
            # Construct Packet: 
            # Header(FF 55) + Len(0A 00) + CMD(ID) + Hour + Min + ID(01) + Flags(7F) + Footer(0D 0A)
            packet = bytearray([
                0xFF, 0x55, 
                0x0A, 0x00, 
                cmd_id,         # CHANGING THIS EVERY TIME
                HEX_HOUR,       # 18
                HEX_MIN,        # 15
                0x01,           # Alarm ID
                0x7F,           # Flags
                0x0D, 0x0A      # Footer
            ])
            
            # Send it
            try:
                await client.write_gatt_char(WRITE_UUID, packet, response=True)
            except:
                pass # Ignore write errors, just keep trying
            
            # Wait 1.5 seconds to see if bottle reacts
            await asyncio.sleep(1.5)

        print("Fuzzing complete. Did the bottle react to any number?")

if __name__ == "__main__":
    asyncio.run(fuzz_commands(DEVICE_ID))