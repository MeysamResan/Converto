import os
from pathlib import Path
from PIL import Image

# Supported formats
SUPPORTED_FORMATS = ["jpg", "jpeg", "png"]

def get_desktop_path():
    return os.path.join(os.path.expanduser("~"), "Desktop")

def validate_quality(input_quality):
    try:
        quality = int(input_quality)
        if 1 <= quality <= 100:
            return quality
        else:
            print("Quality must be between 1 and 100.")
    except ValueError:
        print("Invalid input for quality. Please enter a number between 1 and 100.")
    return None

def validate_resize():
    try:
        width = int(input("Enter the width: ").strip())
        height = int(input("Enter the height: ").strip())
        return width, height
    except ValueError:
        print("Invalid dimensions provided.")
        return None

def process_image(input_file, output_file, quality, resize):
    try:
        with Image.open(input_file) as img:
            # Resize if required
            if resize:
                img = img.resize(resize)
            
            # Handle format-specific logic
            if output_file.endswith(('.jpg', '.jpeg')):
                if img.mode in ("RGBA", "LA"):
                    background = Image.new("RGB", img.size, (255, 255, 255))
                    background.paste(img, mask=img.split()[3])
                    img = background
                else:
                    img = img.convert("RGB")
                img.save(output_file, quality=quality, optimize=True, progressive=True)
            elif output_file.endswith('.png'):
                if img.mode not in ("RGBA", "RGB", "LA", "L"):
                    img = img.convert("RGBA")
                img.save(output_file, optimize=True, compress_level=(10 - quality // 10))
            print(f"File saved: {output_file}")
    except Exception as e:
        print(f"Error processing {input_file}: {e}")

def convert_folder(input_folder, output_format, quality, resize):
    output_folder = Path(input_folder).parent / f"expo_{Path(input_folder).name}"
    output_folder.mkdir(parents=True, exist_ok=True)
    for root, _, files in os.walk(input_folder):
        for file in files:
            input_file = os.path.join(root, file)
            try:
                with Image.open(input_file):
                    relative_path = Path(input_file).relative_to(input_folder)
                    output_file = output_folder / relative_path.with_suffix(f".{output_format}")
                    output_file.parent.mkdir(parents=True, exist_ok=True)
                    process_image(input_file, str(output_file), quality, resize)
            except Exception:
                print(f"Skipping non-image file: {input_file}")

def main():
    print("Image File Converter Script")
    input_path = input("Enter the path of the file or folder you want to convert: ").strip().strip('"')
    if not os.path.exists(input_path):
        print("The specified path does not exist.")
        return

    output_format = input(f"Enter the desired format (supported: {', '.join(SUPPORTED_FORMATS)}): ").strip().lower()
    if output_format not in SUPPORTED_FORMATS:
        print(f"Unsupported format '{output_format}'. Supported formats: {', '.join(SUPPORTED_FORMATS)}")
        return

    quality_input = input(f"Enter quality (1-100, default 85): ").strip()
    quality = validate_quality(quality_input or "85")
    if quality is None:
        return

    resize = None
    if input("Do you want to resize? (yes/no): ").strip().lower() in ["yes", "y"]:
        resize = validate_resize()

    if os.path.isdir(input_path):
        convert_folder(input_path, output_format, quality, resize)
    else:
        output_file = input(f"Enter output file path (or type 'desktop'/'d' to save to Desktop): ").strip().strip('"')
        if output_file.lower() in ["desktop", "d"]:
            output_file = str(Path(get_desktop_path()) / f"expo_{Path(input_path).stem}.{output_format}")
        elif not output_file:
            output_file = str(Path(input_path).with_suffix(f".{output_format}"))
        process_image(input_path, output_file, quality, resize)

if __name__ == "__main__":
    main()
