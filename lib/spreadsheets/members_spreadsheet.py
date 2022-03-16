from webbrowser import get
import gspread
import re

# import datetime
# from gspread_formatting import *

gc = gspread.service_account(filename='lib/spreadsheets/credentials.json')
# gc = gspread.service_account(filename='credentials.json')
sh_members = gc.open("MEMBERS 2022")
sh_xp = gc.open("VGS XP Form (NEW) (Responses)")


def find_member(member_id):
    for sheet in sh_members.worksheets():
        if (member_cell := sheet.find(str(member_id))) is not None:
            name = sheet.cell(member_cell.row, 2).value
            committee = sheet.title
            return {"name": name, "committee": committee, "id": member_id}
    return None


def find_member_discord(discord_id):
    for sheet in sh_members.worksheets():
        if (member_cell := sheet.find(str(discord_id))) is not None:
            member_id = sheet.cell(member_cell.row, 1).value
            name = sheet.cell(member_cell.row, 2).value
            committee = sheet.title
            return {"name": name, "committee": committee, "id": member_id}
    return None


def list_ids(committee_name):
    members_parsed = ""
    try:
        members = sh_members.worksheet(committee_name).get_all_values()
        members_parsed += "```"
        for member in members:
            members_parsed = members_parsed + member[0] + "\t" + member[1] + "\n"
        members_parsed += "```"
        return members_parsed
    except gspread.exceptions.WorksheetNotFound:
        return None


def register(member_id, discord_id, admin):

    member = find_member_discord(discord_id)
    if member is not None:
        # this person is already registered with an id
        return 1

    for sheet in sh_members.worksheets():
        member_cell = sheet.find(str(member_id))
        if member_cell is None:
            # member id does not exist in this sheet
            continue

        if sheet.cell(member_cell.row, member_cell.col + 2).value is not None:
            if admin:
                sheet.update_cell(member_cell.row, member_cell.col + 2, str(discord_id))
                return 0
            # id already registered by another person
            return 2
        else:
            # successful registration
            sheet.update_cell(member_cell.row, member_cell.col + 2, str(discord_id))
            return 0

    # member id does not exist at all
    return 3


def unregister(discord_id):
    for sheet in sh_members.worksheets():
        member_cell = sheet.find(str(discord_id))
        if member_cell is None:
            # discord id does not exist in this sheet
            continue
        # delete discord id from this member
        sheet.update_cell(member_cell.row, member_cell.col, "")
        return 0

        # member didn't register in the first place
    return 1


def calc_xp_report(member_id):
    return calc_xp_report_helper(member_id,
    sh_xp.worksheet("Form Responses 1").get_all_values()
    )


def calc_xp_report_helper(member_id, xp_ws):
    xp = 0
    total_xp = 0
    attendance = 0
    report = ""

    worksheet = xp_ws
    for response in worksheet:
        response = [s for s in response if s]
        if str(member_id) in response[4]:
            reason = response[5] # increase in xp
            if "Attendance" in reason:
                attendance += 1
            xp = int(reason[reason.find("[")+1:reason.find("XP]")])
            total_xp += xp
            justification = response[6] # justification
            report += f"{justification}: {xp}XP\n"

    report += f"--------\nAttended {attendance} sessions/meetings\n"
    report += f"Total XP is {total_xp}\n\n\n"
    return report


def get_committee_report(committee):
    report = f"=========== {committee} COMMITTEE REPORT ===========\n\n"
    try:
        committee_ws = sh_members.worksheet(committee).get_all_values()
        xp_ws = sh_xp.worksheet("Form Responses 1").get_all_values()
        for member in committee_ws:
            report += member[0] + "\t" + member[1] + "\n" # [ID, Name]
            report += calc_xp_report_helper(member[0], xp_ws)
        return report
    except gspread.exceptions.WorksheetNotFound:
        return None