import json
import os

# This script scans all movies in the given source path and renames
# pure .srt files to .en.srt with overwrites

def main():
    # load config from a JSON file
    with open("config.json") as config_data:
        config = json.load(config_data)

    base_directory = config['source_path']
    for subdir, dirs, files in os.walk(base_directory):
        for file in files:
            if file.endswith('.srt') and not file.endswith('.en.srt') and not file.endswith('.zh.srt'):
                filename_base = file.split('.srt')[0]
                filename_new = filename_base + '.en.srt'
                old_path = os.path.join(subdir, file)
                new_path = os.path.join(subdir, filename_new)
                os.rename(old_path, new_path)
                print(file + ' --> ' + filename_new)

main()
