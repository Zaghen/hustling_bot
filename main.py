import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import logging

load_dotenv()
TOKEN=os.getenv('DISCORD_TOKEN')

handler=logging.FileHandler(filename='discord.log',mode='w',encoding='utf-8')
intents=discord.Intents.default()
intents.message_content = True
intents.members = True

bot=commands.Bot(command_prefix='/',intents=intents)

@bot.event
async def on_ready():
    print('hai avviato il bot')

@bot.event
async def on_member_join(member:discord.Member):
    try:
        await member.send(f'Benvenuto Soppressata {member.name}')
    except Exception as e:
        print((f"DM non inviato {e} "))
    
    channel = discord.utils.get(member.guild.text_channels, name="generale")
    if channel:
        await channel.send(f"benvenuto {member.mention} nella taverna dei soppressati! ")
    

@bot.event
async def on_message(message:discord.Message):
    if message.author == bot.user:
        return
    
    if "mushoku tensei" in message.content.lower():
        await message.delete()
        await message.channel.send(f"{message.author.mention} - non dirlo o ti piace la soppressata")
    
    await bot.process_commands(message)

@bot.event
async def on_member_remove(member:discord.Member):
    try:
        await member.send(f'Perche te ne sei andato {member.name}')
    except Exception as e:
        print((f'DM non inviato {e}'))

    channel = discord.utils.get(member.guild.text_channels, name="generale")
    if channel:
        await channel.send(f"ci mancherai Soppressata {member.name} a meno che tu non eri GioWithUke alias Nova")


bot.run(token=TOKEN,log_handler=handler,log_level=logging.DEBUG)