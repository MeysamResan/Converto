import os

# Validate the quality input for image formats
def validate_quality(input_quality, output_format):
    if output_format in ["bmp", "ico", "gif", "aac"]:
        print(f"Quality adjustment is not supported for {output_format.upper()} format.")
        return None
    try:
        quality = int(input_quality)
        if 1 <= quality <= 100:
            return quality
        else:
            print("Quality must be between 1 and 100.")
    except ValueError:
        print("Invalid input for quality. Please enter a number between 1 and 100.")
    return None

# Validate the bitrate input for audio formats
def validate_bitrate(input_bitrate):
    if not input_bitrate:
        return None
    try:
        bitrate = int(input_bitrate)
        if bitrate > 0:
            return f"{bitrate}k"
        else:
            print("Bitrate must be a positive number.")
    except ValueError:
        print("Invalid input for bitrate. Please enter a positive number.")
    return None

# Validate the number of audio channels
def validate_channels(input_channels):
    if not input_channels:
        return None
    try:
        channels = int(input_channels)
        if channels in [1, 2]:
            return channels
        else:
            print("Channels must be 1 (mono) or 2 (stereo).")
    except ValueError:
        print("Invalid input for channels. Please enter 1 or 2.")
    return None

# Validate the frequency input for audio formats
def validate_frequency(input_frequency):
    if not input_frequency:
        return None
    try:
        frequency = int(input_frequency)
        if frequency > 0:
            return frequency
        else:
            print("Frequency must be a positive number.")
    except ValueError:
        print("Invalid input for frequency. Please enter a positive number.")
    return None

# Validate the resize dimensions for images
def validate_resize(width, height):
    try:
        width = int(width)
        height = int(height)
        return width, height
    except ValueError:
        print("Invalid dimensions provided.")
        return None