import config
from spotify_controller_repo.sample import gsheets_tool


# Google Sheets Authentication
service = gsheets_tool.authenticate_sheets_api()
# Blacklist sheet:
blacklist_sheet_id = config.blacklist_sheet_id


def blacklist_song_title(title):
    gsheets_tool.write_data_list_to_sheet(service, blacklist_sheet_id, "A:B", [title])

