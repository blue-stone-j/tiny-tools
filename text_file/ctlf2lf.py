import os
import mimetypes

# Allowed extensions
TARGET_EXTENSIONS = {".cpp", ".h", ".hpp"}

def is_target_file(file_path):
    mime_type, _ = mimetypes.guess_type(file_path)
    return (mime_type is not None and mime_type.startswith("text")) or file_path.endswith(tuple(TARGET_EXTENSIONS))

def convert_crlf_to_lf(directory):
    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            if is_target_file(file_path):
                try:
                    with open(file_path, 'rb') as f:
                        content = f.read()
                    new_content = content.replace(b'\r\n', b'\n')

                    if new_content != content:
                        with open(file_path, 'wb') as f:
                            f.write(new_content)
                        print(f"Converted: {file_path}")

                except Exception as e:
                    print(f"Error processing {file_path}: {e}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python convert_crlf_to_lf.py <directory>")
        sys.exit(1)

    convert_crlf_to_lf(sys.argv[1])

