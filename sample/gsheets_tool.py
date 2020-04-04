from __future__ import print_function
import config
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# NOTICE: If modifying scopes, delete the file token.pickle.


# Authenticates by creating token.pickle, if one doesn't already exist and sets up service object
def authenticate_sheets_api():
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'client_secrets_file.json', "https://www.googleapis.com/auth/spreadsheets")
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('sheets', 'v4', credentials=creds)

    return service


# Returns all data in spreadsheet
def get_all_sheets_data(current_service, sheet_id, sheet_range):
    # Call the Sheets API
    sheet = current_service.spreadsheets()
    result = sheet.values().get(spreadsheetId=sheet_id, range=sheet_range).execute()
    values = result.get('values', [])

    return values


# returns data row at specific location
# uses "code style" list indexing, which means the first row is row "0"
def get_specific_sheet_pair_data(current_service, sheet_id, row, sheet_range="A:B"):
    # Call the Sheets API
    sheet = current_service.spreadsheets()
    result = sheet.values().get(spreadsheetId=sheet_id, range=sheet_range).execute()
    values = result.get('values', [])
    row_values = values[row]

    return row_values


# returns single data at specific location
# uses "code style" list indexing, which means the first row is row "0"
def get_specific_sheet_single_data(current_service, sheet_id, row, column, sheet_range="A:B"):
    # Call the Sheets API
    sheet = current_service.spreadsheets()
    result = sheet.values().get(spreadsheetId=sheet_id, range=sheet_range).execute()
    values = result.get('values', [])
    row_values = values[row]
    single = row_values[column]

    return single


# writes a pair of values to a specific row in a sheet (in columns 0 and 1)
def write_data_pair_to_sheet(current_service, sheet_id, sheet_range, data_first, data_second, notify=False):
    values = [[data_first, data_second]]

    body = {
        'values': values
    }
    result = current_service.spreadsheets().values().append(
        spreadsheetId=sheet_id, range=sheet_range,
        valueInputOption="RAW", body=body).execute()

    # notify action performed if desired
    if notify:
        print('{0} cells appended.'.format(result.get('updates').get('updatedCells')))


# This can be used to write an entire list to one row in a sheet. Each item in the list will be in its own column
# This can also be useful for entering a single data value instead of a pair.
def write_data_list_to_sheet(current_service, sheet_id, sheet_range, data_list, notify=False):
    values = [data_list]

    body = {
        'values': values
    }
    result = current_service.spreadsheets().values().append(
        spreadsheetId=sheet_id, range=sheet_range,
        valueInputOption="RAW", body=body).execute()

    # notify action performed if desired
    if notify:
        print('{0} cells appended.'.format(result.get('updates').get('updatedCells')))


# Lays out the code flow, runs sample if called directly
def main():
    service = authenticate_sheets_api()
    current_sheet_id = config.song_log_sheet_id

    print(get_all_sheets_data(service, current_sheet_id, "A:B"))

    print(get_specific_sheet_pair_data(service, current_sheet_id, 4))  # using default range ("A:B")

    print(get_specific_sheet_single_data(service, current_sheet_id, 4, 0))  # using default range ("A:B")
    print(get_specific_sheet_single_data(service, current_sheet_id, 4, 1))  # using default range ("A:B")

    write_data_pair_to_sheet(service, current_sheet_id, "A:B", "the song 1", "the artist 1")
    write_data_pair_to_sheet(service, current_sheet_id, "A:B", "the song 1", "the artist 1", True)  # notifies

    write_data_list_to_sheet(service, current_sheet_id, "A:B", ["value A", "value B", "value C", "value D"])
    write_data_list_to_sheet(service, current_sheet_id, "A:B", ["value A", "value B", "value C", "value D"], True)


# runs main (sample) if called directly
if __name__ == '__main__':
    main()
