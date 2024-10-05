import discord
from discord.ext import commands
import json
from typing import Optional, Dict, List, Any
import os

class Warn(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name='warn', help='Warn a member for a specified reason. Usage: !warn @member [reason]')
    @commands.has_permissions(manage_messages=True)
    async def warn(self, ctx: commands.Context, member: discord.Member, *, reason: Optional[str] = "No reason provided") -> None:
        try:
            warnings_file_path = os.path.join(os.path.dirname(__file__), '../warnings.json')

            # Load existing warnings
            try:
                with open(warnings_file_path, 'r') as f:
                    warnings: Dict[str, List[Dict[str, Any]]] = json.load(f)
            except FileNotFoundError:
                warnings = {}
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON: {e}")
                warnings = {}

            # Add the warning
            if str(member.id) not in warnings:
                warnings[str(member.id)] = []

            warnings[str(member.id)].append({
                "reason": reason,
                "warned_by": ctx.author.name,
                "timestamp": ctx.message.created_at.isoformat()
            })

            # Save the warnings
            try:
                with open(warnings_file_path, 'w') as f:
                    json.dump(warnings, f, indent=4)
                print("Warnings successfully saved.")
            except Exception as e:
                print(f"Error saving warnings: {e}")

            # Create an embed for the warning message
            embed = discord.Embed(title="Member Warned", color=discord.Color.orange())
            embed.add_field(name="Member", value=member.mention, inline=False)
            embed.add_field(name="Reason", value=reason, inline=False)
            embed.add_field(name="Warned by", value=ctx.author.name, inline=False)
            embed.set_footer(text=f"Timestamp: {ctx.message.created_at}")

            await ctx.send(embed=embed)

        except Exception as e:
            await ctx.send(f"An error occurred while warning the member: {str(e)}")
            print(f"An error occurred: {e}")

    @commands.command(name='clearwarnings', help='Clears all warnings for a specified member. Usage: !clearwarnings @member')
    @commands.has_permissions(manage_messages=True)
    async def clear_warnings(self, ctx: commands.Context, member: discord.Member) -> None:
        try:
            warnings_file_path = os.path.join(os.path.dirname(__file__), '../warnings.json')
            # Load existing warnings
            try:
                with open(warnings_file_path, 'r') as f:
                    warnings: Dict[str, List[Dict[str, Any]]] = json.load(f)
            except FileNotFoundError:
                warnings = {}
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON: {e}")
                warnings = {}

            # Check if the member has warnings
            if str(member.id) in warnings:
                del warnings[str(member.id)]

                # Save the updated warnings
                try:
                    with open(warnings_file_path, 'w') as f:
                        json.dump(warnings, f, indent=4)
                    print("Warnings successfully cleared.")
                except Exception as e:
                    print(f"Error saving warnings: {e}")

                embed = discord.Embed(title="Warnings Cleared", color=discord.Color.green())
                embed.add_field(name="Member", value=member.mention, inline=False)
                embed.add_field(name="Status", value="All warnings have been cleared.", inline=False)
                await ctx.send(embed=embed)
            else:
                embed = discord.Embed(title="No Warnings Found", color=discord.Color.red())
                embed.add_field(name="Member", value=member.mention, inline=False)
                embed.add_field(name="Status", value="This member has no warnings.", inline=False)
                await ctx.send(embed=embed)

        except Exception as e:
            embed = discord.Embed(title="Error", color=discord.Color.red())
            embed.add_field(name="An error occurred while clearing the warnings", value=str(e), inline=False)
            await ctx.send(embed=embed)
            print(f"An error occurred: {e}")

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Warn(bot))