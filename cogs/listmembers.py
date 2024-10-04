import discord
from discord.ext import commands
from discord.ext.commands import Context
from discord import Embed

class ListMembersCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='listmembers', help="Lists all members in the server")
    async def list_members(self, ctx: Context):
        members = ctx.guild.members
        members_list = [member.name for member in members]
        embed = Embed(title="Server Members", description="\n".join(members_list), color=discord.Color.blue())
        await ctx.send(embed=embed)
        
async def setup(bot: commands.Bot):
    await bot.add_cog(ListMembersCog(bot))
    