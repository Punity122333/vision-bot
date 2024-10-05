import discord
from discord.ext import commands
import aiohttp

class PokemonCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name='pokemon', help='Fetches information about a specified Pokémon.')
    async def fetch_pokemon(self, ctx: commands.Context, pokemon_name: str) -> None:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f'https://pokeapi.co/api/v2/pokemon/{pokemon_name.lower()}') as response:
                    if response.status == 200:
                        data = await response.json()
                        species_url = data['species']['url']
                        
                        async with session.get(species_url) as species_response:
                            species_data = await species_response.json()
                            
                            # Get English flavor text entries (lore snippets)
                            flavor_texts = [entry['flavor_text'] for entry in species_data['flavor_text_entries'] if entry['language']['name'] == 'en']
                            
                            embed = discord.Embed(
                                title=data['name'].capitalize(),
                                description=f"ID: {data['id']}\nHeight: {data['height']}\nWeight: {data['weight']}",
                                color=discord.Color.blue()
                            )
                            embed.set_image(url=data['sprites']['other']['official-artwork']['front_default'])
                            
                            # Add stats to embed with bold and emojis
                            stat_emojis = {
                                'hp': '❤️',
                                'attack': '⚔️',
                                'defense': '🛡️',
                                'special-attack': '🔮',
                                'special-defense': '🔰',
                                'speed': '💨'
                            }
                            stats = "\n".join([f"**{stat_emojis.get(stat['stat']['name'], '')} {stat['stat']['name'].replace('-', ' ').capitalize()}:** {stat['base_stat']}" for stat in data['stats']])
                            
                            embed.add_field(name="Stats", value=stats, inline=False)
                            
                            # Add English flavor text (lore snippets) to embed
                            flavor_texts_str = flavor_texts[0].replace('\n', ' ')
                            if len(flavor_texts_str) > 1024:
                                flavor_texts_str = flavor_texts_str[:1021] + '...'
                            embed.add_field(name="Lore Snippets", value=flavor_texts_str, inline=False)
                            
                            await ctx.send(embed=embed)
                    else:
                        await ctx.send(f"Could not find information for Pokémon: {pokemon_name}")
        except aiohttp.ClientError as e:
            await ctx.send(f"An error occurred while fetching data: {str(e)}")
        except KeyError as e:
            await ctx.send(f"Unexpected data format received: missing key {str(e)}")
        except Exception as e:
            await ctx.send(f"An unexpected error occurred: {str(e)}")

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(PokemonCog(bot))