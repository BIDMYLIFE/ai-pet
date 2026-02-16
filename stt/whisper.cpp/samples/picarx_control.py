"""
PiCar-X Motor and Servo Control Module
Provides a simple interface for controlling the PiCar-X robot platform
"""
import time

try:
    from picarx import Picarx
except ImportError:
    print("Warning: picarx library not found. Running in simulation mode.")
    Picarx = None


class PiCarXController:
    """Controller for PiCar-X robot movements and servo control"""
    
    def __init__(self, simulation_mode=False):
        """
        Initialize PiCar-X controller
        
        Args:
            simulation_mode: If True, runs without actual hardware
        """
        self.simulation_mode = simulation_mode or Picarx is None
        
        if not self.simulation_mode:
            try:
                self.picar = Picarx()
                print("✓ PiCar-X initialized successfully")
            except Exception as e:
                print(f"Warning: Could not initialize PiCar-X hardware: {e}")
                print("Running in simulation mode")
                self.simulation_mode = True
                self.picar = None
        else:
            self.picar = None
            print("✓ PiCar-X running in simulation mode")
        
        # Default speeds and angles
        self.default_speed = 30
        self.default_angle = 0
        
    def forward(self, speed=None, duration=None):
        """
        Move forward
        
        Args:
            speed: Speed percentage (0-100), default 30
            duration: Time in seconds to move, None for continuous
        """
        speed = speed or self.default_speed
        
        if self.simulation_mode:
            print(f"[SIM] Moving forward at speed {speed}%")
        else:
            self.picar.forward(speed)
        
        if duration:
            time.sleep(duration)
            self.stop()
    
    def backward(self, speed=None, duration=None):
        """
        Move backward
        
        Args:
            speed: Speed percentage (0-100), default 30
            duration: Time in seconds to move, None for continuous
        """
        speed = speed or self.default_speed
        
        if self.simulation_mode:
            print(f"[SIM] Moving backward at speed {speed}%")
        else:
            self.picar.backward(speed)
        
        if duration:
            time.sleep(duration)
            self.stop()
    
    def turn_left(self, angle=None, duration=None):
        """
        Turn left
        
        Args:
            angle: Steering angle (-40 to 40), default -30
            duration: Time in seconds to turn, None for continuous
        """
        angle = angle if angle is not None else -30
        
        if self.simulation_mode:
            print(f"[SIM] Turning left at angle {angle}")
        else:
            self.picar.set_dir_servo_angle(angle)
            self.picar.forward(self.default_speed)
        
        if duration:
            time.sleep(duration)
            self.stop()
    
    def turn_right(self, angle=None, duration=None):
        """
        Turn right
        
        Args:
            angle: Steering angle (-40 to 40), default 30
            duration: Time in seconds to turn, None for continuous
        """
        angle = angle if angle is not None else 30
        
        if self.simulation_mode:
            print(f"[SIM] Turning right at angle {angle}")
        else:
            self.picar.set_dir_servo_angle(angle)
            self.picar.forward(self.default_speed)
        
        if duration:
            time.sleep(duration)
            self.stop()
    
    def stop(self):
        """Stop all movement"""
        if self.simulation_mode:
            print("[SIM] Stopped")
        else:
            self.picar.stop()
            self.picar.set_dir_servo_angle(0)
    
    def set_camera_pan(self, angle):
        """
        Set camera pan servo angle
        
        Args:
            angle: Angle in degrees (-90 to 90)
        """
        if self.simulation_mode:
            print(f"[SIM] Camera pan set to {angle}°")
        else:
            self.picar.set_camera_servo1_angle(angle)
    
    def set_camera_tilt(self, angle):
        """
        Set camera tilt servo angle
        
        Args:
            angle: Angle in degrees (-90 to 90)
        """
        if self.simulation_mode:
            print(f"[SIM] Camera tilt set to {angle}°")
        else:
            self.picar.set_camera_servo2_angle(angle)
    
    def look_forward(self):
        """Reset camera to forward position"""
        if self.simulation_mode:
            print("[SIM] Camera reset to forward")
        else:
            self.picar.set_camera_servo1_angle(0)
            self.picar.set_camera_servo2_angle(0)
    
    def nod(self, times=1):
        """
        Make the camera nod (yes gesture)
        
        Args:
            times: Number of nods
        """
        for _ in range(times):
            self.set_camera_tilt(-20)
            time.sleep(0.3)
            self.set_camera_tilt(20)
            time.sleep(0.3)
        self.set_camera_tilt(0)
    
    def shake_head(self, times=1):
        """
        Make the camera shake (no gesture)
        
        Args:
            times: Number of shakes
        """
        for _ in range(times):
            self.set_camera_pan(-30)
            time.sleep(0.3)
            self.set_camera_pan(30)
            time.sleep(0.3)
        self.set_camera_pan(0)
    
    def cleanup(self):
        """Cleanup and reset servos"""
        if not self.simulation_mode and self.picar:
            self.stop()
            self.look_forward()


def parse_movement_command(text):
    """
    Parse text for movement commands
    
    Args:
        text: Text to parse for commands
        
    Returns:
        dict with action and parameters, or None
    """
    text_lower = text.lower()
    
    # Movement commands
    if any(word in text_lower for word in ["forward", "ahead", "move forward", "go forward"]):
        return {"action": "forward", "duration": 2.0}
    
    if any(word in text_lower for word in ["backward", "back", "move back", "go back"]):
        return {"action": "backward", "duration": 2.0}
    
    if any(word in text_lower for word in ["turn left", "left", "go left"]):
        return {"action": "turn_left", "duration": 1.5}
    
    if any(word in text_lower for word in ["turn right", "right", "go right"]):
        return {"action": "turn_right", "duration": 1.5}
    
    if any(word in text_lower for word in ["stop", "halt", "wait"]):
        return {"action": "stop"}
    
    # Gesture commands
    if any(word in text_lower for word in ["nod", "yes"]) and "head" in text_lower:
        return {"action": "nod", "times": 2}
    
    if any(word in text_lower for word in ["shake", "no"]) and "head" in text_lower:
        return {"action": "shake_head", "times": 2}
    
    return None


if __name__ == "__main__":
    # Test the controller
    print("Testing PiCar-X Controller")
    controller = PiCarXController(simulation_mode=True)
    
    # Test movements
    print("\n--- Testing Movements ---")
    controller.forward(30, 1)
    time.sleep(0.5)
    controller.backward(30, 1)
    time.sleep(0.5)
    controller.turn_left(duration=1)
    time.sleep(0.5)
    controller.turn_right(duration=1)
    time.sleep(0.5)
    
    # Test gestures
    print("\n--- Testing Gestures ---")
    controller.nod(2)
    time.sleep(0.5)
    controller.shake_head(2)
    
    # Test command parsing
    print("\n--- Testing Command Parsing ---")
    test_commands = [
        "Please move forward",
        "Turn left now",
        "Go backward",
        "Stop moving",
        "Nod your head"
    ]
    
    for cmd in test_commands:
        result = parse_movement_command(cmd)
        print(f"'{cmd}' -> {result}")
    
    controller.cleanup()
    print("\n✓ Test complete")
