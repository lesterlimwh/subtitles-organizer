from pythonopensubtitles.utils import File
from pythonopensubtitles.opensubtitles import OpenSubtitles
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

    subtitleLanguageIDs = sys.argv[1]

    # clear previous log
    clearLog()

    # bootstrap OST
    with open("config.json") as config:
        config_data = json.load(config)
    ost = OpenSubtitles()
    ost.login(config_data["username"], config_data["password"])

    # grab all movie folder names in the path specified in config.json
    base_directory = config_data["path"]
    for movie_directory in os.listdir(base_directory):
        for file in os.listdir(os.path.join(base_directory, movie_directory)):
            filename = os.fsdecode(file)
            if filename.endswith('.mkv') or filename.endswith('.mp4'):
                ost_data = ost.search_subtitles([{
                    'sublanguageid': subtitleLanguageIDs,
                    'query': filename
                    }])
                if len(ost_data) > 0:
                    id_subtitle_file = ost_data[0].get('IDSubtitleFile')
                    subtitle_file_name = filename + '.zh'
                    ost.download_subtitles(
                        [id_subtitle_file],
                        override_filenames={id_subtitle_file : subtitle_file_name},
                        output_directory=os.path.join(base_directory, movie_directory),
                        extension='srt')
                else:
                    # log the movies that need manual subtitles
                    writeLog(filename)

main()
