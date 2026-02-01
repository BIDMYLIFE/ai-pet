import subprocess
PIPER_MODEL = "/home/charles/voice-assisant/stt/whisper.cpp/piper/models/zh_CN-huayan-medium.onnx"
PIPER_BIN = "/home/charles/voice-assisant/stt/whisper.cpp/piper/piper"
text = "你好，我是你的语音助手。今天的天气很好。"

cmd = [
    PIPER_BIN,
    "--model", PIPER_MODEL,
    "--length_scale", "1.05",
    "--noise_scale", "0.4",
    "--noise_w", "0.8"
]


proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
audio, _ = proc.communicate(text.encode("utf-8"))  # UTF-8 required

# Play audio
subprocess.Popen(["aplay"], stdin=subprocess.PIPE).communicate(audio)