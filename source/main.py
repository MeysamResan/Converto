from pathlib import Path
import os
from utils import validate_quality, validate_resize, validate_bitrate, validate_channels, validate_frequency
from image_processing import process_image, convert_folder_images
from audio_processing import process_audio, convert_folder_audio

SUPPORTED_FORMATS = ["jpg", "jpeg", "png", "bmp", "ico", "gif", "webp", "aac"]
DEFAULT_QUALITY = 85
ICO_SIZES = [(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]

def get_user_input(prompt, default=None, valid_options=None):
    while True:
        user_input = input(prompt).strip()
        if not user_input and default is not None:
            return default
        if valid_options and user_input not in valid_options:
            print(f"Invalid input. Valid options are: {', '.join(valid_options)}")
        else:
            return user_input

def main():
    input_path = get_user_input("Enter the path of the file or folder you want to convert: ").strip('"')
    if not os.path.exists(input_path):
        print("The specified path does not exist.")
        return

    output_format = get_user_input(f"Enter the desired format (supported: {', '.join(SUPPORTED_FORMATS)}): ", valid_options=SUPPORTED_FORMATS).lower()

    quality = None
    if output_format not in ["bmp", "ico", "gif", "aac"]:
        quality_input = get_user_input(f"Enter quality (1-100, default {DEFAULT_QUALITY}): ", str(DEFAULT_QUALITY))
        quality = validate_quality(quality_input, output_format)
        if quality is None:
            return

    resize = None
    if output_format in ["jpg", "jpeg", "png", "bmp", "ico", "gif", "webp"]:
        if output_format == "ico":
            print("Choose a size for the ICO file:")
            for idx, size in enumerate(ICO_SIZES):
                print(f"{idx + 1}. {size[0]}x{size[1]}")
            size_choice = get_user_input("Enter the number corresponding to the size: ")
            resize = ICO_SIZES[int(size_choice) - 1] if size_choice.isdigit() and 1 <= int(size_choice) <= len(ICO_SIZES) else None
        else:
            resize_input = get_user_input("Do you want to resize? (yes/no, leave blank to keep original): ", default="no").lower()
            if resize_input in ["yes", "y"]:
                width = get_user_input("Enter the width: ")
                height = get_user_input("Enter the height: ")
                resize = validate_resize(width, height)

    bitrate = None
    channels = None
    frequency = None
    normalize = False
    if output_format == "aac":
        bitrate_input = get_user_input("Enter bitrate (range 32k-320k, leave blank to keep original): ")
        bitrate = validate_bitrate(bitrate_input)

        channels_input = get_user_input("Enter number of channels (1, 2, or leave blank to keep original): ")
        channels = validate_channels(channels_input)

        frequency_input = get_user_input("Enter frequency (range 8000-48000, leave blank to keep original): ")
        frequency = validate_frequency(frequency_input)

        normalize_input = get_user_input("Do you want to normalize the audio? (yes/no, leave blank to keep original): ", default="no").lower()
        normalize = normalize_input in ["yes", "y"]

    if os.path.isdir(input_path):
        if output_format == "aac":
            convert_folder_audio(input_path, output_format, bitrate, channels, frequency, normalize)
        else:
            convert_folder_images(input_path, output_format, quality, resize)
    else:
        output_file = str(Path(input_path).with_name(f"expo_{Path(input_path).stem}").with_suffix(f".{output_format}"))
        if output_format == "aac":
            process_audio(input_path, output_file, bitrate, channels, frequency, normalize)
        else:
            process_image(input_path, output_file, quality, resize)

    print("Conversion completed.")

if __name__ == "__main__":
    main()