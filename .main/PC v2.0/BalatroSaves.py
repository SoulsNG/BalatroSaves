import os
import io
import shutil
from datetime import *
import sys

#google imports
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from googleapiclient.http import MediaIoBaseDownload
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/drive']
PARENT_FOLDER_ID = "paste folder ID here" # ID for savesBalatro folder on Google Drive

def list_folder(drive_service, parent_folder_id=None, delete=False):
    file_data = {}
    page_token = None
    
    # getting the files with google api
    while True:
        results = drive_service.files().list(
            q=f"'{parent_folder_id}' in parents and trashed=false" if parent_folder_id else None,
            pageSize=1000,
            fields="nextPageToken, files(id, name, mimeType, modifiedTime, size)",
            pageToken=page_token  
        ).execute()

        items = results.get('files', [])
        
        # putting the results to the dictionary and handling the repeated file names
        for item in items:
            file_name = item['name']
            file_id = item['id']
            file_size = item['size']

            # converting time spit out by the google drive to unix time for easy comparing
            file_mtime_iso = datetime.strptime(item['modifiedTime'], "%Y-%m-%dT%H:%M:%S.%fZ") 
            file_mtime = int(file_mtime_iso.replace(tzinfo=timezone.utc).timestamp()) #get the correct timestamp of the seconds since the epoch

            if file_name in file_data:
                file_data[file_name].append((file_id, file_mtime, file_size))  # thanks daddy chatgpt for tuple tutorial - i understand it now
            else:
                file_data[file_name] = [(file_id, file_mtime, file_size)]  # OMG TUPLE AGAIN

        page_token = results.get('nextPageToken')
        if not page_token:
            break

    return file_data

def get_saves(drive_service, drive_files_dic):
    files_to_upload = None
    
    home_dir = os.path.expanduser("~")  # Expands "~" to the actual home directory
    balatro_dir = os.path.join(home_dir, "AppData", "Roaming", "Balatro", "1")
    src_files = os.listdir(balatro_dir)
    
    for file_name in src_files:
        full_file_name = os.path.join(balatro_dir, file_name)
        if file_name in drive_files_dic and files_to_upload != True:
            drive_files_mdata = drive_files_dic.get(file_name)[0][1]
            os_files_mdata = int(os.path.getmtime(full_file_name))
            os_files_size = os.path.getsize(full_file_name)
            drive_files_size = int(drive_files_dic.get(file_name)[0][2])
            print("drive: " + str(drive_files_size))
            print("os: " + str(os_files_size))
            print("os_files_mdata: " + str(os_files_mdata))
            print("drive_files_mdata: " + str(drive_files_mdata))

            # we check size also for double measure but it doesn't work with saves.jkr cause its size varies a lot
            if file_name != "save.jkr":
                if os_files_mdata > drive_files_mdata and os_files_size > drive_files_size:
                    files_to_upload = True
                else:
                    print("No new files to upload. Begining download of files...")
            else:
                if os_files_mdata > drive_files_mdata:
                    files_to_upload = True
                else:
                    print("No new files to upload. Begining download of files...")

        elif not drive_files_dic:
            files_to_upload = True

    if files_to_upload == True:
       print("Files to upload: " + str(src_files))
       return src_files
    else:
       print("No files to upload. Downloading...")
       return False

def upload_files(drive_service, drive_files_dic, files_to_upload):
    # deleting old files from drive
    drive_files = list(drive_files_dic.keys())
    for drive_file_name in drive_files:
        try:
            drive_service.files().delete(fileId=drive_files_dic.get(drive_file_name)[0][0]).execute()
            print(f"Successfully deleted file/folder with ID: {drive_files_dic.get(drive_file_name)[0][0]}")
        except Exception as e:
            print(f"Error deleting file/folder with ID: {drive_files_dic.get(drive_file_name)[0][0]}")
            print(f"Error details: {str(e)}")
     
    # uploading saves
    home_dir = os.path.expanduser("~")  # Expands "~" to the actual home directory
    balatro_dir = os.path.join(home_dir, "AppData", "Roaming", "Balatro", "1")
    for file_name in files_to_upload:
        file_metadata = {
            'name' : file_name,
            'parents' : [PARENT_FOLDER_ID],
        }

        full_file_name = os.path.join(balatro_dir, file_name)
        # shutil.copy(full_file_name, r"saves_copy")
        # print(file_name + " copied!")

        # full_file_name_copied = os.path.join(r"saves_copy", file_name)

        # google doesnt know .jkr files balatro uses so we use generic MIME type that just tells google its a binary file
        media = MediaFileUpload(full_file_name, mimetype='application/octet-stream')
        
        file = drive_service.files().create(body=file_metadata, media_body=media).execute()
        
        print(f"File uploaded: {file.get('id')}")

def download_files(drive_service, drive_files_dic):
    drive_files = list(drive_files_dic.keys())
    
    home_dir = os.path.expanduser("~")  # Expands "~" to the actual home directory
    balatro_dir = os.path.join(home_dir, "AppData", "Roaming", "Balatro", "1")
    src_files = os.listdir(balatro_dir)
    
    #delete files from the balatro1 folder
    for file_name in src_files:
        full_file_name = os.path.join(balatro_dir, file_name)
        os.remove(full_file_name)
        print(f"Deleted {file_name} old save from balatro save folder")

    #download files
    for drive_file_name in drive_files:
        try:
            request = drive_service.files().get_media(fileId=drive_files_dic.get(drive_file_name)[0][0])
            destination_path = os.path.join(balatro_dir, drive_file_name)
            fh = io.FileIO(destination_path, mode='wb')
            
            downloader = MediaIoBaseDownload(fh, request)
            
            done = False
            while not done:
                status, done = downloader.next_chunk()
                print(f"Download {int(status.progress() * 100)}%.")
            print("Download complete!")

        except Exception as e:
            print(f"Error downloading file/folder with ID: {drive_files_dic.get(drive_file_name)[0][0]}")
            print(f"Error details: {str(e)}")

def main():
  """Shows basic usage of the Drive v3 API.
  Prints the names and ids of the first 10 files the user has access to.
  """
  creds = None
  # The file token.json stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time.
  if os.path.exists("credentials/token.json"):
    creds = Credentials.from_authorized_user_file("credentials/token.json", SCOPES)
  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
          "credentials/credentials.json", SCOPES
      )
      creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open("credentials/token.json", "w") as token:
      token.write(creds.to_json())

  try:
    drive_service = build("drive", "v3", credentials=creds)

    drive_files_dic = list_folder(drive_service, PARENT_FOLDER_ID)
    files_to_upload = get_saves(drive_service, drive_files_dic)
    print(files_to_upload)

    # autorun.bat integration
    if len(sys.argv) > 1:
        autorun_value = int(sys.argv[1])
        if autorun_value == 0:
            if files_to_upload == False:
                download_files(drive_service, drive_files_dic)
        elif autorun_value == 1:
            if files_to_upload:
                upload_files(drive_service, drive_files_dic, files_to_upload)
    else:
        print("No special argument provided!")
        if files_to_upload == False:
            download_files(drive_service, drive_files_dic)
        else:
            upload_files(drive_service, drive_files_dic, files_to_upload)

  except HttpError as error:
    print(f"An error occurred: {error}")
  

if __name__ == "__main__":
  main()