import subprocess

TEXT_FILE = "test16k.wav.txt"
MODEL = "tinyllama"

# read speech-to-text
with open(TEXT_FILE, "r", encoding="utf-8") as f:
    user_text = f.read().strip()

if not user_text:
    print("No text detected")
    exit(0)

print("User:", user_text)

# prompt for LLM
prompt = f"""
You are a helpful voice assistant running on a Raspberry Pi.
Reply briefly and clearly.

User: {user_text}
Ai:
"""

# run LLM
result = subprocess.run(
    ["ollama", "run", MODEL],
    input=prompt,
    text=True,
    capture_output=True
)

response = result.stdout.strip()
print("Assistant:", response)

# speak response
subprocess.run([
    "espeak-ng",
    "-p", "70",      #
    "-s", "145",      # speed
    "-v", "yue",       # voice
    "-a","165",
    "-g","2",
    response
])
