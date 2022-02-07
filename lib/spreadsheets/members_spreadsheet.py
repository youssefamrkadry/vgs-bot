import gspread

# import datetime
# from gspread_formatting import *

gc = gspread.service_account(filename='lib/spreadsheets/credentials.json')
# gc = gspread.service_account(filename='credentials.json')
sh_members = gc.open("MEMBERS 2022")
sh_attendance = gc.open("VGS Attendance Form (Responses)")
sh_xp = gc.open("VGS XP Form (Responses)")


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
        for member in members:
            members_parsed = members_parsed + member[0] + "\t" + member[1] + "\n"
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
    attendance_xp = 0
    misc_xp = 0
    report = ""

    worksheet = sh_attendance.worksheet("Form Responses 1")
    worksheet_values = worksheet.get_all_values()
    for row in worksheet_values:
        for cell in row:
            if f"[{member_id}]" in cell:
                attendance_xp += 1
    report += f"Attendance: {attendance_xp}\n"

    worksheet = sh_xp.worksheet("Form Responses 1")
    instances = worksheet.findall(f"{member_id}")
    for cell in instances:
        xp_inc = int(worksheet.cell(cell.row, cell.col + 1).value)
        justification = worksheet.cell(cell.row, cell.col + 2).value
        misc_xp += xp_inc
        report += f"{justification}: {xp_inc}\n"

    total_xp = attendance_xp + misc_xp
    report += f"\nTotal XP is {total_xp}"

    return report
