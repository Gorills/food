import os
from transliterate import translit

def transliterate_file(instance, filename):
    """
    Function to transliterate the file name
    """
    # Get the file extension
    root, ext = os.path.splitext(filename)
    # Transliterate the file name without the extension
    try:
        transliterated_name = translit(root, 'ru', reversed=True)
    except Exception as e:
        print(f"Transliteration failed: {e}")
        transliterated_name = root
    # Form the new file name with the transliterated name and extension
    new_filename = transliterated_name + ext
    # Return the new file name
    return new_filename
