## Installation Guide

### 1. Installing FFmpeg

This tool requires **FFmpeg** to convert video and audio formats. You can install FFmpeg easily using Chocolatey on Windows:

1. Open **PowerShell** as Administrator.  
2. Run the following command to install Chocolatey (if you don't have it yet):

```powershell
Set-ExecutionPolicy Bypass -Scope Process -Force; `
[System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; `
iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
```

3. After Chocolatey is installed, install FFmpeg by running:

```powershell
choco install ffmpeg -y
```

4. Close and reopen your terminal or PowerShell, then verify the installation by typing:

```powershell
ffmpeg -version
```

If the version information is displayed, FFmpeg is installed correctly.

---

### 2. Installing Python dependencies

Make sure you have Python 3.7 or later installed. Then install required Python packages with:

```bash
pip install -r requirements.txt
```

---

### 3. Using the y2b tool

Run the tool using:

```bash
python y2b.py -mp3 [YouTube URL]
python y2b.py -mp4 -p720 [YouTube URL]
python y2b.py -mp4 [YouTube URL]  # defaults to 1080p if quality is not specified
```
there is a option, p1080(1080p),p720(720p),p480(480p),p360(360p)
---

### 4. Building executable (optional)

If you want to build a standalone `.exe` file, use PyInstaller:

```bash
pyinstaller --onefile y2b.py
```

The executable will be located in the `dist/` folder.

---

## Before Use
need to PATH to use the exe file.<br>
Only works in windows.

---
### Notes

- FFmpeg must be installed and added to your system PATH for the tool to work correctly.
- The downloaded files will be saved to your Windows **Downloads** folder.
