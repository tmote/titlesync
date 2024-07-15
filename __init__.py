import logging
import requests
import json
import os
import azure.functions as func

RADARR_API_KEY = os.getenv('RADARR_API_KEY')
SONARR_API_KEY = os.getenv('SONARR_API_KEY')
OVERSEERR_API_KEY = os.getenv('OVERSEERR_API_KEY')

RADARR_URL = os.getenv('RADARR_URL')
SONARR_URL = os.getenv('SONARR_URL')
OVERSEERR_URL = os.getenv('OVERSEERR_URL')

def check_radarr(movie_id):
    response = requests.get(f'{RADARR_URL}/movie/{movie_id}', headers={'X-Api-Key': RADARR_API_KEY})
    return response.status_code == 404

def check_sonarr(series_id):
    response = requests.get(f'{SONARR_URL}/series/{series_id}', headers={'X-Api-Key': SONARR_API_KEY})
    return response.status_code == 404

def remove_overseerr_status(media_id, media_type):
    requests.delete(f'{OVERSEERR_URL}/request/{media_id}', headers={'X-Api-Key': OVERSEERR_API_KEY})

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    try:
        data = req.get_json()
    except ValueError:
        return func.HttpResponse(
            "Invalid JSON",
            status_code=400
        )

    media_type = data.get('mediaType')
    media_id = data.get('mediaId')

    if media_type == 'movie':
        if check_radarr(media_id):
            remove_overseerr_status(media_id, media_type)
    elif media_type == 'tv':
        if check_sonarr(media_id):
            remove_overseerr_status(media_id, media_type)

    return func.HttpResponse(
        json.dumps({'status': 'success'}),
        mimetype="application/json",
        status_code=200
    )
