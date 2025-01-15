<p align="center">
  <img src="assets/MXS2750.gif" alt="MXS2750"/>
</p>

# Files Converter

## Introduction

A Python-based file converter script, a versatile and user-friendly tool designed to make file processing simple and efficient. This script supports various types of files, including images and beyond, offering capabilities such as format conversion, quality adjustments, and resizing. Whether you're working with single files, multiple files, or even entire folders, this tool is designed to handle it all effortlessly.

I created this script out of a need for a free, offline solution to convert files without relying on a web browser, dedicated apps, or other complex setups. It’s designed to integrate directly into your workflow by allowing you to select files or folders and initiate the conversion process directly from the context menu. With this convenient and efficient approach, you can convert files anytime, anywhere, without additional hassle.

## Features

- Convert images to JPG, JPEG, PNG, BMP, ICO, or GIF formats.
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
  * Choose the desired output format (JPG, JPEG, PNG, BMP, ICO, or GIF).
  * Adjust the image quality (1-100, default is 85).
  * Optionally, resize the image by providing custom dimensions.

## Supported Files and Formats
* **Images:** JPG, JPEG, PNG, BMP, ICO, and GIF.

## Features to Add
1. [ ] Most popular image formats.
2. [ ] Most popular audio formats.
3. [ ] Most popular video formats.
4. [ ] Most popular document formats.
5. [ ] A desktop application version with GUI.
6. [ ] The abilty to convert from context menu by simply right clicking on a file/folder then select convert.