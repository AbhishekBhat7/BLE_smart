import asyncio
from bleak import BleakClient
import struct

class SGUAICommandClient:
    def __init__(self, device_id):
        self.device_id = device_id
        self.service_uuid = "0000ff00-0000-1000-8000-00805f9b34fb"
        self.write_char = "0000ff01-0000-1000-8000-00805f9b34fb"
        self.notify_char = "0000ff02-0000-1000-8000-00805f9b34fb"
        self.last_response = None
    
    def response_handler(self, sender, data):
        """Capture device responses"""
        self.last_response = data
        hex_str = data.hex().upper()
        
        # Check if it's a response (starts with FF55, ends with 0D0A)
        if hex_str.startswith("FF55") and hex_str.endswith("0D0A"):
            print(f"✓ Response: {hex_str}")
            
            # Parse response
            if len(data) >= 4:
                length = data[2]
                cmd_echo = data[3]
                param_echo = data[4] if len(data) > 4 else 0
                
                print(f"  → Command Code: 0x{cmd_echo:02X}")
                print(f"  → Parameter: 0x{param_echo:02X}")
        else:
            # Sensor data (accelerometer)
            if len(data) == 12 and hex_str.startswith("FF55"):
                x = int.from_bytes(data[4:6], 'big')
                y = int.from_bytes(data[6:8], 'big')
                z = int.from_bytes(data[8:10], 'big')
                print(f"Sensor: X={x}, Y={y}, Z={z}")
    
    async def send_command(self, command_hex):
        """Send command and get response"""
        print(f"\n→ Sending: {command_hex}")
        
        # Convert hex string to bytes
        command_bytes = bytes.fromhex(command_hex.replace(" ", ""))
        
        # Send command
        await self.client.write_gatt_char(
            self.write_char,
            command_bytes,
            response=True
        )
        
        # Wait for response (max 1 second)
        await asyncio.sleep(0.5)
        
        if self.last_response:
            return self.last_response.hex().upper()
        return None
    
    async def reset_display(self):
        """Send reset display command and check response"""
        command = "FF 55 07 00 02 15 00"
        response = await self.send_command(command)
        
        if response == "FF550115000D0A":
            print("✓ Reset display command successful!")
            return True
        else:
            print(f"⚠ Unexpected response: {response}")
            return False
    
    async def send_text(self, text):
        """Send text display command"""
        command = ["FF", "55", "07", "00", "02", "17", "01"]
        
        # Add text as UTF-16 big-endian
        for char in text:
            code = ord(char)
            command.append(f"{(code >> 8) & 0xFF:02X}")
            command.append(f"{code & 0xFF:02X}")
        
        command_hex = " ".join(command)
        response = await self.send_command(command_hex)
        
        if response and response.startswith("FF550117"):
            print(f"✓ Text display command successful!")
            return True
        return False
    
    async def send_wifi(self, ssid, password):
        """Send WiFi configuration"""
        command = ["FF", "55", "00", "00", "02", "07"]
        
        for char in ssid:
            command.append(f"{ord(char):02X}")
        
        for char in password:
            command.append(f"{ord(char):02X}")
        
        command_hex = " ".join(command)
        response = await self.send_command(command_hex)
        
        if response and response.startswith("FF550107"):
            print(f"✓ WiFi config command successful!")
            return True
        return False
    
    async def run(self):
        """Connect and run tests"""
        async with BleakClient(self.device_id) as client:
            self.client = client
            print(f"✓ Connected to {self.device_id}")
            
            # Enable notifications for responses
            await client.start_notify(self.notify_char, self.response_handler)
            print("✓ Listening for responses...\n")
            
            # Test commands one by one
            
            # Test 1: Reset Display
            print("=" * 50)
            print("TEST 1: Reset Display Command")
            print("=" * 50)
            await self.reset_display()
            await asyncio.sleep(0.5)
            
            # Test 2: Display Text
            print("\n" + "=" * 50)
            print("TEST 2: Display Text 'Hi'")
            print("=" * 50)
            await self.send_text("Hi")
            await asyncio.sleep(0.5)
            
            # Test 3: WiFi Config
            print("\n" + "=" * 50)
            print("TEST 3: WiFi Configuration")
            print("=" * 50)
            await self.send_wifi("MyNetwork", "password")
            await asyncio.sleep(0.5)
            
            # Listen for sensor data
            print("\n" + "=" * 50)
            print("Listening for sensor data...")
            print("(Shake the device to see accelerometer readings)")
            print("=" * 50)
            await asyncio.sleep(10)
            
            # Stop notifications
            await client.stop_notify(self.notify_char)
            print("\n✓ Test complete")

# Usage
async def main():
    client = SGUAICommandClient("1CE2A01D-CB27-AE2A-1E7C-EE0BC580DFF8")
    await client.run()

if __name__ == "__main__":
    asyncio.run(main())