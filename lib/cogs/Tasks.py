from discord.ext.commands import Cog
# from discord.ext.commands import command
# from discord.ext.commands import Context
# from discord import Embed


class Tasks(Cog):
    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("Tasks")


def setup(bot):
    bot.add_cog(Tasks(bot))
