import requests
import pytest

@pytest.mark.unit
def test_spotify_search_status(spotify_token):
    headers = {"Authorization": f"Bearer {spotify_token}"}
    response = requests.get(
        "https://api.spotify.com/v1/search",
        params={"q": "podcast", "type": "show"},
        headers=headers
    )
    assert response.status_code == 200

@pytest.mark.integration
def test_spotify_search_track(spotify_token):
    query = "Bohemian Rhapsody"
    headers = {"Authorization": f"Bearer {spotify_token}"}
    response = requests.get(
        "https://api.spotify.com/v1/search",
        params={"q": query, "type": "track"},
        headers=headers
    )

    assert response.status_code == 200

    data = response.json()
    assert "tracks" in data
    assert len(data["tracks"]["items"]) > 0
    track = data["tracks"]["items"][0]
    assert query.lower() in track["name"].lower()

