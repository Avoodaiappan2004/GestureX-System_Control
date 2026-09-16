# GestureX 🖐️

### AI-Powered Touchless Computer and Game Controller

GestureX is a real-time hand gesture-based human-computer interaction system that allows users to control basic computer operations and browser games without continuously using a physical mouse or keyboard.

## 🎯 Problem Statement

Traditional computer interaction mainly depends on physical input devices such as a mouse, keyboard, or touchscreen.

In some situations, users may find physical interaction inconvenient or difficult. GestureX explores a touchless alternative by recognizing hand gestures through a webcam and converting them into computer actions.

## 💡 Features

* Real-time hand detection
* Hand gesture recognition
* Mouse movement using one finger
* Left click using thumbs up
* Right click using thumbs down
* Vertical and horizontal scrolling
* Game control using hand gestures
* Separate System Mode and Game Mode
* Multi-frame gesture confirmation
* Emergency stop using ESC
* Local processing without requiring an internet connection

## 🖐️ Gesture Mapping

| Gesture        | Action                       |
| -------------- | ---------------------------- |
| ☝️ One Finger  | Mouse Control                |
| ✌️ Two Fingers | Scroll                       |
| 👍 Thumbs Up   | Left Click / Game Action     |
| 👎 Thumbs Down | Right Click / Exit           |
| 🖐️ Open Palm  | Game Acceleration / Steering |
| ✊ Fist         | Stop / Brake                 |

## 🎮 Modes

### System Mode

Press:

```text
F1
```

System Mode allows gesture-based:

* Mouse movement
* Left click
* Right click
* Scrolling

### Game Mode

Press:

```text
F2
```

Game Mode converts gestures into keyboard controls.

### Emergency Stop

Press:

```text
ESC
```

This releases active game keys and stops the current control action.

### Exit

Press:

```text
Q
```

## 🧠 How It Works

```text
Webcam
   ↓
OpenCV
   ↓
MediaPipe Hands
   ↓
21 Hand Landmarks
   ↓
Gesture Detection
   ↓
Gesture State / Stabilization
   ↓
Action Mapping
   ↓
PyAutoGUI / Keyboard
   ↓
Computer or Game
```

## 🛠️ Technologies Used

* Python
* OpenCV
* MediaPipe
* NumPy
* PyAutoGUI
* Keyboard Library

## 📁 Project Structure

```text
GestureX/
│
├── src/
│   ├── gesture_detector.py
│   ├── gesture_state.py
│   ├── mouse_controller.py
│   ├── scroll_controller.py
│   ├── game_controller.py
│   └── system_control_test.py
│
├── requirements.txt
├── .gitignore
└── README.md
```

## ⚙️ Installation

Clone the repository:

```bash
git clone https://github.com/YOUR_USERNAME/GestureX.git
```

Open the project:

```bash
cd GestureX
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate it on Windows:

```powershell
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run GestureX:

```bash
python src/system_control_test.py
```

## ⚠️ Limitations

Recognition can be affected by:

* Poor lighting
* Hand occlusion
* Camera quality
* Very fast movements
* Hand orientation
* Distance from the camera

The system also depends on the user's ability to perform the predefined gestures.

## 🚀 Future Scope

* Personalized gesture calibration
* More customizable gestures
* Multi-hand interaction
* Voice + gesture hybrid control
* Adaptive sensitivity
* Mobile and IoT integration
* Additional computer-control functions

## 👨‍💻 Project

GestureX was developed as an AI and computer-vision based human-computer interaction project.
