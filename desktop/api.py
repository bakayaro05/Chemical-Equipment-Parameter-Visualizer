import requests

BASE_URL = "http://127.0.0.1:8000/api"

def upload_csv(file_path):
    with open(file_path, "rb") as f:
        files = {"file": f}
        res = requests.post(f"{BASE_URL}/upload/", files=files)
    res.raise_for_status()
    return res.json()

def get_history():
    res = requests.get(f"{BASE_URL}/history/")
    res.raise_for_status()
    return res.json()

def download_pdf(save_path):
    res = requests.get(f"{BASE_URL}/pdf/")
    res.raise_for_status()

    with open(save_path, "wb") as f:
        f.write(res.content)


def get_dataset(dataset_id):
    res = requests.get(f"{BASE_URL}/dataset/{dataset_id}/")
    res.raise_for_status()
    return res.json()
