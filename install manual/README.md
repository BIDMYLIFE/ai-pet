# AI Pet Project

## Overview
The AI Pet project is designed to create an interactive AI companion that can listen to user input, process speech-to-text, and respond using text-to-speech synthesis. The project utilizes various external tools and machine learning models to achieve its functionality.

## Project Structure
```
ai-pet
├── stt
│   ├── whisper.cpp
│   │   └── samples
│   │       ├── voice_loop3.py
│   │       └── gui_frame.py
│   └── piper
│       └── models
│           └── en_US-lessac-medium.onnx
├── scripts
│   └── setup.sh
├── requirements.txt
├── install.md
├── README.md
└── .gitignore
```

## Installation Instructions

### Prerequisites
- Ensure you have Python 3.6 or higher installed on your system.
- Install necessary system dependencies for audio recording and playback.

### Step 1: Clone the Repository
Clone the project repository to your local machine using the following command:
```
git clone <repository-url>
cd ai-pet
```

### Step 2: Install Dependencies
Install the required Python packages listed in `requirements.txt`:
```
pip install -r requirements.txt
```

### Step 3: Set Up Environment
Run the setup script to configure the environment:
```
bash scripts/setup.sh
```

### Step 4: Configure Audio Devices
Make sure your audio recording and playback devices are correctly configured. You may need to adjust the device settings in the `voice_loop3.py` script.

### Step 5: Run the Application
You can start the application by running the `voice_loop3.py` script:
```
python stt/whisper.cpp/samples/voice_loop3.py
```

## Usage
Once the application is running, it will continuously listen for audio input, transcribe it, and respond in a friendly manner. You can interact with the AI pet by speaking to it.

## Contributing
Contributions are welcome! Please feel free to submit a pull request or open an issue for any improvements or bug fixes.

## License
This project is licensed under the MIT License. See the LICENSE file for more details.