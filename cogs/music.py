import discord
from discord.ext import commands
import yt_dlp as youtube_dl
import asyncio
from typing import Optional

# Suppress noise about console usage from errors
youtube_dl.utils.bug_reports_message = lambda: ''

ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0'  # Bind to IPv4 since IPv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source: discord.FFmpegPCMAudio, *, data: dict, volume: float = 0.5) -> None:
        super().__init__(source, volume)

        self.data: dict = data

        self.title: Optional[str] = data.get('title')
        self.url: Optional[str] = data.get('url')

    @classmethod
    async def from_url(cls, url: str, *, loop: Optional[asyncio.AbstractEventLoop] = None, stream: bool = False) -> 'YTDLSource':
        loop = loop or asyncio.get_event_loop()
        try:
            data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))
        except youtube_dl.DownloadError as e:
            raise commands.CommandError(f"An error occurred while downloading the video: {e}")

        if 'entries' in data:
            # Take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)

class Music(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot: commands.Bot = bot

    @commands.command(name='join', help='Tells the bot to join the voice channel')
    async def join(self, ctx: commands.Context) -> None:
        if not ctx.message.author.voice:
            embed = discord.Embed(description=f"{ctx.message.author.name} is not connected to a voice channel", color=discord.Color.red())
            await ctx.send(embed=embed)
            return
        else:
            channel: discord.VoiceChannel = ctx.message.author.voice.channel

        try:
            await channel.connect()
            embed = discord.Embed(description=f"Joined 🔊 {channel.name}", color=discord.Color.green())
            await ctx.send(embed=embed)
        except discord.ClientException as e:
            embed = discord.Embed(description=f"An error occurred while trying to connect to the voice channel: {e}", color=discord.Color.red())
            await ctx.send(embed=embed)

    @commands.command(name='leave', help='To make the bot leave the voice channel')
    async def leave(self, ctx: commands.Context) -> None:
        if ctx.voice_client:
            try:
                await ctx.guild.voice_client.disconnect()
                embed = discord.Embed(description="I have left the voice channel", color=discord.Color.green())
                await ctx.send(embed=embed)
            except discord.ClientException as e:
                embed = discord.Embed(description=f"An error occurred while trying to leave the voice channel: {e}", color=discord.Color.red())
                await ctx.send(embed=embed)
        else:
            embed = discord.Embed(description="I'm not in a voice channel", color=discord.Color.red())
            await ctx.send(embed=embed)

    @commands.command(name='play', help='To play song')
    async def play(self, ctx: commands.Context, *, url: str) -> None:
        async with ctx.typing():
            try:
                player: YTDLSource = await YTDLSource.from_url(url, loop=self.bot.loop)
                ctx.voice_client.play(player, after=lambda e: print('Player error: %s' % e) if e else None)
            except commands.CommandError as e:
                embed = discord.Embed(description=f"An error occurred: {e}", color=discord.Color.red())
                await ctx.send(embed=embed)
                return

        embed = discord.Embed(description=f'Now playing: {player.title}', color=discord.Color.green())
        await ctx.send(embed=embed)

    @commands.command(name='pause', help='This command pauses the song')
    async def pause(self, ctx: commands.Context) -> None:
        if ctx.voice_client and not ctx.voice_client.is_paused():
            ctx.voice_client.pause()
            embed = discord.Embed(description="Paused ⏸️", color=discord.Color.green())
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(description="I'm not in a voice channel", color=discord.Color.red())
            await ctx.send(embed=embed)
    
    @commands.command(name='resume', help='Resumes the song')
    async def resume(self, ctx: commands.Context) -> None:
        if ctx.voice_client:
            ctx.voice_client.resume()
            embed = discord.Embed(description="Resumed ⏯️", color=discord.Color.green())
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(description="I'm not in a voice channel", color=discord.Color.red())
            await ctx.send(embed=embed)

    @commands.command(name='stop', help='Stops the song')
    async def stop(self, ctx: commands.Context) -> None:
        if ctx.voice_client:
            ctx.voice_client.stop()
            embed = discord.Embed(description="Stopped ⏹️", color=discord.Color.green())
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(description="I am not in a voice channel", color=discord.Color.red())
            await ctx.send(embed=embed)

    @play.before_invoke
    @pause.before_invoke
    @resume.before_invoke
    @stop.before_invoke
    async def ensure_voice(self, ctx: commands.Context) -> None:
        if ctx.voice_client is None:
            if ctx.author.voice:
                try:
                    await ctx.author.voice.channel.connect()
                except discord.ClientException as e:
                    embed = discord.Embed(description=f"An error occurred while trying to connect to the voice channel: {e}", color=discord.Color.red())
                    await ctx.send(embed=embed)
                    raise commands.CommandError("Author not connected to a voice channel.")
            else:
                embed = discord.Embed(description="You are not connected to a voice channel.", color=discord.Color.red())
                await ctx.send(embed=embed)
                raise commands.CommandError("Author not connected to a voice channel.")
        elif ctx.voice_client.is_playing():
            ctx.voice_client.stop()

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Music(bot))