from client import client
from modules import _common
import discord
import esix

cmd_name = "tag"

client.basic_help(title=cmd_name, desc="Creates a screenshot of an e621 tag")

detailed_help = {
        "Usage": f"`{client.default_prefix}{cmd_name} <tag>`",
        "Arguments": "`tag` - tag to be searched",
        "Description": "This command creates a screenshot of an e621 tag"
}
client.long_help(cmd=cmd_name, mapping=detailed_help)

def get_tag_by_name(name):
        url = f"{esix.config.BASE_URL}tag/index.json?name={name}"
        rs = esix.api._fetch_data(url)
        if len(rs) == 0:
                return None
        else:
                return esix.tag.Tag(tag_data=rs[0])

@client.command(trigger=cmd_name)
async def tag(command: str, message: discord.Message):
        name = command.lower()[4:]
        if name == "":
                # No tag provided
                await message.channel.send("You must provide a tag to be shown")                  
                return

        tag = get_tag_by_name(name)
        if tag is not None:
                subprocess.call(["./createtag.sh", name, tag.type_str.upper(), str(tag.count)])
                f = open('tag.png', 'r')
                await message.channel.send(file=discord.File(f))
        else:
                await message.channel.send("No such tag")
