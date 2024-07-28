import time
from tqdm import tqdm
from hashlib import md5
import requests
import yaml
import ssl

# Load API keys from the YAML file
with open("secrets.yaml", "r") as file:
    secrets = yaml.safe_load(file)

public_key = secrets["public_key"]
private_key = secrets["private_key"]
base_url = "https://gateway.marvel.com:443"


class TLSAdapter(requests.adapters.HTTPAdapter):
    # Adapter to set specific SSL settings
    def init_poolmanager(self, *args, **kwargs):
        ctx = ssl.create_default_context()
        ctx.set_ciphers("DEFAULT@SECLEVEL=1")
        kwargs["ssl_context"] = ctx
        return super(TLSAdapter, self).init_poolmanager(*args, **kwargs)


def get_characters():
    session = requests.session()
    get_character_url = f"{base_url}/v1/public/characters"
    session.mount(get_character_url, TLSAdapter())
    ts = str(time.time())
    limit = 15
    hash_str = md5(f"{ts}{private_key}{public_key}".encode("utf8")).hexdigest()
    # Parameters for the API request
    params = {
        "apikey": public_key,
        "ts": ts,
        "hash": hash_str,
        "orderBy": "name",
        "limit": limit,
    }
    res = session.get(get_character_url, params=params)
    data = res.json()
    total_characters = data["data"]["total"]
    print(total_characters)
    characters = data["data"]["results"]
    # List to hold all the character dictionaries
    all_character_list = []
    # Create dictionary with character name, number of comics and the list of comics the character appeared
    for character in characters:
        char_name = character["name"]
        char_comics_count = character["comics"]["available"]
        comic_item_list = character["comics"]["items"]
        character_dict = {
            "character": char_name,
            "no_of_comics": char_comics_count,
            "comic_list": [],
        }
        # Extract the list of comics for the character
        for index in range(len(comic_item_list)):
            character_dict["comic_list"].append(comic_item_list[index]["name"])

        all_character_list.append(character_dict)

    return all_character_list


def get_all_characters():
    character_comics = {}
    limit = 15  # Max characters per request
    offset = 0  # Initial offset
    total_characters = 1  # Initialize to enter the loop
    retries = 3  # Number of retries for each request
    get_character_url = f"{base_url}/v1/public/characters"
    ts = str(time.time())
    hash_str = md5(f"{ts}{private_key}{public_key}".encode("utf8")).hexdigest()

    # Fetch initial total characters to initialize tqdm
    session = requests.session()
    session.mount(base_url, TLSAdapter())
    params = {
        "apikey": public_key,
        "ts": ts,
        "hash": hash_str,
        "limit": limit,
        "offset": offset,
    }
    response = session.get(get_character_url, params=params)
    data = response.json()
    total_characters = data["data"]["total"]

    with tqdm(total=total_characters, desc="Fetching Characters") as pbar:
        while offset < total_characters:
            params["offset"] = offset

            for _ in range(retries):
                try:
                    response = session.get(get_character_url, params=params)
                    data = response.json()
                    characters = data["data"]["results"]

                    for character in characters:
                        char_name = character["name"]
                        char_comics_count = character["comics"]["available"]
                        character_comics[char_name] = char_comics_count

                    offset += limit  # Move to the next batch
                    pbar.update(limit)
                    break
                except requests.exceptions.RequestException as e:
                    print(f"Error occurred: {e}")
                    time.sleep(5)  # Wait before retrying
            else:
                print(f"Failed to fetch data after {retries} retries.")
                break  # Exit the loop if retries are exhausted

    return character_comics


def get_comics():
    session = requests.session()
    get_comic_url = f"{base_url}/v1/public/comics"
    session.mount(get_comic_url, TLSAdapter())
    ts = str(time.time())
    hash_str = md5(f"{ts}{private_key}{public_key}".encode("utf8")).hexdigest()
    # Parameters for the API request
    params = {
        "apikey": public_key,
        "ts": ts,
        "hash": hash_str,
        "limit": 50,
    }
    res = session.get(get_comic_url, params=params)
    return res.json()


characters = get_characters()
# comics = get_comics()
print(characters)

# all character output location
# https://colab.research.google.com/drive/14RcImogXzXiVciTxS2mCVpSI87bBp1Am?usp=sharing
