import discord
from discord.ext import commands
from typing import Any, List, Optional, Union, Literal
import os
import asyncio
from discord import Embed, Reaction
from termcolor import colored
import logging
from concurrent.futures import ThreadPoolExecutor
if os.path.exists('bot_errors.log'):
    os.remove('bot_errors.log')

# Create a new bot_errors.log file
with open('bot_errors.log', 'w') as f:
    f.write('')

class ThreadedHandler(logging.Handler):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.executor = ThreadPoolExecutor(max_workers=1)

    def emit(self, record):
        self.executor.submit(self._emit, record)

    def _emit(self, record):
        super().emit(record)

        
file_handler: logging.FileHandler = logging.FileHandler('bot_errors.log')
stream_handler: logging.StreamHandler = logging.StreamHandler()
threaded_handler: ThreadedHandler = ThreadedHandler()
threaded_handler.setFormatter(logging.Formatter('%(asctime)s %(name)s %(message)s %(levelname)s '))

logging.basicConfig(level=logging.ERROR, handlers=[threaded_handler, file_handler, stream_handler])
logging.getLogger('discord').setLevel(logging.WARNING)

class CustomHelpCommand(commands.HelpCommand):
    def __init__(self) -> None:
        super().__init__()

    async def send_bot_help(self, mapping: dict) -> None:
        ctx: commands.Context[Union[commands.Bot, commands.AutoShardedBot]] = self.context
        commands_per_page: int = 5
        pages: List[Embed] = []
        commands_list: List[commands.Command] = list(self.context.bot.commands)

        for i in range(0, len(commands_list), commands_per_page):
            embed: Embed = Embed(title="Registered Commands", color=0x00ff00)
            for command in commands_list[i:i + commands_per_page]:
                embed.add_field(name=command.name, value=command.help or "No description", inline=False)
            pages.append(embed)

        message: discord.Message = await ctx.send(embed=pages[0])
        await message.add_reaction('⬅️')
        await message.add_reaction('➡️')

        def check(reaction: Reaction, user: discord.User) -> Union[Any, Literal[False]]:
            return user == ctx.author and str(reaction.emoji) in ['⬅️', '➡️'] and reaction.message.id == message.id

        i: int = 0
        while True:
            try:
                reaction, user = await self.context.bot.wait_for('reaction_add', timeout=60.0, check=check)
                if str(reaction.emoji) == '➡️':
                    i += 1
                    if i >= len(pages):
                        i = 0
                    await message.edit(embed=pages[i])
                elif str(reaction.emoji) == '⬅️':
                    i -= 1
                    if i < 0:
                        i = len(pages) - 1
                    await message.edit(embed=pages[i])
                await message.remove_reaction(reaction, user)
            except asyncio.TimeoutError:
                break

    async def send_command_help(self, command: commands.Command) -> None:
        embed: Embed = Embed(title=f"Help for command '{command.name}'", color=0x00ff00)
        embed.add_field(name=command.name, value=command.help or "No description", inline=False)
        await self.context.send(embed=embed)

bot: commands.Bot = commands.Bot(command_prefix='!', intents=discord.Intents.all(), help_command=CustomHelpCommand())

@bot.event
async def on_ready() -> None:
    print(colored(f"\nLogged in as {bot.user}", "green"))
    await bot.tree.sync()  # Sync the slash commands with Discord

@bot.event
async def on_command_error(ctx: commands.Context, error: commands.CommandError) -> None:
    logging.error(f"An error occurred: {error}", exc_info=True)
    embed: Embed
    if isinstance(error, commands.CommandNotFound):
        embed = Embed(title="Error", description=f"Command '{ctx.invoked_with}' not found.", color=0xff0000)
    elif isinstance(error, commands.MissingRequiredArgument):
        embed = Embed(title="Error", description=f"Missing required argument: **{error.param}**. Please check the command usage.", color=0xff0000)
    elif isinstance(error, commands.BadArgument):
        embed = Embed(title="Error", description=f"Bad argument: **{error}**. Please check the command usage.", color=0xff0000)
    elif isinstance(error, commands.CommandOnCooldown):
        embed = Embed(title="Error", description=f"This command is on cooldown. Try again after {error.retry_after:.2f} seconds.", color=0xff0000)
    elif isinstance(error, commands.MissingPermissions):
        missing_perms: str = ', '.join(error.missing_permissions)
        embed = Embed(title="Error", description=f"You do not have the required permissions to use this command. Missing permissions: {missing_perms}", color=0xff0000)
    else:
        embed = Embed(title="Error", description=str(error), color=0xff0000)
    await ctx.send(embed=embed)

@bot.command(name='reload_cogs', help="Reloads all cogs or a specific cog")
async def reload_cogs(ctx: commands.Context, cog_name: Optional[str] = None) -> None:
    embed: Embed = Embed(title="Reload Cogs", color=0x00ff00)
    
    if cog_name:
        # Reload specific cog
        cog_path: str = f'cogs.{cog_name}'
        try:
            await bot.reload_extension(cog_path)
            embed.add_field(name=cog_path, value="Successfully reloaded", inline=False)
        except Exception as e:
            embed.add_field(name=cog_path, value=f"Failed to reload: {e}", inline=False)
    else:
        # Reload all cogs
        embed.description = "Reloading all cogs..."
        for filename in os.listdir('./cogs'):
            if filename.endswith('.py'):
                cog_name: str = f'cogs.{filename[:-3]}'
                try:
                    await bot.reload_extension(cog_name)
                    embed.add_field(name=cog_name, value="Successfully reloaded", inline=False)
                except Exception as e:
                    embed.add_field(name=cog_name, value=f"Failed to reload: {e}", inline=False)
    
    await ctx.send(embed=embed)

async def load_cogs() -> None:
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            cog_name: str = f'cogs.{filename[:-3]}'
            try:
                await bot.load_extension(cog_name)
                print(f'Successfully loaded {cog_name}')
            except Exception as e:
                print(f'Failed to load {cog_name}: {e}')
    # Load Jishaku
    try:
        await bot.load_extension('jishaku')
        print('Successfully loaded Jishaku')
    except Exception as e:
        print(f'Failed to load Jishaku: {e}')

async def main() -> None:
    await load_cogs()
    await bot.start('TOKEN')  # Replace with your bot token

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('\rBot stopped')
