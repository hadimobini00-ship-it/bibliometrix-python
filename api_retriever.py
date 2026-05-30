import requests
import pandas as pd


def fetch_from_openalex(query):
    """
    Queries OpenAlex for a given search string and returns a DataFrame.
    Handles basic API interaction.
    """
    base_url = "https://api.openalex.org/works"
    params = {"search": query, "per-page": 20}

    print(f"Fetching data for: {query}...")
    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        data = response.json().get('results', [])
        return pd.DataFrame(data)
    else:
        print(f"Error fetching data: {response.status_code}")
        return pd.DataFrame()