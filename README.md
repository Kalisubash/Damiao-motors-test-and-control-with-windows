# Damiao-motors-test-and-control-with-windows
in this repository the damiao motors can be control by any python terminal using windows os and with damiao debugger


# DM6006 Motor Controller - Windows

A Python-based controller for Damiao DM6006 motors using USB-CAN adapter on Windows. This project provides easy-to-use scripts for controlling single and dual motor setups with velocity control.



## ✨ Features

- **Single Motor Control**: Test and control individual DM6006 motors
- **Dual Motor Control**: Synchronous control of two motors
- **Velocity Control Mode**: Precise speed control in rad/s
- **Test Sequences**: Pre-programmed movement patterns
- **Windows Compatible**: Optimized for Windows COM port communication
- **Error Handling**: Robust error handling with helpful troubleshooting messages
- **Clean Shutdown**: Safe motor disable and connection closure

## 🔧 Hardware Requirements

- **Motors**: Damiao DM6006 brushless motors (1 or 2 units)
- **Adapter**: USB-to-CAN adapter (slcan compatible)   https://github.com/Kalisubash/Damiao-motors-test-and-control-with-windows/blob/main/Damiao%20can%20debugger.jpeg
- **Power Supply**: Appropriate power supply for DM6006 motors
- **Computer**: Windows PC with available USB port
- **Cables**: CAN bus cables and connectors

### Motor Specifications (DM6006)
- Type: Brushless DC Motor
- Control: CAN Bus communication
- Baud Rate: 921600
- Protocol: Damiao proprietary

## 💻 Software Requirements

- **Operating System**: Windows 10/11
- **Python**: Python 3.7 or higher
- **Libraries**:
  - `pyserial` - Serial communication
  - `DM_CAN_Library` - Damiao motor control library

## 📦 Installation



### 2. Install Python

