import pandas as pd
import requests
import base64
import json

# Load your dataset
file_path = 'path_to_your_csv.csv'
spotify_data = pd.read_csv(file_path, encoding='ISO-8859-1')

# Spotify API credentials (replace with your actual credentials)
client_id = 'your_client_id'
client_secret = 'your_client_secret'

# Function to get Spotify API token
def get_spotify_token(client_id, client_secret):
    auth_url = 'https://accounts.spotify.com/api/token'
    auth_headers = {
        'Authorization': 'Basic ' + base64.b64encode(f"{client_id}:{client_secret}".encode()).decode()
    }
    auth_data = {
        'grant_type': 'client_credentials'
    }
    response = requests.post(auth_url, headers=auth_headers, data=auth_data)
    return response.json().get('access_token')

# Function to search for a track and get the cover URL
def get_cover_url(track_name, artist_name, token):
    search_url = f"https://api.spotify.com/v1/search?q=track:{track_name}%20artist:{artist_name}&type=track"
    headers = {
        'Authorization': f'Bearer {token}'
    }
    response = requests.get(search_url, headers=headers)
    results = response.json()
    try:
        # Get the first track's album cover URL
        cover_url = results['tracks']['items'][0]['album']['images'][0]['url']
        return cover_url
    except (IndexError, KeyError):
        return None

# Get Spotify token
token = get_spotify_token(client_id, client_secret)

# Add a new column for cover URLs
spotify_data['cover_url'] = spotify_data.apply(
    lambda row: get_cover_url(row['track_name'], row["artist(s)_name"], token), axis=1
)

# Save the updated dataset
spotify_data.to_csv('spotify_data_with_covers.csv', index=False)
