from discord.ext.commands import Cog
from discord.ext.commands import command
from discord.ext.commands import Context
from subprocess import check_output


class Minecraft(Cog):
    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("Minecraft")

    @command(name="start-minecraft-server")
    async def start_server(self, ctx: Context):
        await ctx.send(f"Starting minecraft server...")
        check_output('node lib/aternosAPI-master/src/index.js --start')
        await ctx.send(f"Minecraft server is up!!")

    @command(name="stop-minecraft-server")
    async def stop_server(self, ctx: Context):
        await ctx.send(f"Stopping minecraft server...")
        check_output('node lib/aternosAPI-master/src/index.js --stop')
        await ctx.send(f"Minecraft server has been stopped")

    @command(name="minecraft-server-info")
    async def stop_server(self, ctx: Context):
        await ctx.send(f"Checking info...")
        info = check_output('node lib/aternosAPI-master/src/index.js --info').decode('utf-8')
        if "Online" in info:
            await ctx.send(f"Minecraft server is online let's gooooo!")
        elif "Offline" in info:
            await ctx.send(f"Minecraft server is offline :(")
        else:
            await ctx.send(f"Error")

    @command(name="minecraft-server-help")
    async def help_server(self, ctx: Context):
        await ctx.send(f"Commands:\n\n"
                       f"start-minecraft-server\n"
                       f"stop-minecraft-server\n"
                       f"minecraft-server-info")


def setup(bot):
    bot.add_cog(Minecraft(bot))
