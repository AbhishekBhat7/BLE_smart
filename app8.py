# import asyncio
# from bleak import BleakClient, BleakScanner

# # --- 1. THE COMMANDS WE REVERSED ---
# # The exact hex strings from your Wireshark analysis

# # Frame 2296: LOGIN / AUTH (The "Key" to unlock the device)
# PACKET_LOGIN = bytes.fromhex("ff550d0002046971bde0000226")

# # Frame 2299: HEARTBEAT (Keep-alive)
# PACKET_HEARTBEAT = bytes.fromhex("ff5506000127")

# # Frame 2331: CONTROL COMMAND (Mode 2, Intensity 16)
# # You can change the '10' (16) to other values to test speed
# PACKET_CONTROL = bytes.fromhex("ff550700021000")

# # Packet to Turn OFF (Optional test)
# PACKET_OFF = bytes.fromhex("ff5506000027") 


# def notification_handler(sender, data):
#     """Callback to print whatever the device sends back."""
#     print(f"   🔔 RECEIVED RESPONSE: {data.hex()}")


# async def run_control_sequence():
#     print("🔍 Scanning for SGUAI / T30 devices...")
    
#     # 1. SCAN AND FIND DEVICE
#     target_device = None
#     devices = await BleakScanner.discover(timeout=5.0)
    
#     for device in devices:
#         name = device.name or "Unknown"
#         if "SGUAI" in name.upper() or "T30" in name.upper():
#             target_device = device
#             print(f"   ⭐ FOUND TARGET: {name} ({device.address})")
#             break
            
#     if not target_device:
#         print("❌ No device found. Make sure it is ON and not connected to your phone app.")
#         return

#     # 2. CONNECT
#     print(f"\n🔗 Connecting to {target_device.address}...")
#     async with BleakClient(target_device.address) as client:
#         print("   ✅ Connected!")

#         # 3. AUTO-DETECT THE WRITE CHARACTERISTIC
#         # We need the UUID that supports "write-without-response" (0x52)
#         write_uuid = None
#         notify_uuid = None

#         for service in client.services:
#             for char in service.characteristics:
#                 props = char.properties
                
#                 # We prioritize characteristics that allow "write-without-response"
#                 if "write-without-response" in props:
#                     write_uuid = char.uuid
#                 elif "write" in props and not write_uuid:
#                     write_uuid = char.uuid
                
#                 if "notify" in props:
#                     notify_uuid = char.uuid

#         if not write_uuid:
#             print("❌ Could not find a Write Characteristic!")
#             return
        
#         # If we didn't find a distinct notify UUID, use the write one (often they are the same)
#         if not notify_uuid:
#             notify_uuid = write_uuid

#         print(f"   🎯 Target UUID: {write_uuid}")

#         # 4. ENABLE NOTIFICATIONS (Crucial for the "Unlock")
#         try:
#             await client.start_notify(notify_uuid, notification_handler)
#             print("   ✅ Notifications Enabled (Listening for response...)")
#         except Exception as e:
#             print(f"   ⚠️ Warning: Could not enable notifications: {e}")

#         # 5. EXECUTE THE HACK SEQUENCE
#         print("\n🚀 STARTING COMMAND SEQUENCE...")

#         # STEP A: Send Login
#         print(f"   ➡️ Sending LOGIN Packet ({len(PACKET_LOGIN)} bytes)")
#         await client.write_gatt_char(write_uuid, PACKET_LOGIN, response=False)
#         await asyncio.sleep(0.2) # Wait for device to process

#         # STEP B: Send Heartbeat (The "Double Tap")
#         print(f"   ➡️ Sending HEARTBEAT")
#         await client.write_gatt_char(write_uuid, PACKET_HEARTBEAT, response=False)
#         # Very short delay implies the command follows immediately
#         await asyncio.sleep(0.1) 

#         # STEP C: Send Control Command
#         print(f"   ➡️ Sending CONTROL (Mode 2, Intensity 16)")
#         await client.write_gatt_char(write_uuid, PACKET_CONTROL, response=False)

#         print("\n✅ Sequence Sent! Watch the device.")
        
#         # Keep the script running for a few seconds to receive any "OK" response
#         await asyncio.sleep(4)
#         print("👋 Disconnecting.")

# if __name__ == "__main__":
#     asyncio.run(run_control_sequence())



# import asyncio
# from bleak import BleakClient, BleakScanner

# # --- YOUR CAPTURED DATA ---
# # Ensure these match what you see in Wireshark TODAY
# LOGIN_PACKET = bytes.fromhex("ff550d0002046971bde0000226")
# CONTROL_PACKET = bytes.fromhex("ff550700021000") # Mode 2, Intensity 16

# async def run_flood_attack():
#     print("🔍 Scanning for SGUAI...")
#     device = await BleakScanner.find_device_by_filter(
#         lambda d, ad: d.name and ("SGUAI" in d.name.upper() or "T30" in d.name.upper())
#     )

#     if not device:
#         print("❌ Device not found.")
#         return

