#!/usr/bin/python
from __future__ import print_function
import httplib2
import os
import sys
import csv

from apiclient import discovery
import oauth2client
from oauth2client import client
from oauth2client import tools

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/checksums_google_drive.json
SCOPES = 'https://www.googleapis.com/auth/drive.metadata.readonly'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'checksums_google_drive'

def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'checksums_google_drive.json')

    store = oauth2client.file.Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def get_google_photos_folder(service):
    q = "name='Google Photos' and mimeType='application/vnd.google-apps.folder' and 'root' in parents and trashed=false"
    response = service.files().list(
        q=q, pageSize=1000, fields="nextPageToken, files(id, name)").execute()
    items = response.get('files', [])

    if not items:
        print('ERROR: Google Photos directory not found.')
        return

    if len(items) > 1:
        print('ERROR: Found multiple Google Photos directories.')
        for item in items:
            print('{0} ({1})'.format(item['name'], item['id']))
        return

    return items[0]

def get_sub_folders_recursive(service, parent):
    q = "mimeType='application/vnd.google-apps.folder' and '{0}' in parents and trashed=false".format(parent['id'])
    response = service.files().list(
        q=q, pageSize=1000, fields="nextPageToken, files(id, name)").execute()
    children = response.get('files', [])

    if not children:
        return

    for child in children:
        child['path'] = parent['path'] + '/' + child['name']

    folders = children

    for child in children:
        sub_folders = get_sub_folders_recursive(service, child)

        if sub_folders:
            folders += sub_folders

    return folders

def get_images(service, folder):
    files = []
    page_token = None

    while True:
        # TODO use spaces='drive' or spaces='photos'?
        q = "'{0}' in parents and (mimeType contains 'image/' or mimeType contains 'video/') and trashed=false".format(folder['id'])
        response = service.files().list(
            q=q, pageToken=page_token, pageSize=1000, fields="nextPageToken, files(id, name, md5Checksum)").execute()

        files += response.get('files', [])
        
        page_token = response.get('nextPageToken', None)
        if page_token is None:
            break;

    return files

def main():
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('drive', 'v3', http=http)

    photos_folder = get_google_photos_folder(service)

    if not photos_folder:
        print("ERROR: Cannot find Google Photos folder")
        sys.exit(-1)

    photos_folder['path'] = ''
    folders = get_sub_folders_recursive(service, photos_folder)

    folders.insert(0, photos_folder)

    with open('checksums_google_drive.tsv', 'wb') as fout:
        writer = csv.writer(fout, delimiter='\t', quotechar='\"', quoting=csv.QUOTE_MINIMAL)

        for folder in folders:
            images = get_images(service, folder)

            for image in images:
                if 'md5Checksum' in image.keys():
                    writer.writerow([folder['path'], image['name'], image['md5Checksum']])
                else:
                    print('ERROR: No MD5 checksum for file: {0}/{1} '.format(folder['path'], image['name']))

if __name__ == '__main__':
    main()
