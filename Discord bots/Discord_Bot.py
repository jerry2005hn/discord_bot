import discord
from discord.ext import commands, tasks
import random
from itertools import cycle
import os
import asyncio
import json
def get_server_prefix(client,message):
    with open("prefixes.json","r") as f:
        prefix = json.load(f)
    return prefix[str(message.guild.id)]

client=commands.Bot(command_prefix=get_server_prefix,intents=discord.Intents.all())

bot_status=cycle(["type !help for help","type !ping for bot latency","Status Three","Status Four"])

@tasks.loop(seconds=10)
async def change_status():
    await client.change_presence(activity=discord.Game(next(bot_status)))
@client.event
async def on_ready():
    await client.tree.sync()
    print("Success: Bot is connected to Discord")
    change_status.start()

@client.tree.command(name="ping",description="Show the bot's latency in ms.") #slash commands
async def ping(interaction: discord.Interaction):
    bot_latency=round(client.latency*1000)
    await interaction.response.send_message(f"Pong! {bot_latency} ms.")
@client.event
async def on_guild_join(guild):
    with open("cogs/jsonfiles/prefixes.json","r") as f:
        prefix=json.load(f)
    prefix[str(guild.id)]="!"
    with open("cogs/jsonfiles/prefixes.json","w") as f:
        json.dump(prefix,f,indent=4)
@client.event
async def on_guild_join(guild):
    with open("cogs/jsonfiles/mutes.json","r") as f:
        mute_role=json.load(f)
        mute_role[str(guild.id)]=None
    with open("cogs/jsonfiles/mutes.json","w") as f:
        json.dump(mute_role,f,indent=4)
@client.event
async def on_guild_remove(guild):
    with open("cogs/jsonfiles/prefixes.json","r") as f:
        prefix=json.load(f)
    prefix.pop(str(guild.id))
    with open("cogs/jsonfiles/prefixes.json","w") as f:
        json.dump(prefix,f,indent=4)
@client.event
async def on_guild_remove(guild):
    with open("cogs/jsonfiles/mutes.json","r") as f:
        mute_role=json.load(f)
        mute_role.pop(str(guild.id))
    with open("cogs/jsonfiles/mutes.json","w") as f:
        json.dump(mute_role,f,indent=4)

@client.command()
async def setprefix(ctx,*,newprefix: str):
    with open("prefixes.json","r") as f:
        prefix=json.load(f)
    prefix[str(ctx.guild.id)]=newprefix
    with open("prefixes.json","w") as f:
        json.dump(prefix,f,indent=4)

async def load():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await client.load_extension(f"cogs.{filename[:-3]}")
            print(f"{filename[:-3]} is loaded!")
async def main():
    async with client:
        await load()
        await client.start("bot token") #use actual bot token when execute
@client.event
async def on_guild_join(guild):
    with open("cogs/jsonfiles/autorole.json","r") as f:
        auto_role=json.load(f)
    auto_role[str(guild.id)]=None
    with open("cogs/jsonfiles/autorole.json","w") as f:
        json.dump(auto_role,f,indent=4)

@client.event
async def on_guild_remove(guild):
    with open("cogs/jsonfiles/autorole.json","r") as f:
        auto_role=json.load(f)
    auto_role.pop(str(guild.id))
    with open("cogs/jsonfiles/autorole.json","w") as f:
        json.dump(auto_role,f,indent=4)
asyncio.run(main())



