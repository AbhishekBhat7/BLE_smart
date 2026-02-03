# # import asyncio
# # from bleak import BleakClient

# # DEVICE_ID = "0443CC0C-A400-4513-8C20-A2E21B412D01"
# # WRITE_UUID = "0000ff01-0000-1000-8000-00805f9b34fb"
# # NOTIFY_UUID = "0000ff02-0000-1000-8000-00805f9b34fb"

# # # Target: 2:45 PM (14:45)
# # HEX_HOUR = 0x0E
# # HEX_MIN  = 0x2D

# # def build_packet(cmd, hour, minute):
# #     # Content: CMD(1) + HOUR(1) + MIN(1) + ID(1) + FLAGS(1) + FOOTER(2)
# #     # Total Content = 7 bytes
# #     content = bytearray([cmd, hour, minute, 0x01, 0x7F, 0x0D, 0x0A])
    
# #     # Total Length: Header(2) + LengthBytes(2) + Content(7) = 11 Bytes (0B)
# #     total_len = 2 + 2 + len(content)
    
# #     packet = bytearray([0xFF, 0x55])       # Header
# #     packet.append(total_len)               # Length Low (will be 0B)
# #     packet.append(0x00)                    # Length High
# #     packet.extend(content)                 # Data
    
# #     return packet

# # async def set_alarm_final(address):
# #     print(f"Connecting to {address}...")
# #     async with BleakClient(address) as client:
# #         print("Connected!")
        
# #         # 1. Listen for confirmation
# #         await client.start_notify(NOTIFY_UUID, lambda s, d: print(f"Reply: {d.hex().upper()}"))
        
# #         # 2. Handshake (Standard)
# #         print("Sending Handshake...")
# #         await client.write_gatt_char(WRITE_UUID, bytearray([0xFF, 0x55, 0x07, 0x00, 0x01, 0x02, 0x00]), response=True)
# #         await asyncio.sleep(1)

# #         # 3. Send Alarm
# #         # Packet will look like: FF 55 0B 00 08 0E 2D 01 7F 0D 0A
# #         packet = build_packet(0x08, HEX_HOUR, HEX_MIN)
        
# #         print(f"Sending 2:45 PM Packet: {packet.hex().upper()}")
# #         await client.write_gatt_char(WRITE_UUID, packet, response=True)
        
# #         print(">>> SENT! Check bottle for 2:45 PM. <<<")
# #         await asyncio.sleep(3)

# # if __name__ == "__main__":
# #     asyncio.run(set_alarm_final(DEVICE_ID))

# #!/usr/bin/env python3
# """Find BLE-related code in decompiled APK"""

# import os
# import re

# # Patterns to search for
# patterns = [
#     r'[0-9a-fA-F]{4,8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}',  # UUIDs
#     r'fff[0-9a-fA-F]',  # Short UUIDs
#     r'writeBLE|readBLE|notifyBLE',
#     r'createBLEConnection',
#     r'getBLEDeviceServices',
#     r'getBLEDeviceCharacteristics',
#     r'onBLECharacteristicValueChange',
#     r'ArrayBuffer|Uint8Array',
#     r'0x[0-9a-fA-F]{2}',  # Hex bytes
#     r'characteristic',
#     r'service[Ii]d',
# ]

# def search_files(directory):
#     results = {}
    
#     for root, dirs, files in os.walk(directory):
#         for file in files:
#             if file.endswith('.js'):
#                 filepath = os.path.join(root, file)
#                 try:
#                     with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
#                         content = f.read()
                        
#                     matches = []
#                     for pattern in patterns:
#                         found = re.findall(pattern, content)
#                         if found:
#                             matches.extend(found[:5])  # Limit matches
                    
#                     if matches:
#                         results[filepath] = list(set(matches))
                        
#                 except Exception as e:
#                     pass
    
#     return results

# if __name__ == "__main__":
#     import sys
#     directory = sys.argv[1] if len(sys.argv) > 1 else "."
    
