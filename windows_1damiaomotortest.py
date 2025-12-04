import time
from DM_CAN_Library import *
import serial

# =========================
# === MOTOR CONFIG ========
# =========================
serial_port = "COM13"  # Change this to your COM port (COM3, COM4, COM5, etc.)
baud_rate = 921600
MotorType = DM_Motor_Type.DM6006

# Single Motor CAN IDs
motor_id = 0x01
feedback_id = 0x11

MAX_SPEED = 6.0    # rad/s

print("\n" + "="*60)
print("DM6006 Motor Controller - Windows")
print("="*60)
print(f"Serial Port: {serial_port}")
print(f"Baud Rate: {baud_rate}")
print(f"Motor ID: {motor_id}")
print("="*60 + "\n")

# =========================
# === INITIALIZE SERIAL & MOTOR ===
# =========================
try:
    serial_device = serial.Serial(serial_port, baud_rate, timeout=0.5)
    print(f"✓ Connected to {serial_port}")
except Exception as e:
    print(f"✗ Error connecting to {serial_port}: {e}")
    print("\nTroubleshooting:")
    print("1. Check if your USB adapter is connected")
    print("2. Open Device Manager (Win + X → Device Manager)")
    print("3. Look under 'Ports (COM & LPT)' for your device")
    print("4. Update serial_port variable with correct COM port")
    print("5. Ensure pyserial is installed: pip install pyserial")
    exit(1)

# Create motor object
motor = Motor(MotorType, motor_id, feedback_id)

# Create MotorControl object
MotorControl = MotorControl(serial_device)
MotorControl.addMotor(motor)
MotorControl.switchControlMode(motor, Control_Type.VEL)
MotorControl.enable(motor)

time.sleep(0.2)
print("Motor enabled. Running test sequence...\n")

# =========================
# === MAIN LOOP ===========
# =========================
try:
    # Run motor forward at half speed for 3 seconds
    print("[1/4] Motor forward at 3.0 rad/s...")
    MotorControl.control_Vel(motor, 3.0)
    time.sleep(3)
    
    # Stop motor for 1 second
    print("[2/4] Motor stopped...")
    MotorControl.control_Vel(motor, 0.0)
    time.sleep(1)
    
    # Run motor backward at half speed for 3 seconds
    print("[3/4] Motor backward at -3.0 rad/s...")
    MotorControl.control_Vel(motor, -3.0)
    time.sleep(3)
    
    # Stop motor
    print("[4/4] Motor stopped...")
    MotorControl.control_Vel(motor, 0.0)
    time.sleep(1)
    
    print("\n✓ Test sequence complete.")

except KeyboardInterrupt:
    print("\n\n⚠ Stopping...")
    
except Exception as e:
    print(f"\n✗ Error during operation: {e}")
    import traceback
    traceback.print_exc()
    
finally:
    # Stop and disable motor
    try:
        print("\n[Shutdown Sequence]")
        MotorControl.control_Vel(motor, 0)
        MotorControl.disable(motor)
        serial_device.close()
        print("✓ Motor disabled, serial closed.")
    except Exception as shutdown_error:
        print(f"✗ Error during shutdown: {shutdown_error}")
    
    print("\n" + "="*60)
    print("Program ended")
    print("="*60)