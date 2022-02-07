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

        if ctx.author.guild_permissions.administrator:
            help_embed.add_field(name="Admin Commands",
                                value="\n-register_member [member VGS ID] [@member] \n=> Forcibely registers the member in the system \n\n"
                                    + "-unregister_member [@member] \n=> Forcibely unregisters the member from the system \n\n"
                                    + "\n\n"
                                    + "\n\n",
                                inline=False)


        help_embed.add_field(name="Member Commands",
                             value="\n-register_self [member VGS ID] \n=> Registers you in the system \n\n"
                                   + "-unregister_self [@member] \n=> Unregisters you from the system \n\n"
                                   + "-list_ids [committee] \n=> Lists all IDs in the committie [CL] [MRKT] [FR] [HR] [MD] [GAD] [GDD] \n\n"
                                   + "-my_xp \n=> Provides your xp report \n\n"
                                   + "\n\n"
                                   + "\n\n",
                             inline=False)

        await ctx.author.send(embed=help_embed)


def setup(bot):
    bot.add_cog(Help(bot))
