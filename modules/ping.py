from client import client
import discord

cmd_name = "ping"

client.basic_help(title=cmd_name, desc="shows the bot's latency to the Discord API endpoint")

detailed_help = {
	"Usage": f"{client.default_prefix}{cmd_name}",
	"Arguments": "None",
	"Description": "Returns the bot's latency to the Discord endpoint (implicitly telling you your connection is working).",
}
client.long_help(cmd=cmd_name, mapping=detailed_help)


@client.command(trigger=cmd_name)
async def ping(command: str, message: discord.Message):
	await message.channel.send(f"Latency from bot to Discord endpoint (ms): `{client.latency*1000:.2f}`")
	return
