import os
from pathlib import Path
from PIL import Image, ImageCms

def convert_image(input_file, output_file, quality=85, resize=None):
    try:
        with Image.open(input_file) as img:
            #Preserve color profile
            icc_profile = img.info.get("icc_profile")

            #Resize the image
            if resize:
                img = img.resize(resize)

            if output_file.endswith(('.jpg', '.jpeg')):
                #Handle transparency for JPG/JPEG format
                if img.mode in ("RGBA", "LA"):
                    #Create a white background
                    background = Image.new("RGB", img.size, (255, 255, 255))
                    background.paste(img, mask=img.split()[3])
                    img = background
                else:
                    img = img.convert("RGB")

            #Save with ICC profile if available
            img.save(output_file, quality=quality, optimize=True, progressive=True, icc_profile=icc_profile)
        print(f"Image has been converted and saved as: {output_file}")
    except Exception as e:
        print(f"An error occurred during image conversion: {e}")

def get_desktop_path():
    return os.path.join(os.path.expanduser("~"), "Desktop")

def convert_folder(input_folder, output_format, quality=85, resize=None):
    output_folder_name = f"expo_{Path(input_folder).name}"
    output_folder_path = Path(input_folder).parent / output_folder_name
    output_folder_path.mkdir(parents=True, exist_ok=True)

    for root, _, files in os.walk(input_folder):
        for file in files:
            input_file = os.path.join(root, file)
            try:
                with Image.open(input_file):
                    input_path = Path(input_file)
                    relative_path = input_path.relative_to(input_folder)
                    output_file = output_folder_path / relative_path.with_name(f"expo_{input_path.stem}.{output_format}")
                    output_file.parent.mkdir(parents=True, exist_ok=True)
                    convert_image(input_file, str(output_file), quality=quality, resize=resize)
            except Exception:
                print(f"Skipping non-image file: {input_file}")

def main():
    print("Image File Converter Script")

    #Ask the user for the file or folder path
    input_path = input("Enter the path of the image or folder you want to convert: ").strip().strip('"')

    if not os.path.exists(input_path):
        print("The specified path does not exist.")
        return

    #Ask the user for the output format
    output_format = input("Enter the desired file format: ").strip().lower()

    supported_formats = ["jpg", "jpeg"]
    if output_format not in supported_formats:
        print(f"The specified format '{output_format}' is not supported.")
        print(f"Supported formats are: {', '.join(supported_formats)}")
        return

    #Additional options for JPG
    quality = 85
    resize = None

    if output_format in ("jpg", "jpeg"):
        try:
            quality_input = input("Enter the quality for the JPG (1-100, default is 85): ").strip()
            if not quality_input:
                quality = 85
            else:
                quality = int(quality_input)
                if quality < 1 or quality > 100:
                    print("Invalid quality value.")
                    return
        except ValueError:
            print("Invalid input for quality.")
            return

    #Ask for resize dimensions
    resize_choice = input("Do you want to resize the image(s)? (default is no): ").strip().lower()
    if resize_choice in ["yes", "y"]:
        try:
            width = int(input("Enter the width: ").strip())
            height = int(input("Enter the height: ").strip())
            resize = (width, height)
        except ValueError:
            print("Invalid dimensions provided. Skipping resize.")

    #Check if path is a folder
    if os.path.isdir(input_path):
        convert_folder(input_path, output_format, quality=quality, resize=resize)
    else:
        #Check if file is an image
        try:
            with Image.open(input_path):
                pass
        except Exception:
            print("The specified file is not a valid image.")
            return

        #Derive the output file name and path
        input_path_obj = Path(input_path)
        output_file = input(f"Enter the output file path (leave blank to use expo_{input_path_obj.stem}.{output_format} or type 'desktop'/'d' to save to Desktop): ").strip().strip('"')

        if output_file.lower() in ["desktop", "d"]:
            desktop_path = get_desktop_path()
            output_file = str(Path(desktop_path) / f"expo_{input_path_obj.stem}.{output_format}")
        elif not output_file:
            output_file = str(input_path_obj.with_name(f'expo_{input_path_obj.stem}').with_suffix(f'.{output_format}'))

        #Do the image conversion
        convert_image(input_path, output_file, quality=quality, resize=resize)

if __name__ == "__main__":
    main()
