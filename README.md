# 🖼️ Image Converter with libwebp API Integration

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)](https://streamlit.io/)
[![License](https://img.shields.io/badge/License-GPLv3-blue.svg)](LICENSE)

A modern, web-based image converter built with Streamlit that uses the **libwebp C API directly** for WebP encoding and decoding. Convert between multiple image formats with support for lossy and lossless WebP compression.

## ✨ Features

- 🔌 **Direct libwebp API Integration**: Uses Python's `ctypes` to call libwebp C functions directly
- 🎨 **WebP Support**: Full support for WebP encoding (lossy and lossless) and decoding
- 🧪 **AVIF Support**: Advanced, high-efficiency AVIF image encoding via Pillow/`pillow-avif-plugin`
- 🎭 **SVG Support**: Vector SVG files can be rasterized and converted to raster formats
- 📸 **Multiple Formats**: Supports PNG, JPEG, JFIF, BMP, WebP, AVIF, and SVG
- ⚙️ **Quality Control**: Adjustable quality settings (0-100) for lossy formats
- 🎯 **Lossless Option**: Option for lossless WebP and AVIF encoding
- 🛠️ **Advanced Compression Tools**:
  - **MozJPEG**: For optimizing JPEG files when `cjpeg`/MozJPEG is available
  - **OxiPNG/OptiPNG**: For lossless PNG optimization when installed
  - **WebP (and future WebP v2)**: For modern, efficient lossy and lossless compression via libwebp/Pillow
- 🔄 **Automatic Fallback**: Falls back to Pillow's WebP support if libwebp is unavailable
- 🖥️ **Cross-Platform**: Works on Windows, Linux, and macOS
- 🎨 **Modern UI**: Clean, intuitive Streamlit interface
- 🛡️ **File Size Protection**: Enforces a 200MB maximum file size limit to prevent resource exhaustion

## 📋 Table of Contents

- [Installation](#-installation)
- [Usage](#-usage)
- [Project Structure](#-project-structure)
- [How It Works](#-how-it-works)
- [Troubleshooting](#-troubleshooting)
- [Technical Details](#-technical-details)
- [Contributing](#-contributing)
- [License](#-license)

## 🚀 Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/IMGCONVERTOR.git
cd IMGCONVERTOR
```

### Step 2: Install Python Dependencies

#### Option A: Development Installation (Recommended for Development)

```bash
pip install -r requirements.txt
```

This will install the minimum required versions and allow automatic updates for bug fixes and security patches.

#### Option B: Production Installation (Recommended for Production/Deployment)

```bash
pip install -r requirements-lock.txt
```

This installs exact pinned versions for reproducible builds and consistent environments across different machines.

**Which file to use?**
- **`requirements.txt`**: Use for development. Contains minimum version requirements (`>=`) allowing flexibility for updates.
- **`requirements-lock.txt`**: Use for production deployments. Contains exact pinned versions (`==`) ensuring everyone gets the same package versions.

**To regenerate `requirements-lock.txt`** (after updating dependencies):
```bash
pip freeze > requirements-lock.txt
```

**Dependencies installed:**
- `streamlit` (>=1.28.0) - Web interface
- `Pillow` (>=10.0.0) - Image processing
- `numpy` (>=1.24.0) - Array handling
- `pillow-avif-plugin` (>=1.4.6) - AVIF encoding/decoding support
- `svglib` (>=1.5.1) - SVG to ReportLab drawing conversion
- `reportlab` (>=4.0.0) - PDF rendering (no Cairo dependency)
- `pdf2image` (>=1.16.0) - PDF to image conversion

**Note for SVG support on Windows**: `pdf2image` requires `poppler` to be installed. See [pdf2image installation guide](https://github.com/Belval/pdf2image) for Windows setup instructions.

### Step 3: Install libwebp Library

The application requires the libwebp library to be installed on your system for direct API access. However, it will automatically fall back to Pillow's built-in WebP support if libwebp is not found.

#### Windows (Easiest Method)

**Option A: Automatic Setup Scripts**

Run one of these scripts in the project directory:

**PowerShell:**
```powershell
.\setup_libwebp.ps1
```

**Command Prompt:**
```cmd
setup_libwebp.bat
```

These scripts will automatically:
- Download libwebp from Google's servers
- Extract the files
- Copy `libwebp.dll` to your project folder
- Clean up temporary files

**Option B: Manual Installation**

1. Download libwebp from: [libwebp-1.2.1-windows-x64.zip](https://storage.googleapis.com/downloads.webmproject.org/releases/webp/libwebp-1.2.1-windows-x64.zip)
2. Extract the ZIP file
3. Copy `libwebp.dll` from the `bin` folder to:
   - The same directory as `app.py` (recommended), OR
   - `C:\Windows\System32\`, OR
   - Any directory in your system PATH

#### Linux

```bash
# Ubuntu/Debian
sudo apt-get install libwebp-dev

# Fedora
sudo dnf install libwebp-devel

# Arch Linux
sudo pacman -S libwebp

# openSUSE
sudo zypper install libwebp-devel
```

#### macOS

```bash
# Using Homebrew
brew install webp

# Using MacPorts
sudo port install libwebp
```

### Optional: Install External Optimization Tools

To enable advanced compression for JPEG and PNG, install:

- **MozJPEG** (`cjpeg` binary on PATH) – used for high-quality JPEG optimization
- **OxiPNG** (`oxipng` on PATH) – preferred PNG optimizer when available
- **OptiPNG** (`optipng` on PATH) – fallback PNG optimizer

If these tools are not installed, the app will still work and fall back to Pillow’s built-in optimizations.

### Optional: SVG Support Setup

SVG support requires `pdf2image` which needs `poppler` on Windows:

**Windows (Choose one method):**

**Method 1: Manual Installation (No Admin Required - Recommended)**
1. Download poppler for Windows from: https://github.com/oschwartz10612/poppler-windows/releases/
2. Extract the ZIP file to a location like `C:\Users\YourName\poppler` or `C:\poppler`
3. Add the `bin` folder to your user PATH:
   - Open PowerShell and run: `[Environment]::SetEnvironmentVariable("Path", $env:Path + ";C:\path\to\poppler\bin", "User")`
   - Replace `C:\path\to\poppler\bin` with your actual poppler bin folder path (e.g., `C:\poppler\Library\bin`)
   - Restart your terminal/IDE for the PATH change to take effect
   - Verify: Run `pdftoppm -h` in a new terminal window

**Method 2: Chocolatey (Requires Admin)**
1. Open PowerShell as Administrator (Right-click → Run as Administrator)
2. Run: `choco install poppler`

**Method 3: Scoop (No Admin Required)**
1. Install Scoop if you don't have it: https://scoop.sh/
2. Run: `scoop install poppler`

**Linux:**
```bash
sudo apt-get install poppler-utils  # Ubuntu/Debian
sudo dnf install poppler-utils      # Fedora
```

**macOS:**
```bash
brew install poppler
```

If poppler is not installed, SVG conversion will show a helpful error message. The app will still work for all other formats.

### Step 4: Verify Installation

Run the application and check the status indicator at the top of the page. It will show:
- ✅ **Available** - libwebp is detected and will be used
- ⚠️ **Not found** - Using Pillow fallback (still works, but not direct API)

## 💻 Usage

### Running the Application

```bash
streamlit run app.py
```

The application will automatically open in your default browser at `http://localhost:8501`

### Using the Image Converter

1. **Upload an Image**: Click "Upload an Image" and select a file (PNG, JPEG, JFIF, BMP, WebP, AVIF, or SVG)
   - **File Size Limit**: Maximum file size is **200MB** per file
   - Files exceeding this limit will be rejected with a clear error message
2. **Select Output Format**: Choose your desired output format from the dropdown
3. **Adjust Settings**:
   - **Quality**: Adjust the quality slider (0-100) for lossy formats
   - **Lossless**: Enable lossless encoding for WebP/AVIF output (checkbox)
   - **Advanced optimization**: Enable for PNG/JPEG to use MozJPEG/OxiPNG/OptiPNG (if available)
4. **Convert**: Click the "Convert 📸" button
5. **Download**: Click the download button to save your converted image

**Note**: SVG files are automatically rasterized before conversion to the selected format.

### Example Use Cases

- Convert PNG images to WebP for smaller file sizes
- Convert JPEG to WebP with lossless compression
- Batch convert images (upload multiple times)
- Optimize images for web use

## 📁 Project Structure

```
IMGCONVERTOR/
│
├── app.py                 # Main Streamlit application
├── imgconvrtr.py          # Image conversion module with libwebp integration
├── requirements.txt       # Python dependencies (minimum versions for development)
├── requirements-lock.txt  # Locked dependency versions (exact versions for production)
├── setup_libwebp.ps1      # PowerShell setup script for Windows
├── setup_libwebp.bat      # Batch setup script for Windows
├── README.md              # This file
│
└── libwebp.dll           # libwebp library (after setup, Windows only)
```

## 🔧 How It Works

### libwebp API Integration

The `imgconvrtr.py` module uses Python's `ctypes` library to directly call libwebp C functions:

#### Encoding Functions
- `WebPEncodeRGBA()`: Lossy RGBA to WebP encoding with quality control
- `WebPEncodeLosslessRGBA()`: Lossless RGBA to WebP encoding

#### Decoding Functions
- `WebPDecodeRGBA()`: WebP to RGBA decoding
- `WebPGetInfo()`: Get WebP image dimensions without full decoding

#### Memory Management
- `WebPFree()`: Properly frees memory allocated by libwebp

### Format Support

| Format | Input | Output | Method |
|--------|-------|--------|--------|
| AVIF   | ✅    | ✅     | Pillow + `pillow-avif-plugin` |
| WebP   | ✅    | ✅     | libwebp API (with Pillow fallback) |
| SVG    | ✅    | ❌     | svglib + reportlab (rasterized to other formats) |
| PNG    | ✅    | ✅     | Pillow (+ OxiPNG/OptiPNG when available) |
| JPEG   | ✅    | ✅     | Pillow (+ MozJPEG when available) |
| JFIF   | ✅    | ✅     | Pillow |
| BMP    | ✅    | ✅     | Pillow |

### Conversion Flow

1. **Input Processing**: Image is read and converted to RGBA format
2. **WebP Encoding**: If output is WebP, uses libwebp API (or Pillow fallback)
3. **WebP Decoding**: If input is WebP, uses libwebp API for decoding
4. **Format Conversion**: Other formats use Pillow for conversion
5. **Output**: Converted image is returned as BytesIO object

## 🐛 Troubleshooting

### libwebp Not Found

**Symptoms**: Status shows "⚠️ Not found (using Pillow fallback)"

**Solutions**:
1. **Check Diagnostic Information**: Expand the diagnostic section in the app to see what was tried
2. **Verify Installation**: Ensure libwebp is installed on your system
3. **Check File Location**: On Windows, ensure `libwebp.dll` is in the project folder or system PATH
4. **Use Setup Scripts**: Run `setup_libwebp.ps1` or `setup_libwebp.bat` for automatic setup
5. **Fallback Works**: The app will still work using Pillow's WebP support

### Conversion Errors

**"cannot identify image file" Error**:
- Ensure the uploaded file is a valid image format
- Check that the file is not corrupted
- Try converting the image with another tool first

**Memory Errors**:
- Reduce image size before conversion
- Close other applications to free up memory
- Try converting smaller images first

**Quality Issues**:
- Adjust quality settings (higher = better quality, larger file)
- Try lossless encoding for WebP if quality is critical
- For JPEG output, quality 85-95 is usually optimal

**File Size Limit Errors**:
- **Error**: "File size exceeds the maximum limit of 200MB"
- **Cause**: The uploaded file is larger than 200MB
- **Solutions**:
  - Compress or resize the image before uploading
  - Split large images into smaller files
  - Use image editing software to reduce file size
  - The 200MB limit helps prevent resource exhaustion and ensures smooth operation

### Platform-Specific Issues

**Windows**:
- Ensure you have the correct architecture (x64) version of libwebp
- Check that DLL dependencies are available (usually included)

**Linux**:
- Install development packages (`libwebp-dev` not just `libwebp`)
- Check library path: `ldconfig -p | grep webp`

**macOS**:
- Ensure Homebrew/MacPorts is up to date
- Check library location: `brew list webp`

## 🔬 Technical Details

### API Functions Used

| Function | Purpose | Parameters |
|----------|---------|------------|
| `WebPEncodeRGBA()` | Lossy encoding | RGBA data, dimensions, stride, quality |
| `WebPEncodeLosslessRGBA()` | Lossless encoding | RGBA data, dimensions, stride |
| `WebPDecodeRGBA()` | Decode WebP | WebP data, data size |
| `WebPGetInfo()` | Get dimensions | WebP data, data size |
| `WebPFree()` | Free memory | Pointer to allocated memory |

### Dependencies

#### Python Packages
- **streamlit**: Web framework for the user interface
- **Pillow**: Image processing library (handles non-WebP formats)
- **numpy**: Array operations for image data handling

#### System Libraries
- **libwebp**: C library for WebP operations (optional, with Pillow fallback)

### Performance Considerations

- **Direct libwebp API**: Faster encoding/decoding for WebP
- **Memory Usage**: Large images may require significant RAM
- **Quality vs Size**: Lower quality = smaller files but more compression artifacts
- **Lossless**: Larger files but perfect quality preservation
- **File Size Limit**: Maximum 200MB per file to prevent resource exhaustion and ensure system stability

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

### How to Contribute

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Development Setup

```bash
# Clone your fork
git clone https://github.com/yourusername/IMGCONVERTOR.git
cd IMGCONVERTOR

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

### Code Style

- Follow PEP 8 Python style guide
- Use meaningful variable names
- Add comments for complex logic
- Update documentation for new features

## 📄 License

This project is open source and available under the [GNU General Public License v3](LICENSE).

### Third-Party Licenses

- **libwebp**: Licensed under the [New BSD License](https://developers.google.com/speed/webp/license)
- **Streamlit**: Licensed under the [Apache License 2.0](https://github.com/streamlit/streamlit/blob/develop/LICENSE)
- **Pillow**: Licensed under the [HPND License](https://github.com/python-pillow/Pillow/blob/main/LICENSE)

## 🙏 Acknowledgments

- [Google's libwebp](https://developers.google.com/speed/webp) for the WebP library
- [Streamlit](https://streamlit.io/) for the web framework
- [Pillow](https://python-pillow.org/) for image processing capabilities

## 📞 Support

If you encounter any issues or have questions:

1. Check the [Troubleshooting](#-troubleshooting) section
2. Review the diagnostic information in the app
3. Open an [Issue](https://github.com/yourusername/IMGCONVERTOR/issues) on GitHub

---

Made with ❤️ using Streamlit and libwebp
