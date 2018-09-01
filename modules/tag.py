from client import client
from modules import _common
import discord
import esix

cmd_name = "tag"

client.basic_help(title=cmd_name, desc="creates a screenshot of an e621 tag")

detailed_help = {
        "Usage": f"`{client.default_prefix}{cmd_name} [mention]`",
        "args": "`tag` - tag to be searched",
        "desc": "This command creates a screenshot of an e621 tag"
}
client.long_help(cmd=cmd_name, mapping=detailed_help)

def get_tag_by_name(name):
    url = esix.config.BASE_URL + 'tag/index.json?name=' + name
    result = 0
    rs = esix.api._fetch_data(url)
    result += len(rs)
    return esix.tag.Tag(tag_data=rs[0])

@client.command(trigger=cmd_name,
                                aliases=[])
async def tag(command: str, message: discord.Message):
        if command.lower().startswith("tag "):
                name = command.lower()[4:]
                tag = get_tag_by_name(name)
                if (tag != None):
                    subprocess.call(["./createtag.sh", name, tag.type_str.upper(), str(tag.count)])
                    f = open('tag.png', 'r')
                    await message.channel.send(file=discord.File(f))
        else:
                await message.channel.send("You must provide a tag to be shown")                  
