# Installation Instructions for AI Pet Project

## Project Structure
The project is organized as follows:

```
ai-pet
├── stt
│   ├── whisper.cpp
│   │   └── samples
│   │       ├── voice_loop3.py
│   │       ├── face_r.py
|   |       └── gui_frame.py
|   |       
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
Before you begin, ensure you have the following installed on your system:
- Python 3.6 or higher
- Git
- A compatible audio recording device

### Step 1: Clone the Repository
Clone the project repository to your local machine using Git:

```bash
git clone <repository-url>
cd ai-pet
```

### Step 2: Install Dependencies
Install the required Python packages listed in `requirements.txt`. You can do this using pip:

```bash
pip install -r requirements.txt
```

### Step 3: Set Up Environment
Run the setup script to configure the environment and any necessary dependencies:

```bash
bash scripts/setup.sh
```

### Step 4: Configure Audio Device
Ensure that your audio recording device is properly configured. You may need to adjust the device settings in the `voice_loop3.py` script to match your hardware.

### Step 5: Run the Application
You can now run the application by executing the `voice_loop3.py` script:

```bash
python stt/whisper.cpp/samples/voice_loop3.py
```

### Additional Information
- Refer to `README.md` for more details on how to use the application and its features.
- If you encounter any issues, please check the `.gitignore` file to ensure that necessary files are not being ignored by Git.

## Conclusion
You are now ready to use the AI Pet project! Enjoy interacting with your friendly AI companion.