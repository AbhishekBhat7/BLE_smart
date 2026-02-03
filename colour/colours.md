ff550b0002280100c300c3 blue
ff550b00022801004c004c yellow
ff550b00022801014f014f pink 
ff550b0002280100040004  red

Based on the packet captures you provided, we can successfully reverse engineer the color encoding logic. The device is not using RGB (Red, Green, Blue) values directly. Instead, it is using a **Hue (HSV/HSL)** color wheel representation.

Here is the breakdown of the packet structure and the predicted commands for other colors.

### 1. Packet Analysis

Let's break down the structure of your captured packets:
`ff 55 0b 00 02 28 01 [AA BB] [AA BB]`

*   **Header (`ff 55 0b 00 02 28 01`):** This is the static prefix. `0b` likely represents the packet length (11 bytes).
*   **Color Data (`AA BB`):** These two bytes represent the color.
*   **Repetition (`AA BB`):** The color data is repeated immediately after for redundancy/validation.

#### Decoding the Color Value
The two bytes `[AA BB]` form a 16-bit integer (Big Endian) that corresponds to the **Hue** angle on a standard 360° color wheel.

*   **Red:** Hex `00 04` = Decimal **4** (Close to 0°, which is Red)
*   **Yellow:** Hex `00 4C` = Decimal **76** (Close to 60°, which is Yellow)
*   **Blue:** Hex `00 C3` = Decimal **195** (This is actually Light Blue/Cyan. 180° is Cyan, 240° is Blue)
*   **Pink:** Hex `01 4F` = Decimal **335** (300° is Magenta, 335° is Pink/Rose)

**The Formula:**
To get a specific color, choose a degree (0-360) and convert it to a 4-digit Hex string.

### 2. Predicted Colors

Here are the predicted packets for other common colors based on the Hue logic.

**Standard Green (120°)**
*   Decimal: 120
*   Hex: `00 78`
*   **Packet:** `ff550b0002280100780078`

**Deep Blue (240°)**
*   *(Your captured "Blue" was 195, which is light blue. This is deep blue)*
*   Decimal: 240
*   Hex: `00 F0`
*   **Packet:** `ff550b0002280100f000f0`

**Orange (30°)**
*   Decimal: 30
*   Hex: `00 1E`
*   **Packet:** `ff550b00022801001e001e`

**Cyan / Turquoise (180°)**
*   Decimal: 180
*   Hex: `00 B4`
*   **Packet:** `ff550b0002280100b400b4`

**Purple / Violet (270°)**
*   Decimal: 270
*   Hex: `01 0E`
*   **Packet:** `ff550b00022801010e010e`

### 3. How to calculate any color manually

If you want to create a custom color:

1.  Look at a **Color Wheel** and pick the degree ($0$ to $360$) of the color you want.
2.  Convert that number to **Hexadecimal** (you can use an online converter or Windows Calculator in Programmer mode).
3.  Pad it with zeros to make it 4 digits (e.g., if you get `F0`, make it `00F0`. If you get `10E`, make it `010E`).
4.  Split it into two bytes (e.g., `01` and `0E`).
5.  Construct the string: `ff550b00022801` + `Byte1 Byte2` + `Byte1 Byte2`.

### Summary Table

| Color | Angle | Hex Value | Complete Packet |
| :--- | :--- | :--- | :--- |
| **Red** | 4° | `00 04` | `ff550b0002280100040004` |
| **Orange** | 30° | `00 1E` | `ff550b00022801001e001e` |
| **Yellow** | 76° | `00 4C` | `ff550b00022801004c004c` |
| **Green** | 120° | `00 78` | `ff550b0002280100780078` |
| **Cyan** | 180° | `00 B4` | `ff550b0002280100b400b4` |
| **Light Blue** | 195° | `00 C3` | `ff550b0002280100c300c3` |
| **Deep Blue** | 240° | `00 F0` | `ff550b0002280100f000f0` |
| **Purple** | 270° | `01 0E` | `ff550b00022801010e010e` |
| **Pink** | 335° | `01 4F` | `ff550b00022801014f014f` |




Q&A


Great to hear it worked! Reverse engineering is basically solving puzzles, so it feels great when the pieces fit.

Here is the breakdown of how I deduced the logic, why the data repeats, and what the prefix means. This is standard procedure for analyzing **IoT (Internet of Things) Bluetooth Low Energy (BLE)** packets.

---

### 1. How I predicted it was "Degrees" (Hue)
I didn't guess; I looked for **patterns in the numbers** after converting them from Hex to Decimal.

