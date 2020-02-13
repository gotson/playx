# PLAYX

A simple script to download Plex playlists as `m3u` files.

## Usage

```
usage: playx.py [-h] -s SERVER -t TOKEN [-d DIRECTORY]

Export Plex playlists to m3u files.

optional arguments:
  -h, --help            show this help message and exit
  -s SERVER, --server SERVER
                        Plex server to connect to
  -t TOKEN, --token TOKEN
                        Plex authentication token
  -d DIRECTORY, --directory DIRECTORY
                        Output directory, defaults to current
```

You will need a Plex authentication token, refer [here](https://support.plex.tv/articles/204059436-finding-an-authentication-token-x-plex-token/) for instructions on how to get one.