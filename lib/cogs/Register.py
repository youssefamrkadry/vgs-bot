from discord.ext.commands import Cog
from discord.ext.commands import command
from discord.ext.commands import Context
from discord import Embed
from ..db import db
from ..spreadsheets import members_spreadsheet


class Register(Cog):
    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("Register")

    @command(name="register_self")
    async def register_member(self, ctx: Context, member_id):

        if (member_data := members_spreadsheet.find_member(member_id)) is not None:
            member_name = member_data["name"]
            member_committee = member_data["committee"]

            # if this member is already registered
            prev_entry = db.record("SELECT MemberID FROM members "
                                   f"WHERE UserID = {ctx.author.id}")
            if prev_entry:
                await ctx.send(f"Hi {ctx.author.mention}!\nYou are already registered as {prev_entry[0]}, you'll have to unregister before registering again.")
                return

            # if a member already is registered with this id
            prev_entry = db.record("SELECT UserID FROM members "
                                   f"WHERE MemberID = {member_id}")
            if prev_entry:
                await ctx.send(
                    f"Hi {ctx.author.mention}!\nThis ID is already taken by <@{prev_entry[0]}>, if you believe it's yours please contact your supervisor.")
                return

            db.execute("INSERT INTO members"
                       "(MemberID, UserID, Name, Committee)"
                       "VALUES"
                       f"({member_id}, {ctx.author.id}, '{member_name}', '{member_committee}')")

            reg_embed = Embed(color=0xFF0000, title="You have been registered!").set_thumbnail(url=self.bot.icon)

            reg_embed.add_field(name="You are Registered as",
                                value=f"Name: {member_name}\n"
                                      f"Member ID: {member_id}\n"
                                      f"Committee: {member_committee}\n",
                                inline=False)

            await ctx.send(embed=reg_embed)

        else:

            await ctx.send(f"Hi {ctx.author.mention}!\nTThere is no record of this ID, list IDs to find your correct ID!")

    @command(name="register_member")
    async def register_member_admin(self, ctx: Context, member_id):

        member_user = ctx.message.mentions[0]

        if (member_data := members_spreadsheet.find_member(member_id)) is not None:
            member_name = member_data["name"]
            member_committee = member_data["committee"]

            # if this member is already registered
            prev_entry = db.record("SELECT MemberID FROM members "
                                   f"WHERE UserID = {member_user.id}")
            if prev_entry:
                await ctx.send(
                    f"Hi {ctx.author.mention}!\nMember already registered as {prev_entry[0]}, you'll have to unregister them before registering again.")
                return

            # if a member already is registered with this id
            prev_entry = db.record("SELECT UserID FROM members "
                                   f"WHERE MemberID = {member_id}")
            if prev_entry:
                await ctx.send(
                    f"Hi {ctx.author.mention}!\nThis ID is already taken by <@{prev_entry[0]}>, if it's not theirs unregister them.")
                return

            db.execute("INSERT INTO members"
                       "(MemberID, UserID, Name, Committee)"
                       "VALUES"
                       f"({member_id}, {member_user.id}, '{member_name}', '{member_committee}')")

            reg_embed = Embed(color=0xFF0000, title="You have been registered!").set_thumbnail(url=self.bot.icon)

            reg_embed.add_field(name="You are Registered as",
                                value=f"Name: {member_name}\n"
                                      f"Member ID: {member_id}\n"
                                      f"Committee: {member_committee}\n",
                                inline=False)

            await ctx.send(embed=reg_embed)

        else:

            await ctx.send(
                f"Hi {ctx.author.mention}!\nThere is no record of this ID, list IDs to find their correct ID!")

    @command(name="unregister_self")
    async def unregister_member(self, ctx: Context):

        prev_entry = db.record("SELECT UserID FROM members "
                               f"WHERE UserID = {ctx.author.id}")
        if prev_entry:
            db.execute("DELETE FROM members "
                       f"WHERE UserID = {ctx.author.id}")
            await ctx.send(f"Hi {ctx.author.mention}!\nYou have been successfully unregistered!")
        else:
            await ctx.send(f"Hi {ctx.author.mention}!\nYou are not registered in the first place!")

    @command(name="unregister_member")
    async def unregister_member_admin(self, ctx: Context):

        member_user = ctx.message.mentions[0]

        prev_entry = db.record("SELECT UserID FROM members "
                               f"WHERE UserID = {member_user.id}")
        if prev_entry:
            db.execute("DELETE FROM members "
                       f"WHERE UserID = {member_user.id}")
            await ctx.send(f"Hi {ctx.author.mention}!\n<@{prev_entry[0]}> has been successfully unregistered!")
        else:
            await ctx.send(f"Hi {ctx.author.mention}!\nThis member isn't registered in the first place!")

    @command(name="list_ids")
    async def list_ids(self, ctx: Context, member_committee):

        if (ids := members_spreadsheet.list_ids(member_committee)) is not None:

            ids_embed = Embed().set_thumbnail(url=self.bot.icon)

            ids_embed.add_field(name=f"{member_committee} Members:\n",
                                value=ids,
                                inline=False)

            await ctx.send(embed=ids_embed)

        else:

            await ctx.send(f"Hi {ctx.author.mention}!\n{member_committee} is not a valid committee")


def setup(bot):
    bot.add_cog(Register(bot))
