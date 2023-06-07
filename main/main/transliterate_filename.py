import os
from transliterate import translit

def transliterate_file(instance, filename):
    """
    Function to transliterate the file name
    """
    # Get the file extension
    ext = filename.split('.')[-1]
    # Transliterate the file name without the extension
    try:
        transliterated_name = translit(''.join(filename.split('.')[:-1]), reversed=True)
    except:
        transliterated_name = filename
    # Form the new file name with the transliterated name and extension
    new_filename = f"{transliterated_name}.{ext}"
    # Return the new file name
    return new_filename