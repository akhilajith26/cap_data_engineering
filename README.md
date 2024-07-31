# Marvel API Character and Comics Fetcher

This project fetches Marvel characters and their comic appearances using the Marvel API.

## Folder Structure

```
my_marvel_project/
├── secrets.yaml
├── main.py
├── cap_assessment.ipyb
├── requirements.txt
├── flow_diagram.txt
├── flow_diagram.jpg
```

## Prerequisites

- Python 3.x
- `requests` library
- `tqdm` library
- `PyYAML` library

Install the required libraries:
```sh
pip install requests tqdm pyyaml
```

## Setup

1. **Clone the repository**:
    ```sh
    git clone git@github.com:akhilajith26/cap_data_engineering.git
    ```

2. **Create `secrets.yaml` file**:
    ```yaml
    public_key: "your_public_key"
    private_key: "your_private_key"
    ```

## Usage

Run the script to fetch Marvel characters and their comic appearances:
```sh
python main.py
```

## Files

- `secrets.yaml`: Contains the Marvel API public and private keys.
- `main.py`: Main script to fetch characters and comics using Marvel API.
- `cap_assessment.ipyb`: Colab noteboook to run the code.
- `requirements.txt`: Contains all the dependencies to be installed
- `flow_diagram.txt`: Contains the flow diagram of get_character()
- `flow_diagram.jpg`: Contains the flow chart image of the implementation in general

## Functions

### `get_characters()`

Fetches a list of Marvel characters along with their comic appearances.

### `get_all_characters()`

Fetches all Marvel characters and the number of comics they appear in, with pagination support.

### `get_comics()`

Fetches a list of Marvel comics.
