import subprocess
import time
import os

MODEL = "tinyllama"
WAV_FILE = "test16k.wav"
TXT_FILE = "test16k.wav.txt"

def record_audio():
    subprocess.run([
        "arecord",
        "-D", "plughw:3,0",
        "-f", "cd",
        "-d", "5",  # record 5 seconds
        "-r","16000",
        "-c","1",
        WAV_FILE
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def run_stt():
    # REPLACE this with YOUR STT command if different
    subprocess.run([
        "../build/bin/whisper-cli",
        "-m", "../models/ggml-tiny.bin",
        "-f", WAV_FILE,
        "-otxt",
        "-nt",
        "-p", "1"
    ])

def speak(text):
    subprocess.run([
        "espeak-ng",
        "-v", "en-us",
        "-p", "48",
        "-s", "135",
        "-a", "130",
        text
    ])

print("🎤 Always listening... (Ctrl+C to stop)")

while True:
    print("\n🎙 Recording...")
    record_audio()

    print("📝 Transcribing...")
    run_stt()

    if not os.path.exists(TXT_FILE):
        print("❌ No STT output")
        continue

    with open(TXT_FILE, "r", encoding="utf-8") as f:
        user_text = f.read().strip()

    if len(user_text) < 2:
        print("🔇 Silence / noise detected")
        continue

    print("👤 User:", user_text)

    prompt = f"""
You are a helpful voice assistant running on a Raspberry Pi.
Reply briefly.

User: {user_text}
Assistant:
"""
    response='no content';
    if ("P" in user_text or "p" in user_text or "B" in user_text or "b" in user_text) and "BLANK_AUDIO" not in user_text:
        result = subprocess.run(
            #["ollama", "run", MODEL, "--max-tokens", "1024"],
            ["ollama", "run", MODEL],
            input=prompt,
            text=True,
            capture_output=True
    )
        response = result.stdout.strip()
        print("🤖 Assistant:", response)

        speak("".join(response.split()[:20]))

    time.sleep(0.5)

