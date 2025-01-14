# File Converter

A Python-based file converter script to process images in various formats. This tool supports format conversion, quality adjustments, and resizing of images. It is designed to work seamlessly for single images or entire folders.

## Features

- Convert images to **JPG**, **JPEG**, or **PNG** formats.
- Preserve ICC color profiles for accurate color representation.
- Adjust image quality for both **JPG/JPEG** and **PNG** formats.
- Resize images to custom dimensions.
- Batch process all images in a folder while preserving folder structure.
- Save output to a custom location or the desktop with organized file naming.

## Installation

1. Ensure you have Python 3.6 or later installed.
2. Install the required dependencies:
   ```bash
   pip install pillow
## Usage
1. Clone the repository: `git clone <repository-url>`
2. Run the script: `python files_converter.py`
3. Follow the prompts to:
  * Select a file or folder for conversion.
  * Choose the desired output format (JPG, JPEG, or PNG).
  * Adjust the image quality (1-100, default is 85).
  * Optionally, resize the image by providing custom dimensions.

## Supported Formats
* **Images:** JPG, JPEG, and PNG.
