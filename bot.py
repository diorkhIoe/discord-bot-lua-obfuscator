from importlib.resources import path
import discord
import requests
import os
import subprocess
import shutil

token = "ODM3MDU4MTE4ODE0NDAwNTUy.GyNFrS.Iy2Khub_VhI2oplFx2wqGoZNDJ98WkYq7e8MGg"
channel_id = 1052077187131510824

intents = discord.Intents.default()
intents.messages = True

bot = discord.Client(intents=intents, guilds=True)

def obfuscation(path, author):
    copy = f"{os.getcwd()}/obfuscated/{author}.lua"

    #removing duplicates
    if os.path.exists(copy):
        os.remove(copy)

    #copying uploaded one to make operations on it
    shutil.copyfile(path, copy)

    #copying obfuscate file to copied one
    text_file = open(f"{os.getcwd()}/obfuscate.lua", "r")
    data = text_file.read()
    text_file.close()
    f = open(copy, "a")
    f.truncate(0)
    f.write(data)
    f.close()

    #writing upload file into obfuscation script
    originalupload = open(path, "r")
    originalupload_data = originalupload.read()
    originalupload.close()

    with open(copy, "r") as in_file:
        buf = in_file.readlines()

    with open(copy, "w") as out_file:
        for line in buf:
            if line == "--SCRIPT\n":
                line = line + originalupload_data + '\n'
            out_file.write(line)

    #executing script and making new file with obfuscated output
    output = subprocess.getoutput(f'lua {copy}')

    if os.path.exists(f"{os.getcwd()}/obfuscated/{author}-obfuscated.lua"):
        os.remove(f"{os.getcwd()}/obfuscated/{author}-obfuscated.lua")

    f = open(f"{os.getcwd()}/obfuscated/{author}-obfuscated.lua", "a")
    f.write(output)
    f.close()

    os.remove(copy)

@bot.event
async def on_ready():
    print(f"{bot.user} is online ✔️")
    await bot.change_presence(status=discord.Status.online, activity=discord.Game(name="yunglean_#4171 lua obfuscator"))

@bot.event
async def on_message(message):
    channel = str(message.channel)
    author=str(message.author)
    channel = bot.get_channel(channel_id)

    try:
        url = message.attachments[0].url
        if not message.author.bot:
            if message.channel.id == channel_id:
                if message.attachments[0].url:
                    if '.lua' not in url:
                        embed=discord.Embed(title=f"***Wrong file extension!***", description=f"only ``.lua`` allowed", color=0xFF3357)
                        message = await channel.send(embed=embed)
                    else:
                        uploads_dir = f"{os.getcwd()}/uploads"
                        obfuscated_dir = f"{os.getcwd()}/obfuscated"

                        if not os.path.exists(uploads_dir):
                            os.makedirs(uploads_dir)
                        if not os.path.exists(obfuscated_dir):
                            os.makedirs(obfuscated_dir)
                            
                        print(f'\nNew lua script received from {author}.')
                        print(f'Attachment Link: {message.attachments[0].url}\n')
                        response = requests.get(url)
                        path = f"{os.getcwd()}/uploads/{author}.lua"

                        if os.path.exists(path):
                            os.remove(path)

                        open(path, "wb").write(response.content)
                        obfuscation(path, author)
                        embed=discord.Embed(title="File has been obfuscated", color=0x3357FF)
                        await channel.send(embed=embed, file=discord.File(f"{os.getcwd()}/obfuscated/{author}-obfuscated.lua"))
    except:
        pass

bot.run(token)
