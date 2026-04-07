import discord
import mysql.connector
import signal
from discord.ext import commands
from dotenv import load_dotenv
import os
import logging
import sys

load_dotenv()
TOKEN=os.getenv('DISCORD_TOKEN')

handler=logging.FileHandler(filename='discord.log',mode='w',encoding='utf-8')
intents=discord.Intents.default()
intents.message_content = True
intents.members = True

bot=commands.Bot(command_prefix='!',intents=intents)

dataBase = mysql.connector.connect(
    host = 'localhost',
    user = 'user',
    passwd = 'password',
    database= 'hustling',
    autocommit = True
)

cursor= dataBase.cursor()

def signal_handler(sig, frame):
    dataBase.close()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)


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

@bot.command()
async def subscribe(ctx):
    user_id=ctx.author.id
    cursor.execute(f" SELECT username FROM USER WHERE username = {user_id};")
    user=cursor.fetchone()
    if not user :
        cursor.execute(
            f""" 
             INSERT INTO USER (USERNAME) values ({user_id});
             """
        )
        await ctx.send(f"Utente {ctx.author.name} aggiunto al database")
    else:
        await ctx.send("Esisti gia' nel database")

@bot.command()
async def unsubscribe(ctx):
    user_id=ctx.author.id
    cursor.execute(f" SELECT username FROM USER WHERE username = {user_id};")
    user=cursor.fetchone()
    if user :
        cursor.execute(
            f""" 
             DELETE FROM USER WHERE username = {user_id};
             """
        )
        await ctx.send(f"Utente {ctx.author.name} rimosso dal database")
    else:
        await ctx.send("Non esisti nel database")

@bot.command()
async def add_mod(ctx,mod_name,version,type,link): #aggiunge una mod
    if not mod_name or not version or not type or not link:
        await ctx.send("sintassi incorretta,usa !add_mod NOME_MOD VERSIONE TIPO LINK")
        return
    if type.lower() not in ('stream','iso'):
        await ctx.send('il tipo non corrisponde a uno dei du richiesti exp=(stream,iso)')
        return
    if link.lower().startswith('https://discord.com/channels/1042370928195162132/1043747965564633108'):
        await ctx.send('formato del link errato,specificane uno corretto')
        return
    cursor.execute(f"SELECT nome FROM MODS WHERE nome = '{mod_name}'")
    mod=cursor.fetchone()
    if not mod :
        cursor.execute(
            f""" 
             INSERT INTO MODS (nome,versione,tipo,link) values ('{mod_name}','{version}','{type}','{link}');
             """
        )
        await ctx.send(f"Mod {mod_name} aggiunta al database")
    else:
        await ctx.send("La mod esiste gia' nel database")

@bot.command()
async def remove_mod(ctx,mod_name):
    if not mod_name:
        await ctx.send('impossibile rimuovere una mod senza nome, controlla la sintassi, specificane uno')
        return
    cursor.execute(f"SELECT nome FROM MODS WHERE nome ='{mod_name}'")
    mod=cursor.fetchone()
    if mod:
        cursor.execute(
            f"""
             DELETE FROM MODS WHERE nome = '{mod_name}';
             """
        )
        await ctx.send("la mod da te selezionata e' stata eliminata")
    else:
        await ctx.send("'la mod da te indicata non esiste,controlla se ci sono errori nel nome'")
"""
@bot.command()
async def edit_mod(ctx,mod_name,new_mod_name,new_version,new_type,new_link):
    if not mod_name :
        await ctx.send("impossibile modificare una mod senza nome, controlla la sintassi, specificane uno")
        return
    cursor.execute(f"SELECT nome FROM MODS WHERE nome = {mod_name}")
    mod=cursor.fetchone()
    if mod:
        query="UPDATE MODS SET "
        if new_mod_name:
            query+=f'nome = {new_mod_name}'
        cursor.execut(
        )
        await ctx.send("la tua mod e' stata modificata")
    else:
        await ctx.send("'la mod da te indicata non esiste,controlla se ci sono errori nel nome'")
"""

@bot.command()
async def show_mods(ctx):
    cursor.execute(
        """
        SELECT * FROM MODS;
        """)
    mods=cursor.fetchall()
    print(mods)
    lista_mods=''
    for mod in mods:
        ext_mod=" ".join(mod)
        lista_mods+=f'\n{ext_mod}'
    await ctx.send(f'{lista_mods}')

@bot.command()
async def show_users(ctx):
    cursor.execute( 
        """ 
        select * from USER;
        """)
    utenti=cursor.fetchall()
    print(utenti)
    lista_nomi = "\n".join(u[0] for u in utenti)
    await ctx.send(f"**Utenti nel database:**\n{lista_nomi}")
    

bot.run(token=TOKEN,log_handler=handler,log_level=logging.DEBUG)