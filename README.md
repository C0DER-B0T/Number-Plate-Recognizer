
# Indian Number Plate Recognizer (ANPR) Python=3.10

An Automatic Number Plate Recognition (ANPR) system tailored for **Indian vehicles**. It uses **YOLOv8** for detection, **SORT** for tracking, and **EasyOCR** for reading text.

Specialized logic is included to handle:
* **Standard Indian Plates** (e.g., `MH 20 DV 2366`)
* **BH (Bharat) Series Plates** (e.g., `22 BH 1234 XX`)

---

##  Features
* **Vehicle Detection:** Identifies Cars, Motorcycles, Buses, and Trucks.
* **License Plate Detection:** Crops and isolates plates from moving vehicles.
* **OCR & Formatting:** Reads text and autocorrects common errors (like `0` vs `O` or `5` vs `S`) based on Indian RTO formats.
* **Codespace Ready:** Optimized to run in "headless" environments (like GitHub Codespaces) without crashing.

##  Installation

**1. Clone the repository**
```bash
git clone [https://github.com/C0DER-B0T/Number-Plate-Recognizer.git](https://github.com/C0DER-B0T/Number-Plate-Recognizer.git)
cd Number-Plate-Recognizer

```

**2. Create a clean environment (Recommended)**

```bash
conda create -n proenv python=3.10 -c conda-forge -y
conda activate proenv

```

**3. Install dependencies**

```bash
# Install standard requirements
pip install -r requirements.txt

# Fix for "ImpImporter" or "AttributeError" issues in newer Python versions
pip install "Pillow==9.5.0"
pip install --upgrade ultralytics

```

**4. Install System Libraries (If using Linux/Codespaces)**

```bash
sudo apt-get update && sudo apt-get install ffmpeg libsm6 libxext6 -y

```

---

## How to Run

### Step 1: Detect & Read (The Brain)

This script processes the video, tracks vehicles, and saves the data to a CSV file.

```bash
python main.py

```

* **Input:** `sample.mp4`
* **Output:** `test.csv` (Contains frame numbers, IDs, and recognized text)

### Step 2: Generate Video (The Visuals)

This script draws the bounding boxes and text onto the video so you can see the results.

```bash
python visualize.py

```

* **Input:** `sample.mp4` + `test.csv`
* **Output:** `out.mp4`

> **Note:** If you are on Codespaces, right-click `out.mp4` in the file explorer and select **Download** to watch it.

---

## Project Structure

* `main.py`: Core logic. Loads YOLO models, runs the tracker, and saves CSV data.
* `util.py`: Helper functions. Contains the **Indian format validation** logic (`verify_format_bh`, `verify_format_standard`).
* `visualize.py`: Draws boxes and text on the video.
* `sort/`: Folder containing the SORT tracking algorithm.

## Common Issues & Fixes

* **"Encoder not found" / Video won't play:**
* The code uses `mp4v` codec by default to ensure it works on Linux servers. If it doesn't play on Windows, open it with VLC Media Player.


* **"AttributeError: module 'PIL.Image' has no attribute 'ANTIALIAS'":**
* Run `pip install "Pillow==9.5.0"`.



---
Made By ~[ Satyam Chandra AKA Coder bot](https://github.com/C0DER-B0T)

*Built with  using YOLOv8, OpenCV, and EasyOCR & big support of the GitHub Codespace.*
