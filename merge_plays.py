"""
This program merges and simplifies Last.fm scrobble data from multiple JSON files.

It performs the following operations:
1. Reads all JSON files containing scrobble data from a specified directory.
2. Merges the scrobbles, removing duplicates based on a unique key.
3. Simplifies the data structure of each scrobble, keeping only essential information.
4. Saves the merged and simplified scrobbles to a new JSON file.

The program uses a composite key (artist + track name + timestamp) to identify unique plays,
and flattens the JSON structure for easier processing and reduced file size.

Usage:
Set the 'directory' variable to the folder containing your scrobble JSON files.
Set the 'output_file' variable to your desired output file name.
Run the script to generate a merged and simplified JSON file of your Last.fm scrobbles.
"""

import json
import glob
import os

def create_key(play):
    # Create a unique key for each play
    return f"{play['artist']['#text']}_{play['name']}_{play['date']['uts']}"

def simplify_play(play):
    return {
        "album": play['album']['#text'],
        "artist": play['artist']['#text'],
        "name": play['name'],
        "date": play['date']['uts']
    }

def merge_scrobbles(directory):
    all_plays = {}

    # Get all JSON files in the specified directory
    json_files = glob.glob(os.path.join(directory, '*.json'))

    for file_path in json_files:
        with open(file_path, 'r') as file:
            plays = json.load(file)
            print(f"Loaded {len(plays)} songs from {file_path}")

            for play in plays:
                key = create_key(play)
                if key not in all_plays:
                    all_plays[key] = simplify_play(play)

    merged_plays = list(all_plays.values())

    return merged_plays

def save_merged_data(merged_plays, output_file):
    with open(output_file, 'w') as file:
        json.dump(merged_plays, file, indent=2)

# Usage
directory = './scrobbles'
output_file = 'merged_scrobbles.json'

merged_plays = merge_scrobbles(directory)
save_merged_data(merged_plays, output_file)

print(f"Merged {len(merged_plays)} unique plays into {output_file}")
