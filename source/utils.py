SUPPORTED_FORMATS = ["bmp", "ico", "gif", "aac"]
QUALITY_RANGE = (1, 100)
BITRATE_MIN = 32
BITRATE_MAX = 320
CHANNELS_OPTIONS = [1, 2]
FREQUENCY_MIN = 8000
FREQUENCY_MAX = 48000

def validate_input(input_value, value_type, valid_range=None, valid_options=None):
    try:
        value = value_type(input_value)
        if valid_range and not (valid_range[0] <= value <= valid_range[1]):
            raise ValueError(f"Value must be between {valid_range[0]} and {valid_range[1]}.")
        if valid_options and value not in valid_options:
            raise ValueError(f"Value must be one of {valid_options}.")
        return value
    except ValueError as e:
        print(f"Invalid input: {e}")
        return None

def validate_quality(input_quality, output_format):
    if output_format in SUPPORTED_FORMATS:
        print(f"Quality adjustment is not supported for {output_format.upper()} format.")
        return None
    return validate_input(input_quality, int, QUALITY_RANGE)

def validate_bitrate(input_bitrate):
    if not input_bitrate:
        return None
    return validate_input(input_bitrate, int, (BITRATE_MIN, BITRATE_MAX))

def validate_channels(input_channels):
    if not input_channels:
        return None
    return validate_input(input_channels, int, valid_options=CHANNELS_OPTIONS)

def validate_frequency(input_frequency):
    if not input_frequency:
        return None
    return validate_input(input_frequency, int, (FREQUENCY_MIN, FREQUENCY_MAX))

def validate_resize(width, height):
    return validate_input(width, int), validate_input(height, int)