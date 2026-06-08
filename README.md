# 🔐 StegaVault — Multi-Modal Steganography System

StegaVault is a premium, high-security, multi-modal steganography application designed to hide sensitive payload data (Text, Images, or Audio) inside various carrier files (Images, Audio, or Video). To guarantee complete confidentiality, it features built-in AES-256 encryption.

The user interface is powered by a custom dark-themed Streamlit design with glassmorphic elements, modern typography, and clean layouts.

---

## 🌟 Key Features

- **Multi-Modal Capabilities**: Support for multiple steganographic carrier/payload combinations:
  - **Text / Image / Audio** payloads.
  - **Image** carrier (using PNG/BMP LSB encoding).
  - **Audio** carrier (using WAV LSB encoding with sample-width-aware packing).
  - **Video** carrier (using frame-by-frame LSB encoding, preserved losslessly using the `FFV1` codec inside an AVI wrapper).
- **AES-256 Encryption (Optional)**: Secures the hidden payload prior to embedding. Keys are derived from user-specified passwords using **SHA-256**, and payloads are encrypted using **AES-256-CBC** with PKCS7 padding.
- **Automatic Capacity Verification**: Real-time capacity computation checks the carrier size against the payload size before encoding, warning users if the data exceeds the maximum embeddable limits.
- **Visual Validation**: Side-by-side rendering comparing the original carrier image and the generated stego image to verify imperceptibility.
- **Clean Extracted Output**: Automatically recognizes payload data types (Text, Image, Audio) and provides direct inline preview and download options.

---

## 📐 System Architecture

StegaVault is organized into a modular structure separating UI components from the underlying steganography engine:

```
Steganography/
├── app.py                  # Streamlit entry point, layout, and page routing
├── requirements.txt        # Package dependencies
├── core/
│   ├── __init__.py
│   ├── engine.py           # Unified encoding/decoding orchestrator
│   ├── crypto.py           # AES-256 encryption/decryption utilities
│   ├── image_steg.py       # LSB image embedding and recovery
│   ├── audio_steg.py       # LSB audio sample manipulation
│   ├── video_steg.py       # LSB video frame manipulation via OpenCV
│   └── utils.py            # Binary parsing and header preparation helper functions
└── ui/
    ├── __init__.py
    └── styles.py           # Custom CSS styling (dark glassmorphism, badges, banners)
```

---

## 📥 Steganography Headers & Protocol

To allow automated extraction without prior knowledge of the data size or format, StegaVault embeds a **40-bit custom metadata header** at the start of every stego carrier:

| Component | Offset (Bits) | Description |
|---|---|---|
| **Data Type** | `0 - 7` (8 bits) | Identifies payload type: `0x01` = Text, `0x02` = Image, `0x03` = Audio. |
| **Payload Length** | `8 - 39` (32 bits) | Unsigned integer specifying the payload size in bytes. |
| **Encrypted Payload** | `40+` (variable) | The actual text, image, or audio bytes (potentially AES-256 encrypted). |

---

## 🛠️ Carrier Modules & Tech Stack

### 1. Image Carrier (`core/image_steg.py`)
- Standard LSB (Least Significant Bit) replacement on RGB channels of flat pixel arrays.
- High capacity carrier.
- Uses `PIL` and `NumPy` for efficient flattening and reshaping of image channels.

### 2. Audio Carrier (`core/audio_steg.py`)
- LSB replacement within raw audio samples.
- Supports both **8-bit unsigned** and **16-bit signed** WAV formats.
- Correctly handles negative values in 16-bit audio to prevent distortion or noise issues during playback.

### 3. Video Carrier (`core/video_steg.py`)
- Performs frame-by-frame steganography across pixel channels.
- Employs the **FFV1** video codec, a lossless intra-frame compression standard, ensuring that normal video compression doesn't destroy the payload bits.
- Powered by OpenCV (`cv2`) for frame retrieval, packing, and reassembly.

### 4. Cryptography (`core/crypto.py`)
- Derives a 256-bit key from user input via **SHA-256**.
- Uses a cryptographically secure random **16-byte Initialization Vector (IV)** for AES CBC mode.
- Output byte layout: `IV (16 bytes)` followed by the `Ciphertext`.

---

## 🚀 Installation & Setup

Ensure you have **Python 3.8+** installed.

### 1. Clone the Repository
```bash
git clone https://github.com/A-RYAN-KR/Steganography.git
cd Steganography
```

### 2. Set Up a Virtual Environment (Recommended)
```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the Streamlit Application
```bash
streamlit run app.py
```
Open [http://localhost:8501](http://localhost:8501) in your browser to start hiding your secrets.

---

## 📦 Dependencies

The application relies on the following packages:
- `streamlit` — Frontend interactive dashboard framework.
- `numpy` — Array manipulations for images and video frames.
- `opencv-python` — Lossless frame extraction and compilation.
- `Pillow` — Image loading, conversion, and metadata processing.
- `pydub` — Audio file loading and format conversions.
- `pycryptodome` — AES-256-CBC implementation.

---

## 🔒 Security Notice

StegaVault is designed to hide information visually and acoustically (steganography) alongside strong cryptographic protection. Please note that LSB-based steganography is vulnerable to carrier transformation (resizing, lossy compression, file conversion). Always share the stego carrier in its original format (e.g., `.png` for images, `.wav` for audio, and `.avi` with `FFV1` for video) to avoid destroying the embedded payload.

---

## 📝 License

This project is licensed under the MIT License.
