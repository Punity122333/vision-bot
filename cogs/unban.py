import discord
from discord.ext import commands
from discord.ext.commands import Bot, Context

class Unban(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @commands.command(name="unban", help="Unban a user by their ID. Usage: !unban <user_id>")
    async def unban(self, ctx: Context, user_id: int):
        guild = ctx.guild
        user = discord.Object(id=user_id)
        
        try:
            await guild.unban(user)
            embed = discord.Embed(
                title="User Unbanned",
                description=f"Successfully unbanned user with ID {user_id}.",
                color=discord.Color.green()
            )
        except discord.NotFound:
            embed = discord.Embed(
                title="User Not Found",
                description=f"No banned user found with ID {user_id}.",
                color=discord.Color.red()
            )
        except discord.Forbidden:
            embed = discord.Embed(
                title="Permission Denied",
                description="I do not have permission to unban this user.",
                color=discord.Color.red()
            )
        except Exception as e:
            embed = discord.Embed(
                title="Error",
                description=f"An error occurred: {str(e)}",
                color=discord.Color.red()
            )
        
        await ctx.send(embed=embed)

async def setup(bot: Bot):
    await bot.add_cog(Unban(bot))