import requests
import json
import time
import os

BASE_URL = "https://api.opendota.com/api"

RAW_DATA_PATH = "data/raw"


def ensure_dir():
    if not os.path.exists(RAW_DATA_PATH):
        os.makedirs(RAW_DATA_PATH)


def fetch_pro_matches(limit=300):
    """
    Fetch recent pro matches
    """

    url = f"{BASE_URL}/proMatches"
    response = requests.get(url)

    if response.status_code != 200:
        raise Exception(f"Error fetching pro matches: {response.status_code}")

    data = response.json()
    return data[:limit]


def fetch_match_details(match_id):
    url = f"{BASE_URL}/matches/{match_id}"
    response = requests.get(url)

    if response.status_code != 200:
        print(f"Failed match {match_id}")
        return None

    return response.json()


def save_raw_match(match_data):
    """
    Save raw JSON
    """

    match_id = match_data["match_id"]
    filepath = os.path.join(RAW_DATA_PATH, f"{match_id}.json")

    with open(filepath, "w") as f:
        json.dump(match_data, f)

def count_files():
    """
    Use this in case to check how many file you have fetched at the data/raw folder.
    """

    file_count = len([f for f in os.listdir(RAW_DATA_PATH) if os.path.isfile(os.path.join(RAW_DATA_PATH, f))])

    print(f"Total files: {file_count}")

def main():
    ensure_dir()

    print("Fetching pro matches...")
    matches = fetch_pro_matches(limit=100)

    print(f"Found {len(matches)} matches")

    for match in matches:
        match_id = match["match_id"]
        print(f"Fetching match {match_id}")

        data = fetch_match_details(match_id)

        if data:
            save_raw_match(data)

        time.sleep(1)

    count_files()    


if __name__ == "__main__":
    main()

