import os

class SpotifyApi:
    """
    A client for interacting with the Spotify Web API.
    """
    # Convention: The STATUS is determined by checking an environment variable.
    STATUS = "API Key Loaded" if os.environ.get("SPOTIFY_API_KEY") else "⚠️ No API Key"

    def get_playlist(self, user_id: str, playlist_id: str):
        """Fetches a specific playlist for a user."""
        pass

    def search_track(self, track_name: str):
        """Searches for a track."""
        pass
