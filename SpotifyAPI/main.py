from SpotifyAPI import SpotifyAPI
import json
import sys

spotify_creds = {
        'client_id': '91475fef909246e6b0eb9a1bf70d73ee',
        'client_secret': 'b0a2b223496040d58bb8cfed63b5a2ab'
    }

if __name__ == '__main__':
    spotify = SpotifyAPI(spotify_creds['client_id'], spotify_creds['client_secret'])
    print(json.dumps(spotify.get_artist(sys.argv[1])))
