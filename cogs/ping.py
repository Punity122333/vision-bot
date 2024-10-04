import discord
from discord.ext import commands

class PingCog(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.command(name='ping', help="Returns the bot's latency")
    async def ping(self, ctx: commands.Context) -> None:
        latency = round(self.bot.latency * 1000)  # Convert to milliseconds
        embed = discord.Embed(title="🏓 Pong!", description=f"Latency: {latency}ms", color=discord.Color.blue())
        await ctx.send(embed=embed)

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(PingCog(bot))