#     print("🔍 Searching for BLE-related code...\n")
#     results = search_files(directory)
    
#     for filepath, matches in sorted(results.items(), key=lambda x: -len(x[1])):
#         print(f"\n📄 {filepath}")
#         print(f"   Matches: {matches[:10]}")



#!/usr/bin/env python3
"""
SGUAI T30 Smart Water Bottle - BLE Communication
Install: pip install bleak
"""

import asyncio
from bleak import BleakClient, BleakScanner
from datetime import datetime
import struct

# ============================================
# SGUAI T30 CONFIGURATION
# ============================================

DEVICE_NAME = "SGUAI-T30"

# Common SGUAI UUIDs (may need adjustment)
# Try these first - update if different
SERVICE_UUID = "0000fff0-0000-1000-8000-00805f9b34fb"
WRITE_CHAR_UUID = "0000fff1-0000-1000-8000-00805f9b34fb"
NOTIFY_CHAR_UUID = "0000fff2-0000-1000-8000-00805f9b34fb"

# Alternative UUIDs to try
ALT_SERVICE_UUID = "0000fee7-0000-1000-8000-00805f9b34fb"
ALT_WRITE_UUID = "0000fee7-0000-1000-8000-00805f9b34fb"

# ============================================
# SGUAI COMMAND DEFINITIONS
# ============================================

class SGUAICommands:
    """SGUAI T30 Command Set"""
    
    # Known commands from your decompiled app
    GET_DEVICE_INFO = 0x02
    GET_BATTERY = 0x03
    GET_TEMPERATURE = 0x27
    GET_WATER_INTAKE = 0x28
    GET_HISTORY = 0x29
    SET_REMINDER = 0x2A
    SYNC_TIME = 0x2B
    
    # Common SGUAI packet structure
    HEADER = 0xAA  # or could be 0xFE, 0x5A, etc.
    
    @staticmethod
    def calculate_checksum(data: bytes) -> int:
        """Calculate checksum - XOR of all bytes"""
        checksum = 0
        for byte in data:
            checksum ^= byte
        return checksum
    
    @staticmethod
    def build_packet(command: int, payload: bytes = b'') -> bytes:
        """
        Build command packet
        Common formats:
        - [Header][Command][Length][Payload][Checksum]
        - [Header][Length][Command][Payload][Checksum]
        """
        # Format 1: Simple
        packet = bytes([SGUAICommands.HEADER, command, len(payload)]) + payload
        checksum = SGUAICommands.calculate_checksum(packet)
        return packet + bytes([checksum])
    
    @staticmethod
    def build_packet_v2(command: int, payload: bytes = b'') -> bytes:
        """Alternative packet format"""
        length = len(payload) + 2
        packet = bytes([0xFE, length, command]) + payload
        checksum = sum(packet) & 0xFF
        return packet + bytes([checksum])
    
    @classmethod
    def get_device_info(cls) -> bytes:
        return cls.build_packet(cls.GET_DEVICE_INFO)
    
    @classmethod
    def get_battery(cls) -> bytes:
        return cls.build_packet(cls.GET_BATTERY)
    
    @classmethod
    def get_temperature(cls) -> bytes:
        return cls.build_packet(cls.GET_TEMPERATURE)
    
    @classmethod
    def get_water_intake(cls) -> bytes:
        return cls.build_packet(cls.GET_WATER_INTAKE)
    
    @classmethod
    def get_history(cls) -> bytes:
        return cls.build_packet(cls.GET_HISTORY)
    
    @classmethod
    def sync_time(cls) -> bytes:
        """Sync current time to device"""
        now = datetime.now()
        # Common time format: [year-2000][month][day][hour][minute][second]
        payload = bytes([
            now.year - 2000,
            now.month,
            now.day,
            now.hour,
            now.minute,
            now.second
        ])
        return cls.build_packet(cls.SYNC_TIME, payload)
    
    @classmethod
    def set_reminder(cls, interval_minutes: int = 60, enabled: bool = True) -> bytes:
        """Set drinking reminder"""
        payload = bytes([
            0x01 if enabled else 0x00,
            interval_minutes
        ])
        return cls.build_packet(cls.SET_REMINDER, payload)

