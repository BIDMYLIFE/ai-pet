# AI Pet Setup Guide for Raspberry Pi 5 with PiCar-X

This guide covers the complete setup of the AI Pet project on a Raspberry Pi 5 with PiCar-X robot platform, including local LLM integration.

## Table of Contents
1. [Hardware Requirements](#hardware-requirements)
2. [Software Prerequisites](#software-prerequisites)
3. [Installation Steps](#installation-steps)
4. [Configuration](#configuration)
5. [Running the Application](#running-the-application)
6. [Troubleshooting](#troubleshooting)

## Hardware Requirements

### Required Hardware
- **Raspberry Pi 5** (4GB or 8GB RAM recommended)
- **PiCar-X Robot Kit** by SunFounder
  - Includes motors, servos, camera mount
  - Ultrasonic sensor for collision detection
- **USB Microphone** or **I2S Microphone HAT**
- **Speaker** (USB or via audio jack/HAT)
- **MicroSD Card** (32GB+ recommended)
- **Power Supply** for Raspberry Pi 5 (5V 5A USB-C recommended)
- **Battery Pack** for PiCar-X (7.4V LiPo recommended)

### Optional Hardware
- **Raspberry Pi Camera Module** (for face recognition)
- **LCD Display** (for character animations)
- **Cooling Fan/Heatsink** (recommended for LLM inference)

## Software Prerequisites

### 1. Operating System
Install **Raspberry Pi OS (64-bit)** - Bookworm or later recommended
```bash
# Use Raspberry Pi Imager to flash the SD card
# Enable SSH and configure Wi-Fi during setup
```

### 2. System Updates
```bash
sudo apt update && sudo apt upgrade -y
```

### 3. Install System Dependencies
```bash
# Audio tools
sudo apt install -y alsa-utils pulseaudio-utils pipewire-audio-client-libraries

# Build tools
sudo apt install -y build-essential cmake git

# Python and development tools
sudo apt install -y python3 python3-pip python3-dev python3-venv

# Audio/video libraries
sudo apt install -y sox ffmpeg libportaudio2

# GUI support
sudo apt install -y python3-tk

# Camera support (if using camera)
sudo apt install -y libcamera-dev libopencv-dev
```

## Installation Steps

### Step 1: Clone the Repository
```bash
cd ~
git clone <repository-url> ai-pet
cd ai-pet
```

### Step 2: Install Python Dependencies
```bash
# Create virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate

# Install Python packages
pip install -r requirements.txt
```

### Step 3: Install Whisper.cpp (Speech-to-Text)
```bash
cd ~/ai-pet/stt/whisper.cpp

# Build Whisper.cpp
mkdir -p build
cd build
cmake ..
make -j4

# Download Whisper model
cd ..
bash ./models/download-ggml-model.sh tiny
```

### Step 4: Install Piper TTS (Text-to-Speech)
```bash
cd ~/ai-pet/stt/whisper.cpp

# Download Piper binary
mkdir -p piper
cd piper
wget https://github.com/rhasspy/piper/releases/download/v1.2.0/piper_arm64.tar.gz
tar -xzf piper_arm64.tar.gz
chmod +x piper

# Download voice model
mkdir -p models
cd models
wget https://huggingface.co/rhasspy/piper-voices/resolve/main/en/en_US/lessac/medium/en_US-lessac-medium.onnx
wget https://huggingface.co/rhasspy/piper-voices/resolve/main/en/en_US/lessac/medium/en_US-lessac-medium.onnx.json
```

### Step 5: Install Ollama (Local LLM)
```bash
# Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Start Ollama service
sudo systemctl enable ollama
sudo systemctl start ollama

# Pull a lightweight model suitable for Raspberry Pi 5
ollama pull gemma2:2b
# or for even lighter option:
ollama pull tinyllama
```

**Recommended models for Raspberry Pi 5:**
- `gemma2:2b` - Good balance (2GB RAM, ~8 tokens/sec)
- `tinyllama` - Fastest (637MB RAM, ~15 tokens/sec)
- `phi3:mini` - Higher quality (2.3GB RAM, ~6 tokens/sec)

### Step 6: Install PiCar-X Software
```bash
# Install robot-hat library
cd ~
git clone https://github.com/sunfounder/robot-hat.git
cd robot-hat
sudo python3 setup.py install

# Install PiCar-X library
cd ~
git clone https://github.com/sunfounder/picar-x.git
cd picar-x
sudo python3 setup.py install

# Calibrate servos (important!)
cd ~/picar-x
sudo python3 examples/calibration.py
```

### Step 7: Configure Audio Devices
```bash
# List audio devices
arecord -l
aplay -l

# Test microphone
arecord -D hw:2,0 -f S16_LE -r 16000 -d 5 test.wav
aplay test.wav

# Adjust microphone volume
alsamixer
```

**Note**: Update the `audio_device` in `config.json` to match your hardware device ID.

## Configuration

### Create Configuration File
```bash
cd ~/ai-pet/stt/whisper.cpp/samples
python3 config.py create config.json
```

### Edit config.json
```json
{
  "base_dir": "/home/pi/ai-pet",
  "whisper_cli": "/home/pi/ai-pet/stt/whisper.cpp/build/bin/whisper-cli",
  "piper_bin": "/home/pi/ai-pet/stt/whisper.cpp/piper/piper",
  "piper_model": "/home/pi/ai-pet/stt/whisper.cpp/piper/models/en_US-lessac-medium.onnx",
  "whisper_model": "../models/ggml-tiny.bin",
  
  "llm_model": "gemma2:2b",
  "llm_backend": "ollama",
  
  "audio_device": "hw:2,0",
  "playback_device": "plughw:0,0",
  
  "enable_picarx": true,
  "picarx_simulation": false,
  "enable_movement_commands": true,
  
  "default_greeting": "Hello! I'm Pickcu, your AI pet robot!"
}
```

### Simulation Mode
To test without PiCar-X hardware:
```json
{
  "enable_picarx": true,
  "picarx_simulation": true
}
```

## Running the Application

### Run with PiCar-X Integration
```bash
cd ~/ai-pet/stt/whisper.cpp/samples
python3 voice_loop_picarx.py
```

### Run Original Version (No PiCar-X)
```bash
python3 voice_loop3.py
```

### Test Individual Components

**Test PiCar-X Control:**
```bash
python3 picarx_control.py
```

**Test Configuration:**
```bash
python3 config.py
```

**Test LLM:**
```bash
ollama run gemma2:2b
```

## Voice Commands

### Conversation Commands
- General conversation with AI pet personality
- Ask about your day, mood, etc.

### Movement Commands (when PiCar-X enabled)
- "Move forward" / "Go ahead"
- "Move backward" / "Go back"
- "Turn left" / "Go left"
- "Turn right" / "Go right"
- "Stop" / "Halt"

### Gesture Commands
- "Nod your head" (yes gesture)
- "Shake your head" (no gesture)

## Troubleshooting

### Audio Issues
**Problem**: No audio recording
```bash
# Check device permissions
sudo usermod -a -G audio $USER
# Reboot required after group change

# Test audio directly
arecord -D hw:2,0 -f S16_LE -r 16000 -d 5 test.wav
```

### PiCar-X Issues
**Problem**: Motors not responding
```bash
# Re-run calibration
cd ~/picar-x
sudo python3 examples/calibration.py

# Check I2C
sudo i2cdetect -y 1
```

**Problem**: Import error for picarx
```bash
# Reinstall libraries
cd ~/robot-hat
sudo python3 setup.py install --force

cd ~/picar-x
sudo python3 setup.py install --force
```

### LLM Issues
**Problem**: Ollama not responding
```bash
# Check Ollama service
sudo systemctl status ollama

# Restart service
sudo systemctl restart ollama

# Check if model is downloaded
ollama list
```

**Problem**: Slow inference
- Use a smaller model (tinyllama)
- Add active cooling for Raspberry Pi 5
- Close other applications
- Consider overclocking (with proper cooling)

### Whisper Issues
**Problem**: Whisper binary not found
```bash
# Rebuild Whisper.cpp
cd ~/ai-pet/stt/whisper.cpp/build
rm -rf *
cmake ..
make -j4
```

### Permission Issues
```bash
# Add user to required groups
sudo usermod -a -G audio,video,i2c,gpio $USER

# Set up GPIO permissions
sudo chgrp gpio /dev/gpiomem
sudo chmod g+rw /dev/gpiomem
```

## Performance Tips

1. **Use 64-bit OS** - Better performance for LLM inference
2. **Active Cooling** - Prevents thermal throttling during LLM inference
3. **Lightweight Model** - Start with tinyllama or gemma2:2b
4. **Overclock** (optional):
   ```bash
   # Edit /boot/firmware/config.txt
   # Add: over_voltage=6
   # Add: arm_freq=2600
   ```
5. **Disable GUI** if running headless:
   ```bash
   sudo systemctl set-default multi-user.target
   ```

## Auto-Start on Boot

Create systemd service:
```bash
sudo nano /etc/systemd/system/ai-pet.service
```

Add content:
```ini
[Unit]
Description=AI Pet Voice Assistant
After=network.target ollama.service

[Service]
Type=simple
User=pi
WorkingDirectory=/home/pi/ai-pet/stt/whisper.cpp/samples
Environment="PATH=/home/pi/ai-pet/venv/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
ExecStart=/home/pi/ai-pet/venv/bin/python3 voice_loop_picarx.py
Restart=on-failure
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable service:
```bash
sudo systemctl enable ai-pet.service
sudo systemctl start ai-pet.service
```

## Safety Notes

1. **Test in simulation mode first** before enabling hardware
2. **Clear workspace** - Ensure PiCar-X has room to move
3. **Emergency stop** - Keep Ctrl+C ready or add physical kill switch
4. **Battery monitoring** - Monitor battery voltage to prevent damage
5. **Supervision** - Always supervise robot operation

## Additional Resources

- [Raspberry Pi Documentation](https://www.raspberrypi.com/documentation/)
- [PiCar-X Documentation](https://docs.sunfounder.com/projects/picar-x/en/latest/)
- [Ollama Documentation](https://github.com/ollama/ollama)
- [Whisper.cpp](https://github.com/ggerganov/whisper.cpp)
- [Piper TTS](https://github.com/rhasspy/piper)

## Support

For issues specific to:
- **PiCar-X**: SunFounder support forums
- **Raspberry Pi**: Raspberry Pi forums
- **This project**: Open an issue in the repository

---

**Enjoy your AI Pet on PiCar-X! 🤖🎉**
