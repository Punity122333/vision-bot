import discord
from discord.ext import commands
import asyncpraw.models
import asyncpraw
import random
from typing import List

class MemeCog(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot: commands.Bot = bot
        self.reddit: asyncpraw.Reddit = asyncpraw.Reddit(
            client_id='9G_-8UywQ03rOOnOrtT5nw',
            client_secret='OFH9M9sZT9Efdb874KPX3jbcV6Xn0w',
            user_agent='Vision/1.0 by pxnity'
        )

    @commands.command(name='meme', help="Fetches a random meme from Reddit and displays it.")
    async def meme(self, ctx: commands.Context) -> None:
        # Send initial embed indicating fetching
        fetching_embed = discord.Embed(title="Fetching a meme...", color=discord.Color.orange())
        message = await ctx.send(embed=fetching_embed)

        # Fetch the meme
        subreddit: asyncpraw.models.Subreddit = await self.reddit.subreddit('memes')
        memes: List[asyncpraw.models.Submission] = [submission async for submission in subreddit.hot(limit=50) if not submission.stickied]
        meme: asyncpraw.models.Submission = random.choice(memes)

        # Create the meme embed
        meme_embed: discord.Embed = discord.Embed(title=meme.title, color=discord.Color.blue())
        meme_embed.set_image(url=meme.url)
        meme_embed.set_footer(text=f"👍 {meme.score} | 💬 {meme.num_comments}")

        # Edit the message with the meme embed
        await message.edit(embed=meme_embed)

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(MemeCog(bot))
