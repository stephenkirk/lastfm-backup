#!/usr/bin/env python3

import json
import csv
import os.path
import requests

def get_pages(username, api_key, limit=200):
    """ Getting the number of pages with scrobbling data """

    response = requests.get(
        "https://ws.audioscrobbler.com/2.0/"
        "?method=user.getrecenttracks&user="
        "{0}&api_key={1}&format=json&limit={2}".format(username, api_key, limit)
    )

    data = json.loads(response.content.decode("utf8"))

    return int(data["recenttracks"]["@attr"]["totalPages"])


def get_page(username, api_key, page, limit=200):
    """ Getting scrobbling data from a page """

    response = requests.get(
        "https://ws.audioscrobbler.com/2.0/"
        "?method=user.getrecenttracks&user={0}&api_key={1}&format=json"
        "&limit={2}&page={3}".format(username, api_key, limit, page)
    )

    data = json.loads(response.content.decode("utf8"))

    return data["recenttracks"]["track"]


def get_now_scrobbling(username, api_key):
    """ Getting now scrobbling track """

    response = requests.get(
        "https://ws.audioscrobbler.com/2.0/"
        "?method=user.getrecenttracks&user={0}"
        "&api_key={1}&format=json&limit=1".format(username, api_key)
    )

    data = json.loads(response.content.decode("utf-8"))

    if "@attr" in data["recenttracks"]["track"][0]:
        return True
    else:
        return False


def scrobbling_export(tracks, username, start_from_page=1):
    import os

    # Create scrobbles directory if it doesn't exist
    scrobbles_dir = "./scrobbles"
    os.makedirs(scrobbles_dir, exist_ok=True)

    filename = os.path.join(scrobbles_dir, f"{username}_{start_from_page}.json")
    with open(filename, "w", encoding="utf-8") as f:
        data = json.dumps(tracks, indent=4, sort_keys=True, ensure_ascii=False)
        f.write(data)

    return 1


if __name__ == "__main__":
    _ = dict()

    if os.path.exists("./config.json"):
        with open("./config.json") as f:
            _ = json.loads(f.read())
    else:
        _["api_key"] = input("API Key: ")
        _["username"] = input("Username: ")
    api_key, username = _["api_key"], _["username"]

    start_from_page = _.get("start_from_page", 1)
    current_page = start_from_page

    total_pages = get_pages(username, api_key)
    scrobbled = []

    while current_page <= total_pages:
        print(
            "\r{0:.2f}% [{1} of {2}]".format(
                (current_page * 100 / total_pages), current_page, total_pages
            ),
            end="",
        )

        response = get_page(username, api_key, current_page)

        for track in response:
            scrobbled.append(track)

        if current_page % 10 == 0:
            if scrobbling_export(scrobbled, username, start_from_page):
                print("\n{0} tracks saved!".format(len(scrobbled), username))

        current_page += 1

    if scrobbling_export(scrobbled, username, start_from_page):
        print("\n{0} tracks saved!".format(len(scrobbled), username))
