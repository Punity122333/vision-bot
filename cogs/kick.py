import discord
from discord.ext import commands


class KickCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name='kick', help='Kick a user from the server. Usage: !kick @user [reason]')
    @commands.has_permissions(ban_members=True)
    async def kick(self, ctx: commands.Context, member: discord.Member, *, reason: str = None) -> None:
        """Ban a user from the server."""
        embed = discord.Embed(title="Kick Command")
        try:
            await member.kick(reason=reason)
            embed.description = f'User {member} has been kicked for: {reason}'
            embed.color = discord.Color.red()
        except discord.Forbidden:
            embed.description = 'I do not have permission to kick this user.'
            embed.color = discord.Color.orange()
        except discord.HTTPException:
            embed.description = 'Kicking failed. Please try again.'
            embed.color = discord.Color.orange()
        
        await ctx.send(embed=embed)

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(KickCog(bot))