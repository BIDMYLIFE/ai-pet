"""
Configuration management for AI Pet project
Provides flexible path configuration for different environments
"""
import os
import json
from pathlib import Path


class Config:
    """Configuration manager for AI Pet"""
    
    def __init__(self, config_file=None):
        """
        Initialize configuration
        
        Args:
            config_file: Optional path to JSON config file
        """
        # Default configuration
        self.defaults = {
            # Paths
            "base_dir": str(Path.home() / "ai-pet"),
            "whisper_cli": "whisper-cli",
            "piper_bin": "piper",
            "piper_model": "models/en_US-lessac-medium.onnx",
            "whisper_model": "../models/ggml-tiny.bin",
            
            # Files
            "wav_file": "test16k.wav",
            "txt_file": "test16k.wav.txt",
            "watch_file": "watch.txt",
            "piper_out": "tts.wav",
            
            # LLM settings
            "llm_model": "gemma3:270m",
            "llm_backend": "ollama",
            
            # Audio settings
            "audio_device": "hw:2,0",
            "audio_format": "S16_LE",
            "audio_rate": 16000,
            "audio_channels": 1,
            "record_duration": 5,
            "playback_device": "plughw:0,0",
            
            # Character settings
            "character_idle": "characters/character0.gif",
            "character_talking": "characters/character1.gif",
            "display_time_ms": 3000,
            "frame_delay_ms": 100,
            
            # PiCar-X settings
            "enable_picarx": False,
            "picarx_simulation": True,
            "picarx_speed": 30,
            "enable_movement_commands": True,
            
            # Greeting
            "default_greeting": "Hello"
        }
        
        self.config = self.defaults.copy()
        
        # Try to load from config file
        if config_file and os.path.exists(config_file):
            self.load_from_file(config_file)
        else:
            # Try default locations
            default_locations = [
                "config.json",
                os.path.join(str(Path.home()), ".ai-pet-config.json"),
                "/etc/ai-pet/config.json"
            ]
            
            for location in default_locations:
                if os.path.exists(location):
                    self.load_from_file(location)
                    break
    
    def load_from_file(self, config_file):
        """Load configuration from JSON file"""
        try:
            with open(config_file, 'r') as f:
                user_config = json.load(f)
                self.config.update(user_config)
            print(f"✓ Loaded configuration from {config_file}")
        except Exception as e:
            print(f"Warning: Could not load config from {config_file}: {e}")
    
    def save_to_file(self, config_file):
        """Save current configuration to JSON file"""
        try:
            with open(config_file, 'w') as f:
                json.dump(self.config, f, indent=2)
            print(f"✓ Saved configuration to {config_file}")
        except Exception as e:
            print(f"Error: Could not save config to {config_file}: {e}")
    
    def get(self, key, default=None):
        """Get a configuration value"""
        return self.config.get(key, default)
    
    def set(self, key, value):
        """Set a configuration value"""
        self.config[key] = value
    
    def get_absolute_path(self, key):
        """Get absolute path for a file/directory configuration"""
        value = self.get(key)
        if not value:
            return None
        
        # If already absolute, return as-is
        if os.path.isabs(value):
            return value
        
        # Otherwise, make relative to base_dir or script directory
        base_dir = self.get("base_dir")
        if base_dir and os.path.exists(base_dir):
            return os.path.join(base_dir, value)
        
        # Fall back to script directory
        script_dir = os.path.dirname(os.path.abspath(__file__))
        return os.path.join(script_dir, value)
    
    def create_sample_config(self, output_file="config.json"):
        """Create a sample configuration file"""
        with open(output_file, 'w') as f:
            json.dump(self.defaults, f, indent=2)
        print(f"✓ Created sample config at {output_file}")
        print(f"  Edit this file to customize your AI Pet settings")


# Global config instance
_config = None


def get_config(config_file=None):
    """Get the global configuration instance"""
    global _config
    if _config is None:
        _config = Config(config_file)
    return _config


if __name__ == "__main__":
    import sys
    
    # Command line interface for config management
    if len(sys.argv) > 1 and sys.argv[1] == "create":
        config = Config()
        output_file = sys.argv[2] if len(sys.argv) > 2 else "config.json"
        config.create_sample_config(output_file)
    else:
        # Test configuration
        print("Testing configuration system\n")
        config = get_config()
        
        print("Configuration values:")
        for key in ["base_dir", "llm_model", "enable_picarx", "picarx_simulation"]:
            print(f"  {key}: {config.get(key)}")
        
        print("\n✓ Configuration test complete")
        print("\nTo create a sample config file, run:")
        print("  python config.py create [filename]")
