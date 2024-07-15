import logging
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

RADARR_API_KEY = 'your_radarr_api_key'
SONARR_API_KEY = 'your_sonarr_api_key'
OVERSEERR_API_KEY = 'your_overseerr_api_key'

RADARR_URL = 'http://localhost:7878/api/v3'
SONARR_URL = 'http://localhost:8989/api/v3'
OVERSEERR_URL = 'http://localhost:5055/api/v1'

def check_radarr(movie_id):
    response = requests.get(f'{RADARR_URL}/movie/{movie_id}', headers={'X-Api-Key': RADARR_API_KEY})
    return response.status_code == 404

def check_sonarr(series_id):
    response = requests.get(f'{SONARR_URL}/series/{series_id}', headers={'X-Api-Key': SONARR_API_KEY})
    return response.status_code == 404

def remove_overseerr_status(media_id, media_type):
    requests.delete(f'{OVERSEERR_URL}/request/{media_id}', headers={'X-Api-Key': OVERSEERR_API_KEY})

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    media_type = data.get('mediaType')
    media_id = data.get('mediaId')

    if media_type == 'movie':
        if check_radarr(media_id):
            remove_overseerr_status(media_id, media_type)
    elif media_type == 'tv':
        if check_sonarr(media_id):
            remove_overseerr_status(media_id, media_type)

    return jsonify({'status': 'success'}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
