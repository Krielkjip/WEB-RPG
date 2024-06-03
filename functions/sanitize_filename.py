import re


def sanitize_filename(filename: str, replacement: str = '_') -> str:
    """
    Sanitizes a filename by removing invalid characters and replacing spaces with a specified replacement character.

    Args:
        filename (str): The filename to sanitize.
        replacement (str, optional): The character to replace spaces with. Defaults to '_'.

    Returns:
        str: The sanitized filename.
    """

    # Define a regular expression pattern for invalid filename characters
    # The pattern matches the following characters:
    # - '<', '>', ':', '/', '\\', '|', '?', '*', and all control characters (0x00-0x1F)
    invalid_chars = r'[<>:"/\\|?*\x00-\x1F]'

    # Remove invalid characters from the filename using the regular expression
    # The re.sub function replaces all occurrences of the pattern in the filename with an empty string
    sanitized = re.sub(invalid_chars, '', filename)

    # Replace one or more spaces in the sanitized filename with the specified replacement character
    # The re.sub function replaces all occurrences of one or more spaces with the replacement character
    sanitized = re.sub(r'\s+', replacement, sanitized)

    # Return the sanitized filename
    return sanitized
