#!/usr/bin/env python3
"""
SGUAI T30 - Service Discovery Script
This will find the REAL UUIDs used by your device
"""

import asyncio
from bleak import BleakClient, BleakScanner

DEVICE_NAME = "SGUAI"

async def discover_device():
    print("🔍 Scanning for SGUAI devices...\n")
    
    devices = await BleakScanner.discover(timeout=15.0)
    
    target_device = None
    
    print("="*60)
    print("ALL DEVICES FOUND:")
    print("="*60)
    
    for device in devices:
        name = device.name or "Unknown"
        print(f"  {name:30} | {device.address}")
        
        if "SGUAI" in name.upper() or "T30" in name.upper():
            target_device = device
            print(f"  ⭐ TARGET DEVICE FOUND!")
    
    if not target_device:
        print("\n❌ No SGUAI device found!")
        print("Make sure your bottle is:")
        print("  1. Powered on")
        print("  2. Not connected to another device")
        print("  3. In Bluetooth range")
        return
    
    print(f"\n\n🔗 Connecting to: {target_device.name} ({target_device.address})")
    
    async with BleakClient(target_device.address) as client:
        print("✅ Connected!\n")
        
        print("="*60)
        print("📦 COMPLETE SERVICE MAP")
        print("="*60)
        
        # Store found characteristics
        write_chars = []
        notify_chars = []
        read_chars = []
        
        for service in client.services:
            print(f"\n🔷 SERVICE: {service.uuid}")
            print(f"   Description: {service.description}")
            
            for char in service.characteristics:
                props = char.properties
                props_str = ", ".join(props)
                
                print(f"\n   📝 CHARACTERISTIC: {char.uuid}")
                print(f"      Handle: {char.handle}")
                print(f"      Properties: {props_str}")
                
                # Categorize characteristics
                if "write" in props or "write-without-response" in props:
                    write_chars.append({
                        "uuid": char.uuid,
                        "service": service.uuid,
                        "props": props_str
                    })
                    print(f"      ✏️  CAN WRITE")
                
                if "notify" in props or "indicate" in props:
                    notify_chars.append({
                        "uuid": char.uuid,
                        "service": service.uuid,
                        "props": props_str
                    })
                    print(f"      🔔 CAN NOTIFY")
                
                if "read" in props:
                    read_chars.append({
                        "uuid": char.uuid,
                        "service": service.uuid,
                        "props": props_str
                    })
                    print(f"      👁️  CAN READ")
                    
                    # Try to read current value
                    try:
                        value = await client.read_gatt_char(char.uuid)
                        hex_val = value.hex().upper()
                        print(f"      📖 Current Value: {hex_val}")
                        
                        # Try to decode as string
                        try:
                            text = value.decode('utf-8', errors='ignore')
                            if text.isprintable() and len(text) > 0:
                                print(f"      📖 As Text: {text}")
                        except:
                            pass
                    except Exception as e:
                        print(f"      ⚠️  Read Error: {e}")
                
                # List descriptors
                for desc in char.descriptors:
                    print(f"      📎 Descriptor: {desc.uuid}")
        
        # Summary
        print("\n")
        print("="*60)
        print("📋 SUMMARY - USE THESE IN YOUR SCRIPT")
        print("="*60)
        
        print("\n✏️  WRITE CHARACTERISTICS (for sending commands):")
        for char in write_chars:
            print(f"   UUID: {char['uuid']}")
            print(f"   Service: {char['service']}")
            print(f"   Properties: {char['props']}")
            print()
        
        print("\n🔔 NOTIFY CHARACTERISTICS (for receiving data):")
        for char in notify_chars:
            print(f"   UUID: {char['uuid']}")
            print(f"   Service: {char['service']}")
            print(f"   Properties: {char['props']}")
            print()
        
        print("\n👁️  READ CHARACTERISTICS:")
        for char in read_chars:
            print(f"   UUID: {char['uuid']}")
            print(f"   Service: {char['service']}")
            print(f"   Properties: {char['props']}")
            print()
        
        # Generate code snippet
        print("\n")
        print("="*60)
        print("📝 COPY THIS CONFIGURATION:")
        print("="*60)
        
        if write_chars:
            print(f'\nWRITE_CHAR_UUID = "{write_chars[0]["uuid"]}"')
        if notify_chars:
            print(f'NOTIFY_CHAR_UUID = "{notify_chars[0]["uuid"]}"')
        if write_chars:
            print(f'SERVICE_UUID = "{write_chars[0]["service"]}"')
        
        print("\n")
        print("="*60)

if __name__ == "__main__":
    asyncio.run(discover_device())



# import asyncio
# from bleak import BleakClient, BleakScanner

# # --- CONFIGURATION FROM YOUR SERVICE MAP ---
# DEVICE_NAME_FILTER = "SGUAI-T30"

# # Based on your map, these two support 'NOTIFY'
# # We listen to both to ensure we catch all data.
# NOTIFY_UUID_1 = "0000ff01-0000-1000-8000-00805f9b34fb"
# NOTIFY_UUID_2 = "0000ff02-0000-1000-8000-00805f9b34fb"

