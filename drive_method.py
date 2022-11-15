from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

import configparser

config = configparser.ConfigParser()
config.read('config.ini')

def authorize_drive():
        gauth = GoogleAuth()
        gauth.DEFAULT_SETTINGS['client_config_file'] = "client_secret.json"

        gauth.LoadCredentialsFile("mycreds.txt")
        if gauth.credentials is None:
            # Authenticate if they're not there
            gauth.LocalWebserverAuth()
        elif gauth.access_token_expired:
        # Refresh them if expired
            gauth.Refresh()
        else:
            # Initialize the saved creds
            gauth.Authorize()
        # Save the current credentials to a file
        gauth.SaveCredentialsFile("mycreds.txt")
        
        return GoogleDrive(gauth)

class drive_method(object):

    def download(self, local_path, file_id):
        file = self.drive.CreateFile({'id': file_id})
        file.GetContentFile(local_path)
        print('download done')

    def update(self, local_path, file_id):
        file = self.drive.CreateFile({'id': file_id})
        file.SetContentFile(local_path)
        file.Upload()
        print('update done')

    def __init__(self):
        self.drive = authorize_drive()