# This script is written to copy songs from xspf playlist (used in Tauon Music Box) to any other path

import argparse
import re
import os
import shutil
import subprocess
from ftplib import FTP
import getpass

parser = argparse.ArgumentParser()

parser.add_argument("-p", "--file-path",
                    help="Path to the xspf file", required=True)
parser.add_argument("-c", "--convert-flac",
                    help="Convert flac to mp3", nargs="?", const=True)
parser.add_argument("-s", "--sync",
                    help="Sync playlist with output folder", nargs="?", const=True)
parser.add_argument("-o", "--output-path",
                    help="Path to the output folder\nFor FTP: relative path to the folder", required=True)
parser.add_argument("-ftp", "--ftp-server",
                    help="FTP server address")

args = parser.parse_args()

file_path = args.file_path
transcode = args.convert_flac
output = args.output_path
sync = args.sync
ftp = args.ftp_server


def get_filename(path):
    return path[::-1].split('/')[0][::-1]


def connect_ftp():
    f = FTP()
    port = int(input('\nEnter port: '))
    f.connect(ftp, port=port)
    require_sign_in = input('\nDoes it require login? (Y/N): ')
    if require_sign_in in 'yY':
        user = input('\nEnter username: ')
        password = getpass.getpass('Enter password: ')
        f.login(user=user, passwd=password)
    else:
        f.login()
    return f


def upload_to_ftp(file_path, ftp_instance):
    try:
        with open(file_path, "rb") as song_file:
            ftp_instance.storbinary(f"STOR {get_filename(file_path)}", song_file)
    except FileNotFoundError:
        print(f"Could not upload {file_path}")


# Open xspf playlist file
xspf = open(file_path, "r", encoding="utf-8")
lines = xspf.readlines()

# List song path from xspf file
song_paths = []
for line in lines:
    # append string with <location> tag to song_paths list
    if "<location>" in line:
        song_paths.append(line[16:][::-1][12:][::-1])

# List songs in output directory
extensions = ['.mp3', '.flac']
output_songs = []
if ftp == None:
    for song_path in os.listdir(output):
        file_extension = os.path.splitext(song_path)[1]
        if file_extension in extensions:
            song = get_filename(song_path)
            output_songs.append(song)
else:
    f = connect_ftp()
    f.cwd(output)
    for file_data in f.mlsd():
        file_name, meta = file_data
        if meta.get("type") == "file":
            extension = os.path.splitext(file_name)[1]
            if extension in extensions:
                output_songs.append(file_name)

# Remove extensions so that same song will not remain in both .flac and .mp3 format (output_songs_without_extension)
output_songs_we = [
    os.path.splitext(song)[0] for song in output_songs]

print()
# Start copying or transcoding songs from playlist
for song_path in song_paths:
    song_name = get_filename(song_path)
    # song_name_without_extension
    song_name_we = os.path.splitext(song_name)[0]

    if song_name_we in output_songs_we:
        # Remove song from output list to sync by deleting them if -s is passed
        for song in output_songs:
            if song_name_we in song:
                output_songs.remove(song)
    else:
        song_extension = os.path.splitext(song_name)[1]
        if song_extension == '.flac' and transcode != None:
            print('Transcoding ' + song_name)
            if ftp == None:
                transcode_output = f"{output}/{song_name_we}.mp3"
            else:
                try:
                    os.mkdir(".copy_xspf")
                except FileExistsError:
                    shutil.rmtree(".copy_xspf/")
                    os.mkdir(".copy_xspf/")
                transcode_output = f".copy_xspf/{song_name_we}.mp3"
            subprocess.run(["ffmpeg", "-i", f"{song_path}", "-c:a",
                           "libmp3lame", "-q:a", "0", transcode_output],
                           stdout=subprocess.DEVNULL,
                           stderr=subprocess.STDOUT)
            if ftp != None:
                print('Uploading ' + song_name + ' to ' + output)
                upload_to_ftp(transcode_output, f)

        else:
            if ftp != None:
                # with open(song_path, "rb") as song_file:
                #     f.storbinary(f"STOR {song_name}", song_file)
                print('Uploading ' + song_name + ' to ' + output)
                upload_to_ftp(song_path, f)
            else:
                print('Copying ' + song_name + ' to ' + output)
                shutil.copy(song_path, output)
try:
    shutil.rmtree(".copy_xspf/")
except:
    None


# if -s is passed, songs that aren't in playlist will be deleted from output path
if sync != None:
    for output_song in output_songs:
        print(f'Deleting {output_song} from {output}')
        if ftp == None:
            os.remove(f"{output}/{output_song}")
        else:
            f.delete(output_song)
