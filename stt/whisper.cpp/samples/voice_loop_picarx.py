"""
AI Pet Voice Loop with PiCar-X Integration
Main application for Raspberry Pi 5 with PiCar-X robot platform and local LLM
"""
import subprocess
import time
import os
from gui_frame import show_init_frame
from config import get_config
from picarx_control import PiCarXController, parse_movement_command


def record_audio(config):
    """Record audio using arecord"""
    subprocess.run([
        "arecord",
        "-D", config.get("audio_device"),
        "-f", config.get("audio_format"),
        "-r", str(config.get("audio_rate")),
        "-c", str(config.get("audio_channels")),
        "-d", str(config.get("record_duration")),
        config.get("wav_file")
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def run_stt(config):
    """Run speech-to-text transcription using Whisper"""
    whisper_cli = config.get_absolute_path("whisper_cli")
    if not whisper_cli or not os.path.exists(whisper_cli):
        # Try default build location
        whisper_cli = "/home/charles/ai-pet/stt/whisper.cpp/build/bin/whisper-cli"
    
    whisper_model = config.get("whisper_model")
    
    subprocess.run([
        whisper_cli,
        "-m", whisper_model,
        "-f", config.get("wav_file"),
        "-otxt",
        "-nt",
        "-p", "1",
        "-l", "en"
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def clean_text(text, max_words=100):
    """Clean and truncate text for TTS"""
    text = text.replace("\n", " ").replace("Assistant:", "").replace("😊", "").strip()
    return " ".join(text.split()[:max_words])


def speak(text, config):
    """Convert text to speech and play it"""
    text = clean_text(text)
    if not text:
        return

    piper_bin = config.get_absolute_path("piper_bin")
    if not piper_bin or not os.path.exists(piper_bin):
        # Try default location
        piper_bin = "/home/charles/ai-pet/stt/whisper.cpp/piper/piper"
    
    piper_model = config.get_absolute_path("piper_model")
    if not piper_model or not os.path.exists(piper_model):
        # Try default location
        piper_model = "/home/charles/ai-pet/stt/whisper.cpp/piper/models/en_US-lessac-medium.onnx"
    
    piper_out = config.get("piper_out")

    # Generate speech with Piper
    p = subprocess.Popen(
        [
            piper_bin,
            "--model", piper_model,
            "--output_file", piper_out
        ],
        stdin=subprocess.PIPE,
        text=True
    )
    p.communicate(text)

    # Play audio
    subprocess.run(
        ["pw-play", piper_out],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )


def get_llm_response(user_text, config):
    """Get response from local LLM"""
    prompt = f"""
You are Pickcu, a friendly, playful AI pet robot on a PiCar-X platform. 
Speak in a cheerful, gentle tone, sometimes using short playful expressions like "Purr~" or "Chirp!". 
Keep replies short, warm, and comforting. 
Ask the user questions about their day or mood occasionally. 
Do not give long technical explanations unless asked. 
Your personality is cute, curious, and supportive.

If the user asks you to move or perform actions (like "move forward", "turn left", "nod"), 
acknowledge the command in your response with enthusiasm.

User: {user_text}
Pickcu:
"""

    result = subprocess.run(
        ["ollama", "run", config.get("llm_model")],
        input=prompt,
        text=True,
        capture_output=True
    )

    return result.stdout.strip()


def execute_movement_command(text, controller):
    """Parse and execute movement commands"""
    command = parse_movement_command(text)
    
    if not command:
        return False
    
    action = command.get("action")
    
    if action == "forward":
        controller.forward(duration=command.get("duration", 2.0))
    elif action == "backward":
        controller.backward(duration=command.get("duration", 2.0))
    elif action == "turn_left":
        controller.turn_left(duration=command.get("duration", 1.5))
    elif action == "turn_right":
        controller.turn_right(duration=command.get("duration", 1.5))
    elif action == "stop":
        controller.stop()
    elif action == "nod":
        controller.nod(times=command.get("times", 2))
    elif action == "shake_head":
        controller.shake_head(times=command.get("times", 2))
    else:
        return False
    
    return True


def main():
    """Main application loop"""
    # Load configuration
    config = get_config()
    
    # Initialize PiCar-X controller if enabled
    picarx_controller = None
    if config.get("enable_picarx"):
        picarx_controller = PiCarXController(
            simulation_mode=config.get("picarx_simulation")
        )
    
    print("🎤 AI Pet with PiCar-X ready! (Ctrl+C to stop)")
    print(f"   LLM Model: {config.get('llm_model')}")
    print(f"   PiCar-X: {'Enabled' if config.get('enable_picarx') else 'Disabled'}")
    if config.get('enable_picarx'):
        print(f"   Mode: {'Simulation' if config.get('picarx_simulation') else 'Hardware'}")
    print()

    try:
        while True:
            # Prepare greeting
            greeting = config.get("default_greeting")
            try:
                watch_file = config.get("watch_file")
                if watch_file and os.path.exists(watch_file):
                    with open(watch_file, "r", encoding="utf-8") as wf:
                        content = wf.read().strip()
                        if content:
                            greeting = f"Hi, {content}"
            except Exception:
                pass

            # Show idle animation and greet
            show_init_frame(
                gif_path=config.get("character_idle"),
                display_time_ms=config.get("display_time_ms"),
                frame_delay_ms=config.get("frame_delay_ms")
            )
            speak(greeting, config)
            
            # Record audio
            print("\n🎙  Recording...")
            record_audio(config)
            
            # Transcribe
            print("📝 Transcribing...")
            run_stt(config)

            txt_file = config.get("txt_file")
            if not os.path.exists(txt_file):
                print("❌ No STT output")
                continue

            with open(txt_file, "r", encoding="utf-8") as f:
                user_text = f.read().strip()

            if len(user_text) < 2:
                print("🔇 Silence / noise detected")
                continue

            print("👤 User:", user_text)

            # Skip if blank/noise markers
            if "BLANK_AUDIO" in user_text or "[" in user_text or "]" in user_text:
                continue

            # Get LLM response
            response = get_llm_response(user_text, config)
            print("🤖 Pickcu:", response)
            
            # Show talking animation
            show_init_frame(
                gif_path=config.get("character_talking"),
                display_time_ms=config.get("display_time_ms"),
                frame_delay_ms=config.get("frame_delay_ms")
            )
            
            # Speak response
            speak(response, config)
            
            # Execute movement commands if enabled
            if picarx_controller and config.get("enable_movement_commands"):
                # Check both user command and LLM response for movement keywords
                executed = execute_movement_command(user_text, picarx_controller)
                if not executed:
                    execute_movement_command(response, picarx_controller)

            time.sleep(0.5)
            
    except KeyboardInterrupt:
        print("\n\n👋 Shutting down AI Pet...")
    finally:
        if picarx_controller:
            picarx_controller.cleanup()
        print("✓ Goodbye!")


if __name__ == "__main__":
    main()
