import discord
from discord.ext import commands
import random

class HoroscopeCog(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.command(name="horoscope", help="Get a horoscope for a given zodiac sign.")
    async def horoscope(self, ctx: commands.Context, zodiac_sign: str) -> None:
        horoscopes = [
            "Today is a great day to pretend you know what you're doing.",
            "You might face some challenges today, but remember, coffee exists.",
            "Expect some good news to come your way, like finding a dollar in your pocket.",
            "Take time to relax and recharge, because Netflix isn't going to watch itself.",
            "An exciting opportunity is on the horizon, probably involving pizza.",
            "You will find clarity in a confusing situation, or at least a good meme.",
            "Someone close to you has good intentions, like sharing their Wi-Fi password.",
            "A financial opportunity will present itself, maybe in the form of a coupon.",
            "Trust your instincts today, unless they tell you to eat expired sushi.",
            "You will reconnect with an old friend, or at least their social media profile.",
            "A surprise is waiting for you at home, probably involving laundry.",
            "Your hard work will soon pay off, in the form of a nap.",
            "You will find joy in the little things, like not stepping on a Lego.",
            "A new hobby will bring you happiness, unless it's collecting parking tickets.",
            "You will overcome a difficult challenge, like opening a jar of pickles.",
            "Today is a perfect day to start a new project, or just make a to-do list.",
            "You will receive recognition for your efforts, maybe even a gold star sticker.",
            "A pleasant surprise is in store for you, like finding an extra fry in your bag.",
            "You will make a valuable new connection, probably with your Wi-Fi router.",
            "Your creativity will be at its peak today, so doodle away during meetings.",
            "You will find peace in a stressful situation, or at least a quiet corner.",
            "An old problem will finally be resolved, like finding the TV remote.",
            "You will discover a hidden talent, like balancing a spoon on your nose.",
            "A loved one will bring you happiness, especially if they bring snacks.",
            "You will achieve a long-term goal, like finishing a TV series.",
            "Today is a good day to focus on self-care, like eating dessert first.",
            "You will receive good news from afar, like a sale on your favorite website.",
            "A new friendship will blossom, probably with your delivery driver.",
            "You will find inspiration in an unexpected place, like the shower.",
            "Your positive attitude will attract good things, like compliments and cookies.",
            "Today, you might spill coffee on your favorite shirt. Embrace the chaos.",
            "You will lose something important today, like your keys or your patience.",
            "Expect a minor inconvenience, like stepping in a puddle with socks on.",
            "Your plans might go awry today, but at least you have a good story to tell.",
            "Someone will annoy you today, probably by chewing loudly.",
            "You will face a small setback, like running out of toilet paper.",
            "Today, you might forget something important, like your password or lunch.",
            "You will encounter a frustrating situation, like a slow internet connection.",
            "A minor mishap is in your future, like dropping your phone on your face.",
            "You might have an awkward encounter today, like waving back at someone who wasn't waving at you.",
            "Today, you might get stuck in traffic, but at least you have time to think.",
            "You will face a small disappointment, like finding out your favorite snack is sold out.",
            "Today, you might misplace something, like your phone or your sanity.",
            "You will have a clumsy moment today, like tripping over your own feet.",
            "Expect a minor annoyance, like getting a paper cut or a hangnail.",
            "You might have a frustrating day, but remember, tomorrow is a new start."
        ]
        horoscope_message = random.choice(horoscopes)
        
        embed = discord.Embed(title=f"Horoscope for {zodiac_sign}", description=horoscope_message, color=0x00ff00)
        await ctx.send(embed=embed)

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(HoroscopeCog(bot))