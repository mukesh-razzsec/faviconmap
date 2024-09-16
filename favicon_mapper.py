import hashlib
import requests
import yaml
import argparse

YAML_FILE = 'favicons-database.yml'

def fetch_favicon(url):
    try:
        response = requests.get(f'{url}/favicon.ico', timeout=10, verify=False)
        response.raise_for_status()
        return response.content
    except requests.RequestException as e:
        print(f"Error fetching favicon: {e}")
        return None

def calculate_md5(data):
    md5_hash = hashlib.md5()
    md5_hash.update(data)
    return md5_hash.hexdigest()

def check_hash_in_yaml(md5_hash, yaml_file):
    try:
        with open(yaml_file, 'r') as file:
            data = yaml.safe_load(file)
            for entry in data:
                if entry['algorithm'] == 'MD5' and entry['hash'] == md5_hash:
                    return entry
    except Exception as e:
        print(f"Error reading YAML file: {e}")
    return None

def main(url):
    favicon_data = fetch_favicon(url)
    if not favicon_data:
        print("Failed to fetch favicon")
        return

    md5_hash = calculate_md5(favicon_data)
    print(f"MD5 hash of favicon: {md5_hash}")
        
    result = check_hash_in_yaml(md5_hash, YAML_FILE)
    if result:
        print(f"Match found: {result['name']}")
    else:
        print("No match found in YAML file.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fetch favicon and check its MD5 hash against a YAML file.")
    parser.add_argument('url', type=str, help="The URL of the website to fetch the favicon from.")
    args = parser.parse_args()
    main(args.url)
