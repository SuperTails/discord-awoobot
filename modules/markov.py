from client import client
from modules import _common
import markovify
import discord

cmd_name = "markov"

client.basic_help(title=cmd_name, desc="creates a message from a markov chain based on previous messages in a channel")

detailed_help = {
	"Usage": f"`{client.default_prefix}{cmd_name} [mention]`",
	"args": "`id` - (optional) channel mention to generate markov chain from",
	"desc": "This command creates a message based on a markov chain generated from recent messages in the channel or from a channel mention passed as an argument.",
}
client.long_help(cmd=cmd_name, mapping=detailed_help)


@client.command(trigger=cmd_name,
				aliases=[])  # aliases is a list of strs of other triggers for the command
async def markov(command: str, message: discord.Message):
	command = command.split(" ")
	try:
		command[1]
	except IndexError:
		c = message.channel
	else:
		try:
			c = client.get_channel(_common.stripMentionsToID(command[1]))
			if c is None:
				await message.channel.send("Unknown channel - I may not be in that channel's server")
		except ValueError:
			await message.channel.send("First argument to command `markov` must be a channel mention")
			return

	async with message.channel.typing():
		msg_hist = await c.history(limit=3000).flatten()
		msg_hist_content = [x.clean_content for x in msg_hist]
		src_str = "\n".join(msg_hist_content)
		model = markovify.NewlineText(src_str)
		for _ in range(10):
			ret = model.make_short_sentence(500)
			if ret is not None:
				break
		else:
			ret = "<Error: For some reason the chain did not generate an acceptable sentence. Please rerun the command.>"
	await message.channel.send(ret)
	return
