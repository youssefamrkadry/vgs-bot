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
            self.bot.cogs_ready.ready_up("help")

    @command(name="hello")
    async def say_hello(self, ctx: Context):
        await ctx.send(f"Hello {ctx.author.mention}!")

    @command(name="help")
    async def display_help(self, ctx: Context):
        help_embed = Embed(color=0xFF0000, title="Commands") \
            .set_footer(text='Created by Youssef Kadry', icon_url=self.bot.author_icon) \
            .set_thumbnail(url=self.bot.icon)

        help_embed.add_field(name="Director Commands",
                             value="\n-debate_mode [mode] \n=> Changes debate mode to [formal debate] [informal debate] [moderated caucus] [unmoderated caucus] \n\n"
                                   + "-give_floor [@delegation] \n=> Gives the floor to the mentioned delegate \n\n"
                                   + "-take_floor \n=> Gives the floor to the chair and mutes all delegates \n\n"
                                   + "-warn [@delegate] \n=> Gives a warning to the mentioned delegate \n\n"
                                   + "-vote [procedural/substantive] \n=> Starts a voting session\n\n"
                                   + "-vote [end] \n=> Ends a voting session\n\n"
                                   + "-make_observer [@delegation][@][@] \n=>Turns the mentioned delegations into observers \n\n"
                                   + "-make_permanent [@delegation][@][@] \n=>Turns the mentioned delegations into permanent members (veto) \n\n"
                                   + "\n\n"
                                   + "\n\n",
                             inline=False)

        await ctx.author.send(embed=help_embed)


def setup(bot):
    bot.add_cog(Help(bot))
