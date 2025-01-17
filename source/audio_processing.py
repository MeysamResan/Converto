from pydub import AudioSegment
import os
from pathlib import Path

# Process a single audio file
def process_audio(input_file, output_file, bitrate, channels, frequency, normalize):
    try:
        audio = AudioSegment.from_file(input_file)
        # Normalize the audio if requested
        if normalize:
            audio = audio.normalize()
        # Set the frequency if provided
        if frequency:
            audio = audio.set_frame_rate(frequency)
        # Set the number of channels if provided
        if channels:
            audio = audio.set_channels(channels)
        audio = audio.set_sample_width(2)
        export_params = {"format": "adts", "codec": "aac"}
        # Set the bitrate if provided
        if bitrate:
            export_params["bitrate"] = bitrate
        audio.export(output_file, **export_params)
        print(f"File saved: {output_file}")
    except Exception as e:
        print(f"Error processing {input_file}: {e}")

# Convert all audio files in a folder to the specified format
def convert_folder_audio(input_folder, output_format, bitrate, channels, frequency, normalize):
    for root, _, files in os.walk(input_folder):
        for file in files:
            input_file = os.path.join(root, file)
            output_file = os.path.join(root, f"converted_{Path(file).stem}.{output_format}")
            process_audio(input_file, output_file, bitrate, channels, frequency, normalize)