# import asyncio
# from bleak import BleakClient

# DEVICE_ID = "0443CC0C-A400-4513-8C20-A2E21B412D01"
# WRITE_UUID = "0000ff01-0000-1000-8000-00805f9b34fb"
# NOTIFY_UUID = "f000ffc2-0451-4000-b000-000000000000"

# def callback(sender, data):
#     # Print whatever the bottle says back
#     print(f"received: {data.hex().upper()}")

# async def get_status(address):
#     print(f"Connecting to {address}...")
#     async with BleakClient(address) as client:
#         print("Connected!")
#         await client.start_notify(NOTIFY_UUID, callback)
#         print("Listening...")
        
#         # 1. Send Handshake
#         handshake = bytearray([0xFF, 0x55, 0x07, 0x00, 0x01, 0x02, 0x00])
#         await client.write_gatt_char(WRITE_UUID, handshake, response=True)
#         await asyncio.sleep(1)

#         # 2. Try "Get Info" Commands
#         # These are common commands to ask "Who are you?" or "What is your battery?"
        
#         # Command A: Get Time/Status
#         cmd_a = bytearray([0xFF, 0x55, 0x06, 0x00, 0x03, 0x00])
#         print(f"Sending Query A: {cmd_a.hex()}")
#         await client.write_gatt_char(WRITE_UUID, cmd_a, response=True)
#         await asyncio.sleep(1)

#         # Command B: Get Battery
#         cmd_b = bytearray([0xFF, 0x55, 0x06, 0x00, 0x04, 0x00])
#         print(f"Sending Query B: {cmd_b.hex()}")
#         await client.write_gatt_char(WRITE_UUID, cmd_b, response=True)
#         await asyncio.sleep(1)

#         print("Waiting 5 seconds for replies...")
#         await asyncio.sleep(5)

# if __name__ == "__main__":
#     asyncio.run(get_status(DEVICE_ID))

import asyncio
from bleak import BleakClient

DEVICE_ID = "0443CC0C-A400-4513-8C20-A2E21B412D01"

# The standard pair for many devices:
WRITE_UUID = "0000ff01-0000-1000-8000-00805f9b34fb"
NOTIFY_UUID = "0000ff02-0000-1000-8000-00805f9b34fb" # Changed from ffc2

def callback(sender, data):
    print(f">>> BOTTLE REPLIED: {data.hex().upper()}")

async def listen_correctly(address):
    print(f"Connecting to {address}...")
    async with BleakClient(address) as client:
        print("Connected!")
        
        # 1. Listen on the correct channel
        try:
            await client.start_notify(NOTIFY_UUID, callback)
            print(f"Listening on {NOTIFY_UUID}...")
        except Exception as e:
            print(f"Failed to subscribe to ff02: {e}")
            return

        # 2. Send Handshake
        print("Sending Handshake (FF 55 07...)...")
        handshake = bytearray([0xFF, 0x55, 0x07, 0x00, 0x01, 0x02, 0x00])
        await client.write_gatt_char(WRITE_UUID, handshake, response=True)
        
        print("Waiting 10 seconds for a response...")
        await asyncio.sleep(10)

if __name__ == "__main__":
    asyncio.run(listen_correctly(DEVICE_ID))