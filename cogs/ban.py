import discord
from discord.ext import commands


class BanCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name='ban', help='Ban a user from the server. Usage: !ban @user [reason]')
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx: commands.Context, member: discord.Member, *, reason: str = None) -> None:
        """Ban a user from the server."""
        embed = discord.Embed(title="Ban Command")
        try:
            await member.ban(reason=reason)
            embed.description = f'User {member} has been banned for: {reason}'
            embed.color = discord.Color.red()
        except discord.Forbidden:
            embed.description = 'I do not have permission to ban this user.'
            embed.color = discord.Color.orange()
        except discord.HTTPException:
            embed.description = 'Banning failed. Please try again.'
            embed.color = discord.Color.orange()
        
        await ctx.send(embed=embed)

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(BanCog(bot))