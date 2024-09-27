import requests

def download_file(url, output_file):
    response = requests.get(url, stream=True)
    with open(output_file, 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)
    print(f"Downloaded: {output_file}")
