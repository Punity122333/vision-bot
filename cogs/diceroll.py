import discord
from discord.ext import commands
from discord.ext.commands import *
import random

class DiceRoll(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot
    
    @commands.command(name='roll', help='Rolls a dice in NdN format.')
    async def roll(self, ctx: Context, dice: str) -> None:
        try:
            rolls, limit = map(int, dice.split('d'))
        except Exception:
            embed = discord.Embed(title='Invalid Format', description='Format must be in `NdN`!', color=discord.Color.red())
            await ctx.send(embed=embed)
        tupresult = tuple(random.randint(1, limit) for r in range(rolls))
        
        
        embed = discord.Embed(title='Rolls', color=discord.Color.green())
        for ind, i in enumerate(tupresult):
            embed.add_field(name=f'Roll #{ind+1}', value=i, inline=False)
        await ctx.send(embed=embed)
        
async def setup(bot: Bot) -> None:
    await bot.add_cog(DiceRoll(bot))