# import asyncio
# from bleak import BleakClient, BleakScanner

# # --- CONFIGURATION ---
# DEVICE_NAME_FILTER = "SGUAI-T30"

# # WRITE to this UUID (to send commands)
# WRITE_UUID = "0000ff01-0000-1000-8000-00805f9b34fb"

# # LISTEN to this UUID (to see the bottle's response)
# NOTIFY_UUID = "0000ff02-0000-1000-8000-00805f9b34fb"

# def notification_handler(sender, data):
#     """Prints incoming data from the bottle"""
#     print(f"\n🔔 [RESPONSE] {data.hex().upper()}")
#     print("👉 Enter Hex Command: ", end="", flush=True)

# async def input_loop(client):
#     """Waits for user input to send commands"""
#     print("\n✅ READY TO SEND COMMANDS")
#     print("   Type a hex string (e.g., 'FF5500') and press Enter.")
#     print("   Type 'exit' to quit.")
#     print("-" * 50)
    
#     while True:
#         # Get input from user (non-blocking way is complex in simple scripts, 
#         # so we use a standard input wrapped in a thread executor if needed, 
#         # but for simple testing, standard input inside the loop works)
        
#         cmd_str = await asyncio.to_thread(input, "👉 Enter Hex Command: ")
        
#         if cmd_str.lower() in ["exit", "quit"]:
#             break
            
#         # Clean up the input (remove spaces, 0x, etc)
#         cmd_str = cmd_str.replace(" ", "").replace("0x", "")
        
#         try:
#             # Convert text to raw bytes
#             cmd_bytes = bytes.fromhex(cmd_str)
            
#             print(f"📤 SENDING: {cmd_bytes.hex().upper()} ...")
            
#             # WRITE THE COMMAND
#             await client.write_gatt_char(WRITE_UUID, cmd_bytes, response=True)
#             print("✅ Sent.")
            
#         except ValueError:
#             print("❌ Invalid Hex String. Try again.")
#         except Exception as e:
#             print(f"❌ Error sending: {e}")

# async def main():
#     print(f"🔍 Searching for '{DEVICE_NAME_FILTER}'...")
#     device = await BleakScanner.find_device_by_filter(
#         lambda d, ad: d.name and DEVICE_NAME_FILTER in d.name
#     )

#     if not device:
#         print("❌ Device not found.")
#         return

#     print(f"✅ Found {device.name}. Connecting...")

#     async with BleakClient(device) as client:
#         print("🔗 Connected!")
        
#         # Start listening so we can see if the bottle replies to our commands
#         await client.start_notify(NOTIFY_UUID, notification_handler)
        
#         # Start the input loop
#         await input_loop(client)
        
#         # Cleanup
#         await client.stop_notify(NOTIFY_UUID)
#         print("🛑 Disconnected.")

# if __name__ == "__main__":
#     asyncio.run(main())


import asyncio
from bleak import BleakClient, BleakScanner

# --- CONFIGURATION ---
DEVICE_NAME_FILTER = "SGUAI-T30"

# UUIDs
WRITE_UUID = "0000ff01-0000-1000-8000-00805f9b34fb"
NOTIFY_UUID = "0000ff02-0000-1000-8000-00805f9b34fb"

# --- COMMAND SEQUENCE ---
# Based on your NRF logs, the app sends these in order:
CMD_1_VERSION = bytes.fromhex("FF550900000D0A")  # "Hello / Who are you?"
CMD_2_CONFIG  = bytes.fromhex("FF550200000D0A")  # "What represent your settings?"
CMD_3_BATTERY = bytes.fromhex("FF552800000D0A")  # "What is your battery?"

def callback_handler(sender, data):
    hex_str = "-".join("{:02X}".format(x) for x in data)
    
    # Check for Battery Packet (Command 0x28)
    if len(data) > 3 and data[2] == 0x28:
        print(f"\n🔔 [RESPONSE RECEIVED] (0x) {hex_str}")
        
        # Parse based on your log: FF-55-28-00-06-01-00-00-01-67-0D-0A
        # Index 9 is Battery
        batt_raw = data[9]
        is_charging = (data[8] == 1)
        
        print(f"   ✅ SUCCESS! Battery Found.")
        print(f"   🔋 Level: {batt_raw}%")
        print(f"   ⚡ Charging: {'YES' if is_charging else 'NO'}")
        print("   (Note: If charging, value might be > 100)")
        
    elif data[2] == 0x09:
        print(f"   ℹ️  Firmware Version Received")
    elif data[2] == 0x02:
        print(f"   ℹ️  Config Received")
    else:
        print(f"   📩 Other Data: {hex_str}")

async def main():
    print(f"🔍 Searching for '{DEVICE_NAME_FILTER}'...")
    device = await BleakScanner.find_device_by_filter(
        lambda d, ad: d.name and DEVICE_NAME_FILTER in d.name
    )

    if not device:
        print("❌ Device not found.")
        return

    print(f"✅ Found {device.name}. Connecting...")

    async with BleakClient(device) as client:
        print("🔗 Connected!")
        
        # 1. SUBSCRIBE
        await client.start_notify(NOTIFY_UUID, callback_handler)
        await asyncio.sleep(1) 

        # 2. EXECUTE SEQUENCE (Mimic the official App)
        
        print(f"\n1️⃣  Sending Handshake (Version 0x09)...")
        # We use response=False (Write Command) because FF01 is 'write-without-response'
        await client.write_gatt_char(WRITE_UUID, CMD_1_VERSION, response=False)
        await asyncio.sleep(0.5) # Small delay is crucial

        print(f"2️⃣  Sending Config Request (0x02)...")
        await client.write_gatt_char(WRITE_UUID, CMD_2_CONFIG, response=False)
        await asyncio.sleep(0.5)

        print(f"3️⃣  Sending BATTERY Request (0x28)...")
        await client.write_gatt_char(WRITE_UUID, CMD_3_BATTERY, response=False)
        
        # 3. WAIT FOR RESULTS
        print("⏳ Waiting 5 seconds for replies...")
        await asyncio.sleep(5)
        
        print("\n🛑 Disconnecting...")
        await client.stop_notify(NOTIFY_UUID)

if __name__ == "__main__":
    asyncio.run(main())