# def callback_handler(sender, data):
#     """
#     This runs every time the bottle sends data.
#     """
#     # Convert binary data to Hex string (e.g., b'\x01' -> "01")
#     hex_data = data.hex().upper()
    
#     # Identify which UUID sent it based on the handle (simplified for display)
#     if sender == 28: # Handle 28 is usually FF01
#         source = "FF01"
#     elif sender == 30: # Handle 30 is usually FF02
#         source = "FF02"
#     else:
#         source = f"Handle {sender}"

#     print(f"🔔 [{source}] RECEIVED: {hex_data}")

# async def main():
#     print(f"🔍 Scanning for device named containing '{DEVICE_NAME_FILTER}'...")
    
#     # 1. Scan for the specific device
#     device = await BleakScanner.find_device_by_filter(
#         lambda d, ad: d.name and DEVICE_NAME_FILTER in d.name
#     )

#     if not device:
#         print("❌ Device not found. Is it charged and nearby?")
#         return

#     print(f"✅ Found: {device.name} ({device.address})")
#     print("🔗 Connecting...")

#     async with BleakClient(device) as client:
#         print(f"✅ Connected: {client.is_connected}")

#         # 2. Subscribe to Notifications
#         # The bottle usually talks on FF01, but we check FF02 just in case.
        
#         try:
#             await client.start_notify(NOTIFY_UUID_1, callback_handler)
#             print(f"👂 Subscribed to {NOTIFY_UUID_1} (Control)")
#         except Exception as e:
#             print(f"⚠️ Failed to subscribe to FF01: {e}")

#         try:
#             await client.start_notify(NOTIFY_UUID_2, callback_handler)
#             print(f"👂 Subscribed to {NOTIFY_UUID_2} (Data)")
#         except Exception as e:
#             print(f"⚠️ Failed to subscribe to FF02: {e}")

#         print("\n" + "="*60)
#         print("🚀 LISTENING FOR DATA - PERFORM THESE ACTIONS NOW:")
#         print("   1. Open the lid / Cap")
#         print("   2. Drink some water (or simulate it)")
#         print("   3. Touch the screen (if it has one)")
#         print("   4. Put it on the charger")
#         print("="*60 + "\n")

#         # 3. Keep script running for 60 seconds to capture data
#         await asyncio.sleep(60)
        
#         # 4. Cleanup
#         try:
#             await client.stop_notify(NOTIFY_UUID_1)
#             await client.stop_notify(NOTIFY_UUID_2)
#         except:
#             pass
#         print("🛑 Disconnecting...")

# if __name__ == "__main__":
#     asyncio.run(main())


# import asyncio
# from bleak import BleakClient, BleakScanner

# # --- CONFIGURATION ---
# DEVICE_NAME_FILTER = "SGUAI-T30"
# NOTIFY_UUID = "0000ff02-0000-1000-8000-00805f9b34fb"

# def parse_sguai_packet(data):
#     """
#     Decodes the 13-byte packet from the SGUAI bottle.
#     Packet Format: FF 55 C0 00 06 00 [WATER] 00 [TEMP] 00 [BATT] 0D 0A
#     """
#     # 1. basic validation
#     if len(data) != 13:
#         return None
#     if data[0] != 0xFF or data[1] != 0x55:
#         return None

#     # 2. Extract values
#     # Byte 6: Water Level (Raw sensor value, 0-255)
#     water_raw = data[6]
    
#     # Byte 8: Temperature (Celsius)
#     temp_c = data[8]
    
#     # Byte 10: Battery (Percentage)
#     batt_pct = data[10]

#     return {
#         "water_raw": water_raw,
#         "temp_c": temp_c,
#         "battery": batt_pct
#     }

# def callback_handler(sender, data):
#     parsed = parse_sguai_packet(data)
    
#     if parsed:
#         print(f"💧 Water Sensor: {parsed['water_raw']:<3} | "
#               f"🌡️  Temp: {parsed['temp_c']}°C | "
#               f"🔋 Battery: {parsed['battery']}%")
#     else:
#         # Print raw if it doesn't match expected format
#         print(f"⚠️ RAW: {data.hex().upper()}")

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
        
#         # Subscribe to notifications
#         await client.start_notify(NOTIFY_UUID, callback_handler)
        
#         print("------------------------------------------------")
#         print("📊 LIVE DATA STREAM (Ctrl+C to stop)")
#         print("------------------------------------------------")

#         # Keep running until user stops it
#         try:
#             while True:
#                 await asyncio.sleep(1)
#         except asyncio.CancelledError:
#             pass
#         except KeyboardInterrupt:
#             pass
#         finally:
#             await client.stop_notify(NOTIFY_UUID)
#             print("\n🛑 Disconnected.")

# if __name__ == "__main__":
#     try:
#         asyncio.run(main())
#     except KeyboardInterrupt:
#         pass