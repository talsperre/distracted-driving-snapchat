import requests
import os

def download_file_from_google_drive(id, destination):
    def get_confirm_token(response):
        for key, value in response.cookies.items():
            if key.startswith('download_warning'):
                return value

        return None

    def save_response_content(response, destination):
        CHUNK_SIZE = 32768

        with open(destination, "wb") as f:
            for n in range(5):
                try:
                    chunks = response.iter_content(CHUNK_SIZE)
                    for chunk in chunks:
                        if chunk: # filter out keep-alive new chunks
                            f.write(chunk)
                    break
                except:
                    print("dealt with an error")
                    if n == 4:
                        raise e

    URL = "https://docs.google.com/uc?export=download"

    session = requests.Session()

    response = session.get(URL, params = { 'id' : id }, stream = True)
    token = get_confirm_token(response)

    if token:
        params = { 'id' : id, 'confirm' : token }
        response = session.get(URL, params = params, stream = True)

    save_response_content(response, destination)


if __name__ == "__main__":
    import sys
    if len(sys.argv) is not 4:
        print("Usage: python google_drive.py drive_file_id destination_file_dir destination_file_name")
    else:
        # TAKE ID FROM SHAREABLE LINK
        file_id = sys.argv[1]
        # DESTINATION FILE ON YOUR DISK
        destination_dir = sys.argv[2]
        destination_file_name = sys.argv[3]
        os.makedirs(destination_dir, exist_ok=True)
        destination_path = os.path.join(destination_dir, destination_file_name)
        download_file_from_google_drive(file_id, destination_path)