# ============================================
# RESPONSE PARSER
# ============================================

class SGUAIParser:
    """Parse responses from SGUAI device"""
    
    @staticmethod
    def parse(data: bytes) -> dict:
        """Parse device response"""
        if len(data) < 3:
            return {"raw": data.hex().upper(), "error": "Too short"}
        
        result = {
            "raw": data.hex().upper(),
            "header": f"0x{data[0]:02X}",
            "command": f"0x{data[1]:02X}",
            "length": data[2] if len(data) > 2 else 0,
        }
        
        command = data[1]
        payload = data[3:-1] if len(data) > 4 else data[3:]
        
        # Parse based on command
        if command == SGUAICommands.GET_BATTERY:
            if len(payload) >= 1:
                result["battery"] = payload[0]
                result["message"] = f"Battery: {payload[0]}%"
                
        elif command == SGUAICommands.GET_TEMPERATURE:
            if len(payload) >= 2:
                # Temperature might be in different formats
                temp = payload[0] + payload[1] / 10.0 if len(payload) >= 2 else payload[0]
                result["temperature"] = temp
                result["message"] = f"Temperature: {temp}°C"
                
        elif command == SGUAICommands.GET_WATER_INTAKE:
            if len(payload) >= 2:
                # Water intake in ml (16-bit value)
                intake = (payload[0] << 8) | payload[1]
                result["water_intake_ml"] = intake
                result["message"] = f"Water intake today: {intake}ml"
                
        elif command == SGUAICommands.GET_DEVICE_INFO:
            result["device_info"] = payload.hex().upper()
            result["message"] = f"Device info received"
            
        elif command == SGUAICommands.GET_HISTORY:
            result["history_data"] = payload.hex().upper()
            result["message"] = f"History data received"
        
        return result

# ============================================
# MAIN DEVICE CLASS
# ============================================

