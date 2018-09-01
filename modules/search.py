from client import client
from modules import _common
import discord
import esix

cmd_name = "search"

client.basic_help(title=cmd_name, desc="finds a post on e621 matching the given tags")

detailed_help = {
	"Usage": f"`{client.default_prefix}{cmd_name} [mention]`",
	"args": "`tags` - tags to search",
	"desc": "This command finds a post on e621 matching the given tags",
}
client.long_help(cmd=cmd_name, mapping=detailed_help)


@client.command(trigger=cmd_name,
				aliases=[])  # aliases is a list of strs of other triggers for the command
async def search(command: str, message: discord.Message):
        if command.lower().startswith("search "):
                tags = command.lower()[7:]
                post = esix.post.search(tags, 1)[0]
                await message.channel.send("<" + post.url + ">")
                await message.channel.send("Tags: " + str(post.tags))
        else:
                await message.channel.send("You must provide some tags to be searched")
