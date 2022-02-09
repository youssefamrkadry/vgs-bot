from discord.ext import commands
from discord.ext.commands import Cog
from discord.ext.commands import command
from discord.ext.commands import has_permissions
from discord.ext.commands import Context
from ..spreadsheets import members_spreadsheet


class XP(Cog):
    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("XP")

    @command(name="my_xp")
    async def my_xp(self, ctx: Context):

        member = members_spreadsheet.find_member_discord(ctx.author.id)
        if member is None:
            await ctx.send(f"Hi {ctx.author.mention}!\nYou are not registered yet, register yourself first.")
        else:
            await ctx.author.send(members_spreadsheet.calc_xp_report(member['id']))
            await ctx.send(f"Hi {ctx.author.mention}!\nYour XP details are on private.")
    
    @command(name="committee_report")
    @has_permissions(administrator=True)
    async def get_committee_report(self, ctx: Context, committee):

        if committee is None:
            await ctx.send(f"Hi {ctx.author.mention}!\nYou must select a committee from [CL] [MRKT] [FR] [HR] [MD]\nexample: -committee_report CL")

        report = members_spreadsheet.get_committee_report(committee)
        if report is None:
            await ctx.send(f"Hi {ctx.author.mention}!\n{committee} is not a valid committee")
        else:
            await ctx.author.send(report)
            await ctx.send(f"Hi {ctx.author.mention}!\nCommittee report is on private.")
    
    @get_committee_report.error
    async def error(self, ctx: Context, error: commands.CommandError):
        if isinstance(error, commands.MissingPermissions):
            message = f"Hey, you don't have permission to do this!"
        elif isinstance(error, commands.MissingRequiredArgument):
            message = f"Missing a required argument: {error.param}\nPlease use -help for more info."
        else:
            message = "An error has occured while using the command, please report to a supervisor!"
            print(error)

        await ctx.send(message)


def setup(bot):
    bot.add_cog(XP(bot))
