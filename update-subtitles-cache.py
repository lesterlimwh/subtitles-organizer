import json
import os
import pickle

# This script scans all movies in the given source path and updates
# the cache-en.pkl and cache-zh.pkl files

# constants
ENGLISH = 'en'
CHINESE = 'zh'

# get the cache file based on language:
def getCacheFile(language):
    cache_file = ''
    if language == CHINESE:
        cache_file = 'cache-zh.pkl'
    elif language == ENGLISH:
        cache_file = 'cache-en.pkl'
    else:
        cache_file = 'cache.pkl'
    return cache_file

# clear and write the cache
def writeCache(new_cache, language):
    cache_file = getCacheFile(language)
    with open(cache_file, 'wb') as old_cache:
        pickle.dump(new_cache, old_cache, pickle.HIGHEST_PROTOCOL)

def main():
    # load config from a JSON file
    with open("config.json") as config_data:
        config = json.load(config_data)

    # iterate all movie folders in the config source_path
    base_directory = config["source_path"]
    cache_en = {'Dummy Entry': 'True'}
    cache_zh = {'Dummy Entry': 'True'}
    print("Scanning movie folders for subtitle files...")
    for subdir, dirs, files in os.walk(base_directory):
        for file in files:
            if file.endswith(".en.srt"):
                print("Found English subtitle file: " + file)
                cache_en[subdir] = 'True'
                continue
            if file.endswith(".zh.srt"):
                print("Found Chinese subtitle file: " + file)
                cache_zh[subdir] = 'True'
                continue

    # update the cache files
    writeCache(cache_en, ENGLISH)
    writeCache(cache_zh, CHINESE)

main()
