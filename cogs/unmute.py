import discord
from discord.ext import commands

class Unmute(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.command(name='unmute')
    @commands.has_permissions(manage_roles=True)
    async def unmute(self, ctx: commands.Context, member: discord.Member) -> None:
        muted_role = discord.utils.get(ctx.guild.roles, name='Muted')
        if muted_role in member.roles:
            await member.remove_roles(muted_role)
            await ctx.send(f'{member.mention} has been unmuted.')
        else:
            await ctx.send(f'{member.mention} is not muted.')

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Unmute(bot))