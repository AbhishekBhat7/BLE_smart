# import asyncio
# from bleak import BleakClient

# # The ID you just found
# DEVICE_ID = "0443CC0C-A400-4513-8C20-A2E21B412D01"

# # The Handshake Code from your Wireshark screenshot
# # (FF 55 07 00 01 02 00)
# HANDSHAKE_PACKET = bytearray([0xFF, 0x55, 0x07, 0x00, 0x01, 0x02, 0x00])

# async def hack_device(address):
#     print(f"Connecting to SGUAI-T30 ({address})...")
    
#     async with BleakClient(address) as client:
#         print("Connected successfully!")
#         print("-" * 30)
        
#         # 1. Search for the WRITE Characteristic
#         target_uuid = None
        
#         for service in client.services:
#             for char in service.characteristics:
#                 # We are looking for a characteristic that allows "write" or "write-without-response"
#                 if "write" in char.properties or "write-without-response" in char.properties:
#                     print(f"[FOUND] Writable UUID: {char.uuid}")
#                     print(f"        Properties: {char.properties}")
#                     target_uuid = char.uuid
                    
#                     # Usually, there is only one main write UUID. 
#                     # If we find it, we stop looking and try to use it.
#                     break
#             if target_uuid:
#                 break
        
#         # 2. Send the Command
#         if target_uuid:
#             print("-" * 30)
#             print(f"Attempting to send Handshake to: {target_uuid}")
            
#             try:
#                 # Send the packet
#                 await client.write_gatt_char(target_uuid, HANDSHAKE_PACKET, response=True)
#                 print(">>> PACKET SENT SUCCESSFULLY! <<<")
#                 print("Check your band. Did it vibrate or show a connection icon?")
#             except Exception as e:
#                 print(f"Error sending: {e}")
#                 print("Trying without response...")
#                 # Some bands don't send a confirmation back
#                 await client.write_gatt_char(target_uuid, HANDSHAKE_PACKET, response=False)
#                 print(">>> PACKET SENT (No Response Mode) <<<")
                
#         else:
#             print("Could not find a writable characteristic on this device.")

# if __name__ == "__main__":
#     asyncio.run(hack_device(DEVICE_ID))


# import asyncio
# from bleak import BleakClient

# DEVICE_ID = "0443CC0C-A400-4513-8C20-A2E21B412D01"

# # The Handshake (Phone -> Device)
# HANDSHAKE = bytearray([0xFF, 0x55, 0x07, 0x00, 0x01, 0x02, 0x00])

# def notification_handler(sender, data):
#     """This function runs when the bottle talks back to us"""
#     print(f"received response: {data.hex().upper()}")

# async def listen_to_bottle(address):
#     print(f"Connecting to {address}...")
    
#     async with BleakClient(address) as client:
#         print("Connected!")
        
#         # 1. Find the NOTIFY Characteristic (To hear the bottle)
#         notify_uuid = None
#         write_uuid = None
        
#         for service in client.services:
#             for char in service.characteristics:
#                 if "notify" in char.properties:
#                     notify_uuid = char.uuid
#                 if "write" in char.properties or "write-without-response" in char.properties:
#                     write_uuid = char.uuid
        
#         if notify_uuid:
#             print(f"Subscribing to notifications on: {notify_uuid}")
#             await client.start_notify(notify_uuid, notification_handler)
#         else:
#             print("Could not find a Notify channel. We might not hear replies.")

#         # 2. Send Handshake
#         if write_uuid:
#             print(f"Sending Handshake to: {write_uuid}")
#             await client.write_gatt_char(write_uuid, HANDSHAKE, response=True)
#             print("Handshake sent. Waiting 10 seconds for a reply...")
        
#         # 3. Wait and Listen
#         await asyncio.sleep(10)
        
#         print("Done listening.")

# if __name__ == "__main__":
#     asyncio.run(listen_to_bottle(DEVICE_ID))


import asyncio
from bleak import BleakClient

DEVICE_ID = "0443CC0C-A400-4513-8C20-A2E21B412D01"

async def map_handles(address):
    print(f"Connecting to {address}...")
    async with BleakClient(address) as client:
        print("Connected! Mapping Handles to UUIDs...")
        print("-" * 50)
        print(f"{'HANDLE':<10} | {'UUID'}")
        print("-" * 50)
        
        for service in client.services:
            for char in service.characteristics:
                # Print the Handle and the UUID
                print(f"{char.handle:<10} | {char.uuid}")
                
        print("-" * 50)
        print("Look for Handle '29' (which is 0x1d in hex)")

if __name__ == "__main__":
    asyncio.run(map_handles(DEVICE_ID))