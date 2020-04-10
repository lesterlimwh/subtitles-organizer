from pythonopensubtitles.utils import File
from pythonopensubtitles.opensubtitles import OpenSubtitles
import getpass
import json
import os
import sys

# This script should only be used to download one type of language at a time
# Subtitles found will be saved in the given directory in the config file

# Constants
LOG_FILE = "no-subs-found.log"

def clearLog():
    with open(LOG_FILE, 'w') as log:
        log.write('')

def writeLog(filename):
    with open(LOG_FILE, 'a') as log:
        log.write(filename + '\n')

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

    # bootstrap OST with config file specifications
    with open("config.json") as config:
        config_data = json.load(config)
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

    # iterate all torrent files in the path specified in config.json
    directory = config_data["source_path"]
    print("Downloading subtitles for the following movies:")
    for filename in os.listdir(directory):
        print(filename)
        ost_data = ost.search_subtitles([{
            'sublanguageid': subtitleLanguageIDs,
            'query': filename}])
        if ost_data:
            id_subtitle_file = ost_data[0].get('IDSubtitleFile')
            subtitle_file_name = filename + file_extension
            ost.download_subtitles(
                [id_subtitle_file],
                override_filenames = {id_subtitle_file : subtitle_file_name},
                output_directory = os.path.join(directory, filename),
                extension = "srt")
        else:
            # log the movies that need manual subtitles
            writeLog(filename)

main()
