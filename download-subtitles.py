from pythonopensubtitles.utils import File
from pythonopensubtitles.opensubtitles import OpenSubtitles
import getpass
import json
import os
import sys

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
    username = getpass.getuser()
    password = getpass.getpass()

    # clear previous log
    clearLog()

    # bootstrap OST with config file specifications
    with open("config.json") as config:
        config_data = json.load(config)
    ost = OpenSubtitles()
    ost.login(username, password)

    # iterate all torrent files in the path specified in config.json
    directory = config_data["path"]
    for filename in os.listdir(directory):
        if filename.endswith('.torrent'):
            query_filename = filename.split(".torrent", 1)[0]
            ost_data = ost.search_subtitles([{
                'sublanguageid': subtitleLanguageIDs,
                'query': query_filename}])
            if ost_data:
                id_subtitle_file = ost_data[0].get('IDSubtitleFile')
                subtitle_file_name = query_filename + '.zh.srt'
                ost.download_subtitles(
                    [id_subtitle_file],
                    override_filenames={id_subtitle_file : subtitle_file_name},
                    extension='srt')
            else:
                # log the movies that need manual subtitles
                writeLog(filename)

main()
