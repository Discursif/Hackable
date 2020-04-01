# Bot discord

#INFORMATION FOR THE BOT :
# Name : Organisateur
# Client Id : 692710615332159613
# Client secret : JgLYrLCyjJ5MvZPagOZcRXUXTLSYOMTY
# Token : NjkyNzEwNjE1MzMyMTU5NjEz.XnygRw.U_jlqG1beuIqblh6Xyt20xY_1pQ
# Permission Integer : 522304

import discord, time
# --> ça sert à rien pour l'instant : from discord.ext import commands


token = 'NjkyNzEwNjE1MzMyMTU5NjEz.XnygRw.U_jlqG1beuIqblh6Xyt20xY_1pQ' #Token du bot
client = discord.Client() # crée un objet client
#bot = commands.Bot(command_prefix='@')  #les @bot.command commence avec @
channel_terminal = client.get_channel(693493289332244480) # Chanel terminal


@client.event
async def on_ready(): # Ne pas changer 
    print('We have logged in as {0.user}'.format(client))


#error = ('Type of ERROR', 'Message error', message.author.display_name)
@client.event
async def on_message(message): # Ne pas changer
  if message.author==client.user:return # Don't check bots messages
  channel_terminal = client.get_channel(693493289332244480) # Chanel terminal

  ##########################################################
  ####             Functions used after                 ####
  ##########################################################  
 
  def get_liste_hackers():
    liste_hackers=[]
    for member in channel_terminal.members:
        for role in member.roles:
            if role.name == "Hacker":liste_hackers.append(str(member)) 
    return liste_hackers  
  
  def download_decode_animation(name_animation,nb_fct_called):
      nb_htag,nb_points=x,20-x
      download_or_decode_bar=nb_htag*'#'+nb_points*'.' 
      message_animation=name_animation+' ['+download_or_decode_bar+'] '+str(x*5)+'%'
      return message_animation
    

  ##########################################################
  ###########  Message in the terminal channel   ###########
  ###########               /!\                  ###########
  ##########################################################  
   
  if message.channel==channel_terminal:

    ##########################################################
    ####         Get informations in the terminal         ####
    ##########################################################


    if message.content=='$get hackers.server':
        liste_hackers=get_liste_hackers()
        response='File : \nHackers on the server : '
        for x in liste_hackers:
            response=response+x+' ; '
        if response == '':await channel_terminal.send('No hackers on the server')
        else:
            message_download,message_decode='Download File : [....................] 0%','Decode File : [....................] 0%'
            message_download_discord = await channel_terminal.send(message_download)
            await channel_terminal.set_permissions(message.author, read_messages=True, send_messages=False)
            for x in range(0, 21):
                await message_download_discord.edit(content=download_decode_animation('Download File : ',x))
                time.sleep(0.03)
            await channel_terminal.send('Download succeded')
            message_decode_discord = await channel_terminal.send(message_decode)
            for x in range(0,21):
                await message_decode_discord.edit(content=download_decode_animation('Decode File : ',x))
                time.sleep(0.03)
            await channel_terminal.send('Decode succeded')
            await channel_terminal.send(response[:-2])
            await channel_terminal.set_permissions(message.author, read_messages=True, send_messages=True)


    ##########################################################
    ####           Hack someone on the terminal           ####
    ##########################################################

    #random hack
    #target hack

    elif message.content[0]!='$':
        error=('SYNTAXE', 'Missing first character : $', message.author.display_name)
        message_error='------------------------------------------------------------\nERROR '+error[0]+' from : '+error[2]+'\nMessage : '+message.content+'\nError message : '+error[1]+'\n------------------------------------------------------------\n'
        await channel_terminal.send(message_error)
        await message.delete()


client.run(token)