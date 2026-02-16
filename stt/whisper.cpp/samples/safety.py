"""
Safety and collision detection module for PiCar-X
Provides ultrasonic sensor monitoring and emergency stop functionality
"""
import time
import threading

try:
    from picarx import Picarx
except ImportError:
    print("Warning: picarx library not found. Running in simulation mode.")
    Picarx = None


class SafetyMonitor:
    """Safety monitor for PiCar-X with collision detection"""
    
    def __init__(self, picar_controller, simulation_mode=False):
        """
        Initialize safety monitor
        
        Args:
            picar_controller: PiCarXController instance
            simulation_mode: If True, simulates sensor readings
        """
        self.controller = picar_controller
        self.simulation_mode = simulation_mode or Picarx is None
        
        # Safety settings
        self.min_distance = 20  # cm - minimum safe distance
        self.emergency_distance = 10  # cm - emergency stop distance
        
        # Monitoring state
        self.monitoring = False
        self.monitor_thread = None
        self.last_distance = 100
        self.collision_detected = False
        
        # Emergency stop flag
        self.emergency_stop_triggered = False
        
        print(f"✓ Safety Monitor initialized ({'simulation' if self.simulation_mode else 'hardware'} mode)")
    
    def start_monitoring(self):
        """Start background safety monitoring"""
        if self.monitoring:
            return
        
        self.monitoring = True
        self.emergency_stop_triggered = False
        self.monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self.monitor_thread.start()
        print("✓ Safety monitoring started")
    
    def stop_monitoring(self):
        """Stop background safety monitoring"""
        self.monitoring = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=1.0)
        print("✓ Safety monitoring stopped")
    
    def _monitor_loop(self):
        """Background monitoring loop"""
        while self.monitoring:
            distance = self.get_distance()
            self.last_distance = distance
            
            # Check for collision risk
            if distance <= self.emergency_distance:
                if not self.collision_detected:
                    print(f"⚠️  EMERGENCY STOP! Object at {distance}cm")
                    self.emergency_stop()
                    self.collision_detected = True
            elif distance <= self.min_distance:
                if not self.collision_detected:
                    print(f"⚠️  WARNING: Object detected at {distance}cm")
                    # Could slow down instead of full stop
                    self.collision_detected = True
            else:
                self.collision_detected = False
            
            time.sleep(0.1)  # Check 10 times per second
    
    def get_distance(self):
        """
        Get distance reading from ultrasonic sensor
        
        Returns:
            Distance in centimeters
        """
        if self.simulation_mode:
            # Simulate sensor reading (random distance 10-100cm)
            import random
            return random.randint(10, 100)
        
        try:
            if self.controller.picar:
                # Read from ultrasonic sensor
                distance = self.controller.picar.ultrasonic.read()
                return distance if distance > 0 else 100
        except Exception as e:
            print(f"Error reading ultrasonic sensor: {e}")
        
        return 100  # Default safe distance
    
    def emergency_stop(self):
        """Execute emergency stop"""
        self.emergency_stop_triggered = True
        self.controller.stop()
        print("🛑 EMERGENCY STOP ACTIVATED")
    
    def reset_emergency_stop(self):
        """Reset emergency stop flag"""
        self.emergency_stop_triggered = False
        self.collision_detected = False
        print("✓ Emergency stop reset")
    
    def is_safe_to_move(self):
        """
        Check if it's safe to move forward
        
        Returns:
            True if safe, False otherwise
        """
        if self.emergency_stop_triggered:
            return False
        
        distance = self.get_distance()
        return distance > self.min_distance
    
    def get_status(self):
        """
        Get current safety status
        
        Returns:
            dict with status information
        """
        return {
            "monitoring": self.monitoring,
            "distance": self.last_distance,
            "safe": not self.collision_detected,
            "emergency_stop": self.emergency_stop_triggered
        }


class SafePiCarXController:
    """PiCar-X controller wrapper with safety features"""
    
    def __init__(self, base_controller, safety_monitor):
        """
        Initialize safe controller wrapper
        
        Args:
            base_controller: PiCarXController instance
            safety_monitor: SafetyMonitor instance
        """
        self.controller = base_controller
        self.safety = safety_monitor
    
    def forward(self, speed=None, duration=None):
        """Move forward with safety check"""
        if not self.safety.is_safe_to_move():
            print("⚠️  Cannot move forward: obstacle detected")
            return False
        
        self.controller.forward(speed, duration)
        return True
    
    def backward(self, speed=None, duration=None):
        """Move backward (no obstacle check needed)"""
        self.controller.backward(speed, duration)
        return True
    
    def turn_left(self, angle=None, duration=None):
        """Turn left with safety check"""
        if not self.safety.is_safe_to_move():
            print("⚠️  Cannot turn: obstacle detected")
            return False
        
        self.controller.turn_left(angle, duration)
        return True
    
    def turn_right(self, angle=None, duration=None):
        """Turn right with safety check"""
        if not self.safety.is_safe_to_move():
            print("⚠️  Cannot turn: obstacle detected")
            return False
        
        self.controller.turn_right(angle, duration)
        return True
    
    def stop(self):
        """Stop all movement"""
        self.controller.stop()
        return True
    
    def set_camera_pan(self, angle):
        """Set camera pan (no safety check needed)"""
        self.controller.set_camera_pan(angle)
    
    def set_camera_tilt(self, angle):
        """Set camera tilt (no safety check needed)"""
        self.controller.set_camera_tilt(angle)
    
    def look_forward(self):
        """Reset camera to forward"""
        self.controller.look_forward()
    
    def nod(self, times=1):
        """Make nodding gesture"""
        self.controller.nod(times)
    
    def shake_head(self, times=1):
        """Make head-shaking gesture"""
        self.controller.shake_head(times)
    
    def cleanup(self):
        """Cleanup both controller and safety monitor"""
        self.safety.stop_monitoring()
        self.controller.cleanup()
    
    def get_safety_status(self):
        """Get safety status"""
        return self.safety.get_status()


if __name__ == "__main__":
    # Test safety features
    print("Testing Safety Monitor\n")
    
    from picarx_control import PiCarXController
    
    # Create controller
    controller = PiCarXController(simulation_mode=True)
    
    # Create safety monitor
    safety = SafetyMonitor(controller, simulation_mode=True)
    
    # Create safe controller
    safe_controller = SafePiCarXController(controller, safety)
    
    # Start monitoring
    safety.start_monitoring()
    
    print("\n--- Testing Safe Movements ---")
    time.sleep(1)
    
    # Test movements
    print("\nTrying to move forward...")
    success = safe_controller.forward(30, 1)
    print(f"Movement {'succeeded' if success else 'blocked'}")
    
    time.sleep(1)
    
    # Get status
    status = safe_controller.get_safety_status()
    print(f"\nSafety Status: {status}")
    
    # Test emergency stop
    print("\n--- Testing Emergency Stop ---")
    safety.emergency_stop()
    print("Trying to move forward after emergency stop...")
    success = safe_controller.forward(30, 1)
    print(f"Movement {'succeeded' if success else 'blocked'}")
    
    # Reset and try again
    safety.reset_emergency_stop()
    print("\nReset emergency stop, trying to move...")
    time.sleep(0.5)
    success = safe_controller.forward(30, 1)
    print(f"Movement {'succeeded' if success else 'blocked'}")
    
    # Cleanup
    time.sleep(1)
    safe_controller.cleanup()
    
    print("\n✓ Safety test complete")
