from pydub import AudioSegment
import os
from pathlib import Path

def process_audio(input_file, output_file, bitrate=None, channels=None, frequency=None, normalize=False):
    try:
        audio = AudioSegment.from_file(input_file)
        if normalize:
            audio = audio.normalize()
        if frequency:
            audio = audio.set_frame_rate(frequency)
        if channels:
            audio = audio.set_channels(channels)
        audio = audio.set_sample_width(2)
        export_params = {"format": "adts", "codec": "aac"}
        if bitrate:
            export_params["bitrate"] = f"{bitrate}k"
        audio.export(output_file, **export_params)
        print(f"File saved: {output_file}")
    except Exception as e:
        print(f"Error processing {input_file}: {e}")

def convert_folder_audio(input_folder, output_format, bitrate, channels, frequency, normalize):
    for root, _, files in os.walk(input_folder):
        for file in files:
            input_file = os.path.join(root, file)
            output_file = os.path.join(root, f"converted_{Path(file).stem}.{output_format}")
            process_audio(input_file, output_file, bitrate, channels, frequency, normalize)