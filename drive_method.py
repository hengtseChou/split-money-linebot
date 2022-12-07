from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import pandas as pd
from datetime import datetime, timedelta


# load/refresh access token and save to local
def authorize_drive():
        gauth = GoogleAuth()
        gauth.DEFAULT_SETTINGS['client_config_file'] = "config/client_secret.json"

        gauth.LoadCredentialsFile("config/mycreds.txt")
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
        gauth.SaveCredentialsFile("config/mycreds.txt")
        
        return GoogleDrive(gauth)


# drive method: for a given file in google drive, it can be downloaded or uploaded
# file name and id must be consistent
class drive_method(object):

    def __init__(self, local_path, file_id):
        self.drive = authorize_drive()
        self.local_path = local_path
        self.file_id = file_id

    def download(self):
        file = self.drive.CreateFile({'id': self.file_id})
        file.GetContentFile(self.local_path)
        # print('download done')

    def upload(self):
        file = self.drive.CreateFile({'id': self.file_id})
        file.SetContentFile(self.local_path)
        file.Upload(param = {'convert':True})
        # print('update done')

    

# adding new entry to ledger.csv via drive_method object
def new_entry(drive_object, payer, amount):

    drive_object.download() 
            
    df = pd.read_csv('ledger.csv')
    now_time_gmt_plus_8 = datetime.now() + timedelta(hours=8)
    if payer == 'lala':
        new_row = pd.Series({'date': now_time_gmt_plus_8.strftime("%m/%d"), 'hank': 0, 'lala': amount})
    elif payer == 'hank':
        new_row = pd.Series({'date': now_time_gmt_plus_8.strftime("%m/%d"), 'hank': amount, 'lala': 0})
    df = pd.concat([df, new_row.to_frame().T], ignore_index=True)
    df.to_csv('ledger.csv', index=False)

    drive_object.upload()

