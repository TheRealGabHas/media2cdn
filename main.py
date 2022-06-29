import discord
import re

client = discord.Client()
video_extension = ['mp4', 'mov']


@client.event
async def on_ready():
    print('[v] Online')
    server: int = len(client.guilds)
    await client.change_presence(activity=discord.Game(f"Convert media to cdn | {server} servers"))


def contained_url(content: str) -> list:
    link_filter: str = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>" \
                       r"]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
    url_list: list = re.findall(link_filter, content)
    final: list = []
    # Clear the empty strings in the tuples that are inside the list
    for data_tuple in url_list:
        for item in data_tuple:
            if not item == '':
                final.append(item)
    return final


def scan(url: str) -> bool:
    if url.startswith('https://media.discordapp.net'):
        for item in video_extension:
            if url.endswith(item):
                return True
        return False


@client.event
async def on_guild_join():
    server: int = len(client.guilds)
    await client.change_presence(activity=discord.Game(f"Convert media to cdn | {server} servers"))


@client.event
async def on_message(msg):
    if not msg.author.id == 984914381647269898:
        all_url: list = contained_url(msg.content)
        invalid: list = []
        for link in all_url:
            if scan(link):
                invalid.append(link.replace('https://media.discordapp.net', 'https://cdn.discordapp.com'))

        embed = discord.Embed(color=0xf04242)
        embed.set_author(
            name=f"📝 Invalid URL\n> {msg.author.name}#{msg.author.discriminator} just sent an invalid URL "
                 f"video. Here is the new one :")

        for link in invalid:
            await msg.channel.send(embed=embed)
            await msg.channel.send(f'**Oops!** <@{msg.author.id}> attempted to use invalid url. Here is the new one :'
                                   f'\n{link}')
            # I don't send the embed with the message because it will appear under the text and that's not what I expect
            # But you can change this to : msg.channel.send("...", embed=embed)

client.run('TOKEN')
