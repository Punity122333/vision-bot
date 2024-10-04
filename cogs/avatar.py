import discord
from discord.ext import commands
from discord.ext.commands import Bot, Context

class Avatar(commands.Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    @commands.command(name='avatar', help='Displays the avatar of the specified user or the command invoker.')
    async def avatar(self, ctx: Context, *, member: discord.Member = None) -> None:
        """Displays the avatar of the specified user or the command invoker."""
        member = member or ctx.author
        embed = discord.Embed(title=f"{member}'s Avatar")
        embed.set_image(url=member.avatar.url)
        await ctx.send(embed=embed)

async def setup(bot: Bot) -> None:
    await bot.add_cog(Avatar(bot))