When you look at RGB LED controllers, they usually work in one of two ways:
1.  **RGB (Red, Green, Blue):** Uses 3 numbers (e.g., `255, 0, 0` for red).
2.  **HSV (Hue, Saturation, Value):** Uses the "Color Wheel" angle.

**The Clues:**
*   You only had **2 bytes** changing (`00 04`, `00 4c`, etc.). RGB requires 3 bytes, so it wasn't standard RGB.
*   I converted your Hex values to Decimal:
    *   **Red:** `0004` -> **4**
    *   **Yellow:** `004c` -> **76**
    *   **Blue:** `00c3` -> **195**
    *   **Pink:** `014f` -> **335**

**The "Aha!" Moment:**
I mapped these decimal numbers to a circle (0 to 360).
*   On a color wheel, **0° is Red**. Your value was **4** (basically 0).
*   On a color wheel, **Yellow is 60°**. Your value was **76** (close enough).
*   On a color wheel, **Pink/Magenta is 300-340°**. Your value was **335** (perfect match).

Since the numbers fit perfectly onto a 0-360 circle, I knew the device was using the **Hue Angle** to determine color.

---

### 2. Why is the color repeated? (`...C3 00 C3`)
You noticed the structure: `[Data] [Data]`.
For example: `... 01 4F 01 4F`.

There are two likely reasons for this in embedded engineering:

**Reason A: Error Checking (Most Likely)**
Bluetooth can sometimes drop packets or have interference. This is a "lazy man's checksum."
The device's firmware probably has logic like this:
```c
byte1 = readByte();
byte2 = readByte();
if (byte1 == byte2) {
    setColor(byte1);
} else {
    ignore(); // Data is corrupted
}
```
It ensures the device doesn't change to a random flashing color if a bit gets flipped during transmission.

**Reason B: Dual Channel Control**
Some smart devices have LEDs on two sides (Left/Right) or two rings (Inner/Outer). It is sending the command: `[Set Left to Pink] [Set Right to Pink]`. If you sent `01 4f 00 04`, you might find half the device turns pink and the other half turns red. (You can test this!)

---

### 3. What is the Prefix? (`ff 55 0b...`)
This is the **Packet Header**. It tells the chip inside the device "Hey, a message is starting now."

Here is the breakdown of `ff 55 0b 00 02 28 01`:

1.  **`ff 55` (The Preamble / Magic Word):**
    This is a standard synchronization pattern.
    *   `0xFF` in binary is `11111111` (all high).
    *   `0x55` in binary is `01010101` (alternating).
    This distinct pattern wakes up the microcontroller's UART/Serial receiver and says "This is the start of a valid frame." Many Chinese IoT chips (like Tuya or generic MCUs) use `55 AA` or `FF 55`.

2.  **`0b` (Packet Length):**
    `0x0b` in Hex equals **11** in Decimal.
    Count your total bytes: `ff 55 0b 00 02 28 01 [AA BB] [AA BB]`
    That is exactly **11 bytes**.
    The device reads this byte so it knows exactly how many more bytes to listen for before stopping.

3.  **`00 02` (Protocol Version or Device ID):**
    This is likely static. It identifies the type of device or the version of the communication protocol being used.

4.  **`28` (The Command ID):**
    In this specific protocol, `0x28` means "Lighting Control."
    If you were to change the Vibration mode or Suction mode (since this is the SGUAI app), this byte would likely change to something else (like `0x30` or `0x15`).

5.  **`01` (Sub-Command / Mode):**
    This likely means "Set Static Color."
    If you set the light to "Blink" or "Rainbow Mode," this `01` might change to `02` or `03`.

### How to use this for further hacking:
If you want to find the command for the **"Reminder Light"** you mentioned earlier:
1.  Keep the header `ff 55 0b 00 02`.
2.  Try changing the Command ID (`28`) to nearby numbers (`29`, `27`, `30`).
3.  Or, try keeping `28` but change the Mode (`01`) to `00`, `02`, `03`.

Happy sniffing!





///////////////

Reminder
1. The Protocol Analysis
Let's compare the two hex strings you captured:

Red: ff 55 08 00 02 2b 00 00
Blue: ff 55 08 00 02 2b 00 e6
Byte-by-Byte Breakdown:

ff 55: Header/Preamble. This tells the device a message is starting. (Common in generic LED controllers).
08: Packet Length. The total message is 8 bytes long.
00 02: Device Group/ID or internal addressing (likely static).
2b: Command. 0x2B is likely the command for "Set Mode" or "Set Hue/Color Wheel".
00: Parameter 1 (Likely Saturation or Brightness, or simply padding).
00 vs e6: The Variable (Hue). This is the value changing based on your slider.
