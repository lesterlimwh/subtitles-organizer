import json
import os
import sys

# This script scans all episodes in the one piece directory and renames them
    # e.g. One Piece - 579 - Land Ho! The Burning Island, Punk Hazard! [v3][BD][1080p][x264][Eng-Sub]-df68
# becomes One Piece - S16E579 - Land Ho! The Burning Island, Punk Hazard!

def main():
    if len(sys.argv) != 2:
        print('''
            Usage: python download-subtitles.py <season number>
        ''')
        quit()

    # CLI parameters
    season = sys.argv[1]

    # load config from a JSON file
    with open("config.json") as config_data:
        config = json.load(config_data)

    base_directory = config['one_piece_path']
    for subdir, dirs, files in os.walk(base_directory):
        for file in files:
            if file.endswith('.mkv'):
                if len(file.split('One Piece S')) > 1:
                    print('Skipping ' + file)
                    continue
                arr = file.split('-')
                # arr[0] = 'One Piece'
                # arr[1] = ' 579 '
                # arr[2] = ' Land Ho! The Burning Island, Punk Hazard! [v3][BD][1080p][x264][Eng'
                # arr[3] = 'Sub]'
                # arr[4] = 'df68.mkv'

                # tidy up the title
                title = arr[2].strip()
                title_arr = title.split('[')
                # title_arr[0] = 'Land Ho! The Burning Island, Punk Hazard! '
                clean_title = title_arr[0].strip()

                # construct the new filename
                episode = arr[1].strip()
                filename_new = 'One Piece S' + season + 'E' + episode + ' - ' + clean_title + '.mkv'

                # replace the current file
                old_path = os.path.join(subdir, file)
                new_path = os.path.join(subdir, filename_new)
                os.rename(old_path, new_path)
                print(file + ' --> ' + filename_new)
main()
