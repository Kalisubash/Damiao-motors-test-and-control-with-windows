import time
from DM_CAN_Library import *
import serial

# =========================
# === MOTOR CONFIG ========
# =========================
serial_port = "COM13"  # Change this to your COM port (COM3, COM4, COM5, etc.)
baud_rate = 921600
MotorType = DM_Motor_Type.DM6006

# Motor CAN IDs
motor_ids = [0x01, 0x02]
feedback_ids = [0x11, 0x12]

MAX_SPEED = 6.0    # rad/s

print("\n" + "="*60)
print("DM6006 Two-Motor Controller - Windows")
print("="*60)
print(f"Serial Port: {serial_port}")
print(f"Baud Rate: {baud_rate}")
print(f"Motor IDs: {motor_ids}")
print("="*60 + "\n")

# =========================
# === INITIALIZE SERIAL & MOTORS ===
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

# Create motor objects
Motors = []
for m_id, f_id in zip(motor_ids, feedback_ids):
    motor = Motor(MotorType, m_id, f_id)
    Motors.append(motor)

# Create MotorControl object
MotorControl = MotorControl(serial_device)

print("\n[Initialization]")
for idx, (motor, m_id) in enumerate(zip(Motors, motor_ids), 1):
    MotorControl.addMotor(motor)
    MotorControl.switchControlMode(motor, Control_Type.VEL)
    MotorControl.enable(motor)
    print(f"  ✓ Motor {idx} (ID 0x{m_id:02X}) enabled")

time.sleep(0.2)
print("\n✓ Both motors enabled. Running test sequence...\n")

# =========================
# === MAIN LOOP ===========
# =========================
try:
    # Run both motors forward at half speed for 3 seconds
    print("[1/5] Both motors forward at 3.0 rad/s...")
    MotorControl.control_Vel(Motors[0], 3.0)
    MotorControl.control_Vel(Motors[1], 3.0)
    time.sleep(3)
    
    # Stop both motors for 1 second
    print("[2/5] Both motors stopped...")
    MotorControl.control_Vel(Motors[0], 0.0)
    MotorControl.control_Vel(Motors[1], 0.0)
    time.sleep(1)
    
    # Run both motors backward at half speed for 3 seconds
    print("[3/5] Both motors backward at -3.0 rad/s...")
    MotorControl.control_Vel(Motors[0], -3.0)
    MotorControl.control_Vel(Motors[1], -3.0)
    time.sleep(3)
    
    # Stop both motors
    print("[4/5] Both motors stopped...")
    MotorControl.control_Vel(Motors[0], 0.0)
    MotorControl.control_Vel(Motors[1], 0.0)
    time.sleep(1)
    
    # Run motors in opposite directions for 3 seconds
    print("[5/5] Motor 1 forward, Motor 2 backward at 3.0 rad/s...")
    MotorControl.control_Vel(Motors[0], 3.0)
    MotorControl.control_Vel(Motors[1], -3.0)
    time.sleep(3)
    
    # Stop both motors
    print("[Final] Both motors stopped...")
    MotorControl.control_Vel(Motors[0], 0.0)
    MotorControl.control_Vel(Motors[1], 0.0)
    time.sleep(1)
    
    print("\n✓ Test sequence complete.")

except KeyboardInterrupt:
    print("\n\n⚠ Stopping...")
    
except Exception as e:
    print(f"\n✗ Error during operation: {e}")
    import traceback
    traceback.print_exc()
    
finally:
    # Stop and disable all motors
    try:
        print("\n[Shutdown Sequence]")
        for idx, (motor, m_id) in enumerate(zip(Motors, motor_ids), 1):
            MotorControl.control_Vel(motor, 0)
            MotorControl.disable(motor)
            print(f"  ✓ Motor {idx} (ID 0x{m_id:02X}) disabled")
        serial_device.close()
        print("✓ Serial connection closed.")
    except Exception as shutdown_error:
        print(f"✗ Error during shutdown: {shutdown_error}")
    
    print("\n" + "="*60)
    print("Program ended")
    print("="*60)