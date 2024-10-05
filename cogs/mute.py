import discord
from discord.ext import commands

class Mute(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.command(name='mute', help='Mutes a specified user. Usage: !mute @user [reason]')
    @commands.has_permissions(manage_roles=True)
    async def mute(self, ctx: commands.Context, member: discord.Member, *, reason: str = None) -> None:
        guild: discord.Guild = ctx.guild
        muted_role: discord.Role = discord.utils.get(guild.roles, name="Muted")

        if member.guild_permissions.administrator:
            embed = discord.Embed(title="Error", description=f"{member.mention} could not be muted because they are an administrator.", color=discord.Color.red())
            await ctx.send(embed=embed)
            return

        if not muted_role:
            muted_role = await guild.create_role(name="Muted")

        for channel in guild.channels:
            await channel.set_permissions(muted_role, speak=False, send_messages=False, read_message_history=True, read_messages=False)

        await member.add_roles(muted_role)
        reason_message = f" Reason: {reason}" if reason else ""
        embed = discord.Embed(title="Muted", description=f"{member.mention} has been muted.{reason_message}", color=discord.Color.orange())
        await ctx.send(embed=embed)
        

    @mute.error
    async def mute_error(self, ctx: commands.Context, error: commands.CommandError) -> None:
        if isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(title="Error", description="You do not have permission to use this command.", color=discord.Color.red())
        elif isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(title="Error", description="Please mention a user to mute.", color=discord.Color.red())
        else:
            embed = discord.Embed(title="Error", description="An error occurred while trying to mute the user.", color=discord.Color.red())
        
        await ctx.send(embed=embed)
            
async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Mute(bot))
