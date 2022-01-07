import discord
import os
from dotenv import load_dotenv
from discord.ext.commands import Bot as BotBase
# from replit import db
from glob import glob
from asyncio import sleep

PREFIX = "-"
COGS = [path.split("\\")[-1][:-3] for path in glob("./lib/cogs/*.py")]
load_dotenv()


class Ready(object):
    def __init__(self):
        for cog in COGS:
            setattr(self, cog, False)

    def ready_up(self, cog):
        setattr(self, cog, True)
        print(f"{cog} cog ready".lower())

    def all_ready(self):
        return all([getattr(self, cog) for cog in COGS])


class Bot(BotBase):
    def __init__(self):
        self.VERSION = "0.0.0"
        self.PREFIX = PREFIX
        self.ready = False
        self.cogs_ready = Ready()
        self.guild = None
        self.stdout = None
        self.TOKEN = os.getenv('TOKEN')
        print(self.TOKEN)
        self.icon = "https://i.ibb.co/QrkLL3P/VGS-Logo.png"
        self.author_icon = "https://i.ibb.co/wsS4Y4j/IMG-20211119-WA0206-2.jpg"

        super().__init__(command_prefix=PREFIX)

    def setup(self):
        for cog in COGS:
            self.load_extension(f"lib.cogs.{cog}")
            print(f"{cog} cog loaded".lower())

        print("setup complete")

    def run(self, version):

        self.VERSION = version

        print("running setup...")
        self.setup()

        print("running bot...")
        super().run(self.TOKEN, reconnect=True)

    async def on_ready(self):
        if not self.ready:
            self.guild = self.get_guild(871487383500128317)
            self.stdout = self.get_channel(871487383957286955)

            print(f'VGS bot up and ready!\nWe are logged in as {bot.user}')
            await self.change_presence(activity=discord.Game(name="Unity Game Engine"))

            ready_embed = discord.Embed(color=0xFF0000)\
                .set_thumbnail(url=self.icon)
            ready_embed.add_field(name="Bot Online!",
                                  value="\nVGS Bot is now back online,"
                                        f"\nfeel free to use {self.PREFIX}help for more info.\n\n" 
                                        f"version {self.VERSION}")

            await self.stdout.send(embed=ready_embed)

            while not self.cogs_ready.all_ready():
                await sleep(0.5)

            self.ready = True
            print("bot ready")

        else:
            print("bot reconnected")

    async def on_message(self, message: discord.Message):
        await self.process_commands(message)

    @staticmethod
    async def on_connect():
        print("bot connected")

    @staticmethod
    async def on_disconnect():
        print("bot disconnected")


bot = Bot()