class SGUAIT30:
    """SGUAI T30 Smart Bottle Controller"""
    
    def __init__(self):
        self.client = None
        self.connected = False
        self.write_char = None
        self.notify_char = None
        self.responses = []
        
    def notification_handler(self, sender, data: bytearray):
        """Handle incoming data"""
        hex_data = data.hex().upper()
        print(f"\n📥 Received: {hex_data}")
        
        parsed = SGUAIParser.parse(bytes(data))
        self.responses.append(parsed)
        
        for key, value in parsed.items():
            if key != "raw":
                print(f"   {key}: {value}")
    
    async def scan(self, timeout: float = 10.0):
        """Scan for SGUAI devices"""
        print("🔍 Scanning for SGUAI devices...\n")
        
        devices = await BleakScanner.discover(timeout=timeout)
        sguai_devices = []
        
        for device in devices:
            name = device.name or ""
            if "SGUAI" in name.upper() or "T30" in name.upper():
                sguai_devices.append(device)
                print(f"✅ Found SGUAI: {device.name} ({device.address})")
            else:
                print(f"   Other device: {name or 'Unknown'} ({device.address})")
        
        return sguai_devices
    
    async def connect(self, address: str = None):
        """Connect to device"""
        if address is None:
            devices = await self.scan()
            if not devices:
                print("❌ No SGUAI device found!")
                return False
            address = devices[0].address
        
        print(f"\n🔗 Connecting to {address}...")
        
        try:
            self.client = BleakClient(address)
            await self.client.connect()
            self.connected = True
            print("✅ Connected!")
            
            # Discover services
            await self.discover_services()
            
            return True
            
        except Exception as e:
            print(f"❌ Connection failed: {e}")
            return False
    
    async def discover_services(self):
        """Discover and display services"""
        print("\n" + "="*50)
        print("📦 SERVICES AND CHARACTERISTICS")
        print("="*50)
        
        for service in self.client.services:
            print(f"\nService: {service.uuid}")
            
            for char in service.characteristics:
                props = ", ".join(char.properties)
                print(f"  └─ Char: {char.uuid}")
                print(f"     Properties: {props}")
                
                # Auto-detect write and notify characteristics
                if "write" in char.properties or "write-without-response" in char.properties:
                    if "fff1" in char.uuid.lower() or "fee7" in char.uuid.lower():
                        self.write_char = char.uuid
                        print(f"     ⭐ WRITE CHARACTERISTIC DETECTED")
                
                if "notify" in char.properties:
                    if "fff2" in char.uuid.lower() or "fee8" in char.uuid.lower():
                        self.notify_char = char.uuid
                        print(f"     ⭐ NOTIFY CHARACTERISTIC DETECTED")
                        
                        # Enable notifications
                        try:
                            await self.client.start_notify(char.uuid, self.notification_handler)
                            print(f"     ✅ Notifications enabled")
                        except Exception as e:
                            print(f"     ⚠️ Could not enable: {e}")
        
        print("\n" + "="*50)
        
        # Use defaults if not detected
        if not self.write_char:
            self.write_char = WRITE_CHAR_UUID
            print(f"Using default write UUID: {WRITE_CHAR_UUID}")
        if not self.notify_char:
            self.notify_char = NOTIFY_CHAR_UUID
            print(f"Using default notify UUID: {NOTIFY_CHAR_UUID}")
    
    async def send_command(self, data: bytes):
        """Send command to device"""
        hex_data = data.hex().upper()
        print(f"\n📤 Sending: {hex_data}")
        
        try:
            await self.client.write_gatt_char(self.write_char, data, response=False)
            print("✅ Sent successfully")
            await asyncio.sleep(0.5)  # Wait for response
        except Exception as e:
            print(f"❌ Send failed: {e}")
            # Try alternative format
            print("🔄 Trying alternative packet format...")
            try:
                alt_data = SGUAICommands.build_packet_v2(data[1], data[3:-1] if len(data) > 4 else b'')
                print(f"📤 Sending (alt): {alt_data.hex().upper()}")
                await self.client.write_gatt_char(self.write_char, alt_data, response=False)
            except Exception as e2:
                print(f"❌ Alternative also failed: {e2}")
    
    async def get_battery(self):
        """Get battery level"""
        print("\n🔋 Getting battery level...")
        await self.send_command(SGUAICommands.get_battery())
    
    async def get_temperature(self):
        """Get water temperature"""
        print("\n🌡️ Getting temperature...")
        await self.send_command(SGUAICommands.get_temperature())
    
    async def get_water_intake(self):
        """Get today's water intake"""
        print("\n💧 Getting water intake...")
        await self.send_command(SGUAICommands.get_water_intake())
    
    async def get_device_info(self):
        """Get device information"""
        print("\n📱 Getting device info...")
        await self.send_command(SGUAICommands.get_device_info())
    
    async def get_history(self):
        """Get drinking history"""
        print("\n📊 Getting history...")
        await self.send_command(SGUAICommands.get_history())
    
    async def sync_time(self):
        """Sync time to device"""
        print("\n🕐 Syncing time...")
        await self.send_command(SGUAICommands.sync_time())
    
    async def set_reminder(self, minutes: int = 60):
        """Set drinking reminder"""
        print(f"\n⏰ Setting reminder: every {minutes} minutes")
        await self.send_command(SGUAICommands.set_reminder(minutes))
    
    async def send_raw(self, hex_string: str):
        """Send raw hex command"""
        data = bytes.fromhex(hex_string.replace(" ", ""))
        await self.send_command(data)
    
    async def test_all_commands(self):
        """Test all known commands"""
        print("\n" + "="*50)
        print("🧪 TESTING ALL COMMANDS")
        print("="*50)
        
        await self.get_device_info()
        await asyncio.sleep(1)
        
        await self.get_battery()
        await asyncio.sleep(1)
        
        await self.get_temperature()
        await asyncio.sleep(1)
        
        await self.get_water_intake()
        await asyncio.sleep(1)
        
        await self.get_history()
        await asyncio.sleep(1)
        
        await self.sync_time()
        
        print("\n" + "="*50)
        print("📋 ALL RESPONSES:")
        print("="*50)
        for resp in self.responses:
            print(f"  {resp}")
    
    async def brute_force_commands(self, start: int = 0x01, end: int = 0x30):
        """Try range of commands to discover protocol"""
        print(f"\n🔬 Testing commands 0x{start:02X} to 0x{end:02X}...")
        
        for cmd in range(start, end + 1):
            print(f"\n--- Command 0x{cmd:02X} ---")
            packet = SGUAICommands.build_packet(cmd)
            await self.send_command(packet)
            await asyncio.sleep(0.5)
    
    async def disconnect(self):
        """Disconnect from device"""
        if self.client and self.connected:
            await self.client.disconnect()
            print("\n🔌 Disconnected")

