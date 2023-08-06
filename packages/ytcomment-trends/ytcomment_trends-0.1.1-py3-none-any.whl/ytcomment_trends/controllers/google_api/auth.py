import os
import pickle
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

class GoogleAPIAuth:
    """Google API OAuth2.0 authentication class
    """

    def __init__(self, client_secret_json):
        self.CLIENT_SECRETS_FILE = client_secret_json
        self.SCOPES = ['https://www.googleapis.com/auth/youtubepartner', 'https://www.googleapis.com/auth/youtube', 'https://www.googleapis.com/auth/youtube.force-ssl']
        self.API_SERVICE_NAME = 'youtube'
        self.API_VERSION = 'v3'

    def get_authenticated_service(self):
        """Initialize Google Auth service

        Returns:
            googleapiclient object
        """
        if os.path.exists("CREDENTIALS_PICKLE_FILE"):
            with open("CREDENTIALS_PICKLE_FILE", 'rb') as f:
                credentials = pickle.load(f)
        else:
            flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(self.CLIENT_SECRETS_FILE, self.SCOPES)
            credentials = flow.run_console()
            with open("CREDENTIALS_PICKLE_FILE", 'wb') as f:
                pickle.dump(credentials, f)
        return googleapiclient.discovery.build(self.API_SERVICE_NAME, self.API_VERSION, credentials=credentials)