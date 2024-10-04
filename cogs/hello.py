import discord
from discord.ext import commands
from discord.ext.commands import Context
from discord import app_commands

class HelloCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name='hello', help="Says hello")
    async def hello(self, ctx: Context):
        await ctx.send('Hello, world!')

async def setup(bot: commands.Bot):
    cog = HelloCog(bot)
    await bot.add_cog(cog)
    