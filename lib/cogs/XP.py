from discord.ext.commands import Cog
from discord.ext.commands import command
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
    async def get_xp_report(self, ctx: Context):

        member = members_spreadsheet.find_member_discord(ctx.author.id)
        if member is None:
            await ctx.send(f"Hi {ctx.author.mention}!\nYou are not registered yet, register yourself first!")
        else:
            await ctx.author.send(members_spreadsheet.calc_xp_report(member['id']))
            await ctx.send(f"Hi {ctx.author.mention}!\nYour XP details are on private.")


def setup(bot):
    bot.add_cog(XP(bot))
