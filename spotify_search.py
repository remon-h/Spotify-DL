import spotify_client
import requests
from urllib.parse import urlencode
import json
from configparser import ConfigParser
from termcolor import colored

song_dict = {}
config = ConfigParser()
config.read('config.ini')


def get_get_token_header():
    access_token = spotify_client.extract_access_token()[0]
    return {
    'Authorization': f'Bearer {access_token}'
    }
    
def get_user_playlist():
    playlist_id = config['user']['playlist_id']
    url = config['endpoints']['base_url']
    version = '/v1'
    action = '/playlists'
    token_headers = get_get_token_header()
    endpoint = f'{url}{version}{action}/{playlist_id}'
    r = requests.get(endpoint, headers=token_headers)
    
    if r.status_code in range(200, 299):
        data_tracks = (r.json())['tracks']
        for item in data_tracks['items']:
            
            if item is not None:
                track_name = item['track']['name']
                track_artist = item['track']['artists'][0]['name']
                song_dict.update([(track_artist, track_name)])
                song_dict_count = len(song_dict)
        print((colored(f'Succes! We found {song_dict_count} track(s). Status Code: {r.status_code}','green')))
        print(song_dict)
    else:
        print("Invalid request!")
        
        
if __name__ == "__main__":
    
    while config['user']['playlist_id'] == '':
        playlist_id_new = input(colored('We need the Playlist ID. Please enter the ID: ','yellow'))
        if playlist_id_new == '':
            continue
        config['user']['playlist_id'] = playlist_id_new
        # save to a file
        with open('config.ini', 'w') as configfile:
            config.write(configfile)
            print(colored('Playlist has been updated.','green'))
        continue
    else:
        get_user_playlist()