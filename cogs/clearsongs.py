import os
from os.path import dirname, abspath
import discord
from discord.ext import commands

class ClearSongs(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.owner_id = 702136500334100604  # Replace with the actual owner ID

    @commands.command(help="Removes all .webm and .m4a files from the parent directory. (Owner only)")
    async def clearsongs(self, ctx: commands.Context) -> None:
        if ctx.author.id != self.owner_id:
            embed = discord.Embed(description="You do not have permission to use this command.", color=discord.Color.red())
            await ctx.send(embed=embed)
            return

        parent_dir = dirname(dirname(abspath(__file__)))
        
        
        
        removed_files = []

        for filename in os.listdir(parent_dir):
            if filename.endswith('.webm') or filename.endswith('.m4a'):
                file_path = os.path.join(parent_dir, filename)
                os.remove(file_path)
                removed_files.append(filename)

        if removed_files:
            embed = discord.Embed(title="Removed Files", description="\n ".join(removed_files), color=discord.Color.green())
        else:
            embed = discord.Embed(description="No .webm or .m4a files found.", color=discord.Color.orange())

        await ctx.send(embed=embed)

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(ClearSongs(bot))