#     print(f"🔗 Connecting to {device.address}...")
#     async with BleakClient(device.address) as client:
#         print("✅ Connected!")

#         # 1. Find the Write Characteristic
#         write_uuid = None
#         for s in client.services:
#             for c in s.characteristics:
#                 if "write-without-response" in c.properties:
#                     write_uuid = c.uuid
#                     break
        
#         if not write_uuid:
#             print("❌ No Write characteristic found.")
#             return
        
#         print(f"🎯 Writing to UUID: {write_uuid}")

#         # 2. Enable Notifications (Wakes up the comms channel)
#         # Note: We use the same UUID if no specific notify UUID exists
#         try:
#             await client.start_notify(write_uuid, lambda s, d: print(f"🔔 RX: {d.hex()}"))
#             print("✅ Notifications ON")
#         except:
#             print("⚠️ Could not enable notifications (ignoring)")

#         # 3. Send LOGIN
#         print("🔑 Sending Login...")
#         await client.write_gatt_char(write_uuid, LOGIN_PACKET, response=False)
#         await asyncio.sleep(0.2)

#         # 4. START HEARTBEAT FLOOD
#         # The device might need to see the counter increment to accept it is "live"
#         print("💓 Flooding Heartbeats (Waking up device)...")
        
#         # We start at counter 0x20 and go up.
#         # This mimics the app counting up: ...20, 21, 22...
#         start_counter = 0x20 
        
#         for i in range(10):
#             # Construct heartbeat: FF 55 06 00 01 [Counter]
#             # We assume checksum logic is simple, but for now we just increment the byte
#             current_counter = start_counter + i
#             packet = bytearray([0xFF, 0x55, 0x06, 0x00, 0x01, current_counter])
            
#             await client.write_gatt_char(write_uuid, packet, response=False)
#             await asyncio.sleep(0.05) # Send every 50ms (Very fast)

#         # 5. SEND COMMAND (Immediately after the flood)
#         print("🚀 Sending CONTROL Command!")
#         # Send it 3 times just to be sure
#         for _ in range(3):
#             await client.write_gatt_char(write_uuid, CONTROL_PACKET, response=False)
#             await asyncio.sleep(0.05)

#         print("✅ Done. Check device.")
#         await asyncio.sleep(2)

# if __name__ == "__main__":
#     asyncio.run(run_flood_attack())

import asyncio
from bleak import BleakClient

DEVICE_ID = "0443CC0C-A400-4513-8C20-A2E21B412D01"

# CHANGED: We are now writing to EF01 (Handle 41), not FF01
WRITE_UUID = "0000ef01-0000-1000-8000-00805f9b34fb"

# We might need to listen on EF02 (or standard notification channel)
# If this fails, we can try listening on ff02 still.
NOTIFY_UUID = "0000ff02-0000-1000-8000-00805f9b34fb" 

# Target: 4:55 PM
# Hour: 16 (0x10)
# Min:  55 (0x37)

# STRUCTURE FROM YOUR FIRST MESSAGE (FE Protocol)
# -----------------------------------------------
# Packet 1: Time
# FE 00 06 (Length) 01 (Cmd) 10 (Hour) 37 (Min)
PACKET_1 = bytearray([0xFE, 0x00, 0x06, 0x01, 0x10, 0x37])

# Packet 2: Settings (Days/Switches)
# FE 00 07 (Length) 00 (ID) 15 1E (Magic Numbers from your log) 00 (Pad)
PACKET_2 = bytearray([0xFE, 0x00, 0x07, 0x00, 0x15, 0x1E, 0x00])

# Packet 3: Footer
PACKET_3 = bytearray([0xFE, 0x00, 0x0D, 0x0A])

def callback(sender, data):
    print(f">>> BOTTLE REPLIED: {data.hex().upper()}")

async def set_alarm_ef01(address):
    print(f"Connecting to {address}...")
    async with BleakClient(address) as client:
        print("Connected!")
        
        # Listen for replies
        try:
            await client.start_notify(NOTIFY_UUID, callback)
        except:
            pass # EF01 might not have a notify partner, that's okay

        print(f"Sending FE Packets to UUID {WRITE_UUID}...")

        # 1. Send Time
        print(f"Packet 1: {PACKET_1.hex()}")
        await client.write_gatt_char(WRITE_UUID, PACKET_1, response=True)
        await asyncio.sleep(0.1)

        # 2. Send Settings
        print(f"Packet 2: {PACKET_2.hex()}")
        await client.write_gatt_char(WRITE_UUID, PACKET_2, response=True)
        await asyncio.sleep(0.1)

        # 3. Send Footer
        print(f"Packet 3: {PACKET_3.hex()}")
        await client.write_gatt_char(WRITE_UUID, PACKET_3, response=True)
        
        print(">>> SENT TO EF01. Check for 4:55 PM. <<<")
        await asyncio.sleep(2)

if __name__ == "__main__":
    asyncio.run(set_alarm_ef01(DEVICE_ID))