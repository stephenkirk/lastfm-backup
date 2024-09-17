import json
import csv
import os.path
import requests

def get_top_tags(artist, api_key):
    """ TODO """

    response = requests.get(
        "https://ws.audioscrobbler.com/2.0/"
        "?method=artist.gettoptags&artist={0}&api_key={1}&format=json"
        .format(artist, api_key)
    )

    data = json.loads(response.content.decode("utf8"))

    return [tag["name"] for tag in data["toptags"]["tag"][:5]]


if __name__ == "__main__":
    _ = dict()

    if os.path.exists("./config.json"):
        with open("./config.json") as f:
            _ = json.loads(f.read())
    else:
        _["api_key"] = input("API Key: ")
        _["username"] = input("Username: ")
    api_key, username = _["api_key"], _["username"]

    print(get_top_tags("Bladee", api_key));
