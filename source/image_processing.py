import os
from pathlib import Path
from PIL import Image, ImageSequence

def process_image(input_file, output_file, quality, resize):
    try:
        with Image.open(input_file) as img:
            if img.format == "GIF" and getattr(img, "is_animated", False):
                handle_animated_gif(img, output_file, resize)
                return
            if resize:
                img = img.resize(resize)
            save_image(img, output_file, quality)
            print(f"File saved: {output_file}")
    except Exception as e:
        print(f"Error processing {input_file}: {e}")

def handle_animated_gif(img, output_file, resize):
    total_frames = img.n_frames
    print(f"This GIF has {total_frames} frames.")
    frame_number = input("Enter the frame number to extract (type 'all' to extract all frames): ").strip()

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

    if resize:
        img = img.resize(resize)
    img.save(output_file)
    print(f"Extracted frame {frame_number} and saved to {output_file}")

def save_image(img, output_file, quality):
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

def convert_folder_images(input_folder, output_format, quality, resize):
    if output_format == "gif":
        combine_choice = input("Do you want to combine images into a single animated GIF? (yes/no): ").strip().lower()
        if combine_choice in ["yes", "y"]:
            output_file = str(Path(input_folder).parent / f"combined_{Path(input_folder).name}.gif")
            combine_to_gif(input_folder, output_file, resize)
            return
        elif combine_choice not in ["no", "n"]:
            print("Invalid choice. Please enter 'yes', 'y', 'no', or 'n'.")
            return

    for root, _, files in os.walk(input_folder):
        for file in files:
            input_file = os.path.join(root, file)
            output_file = os.path.join(root, f"converted_{Path(file).stem}.{output_format}")
            process_image(input_file, output_file, quality, resize)

def combine_to_gif(input_folder, output_file, resize):
    images = []
    for root, _, files in os.walk(input_folder):
        for file in files:
            input_file = os.path.join(root, file)
            with Image.open(input_file) as img:
                if resize:
                    img = img.resize(resize)
                images.append(img.copy())

    if images:
        images[0].save(output_file, save_all=True, append_images=images[1:], optimize=True, duration=100, loop=0)
        print(f"Animated GIF saved: {output_file}")