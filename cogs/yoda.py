import discord
from discord.ext import commands
import random

class YodaSpeak(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.command(name='yoda', help='Turns any message into Yoda-speak. Legendary, this will be.')
    async def yoda(self, ctx: commands.Context, *, message: str) -> None:
        yoda_message = self.to_yoda_speak(message)
        embed = discord.Embed(title="Yoda Speak", description=yoda_message, color=discord.Color.green())
        await ctx.send(embed=embed)

    def to_yoda_speak(self, message: str) -> str:
        words = message.split()
        if len(words) > 3:
            # Move the last word to the beginning to sound more like Yoda
            words = [words[-1]] + words[:-1]
        yoda_phrases = ["hmmm", "yes", "strong with the Force, you are", "much to learn, you still have"]
        return ' '.join(words) + ', ' + random.choice(yoda_phrases) + '.'

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(YodaSpeak(bot))
