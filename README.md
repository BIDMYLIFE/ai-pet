# AI Pet - Voice Assistant with PiCar-X Support

An interactive AI companion running on Raspberry Pi 5 with PiCar-X robot platform, featuring local LLM, speech recognition, and text-to-speech capabilities.

## Features

- 🎤 **Voice Interaction** - Speak to your AI pet and get responses
- 🤖 **Local LLM** - Runs Ollama locally (Gemma, TinyLlama, Phi-3)
- 🗣️ **Speech-to-Text** - Whisper.cpp for accurate transcription
- 🔊 **Text-to-Speech** - Piper TTS for natural voice output
- 🎨 **Animated Character** - Displays cute character animations
- 👤 **Face Recognition** - Recognizes and greets known users
- 🚗 **PiCar-X Integration** - Voice-controlled robot movements
- 💾 **Fully Local** - No cloud services required

## Hardware Support

- **Raspberry Pi 5** (4GB/8GB recommended)
- **PiCar-X Robot Platform** by SunFounder
- **USB Microphone** or I2S Microphone HAT
- **Speaker** (USB/Audio Jack/HAT)
- **Optional**: Camera module for face recognition

## Quick Start

### For Raspberry Pi 5 with PiCar-X:

See the comprehensive setup guide: [PICARX_SETUP.md](PICARX_SETUP.md)

### Basic Installation:

```bash
# Clone repository
git clone <repository-url> ai-pet
cd ai-pet

# Install dependencies
pip install -r requirements.txt

# Run setup script
bash install\ manual/setup.sh
```

### Run the Application:

```bash
# With PiCar-X support
cd stt/whisper.cpp/samples
python3 voice_loop_picarx.py

# Original version (no robot control)
python3 voice_loop3.py
```

## Documentation

- [PiCar-X Setup Guide](PICARX_SETUP.md) - Complete setup for Raspberry Pi 5 with PiCar-X
- [Installation Manual](install%20manual/install.md) - Basic installation instructions
- [Configuration Guide](stt/whisper.cpp/samples/config.py) - Configuration options

## Project Structure

```
ai-pet/
├── stt/whisper.cpp/
│   ├── samples/
│   │   ├── voice_loop_picarx.py  # Main app with PiCar-X
│   │   ├── voice_loop3.py        # Main app (original)
│   │   ├── picarx_control.py     # PiCar-X motor control
│   │   ├── config.py             # Configuration manager
│   │   ├── gui_frame.py          # Character animation
│   │   └── face_r.py             # Face recognition
│   └── piper/                    # TTS engine
├── requirements.txt               # Python dependencies
├── PICARX_SETUP.md               # Setup guide
└── README.md                     # This file
```

## Voice Commands

### Conversation
- Talk naturally to your AI pet
- Ask questions, chat, or seek companionship

### Movement (PiCar-X mode)
- "Move forward" / "Go ahead"
- "Move backward" / "Go back"
- "Turn left" / "Go left"
- "Turn right" / "Go right"
- "Stop"

### Gestures
- "Nod your head" (yes gesture)
- "Shake your head" (no gesture)

## Configuration

Create a `config.json` file to customize settings:

```bash
cd stt/whisper.cpp/samples
python3 config.py create config.json
# Edit config.json with your preferences
```

Key configuration options:
- `enable_picarx`: Enable/disable robot control
- `picarx_simulation`: Test without hardware
- `llm_model`: Choose LLM model (gemma2:2b, tinyllama, etc.)
- `audio_device`: Set microphone device

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Acknowledgments

- [Whisper.cpp](https://github.com/ggerganov/whisper.cpp) - Fast speech recognition
- [Ollama](https://ollama.com) - Local LLM runtime
- [Piper TTS](https://github.com/rhasspy/piper) - Neural text-to-speech
- [SunFounder PiCar-X](https://www.sunfounder.com/products/picar-x) - Robot platform
