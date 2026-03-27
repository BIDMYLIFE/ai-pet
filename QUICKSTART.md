# Quick Start Guide - AI Pet on PiCar-X

Get your AI Pet robot up and running in minutes!

## Prerequisites Checklist

Before starting, ensure you have:

- [ ] Raspberry Pi 5 with Raspberry Pi OS (64-bit) installed
- [ ] PiCar-X assembled and servos calibrated
- [ ] USB microphone connected and working
- [ ] Speaker connected (USB or 3.5mm jack)
- [ ] Internet connection (for initial setup only)

## Fast Setup (30 minutes)

### 1. Install System Dependencies (5 min)
```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3-pip git build-essential cmake alsa-utils \
    pulseaudio-utils pipewire-audio-client-libraries sox ffmpeg
```

### 2. Clone and Setup Repository (2 min)
```bash
cd ~
git clone https://github.com/BIDMYLIFE/ai-pet.git
cd ai-pet
pip3 install -r requirements.txt
```

### 3. Build Whisper.cpp (5 min)
```bash
cd ~/ai-pet/stt/whisper.cpp
mkdir -p build && cd build
cmake .. && make -j4
cd .. && bash ./models/download-ggml-model.sh tiny
```

### 4. Install Piper TTS (3 min)
```bash
cd ~/ai-pet/stt/whisper.cpp
mkdir -p piper && cd piper

# Download for ARM64
wget https://github.com/rhasspy/piper/releases/download/v1.2.0/piper_arm64.tar.gz
tar -xzf piper_arm64.tar.gz && chmod +x piper

# Download voice model
mkdir -p models && cd models
wget https://huggingface.co/rhasspy/piper-voices/resolve/main/en/en_US/lessac/medium/en_US-lessac-medium.onnx
wget https://huggingface.co/rhasspy/piper-voices/resolve/main/en/en_US/lessac/medium/en_US-lessac-medium.onnx.json
```

### 5. Install Ollama and Model (10 min)
```bash
# Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Pull a lightweight model (choose one)
ollama pull gemma2:2b    # Recommended (2GB, good quality)
# OR
ollama pull tinyllama    # Faster but lower quality
```

### 6. Install PiCar-X Libraries (3 min)
```bash
cd ~
git clone https://github.com/sunfounder/robot-hat.git
cd robot-hat && sudo python3 setup.py install

cd ~
git clone https://github.com/sunfounder/picar-x.git
cd picar-x && sudo python3 setup.py install

# Calibrate servos (IMPORTANT!)
cd ~/picar-x
sudo python3 examples/calibration.py
```

### 7. Configure Audio (2 min)
```bash
# Find your microphone device
arecord -l

# Test recording
arecord -D hw:X,0 -f S16_LE -r 16000 -d 3 test.wav
aplay test.wav

# If it works, note the device ID (hw:X,0)
```

### 8. Create Configuration File (1 min)
```bash
cd ~/ai-pet/stt/whisper.cpp/samples
python3 config.py create config.json

# Edit config.json and update:
nano config.json
```

Update these essential settings:
```json
{
  "audio_device": "hw:2,0",        # Your microphone device
  "enable_picarx": true,           # Enable robot control
  "picarx_simulation": false,      # Set false for real hardware
  "llm_model": "gemma2:2b"        # Your chosen model
}
```

## Running Your AI Pet

### Option 1: Full Featured (with Safety)
```bash
cd ~/ai-pet/stt/whisper.cpp/samples
python3 voice_loop_safe.py
```

### Option 2: Basic PiCar-X Support
```bash
cd ~/ai-pet/stt/whisper.cpp/samples
python3 voice_loop_picarx.py
```

### Option 3: No Robot (Voice Only)
```bash
cd ~/ai-pet/stt/whisper.cpp/samples
python3 voice_loop3.py
```

## First Interaction

Once running, you should see:
```
🎤 AI Pet with PiCar-X ready! (Ctrl+C to stop)
   LLM Model: gemma2:2b
   PiCar-X: Enabled
   Mode: Hardware
   Safety: Enabled

🎙  Recording...
```

**Try saying:**
- "Hello!" (basic greeting)
- "How are you today?" (conversation)
- "Move forward" (robot movement)
- "Turn left" (steering)
- "Stop" (halt movement)

## Troubleshooting

### "No audio device found"
```bash
# Check USB microphone is connected
lsusb

# Re-scan audio devices
sudo alsactl init

# Try different device ID in config.json
```

### "Ollama connection failed"
```bash
# Check Ollama is running
sudo systemctl status ollama

# Start it if needed
sudo systemctl start ollama

# Test manually
ollama run gemma2:2b
```

### "PiCar-X not responding"
```bash
# Re-calibrate servos
cd ~/picar-x
sudo python3 examples/calibration.py

# Check I2C connection
sudo i2cdetect -y 1
```

### "Slow response times"
- Use a smaller model: `ollama pull tinyllama`
- Update config.json: `"llm_model": "tinyllama"`
- Add cooling fan to Raspberry Pi
- Close other applications

## Testing in Simulation Mode

Test everything without hardware:
```json
{
  "enable_picarx": true,
  "picarx_simulation": true
}
```

Run:
```bash
python3 voice_loop_safe.py
```

You'll see `[SIM]` tags showing simulated movements.

## Performance Tips

1. **Best Model Choice for Pi 5:**
   - 8GB RAM: gemma2:2b or phi3:mini
   - 4GB RAM: tinyllama

2. **Speed Up Response:**
   - Keep model in memory: `ollama run gemma2:2b &`
   - Overclock Pi 5 (with cooling)
   - Use faster SD card

3. **Improve Audio Quality:**
   - Use higher quality USB microphone
   - Adjust recording volume with `alsamixer`
   - Test in quiet environment

## Next Steps

- Read full documentation: [PICARX_SETUP.md](PICARX_SETUP.md)
- Customize personality in `voice_loop_safe.py` (lines 95-108)
- Adjust safety distances in `safety.py` (lines 30-31)
- Add face recognition: run `face_r.py` first to train faces
- Set up auto-start on boot (see PICARX_SETUP.md)

## Safety Reminders

⚠️ **Before running with real hardware:**
1. Test in simulation mode first
2. Clear 2 meters of space around robot
3. Keep emergency stop ready (Ctrl+C)
4. Monitor battery voltage
5. Never leave unattended

## Getting Help

- Full setup guide: `PICARX_SETUP.md`
- Test individual components:
  - `python3 picarx_control.py` (test motors)
  - `python3 safety.py` (test safety system)
  - `python3 config.py` (test configuration)

Happy building! 🤖✨
