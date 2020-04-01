
# Code by Cypooos and AngelOverflow - Twitter: @cypooos @XXX - Disursif 2020

# /----------------------
# | Importation
# \----------------------

import sys, os
import com
Log = com.Log

import asyncio, discord
CLIENT = discord.Client()

def echo(*arg):
  print(*arg)
  sys.stdout.flush()

import security
Security = security.Security(CLIENT)

import DiscordCommandLineGenerator
CommandLine = DiscordCommandLineGenerator.CommandLine(CLIENT,Security)


CONFIGURATION = {
  "LogChannel":694996836536025249,
	"consoleChan":694996263241777233
}




# /----------------------
# | Commands of bot
# \----------------------

# ---- COMMAND'S COMMAND ---
async def delete(messages,time):
  await asyncio.sleep(time)
  for message in messages:
    await message.delete()




# ---- General commands ----


# ---- DEBUGS COMMAND ----
@Security.roleNeeded(["botmoderator"])
@CommandLine.addFunction()
async def evaluate(commands:max,**kwargs) -> "eval *PYTHON":
  """Execute du code python.
Execute du code python.
**A éviter !** une fausse manip pourrais casser le bot ou détruire des données.
**IL N'Y A PAS DE RETOUR EN ARRIERE POSSIBLE**
Prévenir <@349114853333663746> en cas de problème."""
  try:
    ret = eval(commands)
  except:
    ret = sys.exc_info()[0]
  return "__Return:__\n```python\n"+str(ret)+"```\n"


@Security.roleNeeded(["botmoderator","admin"])
@CommandLine.addFunction()
async def ping(**kwargs) -> "ping":
  """Répond `pong !`
Répond `pong !`"""
  await CommandLine.message.channel.send("Pong !")



# ---- ADMINS COMMANDS ----
@Security.roleNeeded(["botmoderator","admin"])
@CommandLine.addFunction()
async def stop(**kwargs) -> "stop":
  """Arrête le bot.
A utilliser en cas d'urgence: spam, crash, ou incontrollable.
Prévenir <@349114853333663746> en cas de problème."""
  await CommandLine.message.channel.send("Bye !")
  quit()


@Security.roleNeeded(["botmoderator","admin"])
@CommandLine.addFunction()
async def deleteCmd(nbMsg:(int,1),**kwargs) -> "delete [INT]":
  """Supprimme X messages.
Ne rien indiqué surprimme le dernier message. Nous ne comptons pas la commande dans le nombre de messages."""
  try: nbMsg = int(nbMsg)
  except ValueError: raise AssertionError("Le paramètre doit etre un entier.")
  nbMsg += 1
  async for message in CommandLine.message.channel.history(limit=int(nbMsg)):
    await message.delete()




# ---- HELP COMMAND ----
@CommandLine.addFunction()
async def help(info:(str,""),**kwargs) -> "help [COMMANDE]":
  '''Affiche l'aide d'une commande.
Affiche de l'aide sur une commande, ou sur les commandes en général si aucune n'est précisé.
Les aides sont détaillé au possible, en utillisant la syntaxe usuele.'''
  HELP_AUTH = ["botmoderator","admin","modérateur"]
  message = CommandLine.message
  if info == "":
    embed_cmdUti=discord.Embed(title="__Liste des commandes utilisateurs__", color=0x80ffff)
    
    embed_cmdUti.add_field(name="Nom", value="\n".join(["`"+fct.__name__.split(" ")[0]+"`" for fct in CommandLine.funct if fct.authGroup == None]), inline=True)
    embed_cmdUti.add_field(name="Description", value="\n".join([fct.__doc__.split("\n")[0] for fct in CommandLine.funct if fct.authGroup == None]), inline=True)
    embed_cmdUti.set_footer(text="Ce message d'aide ce détruira au bout de 30 secondes.")

    embed_cmdAdm=discord.Embed(title="__Liste des commandes administrateurs__", color=0xfb0013)

    embed_cmdAdm.add_field(name="Nom", value="\n".join(["`"+fct.__name__.split(" ")[0]+"`" for fct in CommandLine.funct if fct.authGroup != None]), inline=True)
    embed_cmdAdm.add_field(name="Description", value="\n".join([fct.__doc__.split("\n")[0] for fct in CommandLine.funct if fct.authGroup != None]), inline=True)

    embed_cmdUti.set_thumbnail(url="https://media3.giphy.com/media/B7o99rIuystY4/source.gif")
    embed_cmdAdm.set_thumbnail(url="https://media3.giphy.com/media/B7o99rIuystY4/source.gif")
    embed_cmdAdm.set_footer(text="Le bot du jeu Hackable a été créé par Cyprien Bourotte.")
    to_destroy = []
    to_destroy.append(await message.channel.send("Je t'incite à faire `help COMMANDE` pour plus d'infos, ou encore `help cmd` pour des informations complémentaire",embed=embed_cmdUti))
    # test admin
    for x in HELP_AUTH:
      if x.lower() in [y.name.lower() for y in CommandLine.message.author.roles]:
        to_destroy.append(await message.channel.send("",embed=embed_cmdAdm))
    asyncio.get_running_loop().run_in_executor(None, await delete(to_destroy,30))
    return 

  for funct in CommandLine.funct:
    if funct.__name__.split(" ")[0] == info:
      if Security.canBeUse(funct,message.author):
        # HELP FUNCTION
        embed=discord.Embed(title="Commande : "+funct.__name__.split(" ")[0], description=str("\n".join(funct.__doc__.split("\n")[1:])), color=0x80ffff)
        embed.set_footer(text="Ce message d'aide ce détruira au bout de 30 secondes.")
        embed.set_author(name="Aide")
        embed.set_thumbnail(url="https://media1.giphy.com/media/IQ47VvDzlzx9S/giphy.gif")
        embed.add_field(name="Syntaxe :", value="`"+funct.__name__+"`", inline=False)
        t = funct.authGroup
        if isinstance(t,str): t = [t]
        if funct.authGroup != None: embed.set_footer(text="Cette commande n'est utilisable seulement avec le role "+str(" ou ".join(t).lower()))
        to_destroy = await message.channel.send(embed=embed)
        asyncio.get_running_loop().run_in_executor(None, await delete([to_destroy],30))
        return 
      else:
        # DONT ALLOW
        Security.send_warn("Vous n'avez pas accès à cette commande.","Cette commande n'est utilisable seulement avec le role "+str(" ou ".join(funct.authGroup).lower(),CommandLine.message))
        return
  return "Commande pour l'aide inconnue.\nTapez `help` pour la liste des commandes.\n"



# /----------------------
# | Bot
# \----------------------



@CLIENT.event
async def on_message(message):
  if message.author.id != CLIENT.user.id: await Log.message("`<@!"+str(message.author.id)+">` - "+message.content)
  else: return

  if message.channel.id == CONFIGURATION["consoleChan"]:
    message.content = message.content[1:]
    if not await Security.checkCommand(message):return # SECURITY
    ret = await CommandLine.execute(message)
    if ret != None and ret != "": await message.channel.send(ret)
  


@CLIENT.event
async def on_ready():
  Log.channel = CLIENT.get_channel(CONFIGURATION["LogChannel"])
  await Log.info("Username: "+CLIENT.user.name+";    ID: "+str(CLIENT.user.id))


# /----------------------
# | Start
# \----------------------


try:
  token = os.environ['TOKEN']
except KeyError:
  # Not on server
  echo("Exit because TOKEN not found")
  exit()

echo("TOKEN:",token)

CLIENT.run(token)
# if this sentence is modified, it just mean that I need to update the code for refresh the bot on Heraku server.