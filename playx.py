import io
import os
import argparse
from xml.etree import ElementTree
import logging

import requests


def get_plex_playlists_keys(server_url, plex_token, check_ssl):
    try:
        url = f'{server_url}/playlists'
        logging.info(f'Requesting playlists from Plex: {url}')
        params = {'X-Plex-Token': plex_token}
        resp = requests.get(url, timeout=30, verify=check_ssl, params=params)

        if resp.status_code == 200:
            root = ElementTree.fromstring(resp.text)

            keys = []
            for document in root.findall('Playlist'):
                if document.get('smart') == "0" and document.get('playlistType') == 'audio':
                    keys.append(document.get('key'))

            logging.info(f'Found {len(keys)} playlists')

            return keys

    except Exception:
        logging.exception('ERROR: Issue encountered when attempting to list detailed sections info')
        raise SystemExit


def get_plex_playlist(server_url, plex_token, key, check_ssl):
    try:
        url = f'{server_url}{key}'
        logging.info(f'Requesting playlist data from Plex: {url}')
        params = {'X-Plex-Token': plex_token}
        resp = requests.get(url, timeout=30, verify=check_ssl, params=params)

        if resp.status_code == 200:
            root = ElementTree.fromstring(resp.text)

            title = root.get('title')
            playlist = []
            for document in root.findall('Track'):
                playlist.append(document[0][0].get('file'))

            logging.info(f'Found playlist {title} with {len(playlist)} songs')

            return title, playlist

    except Exception:
        logging.exception('ERROR: Issue encountered when attempting to get Plex playlist: {e}')
        raise SystemExit


def main():
    logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO)

    parser = argparse.ArgumentParser(description='Export Plex playlists to m3u files.')
    parser.add_argument('-s', '--server', required=True, help='Plex server to connect to')
    parser.add_argument('-t', '--token', required=True, help='Plex authentication token')
    parser.add_argument('-d', '--directory', default='.', help='Output directory, defaults to current')

    args = parser.parse_args()

    playlists_keys = get_plex_playlists_keys(args.server, args.token, False)

    for key in playlists_keys:
        title, playlist = get_plex_playlist(args.server, args.token, key, False)

        os.makedirs(args.directory, exist_ok=True)
        file_path = os.path.join(args.directory, f'{title}.m3u')
        logging.info(f'Writing playlist to: {file_path}')
        with io.open(file_path, 'w+', encoding='utf8') as outfile:
            for track in playlist:
                outfile.write(f'{track}\n')


if __name__ == '__main__':
    main()
