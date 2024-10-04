import discord
from discord.ext import commands
import os
import asyncio
from discord import Embed

# Bot prefix, you can change this to whatever you want
bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())

@bot.event
async def on_ready() -> None:
    print(f"Logged in as {bot.user}")
    await bot.tree.sync()  # Sync the slash commands with Discord

@bot.command(name='list_commands', help="Lists all registered commands")
async def list_commands(ctx):
    embed = Embed(title="Registered Commands", color=0x00ff00)
    for command in bot.commands:
        embed.add_field(name=command.name, value=command.help or "No description", inline=False)
    await ctx.send(embed=embed)

@bot.command(name='reload_cogs', help="Reloads all cogs or a specific cog")
async def reload_cogs(ctx: commands.Context, cog_name: str = None):
    if cog_name:
        # Reload specific cog
        cog_path = f'cogs.{cog_name}'
        try:
            await bot.reload_extension(cog_path)
            await ctx.send(f'Successfully reloaded {cog_path}')
        except Exception as e:
            await ctx.send(f'Failed to reload {cog_path}: {e}')
    else:
        # Reload all cogs
        await ctx.send("Reloading all cogs...")
        for filename in os.listdir('./cogs'):
            if filename.endswith('.py'):
                cog_name = f'cogs.{filename[:-3]}'
                try:
                    await bot.reload_extension(cog_name)
                    await ctx.send(f'Successfully reloaded {cog_name}')
                except Exception as e:
                    await ctx.send(f'Failed to reload {cog_name}: {e}')

async def load_cogs():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            cog_name = f'cogs.{filename[:-3]}'
            try:
                await bot.load_extension(cog_name)
                print(f'Successfully loaded {cog_name}')
            except Exception as e:
                print(f'Failed to load {cog_name}: {e}')

async def main():
    await load_cogs()
    await bot.start('ODA5NzU3MTkyODM1NDMyNDg4.GOvzH0.pULCPvweqjGIzWyg5_IhAgy1X2I3XhFLuT55y0')  # Replace with your bot token

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Bot stopped')
