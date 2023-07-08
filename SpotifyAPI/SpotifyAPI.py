import base64
import requests
import datetime
from urllib.parse import urlencode


class SpotifyAPI(object):
    access_token = None
    access_token_expires = datetime.datetime.now()
    access_token_did_expire = True
    client_id = None
    client_secret = None
    token_url = "https://accounts.spotify.com/api/token"

    def __init__(self, client_id, client_secret):
        super().__init__()
        self.client_id = client_id
        self.client_secret = client_secret

    def get_client_credentials(self):
        """
        Returns a base64 encoded string
        """
        if self.client_id is None or self.client_secret is None:
            raise Exception("You must set client id and client secret.")
        client_creds = f"{self.client_id}:{self.client_secret}"
        client_creds_b64 = base64.b64encode(client_creds.encode())
        return client_creds_b64.decode()

    def get_token_data(self):
        return {'grant_type': "client_credentials"}

    def get_token_headers(self):
        return {'Authorization': f"Basic {self.get_client_credentials()}"}

    def perform_auth(self):
        r = requests.post(self.token_url, data=self.get_token_data(), headers=self.get_token_headers())
        valid_request = r.status_code in range(200, 299)
        if not valid_request:
            raise Exception("Could not authenticate client.")
        data = r.json()
        now = datetime.datetime.now()
        access_token = data['access_token']
        self.access_token = access_token
        expires_in = data['expires_in']  # seconds
        expires = now + datetime.timedelta(seconds=expires_in)
        self.access_token_expires = expires
        self.access_token_did_expire = expires < datetime.datetime.now()
        return True

    def get_access_token(self):
        token = self.access_token
        expires = self.access_token_expires
        now = datetime.datetime.now()
        if expires < now or token is None:
            self.perform_auth()
            return self.get_access_token()
        return token

    def get_resource_header(self):
        headers = {
            "Authorization": f"Bearer {self.get_access_token()}"
        }
        return headers

    def search(self, query, search_type='track'):
        endpoint = "https://api.spotify.com/v1/search"
        headers = self.get_resource_header()
        data = urlencode({"q": query, "type": search_type.lower()})
        lookup_url = f"{endpoint}?{data}"
        r = requests.get(lookup_url, headers=headers)

        valid_request = r.status_code in range(200, 299)
        if not valid_request:
            return {}
        return r.json()

    def get_resource(self, resource_id, resource_type="tracks", version="v1"):
        endpoint = f"https://api.spotify.com/{version}/{resource_type}/{resource_id}"
        headers = self.get_resource_header()
        r = requests.get(endpoint, headers=headers)
        valid_request = r.status_code in range(200, 299)
        if not valid_request:
            return {}
        return r.json()

    def get_album(self, album_id):
        return self.get_resource(album_id, "albums")

    def get_artist(self, artist_id):
        return self.get_resource(artist_id, "artists")

    def get_track(self, track_id):
        return self.get_resource(track_id, "tracks")

    def get_playlist(self, playlist_id):
        return self.get_resource(playlist_id, "playlists")

    def get_all_playlist_items(self, playlist_id, version="v1"):
        headers = self.get_resource_header()
        still_items, items_read, return_items = True, 0, []

        while still_items:
            endpoint = f"https://api.spotify.com/{version}/playlists/{playlist_id}/tracks?limit=100&offset={items_read}"
            r = requests.get(endpoint, headers=headers)
            valid_request = r.status_code in range(200, 299)
            if not valid_request:
                return {}
            return_items += r.json()['items']  # merge the newly returned json object with the existing json objects
            items_read += len(r.json()['items'])
            if len(r.json()['items']) == 0:  # if the end of the playlist has been reached
                still_items = False
        return return_items

    def get_episode(self, episode_id):
        return self.get_resource(episode_id, "episodes")

    def get_audiobook(self, audiobook_id):
        return self.get_resource(audiobook_id, "audiobooks")