If you don't have Python installed:
1. Download from [python.org](https://www.python.org/downloads/)
2. Run the installer
3. **Important**: Check "Add Python to PATH" during installation

### 3. Install Required Libraries

Open Command Prompt and run:
```bash
# Install PySerial
pip install pyserial

# Verify installation
pip list
```

### 4. Install DM_CAN_Library

**Option A: Local Installation (if you have the library files)**
```bash
# Place DM_CAN_Library.py in the same directory as your scripts
# Or install it:
pip install path/to/DM_CAN_Library
```

**Option B: From GitHub (if available)**
```bash
pip install git+https://github.com/username/DM_CAN_Library.git
```

**Option C: From Manufacturer**
- Contact Damiao Motors for the official library
- Follow their installation instructions

### 5. Install USB-CAN Driver

1. Connect your USB-CAN adapter
2. Windows will attempt to install drivers automatically
3. If needed, download drivers from your adapter manufacturer
4. Verify installation in Device Manager

## ⚙️ Configuration

### Find Your COM Port

1. Press `Win + X` and select **Device Manager**
2. Expand **Ports (COM & LPT)**
3. Look for your USB-CAN adapter (e.g., "USB Serial Port (COM3)")
4. Note the COM port number

### Update Serial Port in Code

Edit the configuration section in the Python files:
```python
# Change this line to match your COM port
serial_port = "COM3"  # Replace with your actual COM port
```

### Motor CAN IDs

Default configuration:
- **Motor 1**: ID `0x01`, Feedback `0x11`
- **Motor 2**: ID `0x02`, Feedback `0x12`

Modify if your motors have different IDs:
```python
motor_ids = [0x01, 0x02]
feedback_ids = [0x11, 0x12]
```

## 🚀 Usage

### Single Motor Test

Run the single motor test script:
```bash
python windows_1damiaomotortest.py
```

**Test Sequence:**
1. Motor forward at 3.0 rad/s (3 seconds)
2. Motor stop (1 second)
3. Motor backward at -3.0 rad/s (3 seconds)
4. Motor stop (1 second)

### Dual Motor Test

Run the dual motor test script:
```bash
python windows_2damiaomotortest.py
```

**Test Sequence:**
1. Both motors forward at 3.0 rad/s (3 seconds)
2. Both motors stop (1 second)
3. Both motors backward at -3.0 rad/s (3 seconds)
4. Both motors stop (1 second)
5. Motors in opposite directions (3 seconds)
6. Final stop

### Emergency Stop

Press `Ctrl + C` at any time to safely stop and disable all motors.

## 📝 Code Examples

### Basic Motor Control
```python
import time
from DM_CAN_Library import *
import serial

# Setup
serial_port = "COM3"
baud_rate = 921600
serial_device = serial.Serial(serial_port, baud_rate, timeout=0.5)

# Create motor
motor = Motor(DM_Motor_Type.DM6006, 0x01, 0x11)
MotorControl = MotorControl(serial_device)
MotorControl.addMotor(motor)

# Enable and control
MotorControl.switchControlMode(motor, Control_Type.VEL)
MotorControl.enable(motor)
MotorControl.control_Vel(motor, 3.0)  # 3.0 rad/s

# Cleanup
MotorControl.control_Vel(motor, 0)
MotorControl.disable(motor)
serial_device.close()
```

### Dual Motor Synchronous Control
```python
# Create two motors
Motors = []
motor_ids = [0x01, 0x02]
feedback_ids = [0x11, 0x12]

for m_id, f_id in zip(motor_ids, feedback_ids):
    motor = Motor(DM_Motor_Type.DM6006, m_id, f_id)
    Motors.append(motor)
    MotorControl.addMotor(motor)
    MotorControl.enable(motor)

# Control both motors
MotorControl.control_Vel(Motors[0], 3.0)
MotorControl.control_Vel(Motors[1], 3.0)
```

## 🔍 Troubleshooting

### Common Issues

#### "Failed to connect to COM port"

**Solutions:**
- Verify COM port in Device Manager
- Check if another program is using the port
- Try unplugging and replugging the USB adapter
- Update `serial_port` variable in code

#### "ModuleNotFoundError: No module named 'DM_CAN_Library'"

**Solutions:**
```bash
# Ensure the library is in the same directory
# Or install it properly
pip install path/to/DM_CAN_Library
```

#### "Access Denied" Error

**Solutions:**
- Close any other programs using the COM port
- Run Command Prompt as Administrator
- Check USB cable connection

#### Motors Not Responding

**Solutions:**
- Verify motor power supply
- Check CAN bus wiring
- Confirm motor IDs match configuration
- Test with manufacturer's software first

#### "pyserial not found"

**Solutions:**
```bash
# Reinstall pyserial
pip uninstall pyserial
pip install pyserial

# Or use python -m pip
python -m pip install pyserial
```

### Testing Your Setup

1. **Test Python Installation:**
```bash
   python --version
```

2. **Test PySerial:**
```python
   python
   >>> import serial
   >>> print(serial.VERSION)
```

3. **Test COM Port:**
```python
   import serial
   ser = serial.Serial('COM3', 921600, timeout=0.5)
   print("Connected!")
   ser.close()
```





## 🎯 Motor Parameters

### Adjustable Parameters
```python
MAX_SPEED = 6.0           # Maximum speed (rad/s)
baud_rate = 921600        # Serial baud rate
timeout = 0.5             # Serial timeout (seconds)
```

### Safe Operating Limits

- **Max Speed**: 6.0 rad/s (recommended)
- **Test Speed**: 3.0 rad/s (safe testing)
- **Acceleration**: Gradual speed changes recommended
- **Temperature**: Monitor motor temperature during operation

## 🔒 Safety Guidelines

1. **Always test with low speeds first**
2. **Ensure motors are properly mounted and secured**
3. **Keep emergency stop (Ctrl+C) accessible**
4. **Monitor motor temperature**
5. **Use appropriate power supply ratings**
6. **Check all connections before powering on**
7. **Maintain proper CAN bus termination**



## 🗺️ Roadmap

- [ ] Position control mode
- [ ] GUI interface
- [ ] Real-time plotting
- [ ] Configuration file support
- [ ] Multi-motor support (3+)
- [ ] Speed profile generation
- [ ] Data logging and analysis

---

**Made with ❤️ for robotics enthusiasts**

*For questions or support, please open an issue on GitHub.*
