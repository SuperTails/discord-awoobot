from client import client
from modules import _common
import discord
import esix

cmd_name = "search"

client.basic_help(title=cmd_name, desc="Finds a post on e621 matching the given ")

detailed_help = {
	"Usage": f"`{client.default_prefix}{cmd_name} <query>`",
        "Arguments": "`query` - Query to be searched, e.g. 'rating:safe fox'",
	"Description": "This command finds a post on e621 matching the given query",
}
client.long_help(cmd=cmd_name, mapping=detailed_help)


@client.command(trigger=cmd_name)  # aliases is a list of strs of other triggers for the command
async def search(command: str, message: discord.Message):
        query = command.lower()[7:]
        if query == "":
                await message.channel.send("No search terms provided")
                return


        results = list(esix.post.search(query, 1))
        if len(results) == 0:
                await message.channel.send("No posts found")
        else:
                post = results[0]
                await message.channel.send(f"<{post.url}>")
                await message.channel.send(f"Tags: {post.tags}")
