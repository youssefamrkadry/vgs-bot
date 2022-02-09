from discord.ext.commands import Cog
from discord.ext.commands import command
from discord.ext.commands import Context
from discord import Embed


class Help(Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.remove_command("help")

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("Help")

    @command(name="hello")
    async def say_hello(self, ctx: Context):
        await ctx.send(f"Hello {ctx.author.mention}!")

    @command(name="help")
    async def display_help(self, ctx: Context):
        help_embed = Embed(color=0xFF0000, title="Commands") \
            .set_footer(text='Created by Youssef Kadry', icon_url=self.bot.author_icon) \
            .set_thumbnail(url=self.bot.icon)

        # Administrator commands help, reserved for heads and mentors
        if ctx.author.guild_permissions.administrator:
            help_embed.add_field(name="Admin Commands",
                                value="\n-register_member [member VGS ID] [@member] \n=> Forcibely registers the member in the system \nexample: -register_member 983 @Ahmed \n\n"
                                    + "-unregister_member [@member] \n=> Forcibely unregisters the member from the system \nexample: -unregister_member @Ahmed \n\n"
                                    + "\n\n"
                                    + "\n\n",
                                inline=False)

        # Member and Apprentices commands, accessible by anyone
        help_embed.add_field(name="Member Commands",
                             value="\n-register_self [member VGS ID] \n=> Registers you in the system \nexample: -register_self 983 \n\n"
                                   + "-unregister_self \n=> Unregisters you from the system \nexample: -unregister_self \n\n"
                                   + "-list_ids [committee] \n=> Lists all IDs in the committie [CL] [MRKT] [FR] [HR] [MD] [GAD] [GDD] \nexample: -list_ids CL \n\n"
                                   + "-my_xp \n=> Provides your xp report \nexample: -my_xp \n\n"
                                   + "\n\n"
                                   + "\n\n",
                             inline=False)

        await ctx.author.send(embed=help_embed)


def setup(bot):
    bot.add_cog(Help(bot))
