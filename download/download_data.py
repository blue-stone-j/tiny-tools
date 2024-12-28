import requests
import re
from tqdm import tqdm

def download_file_with_progress_bar(url, output_dir="."):
    response = requests.get(url, stream=True)
    
    # Extract the filename from the Content-Disposition header
    if "Content-Disposition" in response.headers:
        filename = re.findall("filename=\"(.+)\"", response.headers["Content-Disposition"])[0]
    else:
        filename = url.split("/")[-1]  # Fallback to the last part of the URL

    filepath = f"{output_dir}/{filename}"
    
    # Get total file size from headers
    total_size = int(response.headers.get("Content-Length", 0))
    
    # Download the file with a progress bar
    with open(filepath, "wb") as file, tqdm(
        desc=filename,
        total=total_size,
        unit="B",
        unit_scale=True,
        unit_divisor=1024,
    ) as bar:
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                file.write(chunk)
                bar.update(len(chunk))
    
    print(f"File downloaded as: {filepath}")


file_url = "https://drive.google.com/uc?id=1i0SWkAqjVtyhPyeIDyAsQVO6KHhGkOtY&export=download"
download_path = "../data"
download_file_with_progress_bar(file_url, download_path)

