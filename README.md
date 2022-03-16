# copy_xspf
This script is written to copy/sync songs from xspf playlist (used in Tauon Music Box) to any other path or to a FTP server

## Requirements:
 - ffmpeg
 - opus-tools

# Usage

### For Tauon Music Box users
First, you need to export the xspf file

To do so, right click on playlist, then Misc -> Export xspf and you are redirected to the folder where the playlist is stored

### After you have .xspf file
#### To copy/sync the playlist with FTP server:

```bash
python copy_xspf.py -p (path_to_xspf_file) -o (playlist_directory_in_ftp_server) -f (ftp_server_address) 
```

```
Enter port: (enter your port number)

Does it require login? (Y/N): (enter if it requires login)
```

##### Example
```bash
python copy_xspf.py -p "/home/cyclonejet/.local/share/TauonMusicBox/playlists/vibe.xspf" -o "Music/playlist" -f 192.168.255.1
```

```
Enter port: 2121

Does it require login? (Y/N): N
```

- To transcode/convert flac to mp3 v0, pass ```-c```
- To sync playlist with destination, pass ```-s```

---

#### To copy/sync the playlist with another directory:

```bash
python copy_xspf.py -p (path_to_xspf_file) -o (directory_path) 
```

##### Example
```bash
python copy_xspf.py -p "/home/cyclonejet/.local/share/TauonMusicBox/playlists/vibe.xspf" -o "/run/media/cyclonejet/phone_sd"
```

- To transcode/convert flac to mp3 v0, pass ```-c```
- To sync playlist with destination, pass ```-s```

---
---
Pull requests are welcome!