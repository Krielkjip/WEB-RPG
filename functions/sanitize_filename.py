import re


def sanitize_filename(filename: str, replacement: str = '_') -> str:
    # Define a regular expression pattern for invalid filename characters
    invalid_chars = r'[<>:"/\\|?*\x00-\x1F]'

    # Remove invalid characters using the regular expression
    sanitized = re.sub(invalid_chars, '', filename)

    # Replace spaces with the specified replacement character
    sanitized = re.sub(r'\s+', replacement, sanitized)

    # Return the sanitized filename
    return sanitized
