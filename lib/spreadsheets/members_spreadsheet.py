import gspread

# import datetime
# from gspread_formatting import *

gc = gspread.service_account(filename='lib/spreadsheets/credentials.json')
# gc = gspread.service_account(filename='credentials.json')
sh = gc.open("MEMBERS 2022")


def find_member(member_id):
    for sheet in sh.worksheets():
        if (member_cell := sheet.find(str(member_id))) is not None:
            name = sheet.cell(member_cell.row, 2).value
            committee = sheet.title
            return {"name": name, "committee": committee, "id": member_id}
    return None


def list_ids(committee_name):
    members_parsed = ""
    try:
        members = sh.worksheet(committee_name).get_all_values()
        for member in members:
            members_parsed = members_parsed + member[0] + "\t" + member[1] + "\n"
        return members_parsed
    except gspread.exceptions.WorksheetNotFound:
        return None
