import discord
from discord.ext import commands
import asyncio

class Clear(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name='clear', help='Clears a specified number of messages in the channel.')
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx: commands.Context, amount: int = 1):
        if amount < 1:
            await ctx.send("Please specify a positive number of messages to delete.")
            return

        deleted = await ctx.channel.purge(limit=amount + 1)
        await asyncio.sleep(0.5)# +1 to include the command message itself
        await ctx.send(f"Deleted {len(deleted) - 1} messages.", delete_after=5)

async def setup(bot: commands.Bot):
    await bot.add_cog(Clear(bot))