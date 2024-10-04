import discord
from discord.ext import commands
from discord.ext.commands import Bot, Context

class UserInfo(commands.Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    @commands.command(name='userinfo', help='Displays information about a user')
    async def userinfo(self, ctx: Context, member: discord.Member = None) -> None:
        try:
            if member is None:
                member = ctx.author

            embed = discord.Embed(title=f"User Info - {member}", color=discord.Color.blue())
            embed.set_thumbnail(url=member.avatar.url)
            embed.add_field(name="ID", value=member.id, inline=True)
            embed.add_field(name="Name", value=str(member), inline=True)
            embed.add_field(name="Nickname", value=member.nick, inline=True)
            embed.add_field(name="Status", value=member.status, inline=True)
            embed.add_field(name="Top Role", value=member.top_role.mention, inline=True)
            embed.add_field(name="Joined Server", value=member.joined_at.strftime("%Y-%m-%d %H:%M:%S"), inline=True)
            embed.add_field(name="Joined Discord", value=member.created_at.strftime("%Y-%m-%d %H:%M:%S"), inline=True)

            await ctx.send(embed=embed)
            print(f"Embed sent for user: {member}")
        except Exception as e:
            print(f"Failed to send embed: {e}")
            await ctx.send("An error occurred while trying to fetch user info.")

async def setup(bot: Bot) -> None:
    await bot.add_cog(UserInfo(bot))