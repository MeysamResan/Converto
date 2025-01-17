from pathlib import Path
import os
from utils import validate_quality, validate_resize, validate_bitrate, validate_channels, validate_frequency
from image_processing import process_image, convert_folder_images
from audio_processing import process_audio, convert_folder_audio

SUPPORTED_FORMATS = ["jpg", "jpeg", "png", "bmp", "ico", "gif", "webp", "aac"]
DEFAULT_QUALITY = 85
ICO_SIZES = [(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]

# Main function to handle user input and initiate the conversion process
def main():
    input_path = input("Enter the path of the file or folder you want to convert: ").strip().strip('"')
    if not os.path.exists(input_path):
        print("The specified path does not exist.")
        return

    output_format = input(f"Enter the desired format (supported: {', '.join(SUPPORTED_FORMATS)}): ").strip().lower()
    if output_format not in SUPPORTED_FORMATS:
        print(f"Unsupported format '{output_format}'. Supported formats: {', '.join(SUPPORTED_FORMATS)}")
        return

    quality = None
    if output_format not in ["bmp", "ico", "gif", "aac"]:
        quality_input = input(f"Enter quality (1-100, default {DEFAULT_QUALITY}): ").strip()
        quality = validate_quality(quality_input or str(DEFAULT_QUALITY), output_format)
        if quality is None:
            return

    resize = None
    if output_format in ["jpg", "jpeg", "png", "bmp", "ico", "gif", "webp"]:
        if output_format == "ico":
            print("Choose a size for the ICO file:")
            for idx, size in enumerate(ICO_SIZES):
                print(f"{idx + 1}. {size[0]}x{size[1]}")
            size_choice = input("Enter the number corresponding to the size: ").strip()
            try:
                size_choice = int(size_choice)
                if 1 <= size_choice <= len(ICO_SIZES):
                    resize = ICO_SIZES[size_choice - 1]
                else:
                    print("Invalid choice. Using default size.")
            except ValueError:
                print("Invalid input. Using default size.")
        else:
            resize_input = input("Do you want to resize? (yes/no, leave blank to keep original): ").strip().lower()
            if resize_input in ["yes", "y"]:
                width = input("Enter the width: ").strip()
                height = input("Enter the height: ").strip()
                resize = validate_resize(width, height)
            elif resize_input not in ["no", "n", ""]:
                print("Invalid input. Please enter 'yes', 'y', 'no', 'n', or leave blank to keep original.")
                return

    bitrate = None
    channels = None
    frequency = None
    normalize = False
    if output_format == "aac":
        bitrate_input = input("Enter bitrate (range 32k-320k, leave blank to keep original): ").strip()
        bitrate = validate_bitrate(bitrate_input)

        channels_input = input("Enter number of channels (1, 2, or leave blank to keep original): ").strip()
        channels = validate_channels(channels_input)

        frequency_input = input("Enter frequency (range 8000-48000, leave blank to keep original): ").strip()
        frequency = validate_frequency(frequency_input)
        if frequency is None:
            frequency = None

        normalize_input = input("Do you want to normalize the audio? (yes/no, leave blank to keep original): ").strip().lower()
        if normalize_input in ["yes", "y"]:
            normalize = True
        elif normalize_input in ["no", "n", ""]:
            normalize = False
        else:
            print("Invalid input. Please enter 'yes', 'y', 'no', 'n', or leave blank to keep original.")
            return

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