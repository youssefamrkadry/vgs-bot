from discord.ext import commands
from discord.ext.commands import Cog
from discord.ext.commands import command
from discord.ext.commands import has_permissions
from discord.ext.commands import Context
from discord import Embed
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

        exit_code = members_spreadsheet.register(
            member_id, ctx.author.id, False)
        if exit_code == 0:
            await ctx.send(f"Hi {ctx.author.mention}!\nYou are now registered with the ID {member_id}!")
        elif exit_code == 1:
            await ctx.send(f"Hi {ctx.author.mention}!\nYou are already registered , you'll have to unregister before registering again.")
        elif exit_code == 2:
            await ctx.send(f"Hi {ctx.author.mention}!\nThis ID is already taken, if you believe it's yours please contact your supervisor.")
        else:
            await ctx.send(f"Hi {ctx.author.mention}!\nThere is no record of this ID, list IDs to find your correct ID!")

    @command(name="register_member")
    @has_permissions(administrator=True)
    async def register_member_admin(self, ctx: Context, member_id):

        try:
            member_user = ctx.message.mentions[0]
        except IndexError:
            await ctx.send(f"Hi {ctx.author.mention}!\nIncorrect usage of the command, use -help for more information!")
            return

        exit_code = members_spreadsheet.register(
            member_id, member_user.id, True)
        if exit_code == 0:
            await ctx.send(f"Hi {ctx.author.mention}!\nMember is now registered with the ID {member_id}!")
        elif exit_code == 1:
            await ctx.send(f"Hi {ctx.author.mention}!\nMember is already registered with this ID")
        else:
            await ctx.send(f"Hi {ctx.author.mention}!\nThere is no record of this ID, list IDs to find the correct ID!")

    @command(name="unregister_self")
    async def unregister_member(self, ctx: Context):

        exit_code = members_spreadsheet.unregister(ctx.author.id)
        if exit_code == 0:
            await ctx.send(f"Hi {ctx.author.mention}!\nYou have been successfully unregistered!")
        else:
            await ctx.send(f"Hi {ctx.author.mention}!\nYou are not registered in the first place!")

    @command(name="unregister_member")
    @has_permissions(administrator=True)
    async def unregister_member_admin(self, ctx: Context):

        try:
            member_user = ctx.message.mentions[0]
        except IndexError:
            await ctx.send(f"Hi {ctx.author.mention}!\nIncorrect usage of the command, use -help for more information!")
            return

        exit_code = members_spreadsheet.unregister(member_user.id)
        if exit_code == 0:
            await ctx.send(f"Hi {ctx.author.mention}!\nMember has been successfully unregistered!")
        else:
            await ctx.send(f"Hi {ctx.author.mention}!\nMember isn't registered in the first place!")

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

    @register_member.error
    @register_member_admin.error
    @unregister_member.error
    @unregister_member_admin.error
    @list_ids.error
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
    bot.add_cog(Register(bot))
