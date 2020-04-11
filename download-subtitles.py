from pythonopensubtitles.utils import File
from pythonopensubtitles.opensubtitles import OpenSubtitles
import getpass
import json
import os
import pickle
import sys

# This script should only be used to download one type of language at a time
# Subtitles found will be saved in the given directory in the config file
# Movies that already have subtitles will be recorded in cache.json

# constants
LOG_FILE = "no-subs-found.log"
ENGLISH = 'en'
CHINESE = 'zh'

# clear the no-subs-found log
def clearLog():
    with open(LOG_FILE, 'w') as log:
        log.write('')

# add an entry to the no-subs-found log
def writeLog(filename):
    with open(LOG_FILE, 'a') as log:
        log.write(filename + '\n')

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

# return the cache as a dictionary
def readCache(language):
    cache_file = getCacheFile(language)
    with open(cache_file, 'rb') as cache:
        return pickle.load(cache)

def main():
    if len(sys.argv) != 2:
        print('''
            Usage: python download-subtitles.py
            <subtitle language ID, separated by commas e.g. "chi,zht,zhe">
        ''')
        quit()

    # CLI parameters
    subtitleLanguageIDs = sys.argv[1]

    # Prompt user login
    print("Enter OpenSubtitles login credentials")
    username = input("Username: ")
    password = getpass.getpass()

    # clear previous log
    clearLog()

    # initialize cache-en.pkl and cache-zh.pkl files if they do not exist
    if not os.path.exists('cache-en.pkl'):
        empty_dict = {'Dummy Entry': 'True'}
        writeCache(empty_dict, ENGLISH)
    if not os.path.exists('cache-zh.pkl'):
        empty_dict = {'Dummy Entry': 'True'}
        writeCache(empty_dict, CHINESE)

    # load config from a JSON file
    with open("config.json") as config_data:
        config = json.load(config_data)

    # authenticate with OST API
    ost = OpenSubtitles()
    ost.login(username, password)

    # initialize file extension format
    file_extension = ""
    if subtitleLanguageIDs == "chi,zht,zhe":
        file_extension = ".zh.srt"
    elif subtitleLanguageIDs == "en":
        file_extension = ".en.srt"
    else:
        file_extension = ".srt"

    # get language to use for cache (default to chinese)
    cache_language = CHINESE
    if subtitleLanguageIDs == 'en':
        cache_language = ENGLISH

    # iterate all torrent files in the path specified in config.json
    base_directory = config["source_path"]
    cache = readCache(cache_language)
    print("Searching subtitles for the following movies:")
    for filename in os.listdir(base_directory):
        # check if subtitles already downloaded for this movie
        if filename in cache:
            print("Skipping: " + filename)
            continue
        # search for subtitles
        ost_data = ost.search_subtitles([{
            'sublanguageid': subtitleLanguageIDs,
            'query': filename}])
        if ost_data:
            print("Downloading: " + filename)
            # subtitles found, start the download
            id_subtitle_file = ost_data[0].get('IDSubtitleFile')
            subtitle_file_name = filename + file_extension
            ost.download_subtitles(
                [id_subtitle_file],
                override_filenames = {id_subtitle_file : subtitle_file_name},
                output_directory = os.path.join(base_directory, filename),
                extension = "srt")
            # successfully downloaded, add entry to cache
            cache[filename] = 'True'
            writeCache(cache, cache_language)
        else:
            print("Failed to download: " + filename)
            # log the movies that need manual subtitles
            writeLog(filename)

main()
