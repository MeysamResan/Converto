import os
from pathlib import Path
from PIL import Image, ImageSequence

# Supported formats
SUPPORTED_FORMATS = ["jpg", "jpeg", "png", "bmp", "ico", "gif", "webp"]

def get_desktop_path():
    return os.path.join(os.path.expanduser("~"), "Desktop")

def validate_quality(input_quality, output_format):
    if output_format in ["bmp", "ico", "gif"]:
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
            # Handle animated GIFs
            if img.format == "GIF" and getattr(img, "is_animated", False):
                total_frames = img.n_frames
                print(f"This GIF has {total_frames} frames.")
                frame_number = input("Enter the frame number to extract (type 'all' to extract all frames, leave blank for the first frame): ").strip()

                if frame_number.lower() == "all":
                    output_base = Path(output_file).stem
                    output_dir = Path(output_file).parent
                    output_dir.mkdir(parents=True, exist_ok=True)
                    for frame_idx in range(total_frames):
                        try:
                            img.seek(frame_idx)
                            frame_output = output_dir / f"{output_base}_frame{frame_idx}.{Path(output_file).suffix.strip('.')}"
                            frame = img.copy()
                            if resize:
                                frame = frame.resize(resize)
                            frame.save(frame_output)
                            print(f"Saved frame {frame_idx} to {frame_output}")
                        except EOFError:
                            break
                    return

                frame_number = int(frame_number) if frame_number.isdigit() else 0

                try:
                    img.seek(frame_number)
                except EOFError:
                    print(f"Invalid frame number: {frame_number}. Using the first frame instead.")
                    img.seek(0)

                # Resize the selected frame if needed
                if resize:
                    img = img.resize(resize)

                # Save the extracted frame
                img.save(output_file)
                print(f"Extracted frame {frame_number} and saved to {output_file}")
                return

            # Resize if required
            if resize:
                img = img.resize(resize)
            
            # Handle format-specific logic
            if output_file.endswith((".jpg", ".jpeg")):
                if img.mode in ("RGBA", "LA"):
                    background = Image.new("RGB", img.size, (255, 255, 255))
                    background.paste(img, mask=img.split()[3])
                    img = background
                else:
                    img = img.convert("RGB")
                img.save(output_file, quality=quality, optimize=True, progressive=True)
            elif output_file.endswith(".png"):
                if img.mode not in ("RGBA", "RGB", "LA", "L"):
                    img = img.convert("RGBA")
                img.save(output_file, optimize=True, compress_level=(10 - quality // 10))
            elif output_file.endswith(".bmp"):
                if img.mode not in ("RGB", "L"):
                    img = img.convert("RGB")
                img.save(output_file)
            elif output_file.endswith(".ico"):
                if img.mode not in ("RGBA", "RGB"):
                    img = img.convert("RGBA")
                img.save(output_file)
            elif output_file.endswith(".gif"):
                img.save(output_file, optimize=True)
            elif output_file.endswith(".webp"):
                if img.mode in ("RGBA", "LA"):
                    img = img.convert("RGBA")
                else:
                    img = img.convert("RGB")
                img.save(output_file, quality=quality, optimize=True)
            print(f"File saved: {output_file}")
    except Exception as e:
        print(f"Error processing {input_file}: {e}")

def combine_to_gif(input_folder, output_file, resize):
    images = []
    max_width, max_height = 0, 0

    # Collect images and calculate the maximum dimensions
    for root, _, files in os.walk(input_folder):
        for file in files:
            input_file = os.path.join(root, file)
            try:
                with Image.open(input_file) as img:
                    max_width = max(max_width, img.width)
                    max_height = max(max_height, img.height)
                    if resize:
                        img = img.resize(resize)
                    images.append(img.copy())
            except Exception:
                print(f"Skipping non-image file: {input_file}")

    if images:
        disposal_choice = input("Should each frame replace the previous one? (yes/no, default: yes): ").strip().lower()
        if not disposal_choice:  # Default to 'replace'
            disposal_choice = "yes"
        disposal_method = 2 if disposal_choice in ["yes", "y"] else 1  # 2 for replace, 1 for overlay

        # Center each image on a canvas of max dimensions
        centered_images = []
        for img in images:
            canvas = Image.new("RGBA", (max_width, max_height), (255, 255, 255, 0))
            offset = ((max_width - img.width) // 2, (max_height - img.height) // 2)
            canvas.paste(img, offset)
            centered_images.append(canvas)

        centered_images[0].save(
            output_file,
            save_all=True,
            append_images=centered_images[1:],
            optimize=True,
            loop=0,
            disposal=disposal_method
        )
        print(f"Combined images into animated GIF: {output_file}")
    else:
        print("No valid images found to combine into a GIF.")

def convert_folder(input_folder, output_format, quality, resize):
    if output_format == "gif":
        combine_choice = input("Do you want to combine images into a single animated GIF? (yes/no): ").strip().lower()
        if combine_choice in ["yes", "y"]:
            output_file = input(f"Enter output file path for the animated GIF (or type 'desktop'/'d' to save to Desktop): ").strip().strip('"')
            if output_file.lower() in ["desktop", "d"]:
                output_file = str(Path(get_desktop_path()) / f"combined_{Path(input_folder).name}.gif")
            elif not output_file:
                output_file = str(Path(input_folder).parent / f"combined_{Path(input_folder).name}.gif")
            combine_to_gif(input_folder, output_file, resize)
            return

    output_folder = input(f"Enter output folder path (or type 'desktop'/'d' to save to Desktop): ").strip().strip('"')
    if output_folder.lower() in ["desktop", "d"]:
        output_folder = str(Path(get_desktop_path()) / f"expo_{Path(input_folder).name}")
    elif not output_folder:
        output_folder = str(Path(input_folder).parent / f"expo_{Path(input_folder).name}")
    else:
        output_folder = str(Path(output_folder))

    output_folder_path = Path(output_folder)
    output_folder_path.mkdir(parents=True, exist_ok=True)

    for root, _, files in os.walk(input_folder):
        for file in files:
            input_file = os.path.join(root, file)
            try:
                with Image.open(input_file):
                    relative_path = Path(input_file).relative_to(input_folder)
                    output_file = output_folder_path / relative_path.with_suffix(f".{output_format}")
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

    quality = None
    if output_format not in ["bmp", "ico", "gif"]:
        quality_input = input(f"Enter quality (1-100, default 85): ").strip()
        quality = validate_quality(quality_input or "85", output_format)
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
            output_file = str(Path(input_path).with_name(f"expo_{Path(input_path).stem}").with_suffix(f".{output_format}"))
        else:
            output_file = str(Path(output_file).with_suffix(f".{output_format}"))
        process_image(input_path, output_file, quality, resize)

if __name__ == "__main__":
    main()
