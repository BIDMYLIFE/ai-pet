import subprocess

PIPER_BIN = "/home/charles/voice-assisant/stt/whisper.cpp/piper/piper"
PIPER_MODEL = "models/en_US-lessac-medium.onnx"
PIPER_OUT = "tts.wav"
subprocess.run([PIPER_BIN, "--help"])
