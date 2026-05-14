# Smart CCTV

A simple AI-powered CCTV script that uses your laptop webcam to detect and recognize faces in real-time. It identifies known faces and alerts you when an unknown person is detected, saving a snapshot of the intruder.

## Features

- Real-time face detection and recognition using a webcam.
- Identifies authorized people based on a directory of known faces.
- Detects "UNKNOWN" faces, highlights them in red, and logs a warning.
- Automatically captures and saves photos of intruders to a `captures` directory.
- Built-in rate limiting prevents spamming alerts (maximum one alert per 10 seconds per location).

## Installation

1. Create and activate a Python virtual environment:

    ```bash
    python -m venv venv
    source venv/bin/activate
    ```

2. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```
    _Note: This project pins `setuptools<81` due to a deprecated `pkg_resources` dependency in `face_recognition_models`._

## Usage

1. **Add Known Faces:**
   Place images of authorized people into the `known_faces/` directory. The name of the file (e.g., `john_doe.jpg`) will be used as the person's label on the camera feed.

2. **Verify Known Faces (Optional):**
   You can run the helper script to ensure the faces in your known directory are successfully detected:

    ```bash
    python known.py
    ```

3. **Start the CCTV:**
   Run the main script to activate your webcam and start monitoring:

    ```bash
    python main.py
    ```

4. **Quit:**
   Press the `q` key while focused on the video window to stop the program and close the camera.

## Project Structure

- `main.py`: The primary script that captures video, processes faces, and triggers alerts.
- `known.py`: A utility script to verify that images in the known faces folder contain readable encodings.
- `known_faces/`: Directory where you store images of authorized people.
- `captures/`: Directory where the script automatically saves images of unrecognized faces.
- `requirements.txt`: Python package dependencies.