# ============================================
# INTERACTIVE MODE
# ============================================

async def interactive(address: str = None):
    """Interactive control mode"""
    device = SGUAIT30()
    
    if not await device.connect(address):
        return
    
    print("\n" + "="*50)
    print("🎮 SGUAI T30 INTERACTIVE MODE")
    print("="*50)
    print("""
Commands:
  info      - Get device info
  battery   - Get battery level
  temp      - Get temperature
  water     - Get water intake
  history   - Get drinking history
  sync      - Sync time
  reminder  - Set reminder (60 min)
  test      - Test all commands
  brute     - Brute force command discovery
  raw XX    - Send raw hex (e.g., raw AA0200AB)
  quit      - Exit
""")
    print("="*50)
    
    try:
        while True:
            cmd = input("\n>>> ").strip().lower()
            
            if cmd in ["quit", "exit", "q"]:
                break
            elif cmd == "info":
                await device.get_device_info()
            elif cmd == "battery":
                await device.get_battery()
            elif cmd == "temp":
                await device.get_temperature()
            elif cmd == "water":
                await device.get_water_intake()
            elif cmd == "history":
                await device.get_history()
            elif cmd == "sync":
                await device.sync_time()
            elif cmd == "reminder":
                await device.set_reminder(60)
            elif cmd == "test":
                await device.test_all_commands()
            elif cmd == "brute":
                await device.brute_force_commands()
            elif cmd.startswith("raw "):
                await device.send_raw(cmd[4:])
            else:
                print("Unknown command")
                
    except KeyboardInterrupt:
        pass
    finally:
        await device.disconnect()

# ============================================
# MAIN
# ============================================

async def main():
    import sys
    
    print("""
╔═══════════════════════════════════════════════════════════╗
║           SGUAI T30 Smart Bottle Controller               ║
╚═══════════════════════════════════════════════════════════╝
    """)
    
    device = SGUAIT30()
    
    if len(sys.argv) > 1:
        cmd = sys.argv[1].lower()
        
        if cmd == "scan":
            await device.scan(15)
        elif cmd == "connect":
            addr = sys.argv[2] if len(sys.argv) > 2 else None
            await interactive(addr)
        elif cmd == "test":
            addr = sys.argv[2] if len(sys.argv) > 2 else None
            if await device.connect(addr):
                await device.test_all_commands()
                await asyncio.sleep(2)
                await device.disconnect()
    else:
        print("Usage:")
        print("  python sguai_t30.py scan           - Scan for devices")
        print("  python sguai_t30.py connect [MAC]  - Interactive mode")
        print("  python sguai_t30.py test [MAC]     - Test all commands")

if __name__ == "__main__":
    asyncio.run(main())