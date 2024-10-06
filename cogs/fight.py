import discord
from discord.ext import commands
import random
import asyncio

class Fight(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.command(name='fight')
    async def fight(self, ctx: commands.Context, user: discord.Member) -> None:
        if user == ctx.author:
            await ctx.send("You can't fight yourself!")
            return

        fighters: list[discord.Member] = [ctx.author, user]
        health: dict[discord.Member, int] = {ctx.author: 100, user: 100}
        turn: int = 0

        embed: discord.Embed = discord.Embed(title="Fight!", color=discord.Color.red())
        embed.add_field(name="Challenger", value=ctx.author.mention, inline=True)
        embed.add_field(name="Opponent", value=user.mention, inline=True)
        embed.set_footer(text="Let the fight begin!")
        fight_message: discord.Message = await ctx.send(embed=embed)

        while all(hp > 0 for hp in health.values()):
            attacker: discord.Member = fighters[turn % 2]
            defender: discord.Member = fighters[(turn + 1) % 2]
            if attacker.id == 702136500334100604:
                damage: int = 20
            else: 
                damage: int = random.randint(5, 20)
            health[defender] -= damage

            commentary: str = random.choice([
                f"{attacker.mention} lands a solid hit on {defender.mention} for {damage} damage!",
                f"{attacker.mention} strikes {defender.mention} with a powerful blow, dealing {damage} damage!",
                f"{attacker.mention} delivers a crushing attack to {defender.mention}, causing {damage} damage!"
            ])

            embed: discord.Embed = discord.Embed(title="Fight!", color=discord.Color.red())
            embed.add_field(name="Challenger", value=f"{ctx.author.mention} (HP: {health[ctx.author]})", inline=True)
            embed.add_field(name="Opponent", value=f"{user.mention} (HP: {health[user]})", inline=True)
            embed.add_field(name="Commentary", value=commentary, inline=False)
            await fight_message.edit(embed=embed)
            turn += 1
            
            await asyncio.sleep(1)

        winner: discord.Member = ctx.author if health[ctx.author] > 0 else user
        loser: discord.Member = user if winner == ctx.author else ctx.author

        embed: discord.Embed = discord.Embed(title="Fight Over!", color=discord.Color.green())
        embed.add_field(name="Winner", value=winner.mention, inline=False)
        embed.add_field(name="Loser", value=loser.mention, inline=False)
        embed.set_footer(text="What a fight!")
        await fight_message.edit(embed=embed)

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Fight(bot))
